#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import gettext
_ = gettext.gettext
import gtk
import pygtk
pygtk.require('2.0')
from lyricsgrabber.walker import Walker
#from lyricsgrabber.cl_trawler import ClTrawler
import sys
#sys.path.append('/home/chm/Projekte/de.cmartel.python.lyricsgrabber/experimental')
from lyricsgrabber.lw_trawler import LwTrawler
from lyricsgrabber.taghandler import TagHandler
from gtkspell import Spell

class DirSelector():
    def __init__(self):
        self.dirchooser_dialog = gtk.Builder()
        self.dirchooser_dialog.add_from_file("gui/dirchooser.glade")
        self.dirchooser_dialog.connect_signals(self)
        self.dialog = \
            self.dirchooser_dialog.get_object('dirchooserdialog')
        self.checkbutton_recursive = \
            self.dirchooser_dialog.get_object('checkbutton_recursive')
        self.directory = None
        self.recursive = self.checkbutton_recursive.get_active()

    def quit(self):
        self.dialog.destroy()

    def on_button_cancel_clicked(self, *args):
        self.quit()

    def on_button_ok_clicked(self, *args):
        self.recursive = self.checkbutton_recursive.get_active()
        self.directory = self.dialog.get_filename()


class LyricsEditDialog():
    def __init__(self, selected_tracks):
        self.selected_tracks = selected_tracks
        self.selected_tracks_pointer = 0
        self.lyric_edit_dialog = gtk.Builder()
        self.lyric_edit_dialog.add_from_file("gui/lyricsedit.glade")
        self.lyric_edit_dialog.connect_signals(self)
        self.dialog = \
            self.lyric_edit_dialog.get_object('dialog_lyrics_edit')
        self.textbuffer = gtk.TextBuffer()
        self.textbuffer.connect('changed', self.on_textbuffer_changed)
        self.textview = self.lyric_edit_dialog.get_object('textview')
        self.textview.set_buffer(self.textbuffer)
        self.display_track(self.selected_tracks[self.selected_tracks_pointer])
        if len(self.selected_tracks) > 1:
            self.lyric_edit_dialog.get_object('toolbutton_next').\
                set_sensitive(True)
        self.spell_checker = None
        self.lyric_edit_dialog.get_object('toolbutton_save').\
            set_sensitive(False)

    def on_textbuffer_changed(self, *args):
        if self.textbuffer.get_modified() == False:
            self.textbuffer.set_modified(True)
        self.selected_tracks[self.selected_tracks_pointer]['modified'] = \
            self.textbuffer.get_modified()
        print self.selected_tracks[self.selected_tracks_pointer]
        self.lyric_edit_dialog.get_object('toolbutton_save').\
            set_sensitive(True)

    def store_track(self, track):
        pass

    def display_track(self, track):
        self.dialog.set_title(track['artist'] + ": " + track['title'])
        lyrics = track['lyrics']
        self.textbuffer.set_text(lyrics)

    def on_toolbutton_spell_toggled(self, *args):
        if not self.spell_checker:
            self.spell_checker = Spell(self.textview, 'en_US')
        else:
            self.spell_checker.detach()
            self.spell_checker = None

    def on_toolbutton_wrap_clicked(self, *args):
        pass

    def on_toolbutton_save_clicked(self, *args):
        pass

    def on_toolbutton_next_clicked(self, *args):
        self.lyric_edit_dialog.get_object('toolbutton_prev').\
            set_sensitive(True)
        if self.selected_tracks_pointer + 1 < len(self.selected_tracks) - 1:
            self.selected_tracks_pointer = self.selected_tracks_pointer + 1
            self.display_track(self.selected_tracks[self.selected_tracks_pointer])
        else:
            self.selected_tracks_pointer = self.selected_tracks_pointer + 1
            self.display_track(self.selected_tracks[self.selected_tracks_pointer])
            self.lyric_edit_dialog.get_object('toolbutton_next').\
                set_sensitive(False)

    def on_toolbutton_prev_clicked(self, *args):
        self.lyric_edit_dialog.get_object('toolbutton_next').\
            set_sensitive(True)
        if self.selected_tracks_pointer - 1 > 0:
            self.selected_tracks_pointer = self.selected_tracks_pointer - 1
            self.display_track(self.selected_tracks[self.selected_tracks_pointer])
        else:
            self.selected_tracks_pointer = self.selected_tracks_pointer - 1
            self.display_track(self.selected_tracks[self.selected_tracks_pointer])
            self.lyric_edit_dialog.get_object('toolbutton_prev').\
                set_sensitive(False)

    def on_button_save_and_quit_clicked(self, *args):
        pass

    def on_button_cancel_clicked(self, *args):
        self.quit()

    def on_toolbutton_search_show_menu(self, *args):
        pass

    def quit(self):
        self.dialog.destroy()

class Lyricsgrabber(object):
    def __init__(self):
        self.settings = { 'verbose' : True,
                          'force' : True,
                          'logFileName' : 'someString.log',
                          'interactive' : False,
                          'recursive' : True,
                          'timeout' : 10}

        self.main_window = gtk.Builder()
        self.main_window.add_from_file("gui/lyricsgrabber.glade")
        self.main_window.connect_signals(self)
        self.win = self.main_window.get_object('window_main')

        self.trackview = \
            self.main_window.get_object('trackview')
        self.trackstore = \
            gtk.ListStore(str, str, str, str, str, str, 'gboolean')
        self.trackview.set_model(self.trackstore)
        self.cell = gtk.CellRendererText()
        self.cell.set_property('weight', 400)
#        self.cell_bold = gtk.CellRendererText()
#        self.cell_bold.set_property('weight', 800)
        for pos, col_head in enumerate(
            [_('Artist'), _('Titel'), _('Album'), _('Text')]):
            col = gtk.TreeViewColumn(col_head, self.cell, text=pos)
            self.trackview.append_column(col)
        self.trackselection = self.trackview.get_selection()
        self.trackselection.set_mode(gtk.SELECTION_MULTIPLE)

        self.popup_trackview = self.main_window.get_object('menu_edit')

        self.trawler = LwTrawler(self.settings)

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass

    def quit(self):
        gtk.main_quit()

    def select_directory(self):
        dir_selector = DirSelector()
        dir_selector.checkbutton_recursive.set_active(
            self.settings['recursive'])
        result = dir_selector.dialog.run()
        top_directory = dir_selector.directory
        self.settings['recursive'] = dir_selector.recursive
        dir_selector.quit()
        if top_directory is not None:
            self.update_list(top_directory)

    def show_application_info(self):
        about_dialog = gtk.AboutDialog()
        about_dialog.connect("response", lambda d, r: d.destroy())
        about_dialog.set_authors(["Chris Martel"])
        about_dialog.set_comments(_("Liedtexte finden & in MP3 schreiben"))
        about_dialog.set_copyright("Copyright (C) 2010 Chris Martel")
        about_dialog.set_wrap_license(True)
        about_dialog.set_license("This program is free software; " +
        "you can redistribute it and/or modify it " +
        "under the terms of the GNU General Public License as published by " +
        "the Free Software Foundation; either version 3 of the License, or " +
        "(at your option) any later version. " +
        "This program is distributed in the hope that it will be useful, " +
        "but WITHOUT ANY WARRANTY; without even the implied warranty of " +
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU " +
        "General Public License for more details. " +
        "\n" +
        "You should have received a copy of the GNU General Public License " +
        "along with this program; if not, see <http://www.gnu.org/licenses/>.")
        about_dialog.set_name("LyricsGrabber")
        about_dialog.set_version("0.1.3")
        about_dialog.set_website("http://lyricsgrabber.sourceforge.net/")
        about_dialog.run()

    def preview_string(self, lyrics): # CODE: this might go in taghandler...
        lines = lyrics.splitlines()
        preview_length = 60
        preview = ''
        if lyrics == '':
            return lyrics
        i = 0
        for line in lines:
            words = line.split()
            for word in words:
                if len(preview) <= (preview_length - (len(word) + 1)):
                    preview = preview + " " + word
                else:
                    break
            preview = preview + " / "
        return preview.strip(' / ') + '...'

    def update_list(self, top_directory):
        self.trackstore.clear()
        walker = Walker(self.settings)
        walker.walk(top_directory)
        trackdata = walker.getFiles()
        (ignored, added) = walker.getFileCounts()
        for track in trackdata:
            row = [track['artist'], \
                   track['track'], \
                   track['album'], \
                   self.preview_string(track['lyrics']), \
                   track['lyrics'], \
                   track['path'], \
                   track['modified']]
            self.trackstore.append(row)

    def mark_as_modified(self, row):
        pass


    def get_track_info(self, pathlist):
        selected_tracks = []
        for path in pathlist:
            track = {
                'artist' : '',
                'title' : '',
                'album' : '',
                'path' : '',
                'preview' : '',
                'lyrics' : '',
                'row' : None,
                'modified' : False }
            iter = self.trackstore.get_iter(path)
            track['row'] = iter
            track['artist'] = self.trackstore.get_value(iter, 0)
            track['title'] = self.trackstore.get_value(iter, 1)
            track['album'] = self.trackstore.get_value(iter, 2)
            track['preview'] = self.trackstore.get_value(iter, 3)
            track['lyrics'] = self.trackstore.get_value(iter, 4)
            track['path'] = self.trackstore.get_value(iter, 5)
            track['modified'] = self.trackstore.get_value(iter, 6)
            selected_tracks.append(track)
        return selected_tracks

    def grab_lyrics(self):
        (model, pathlist) = self.trackselection.get_selected_rows()
        for track in self.get_track_info(pathlist):
            if self.trawler.set_text(str(track['artist']), str(track['title'])):
                lyrics = self.trawler.get_text()
                print track['artist'], track['title']
                print lyrics
                print
                self.trackstore.set(track['row'],
                                    3, self.preview_string(lyrics))
                self.trackstore.set(track['row'], 4, lyrics)
                if lyrics != '':
                    self.trackstore.set(track['row'], 6, True)

    def edit_lyrics(self):
        (model, pathlist) = self.trackselection.get_selected_rows()
        selected_tracks = self.get_track_info(pathlist)
        edit_dialog = LyricsEditDialog(selected_tracks)
        result = edit_dialog.dialog.run()
        edit_dialog.quit()

    def save_modified(self):
        tH = TagHandler(self.settings)
        for row in self.trackstore:
            iter = row.iter
            modified = self.trackstore.get_value(iter, 6)
            if modified:
                path = self.trackstore.get_value(iter, 5)
                lyrics = self.trackstore.get_value(iter, 4)
                if tH.add_lyrics_from_string(path, lyrics):
                    self.trackstore.set(iter, 6, False)

    ##########################################################################
    # event handlers
    ##########################################################################

    def on_window_main_delete_event(self, *args):
        self.quit()

    def on_imagemenuitem_file_open_activate(self, *args):
        self.select_directory()

    def on_imagemenuitem_file_save_activate(self, *args):
        self.save_modified()

    def on_imagemenuitem_file_quit_activate(self, *args):
        self.quit()

    def on_imagemenuitem_edit_grablyrics_activate(self, *args):
        if self.trackselection.count_selected_rows() > 0:
            self.grab_lyrics()

    def on_menuitem_edit_editlyrics_activate(self, *args):
        if self.trackselection.count_selected_rows() > 0:
            self.edit_lyrics()

    def on_imagemenuitem_edit_options_activate(self, *args):
        print "menu edit options"

    def on_imagemenuitem_help_about_activate(self, *args):
        self.show_application_info()

    def on_toolbutton_open_clicked(self, *args):
        self.select_directory()

    def on_toolbutton_save_clicked(self, *args):
        self.save_modified()

    def on_toolbutton_grablyrics_clicked(self, *args):
        self.grab_lyrics()

    def on_toolbutton_editlyrics_clicked(self, *args):
        self.edit_lyrics()

    def on_toolbutton_options_clicked(self, *args):
        print "toolbutton options"

    def on_trackview_trackdata_row_activated(self, *args):
        print "treeview row activated"

    def on_trackview_button_press_event(self, treeview, event):
        if event.button == 3:
            self.popup_trackview.popup(None, None, None,
                                       event.button, event.time)
            return True


def main():
    app = Lyricsgrabber()
    app.run()
    return 0

if __name__ == '__main__':
    main()
