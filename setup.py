#!/usr/bin/env python
#-*- coding:utf-8 -*-

import DistUtilsExtra.auto

DistUtilsExtra.auto.setup(
	name='jindicator',
	version='1.0',
	license='GPL-3',
	author='Onur Ağtaş',
	author_email='agtasonur@gmail.com',
	description='A system monitor indicator.',
	long_description='a system monitor indicator that displays CPU usage, memory usage, swap usage, disk usage and network traffic.',
	url='http://resoft.org',
	data_files=[
		('/etc/xdg/autostart', ['autostart/jindicator.desktop',]),
	],
)
