import pxml
import glob
import json
import sys

# https://stackoverflow.com/a/8230505/763231
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
           return sorted(list(obj))
       return json.JSONEncoder.default(self, obj)

def prettyDump(obj):
    sortedObj = sorted(obj) if (isinstance(obj, set) or isinstance(obj, list)) else obj
    print json.dumps(sortedObj, sort_keys=True, indent=4, cls=SetEncoder)

def getComplexity(property):
    value = property.propertyValue
    return "single" if value.propertyData is not None \
        else "interval" if value.propertyTimeInterval is not None \
        else getMultiComplexity(value) if value.propertyComponent is not None \
        else "unknown"

def getMultiComplexity(value):
    components = value.propertyComponent
    return str(map(lambda x: x.type_, components))

# Documentation for PXML can be found at - https://docs.palantir.com/gotham/all/index.html#../Subsystems/gotham/Content/xml/pXMLFormatOverview.htm
# No matter how complicated the XML looks, it will always have this structure:
# An element called 'graph' that contains these elements (these elements may be empty, i.e. if there are no links)
#       aclSet
#       dataSourceSet
#       objectSet
#       linkSet
def parseObjects(xmlFile, index, totalFiles):
    # Output to stderr so it's visible even when redirecting to file.
    print >> sys.stderr, "Processing object %s / %s (%s)..." % (index, totalFiles, xmlFile)

    try:
        root = pxml.parse(xmlFile, True)
        parsedDocs[xmlFile] = root
    except:
        parseFailures.add(xmlFile)
        return

    if root.graph.objectSet is not None:
        for object in root.graph.objectSet.object:
            objectType = object.type_.replace("com.palantir.object.", "")
            # print "\t%s" % objectType

            if objectType == "abstract":
                continue

            if objectType not in objectTypes:
                objectTypes[objectType] = set()

            if object.propertySet is not None:
                # print "\tProperties..."
                for property in object.propertySet.property:
                    propertyType = property.type_.replace("com.palantir.property.", "")
                    # print "\t\t%s: %s" % (property.type_, property.propertyValue.propertyData)

                    complexity = getComplexity(property)

                    propertyString = propertyType + " (" + complexity + ")"
                    objectTypes[objectType].add(propertyString)

            # Create a media/ folder in the same directory as this script if you want to capture attachments
            if object.mediaSet is not None:
                for media in object.mediaSet.media:
                    try:
                        title = media.mediaTitle.encode("utf-8")
                    except:
                        # Possible encoding issue with arabic (according to original author).
                        title = media.id

                    data = media.mediaData

                    mediaFile = open('media/' + title, 'wb')
                    mediaFile.write(data)
                    mediaFile.close()

            # this will just be an easy way to reference a linked object later if we want to
            objects[object.id] = object

def parseLinks(xmlFile, index, totalFiles):
    print "Processing link %s / %s (%s)..." % (index, totalFiles, xmlFile)

    try:
        root = parsedDocs[xmlFile]
    except:
        parseFailures.add(xmlFile)
        return

    if root.graph.linkSet is not None:
        for link in root.graph.linkSet.link:
            # look up the object by this ID in the objects hash for more information about the object itself
            # print "%s is the parent of %s" % (link.parentRef, link.childRef)
            try:
                parentType = objects[link.parentRef].type_.replace("com.palantir.object.", "")
                childType = objects[link.childRef].type_.replace("com.palantir.object.", "")
            except:
                linkFailures.add(xmlFile)
                continue

            linkType = parentType + " -[" + link.type_.replace("com.palantir.link.", "") + "]-> " + childType
            linkTypes.add(linkType)

####################################################################################################

# Parsing metadata.
parsedDocs = {}
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

print "\nObject types (raw):"
prettyDump(objectTypes.keys())

print "\nLinks:"
prettyDump(linkTypes)

print "\nParse failures (unknown cause):"
prettyDump(parseFailures)

print "\nLink failures (probably exist in a file that wasn't included):"
prettyDump(linkFailures)
