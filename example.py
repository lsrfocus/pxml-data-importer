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
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "pwd"))

def addObject(tx, objectType, id, props):
    print "Saving " + objectType + " # " + id + " with props: " + str(props)

    # TODO: Handle `None` = `null`
    # CypherTypeError: Property values can only be of primitive types or arrays thereof
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

def getPropertyValue(property):
    value = property.propertyValue
    simpleComplexity = getSimpleComplexity(value)

    # TODO: Handle interval, multiComplexity.
    return {
        "data": value.propertyData,
        "raw": value.propertyRawValue,
        "unparsed": value.propertyUnparsedValue,
        "interval": 'None',
    }.get(simpleComplexity, 'None')

def getSimpleComplexity(value):
    return "data" if value.propertyData is not None \
        else "raw" if value.propertyRawValue is not None \
        else "unparsed" if value.propertyUnparsedValue is not None \
        else "interval" if value.propertyTimeInterval is not None \
        else getMultiComplexity(value) if value.propertyComponent is not None \
        else "unknown"

def getComplexity(property):
    value = property.propertyValue
    simpleComplexity = getSimpleComplexity(value)

    if simpleComplexity == "interval":
        # Discard propertyTimeInterval because it always has either timestamp or timeInterval instead.
        # This is verified by the assertions below.
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
    extraProps = []
    if property.timestamp is not None:
        extraProps.append("timestamp")
    if property.timeInterval is not None:
        extraProps.append("timeInterval")
    if property.gisData is not None:
        extraProps.append("gisData")

    if simpleComplexity is "DISCARD" and len(extraProps) is 0:
        return None

    extraPropsStr = " + " + " + ".join(extraProps) if len(extraProps) > 0 else ""
    return (simpleComplexity + extraPropsStr).replace("DISCARD + ", "")

def getMultiComplexity(value):
    components = value.propertyComponent
    if len(components) == 0:
        print "WARN: No components"
    return str(map(lambda x: x.type_, components))

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

    if root.graph.objectSet is not None:
        for object in root.graph.objectSet.object:
            objectType = object.type_.replace("com.palantir.object.", "")
            # print "\t%s" % objectType

            currProps = {}

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

                    complexity = getComplexity(property)
                    if complexity is None:
                        continue;

                    localPropertyTypes.add(propertyType)

                    if propertyType not in currProps:
                        currProps[propertyType] = []

                    currProps[propertyType].append(getPropertyValue(property))

                    propertyStringSingle = propertyType + " (" + complexity + ")"
                    propertyStringMulti = propertyType + "* (" + complexity + ")"

                    # Make sure there's exactly one type.
                    if hasMulti:
                        objectTypes[objectType].add(propertyStringMulti)
                        if propertyStringSingle in objectTypes[objectType]:
                            objectTypes[objectType].remove(propertyStringSingle)
                    elif propertyStringMulti not in objectTypes[objectType]:
                        objectTypes[objectType].add(propertyStringSingle)

            # Create a media/ folder in the same directory as this script if you want to capture attachments
            # if object.mediaSet is not None:
            #     for media in object.mediaSet.media:
            #         try:
            #             title = media.mediaTitle.encode("utf-8")
            #         except:
            #             # Possible encoding issue with arabic (according to original author).
            #             title = media.id

            #         data = media.mediaData

            #         mediaFile = open('media/' + title, 'wb')
            #         mediaFile.write(data)
            #         mediaFile.close()

            # this will just be an easy way to reference a linked object later if we want to
            objects[object.id] = objectType

            with driver.session() as session:
                session.write_transaction(addObject, objectType, object.id, currProps)

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
