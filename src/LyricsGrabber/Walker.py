#==============================================================================
# Walker.py - scans directories for suitable MP3 files
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------- 
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
#==============================================================================
'''
Walker - scans a directory for suitable files
@copyright: Christoph Martel
@license: GPLv3
@author: Christoph Martel
@version: 0.1
'''

import os
import eyeD3
import TagHandler

class Walker():
    '''Scans a directory and stores suitable files with tag information.
    
    Typical usage would be:
    walker = Walker(someSettings)
    walker.walk(someDir)
    fileList = walker.getFiles()
    (ignored, added) = walker.getFileCounts
    
    The settings parameter for initialization is a directory which holds the 
    following information
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
    '''
    def __init__(self, settings):
        self.__settings = settings
        self.__file_container = []
        self.__ignored_files_count = 0
        self.__added_files_count = 0

    def walk(self, startdir):
        '''
        Walks through directory tree, collects suitable files for tagging.
        
        @type startdir: string
        @param startdir: path of top level directory to walk down
        '''
        if self.__settings['recursive']:
            for dirpath, dirnames, filenames in os.walk(startdir):
                for f in filenames:
                    self.__filter_and_store_file(os.path.join(dirpath, f))
        else: # we don't want recursive scan
            for entry in os.listdir(startdir):
                if os.path.isdir(entry):
                    continue
                else:
                    self.__filter_and_store_file(\
                    os.path.join (os.path.abspath(startdir), entry))

    def __filter_and_store_file(self, fpath):
        '''
        Test whether file is suitable, read it's tags and store information.
        
        @type fpath: string
        @param fpath: path of file to be tested
        '''
        tH = TagHandler.TagHandler(self.__settings)
        # this is the data structure which holds information of file
        file = {'path' : fpath,
                'artist' : '',
                'track' : '',
                'album' : '',
                'lyrics' : [] }
        if not eyeD3.isMp3File(file['path']):
            self.__ignored_files_count += 1
            return False
        else:
            tH.set_MP3_tags(file['path'])
            (file['artist'],
             file['track'],
             file['album'],
             file['lyrics']) = tH.get_MP3_tags()
        if not self.__settings['force'] or file['lyrics'] != []:
            return False
        else:
            self.__file_container.append(file)
            self.__added_files_count += 1

    def getFiles(self):
        '''
        Returns stored list of suitable files.
        
        @rtype: list
        @return: stored list of suitable files for tagging (object property)
        '''
        return self.__file_container

    def getFileCounts(self):
        '''
        Returns stored properties of ignored/selected files.
        
        @rtype: tuple
        @return: stored properties of ignored/selected files for tagging
        '''
        return self.__ignored_files_count, self.__added_files_count