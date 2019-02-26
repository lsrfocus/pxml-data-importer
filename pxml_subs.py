#!/usr/bin/env python

#
# Generated Thu Apr 14 17:07:56 2016 by generateDS.py version 2.22a.
#
# Command line options:
#   ('-o', 'pxml.py')
#   ('-s', 'pxml_subs.py')
#
# Command line arguments:
#   PalantirXMLImportSchema.xsd
#
# Command line:
#   generateDS.py -o "pxml.py" -s "pxml_subs.py" PalantirXMLImportSchema.xsd
#
# Current working directory (os.getcwd()):
#   generateDS-2.22a0
#

import sys
from lxml import etree as etree_

import ??? as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#


class stringPositionLocatorSub(supermod.stringPositionLocator):
    def __init__(self, startPosition=None, endPosition=None, sentenceNumber=None, paragraphNumber=None):
        super(stringPositionLocatorSub, self).__init__(startPosition, endPosition, sentenceNumber, paragraphNumber, )
supermod.stringPositionLocator.subclass = stringPositionLocatorSub
# end class stringPositionLocatorSub


class dataSourceRecordSub(supermod.dataSourceRecord):
    def __init__(self, dataSource=None, importKey=None, recordLocator=None, aclId=None, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, stringPositionLocator=None):
        super(dataSourceRecordSub, self).__init__(dataSource, importKey, recordLocator, aclId, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, stringPositionLocator, )
supermod.dataSourceRecord.subclass = dataSourceRecordSub
# end class dataSourceRecordSub


class dataSourceRecordSetSub(supermod.dataSourceRecordSet):
    def __init__(self, dataSourceRecord=None):
        super(dataSourceRecordSetSub, self).__init__(dataSourceRecord, )
supermod.dataSourceRecordSet.subclass = dataSourceRecordSetSub
# end class dataSourceRecordSetSub


class propertySub(supermod.property):
    def __init__(self, id=None, type_=None, linkType=None, role=None, keywordDisabled=None, aclId=None, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, customKeyword=None, timestamp=None, timeInterval=None, gisData=None, propertyValue=None, dataSourceRecordSet=None):
        super(propertySub, self).__init__(id, type_, linkType, role, keywordDisabled, aclId, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, customKeyword, timestamp, timeInterval, gisData, propertyValue, dataSourceRecordSet, )
supermod.property.subclass = propertySub
# end class propertySub


class propertyComponentSub(supermod.propertyComponent):
    def __init__(self, type_=None, propertyData=None):
        super(propertyComponentSub, self).__init__(type_, propertyData, )
supermod.propertyComponent.subclass = propertyComponentSub
# end class propertyComponentSub


class propertyValueSub(supermod.propertyValue):
    def __init__(self, propertyData=None, propertyComponent=None, propertyTimeInterval=None, propertyUnparsedValue=None, propertyRawValue=None):
        super(propertyValueSub, self).__init__(propertyData, propertyComponent, propertyTimeInterval, propertyUnparsedValue, propertyRawValue, )
supermod.propertyValue.subclass = propertyValueSub
# end class propertyValueSub


class propertySetSub(supermod.propertySet):
    def __init__(self, property=None):
        super(propertySetSub, self).__init__(property, )
supermod.propertySet.subclass = propertySetSub
# end class propertySetSub


class mediaSetSub(supermod.mediaSet):
    def __init__(self, media=None):
        super(mediaSetSub, self).__init__(media, )
supermod.mediaSet.subclass = mediaSetSub
# end class mediaSetSub


class mediaSub(supermod.media):
    def __init__(self, id=None, mediaType=None, linkType=None, mimeType=None, filename=None, aclId=None, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, mediaTitle=None, mediaShortDescription=None, mediaDescription=None, mediaData=None, thumbnail=None, dataSourceRecordSet=None):
        super(mediaSub, self).__init__(id, mediaType, linkType, mimeType, filename, aclId, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, mediaTitle, mediaShortDescription, mediaDescription, mediaData, thumbnail, dataSourceRecordSet, )
supermod.media.subclass = mediaSub
# end class mediaSub


class noteSub(supermod.note):
    def __init__(self, linkType=None, aclId=None, id=None, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, noteTitle=None, noteData=None, dataSourceRecordSet=None):
        super(noteSub, self).__init__(linkType, aclId, id, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, noteTitle, noteData, dataSourceRecordSet, )
supermod.note.subclass = noteSub
# end class noteSub


class objectSub(supermod.object):
    def __init__(self, id=None, externalId=None, resolvesTo=None, type_=None, baseType=None, timeStart=None, timeEnd=None, groupFlag=False, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, title=None, description=None, propertySet=None, mediaSet=None, noteSet=None):
        super(objectSub, self).__init__(id, externalId, resolvesTo, type_, baseType, timeStart, timeEnd, groupFlag, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, title, description, propertySet, mediaSet, noteSet, )
supermod.object.subclass = objectSub
# end class objectSub


class noteSetSub(supermod.noteSet):
    def __init__(self, note=None):
        super(noteSetSub, self).__init__(note, )
supermod.noteSet.subclass = noteSetSub
# end class noteSetSub


class objectSetSub(supermod.objectSet):
    def __init__(self, object=None):
        super(objectSetSub, self).__init__(object, )
supermod.objectSet.subclass = objectSetSub
# end class objectSetSub


class dataSourceSub(supermod.dataSource):
    def __init__(self, type_=None, id=None, externalId=None, isStub=None, aclId=None, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, name=None, description=None, discoveryMessage=None, primaryObject=None):
        super(dataSourceSub, self).__init__(type_, id, externalId, isStub, aclId, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, name, description, discoveryMessage, primaryObject, )
supermod.dataSource.subclass = dataSourceSub
# end class dataSourceSub


class dataSourceSetSub(supermod.dataSourceSet):
    def __init__(self, dataSource=None):
        super(dataSourceSetSub, self).__init__(dataSource, )
supermod.dataSourceSet.subclass = dataSourceSetSub
# end class dataSourceSetSub


class linkSub(supermod.link):
    def __init__(self, parentRef=None, childRef=None, type_=None, role=None, id=None, aclId=None, classification=None, FGIsourceOpen=None, FGIsourceProtected=None, SCIcontrols=None, declassification=None, disseminationControls=None, nonICmarkings=None, nonUSmarkings=None, releasableTo=None, text=None, timestamp=None, timeInterval=None, dataSourceRecordSet=None):
        super(linkSub, self).__init__(parentRef, childRef, type_, role, id, aclId, classification, FGIsourceOpen, FGIsourceProtected, SCIcontrols, declassification, disseminationControls, nonICmarkings, nonUSmarkings, releasableTo, text, timestamp, timeInterval, dataSourceRecordSet, )
supermod.link.subclass = linkSub
# end class linkSub


class linkSetSub(supermod.linkSet):
    def __init__(self, link=None):
        super(linkSetSub, self).__init__(link, )
supermod.linkSet.subclass = linkSetSub
# end class linkSetSub


class graphSub(supermod.graph):
    def __init__(self, aclSet=None, dataSourceSet=None, objectSet=None, linkSet=None):
        super(graphSub, self).__init__(aclSet, dataSourceSet, objectSet, linkSet, )
supermod.graph.subclass = graphSub
# end class graphSub


class palantirSub(supermod.palantir):
    def __init__(self, systemId=None, graph=None):
        super(palantirSub, self).__init__(systemId, graph, )
supermod.palantir.subclass = palantirSub
# end class palantirSub


class primaryObjectSub(supermod.primaryObject):
    def __init__(self, objectRef=None):
        super(primaryObjectSub, self).__init__(objectRef, )
supermod.primaryObject.subclass = primaryObjectSub
# end class primaryObjectSub


class propertyRawValueSub(supermod.propertyRawValue):
    def __init__(self, valueOf_=None):
        super(propertyRawValueSub, self).__init__(valueOf_, )
supermod.propertyRawValue.subclass = propertyRawValueSub
# end class propertyRawValueSub


class propertyUnparsedValueSub(supermod.propertyUnparsedValue):
    def __init__(self, valueOf_=None):
        super(propertyUnparsedValueSub, self).__init__(valueOf_, )
supermod.propertyUnparsedValue.subclass = propertyUnparsedValueSub
# end class propertyUnparsedValueSub


class propertyTimeIntervalSub(supermod.propertyTimeInterval):
    def __init__(self, timeStart=None, timeEnd=None):
        super(propertyTimeIntervalSub, self).__init__(timeStart, timeEnd, )
supermod.propertyTimeInterval.subclass = propertyTimeIntervalSub
# end class propertyTimeIntervalSub


class aclSetSub(supermod.aclSet):
    def __init__(self, defaultAcl=None, acl=None):
        super(aclSetSub, self).__init__(defaultAcl, acl, )
supermod.aclSet.subclass = aclSetSub
# end class aclSetSub


class aclSub(supermod.acl):
    def __init__(self, aclId=None, aclDomain=None, aclReference=None, aclSpecification=None):
        super(aclSub, self).__init__(aclId, aclDomain, aclReference, aclSpecification, )
supermod.acl.subclass = aclSub
# end class aclSub


class aclReferenceSub(supermod.aclReference):
    def __init__(self, aclId=None):
        super(aclReferenceSub, self).__init__(aclId, )
supermod.aclReference.subclass = aclReferenceSub
# end class aclReferenceSub


class aclSpecificationSub(supermod.aclSpecification):
    def __init__(self, type_='group', authSourceTag=None, externalId=None, permissions=None):
        super(aclSpecificationSub, self).__init__(type_, authSourceTag, externalId, permissions, )
supermod.aclSpecification.subclass = aclSpecificationSub
# end class aclSpecificationSub


class gisDataSub(supermod.gisData):
    def __init__(self, point=None, geo_data=None):
        super(gisDataSub, self).__init__(point, geo_data, )
supermod.gisData.subclass = gisDataSub
# end class gisDataSub


class pointSub(supermod.point):
    def __init__(self, latitude=None, longitude=None, elevation=None, userLatLong=None, userUTM=None, userMGRS=None, userElevation=None):
        super(pointSub, self).__init__(latitude, longitude, elevation, userLatLong, userUTM, userMGRS, userElevation, )
supermod.point.subclass = pointSub
# end class pointSub


class userLatLongSub(supermod.userLatLong):
    def __init__(self, latitude=None, longitude=None):
        super(userLatLongSub, self).__init__(latitude, longitude, )
supermod.userLatLong.subclass = userLatLongSub
# end class userLatLongSub


class userElevationSub(supermod.userElevation):
    def __init__(self, elevation=None):
        super(userElevationSub, self).__init__(elevation, )
supermod.userElevation.subclass = userElevationSub
# end class userElevationSub


class userUTMSub(supermod.userUTM):
    def __init__(self, utmZone=None, utmNorthing=None, utmEasting=None):
        super(userUTMSub, self).__init__(utmZone, utmNorthing, utmEasting, )
supermod.userUTM.subclass = userUTMSub
# end class userUTMSub


class userMGRSSub(supermod.userMGRS):
    def __init__(self, mgrs=None):
        super(userMGRSSub, self).__init__(mgrs, )
supermod.userMGRS.subclass = userMGRSSub
# end class userMGRSSub


class timeIntervalSub(supermod.timeInterval):
    def __init__(self, timeStart=None, timeEnd=None):
        super(timeIntervalSub, self).__init__(timeStart, timeEnd, )
supermod.timeInterval.subclass = timeIntervalSub
# end class timeIntervalSub


class timestampSub(supermod.timestamp):
    def __init__(self, timestamp_member=None):
        super(timestampSub, self).__init__(timestamp_member, )
supermod.timestamp.subclass = timestampSub
# end class timestampSub


class thumbnailTypeSub(supermod.thumbnailType):
    def __init__(self, mimeType=None, thumbnailData=None):
        super(thumbnailTypeSub, self).__init__(mimeType, thumbnailData, )
supermod.thumbnailType.subclass = thumbnailTypeSub
# end class thumbnailTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'stringPositionLocator'
        rootClass = supermod.stringPositionLocator
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://www.palantirtech.com/pg/schema/import/"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'stringPositionLocator'
        rootClass = supermod.stringPositionLocator
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from StringIO import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'stringPositionLocator'
        rootClass = supermod.stringPositionLocator
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://www.palantirtech.com/pg/schema/import/"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'stringPositionLocator'
        rootClass = supermod.stringPositionLocator
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from ??? import *\n\n')
        sys.stdout.write('import ??? as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
