# ============================================================
#################################
# guisettings_xml.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab3 > guisettings_xml.py
# type: backup and restore
# functionality: gui settings backup and restore of special://userdata/guisettings.xml
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
GUISETTINGS = configuration.GUISETTINGS
GUISETTINGS_FILE = configuration.GUISETTINGS_FILE
GUISETTINGS_FOLDER = configuration.GUISETTINGS_FOLDER
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_VALUE = configuration.TEXT_VALUE
USERDATA = configuration.USERDATA

# ============================================================
# Favourites
# ============================================================

Guisettings = ('[COLOR %s]guisettings_xml > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Guisettings_Backup
# ============================================================

def Guisettings_Backup():

	if not os.path.exists(GUISETTINGS_FOLDER):
		os.makedirs(GUISETTINGS_FOLDER)

	if os.path.exists(GUISETTINGS):
		shutil.copy(GUISETTINGS, GUISETTINGS_FOLDER)

		ADDON.setSetting('guisettings_backup_saved', Now())

		Notification(Addon_Title, '[COLOR %s]Backup GUI Settings: backup saved[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Guisettings + 'Backup GUI Settings: backup saved', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Backup GUI Settings: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Guisettings_Delete
# ============================================================

def Guisettings_Delete():

	if os.path.exists(GUISETTINGS_FILE):

		choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup GUI Settings: [LIGHT](MT_guisettings/guisettings.xml)[/LIGHT][CR][CR]Would you like to delete the GUI settings backup ?[/COLOR]' % TEXT_GENERAL, yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if choice == 0:
			return
		elif choice == 1:

			shutil.rmtree(GUISETTINGS_FOLDER)
			os.makedirs(GUISETTINGS_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup GUI Settings: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Guisettings + 'Delete Backup GUI Settings: backup deleted', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup GUI Settings: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Guisettings_Restore
# ============================================================

def Guisettings_Restore():

	if os.path.exists(GUISETTINGS_FILE):
		shutil.copy(GUISETTINGS_FILE, USERDATA)

		Notification(Addon_Title, '[COLOR %s]Restore GUI Settings: backup restored[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Guisettings + 'Restore GUI Settings: backup restored', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Restore GUI Settings: none found[/COLOR]' % TEXT_GENERAL)