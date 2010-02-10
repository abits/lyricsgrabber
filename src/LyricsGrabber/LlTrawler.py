# -*- coding: utf-8 -*-
# LlTrawler.py - client for <http://www.leoslyrics.com/>
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

import urllib2
import xml.etree.ElementTree as ET

class LlTrawler():
    '''An object retrieves song lyrics from <http://www.leoslyrics.com/> via REST API.
    Response may be written to file.  Object initialization requires as parameters a user id 
    from the website for REST calls.
    
    A typical usage might look like:
        leoTrawler = LlTrawler("duane")
        leoTrawler.setText(someArtist, someSong)
        if leoTrawler.getText() != '':    # make sure we have found lyrics for that song
            lyrics = leoTrawler.getText() # read out the song lyrics
    
    If no lyrics are found the stored lyrics property of the object is set to an empty string.
    @author: Christoph Martel
    @copyright: Christoph Martel
    @license: GPLv3    
    '''
    def __init__(self, uid):
        self.apiSearchUri = 'http://api.leoslyrics.com/api_search.php'
        self.apiLyricsUri = 'http://api.leoslyrics.com/api_lyrics.php'   
        self.hidResponse = None
        self.textResponse = None
        self.uid = uid  # use 'duane'
        self.hid = ''
        self.text = ''
    
    def buildHidRequest(self, artist, track):
        '''constructs a url to query Leo's Lyrics for track id
        @type artist: string
        @type track: string
        @param artist: name of the artist to search in lyrics database
        @param track: name of the song to retrieve lyrics for
        @rtype: string
        @return: uri to query Leo's Lyrics for a track id'''
        auth = 'auth=' + self.uid
        artist = 'artist=' + urllib2.quote(artist.encode('utf-8'))
        track = 'songtitle=' + urllib2.quote(track.encode('utf-8'))
        paramList = [auth, artist, track]
        parameters = '&'.join(paramList)
        uriList = [self.apiSearchUri, parameters]
        hidRequestUri = '?'.join(uriList)
        return hidRequestUri
    
    def buildTextRequest(self, hid):
        '''constructs a url to query Leo's Lyrics for song lyrics
        @type hid: string
        @param hid: track id from Leo's Lyric's database
        @rtype: string
        @return: uri to query Leo's Lyrics for song lyrics'''
        auth = 'auth=' + self.uid 
        hid = 'hid=' + hid
        paramList = [auth, hid]
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
        hidRequestUri = self.buildHidRequest(artist, track) # build url
        self.hidResponse = self.queryServer(hidRequestUri)  # ask server
        self.hid = self.extractHid(self.hidResponse)         # parse response
        if self.hid != None:
            textRequestUri = self.buildTextRequest(self.hid)
            #print textRequestUri
            self.textResponse = self.queryServer(textRequestUri)
            if self.extractText(self.textResponse):
                return True
            else:
                return False # no success, no lyrics found
        else:
            return False # no success, no lyrics found
    
    def extractHid(self, response):
        '''parses xml response file and returns the track id
        @type responseFileName: string
        @param responseFileName: path of the temp xml file to parse for hid
        @rtype: string
        @return: the track id of song we look for'''
        tree = ET.parse(response)
        if tree.find('*/result') == None:
            return None
        if tree.find('*/result').get('exactMatch') == 'true':
            hid = tree.find('*/result').get('hid')
            return hid
        else:
            return None
    
    def extractText(self, response):
        '''parses xml response file and sets song lyrics property
        @type responseFileName: string
        @param responseFileName: path of the temp xml file to parse for lyrics
        @rtype: boolean
        @return: success extracting lyrics'''
        #response = unicode(response, 'utf-8').encode('latin-1')
        tree = ET.parse(response)
        text = tree.findtext('lyric/text')
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
        return self.text        