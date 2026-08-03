# ============================================================
#################################
# addon_data.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab4 > addon_data.py
# type: backup and restore
# functionality: addon_data backup and delete backup of special://userdata/addon_data + list addon_data in text file
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

import xbmc, xbmcgui, xbmcvfs
import os, shutil

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, List_Folders, Log, Log_Title, Notification, Now

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
ADDON_DATA = configuration.ADDON_DATA
ADDON_DATA_FOLDER = configuration.ADDON_DATA_FOLDER
ADDON_DATA_LIST = configuration.ADDON_DATA_LIST
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE

# ============================================================
# Addon_Data
# ============================================================

Addon_Data = ('[COLOR %s]addon_data > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Addon_Data_Backup
# ============================================================

def Addon_Data_Backup():

	if not os.path.exists(ADDON_DATA_FOLDER):

		backup_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Backup Add-on Data: [LIGHT](MT_addon_data) ~ 10 seconds[CR][COLOR %s]Kodi is unusable during this time.[CR]Message confirms completion.[/LIGHT][/COLOR][CR]Would you like to continue with the backup ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = '[COLOR %s]Continue Backup[/COLOR]' % TEXT_VALUE, nolabel = '[COLOR %s]Cancel Backup[/COLOR]' % TEXT_HIGHLIGHT)

		if backup_choice == 0:
			return
		elif backup_choice == 1:

			if os.path.exists(ADDON_DATA):
				shutil.copytree(ADDON_DATA, ADDON_DATA_FOLDER)

				ADDON.setSetting('addon_data_backup_saved', Now())
				List_Folders(ADDON_DATA, ADDON_DATA_LIST)

				Notification(Addon_Title, '[COLOR %s]Backup Add-on Data: backup saved[/COLOR]' % TEXT_GENERAL)
				Log(Log_Title + Addon_Data + 'Backup Add-on Data: backup saved', xbmc.LOGINFO)
				Dialogue.ok(Addon_Title, '[COLOR %s]Backup Add-on Data: [LIGHT](MT_addon_data)[CR][COLOR %s]Add-on Data backup saved.[CR]Kodi is now usable.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	else:
			Dialogue.ok(Addon_Title, '[COLOR %s]Backup Add-on Data: [LIGHT](MT_addon_data)[CR][COLOR %s]Run Delete Backup Add-on Data[CR]or move / rename backup folder to keep it and try again.[/LIGHT][/COLOR][CR]Backup already exists.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

# ============================================================
# FUNCTION: Addon_Data_Delete
# ============================================================

def Addon_Data_Delete():

	if os.path.exists(ADDON_DATA_FOLDER):

		delete_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Add-on Data: [LIGHT](MT_addon_data) ~ 5 seconds[CR][COLOR %s]Kodi is unusable during this time.[CR]Message confirms completion.[/LIGHT][/COLOR][CR]Would you like to delete the backup ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if delete_choice == 0:
			return
		elif delete_choice == 1:

			shutil.rmtree(ADDON_DATA_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Add-on Data: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Addon_Data + 'Delete Backup Add-on Data: backup deleted', xbmc.LOGINFO)
			Dialogue.ok(Addon_Title, '[COLOR %s]Delete Backup Add-on Data: [LIGHT](MT_addon_data)[CR][COLOR %s]Add-on Data backup deleted.[CR]Kodi is now usable.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup Add-on Data: none found[/COLOR]' % TEXT_GENERAL)