# ============================================================
#################################
# sources_xml.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab3 > sources_xml.py
# type: backup and restore
# functionality: sources backup and restore of special://userdata/sources.xml
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

SOURCES = configuration.SOURCES
SOURCES_FILE = configuration.SOURCES_FILE
SOURCES_FOLDER = configuration.SOURCES_FOLDER
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_VALUE = configuration.TEXT_VALUE
USERDATA = configuration.USERDATA

# ============================================================
# Favourites
# ============================================================

Sources = ('[COLOR %s]sources_xml > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Sources_Backup
# ============================================================

def Sources_Backup():

	if not os.path.exists(SOURCES_FOLDER):
		os.makedirs(SOURCES_FOLDER)

	if os.path.exists(SOURCES):
		shutil.copy(SOURCES, SOURCES_FOLDER)

		Settings_Set('sources_backup_saved', Now())

		Notification(Addon_Title, '[COLOR %s]Backup Sources: backup saved[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Sources + 'Backup Sources: backup saved', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Backup Sources: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Sources_Delete
# ============================================================

def Sources_Delete():

	if os.path.exists(SOURCES_FILE):

		choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Sources: [LIGHT](MT_sources/sources.xml)[/LIGHT][CR][CR]Would you like to delete the sources backup ?[/COLOR]' % TEXT_GENERAL, yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if choice == 0:
			return
		elif choice == 1:

			shutil.rmtree(SOURCES_FOLDER)
			os.makedirs(SOURCES_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Sources: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Sources + 'Delete Backup Sources: backup deleted', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup Sources: none found[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Sources_Restore
# ============================================================

def Sources_Restore():

	if os.path.exists(SOURCES_FILE):
		shutil.copy(SOURCES_FILE, USERDATA)

		Notification(Addon_Title, '[COLOR %s]Restore Sources: backup restored[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Sources + 'Restore Sources: backup restored', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Restore Sources: none found[/COLOR]' % TEXT_GENERAL)