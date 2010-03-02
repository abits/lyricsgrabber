#==============================================================================
# timer.py - provides basic timing functionality for logging
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
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License f
# or more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#==============================================================================
'''
timer - Can be used to take running time of processes.
@author: Christoph Martel
@copyright: Christoph Martel
@license: GPLv3
'''


import time


class Timer():
    '''Can be used to take running time of processes.
    
    Time is retrieved in seconds passed.  Typical usage:
    
    timer = Timer()
    timer.start()
      ... some processing ...
    timer.stop()
    print timer.getTime()
    '''
    def __init__(self):
        '''initalize a timer object'''
        self.__passed_seconds = 0.0 # this is we we store the passed seconds
        self.__start_second = 0.0
        self.__stop_second = 0.0

    def start(self):
        '''start timer'''
        self.__start_second = time.time()

    def stop(self):
        '''stop timer and store passed seconds'''
        self.__stop_second = time.time()
        self.__passed_seconds = self.__stop_second - self.__start_second

    def getTime(self):
        '''retrieve stored passed seconds'''
        return self.__passed_seconds

    def resetTime(self):
        '''reset all initialization values'''
        self.__passed_seconds = 0.0
        self.__start_second = 0.0
        self.__stop_second = 0.0