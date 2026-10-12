# ============================================================
#################################
# clear_temp.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.openwizard > resources > libs > clear.py (drinfernoo)
# location: plugin.program.maintenance-toolbox > resources > lib > clear_temp.py
# type: clear
# functionality: clear temp and archive_cache folders
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
ARCHIVE_CACHE = configuration.ARCHIVE_CACHE
TEMP = configuration.TEMP
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL

# ============================================================
# Temp
# ============================================================

Temp = ('[COLOR %s]temp > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# CONTROL FUNCTION: Clear_Temp
# ============================================================

def Clear_Temp():

	if ADDON.getSetting('clear_archive_cache') == 'true':
		ADDON.setSetting('clear_archive_cache_last_ran', Now())
		Clear_Archive_Cache()
	else:
		Log(Log_Title + Temp + 'Clear Archive Cache: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Archive Cache: not enabled[/COLOR]' % TEXT_GENERAL)

	ADDON.setSetting('clear_temp_folder_last_ran', Now())
	Clear_Temp_Folder()

# ============================================================
# CONTROL FUNCTION: Clear_Temp_Startup
# ============================================================

def Clear_Temp_Startup():

	ADDON.setSetting('startup_temp_folder_last_ran', Now())
	Clear_Temp_Folder()

# ============================================================
# FUNCTION: Clear_Archive_Cache
# ============================================================

def Clear_Archive_Cache():

	Log(Log_Title + Temp + '[COLOR %s][LIGHT]Started (archive cache: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, ARCHIVE_CACHE), xbmc.LOGINFO)

	deleted_files = 0
	deleted_folders = 0
	deleted_size = 0

	if not os.path.exists(ARCHIVE_CACHE):
		Log(Log_Title + Temp + 'Clear Archive Cache: folder not found', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Archive Cache: folder not found[/COLOR]' % TEXT_GENERAL)

	else:
		for root, dirs, files in os.walk(ARCHIVE_CACHE):
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
						Log(Log_Title + Temp + '%s deleted' % file_path, xbmc.LOGINFO)

				except Exception as e:
					Log(Log_Title + Temp + 'Clear Archive Cache: failed to delete file %s %s' % (file_path, e), xbmc.LOGINFO)

			for dir_name in list(dirs):
				dir_path = os.path.join(root, dir_name)
				try:
					shutil.rmtree(dir_path)
					deleted_folders += 1
					if ADDON.getSetting('log_details_for_clears') == 'true':
						Log(Log_Title + Temp + '%s deleted' % dir_path, xbmc.LOGINFO)

				except Exception as e:
					Log(Log_Title + Temp + 'Clear Archive Cache: failed to delete folder %s %s' % (dir_path, e), xbmc.LOGINFO)

	Log(Log_Title + Temp + 'Clear Archive Cache: %s / %s file(s) / %s folder(s) deleted' % (Size_Convert(deleted_size), deleted_files, deleted_folders), xbmc.LOGINFO)
	Notification(Addon_Title, '[COLOR %s]Clear Archive Cache: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Size_Convert(deleted_size), deleted_files))

	Log(Log_Title + Temp + '[COLOR %s][LIGHT]Finished (archive cache: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, ARCHIVE_CACHE), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Temp_Folder
# ============================================================

def Clear_Temp_Folder():

	Log(Log_Title + Temp + '[COLOR %s][LIGHT]Started (temp folder: //%s excluding archive_cache & system logs)[/LIGHT][/COLOR]' % (TEXT_DARK, TEMP), xbmc.LOGINFO)

	if not os.path.exists(TEMP):
		Log(Log_Title + Temp + 'Clear Temp Folder: folder not found', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Temp Folder: folder not found[/COLOR]' % TEXT_GENERAL)
		return

	deleted_files = 0
	deleted_folders = 0
	deleted_size = 0

	for entry in os.listdir(TEMP):
		file_path = os.path.join(TEMP, entry)
		try:
			if os.path.isfile(file_path) and not entry.lower().endswith('.log'):
				try:
					file_size = os.path.getsize(file_path)
				except OSError:
					file_size = 0
				os.remove(file_path)
				deleted_files += 1
				deleted_size += file_size
				if ADDON.getSetting('log_details_for_clears') == 'true':
					Log(Log_Title + Temp + '%s deleted' % file_path, xbmc.LOGINFO)

		except Exception as e:
			Log(Log_Title + Temp + 'Clear Temp Folder: failed to delete file %s %s' % (file_path, e), xbmc.LOGINFO)

	for entry in os.listdir(TEMP):
		folder_path = os.path.join(TEMP, entry)
		if os.path.isdir(folder_path) and entry != 'archive_cache':
			try:
				shutil.rmtree(folder_path)
				deleted_folders += 1
				if ADDON.getSetting('log_details_for_clears') == 'true':
					Log(Log_Title + Temp + '%s deleted' % folder_path, xbmc.LOGINFO)

			except Exception as e:
				Log(Log_Title + Temp + 'Clear Temp Folder: failed to delete folder %s %s' % (folder_path, e), xbmc.LOGINFO)

	Log(Log_Title + Temp + 'Clear Temp Folder: %s / %s file(s) / %s folder(s) deleted' % (Size_Convert(deleted_size), deleted_files, deleted_folders), xbmc.LOGINFO)
	Notification(Addon_Title, '[COLOR %s]Clear Temp Folder: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Size_Convert(deleted_size), deleted_files))

	Log(Log_Title + Temp + '[COLOR %s][LIGHT]Finished (temp folder: //%s excluding archive_cache & system logs)[/LIGHT][/COLOR]' % (TEXT_DARK, TEMP), xbmc.LOGINFO)