#==============================================================================
# trawler.py - client template for trawler modules
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
trawler - parent for client modules for lyrics API.
@author: Christoph Martel
@copyright: Christoph Martel
@license: GPLv3
'''

import time
import sys
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
        Queries the site in repeat loop.
        @type  request_URI: string
        @param request_URI: request as return by buildRequest method
        @rtype: boolean
        @return: did we successfully communicate with the server
        '''
        wait_period = 5
        retry_max = 1

        response_code = 0
        retry_counter = 0
        while retry_counter <= retry_max:
            retry_counter = retry_counter + 1
            response_code = self.query(request_URI)
            if response_code == 0:
                return True
            elif response_code == 104 and retry_max != 0:
                print "Waiting %s seconds to reconnect..." % wait_period
                time.sleep(wait_period)
            else:
                return False
        
            
    def query(self, request_URI): 
        '''
        Executes a single server query, sets temp file with response.        
        @type request_URI: string
        @param request_URI: request as return by buildRequest
        @rtype: int
        @return: response code for the wrapper loop query_server
        '''
        try:
            self.response = urllib2.urlopen(request_URI)
            return 0
        except urllib2.HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            self.response = None
            return 1
        except urllib2.URLError, e:
            print 'Failed to reach a server.'
            print 'Reason: ', e.reason
            self.response = None
            return 104
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.response = None
            return 1
        
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
