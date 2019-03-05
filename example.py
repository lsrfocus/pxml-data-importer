# Documentation for PXML can be found at - https://docs.palantir.com/gotham/all/index.html#../Subsystems/gotham/Content/xml/pXMLFormatOverview.htm
# No matter how complicated the XML looks, it will always have this structure:
# An element called 'graph' that contains these elements (these elements may be empty, i.e. if there are no links)
#       aclSet
#       dataSourceSet
#       objectSet
#       linkSet

import pxml
import glob
import json
import sys
import datetime
import pytz
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pwd"))

def addObject(tx, objectType, id, props, media):
    print "Saving " + objectType + " # " + id
    print "  props: " + str(props)
    print "  media: " + str(media)
    tx.run("MERGE (o:" + objectType + " {_id: $id}) SET o += $props", id=id, props=props)

# https://stackoverflow.com/a/8230505/763231
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
           return sorted(list(obj))
       return json.JSONEncoder.default(self, obj)

def prettyDump(obj):
    sortedObj = sorted(obj) if (isinstance(obj, set) or isinstance(obj, list)) else obj
    print json.dumps(sortedObj, sort_keys=True, indent=4, cls=SetEncoder)

epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)

# https://stackoverflow.com/a/11111177/763231
def toEpochMs(dt):
    return int((dt - epoch).total_seconds() * 1000)

def getSimpleComplexity(value):
    return "data" if value.propertyData is not None \
        else "raw" if value.propertyRawValue is not None \
        else "unparsed" if value.propertyUnparsedValue is not None \
        else "interval" if value.propertyTimeInterval is not None \
        else "multi" if value.propertyComponent is not None \
        else "unknown"

def parseProperty(property):
    value = property.propertyValue
    simpleComplexity = getSimpleComplexity(value)
    multiComplexity = getMultiComplexity(value) if simpleComplexity is "multi" else None

    if simpleComplexity == "interval":
        # Discard propertyTimeInterval because it always has either timestamp or timeInterval in addition
        # (which are more precise). This is verified by the assertions below.
        simpleComplexity = "DISCARD"

        if value.propertyTimeInterval.timeStart is not None or value.propertyTimeInterval.timeEnd is not None:
            if property.timestamp is None and property.timeInterval is None:
                print "WARN: Found propertyTimeInterval without associated extraProps"
                exit()

        if property.timestamp is not None:
            if not value.propertyTimeInterval.timeStart == value.propertyTimeInterval.timeEnd:
                print "WARN: Timestamp has duration"
                exit()

            if not value.propertyTimeInterval.timeStart == property.timestamp.timestamp:
                print "WARN: propertyTimeInterval != property.timestamp"
                exit()

        if property.timeInterval is not None:
            if value.propertyTimeInterval.timeStart == value.propertyTimeInterval.timeEnd:
                print "WARN: Interval has no duration"
                exit()

            if (not value.propertyTimeInterval.timeStart == property.timeInterval.timeStart) \
                    or (not value.propertyTimeInterval.timeEnd == property.timeInterval.timeEnd):
                print "WARN: propertyTimeInterval != property.timeInterval"
                exit()

    # After grepping the whole dataset, these 3 are the only additional attributes used.
    # See pxml.py#property class for all the other possibilities.
    extraProps = {}
    if property.timestamp is not None:
        extraProps["timestamp"] = toEpochMs(property.timestamp.timestamp)
    if property.timeInterval is not None:
        extraProps["start"] = toEpochMs(property.timeInterval.timeStart)
        extraProps["end"] = toEpochMs(property.timeInterval.timeEnd)
    if property.gisData is not None:
        extraProps["lat"] = property.gisData.point.latitude
        extraProps["long"] = property.gisData.point.longitude

    extraKeys = extraProps.keys()
    numExtras = len(extraKeys)

    if simpleComplexity is "DISCARD" and numExtras is 0:
        return [None, None]

    # Get the simple value, if any.
    parsedValue = value.propertyData.encode("utf-8") if simpleComplexity is "data" \
        else value.propertyRawValue.valueOf_.encode("utf-8") if simpleComplexity is "raw" \
        else value.propertyUnparsedValue.valueOf_.encode("utf-8") if simpleComplexity is "unparsed" \
        else multiComplexity if simpleComplexity is "multi" \
        else None

    # Add extras if there are any.
    if numExtras > 0:
        parsedValue = parsedValue if multiComplexity is not None \
            else {"data": parsedValue} if parsedValue is not None \
            else {}

        parsedValue.update(extraProps)

    complexity = str(multiComplexity.keys()) if multiComplexity is not None else simpleComplexity
    extrasStr = " + " + " + ".join(extraKeys) if numExtras > 0 else ""
    return [
        (complexity + extrasStr).replace("DISCARD + ", ""),
        str(parsedValue)
    ]

def getMultiComplexity(value):
    components = value.propertyComponent

    if len(components) == 0:
        print "WARN: No components"
        exit()

    complexity = {}

    for component in components:
        if component.propertyData is None:
            # Make sure we don't need to parse any other data types.
            print "WARN: No propertyData for multi-part property"
            exit()

        complexity[component.type_] = component.propertyData.encode("utf-8")

    return complexity

def initParse(parseType, xmlFile, index, totalFiles):
    # Output to stderr so it's visible even when redirecting to file.
    print >> sys.stderr, "Processing %s %s / %s (%s)..." % (parseType, index, totalFiles, xmlFile)

def parseObjects(xmlFile, index, totalFiles):
    initParse("object", xmlFile, index, totalFiles)

    try:
        root = pxml.parse(xmlFile, True)
    except:
        parseFailures.add(xmlFile)
        return

    # Properties just for this file.
    localPropertyTypes = set()

    # get the data sources
    # print "Data Sources:"
    # for dataSource in root.graph.dataSourceSet.dataSource:
    #     name = dataSource.name
    #     description = dataSource.description

    if root.graph.objectSet is not None:
        for object in root.graph.objectSet.object:
            objectType = object.type_.replace("com.palantir.object.", "")
            # print "\t%s" % objectType

            currProps = {}
            currMedia = []

            if objectType == "abstract":
                continue

            if objectType not in objectTypes:
                objectTypes[objectType] = set()

            if object.propertySet is not None:
                # print "\tProperties..."
                for property in object.propertySet.property:
                    propertyType = property.type_.replace("com.palantir.property.", "")
                    propertyTypeStr = propertyType
                    hasMulti = False
                    # print "\t\t%s: %s" % (property.type_, property.propertyValue.propertyData)

                    if propertyType in localPropertyTypes:
                        # Designate that this property type has multiple instances per object.
                        hasMulti = True

                    [complexity, value] = parseProperty(property)
                    if complexity is None:
                        continue;

                    localPropertyTypes.add(propertyType)

                    if propertyType not in currProps:
                        currProps[propertyType] = []

                    currProps[propertyType].append(value)

                    propertyStringSingle = propertyType + " (" + complexity + ")"
                    propertyStringMulti = propertyType + "* (" + complexity + ")"

                    # Make sure there's exactly one type.
                    if hasMulti:
                        objectTypes[objectType].add(propertyStringMulti)
                        if propertyStringSingle in objectTypes[objectType]:
                            objectTypes[objectType].remove(propertyStringSingle)
                    elif propertyStringMulti not in objectTypes[objectType]:
                        objectTypes[objectType].add(propertyStringSingle)

            if object.mediaSet is not None:
                for media in object.mediaSet.media:
                    title = media.mediaTitle.encode("utf-8")
                    mediaProps = {
                        "_id": media.id,
                        "filename": title,
                        "linkType": media.linkType.replace("com.palantir.link.", ""),
                        "mimeType": media.mimeType,
                    }
                    currMedia.append(mediaProps)

                    # Write to disk.
                    mediaFile = open('media/' + title, 'wb')
                    mediaFile.write(media.mediaData)
                    mediaFile.close()

            # this will just be an easy way to reference a linked object later if we want to
            objects[object.id] = objectType

            with driver.session() as session:
                session.write_transaction(addObject, objectType, object.id, currProps, currMedia)

def parseLinks(xmlFile, index, totalFiles):
    initParse("link", xmlFile, index, totalFiles)

    try:
        root = pxml.parse(xmlFile, True)
    except:
        parseFailures.add(xmlFile)
        return

    if root.graph.linkSet is not None:
        for link in root.graph.linkSet.link:
            # look up the object by this ID in the objects hash for more information about the object itself
            # print "%s is the parent of %s" % (link.parentRef, link.childRef)
            try:
                parentType = objects[link.parentRef]
                childType = objects[link.childRef]
            except:
                linkFailures.add(xmlFile)
                continue

            linkType = parentType + " -[" + link.type_.replace("com.palantir.link.", "") + "]-> " + childType
            linkTypes.add(linkType)

####################################################################################################

# Parsing metadata.
objects = {}
parseFailures = set()
linkFailures = set()

# Metadata for the schema.
objectTypes = {}
linkTypes = set()

# this will give us a list of all xml files in the data directory
files = glob.glob('./baseRealmDump/9/9/9/*.xml')
totalFiles = len(files)

index = 1
for xml in files:
    parseObjects(xml, index, totalFiles)
    index += 1

index = 1
for xml in files:
    parseLinks(xml, index, totalFiles)
    index += 1

print "\nObject types (with properties):"
prettyDump(objectTypes)

print "\nObject types (just the keys):"
prettyDump(objectTypes.keys())

print "\nLinks:"
prettyDump(linkTypes)

print "\nParse failures (unknown cause):"
prettyDump(parseFailures)

print "\nLink failures (probably exist in a file that wasn't included):"
prettyDump(linkFailures)
