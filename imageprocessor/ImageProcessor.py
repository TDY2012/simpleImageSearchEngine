##########################################################################
#   IMPORT
##########################################################################

import os
from PIL import Image
from typing import Tuple

##########################################################################
#   GLOBAL
##########################################################################

##########################################################################
#   HELPER
##########################################################################

##########################################################################
#   CLASS
##########################################################################

class ImageProcessor(object):

    @staticmethod
    def getColorHistogram( imageFilePath : str ) -> Tuple[float]:
        ''' This function computes given image color histogram
            value
        '''

        if not os.path.exists( imageFilePath ):
            raise ValueError( 'getColorHistogram() - Cannot find image at {}.'.format(imageFilePath) )\

        #   Read input image file path
        image = Image.open( imageFilePath )

        #   Initialize color histogram of three channels: R, G and B
        histogram = [0]*(256*3)

        #   Assign each pixel to their respective index of histogram
        for pixel in image.getdata():
            for i in range(3):
                histogram[pixel[i]+(256*i)] += 1

        #   Normalize histogram with number of pixels
        histogram = tuple( [ x/len(image.getdata()) for x in histogram] )

        return histogram

    @staticmethod
    def compareColorHistogram( hist1 : Tuple[float], hist2 : Tuple[float] ) -> float:
        ''' This function compares two color histograms similarity
            using color histogram intersection method
        '''

        assert(len(hist1) == len(hist2))

        #   Compute histogram intersection
        histogramIntersection = [ min(x,y) for x,y in zip(hist1, hist2) ]

        #   Split histogram by channel
        redHistogramIntersection = histogramIntersection[0:256]
        greenHistogramIntersection = histogramIntersection[256:256*2]
        blueHistogramIntersection = histogramIntersection[256*2:256*3]

        #   Multiply them
        return sum( redHistogramIntersection )*sum( greenHistogramIntersection )*sum( blueHistogramIntersection )
