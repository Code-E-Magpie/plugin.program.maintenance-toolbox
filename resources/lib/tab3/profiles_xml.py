# ============================================================
#################################
# profiles_xml.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab3 > profiles_xml.py
# type: backup and restore
# functionality: profiles backup and restore of special://userdata/profiles.xml
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
from resources.lib.common.function import Addon_Title, Dialogue, Log, Log_Title, Notification, Now

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
PROFILES = configuration.PROFILES
PROFILES_FILE = configuration.PROFILES_FILE
PROFILES_FOLDER = configuration.PROFILES_FOLDER
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
USERDATA = configuration.USERDATA

# ============================================================
# Favourites
# ============================================================

Profiles = ('[COLOR %s]profiles_xml > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Profiles_Backup
# ============================================================

def Profiles_Backup():

	if not os.path.exists(PROFILES_FOLDER):
		os.makedirs(PROFILES_FOLDER)

	if os.path.exists(PROFILES):
		shutil.copy(PROFILES, PROFILES_FOLDER)

		ADDON.setSetting('profiles_backup_save', Now())

		Notification(Addon_Title, '[COLOR %s]Backup Profiles: backup saved[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Profiles + 'Backup Profiles: backup saved', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Backup Profiles: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Profiles_Delete
# ============================================================

def Profiles_Delete():

	if os.path.exists(PROFILES_FILE):

		choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Profiles: [LIGHT](MT_profiles/profiles.xml)[CR][COLOR %s]Automatic tab refresh after Delete Backup.[CR]Automatic tab refresh after Keep Backup.[/LIGHT][/COLOR][CR]Would you like to delete the backup ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if choice == 0:
			return
		elif choice == 1:

			shutil.rmtree(PROFILES_FOLDER)
			os.makedirs(PROFILES_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Profiles: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Profiles + 'Delete Backup Profiles: backup deleted', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup Profiles: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Profiles_Restore
# ============================================================

def Profiles_Restore():

	if os.path.exists(PROFILES_FILE):
		shutil.copy(PROFILES_FILE, USERDATA)

		Notification(Addon_Title, '[COLOR %s]Restore Profiles: backup restored[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Profiles + 'Restore Profiles: backup restored', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Restore Profiles: none found[/COLOR]' % TEXT_GENERAL)