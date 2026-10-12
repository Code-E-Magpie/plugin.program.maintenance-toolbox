# ============================================================
#################################
# clear_surplus.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.openwizard > resources > libs > clear.py (drinfernoo)
# location: plugin.program.maintenance-toolbox > resources > lib > clear_surplus.py
# type: clear
# functionality: clear already installed add-on update files in packages and temp folders
# development:
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

import xbmc
import os, shutil

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Log, Log_Title, Notification, Now, Size_Convert

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
ADDONS_PACKAGES = configuration.ADDONS_PACKAGES
ADDONS_TEMP = configuration.ADDONS_TEMP
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL

# ============================================================
# Surplus
# ============================================================

Surplus = ('[COLOR %s]surplus > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# CONTROL FUNCTION: Clear_Surplus
# ============================================================

def Clear_Surplus():

	ADDON.setSetting('clear_addons_surplus_last_ran', Now())
	Clear_Addons_Surplus(ADDONS_PACKAGES)
	Clear_Addons_Surplus(ADDONS_TEMP)

# ============================================================
# CONTROL FUNCTION: Clear_Surplus_Startup
# ============================================================

def Clear_Surplus_Startup():

	ADDON.setSetting('startup_addons_surplus_last_ran', Now())
	Clear_Addons_Surplus(ADDONS_PACKAGES)
	Clear_Addons_Surplus(ADDONS_TEMP)

# ============================================================
# FUNCTION: Clear_Addons_Surplus
# ============================================================

def Clear_Addons_Surplus(folder_path):

	Folder_Path = ADDONS_PACKAGES if folder_path == ADDONS_PACKAGES else ADDONS_TEMP
	Message = 'Packages' if folder_path == ADDONS_PACKAGES else 'Temp'

	Log(Log_Title + Surplus + '[COLOR %s][LIGHT]Started (addons %s: //home/%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, Message.lower(), Folder_Path), xbmc.LOGINFO)

	deleted_files = 0
	deleted_folders = 0
	deleted_size = 0

	if not os.path.exists(folder_path):
		Log(Log_Title + Surplus + 'Clear Add-ons %s: folder not found' % Message, xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Add-ons %s: folder not found[/COLOR]' % (TEXT_GENERAL, Message))

	else:
		for root, dirs, files in os.walk(folder_path):
			for file_name in files:
				file_path = os.path.join(root, file_name)
				try:
					try:
						file_size = os.path.getsize(file_path)
					except OSError:
						file_size = 0
					os.unlink(file_path)
					deleted_files += 1
					deleted_size += file_size
					if ADDON.getSetting('log_details_for_clears') == 'true':
						Log(Log_Title + Surplus + '%s/%s deleted' % (root, file_name), xbmc.LOGINFO)

				except Exception as e:
					Log(Log_Title + Surplus + 'Clear Add-ons %s: failed to delete file %s %s' % (Message, file_path, e), xbmc.LOGINFO)

			for dir_name in list(dirs):
				dir_path = os.path.join(root, dir_name)
				try:
					shutil.rmtree(dir_path)
					deleted_folders += 1
					if ADDON.getSetting('log_details_for_clears') == 'true':
						Log(Log_Title + Surplus + '%s/%s deleted' % (root, dir_name), xbmc.LOGINFO)

				except Exception as e:
					Log(Log_Title + Surplus + 'Clear Add-ons %s: failed to delete folder %s %s' % (Message, dir_path, e), xbmc.LOGINFO)

	Log(Log_Title + Surplus + 'Clear Add-ons %s: %s / %s file(s) / %s folder(s) deleted' % (Message, Size_Convert(deleted_size), deleted_files, deleted_folders), xbmc.LOGINFO)
	if Message == 'Packages':
		Notification(Addon_Title, '[COLOR %s]Clear Add-ons %s: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(deleted_size), deleted_files))
	if Message == 'Temp':
		if deleted_files == 0:
			if ADDON.getSetting('skip_notifications_for_clears') == 'false':
				Notification(Addon_Title, '[COLOR %s]Clear Add-ons %s: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(deleted_size), deleted_files))
		else:
			Notification(Addon_Title, '[COLOR %s]Clear Add-ons %s: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(deleted_size), deleted_files))

	Log(Log_Title + Surplus + '[COLOR %s][LIGHT]Finished (addons %s: //home/%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, Message.lower(), Folder_Path), xbmc.LOGINFO)