#==============================================================================
# taghandler.py - reads and writes lyrics tags to MP3 files with eyeD3
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

# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#==============================================================================
'''
taghandler - Reads and writes MP3 lyrics tags based upon eyeD3 library.
@author: Christoph Martel
@copyright: Christoph Martel
@license: GPLv3
'''


import sys
import eyeD3


class TagHandler:

    '''
    Reads and writes MP3 lyrics tags based upon eyeD3 library.
    
    Typical usage:
        tagger = TagHandler.TagHandler(settings)
        tagger.set_MP3_tags(file)
        (artist, track, album, lyrics) = tagger.get_MP3_tags()
        
    An object initialization needs a settings dictionary that holds
    at least a key named "force" pointing to a boolean - files which already
    hold lyrics are only witten when this boolean yields True.
    '''

    def __init__(self, settings):
        '''
        Object initialization.
        
        @param settings: global settings with at least { 'force' : boolean }
        @type param: dictionary
        '''
        self.__settings = settings
        self.artist = ''
        self.track = ''
        self.album = ''
        self.lyrics = '' # lyrics go in here
        self.order_number = None # track number and total tracks

    def set_MP3_tags(self, file):
        '''
        Reads and stores MP3 tags (artist, track, lyrics).
        
        @type file: string
        @param file: name of tagged MP3 file to read tags from
        '''
        if eyeD3.isMp3File(file):
            tag = eyeD3.Tag()
            tag.link(file)
            self.artist = tag.getArtist(eyeD3.ARTIST_FID)
            self.track = tag.getTitle()
            self.lyrics = self.get_lyrics_from_tag(tag)
            self.album = tag.getAlbum()
            self.order_number = tag.getTrackNum()

    def get_MP3_tags(self):
        '''
        Return stored MP3 tags.
        
        @return: tuple of artist, track, album and lyrics array
        @rtype: 4-tuple
        '''
        return (self.artist, 
                self.track, 
                self.album, 
                self.lyrics,
                self.order_number)

    def add_lyrics_from_string(self, MP3_file, lyrics):
        '''
        Write lyrics string to mp3 file.
        
        @type MP3_file: string
        @type lyrics: string
        @param lyrics: song lyrics to be written
        @param MP3_file: name of MP3 file to write lyrics to
        @rtype boolean
        @return: true if modified, false if not
        '''
        #print "DEBUG: %s" % type(lyrics)
        #lyrics = unicode(lyrics).encode('utf-8')
        lyrics = lyrics.replace("\n", "")
        #print "DEBUG: %s" % type(lyrics)
        tag = eyeD3.Tag()
        tag.header.setVersion(eyeD3.ID3_V2_4)
        tag.encoding = "\x03" # set UTF-8 encoding
        tag.link(MP3_file)
        try:
            if self.__settings['force'] == True:
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
        except:
            return False

    def add_lyrics_from_file(self, MP3_file, lyricsfile):
        '''
        Write lyrics from text file to mp3 file.
        
        @type MP3_file: string
        @type lyricsfile: string
        @param MP3_file: name of file to modify lyric tag
        @param lyricsfile: name of text file which contains song lyrics
        '''
        lyrics = open(lyricsfile, "U").read()
        lyrics = lyrics.replace("\r", "\r\n")
        tag = eyeD3.Tag()
        tag.link(MP3_file)
        tag.header.setVersion(eyeD3.ID3_V2_4)
        tag.addLyrics(lyrics)
        tag.update()

    def get_lyrics_from_file(self, MP3_file):
        '''
        Returns lyrics from MP3 file, or empty string.
        
        @type MP3_file: string
        @param MP3_file: name of file to return lyrics
        @rtype: string
        @return: lyrics string from MP3 file or empty string
        '''
        tag = eyeD3.Tag()
        tag.link(MP3_file)
        lyrics_frames = tag.getLyrics()
        lyrics = ''
        if bool(lyrics_frames): 
            for frame in lyrics_frames:
                lyrics = lyrics + frame.lyrics
        return lyrics    

    def get_lyrics_from_tag(self, tag):
        '''
        Returns lyrics from MP3 file, or empty string.
        
        @type tag: instance
        @param MP3_file: eyeD3.tag.Tag instance
        @rtype: string
        @return: lyrics string from MP3 file or empty string
        '''
        lyrics_frames = tag.getLyrics()
        lyrics = ''
        if bool(lyrics_frames): 
            for frame in lyrics_frames:
                lyrics = lyrics + frame.lyrics
        return lyrics    
        
    def clear(self):
        '''Reset MP3 tags.'''
        self.artist = ''
        self.album = ''
        self.lyrics = []

if __name__ == '__main__':
    # test routine
    settings = {}
    tagger = TagHandler(settings)
    tagger.add_lyrics_from_file(sys.argv[1], sys.argv[2])
    tagger.set_MP3_tags(sys.argv[1])


