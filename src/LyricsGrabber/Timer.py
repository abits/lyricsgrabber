# -*- coding: utf-8 -*-
# Timer.py - provides basic timing functionality for logging
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

import time

class Timer():
    '''An object of this class can be used to take the approx. running time of processes etc.
    
    Typical usage:
    myTimer = Timer()
    myTimer.start()
      ... some processing ...
    myTimer.stop()
    print myTimer.getTime()
    
    Time is retrieved in seconds passed.
    @author: Christoph Martel
    @copyright: Christoph Martel
    @license: GPLv3
    '''
    def __init__(self):
        '''initalize a Timer object'''
        self.passedSeconds = 0.0 # this is we we store the passed seconds
        self.startSecond = 0.0
        self.stopSecond = 0.0
    
    def start(self):
        '''start timer'''
        self.startSecond = time.time()
    
    def stop(self):
        '''stop timer and store passed seconds'''
        self.stopSecond = time.time()
        self.passedSeconds = self.stopSecond - self.startSecond
    
    def getTime(self):
        '''retrieve stored passed seconds'''
        return self.passedSeconds
    
    def resetTime(self):
        '''reset all initialization values'''
        self.passedSeconds = 0.0
        self.startSecond = 0.0
        self.stopSecond = 0.0