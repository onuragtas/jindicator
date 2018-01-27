#!/usr/bin/env python3
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

from supplier import *
from helper import human_readable as _h
from gettext import gettext as _

import os


class Indicator():
    menu_items = {}
    suppliers = {}
    active_suppliers = []

    LABEL_CPU = _('CPU') + ': {:.1f}%'
    LABEL_MEMORY = _('Mem') + ': {} ' + _('/') + ' {}'
    LABEL_SWAP = _('Swap') + ': {} ' + _('of') + ' {}'
    LABEL_DISK = _('Disk') + ': {} ' + _('of') + ' {}'
    LABEL_RECEIVING = _('Down') + ': {}/s'
    LABEL_SENDING = _('Up') + ': {}/s'

    NAME = 'Jindicator'
    DISPLAY_NAME = 'Jurix'
    VERSION = '1'
    LICENSE = 'GPL-3'
    COPYRIGHT = 'Copyright (C) 2018 Onur Ağtaş'
    WEBSITE = 'http://resoft.org'

    AUTHORS = [
        'Onur Ağtaş <agtasonur@gmail.com>',
    ]

    def __init__(self):
        self.app = 'jindicator'
        self.net = "jnet"
        self.mem = "jmem"
        iconpath = os.path.abspath("j.png")

        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())

        self.indicator_net = AppIndicator3.Indicator.new(
            self.net, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator_net.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator_net.set_menu(self.create_menu())

        self.indicator_mem = AppIndicator3.Indicator.new(
            self.mem, iconpath, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator_mem.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator_mem.set_menu(self.create_menu())

        self.suppliers['cpu'] = CpuSupplier(self)
        self.suppliers['memswap'] = MemSwapSupplier(self, 2)
        self.suppliers['disk'] = DiskSupplier(self, 2)
        self.suppliers['network'] = NetworkSupplier(self)

        self.active_suppliers = ['cpu', 'network', 'memswap', 'disk']

        for name in self.active_suppliers:
            self.suppliers[name].start()

    def create_menu(self):
        menu = Gtk.Menu()
        # menu item 1
        self.menu_items['cpu'] = Gtk.MenuItem('Cpu')
        menu.append(self.menu_items['cpu'])
        self.menu_items['separator_cpu'] = Gtk.SeparatorMenuItem("sep")
        menu.append(self.menu_items['separator_cpu'])

        self.menu_items['memory'] = Gtk.MenuItem("Memory")
        menu.append(self.menu_items['memory'])

        self.menu_items['swap'] = Gtk.MenuItem("swap")
        menu.append(self.menu_items['swap'])

        self.menu_items['separator_memswap'] = Gtk.SeparatorMenuItem("sep")
        menu.append(self.menu_items['separator_memswap'])

        self.menu_items['disk'] = Gtk.MenuItem("disk")
        menu.append(self.menu_items['disk'])

        self.menu_items['separator_disk'] = Gtk.SeparatorMenuItem("sep")
        menu.append(self.menu_items['separator_disk'])

        self.menu_items['receiving'] = Gtk.MenuItem("receiving")
        menu.append(self.menu_items['receiving'])

        self.menu_items['sending'] = Gtk.MenuItem("sending")
        menu.append(self.menu_items['sending'])

        self.menu_items['separator_network'] = Gtk.SeparatorMenuItem("sep")
        menu.append(self.menu_items['separator_network'])

        about = Gtk.MenuItem(_('About'))
        about.connect('activate', self.about)
        about.show()
        menu.append(about)

        # quit
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def stop(self, source):
        Gtk.main_quit()

    def update_cpu(self, percentage):
        self.menu_items['cpu'].set_label(
            self.LABEL_CPU.format(percentage)
        )
        self.indicator.set_label(self.LABEL_CPU.format(percentage), self.app)

    def update_memswap(self, mem_used, mem_total, swap_used, swap_total):
        self.menu_items['memory'].set_label(
            self.LABEL_MEMORY.format(_h(mem_used), _h(mem_total))
        )
        self.menu_items['swap'].set_label(
            self.LABEL_SWAP.format(_h(swap_used), _h(swap_total))
        )
        self.indicator_mem.set_label(self.LABEL_MEMORY.format(_h(mem_used), _h(
            mem_total))+" | "+self.LABEL_SWAP.format(_h(swap_used), _h(swap_total)), self.mem)

    def update_disk(self, used, total):
        self.menu_items['disk'].set_label(
            self.LABEL_DISK.format(_h(used), _h(total))
        )

    def update_network(self, receiving, sending):
        self.menu_items['receiving'].set_label(
            self.LABEL_RECEIVING.format(_h(receiving))
        )
        self.menu_items['sending'].set_label(
            self.LABEL_SENDING.format(_h(sending))
        )
        self.indicator_net.set_label(self.LABEL_RECEIVING.format(
            _h(receiving))+" | "+self.LABEL_SENDING.format(_h(sending)), self.net)

    def about(self, widget):
        self.aboutdialog = Gtk.AboutDialog()
        self.aboutdialog.set_name(self.DISPLAY_NAME)
        self.aboutdialog.set_version(self.VERSION)
        self.aboutdialog.set_copyright(self.COPYRIGHT)
        self.aboutdialog.set_website(self.WEBSITE)
        self.aboutdialog.set_authors(self.AUTHORS)
        self.aboutdialog.set_logo_icon_name(self.NAME)

        self.aboutdialog.connect('response', self.about_quit)
        self.aboutdialog.show()

    def about_quit(self, widget, event):
        self.aboutdialog.destroy()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
