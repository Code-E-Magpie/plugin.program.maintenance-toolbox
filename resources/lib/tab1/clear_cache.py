# ============================================================
#################################
# clear_cache.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.openwizard > resources > libs > clear.py (drinfernoo)
# location: plugin.program.maintenance-toolbox > resources > lib > clear_cache.py
# type: clear
# functionality: clear uninstalled and empty folders, database and folder cache and pycache folders
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

from pathlib import Path

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Log, Log_Title, Notification, Now, Size_Convert

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
ADDON_DATA = configuration.ADDON_DATA
ADDON_ID = configuration.ADDON_ID
ADDON_PATH = configuration.ADDON_PATH
ADDONS = configuration.ADDONS
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL
XBMCBINADDONS = configuration.XBMCBINADDONS

# ============================================================
# Cache / Database / Folders / Pycache
# ============================================================

Cache = ('[COLOR %s]cache > [/COLOR]' % TEXT_GENERAL)
Database = ('[COLOR %s]db files > [/COLOR]' % TEXT_GENERAL)
Folders = ('[COLOR %s]folders > [/COLOR]' % TEXT_GENERAL)
Pycache = ('[COLOR %s]pycache > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# CONTROL FUNCTION: Clear_Cache
# ============================================================

def Clear_Cache():

	ADDON.setSetting('clear_uninstalled_folders_last_ran', Now())
	Clear_Uninstalled_Folders()

	if ADDON.getSetting('clear_empty_addon_data_folders') == 'true':
		ADDON.setSetting('clear_empty_addon_data_folders_last_ran', Now())
		Clear_Empty_Folders(ADDON_DATA)
	else:
		Log(Log_Title + Cache + 'Clear Empty Add-on Data Folders: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Empty Add-on Data: not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_empty_addon_folders') == 'true':
		ADDON.setSetting('clear_empty_addon_folders_last_ran', Now())
		Clear_Empty_Folders(ADDONS)
	else:
		Log(Log_Title + Cache + 'Clear Empty Add-on Folders: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Empty Add-on: not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_cache_folders') == 'true':
		ADDON.setSetting('clear_cache_folders_last_ran', Now())
		Clear_Cache_Folders()
	else:
		Log(Log_Title + Cache + 'Clear Cache Folders: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Cache Folders: not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_database_cache_db') == 'true':
		ADDON.setSetting('clear_database_cache_db_last_ran', Now())
		Clear_Cache_Databases(ADDON_DATA, 'cache')
	else:
		Log(Log_Title + Cache + 'Clear Cache Databases: add-on data cache.db not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: add-on data cache.db not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_database_thumbs_db') == 'true':
		ADDON.setSetting('clear_database_thumbs_db_last_ran', Now())
		Clear_Cache_Databases(ADDON_DATA, 'thumbs')
	else:
		Log(Log_Title + Cache + 'Clear Cache Databases: add-on data thumbs.db not enable', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: add-on data thumbs.db not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_database_cache_db_addons') == 'true':
		ADDON.setSetting('clear_database_cache_db_addons_last_ran', Now())
		Clear_Cache_Databases(ADDONS, 'cache')
	else:
		Log(Log_Title + Cache + 'Clear Cache Databases: add-ons cache.db not enable', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: add-ons cache.db not enable[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_database_thumbs_db_addons') == 'true':
		ADDON.setSetting('clear_database_thumbs_db_addons_last_ran', Now())
		Clear_Cache_Databases(ADDONS, 'thumbs')
	else:
		Log(Log_Title + Cache + 'Clear Cache Databases: add-ons thumbs.db not enable', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: add-ons thumbs.db not enable[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_addon_pycache') == 'true':
		ADDON.setSetting('clear_addon_pycache_last_ran', Now())
		Clear_Pycache(ADDON_PATH)
	else:
		Log(Log_Title + Cache + 'Clear Add-on Pycache: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Add-on Pycache: not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_addon_resolveurl') == 'true':
		ADDON.setSetting('clear_addon_resolveurl_last_ran', Now())
		Clear_Addon_ResolveURL()
	else:
		Log(Log_Title + Cache + 'Clear Add-on ResolveURL: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Add-on ResolveURL: not enabled[/COLOR]' % TEXT_GENERAL)

	if ADDON.getSetting('clear_pycache_folders') == 'true':
		ADDON.setSetting('clear_pycache_folders_last_ran', Now())
		Clear_Pycache(ADDONS)
	else:
		Log(Log_Title + Cache + 'Clear Pycache Folders: not enabled', xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Pycache Folders: not enabled[/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Clear_Addon_ResolveURL
# ============================================================

def Clear_Addon_ResolveURL():		

	Log(Log_Title + Pycache + '[COLOR %s][LIGHT]Started (add-on resolveURL: //home/addons/script.module.resolveurl)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

	if xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)'):
		xbmc.executebuiltin('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')
		Log(Log_Title + Pycache + 'Clear Add-on ResolveURL: cache reset', xbmc.LOGINFO)

	Log(Log_Title + Pycache + '[COLOR %s][LIGHT]Finished (add-on resolveURL: //home/addons/script.module.resolveurl)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Cache_Databases
# ============================================================

def Clear_Cache_Databases(folder_path, db_type):

	Folder_Path = ('home/' + ADDONS) if folder_path == ADDONS else ADDON_DATA
	Message = 'add-ons' if folder_path == ADDONS else 'add-on data'

	Log(Log_Title + Database + '[COLOR %s][LIGHT]Started (cache databases: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, Folder_Path), xbmc.LOGINFO)

	cache_db_bytes = 0
	cache_db_files = 0
	thumbs_db_bytes = 0
	thumbs_db_files = 0

	for db_path in (folder_path,):
		if not os.path.exists(db_path):
			continue

		for dir_path, _, files in os.walk(db_path):
			for filename in files:
				file_lowercase = filename.casefold()
				file_path = Path(dir_path) / filename

				try:
					if db_type == 'cache':
						if "cache" in file_lowercase and file_lowercase.endswith(".db"):
							cache_db_files += 1
							cache_size = file_path.stat().st_size
							cache_db_bytes += cache_size
							file_path.unlink()
							if ADDON.getSetting('log_details_for_clears') == 'true':
								Log(Log_Title + Database + '%s deleted' % file_path, xbmc.LOGINFO)

					elif db_type == 'thumbs':
						if file_lowercase == "thumbs.db":
							thumbs_db_files += 1
							thumbs_size = file_path.stat().st_size
							thumbs_db_bytes += thumbs_size
							file_path.unlink()
							if ADDON.getSetting('log_details_for_clears') == 'true':
								Log(Log_Title + Database + '%s deleted' % file_path, xbmc.LOGINFO)

				except OSError as e:
					Log(Log_Title + Database + 'Clear Cache Databases: error %s' % str(e), xbmc.LOGERROR)

	if db_type == 'cache':
		Log(Log_Title + Database + 'Clear Cache Databases: %s cache.db %s / %s file(s) deleted' % (Message, Size_Convert(cache_db_bytes), cache_db_files), xbmc.LOGINFO)
		if cache_db_files > 0:
			Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: %s cache.db %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(cache_db_bytes), cache_db_files))
		else:
			if ADDON.getSetting('skip_notifications_for_clears') == 'false':
				Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: %s cache.db %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(cache_db_bytes), cache_db_files))

	if db_type == 'thumbs':
		Log(Log_Title + Database + 'Clear Cache Databases: %s thumbs.db %s / %s file(s) deleted' % (Message, Size_Convert(thumbs_db_bytes), thumbs_db_files), xbmc.LOGINFO)
		if thumbs_db_files > 0:
			Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: %s thumbs.db %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(thumbs_db_bytes), thumbs_db_files))
		else:
			if ADDON.getSetting('skip_notifications_for_clears') == 'false':
				Notification(Addon_Title, '[COLOR %s]Clear Cache Databases: %s thumbs.db %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(thumbs_db_bytes), thumbs_db_files))

	Log(Log_Title + Database + '[COLOR %s][LIGHT]Finished (cache databases: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, Folder_Path), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Cache_Folders
# ============================================================

def Clear_Cache_Folders():

	Log(Log_Title + Folders + '[COLOR %s][LIGHT]Started (cache folders: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, ADDON_DATA), xbmc.LOGINFO)

	cache_bytes = 0
	cache_files = 0
	cache_folders = 0

	for current_root, dirs, _ in os.walk(ADDON_DATA, topdown = True):
		for dirname in list(dirs):
			if "cache" in dirname.lower():
				cache_path = os.path.join(current_root, dirname)

				folder_bytes = 0
				folder_files = 0

				for dir_path, _, file_names in os.walk(cache_path):
					folder_files += len(file_names)
					for file_name in file_names:
						file_path = os.path.join(dir_path, file_name)

						try:
							folder_bytes += os.path.getsize(file_path)
						except FileNotFoundError:
							Log(Log_Title + Folders + 'Clear Cache Folders: not found %s' % file_path, xbmc.LOGERROR)
						except PermissionError as e:
							Log(Log_Title + Folders + 'Clear Cache Folders: error %s %s' % (file_path, str(e)), xbmc.LOGERROR)
						except OSError as e:
							Log(Log_Title + Folders + 'Clear Cache Folders: error %s %s' % (file_path, str(e)), xbmc.LOGERROR)

				try:
					shutil.rmtree(cache_path)
					if ADDON.getSetting('log_details_for_clears') == 'true':
						Log(Log_Title + Folders + '%s deleted' % cache_path, xbmc.LOGINFO)
				except FileNotFoundError:
					Log(Log_Title + Folders + 'Clear Cache Folders: not found %s' % cache_path, xbmc.LOGERROR)
				except PermissionError as e:
					Log(Log_Title + Folders + 'Clear Cache Folders: error %s %s' % (cache_path, str(e)), xbmc.LOGERROR)
				except OSError as e:
					Log(Log_Title + Folders + 'Clear Cache Folders: error %s %s' % (cache_path, str(e)), xbmc.LOGERROR)

				cache_folders += 1
				cache_bytes += folder_bytes
				cache_files += folder_files

				try:
					dirs.remove(dirname)
				except FileNotFoundError:
					Log(Log_Title + Folders + 'Clear Cache Folders: not found %s' % cache_path, xbmc.LOGERROR)
				except PermissionError as e:
					Log(Log_Title + Folders + 'Clear Cache Folders: error %s %s' % (cache_path, str(e)), xbmc.LOGERROR)
				except OSError as e:
					Log(Log_Title + Folders + 'Clear Cache Folders: error %s %s' % (cache_path, str(e)), xbmc.LOGERROR)

	Log(Log_Title + Folders + 'Clear Cache Folders: %s / %s file(s) / %s folder(s) deleted' % (Size_Convert(cache_bytes), cache_files, cache_folders), xbmc.LOGINFO)
	if cache_folders > 0:
		Notification(Addon_Title, '[COLOR %s]Clear Cache Folders: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Size_Convert(cache_bytes), cache_files))
	else:
		if ADDON.getSetting('skip_notifications_for_clears') == 'false':
			Notification(Addon_Title, '[COLOR %s]Clear Cache Folders: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Size_Convert(cache_bytes), cache_files))

	Log(Log_Title + Folders + '[COLOR %s][LIGHT]Finished (cache folders: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, ADDON_DATA), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Empty_Folders
# ============================================================

def Clear_Empty_Folders(folder_path):

	Folder_Path = ('home/' + ADDONS) if folder_path == ADDONS else ADDON_DATA
	Message = 'Add-ons' if folder_path == ADDONS else 'Add-on Data'

	Log(Log_Title + Folders + '[COLOR %s][LIGHT]Started (empty %s folders: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, Message.lower(), Folder_Path), xbmc.LOGINFO)

	count_empty_folders = 0
	folder_path_abs = os.path.abspath(folder_path)
	skip_folders = {"packages", "temp"}

	try:
		for root, dirs, files in os.walk(folder_path, topdown = False):
			root_abs = os.path.abspath(root)
			if root_abs == folder_path_abs:
				continue

			parent_abs = os.path.abspath(os.path.dirname(root_abs))
			base = os.path.basename(root_abs).lower()
			if parent_abs == folder_path_abs and base in skip_folders:
				Log(Log_Title + Folders + '%s folder skipped' % base, xbmc.LOGINFO)
				continue

			try:
				if not os.listdir(root_abs):
					os.rmdir(root_abs)

					count_empty_folders += 1
					if ADDON.getSetting('log_details_for_clears') == 'true':
						Log(Log_Title + Folders + '%s deleted' % root_abs, xbmc.LOGINFO)

			except OSError as e:
				Log(Log_Title + Folders + 'Clear Empty %s Folders: error %s %s' % (Message, root_abs, str(e)), xbmc.LOGERROR)
				continue

	except Exception as e:
		Log(Log_Title + Folders + 'Clear Empty %s Folders: error %s' % (Message, str(e)), xbmc.LOGERROR)
		return 0

	Log(Log_Title + Folders + 'Clear Empty %s Folders: %s deleted' % (Message, count_empty_folders), xbmc.LOGINFO)
	if count_empty_folders > 0:
		Notification(Addon_Title, '[COLOR %s]Clear Empty %s Folders: %s deleted[/COLOR]' % (TEXT_GENERAL, Message, count_empty_folders))
	else:
		if ADDON.getSetting('skip_notifications_for_clears') == 'false':
			Notification(Addon_Title, '[COLOR %s]Clear Empty %s Folders: %s deleted[/COLOR]' % (TEXT_GENERAL, Message, count_empty_folders))

	Log(Log_Title + Folders + '[COLOR %s][LIGHT]Finished (empty %s folders: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, Message.lower(), Folder_Path), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Pycache
# ============================================================

def Clear_Pycache(folder_path):

	Folder_Path = ('//home/' + ADDONS + '/') if folder_path == ADDONS else ADDON_ID
	Message = 'Pycache Folders' if folder_path == ADDONS else 'Add-on Pycache'

	Log(Log_Title + Pycache + '[COLOR %s][LIGHT]Started (%s: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, Message.lower(), Folder_Path), xbmc.LOGINFO)

	folder_count = 0
	total_bytes = 0

	for root, dirs, _ in os.walk(folder_path, topdown = True):
		if os.path.abspath(root) == os.path.abspath(ADDONS):
			dirs[:] = [dir for dir in dirs if dir not in (ADDON_ID, "script.module.resolveurl")]

		if "__pycache__" in dirs:
			pycache_path = os.path.join(root, "__pycache__")

			folder_bytes = 0

			for dir_path, _, file_names in os.walk(pycache_path):
				for file_name in file_names:
					file_path = os.path.join(dir_path, file_name)
					try:
						folder_bytes += os.path.getsize(file_path)
					except FileNotFoundError:
						Log(Log_Title + Pycache + 'Clear %s: not found %s' % (Message, file_path), xbmc.LOGERROR)
					except PermissionError as e:
						Log(Log_Title + Pycache + 'Clear %s: error %s %s' % (Message,file_path, str(e)), xbmc.LOGERROR)
					except OSError as e:
						Log(Log_Title + Pycache + 'Clear %s: error %s %s' % (Message, file_path, str(e)), xbmc.LOGERROR)

			try:
				shutil.rmtree(pycache_path)
				if ADDON.getSetting('log_details_for_clears') == 'true':
					if folder_path == ADDONS:
						Log(Log_Title + Pycache + '%s' % pycache_path.replace("addons/", "").replace("__pycache__", ""), xbmc.LOGINFO)
					else:
						Log(Log_Title + Pycache + '%s' % pycache_path.replace("addons", "").replace("/plugin.program.maintenance-toolbox", ""), xbmc.LOGINFO)

				folder_count += 1
				total_bytes += folder_bytes

			except FileNotFoundError:
				Log(Log_Title + Pycache + 'Clear %s: not found %s' % (Message, pycache_path), xbmc.LOGERROR)
			except PermissionError as e:
				Log(Log_Title + Pycache + 'Clear %s: error %s %s' % (Message, pycache_path, str(e)), xbmc.LOGERROR)
			except OSError as e:
				Log(Log_Title + Pycache + 'Clear %s: error %s %s' % (Message, pycache_path, str(e)), xbmc.LOGERROR)

			try:
				dirs.remove("__pycache__")
			except ValueError:
				Log(Log_Title + Pycache + 'Clear %s: error %s' % (Message, root), xbmc.LOGERROR)

	Log(Log_Title + Pycache + 'Clear %s: %s / %s folder(s) deleted' % (Message, Size_Convert(total_bytes), folder_count), xbmc.LOGINFO)
	if folder_count > 0:
		Notification(Addon_Title, '[COLOR %s]Clear %s: %s / %s[LIGHT] folder(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(total_bytes), folder_count))
	else:
		if ADDON.getSetting('skip_notifications_for_clears') == 'false':
			Notification(Addon_Title, '[COLOR %s]Clear %s: %s / %s[LIGHT] folder(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Message, Size_Convert(total_bytes), folder_count))

	Log(Log_Title + Pycache + '[COLOR %s][LIGHT]Finished (%s: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, Message.lower(), Folder_Path), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Uninstalled_Folders
# ============================================================

def Clear_Uninstalled_Folders():

	Log(Log_Title + Folders + '[COLOR %s][LIGHT]Started (uninstalled folders: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, ADDON_DATA), xbmc.LOGINFO)

	count_uninstalled_folders = 0

	addon_data_folders = os.listdir(ADDON_DATA)

	for folder in addon_data_folders:
		addon_data_path = os.path.join(ADDON_DATA, folder)
		xbmcbinaddons_path = os.path.join(XBMCBINADDONS, folder)
		addons_path = os.path.join(ADDONS, folder)

		if not os.path.exists(xbmcbinaddons_path) and not os.path.exists(addons_path):
			try:
				shutil.rmtree(addon_data_path)

				count_uninstalled_folders += 1
				if ADDON.getSetting('log_details_for_clears') == 'true':
					Log(Log_Title + Folders + '%s deleted' % addon_data_path, xbmc.LOGINFO)

			except (OSError, Exception) as e:
				Log(Log_Title + Folders + 'Clear Uninstalled Folders: error %s' % str(e), xbmc.LOGINFO)

	Log(Log_Title + Folders + 'Clear Uninstalled Folders: %s deleted' % count_uninstalled_folders, xbmc.LOGINFO)
	if count_uninstalled_folders > 0:
		Notification(Addon_Title, '[COLOR %s]Clear Uninstalled Folders: %s deleted[/COLOR]' % (TEXT_GENERAL, count_uninstalled_folders))
	elif ADDON.getSetting('skip_notifications_for_clears') == 'false':
		Notification(Addon_Title, '[COLOR %s]Clear Uninstalled Folders: %s deleted[/COLOR]' % (TEXT_GENERAL, count_uninstalled_folders))
	elif ADDON.getSetting('skip_notifications_for_clears') == 'true':
		Notification(Addon_Title, '[COLOR %s]Clear Cache + Folders: non zero values[/COLOR]' % TEXT_GENERAL)

	Log(Log_Title + Folders + '[COLOR %s][LIGHT]Finished (uninstalled folders: //%s/)[/LIGHT][/COLOR]' % (TEXT_DARK, ADDON_DATA), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Data_Cache_Databases
# ============================================================

def Data_Cache_Databases():

	cache_db_bytes = 0
	cache_db_files = 0
	thumbs_db_bytes = 0
	thumbs_db_files = 0

	for path in (ADDON_DATA, ADDONS):
		if not os.path.exists(path):
			continue

		for dir_path, _, files in os.walk(path):
			for filename in files:
				file_lowercase = filename.casefold()
				file_path = os.path.join(dir_path, filename)

				if "cache" in file_lowercase and file_lowercase.endswith(".db"):
					cache_db_files += 1
					try:
						cache_db_bytes += os.path.getsize(file_path)
					except OSError:
						Log(Log_Title + Cache + 'Database Cache: error %s' % file_path, xbmc.LOGERROR)
						pass
					continue

				if file_lowercase == "thumbs.db":
					thumbs_db_files += 1
					try:
						thumbs_db_bytes += os.path.getsize(file_path)
					except OSError:
						Log(Log_Title + Cache + 'Database Cache: error %s' % file_path, xbmc.LOGERROR)
						pass

	return cache_db_bytes, cache_db_files, thumbs_db_bytes, thumbs_db_files

# ============================================================
# FUNCTION: Data_Cache_Folders
# ============================================================

def Data_Cache_Folders():

	cache_bytes = 0
	cache_files = 0
	cache_folders = 0

	for current_root, dirs, _ in os.walk(ADDON_DATA, topdown = True):
		for dirname in list(dirs):
			if "cache" in dirname.lower():
				cache_path = os.path.join(current_root, dirname)

				folder_bytes = 0
				folder_files = 0

				for dir_path, _, file_names in os.walk(cache_path):
					folder_files += len(file_names)
					for file_name in file_names:
						file_path = os.path.join(dir_path, file_name)

						try:
							folder_bytes += os.path.getsize(file_path)
						except FileNotFoundError:
							Log(Log_Title + Cache + 'Data Cache Folders: not found %s' % file_path, xbmc.LOGERROR)
						except PermissionError as e:
							Log(Log_Title + Cache + 'Data Cache Folders: error %s %s' % (file_path, str(e)), xbmc.LOGERROR)
						except OSError as e:
							Log(Log_Title + Cache + 'Data Cache Folders: error %s %s' % (file_path, str(e)), xbmc.LOGERROR)

				cache_bytes += folder_bytes
				cache_files += folder_files
				cache_folders += 1

				try:
					dirs.remove(dirname)
				except FileNotFoundError:
					Log(Log_Title + Cache + 'Data Cache Folders: not found %s' % cache_path, xbmc.LOGERROR)
				except PermissionError as e:
					Log(Log_Title + Cache + 'Data Cache Folders: error %s %s' % (cache_path, str(e)), xbmc.LOGERROR)
				except OSError as e:
					Log(Log_Title + Cache + 'Data Cache Folders: error %s %s' % (cache_path, str(e)), xbmc.LOGERROR)

	return cache_bytes, cache_files, cache_folders