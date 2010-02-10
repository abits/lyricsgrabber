# -*- coding: utf-8 -*-
# TagHandler.py - reads and writes lyrics tags to MP3 files with eyeD3
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

# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import sys
import eyeD3

class TagHandler:
    '''reads and writes MP3 lyrics tags based upon eyeD3 library
    Typical usage:
        tH = TagHandler.TagHandler(settings)
        tH.setMp3Tags(file)
        (artist, track, album, lyrics) = tH.getMp3Tags()
    An object initialization needs a settings dictionary that holds
    at least a key named "force" pointing to a boolean - files which already
    hold lyrics are only witten when this boolean yields True.
'''
    def __init__(self, settings):
        '''object initialization
        @param settings: global settings with at least a pair { 'force' : boolean }
        @type param: dictionary'''
        self.settings = settings
        self.artist = ''
        self.track = ''
        self.album = ''
        self.lyrics = [] # lyrics tags go in here
           
    def setMp3Tags(self, file):   
        '''reads and stores MP3 tags (artist, track, lyrics)
        @type file: string
        @param file: name of tagged MP3 file to read tags from'''
        if eyeD3.isMp3File(file): 
            tag = eyeD3.Tag()
            tag.link(file)
            self.artist = tag.getArtist(eyeD3.ARTIST_FID)
            self.track = tag.getTitle()
            self.lyrics = tag.getLyrics()
            self.album = tag.getAlbum()
    
    def getMp3Tags(self):
        '''return stored MP3 tags
        @return: tuple of artist, track, album and lyrics array
        @rtype: 4-tuple'''
        return (self.artist, self.track, self.album, self.lyrics)
    
    def addLyricsFromString(self, mp3File, lyrics):
        '''write lyrics string to mp3 file
        @type mp3File: string
        @type lyrics: string
        @param lyrics: song lyrics to be written
        @param mp3File: name of MP3 file to write lyrics to
        @rtype boolean
        @return: true if modified, false if not'''
        #print "DEBUG: %s" % type(lyrics)
        #lyrics = unicode(lyrics).encode('latin-1')
        lyrics = lyrics.replace("\n", "")
        #print "DEBUG: %s" % type(lyrics)
        tag = eyeD3.Tag()
        tag.link(mp3File)
        tag.header.setVersion(eyeD3.ID3_V2_3)
        if self.settings['force'] == True:
            tag.addLyrics(lyrics)
            tag.update()
            return True
        else: # test for existing lyrics before write
            existingTag = tag.getLyrics()
            if len(existingTag) == 0: # no lyric frames, so we can write
                tag.addLyrics(lyrics)
                tag.update()          
                return True
        return False  
    
    def addLyricsFromFile(self, mp3File, lyricsFile):
        '''write lyrics from text file to mp3 file
        @type mp3File: string
        @type lyricsFile: string
        @param mp3File: name of file to modify lyric tag
        @param lyricsFile: name of text file which contains song lyrics'''
        lyrics = open(lyricsFile, "U").read()
        lyrics = lyrics.replace("\r", "\r\n")  
        tag = eyeD3.Tag()
        tag.link(mp3File)
        tag.header.setVersion(eyeD3.ID3_V2_3)
        tag.addLyrics(lyrics)
        tag.update()
    
    def clear(self):
        '''reset MP3 tags'''
        self.artist = ''
        self.album = ''
        self.lyrics = []

if __name__ == '__main__':
    # test routine
    settings = {}
    tH = TagHandler(settings)
    tH.addLyricsFromFile(sys.argv[1], sys.argv[2])
    tH.setMp3Tags(sys.argv[1])


