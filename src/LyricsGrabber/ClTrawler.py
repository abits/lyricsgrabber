#=============================================================================
# ClTrawler.py - client for <http://www.chartlyrics.com/>
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------- 
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
#============================================================================= 
'''
ClTrawler - searches and extracts lyrics against chartlyrics API.
@author: Christoph Martel
@copyright: Christoph Martel
@license: GPLv3
'''


import urllib2
import xml.etree.ElementTree as ET
import Trawler


class ClTrawler(Trawler.Trawler):

    '''
    Retrieves song lyrics from <http://www.chartlyrics.com/> via REST API.
    
    A typical usage might look like:
        trawler = ClTrawler()
        trawler.set_text(someArtist, someSong)
        if trawler.get_text() != '':    # make sure we have found lyrics
            lyrics = trawler.get_text() # read out the song lyrics
    
    If no lyrics are found, the stored lyrics property of the object is set to 
    an empty string.  Responses may also be written to file.
    '''

    def __init__(self, settings):
        self.__settings = settings
        self.__API_search_URI = \
            'http://api.chartlyrics.com/apiv1.asmx/SearchLyric'
        self.__API_lyrics_URI = \
            'http://api.chartlyrics.com/apiv1.asmx/GetLyric'
        self.__search_response = None
        self.__lyrics_response = None
        self.__lyrics_checksum = ''
        self.__lyrics_ID = ''
        self.__text = ''

    def __build_searchrequest(self, artist, track):
        '''
        Constructs a url to query ChartLyrics for track lyrics ID.
        
        @type artist: string
        @type track: string
        @param artist: name of the artist to search in lyrics database
        @param track: name of the song to retrieve lyrics for
        @rtype: string
        @return: uri to query ChartLyrics for a track lyrics ID
        '''
        artist = 'artist=' + urllib2.quote(artist.encode('utf-8'))
        track = 'song=' + urllib2.quote(track.encode('utf-8'))
        param_list = [artist, track]
        parameters = '&'.join(param_list)
        URI_list = [self.__API_search_URI, parameters]
        search_request_URI = '?'.join(URI_list)
        return search_request_URI

    def __build_lyricsrequest(self, lyrics_ID, lyrics_checksum):
        '''
        Constructs a url to query ChartLyrics for song lyrics.
        
        @type lyrics_ID: string
        @param lyrics_ID: track lyrics ID from Leo's Lyric's database
        @rtype: string
        @return: uri to query ChartLyrics for song lyrics
        '''
        lyrics_ID = 'lyricId=' + lyrics_ID
        lyrics_checksum = 'lyricCheckSum=' + lyrics_checksum
        param_list = [lyrics_ID, lyrics_checksum]
        parameters = '&'.join(param_list)
        URI_list = [self.__API_lyrics_URI, parameters]
        text_request_URI = '?'.join(URI_list)
        return text_request_URI

    def __extract_ID_and_checksum(self, response):
        '''
        Parses xml response file and returns the track lyrics ID.
        
        @type responseFileName: string
        @param responseFileName: path of temp xml file to parse for lyrics ID
        @rtype: string
        @return: the track lyrics ID of song we look for
        '''
        tree = ET.parse(response)
        success = True
        for i in tree.getiterator('{http://api.chartlyrics.com/}LyricId'):
            lyrics_ID = i.text
        for i in \
            tree.getiterator('{http://api.chartlyrics.com/}LyricChecksum'):
            lyrics_checksum = i.text
        try:
            self.__lyrics_ID = lyrics_ID
            self.__lyrics_checksum = lyrics_checksum
            if (lyrics_checksum is None) or (lyrics_ID == 0):
                success = False
        except:
            success = False
        return success

    def __extract_text(self, response):
        '''
        Parses xml response file and sets song lyrics property.
        
        @type responseFileName: string
        @param responseFileName: path of the temp xml file to parse for lyrics
        @rtype: boolean
        @return: success extracting lyrics
        '''
        try:
            tree = ET.parse(response)
        except:
            return False
        for i in tree.getiterator('{http://api.chartlyrics.com/}Lyric'):
            text = i.text
        if text is None:
            return False
        else:
            self.__text = text
            return True

    def get_text(self):
        '''
        Return lyrics text string.
        
        @rtype: string       
        @return: lyrics text string'''
        return self.__text

    def set_text(self, artist, track):
        '''
        Retrieves the lyrics for a track by artist.
        
        @type artist: string
        @type track: string
        @param artist: name of artist to look for
        @param track: name of track we want the lyrics for
        @rtype: boolean
        @return: success in finding lyrics for that parameters
        '''
        self.__text = ''
        ID_request_URI = self.__build_searchrequest(artist, track)
        if self.query_server(ID_request_URI):
            self.__search_response = self.response
        else:
            return False # no success, no lyrics found
        if self.__extract_ID_and_checksum(self.__search_response):
            text_request_URI = self.__build_lyricsrequest(self.__lyrics_ID,
                                                     self.__lyrics_checksum)
            if self.query_server(text_request_URI):
                self.__lyrics_response = self.response
            if not self.__lyrics_response is None and \
                self.__extract_text(self.__lyrics_response):
                return True
            else:
                return False # no success, no lyrics found
        else:
            return False # no success, no lyrics found