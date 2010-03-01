#============================================================================== 
# Logger.py - provides logging functionality to file and screen
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------- #
# Copyright (C) 2010 Christoph Martel
#
# This program is free software; you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the 
# Free Software Foundation; either version 3 of the License, or (at your 
# option) any later version.
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#==============================================================================
'''
Logger - logging functionality for stdout and file
@copyright: Christoph Martel
@license: GPLv3
@author: Christoph Martel
@version: 0.1
'''


from time import localtime
from time import strftime


class Logger():

    '''
    This class implements logging functionality for a program.  
    
    It can also output "verbose" style messages directly to stdout.  
    Initialization of an object requires a settings parameter, which is 
    a dictionary that holds at least two key/values: 
        * settings['logFileName'] (string: path)
        * settings['verbose'] (boolean). 
     
    Typical usage:
        logger = Logger(settings)
        logger.add_to_log(logString)
    If settings['verbose'] is true the log messages are also printed to 
    screen.
    '''

    def __init__(self, settings):
        self.__settings = settings
        self.logfile = None

    def __get_time_string(self):
        timeString = strftime("[%d-%b-%Y %H:%M:%S]", localtime())
        return timeString

    def add_to_log(self, string):
        if self.__settings['logFileName'] is not None:
            self.logfile = open(self.__settings['logFileName'], "a")
            try:
                self.logfile.write("%s:\t%s\n" % (self.__get_time_string(),
                                                  unicode(string)))
            except:
                self.logfile.write(("%s:\t%s\n" % (self.__get_time_string(),
                                               "logging error")))
            if self.__settings['verbose'] is True:
                print "LyricsGrabber: " + string
                self.logfile.close()
        else:
            if self.__settings['verbose'] is True:
                print "LyricsGrabber: " + string

if __name__ == '__main__':
    #test routine
    logger = Logger()
    logger.add_to_log(u"received test log entry...")
