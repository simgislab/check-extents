import sys
from lxml import etree
from optparse import OptionParser
from shapely.geometry import Polygon

def echo_err(parser,msg):
    parser.print_help()
    print "*** " + msg
    sys.exit(1)

def main():
   
    ''' Parse keys '''
    usage = 'usage: %prog -f=PATH'
    parser = OptionParser(usage=usage)
    parser.add_option('-f', '--file', action='store', dest='checkedFile')
    parser.add_option('-e', '--extent', action='store', dest='extent')
    (options, args) = parser.parse_args()
    checkedFile = options.checkedFile
    extent = options.extent
   
    if checkedFile == None:
        echo_err(parser, "XML file is required")
   
    if extent == None:
        echo_err(parser, "Extent is required")
    else:
        extentBounds = extent.split(",")
   
    print extentBounds[0],extentBounds[1],extentBounds[2],extentBounds[3]
    if ((float(extentBounds[0]) >= float(extentBounds[2])) or (float(extentBounds[1]) >= float(extentBounds[3]))):
        echo_err(parser, "Incorrect extent format: minLon,minLat,maxLon,maxLat")
   
    '''Extract boundary coordinates from metadata xml file'''
    tree = etree.parse(checkedFile)
    boundaryLat = [p.text for p in tree.iterfind("//PointLatitude")]
    boundaryLon = [p.text for p in tree.iterfind("//PointLongitude")]
   
    boundary = Polygon(((float(boundaryLon[0]), float(boundaryLat[0])),
                        (float(boundaryLon[1]), float(boundaryLat[1])),
                        (float(boundaryLon[2]), float(boundaryLat[2])),
                        (float(boundaryLon[3]), float(boundaryLat[3]))))
   
    ''' Extract boundary from given extent option '''
    boundaryComparative = Polygon(((float(extentBounds[0]), float(extentBounds[1])),
                                   (float(extentBounds[0]), float(extentBounds[3])),
                                   (float(extentBounds[2]), float(extentBounds[3])),
                                   (float(extentBounds[2]), float(extentBounds[1]))))
   
    print boundary.intersects(boundaryComparative)

if __name__=="__main__":
    main()