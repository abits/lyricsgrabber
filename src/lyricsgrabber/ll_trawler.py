#==============================================================================
# ll_trawler.py - client for <http://www.leoslyrics.com/>
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
ll_trawler - searches and extracts lyrics against leoslyrics.com API.
@author: Christoph Martel
@copyright: Christoph Martel
@license: GPLv3
'''


import urllib2
import xml.etree.ElementTree as ET
import trawler


class LlTrawler(trawler.Trawler):

    '''
    Retrieves song lyrics from <http://www.leoslyrics.com/> via REST API.
    Response may be written to file.  Object initialization requires as 
    parameters a user id from the website for REST calls.
    
    A typical usage might look like:
        trawler = ll_trawler("duane")
        trawler.set_text(someArtist, someSong)
        if trawler.get_text() != '':    # make sure we have found lyrics
            lyrics = trawler.get_text() # read out the song lyrics
    
    If no lyrics are found the stored lyrics property of the object is set to
    an empty string.
    '''

    def __init__(self, UID):
        self.__API_search_URI = 'http://api.leoslyrics.com/api_search.php'
        self.__API_lyrics_URI = 'http://api.leoslyrics.com/api_lyrics.php'
        self.__response_HID = None
        self.__response_text = None
        self.__UID = UID  # use 'duane'
        self.__HID = ''
        self.__text = ''

    def __build_HID_request(self, artist, track):
        '''
        Constructs a url to query Leo's Lyrics for track id.
        
        @type artist: string
        @type track: string
        @param artist: name of the artist to search in lyrics database
        @param track: name of the song to retrieve lyrics for
        @rtype: string
        @return: uri to query Leo's Lyrics for a track id
        '''
        auth = 'auth=' + self.__UID
        artist = 'artist=' + urllib2.quote(artist.encode('utf-8'))
        track = 'songtitle=' + urllib2.quote(track.encode('utf-8'))
        param_list = [auth, artist, track]
        parameters = '&'.join(param_list)
        URI_list = [self.__API_search_URI, parameters]
        HID_request_URI = '?'.join(URI_list)
        return HID_request_URI

    def __build_text_request(self, HID):
        '''
        Constructs a url to query Leo's Lyrics for song lyrics.
        
        @type HID: string
        @param HID: track id from Leo's Lyric's database
        @rtype: string
        @return: uri to query Leo's Lyrics for song lyrics
        '''
        auth = 'auth=' + self.__UID
        HID = 'hid=' + HID
        param_list = [auth, HID]
        parameters = '&'.join(param_list)
        URI_list = [self.__API_lyrics_URI, parameters]
        text_request_URI = '?'.join(URI_list)
        return text_request_URI

    def __extract_HID(self, response):
        '''
        Parses xml response file and returns the track id.
        
        @type response: string
        @param response: path of the temp xml file to parse for hid
        @rtype: string
        @return: the track id of song we look for
        '''
        try:
            tree = ET.parse(response)
        except:
            return None
        if tree.find('*/result') == None:
            return None
        if tree.find('*/result').get('exactMatch') == 'true':
            hid = tree.find('*/result').get('hid')
            return hid
        else:
            return None

    def __extract_text(self, response):
        '''
        Parses xml response file and sets song lyrics property.
        
        @type response: string
        @param response: path of the temp xml file to parse for lyrics
        @rtype: boolean
        @return: success extracting lyrics
        '''
        try:
            tree = ET.parse(response)
        except:
            return None
        text = tree.findtext('lyric/text')
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
        HID_request_URI = self.__build_HID_request(artist, track) # build url
        if self.query_server(HID_request_URI): # ask server
            self.__response_HID = self.response
        self.__HID = self.__extract_HID(self.__response_HID) # parse response
        if self.__HID is not None:
            text_request_URI = self.__build_text_request(self.__HID)
            if self.query_server(text_request_URI):
                self.__response_text = self.response
            if not self.__response_text is None and \
                self.__extract_text(self.__response_text):
                return True
            else:
                return False # no success, no lyrics found
        else:
            return False # no success, no lyrics found
