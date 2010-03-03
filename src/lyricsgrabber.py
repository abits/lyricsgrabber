#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lyricsgrabber.py - adds lyrics to MP3 files
#
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

'''
Lyricsgrabber is a python package which searches lyrics for
MP3s and embeds them in their tags.  Relies on leoslyrics.com,
chartlyrics.com, and eyeD3 for tagging.  You pass Lyricsgrabber a directory
or it automatically starts in the current working directory.  It then
collects all MP3 files in that directory, looks up their lyrics according
to artist and trackname tags and, if it finds some text, stores
them in the appropriate tag.  If successful, it should be possible to
view the song lyrics on your iPod.  You could make Lyricsgrabber search
for MP3 files recursively below the start directory.  Lyricsgrabber
features logging, so you could see what texts have been written to what
files.

Lyricsgrabber has an interactive mode: it display the text found
on the internet and ask the user whether it should be written to file.
Use the program at your own risk!

Usage: lyricsgrabber [OPTS] [directory]

Options:
    --version   show program’s version number and exit
    -h  display a short help text and exit
    -f  overwrite existing lyrics tags
    -i  interactive mode, ask user before writing to each file
    -o  LOGFILE save an activity log to LOGFILE
    -v  print log messages to stdout
    -r  scan directory recursively

'''


import os
import socket
from optparse import OptionParser
import lyricsgrabber.cl_trawler
import lyricsgrabber.ll_trawler
import lyricsgrabber.taghandler
import lyricsgrabber.walker
import lyricsgrabber.timer
import lyricsgrabber.logger


if __name__ == '__main__':
    # globals
    ignored_count = 0 # Files which have been found but won't be modified.
    file_count = 0 # Files that may be modified.
    modified_count = 0 # Files which have been modified.
    unresolved_count = 0 # Files where no lyrics could be found.
    files = [] # Holds file info to work with.

    timeout = 10
    socket.setdefaulttimeout(timeout)

    # Parse user options.
    usage = "usage: %prog [options] [DIRPATH]"
    parser = OptionParser(usage=usage, version="%prog 0.1.2")
    parser.add_option("-f", "--force", dest="force",
                      help="overwrite existing lyrics tags",
                      default=False, action="store_true")
    parser.add_option("-i", "--interactive", dest="interactive",
                      action="store_true",
                      help="ask for each file",
                      metavar="TRACK", default=False)
    parser.add_option("-o", "--output", dest="logFileName",
                      help="save text output in FILE",
                      metavar="FILE", default=None)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print status messages to stdout")
    parser.add_option("-r", "--recursive",
                      action="store_true", dest="recursive", default=False,
                      help="scan DIRPATH recursively for MP3 files")
    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")
    settings = {'verbose' : options.verbose,
                'force' : options.force,
                'logFileName' : options.logFileName,
                'interactive' : options.interactive,
                'recursive' : options.recursive}

    # Start logger and initialize components.
    logger = lyricsgrabber.logger.Logger(settings)
    log_string = ("\n\t verbose: %s\n\t force: %s\n\t interactive: %s" %
    	         (settings['verbose'],
    	          settings['force'],
    	          settings['interactive']))
    logger.add_to_log(log_string)
    walker = lyricsgrabber.walker.Walker(settings)
    tag_handler = lyricsgrabber.taghandler.TagHandler(settings)
    leo_trawler = lyricsgrabber.ll_trawler.LlTrawler("duane")
    chartlyrics_trawler = lyricsgrabber.cl_trawler.ClTrawler(settings)
    timer = lyricsgrabber.timer.Timer()

    # Initialize working directory.
    if len(args) == 0:
        work_directory = os.getcwd()
    else:
        work_directory = args[0]
    work_directory = os.path.abspath(work_directory)
    log_string = "Working on %s" % work_directory
    logger.add_to_log(log_string)

    # Scan work directory and web for lyrics, then modify MP3 file.
    timer.start()
    walker.walk(work_directory)
    ignored_count, file_count = walker.getFileCounts()
    files = walker.getFiles()

    # Retrieve lyrics for each file.
    for file in files:
        modified = False
        log_string = ("Searching lyrics for %s: %s" %
        	(file['artist'].encode('utf-8'), file['track'].encode('utf-8')))
        logger.add_to_log(log_string)
        if leo_trawler.set_text(file['artist'], file['track']) == True:
            lyrics = leo_trawler.get_text()
            if settings['interactive'] == True:
                print lyrics
                print
        # We need a second search attempt on another site.
        elif (chartlyrics_trawler.set_text(file['artist'], file['track']) ==
#        if (chartlyrics_trawler.set_text(file['artist'], file['track']) ==
              True):
            lyrics = chartlyrics_trawler.get_text()
            if settings['interactive'] == True:
                print lyrics
                print
        else: # we didn't find lyrics on the web
            unresolved_count += 1
            log_string = ("No lyrics found for file %s" %
            	         (os.path.basename(file['path'])))
            logger.add_to_log(log_string)
            continue # skip file go to next
        # So we found some lyrics on the web, add them to files.
        if lyrics != '':
            if settings['interactive'] == True: # we ask politely
                if (raw_input("\t=> Add text above to \"%s: %s\" [yn]? " %
                	(file['artist'], file['track'])) == 'y'):
                    modified = tag_handler.add_lyrics_from_string(file['path'],
                                                                  lyrics)
            else: # we don't care about user and write to file
                modified = tag_handler.add_lyrics_from_string(file['path'],
                                                              lyrics)
            if modified:
                modified_count += 1
                lyricslines = lyrics.splitlines()
                log_string = ("Added text \"%s...\" to file %s" %
                	          (lyricslines[0], os.path.basename(file['path'])))
            else:
                lyricslines = lyrics.splitlines()
                log_string = ("skipped file %s" %
                	          (os.path.basename(file['path'])))
            logger.add_to_log(log_string)
    timer.stop() # done working

    # Add runtime stats.
    log_string = "\n\tRunning time:\t%.2f sec\n" % (timer.getTime())
    log_string = log_string + \
                ("\tignored:\t%9d\n\
                  \ttried:\t\t%9d\n\
                  \tmodified:\t%9d\n\
                  \tunresolved:\t%9d" %
                  (ignored_count, file_count,
                   modified_count, unresolved_count))
    logger.add_to_log (log_string)
