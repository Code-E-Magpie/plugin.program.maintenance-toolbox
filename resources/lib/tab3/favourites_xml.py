# ============================================================
#################################
# favourites_xml.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > wizard.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab3 > favourites_xml.py
# type: backup and restore
# functionality: favourites backup and restore of special://userdata/favourites.xml
# development:
#	- file content formatted
#	- some functions and variables renamed
#	- reworked Dialogue, Log and Notification
#	- last save date captured using Settings_Set and visible in Settings
#	- functions consolidated to plugin.program.maintenance-toolbox > resources > lib > common > function.py
#	- variables consolidated to plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
#	- code debugged and reengineered if required using https://aipy.dev/tools

# ============================================================
# Import
# ============================================================

import xbmc, xbmcgui
import os, re, shutil

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, Log, Log_Title, Notification, Now, Settings_Set

# ============================================================
# File used by
# ============================================================

# interface.py

# ============================================================
# Variables
# ============================================================

FAVOURITES = configuration.FAVOURITES
FAVOURITES_FILE = configuration.FAVOURITES_FILE
FAVOURITES_FOLDER = configuration.FAVOURITES_FOLDER
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_VALUE = configuration.TEXT_VALUE
USERDATA = configuration.USERDATA

# ============================================================
# Favourites
# ============================================================

Favourites = ('[COLOR %s]favourites_xml > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Favourites_Backup
# ============================================================

def Favourites_Backup():

	if not os.path.exists(FAVOURITES_FOLDER):
		os.makedirs(FAVOURITES_FOLDER)

	if os.path.exists(FAVOURITES):
		shutil.copy(FAVOURITES, FAVOURITES_FOLDER)

		Settings_Set('favourites_backup_saved', Now())

		Notification(Addon_Title, '[COLOR %s]Backup Favourites: backup saved[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Favourites + 'Backup Favourites: backup saved', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Backup Favourites: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Favourites_Delete
# ============================================================

def Favourites_Delete():

	if os.path.exists(FAVOURITES_FILE):

		choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Favourites: [LIGHT](MT_favourites/favourites.xml)[/LIGHT][CR][CR]Would you like to delete the favourites backup ?[/COLOR]' % TEXT_GENERAL, yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if choice == 0:
			return
		elif choice == 1:

			shutil.rmtree(FAVOURITES_FOLDER)
			os.makedirs(FAVOURITES_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Favourites: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Favourites + 'Delete Backup Favourites: backup deleted', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup Favourites: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Favourites_Restore
# ============================================================

def Favourites_Restore():

	if os.path.exists(FAVOURITES_FILE):
		shutil.copy(FAVOURITES_FILE, USERDATA)

		Notification(Addon_Title, '[COLOR %s]Restore Favourites: backup restored[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Favourites + 'Restore Favourites: backup restored', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Restore Favourites: none found[/COLOR]' % TEXT_GENERAL)
