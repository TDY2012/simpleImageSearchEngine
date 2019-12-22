#!/usr/bin/env python

##########################################################################
#   IMPORT
##########################################################################

import sys
from optparse import OptionParser
from indexer.Indexer import Indexer

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 0
ImageDir = '../image'
IndexDir = 'index'
IndexFileName = 'index.pickle'

##########################################################################
#   HELPER
##########################################################################

##########################################################################
#   CLASS
##########################################################################

##########################################################################
#   MAIN
##########################################################################

def main():

    parser = OptionParser(usage='usage: %prog [options]',
                            version='%prog 0.0')
    parser.add_option( '--imgDir',
                        action='store',
                        dest='imgDir',
                        default=ImageDir,
                        help='text file directory (default = {!r})'.format(ImageDir) )

    (options, args) = parser.parse_args()

    #   Parse options
    imageDir = options.imgDir

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    #   Create indexing structure of given images inside directory
    imageIdToImageDataDict = Indexer.index( imageDir )
    
    #   Write to file
    Indexer.writeIndex( imageIdToImageDataDict, IndexDir, IndexFileName )

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()