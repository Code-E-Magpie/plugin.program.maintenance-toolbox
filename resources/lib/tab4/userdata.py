# ============================================================
#################################
# userdata.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab4 > userdata.py
# type: backup and restore
# functionality: userdata backup and delete backup of special://home/userdata excluding Thumbnails and addon_data folders + list userdata in text file
# development:
#	- last save date captured using ADDON.setSetting and visible in Settings
#	- functions consolidated to plugin.program.maintenance-toolbox > resources > lib > common > function.py
#	- variables consolidated to plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
#	- code debugged and reengineered if required using https://aipy.dev/tools

# ============================================================
# File used by
# ============================================================

# interface.py

# ============================================================
# Import
# ============================================================

import xbmc, xbmcgui
import os, shutil

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, List_Files, Log, Log_Title, Notification, Now

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_VALUE = configuration.TEXT_VALUE
USERDATA = configuration.USERDATA
USERDATA_FOLDER = configuration.USERDATA_FOLDER
USERDATA_LIST = configuration.USERDATA_LIST

# ============================================================
# Userdata
# ============================================================

Userdata = ('[COLOR %s]userdata > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Userdata_Backup
# ============================================================

def Userdata_Backup():

	if not os.path.exists(USERDATA_FOLDER):
		if os.path.exists(USERDATA):
			os.makedirs(USERDATA_FOLDER)

			for item in os.listdir(USERDATA):
				source_folder = os.path.join(USERDATA, item)
				destination_folder = os.path.join(USERDATA_FOLDER, item)
				exclude = ['addon_data', 'Thumbnails']

				if os.path.isdir(source_folder) and item in exclude:
					continue

				if os.path.isdir(source_folder):
					shutil.copytree(source_folder, destination_folder)
				else:
					shutil.copy2(source_folder, destination_folder)

			ADDON.setSetting('userdata_backup_saved', Now())
			List_Files(USERDATA, USERDATA_LIST)

			Notification(Addon_Title, '[COLOR %s]Backup Userdata: backup saved[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Userdata + 'Backup Userdata: backup saved', xbmc.LOGINFO)

	else:
			Dialogue.ok(Addon_Title, '[COLOR %s]Backup Userdata: [LIGHT](MT_userdata)[/LIGHT][CR][CR]Backup already exists: run Delete Backup Userdata[CR]Or move / rename backup folder to keep it and try again.[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Userdata_Delete
# ============================================================

def Userdata_Delete():

	if os.path.exists(USERDATA_FOLDER):

		choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Userdata: [LIGHT](MT_userdata)[/LIGHT][CR][CR]Would you like to delete the backup ?[/COLOR]' % TEXT_GENERAL, yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if choice == 0:
			return
		elif choice == 1:

			shutil.rmtree(USERDATA_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Userdata: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Userdata + 'Delete Backup Userdata: backup deleted', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup Userdata: none found[/COLOR]' % TEXT_GENERAL)