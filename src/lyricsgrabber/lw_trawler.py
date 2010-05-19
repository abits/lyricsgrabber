# -*- coding: utf-8 -*-
import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import urllib
import urllib2
import string
import sys
from threading import Thread
import time
import gtk
import gobject
gtk.gdk.threads_init()


class LwTrawler():
    def __init__(self, settings):
        self.__base_url = 'http://lyrics.wikia.com/'
        self.__url = ''
        self.__lyrics = ''
        self.add_attribution = False

    def __build_request(self, artist, track):
        self.__url = ''
        # capitalize words for wiki-conform url 
        artist = string.capwords(artist)
        # quote ? character in search terms
        artist = artist.replace('?', '%3F')
        track = track.replace('?', '%3F')
        # replace whitespace for wiki-conform url
        artist = artist.replace(' ', '_')
        track = track.replace(' ', '_')
        self.__url = self.__base_url + artist + ':' + track
        request = urllib2.Request(self.__url)
        return request
#
#    def set_text_in_thread(self, artist, track):
#        Thread(target=self.set_text, args=(artist, track,)).start()

    def __get_wiki_page(self, artist, track):
        response = None
        request = self.__build_request(artist, track)
        try:
            server_data = urllib2.urlopen(request)
        except:
            return None
        response = server_data.read()
        server_data.close()
        return response

    def set_text(self, artist, track):
        wiki_page = self.__get_wiki_page(artist, track)
        if wiki_page is not None:
            try:
                self.__lyrics = self.__filter(wiki_page)
                return True
            except:
                self.__lyrics = ''
                return False
        else:
            self.__lyrics = ''
            return False

    def get_text(self):
        return self.__lyrics

    def __filter(self, page):
        '''Extract the lyrics text from web content.'''
        tree = BeautifulSoup.BeautifulSoup(page)
        # get rid of comments
        unwanted_comments = tree.findAll(
            text=lambda text:isinstance(text, BeautifulSoup.Comment))
        for comment in unwanted_comments:
            comment.extract()
        # get rid of ads inside the lyricbox div
        unwanted_divs = tree.findAll('div', 'rtMatcher')
        for div in unwanted_divs:
            div.extract()
        # focus on the lyricbox div which contains the text
        filtered_page = tree.find('div', 'lyricbox')
        # convert <br /> tags to line breaks
        lyrics_lines = []
        for index, line in enumerate(filtered_page.contents):
            if str(line) == '<br />':
                if str(filtered_page.contents[index + 1]) == '<br />':
                    lyrics_lines.append('')
                else:
                    continue
            else:
                # convert char entities to string
                filtered_line = BeautifulStoneSoup(line,
                                                   convertEntities=\
                                          BeautifulStoneSoup.HTML_ENTITIES)
                lyrics_lines.append(str(filtered_line))
        #append cc-by-sa attribution end with empty line
        if self.add_attribution:
            attribution = '\nCC-BY-SA: <' + self.__url + '>\n'
            lyrics_lines.append(attribution)
        else:
            lyrics_lines.append('\n')
        # join the lines
        lyrics = '\n'.join(lyrics_lines)
        return lyrics
