# -*- coding: utf-8 -*-
# ClTrawler.py - client for <http://www.chartlyrics.com/>
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

import urllib, urllib2
import xml.etree.ElementTree as ET

class ClTrawler():
    '''An object retrieves song lyrics from <http://www.chartlyrics.com/> via REST API.
    Response may be written to file.
    
    A typical usage might look like:
        clTrawler = ClTrawler()
        clTrawler.setText(someArtist, someSong)
        if clTrawler.getText() != '':    # make sure we have found lyrics for that song
            lyrics = clTrawler.getText() # read out the song lyrics
    
    If no lyrics are found the stored lyrics property of the object is set to an empty string.
    @author: Christoph Martel
    @copyright: Christoph Martel
    @license: GPLv3
    '''
    def __init__(self, settings):
        self.settings = settings
        self.apiSearchUri = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyric'
        self.apiLyricsUri = 'http://api.chartlyrics.com/apiv1.asmx/GetLyric'   
        self.searchResponse = None
        self.lyricsResponse = None
        self.LyricChecksum = ''
        self.lyricId = ''
        self.text = ''
    
    def buildSearchRequest(self, artist, track):
        '''constructs a url to query ChartLyrics for track lyricId
        @type artist: string
        @type track: string
        @param artist: name of the artist to search in lyrics database
        @param track: name of the song to retrieve lyrics for
        @rtype: string
        @return: uri to query ChartLyrics for a track lyricId'''
        artist = 'artist=' + urllib2.quote(artist.encode('utf-8'))
        track = 'song=' + urllib2.quote(track.encode('utf-8'))
        paramList = [artist, track]
        parameters = '&'.join(paramList)
        uriList = [self.apiSearchUri, parameters]
        searchRequestUri = '?'.join(uriList)
        return searchRequestUri
    
    def buildLyricsRequest(self, lyricId, lyricChecksum):
        '''constructs a url to query ChartLyrics for song lyrics
        @type lyricId: string
        @param lyricId: track lyricId from Leo's Lyric's database
        @rtype: string
        @return: uri to query ChartLyrics for song lyrics'''
        lyricId = 'lyricId=' + self.lyricId        
        lyricChecksum = 'lyricCheckSum=' + self.lyricChecksum
        paramList = [lyricId, lyricChecksum]
        parameters = '&'.join(paramList)
        uriList = [self.apiLyricsUri, parameters]
        textRequestUri = '?'.join(uriList)
        return textRequestUri      
    
    def setText(self, artist, track):
        '''retrieves the lyrics for a track by artist
        @type artist: string
        @type track: string
        @param artist: name of artist to look for
        @param track: name of track we want the lyrics for
        @rtype: boolean
        @return: success in finding lyrics for that parameters'''
        self.text = ''
        lyricIdRequestUri = self.buildSearchRequest(artist, track) # build url
        self.searchResponse = self.queryServer(lyricIdRequestUri)  # ask server
        if self.extractIdAndCheckSum(self.searchResponse): # parse response
            textRequestUri = self.buildLyricsRequest(self.lyricId, self.LyricChecksum)
            self.lyricsResponse = self.queryServer(textRequestUri)
            if self.extractText(self.lyricsResponse):
                return True
            else:
                return False # no success, no lyrics found
        else:
            return False # no success, no lyrics found

    def extractIdAndCheckSum(self, response):
        '''parses xml response file and returns the track lyricId
        @type responseFileName: string
        @param responseFileName: path of the temp xml file to parse for lyricId
        @rtype: string
        @return: the track lyricId of song we look for'''
        tree = ET.parse(response)
        success = True
        for i in tree.getiterator('{http://api.chartlyrics.com/}LyricId'):
            lyricId = i.text
        for i in tree.getiterator('{http://api.chartlyrics.com/}LyricChecksum'):
            lyricChecksum = i.text
        try: 
            self.lyricId = lyricId
            self.lyricChecksum = lyricChecksum
            if (lyricChecksum == None) or (lyricId == 0):
                success = False
        except:
            success = False
        return success
    
    def extractText(self, response):
        '''parses xml response file and sets song lyrics property
        @type responseFileName: string
        @param responseFileName: path of the temp xml file to parse for lyrics
        @rtype: boolean
        @return: success extracting lyrics'''
        tree = ET.parse(response)
        for i in tree.getiterator('{http://api.chartlyrics.com/}Lyric'):
            text = i.text
        if text == None:
            return False
        else:
            self.text = text
            return True
    
    def queryServer(self, requestUri):
        '''queries the leoslyrics site, returns temp file name with response
        @type  requestUri: string
        @param requestUri: request as return by buildRequest method
        @rtype: string
        @return: name of temp file containing server response'''
        try:
            response = urllib2.urlopen(requestUri)
        except urllib2.URLError, e:
            print 'Error:' + e.read()
        return response

    def writeFile(self, response, filename):
        '''Write server response message to file
        @type response: string
        @type filename: string
        @param response: xml formatted string server response
        @param filename: name of file to store xml data'''
        xmlFile = open(filename, 'w')
        for line in response:
            xmlFile.write(line)
        xmlFile.close()       
    
    def getText(self):
        '''return lyrics text string
        @rtype: string       
        @return: lyrics text string'''
        #print type(self.text)
        #text = self.text.encode('ascii', 'replace')
        text = self.text
        return text