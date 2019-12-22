##########################################################################
#   IMPORT
##########################################################################

import os
import pickle
from typing import Tuple, Dict
from imageprocessor.ImageProcessor import ImageProcessor

##########################################################################
#   GLOBAL
##########################################################################

##########################################################################
#   HELPER
##########################################################################

##########################################################################
#   CLASS
##########################################################################

class ImageData(object):

    def __init__(self, imageId : int, imageFilePath : str, histogram : Tuple[float] ):
        self.imageId = imageId
        self.imageFilePath = imageFilePath
        self.histogram = histogram

    def __str__(self):
        return 'ImageData( imageId={}, imageFilePath={} )'.format( self.imageId, self.imageFilePath )

class Indexer(object):

    @staticmethod
    def index( imageDir : str ):
        ''' This function indexes images inside given image directory
            by color histrogram value
        '''

        #   Check if image directory exists
        if not os.path.exists( imageDir ):
            raise ValueError( 'index() - Cannot find image directory at {}.'.format( imageDir ) )

        #   Get image file name list from given directory
        imageFileNameList = os.listdir( imageDir )

        #   Initialize image id to image data dictionary
        imageIdToImageDataDict = dict()

        for imageId, imageFileName in enumerate( imageFileNameList ):

            #   Construct image file path
            imageFilePath = os.path.join( imageDir, imageFileName )

            #   Compute color histogram
            histogram = ImageProcessor.getColorHistogram( imageFilePath )

            #   Construct image data
            imageData = ImageData( imageId, imageFilePath, histogram )

            #   Assign to dictionary
            imageIdToImageDataDict[ imageId ] = imageData

        return imageIdToImageDataDict

    @staticmethod
    def writeIndex( imageIdToImageDataDict : Dict, indexDir : str, indexFileName : str ):
        ''' This function writes index to file
        '''

        #   Construct index file path
        indexFilePath = os.path.join( indexDir, indexFileName )

        #   Write index file
        with open( indexFilePath, 'wb' ) as indexFile:
            pickle.dump( imageIdToImageDataDict, indexFile )

    @staticmethod
    def readIndex( indexDir : str, indexFileName : str ):
        ''' This function reads index from file
        '''

        #   Construct index file path
        indexFilePath = os.path.join( indexDir, indexFileName )

        #   Check if index file exists
        if not os.path.exists( indexFilePath ):
            raise ValueError( 'readIndex() - Cannot find index file at {}.'.format( indexFilePath ) )

        #   Write index file
        with open( indexFilePath, 'rb' ) as indexFile:
            imageIdToImageDataDict = pickle.load( indexFile )

        return imageIdToImageDataDict