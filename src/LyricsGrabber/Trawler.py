#==============================================================================
# Trawler.py - client template for trawler modules
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
Trawler - parent for client modules for lyrics API.
@author: Christoph Martel
@copyright: Christoph Martel
@license: GPLv3
'''


import urllib2
import xml.etree.ElementTree as ET


class Trawler():

    '''
    A super class to retrieve song lyrics via REST API.
    Response may be written to file.  Used as template for subclasses
    which serve as clients for websites.  Since requests differ from site
    to site as does the response xml data, this class does not offer
    request and parsing methods.  They have to be supplied by the 
    sub-classed client module.
    '''

    def __init__(self):
        self.response = None

    def query_server(self, request_URI):
        '''
        Queries the leoslyrics site, sets temp file name with response.
        
        @type  request_URI: string
        @param request_URI: request as return by buildRequest method
        @rtype: boolean
        @return: did we successfully communicate with the server
        '''
        try:
            self.response = urllib2.urlopen(request_URI)
            return True
        except:
            return False

    def write_file(self, response, filename):
        '''
        Write server response message to file.
        
        @type response: string
        @type filename: string
        @param response: xml formatted string server response
        @param filename: name of file to store xml data
        '''
        xml_file = open(filename, 'w')
        for line in response:
            xml_file.write(line)
        xml_file.close()
