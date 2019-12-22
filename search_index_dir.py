#!/usr/bin/env python

##########################################################################
#   IMPORT
##########################################################################

import sys
import os
from optparse import OptionParser
from indexer.Indexer import Indexer
from imageprocessor.ImageProcessor import ImageProcessor

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 1

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

    parser = OptionParser(usage='usage: %prog [options] <image_file_path>',
                            version='%prog 0.0')

    (options, args) = parser.parse_args()

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    imageFilePath = args[0]

    #   Check if given image file path exists
    if not os.path.exists( imageFilePath ):
        print( 'search_index_dir() - Cannot find image file at {}.'.format( imageFilePath ) )

    #   Compute given image color histogram
    imageHistogram = ImageProcessor.getColorHistogram( imageFilePath )

    #   Read image index
    imageIdToImageDataDict = Indexer.readIndex( IndexDir, IndexFileName )

    #   Compare color histogram of input image with index
    imageIdToHistogramSimilarityTupleList = [ ( imageId, ImageProcessor.compareColorHistogram( imageHistogram, imageData.histogram ) ) for imageId, imageData in imageIdToImageDataDict.items() ]

    #   Sort by color histogram similarity
    imageIdToHistogramSimilarityTupleList.sort( key=lambda x: x[1], reverse=True )

    for imageId, histogramSimilarity in imageIdToHistogramSimilarityTupleList:

        print('imageId = {}, histogramSimilarity = {}, imageFilePath = {}'.format(imageId, histogramSimilarity, imageIdToImageDataDict[imageId].imageFilePath ))

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()