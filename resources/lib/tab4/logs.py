# ============================================================
#################################
# logs.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab4 > logs.py
# type: log
# functionality: new system log and old system log backup and delete backup of special://logpath + list logs in text file
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
from resources.lib.common.function import Addon_Title, Dialogue, List_Logs, Log, Log_Title, Notification, Now

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
LOG_NEW = configuration.LOG_NEW
LOG_OLD = configuration.LOG_OLD
LOGPATH = configuration.LOGPATH
LOGS_FOLDER = configuration.LOGS_FOLDER
LOGS_LIST = configuration.LOGS_LIST
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE

# ============================================================
# Logs
# ============================================================

Logs = ('[COLOR %s]logs > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Logs_Backup
# ============================================================

def Logs_Backup():

	if not os.path.exists(LOGS_FOLDER):
		os.makedirs(LOGS_FOLDER)

		if os.path.exists(LOGPATH):
			for item in os.listdir(LOGPATH):

				if item.endswith('.log'):
					source_file = os.path.join(LOGPATH, item)
					destination_file = os.path.join(LOGS_FOLDER, item)
					shutil.copy(source_file, destination_file)

					ADDON.setSetting('logs_backup_save', Now())
					List_Logs(LOGPATH, LOGS_LIST)

					Notification(Addon_Title, '[COLOR %s]Backup Logs: backup saved[/COLOR]' % TEXT_GENERAL)
					Log(Log_Title + Logs + 'Backup Logs: backup saved', xbmc.LOGINFO)

	else:
			Dialogue.ok(Addon_Title, '[COLOR %s]Backup Logs: [LIGHT](MT_logs)[CR][COLOR %s]Run Delete Backup Logs or[CR]move / rename backup folder to keep it and try again.[/LIGHT][/COLOR][CR]Backup already exists.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

# ============================================================
# FUNCTION: Logs_Delete
# ============================================================

def Logs_Delete():

	if os.path.exists(LOGS_FOLDER):

		choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Delete Backup Logs: [LIGHT](MT_logs)[CR][COLOR %s]Automatic tab refresh after Delete Backup.[CR]Automatic tab refresh after Keep Backup.[/LIGHT][/COLOR][CR]Would you like to delete the backup ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Delete Backup[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Backup[/COLOR]' % TEXT_HIGHLIGHT))

		if choice == 0:
			return
		elif choice == 1:

			shutil.rmtree(LOGS_FOLDER)

			Notification(Addon_Title, '[COLOR %s]Delete Backup Logs: backup deleted[/COLOR]' % TEXT_GENERAL)
			Log(Log_Title + Logs + 'Delete Backup Logs: backup deleted', xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]Delete Backup Logs: none found[/COLOR]' % TEXT_GENERAL)