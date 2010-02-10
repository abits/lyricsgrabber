#!/usr/bin/env python

from distutils.core import setup

setup(name='LyricsGrabber',
      version='0.1.1',
      description='finds song lyrics and stores them in MP3 tags',
      author='Chris Martel',
      author_email='accidentalbits@googlemail.com',
      license='GPL',
      url='http://gitorious.org/lyricsgrabber',
      package_dir = {'': 'src'},
      packages=['LyricsGrabber'],
      scripts=['src/lyricsgrabber']
     )