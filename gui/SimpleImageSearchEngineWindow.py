##########################################################################
#   IMPORT
##########################################################################

import os
import time
from typing import Optional

from PIL import Image
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from .PyQtHelper import getIntValidator
from indexer.Indexer import Indexer
from imageprocessor.ImageProcessor import ImageProcessor

##########################################################################
#   GLOBAL
##########################################################################

DefaultMaxResultNum = 10

WindowTitle = 'Simple Image Search Engine'

##########################################################################
#   HELPER
##########################################################################

def logResult( imageIdToHistogramSimilarityTupleList ):
    ''' This function logs out formatted results in terminal
    '''

    #   If there is no matching
    if len(imageIdToHistogramSimilarityTupleList) == 0:
        print('No matched result.')
        return

    print(imageIdToHistogramSimilarityTupleList)

def getOpenImageFunc( imageFilePath ):

    def f():
        image = Image.open( imageFilePath )
        image.show()

    return f

##########################################################################
#   CLASS
##########################################################################

class QueryThread( QtCore.QThread ):

    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, imageIdToImageDataDict, inputImageFilePath, isDebug=False):
        QtCore.QThread.__init__(self)
        self.imageIdToImageDataDict = imageIdToImageDataDict
        self.inputImageFilePath = inputImageFilePath
        self.isDebug = isDebug

    def run(self):
        
        #   Start timer
        startTime = time.time()

        #   Compute given image color histogram
        imageHistogram = ImageProcessor.getColorHistogram( self.inputImageFilePath )

        #   Compare color histogram of input image with index
        imageIdToHistogramSimilarityTupleList = [ ( imageId, ImageProcessor.compareColorHistogram( imageHistogram, imageData.histogram ) ) for imageId, imageData in self.imageIdToImageDataDict.items() ]

        #   Sort by color histogram similarity
        imageIdToHistogramSimilarityTupleList.sort( key=lambda x: x[1], reverse=True )

        #   End timer
        deltaTime = time.time() - startTime
        
        if self.isDebug:

            #   Display timer log message
            print( 'Queried in {} seconds.'.format( deltaTime ) )

        #   Return result
        self.signal.emit( imageIdToHistogramSimilarityTupleList )

class SimpleImageSearchEngineWindow( QtWidgets.QMainWindow ):

    def __init__(self, indexDir : str, indexFileName : str, isDebug : Optional[bool]=False):
        super(SimpleImageSearchEngineWindow, self).__init__()

        self.imageIdToImageDataDict = Indexer.readIndex( indexDir, indexFileName )
        self.isDebug = isDebug
        self.maxResultNum = DefaultMaxResultNum
        self.setWindowTitle( WindowTitle )
        self.createGuiComponents()
        self.initializeGuiComponents()

    def createGuiComponents(self):
        
        widget = QtWidgets.QWidget()

        mainLayout = QtWidgets.QVBoxLayout()

        #   Initialize top, mid and bottom layout
        #   as horizontal box layout
        topLayout = QtWidgets.QHBoxLayout()
        bottomLayout = QtWidgets.QHBoxLayout()

        #
        #   Search Option
        #

        #   Create search option group box widget
        groupBoxSearchOption = QtWidgets.QGroupBox('Search Options')

        #   Create search option form layout
        formLayoutSearchOption = QtWidgets.QFormLayout()

        #   Create max result line edit widget
        self.lineEditMaxResult = QtWidgets.QLineEdit()
        self.lineEditMaxResult.setValidator( getIntValidator(bottomValue=1) )

        #   Create key word line edit widget
        self.lineEditInputImage = QtWidgets.QLineEdit()

        #   Assign max result line edit widget
        #   and input image line edit widget to
        #   search option group box form layout
        formLayoutSearchOption.addRow( 'Max Result', self.lineEditMaxResult )
        formLayoutSearchOption.addRow( 'Input Image', self.lineEditInputImage )
        
        #   Set search option group box layout
        groupBoxSearchOption.setLayout(formLayoutSearchOption)

        #
        #   Search Button
        #

        self.buttonSearch = QtWidgets.QPushButton()
        self.buttonSearch.setText( 'Search' )
        self.buttonSearch.setSizePolicy( QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum )

        topLayout.addWidget(groupBoxSearchOption)
        topLayout.addWidget(self.buttonSearch)

        #
        #   Result Table
        #

        #   Create result group box widget
        groupBoxResult = QtWidgets.QGroupBox('Result')

        #   Create result vertical layout
        vBoxResult = QtWidgets.QVBoxLayout()

        #   Create result table widget
        self.tableResult = QtWidgets.QTableWidget()
        self.tableResult.setRowCount(0)
        self.tableResult.setColumnCount(4)
        self.tableResult.setHorizontalHeaderLabels(['Score', 'Id', 'FilePath', 'Action'])
        self.tableResult.setSortingEnabled(True)
        self.tableResult.setEditTriggers( QtWidgets.QAbstractItemView.NoEditTriggers )

        vBoxResult.addWidget(self.tableResult)

        #   Set result group box layout
        groupBoxResult.setLayout(vBoxResult)

        bottomLayout.addWidget(groupBoxResult)

        mainLayout.addLayout( topLayout )
        mainLayout.addLayout( bottomLayout )
        
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def initializeGuiComponents( self ):
        ''' This function sets default value and callback function
            to all gui components
        '''

        #   Set default value and callback function
        #   for max result line edit widget
        self.lineEditMaxResult.setText(str(DefaultMaxResultNum))
        self.lineEditMaxResult.textEdited.connect( self.lineEditMaxResult_cb )

        #   Set callback function for search button
        self.buttonSearch.clicked.connect( self.buttonSearch_cb )

    def lineEditMaxResult_cb( self ):
        ''' This is callback function of max result line edit widget
            which sets maximum result number to query manager
        '''

        try:
            #   Get max result number from max result line edit widget
            maxResultNum = int(self.lineEditMaxResult.text())
        except ValueError:
            self.lineEditMaxResult.setText(str(DefaultMaxResultNum))
            maxResultNum = DefaultMaxResultNum

        #   NOTE -  This is a hack, since I don't know why int validator
        #           cannot handle 0, despite the buttom value = 1
        if maxResultNum < 1:
            self.lineEditMaxResult.setText(str(1))
            maxResultNum = 1

        #   Set max result number
        self.maxResultNum = maxResultNum

    def buttonSearch_cb( self ):
        ''' This is callback function of search button widget
            which performs querying and displays results on
            results table widget
        '''

        #   Get input image file path from input image line edit widget
        inputImageFilePath =  self.lineEditInputImage.text()

        #   Begin query with thread
        self.beginQuery( inputImageFilePath )

    def beginQuery( self, inputImageFilePath ):
        ''' This function constructs query thread and runs it
        '''

        #   Disable the search button while querying
        self.buttonSearch.setEnabled(False)

        #   Construct query thread
        self.queryThread = QueryThread( self.imageIdToImageDataDict, inputImageFilePath, self.isDebug )

        #   Bind query thread signal to finish query function
        self.queryThread.signal.connect( self.finishQuery )

        #   Run query thread
        self.queryThread.start()

    def finishQuery( self, imageIdToHistogramSimilarityTupleList ):
        ''' This function gets result from query thread and
            displays result on table widget
        '''

        if self.isDebug:
            
            #   Display log message in terminal
            logResult( imageIdToHistogramSimilarityTupleList )

        #   Display result on table widget
        self.displayResultsOnTable( imageIdToHistogramSimilarityTupleList )

        #   Reenable search button
        self.buttonSearch.setEnabled(True)

    def displayResultsOnTable( self, imageIdToHistogramSimilarityTupleList ):
        ''' This function populates results table widget with given
            result
        '''

        #   If there is no result, clear all result on table
        if len(imageIdToHistogramSimilarityTupleList) == 0:
            self.tableResult.setRowCount(0)
            return

        #   Limit result with max result number
        imageIdToHistogramSimilarityTupleList = imageIdToHistogramSimilarityTupleList[:self.maxResultNum]

        #   Set table row
        self.tableResult.setRowCount(len(imageIdToHistogramSimilarityTupleList))

        #   Populate record on table
        for resultIndex, imageIdToHistogramSimilarityTuple in enumerate( imageIdToHistogramSimilarityTupleList ):

            imageFilePath = self.imageIdToImageDataDict[ imageIdToHistogramSimilarityTuple[0] ].imageFilePath

            self.tableResult.setItem( resultIndex, 0, QtWidgets.QTableWidgetItem( str(imageIdToHistogramSimilarityTuple[1]) ))
            self.tableResult.setItem( resultIndex, 1, QtWidgets.QTableWidgetItem( str(imageIdToHistogramSimilarityTuple[0]) ))
            self.tableResult.setItem( resultIndex, 2, QtWidgets.QTableWidgetItem( imageFilePath ))

            openButton = QtWidgets.QPushButton()
            openButton.setText('Open')
            openImageFunc = getOpenImageFunc( imageFilePath )
            openButton.clicked.connect( openImageFunc )

            self.tableResult.setCellWidget( resultIndex, 3, openButton )