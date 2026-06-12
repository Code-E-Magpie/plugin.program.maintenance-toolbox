# ============================================================
#################################
# addons.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab4 > addons.py
# type: backup
# functionality: add-ons backup and delete backup of special://home/addons + list add-ons and built-in add-ons special://xbmcbinaddons/ in text file
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

import xbmc, xbmcgui, xbmcvfs
import os, shutil

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, List_Folders, Log, Log_Title, Notification, Now, Settings_Set

# ============================================================
# File used by
# ============================================================

# interface.py

# ============================================================
# Variables
# ============================================================

ADDONS = configuration.ADDONS
ADDONS_FOLDER = configuration.ADDONS_FOLDER
ADDONS_LIST = configuration.ADDONS_LIST
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
XBMCBINADDONS = configuration.XBMCBINADDONS
XBMCBINADDONS_LIST = configuration.XBMCBINADDONS_LIST

# ============================================================
# Addons
# ============================================================

Addons = ('[COLOR %s]addons > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Addons_Backup
# ============================================================

def Addons_Backup():

	if not os.path.exists(ADDONS_FOLDER):

		backup_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Backup Add-ons: [LIGHT](MT_addons)[/LIGHT] ~ 10 add-ons per minute[CR][COLOR %s]Kodi is unusable during this time. Message confirms completion.[/COLOR][CR][CR]Would you like to continue with the backup ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = '[COLOR %s]Continue Backup[/COLOR]' % TEXT_VALUE, nolabel = '[COLOR %s]Cancel Backup[/COLOR]' % TEXT_HIGHLIGHT)

		if backup_choice == 0:
			return
		elif backup_choice == 1:

			if os.path.exists(ADDONS):
				shutil.copytree(ADDONS, ADDONS_FOLDER)

				Settings_Set('addons_backup_saved', Now())
				List_Folders(ADDONS, ADDONS_LIST)
				List_Folders(XBMCBINADDONS, XBMCBINADDONS_LIST)

				Notification(Addon_Title, '[COLOR %s]Backup Add-ons: backup saved[/COLOR]' % TEXT_GENERAL)
				Log(Log_Title + Addons + 'Backup Add-ons: backup saved', xbmc.LOGINFO)
				Dialogue.ok(Addon_Title, '[COLOR %s]Backup Add-ons: [LIGHT](MT_addons)[CR][COLOR %s]Add-ons backup saved. Kodi is now usable.[/COLOR][CR]The "temp" and "packages" folders in the backup can be deleted.[/LIGHT][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	else:
			Dialogue.ok(Addon_Title, '[COLOR %s]Backup Add-ons: [LIGHT](MT_addons)[/LIGHT][CR][CR]Backup already exists: run Delete Backup Add-ons[CR]Or move / rename backup folder to keep it and try again.[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Addons_Delete
# ============================================================

def Addons_Delete():

	if os.path.exists(ADDONS_FOLDER):

		delete_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Add-ons: [LIGHT](MT_addons)[/LIGHT] ~ 20 add-ons per minute[CR][COLOR %s]Kodi is unusable during this time. Message confirms completion.[/COLOR][CR][CR]Would you like to delete the backup ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if delete_choice == 0:
			return
		elif delete_choice == 1:

			shutil.rmtree(ADDONS_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Add-ons: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Addons + 'Delete Backup Add-ons: backup deleted', xbmc.LOGINFO)
			Dialogue.ok(Addon_Title, '[COLOR %s]Delete Backup Add-ons: [LIGHT](MT_addons)[CR][COLOR %s]Add-ons backup deleted. Kodi is now usable.[/LIGHT][/COLOR][CR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	else:
			Notification(Addon_Title, '[COLOR %s]Delete Backup Add-ons: none found[/COLOR]' % TEXT_GENERAL)