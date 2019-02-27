import pxml
import glob
import json

# https://stackoverflow.com/a/8230505/763231
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
           return list(obj)
       return json.JSONEncoder.default(self, obj)

def prettyDump(obj):
    print json.dumps(obj, sort_keys=True, indent=4, cls=SetEncoder)

# Documentation for PXML can be found at - https://docs.palantir.com/gotham/all/index.html#../Subsystems/gotham/Content/xml/pXMLFormatOverview.htm
# No matter how complicated the XML looks, it will always have this structure:
# An element called 'graph' that contains these elements (these elements may be empty, i.e. if there are no links)
#       aclSet
#       dataSourceSet
#       objectSet
#       linkSet
def parse(xmlFile, index, totalFiles):
    print "Processing %s / %s (%s)..." % (index, totalFiles, xmlFile)

    try:
        root = pxml.parse(xmlFile, True)
    except UnicodeEncodeError:
        failures.append(xmlFile)
        return

    # get the data sources
    # print "Data Sources:"
    # for dataSource in root.graph.dataSourceSet.dataSource:
    #     name = dataSource.name
    #     description = dataSource.description
    #     print "\tname=%s" % name
    #     print "\tdescription=%s" % description
    #     print

    # get the objects, properties and media (saved as a separate file)
    # print "Objects:"

    # index all objects by their ID for working with links if we want to
    # later on
    objects = {}

    if root.graph.objectSet is not None:
        for object in root.graph.objectSet.object:
            objectType = object.type_
            # print "\t%s" % objectType

            if objectType not in objectTypes:
                objectTypes[objectType] = set()

            if object.propertySet is not None:
                # print "\tProperties..."
                for property in object.propertySet.property:
                    propertyType = property.type_
                    # print "\t\t%s: %s" % (property.type_, property.propertyValue.propertyData)

                    objectTypes[objectType].add(propertyType)

            # Create a media/ folder in the same directory as this script if you want to capture attachments
            if object.mediaSet is not None:
                objectTypesWithMedia.add(objectType)

                # for media in object.mediaSet.media:
                #     title = media.id
                #     # Could use media.mediaTitle, but that hits encoding issues with Arabic
                #     data = media.mediaData

                #     mediaFile = open('media/' + title, 'wb')
                #     mediaFile.write(data)
                #     mediaFile.close()

            # this will just be an easy way to reference a linked object later if we want to
            objects[object.id] = object

    if root.graph.linkSet is not None:
        for link in root.graph.linkSet.link:
            # look up the object by this ID in the objects hash for more information about the object itself
            # print "%s is the parent of %s" % (link.parentRef, link.childRef)

            parentType = objects[link.parentRef].type_ if objects[link.parentRef] is not None else None
            childType = objects[link.childRef].type_ if objects[link.childRef] is not None else None
            linkType = str(parentType) + " -[" + link.type_.replace("com.palantir.link.", "") + "]-> " + str(childType)
            linkTypes.add(linkType)

####################################################################################################

# Parsing metadata.
failures = []

# Metadata for the schema.
objectTypes = {}
objectTypesWithMedia = set()
linkTypes = set()

# this will give us a list of all xml files in the data directory
files = glob.glob('./baseRealmDump/9/9/9/*.xml')
totalFiles = len(files)
index = 1

for xml in files:
    parse(xml, index, totalFiles)
    index += 1

print "\nObject types (with properties):"
prettyDump(objectTypes)

print "\nObject types (raw):"
prettyDump(objectTypes.keys())

print "\nObject types containing media:"
prettyDump(objectTypesWithMedia)

print "\nLinks:"
prettyDump(linkTypes)

print "\nFailures (probably contain non-ASCII for dataSource names):"
prettyDump(failures)
