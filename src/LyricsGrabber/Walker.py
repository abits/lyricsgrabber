# -*- coding: utf-8 -*-
# Walker.py - scans directories for suitable MP3 files
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

import os
import eyeD3
import TagHandler

class Walker():
    '''scans a directory for suitable files and stores them with tag information in an array.
    
    Typical usage would be:
    myWalker = Walker(someSettings)
    myWalker.walk(someDir)
    fileList = myWalker.getFiles()
    (ignored, added) = myWalker.getFileCounts
    
    The settings parameter for initialization is a directory which holds the following information
        settings = { 'verbose' : someBoolean,
                     'force' : someBoolean,
                     'logFileName' : someString,
                     'interactive' : someBoolean,
                     'recursive' : someBoolean }
    The following information about each scanned file is stored:
        file = {'path' : someFilePath,
                'artist' : someArtist,
                'track' : someSong,
                'album' : someAlbum,
                'lyrics' : [] }
                
    @copyright: Christoph Martel
    @license: GPLv3
    @author: Christoph Martel
    @version: 0.1
    '''
    def __init__(self, settings):
        self.settings = settings
        self.fileContainer = []
        self.ignoredFilesCount = 0
        self.addedFilesCount = 0
        
    def walk(self, startDir):
        '''walks through directory tree, collects suitable files for tagging
        @type startDir: string
        @param startDir: path of top level directory to walk down'''
        if self.settings['recursive']:
            for dirpath, dirnames, filenames in os.walk(startDir):
                for f in filenames:
                    self.filterAndStoreFile(os.path.join(dirpath, f))
        else: # we don't want recursive scan
            for entry in os.listdir(startDir):
                if os.path.isdir(entry):
                    continue
                else:
                    self.filterAndStoreFile(os.path.join(os.path.abspath(startDir), entry))            
            
    def filterAndStoreFile(self, fpath):
        '''test whether file is suitable, read it's tags and store information
        @type fpath: string
        @param fpath: path of file to be tested'''
        tH = TagHandler.TagHandler(self.settings)
        file = {'path' : fpath,  # this is the data structure which holds information of file
                'artist' : '',
                'track' : '',
                'album' : '',
                'lyrics' : [] }
        if not eyeD3.isMp3File(file['path']): 
            self.ignoredFilesCount += 1
            return False
        else:
            tH.setMp3Tags(file['path'])
            (file['artist'], file['track'], file['album'], file['lyrics']) = tH.getMp3Tags()
        if (self.settings['force'] == False) and (file['lyrics'] != []):
            return False
        else:
            self.fileContainer.append(file)
            self.addedFilesCount += 1
                    
    def getFiles(self):
        '''returns stored list of suitable files for tagging
        @rtype: list
        @return: stored list of suitable files for tagging (object property)'''
        return self.fileContainer
    
    def getFileCounts(self):
        '''returns stored properties of ignored/selected files for tagging
        @rtype: tuple
        @return: stored properties of ignored/selected files for tagging'''
        return self.ignoredFilesCount, self.addedFilesCount