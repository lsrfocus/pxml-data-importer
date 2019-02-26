import pxml
import glob

# Documentation for PXML can be found at - https://docs.palantir.com/gotham/all/index.html#../Subsystems/gotham/Content/xml/pXMLFormatOverview.htm
# No matter how complicated the XML looks, it will always have this structure:
# An element called 'graph' that contains these elements (these elements may be empty, i.e. if there are no links)
#       aclSet
#       dataSourceSet
#       objectSet
#       linkSet

def parse(xmlFile):
    print "Processing %s" % xmlFile

    root = pxml.parse(xmlFile, True)

    # get the data sources
    # print "Data Sources:"
    # for dataSource in root.graph.dataSourceSet.dataSource:
    #     name = dataSource.name
    #     description = dataSource.description
    #     print "\tname=%s" % name
    #     print "\tdescription=%s" % description
    #     print

    # get the objects, properties and media (saved as a separate file)
    print "Objects:"

    # index all objects by their ID for working with links if we want to
    # later on
    objects = {}

    if root.graph.objectSet is not None:
        for object in root.graph.objectSet.object:
            print "\t%s" % object.type_

            if object.propertySet is not None:
                print "\tProperties:"
                for property in object.propertySet.property:
                    print "\t\t%s: %s" % (property.type_, property.propertyValue.propertyData)

            # Create a media/ folder in the same directory as this script if you want to capture attachments
            if object.mediaSet is not None:
                for media in object.mediaSet.media:
                    title = media.id
                    # Could use media.mediaTitle, but that hits encoding issues with Arabic
                    data = media.mediaData

                    mediaFile = open('media/' + title, 'wb')
                    mediaFile.write(data)
                    mediaFile.close()

            # this will just be an easy way to reference a linked object later if we want to
            objects[object.id] = object

    if root.graph.linkSet is not None:
        for link in root.graph.linkSet.link:
            # look up the object by this ID in the objects hash for more information about the object itself
            print "%s is the parent of %s" % (link.parentRef, link.childRef)

####################################################################################################
# This is the main entry point of the program; run this as python example.py

# this will give us a list of all xml files in the data directory
for xml in glob.glob('./baseRealmDump/*/*/*/*.xml'):
    parse(xml)
    # break
