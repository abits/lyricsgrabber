# -*- coding: utf-8 -*-
# Logger.py - provides logging functionality to file and screen
#
# Copyright (C) 2010 Christoph Martel
#
# This program is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation; either version 3 of the License, or (at your 
# option) any later version.
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License f
# or more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from time import localtime
from time import strftime

class Logger():
    '''
    This class implements logging functionality for a program.  It can also output "verbose" style
    messages directly to stdout.  
    Initialization of an object requires a settings parameter, which is a dictionary that holds
    at least two key/values: settings['logFileName'] (string: path) and settings['verbose'] (boolean). 
     
    Typical usage:
        myLogger = Logger(settings)
        myLogger.addToLog(logString)
    If settings['verbose'] == True the log messages are also printed to screen.
      
    @copyright: Christoph Martel
    @license: GPLv3
    @author: Christoph Martel
    @version: 0.1
    '''
    def __init__(self, settings):
        self.settings = settings
        self.logFile = None
              
    def getTimeString(self):
        timeString = strftime("[%d-%b-%Y %H:%M:%S]", localtime())
        return timeString
        
    def addToLog(self, string):
        if self.settings['logFileName'] != None:
            self.logFile = open(self.settings['logFileName'], "a")
            try: 
                self.logFile.write("%s:\t%s\n" % (self.getTimeString(),
                                                  unicode(string)))
            except:
                self.logFile.write(("%s:\t%s\n" % (self.getTimeString(),
                                               "logging error")))
            if self.settings['verbose'] == True:
                print "LyricsGrabber: " + string
                self.logFile.close()
        else:
            if self.settings['verbose'] == True:
                print "LyricsGrabber: " + string
                 
if __name__ == '__main__':
    #test routine
    testLogger = Logger()
    testLogger.addToLog("received test log entry...") 
