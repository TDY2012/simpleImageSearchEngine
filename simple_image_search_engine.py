#!/usr/bin/env python3

##########################################################################
#   IMPORT
##########################################################################

import sys
import os
from optparse import OptionParser
from PyQt5 import QtWidgets
from gui.SimpleImageSearchEngineWindow import SimpleImageSearchEngineWindow

##########################################################################
#   GLOBAL
##########################################################################

NumRequiredArgs = 0
IndexDir = 'index'
ImageIndexFileName = 'index.pickle'

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
    parser.add_option( '--debug',
                        dest='isDebug',
                        action='store_true',
                        default=False,
                        help='enable debug mode' )
    (options, args) = parser.parse_args()

    if len(args) != NumRequiredArgs:
        parser.error('Incorrect number of arguments')
        sys.exit(-1)

    #   Parse options
    isDebug = options.isDebug

    #   Construct pyqt application
    app = QtWidgets.QApplication([])

    #   Construct simple image search engine window
    simpleImageSearchEngineWindow = SimpleImageSearchEngineWindow( IndexDir, ImageIndexFileName, isDebug )

    #   Show window
    simpleImageSearchEngineWindow.show()

    #   Exit application
    sys.exit(app.exec())

##########################################################################
#   RUN
##########################################################################

if __name__ == '__main__':
    main()