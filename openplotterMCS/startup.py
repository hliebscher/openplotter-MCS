#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by GeDaD <https://github.com/Thomas-GeDaD/openplotter-MCS>
#                     
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.

import time, os, subprocess, sys
from openplotterSettings import language

# This class will be always called at startup. You should start here only GUI programs. Non GUI progrmas should be started as a services, see setup.py and myappPostInstall.py
class Start():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-MCS',currentLanguage)
		# "self.initialMessage" will be printed at startup if it has content. If not, the function "start" will not be called. Use trasnlatable text: _('Starting My App...')
		self.initialMessage = 'Starting MCS-APP'

	# this funtion will be called only if "self.initialMessage" has content.
	def start(self):
		green = '' # green messages will be printed in green after the "self.initialMessage"
		black = '' # black messages will be printed in black after the green message
		red = '' # red messages will be printed in red in a new line

		###############Start I2C 1-Wire device
		try:
			os.system("echo '0x18' | sudo tee /sys/class/i2c-adapter/i2c-1/delete_device")		    
		except:
			red=_("cannot delete ds2482 device")
		try:
			os.system("echo 'ds2482 0x18' | sudo tee /sys/class/i2c-adapter/i2c-1/new_device")
		except:
			red= _("creating 0X18 DS2482 as new_device not possible")

		green = _("I2C-1Wire Server started")
		########################
		
		
		time.sleep(1) # "check" function is called after "start" function, so if we start any program here we should wait some seconds before checking it. 
		return {'green': green,'black': black,'red': red}

# This class is called after "start" function and when the user checks the system
class Check():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-MCS',currentLanguage)
		# "self.initialMessage" will be printed when checking the system. If it is empty the function check will not be called. Use trasnlatable text: _('Checking My App...')
		self.initialMessage = _('Checking MCS-App running...')

	def check(self):
		green = '' # green messages will be printed in green after the "self.initialMessage"
		black = '' # black messages will be printed in black after the green message
		red = '' # red messages will be printed in red in a new line

		# check any feature and set the messages
		try:
			subprocess.check_output(['systemctl', 'is-active', 'openplotter-MCS-read.service']).decode('utf-8')
			green = _('service is running')
		except: black = _('service is not running')
		
		av = os.listdir("/sys/bus/i2c/drivers/")
		if "ds2482" not in av:
			red = _('ds2482_1-Wire device not availible, Please restart System')
			
		return {'green': green,'black': black,'red': red}

