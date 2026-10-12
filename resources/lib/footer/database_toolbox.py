# ============================================================
#################################
# database_toolbox.py by Code-E-Magpie
#################################
# ============================================================

# ============================================================
# File information
# ============================================================

# sourced from: plugin.program.database-toolbox > database_toolbox.py
# location: plugin.program.maintenance-toolbox > resources > lib > footer > database_toolbox.py
# type: footer
# functionality: database toolbox
# development:
#	- functions consolidated to plugin.program.maintenance-toolbox > resources > lib > common > function.py
#	- variables consolidated to plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
#	- code debugged and reengineered if required using https://aipy.dev/tools

# ============================================================
# File used by
# ============================================================

# footer_menu.py

# ============================================================
# Import
# ============================================================

import xbmc, xbmcgui, xbmcvfs
import fnmatch, glob, os, re, sqlite3, sys

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Addons_Db, Dialogue, Log, Log_Title, Notification, Size_Convert

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
DATABASE = configuration.DATABASE
SIZE_HIGHLIGHT = ADDON.getSetting('size_highlight')
TEXT_DARK = configuration.TEXT_DARK
TEXT_DIM = configuration.TEXT_DIM
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE

# ============================================================
# Addons / Clean_db / Delete_db
# ============================================================

Addons = ('[COLOR %s]addons > [/COLOR]' % TEXT_GENERAL)
Clean_db = ('[COLOR %s]clean db > [/COLOR]' % TEXT_GENERAL)
Delete_db = ('[COLOR %s]delete db > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Clean_Addons_Database
# ============================================================

def Clean_Addons_Database():

	addons_db = Addons_Db()
	success = False

	Log(Log_Title + Addons + '[COLOR %s][LIGHT]Started (addons database: //database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)

	Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Close other add-ons and save any changes.[CR]Restart Kodi if required.[/LIGHT][/COLOR][CR]Backup %s database before proceeding.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db))

	addons_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]%s clean (empty) tables except installed and version.[CR]Kodi will need to close without cleanup at the end.[/LIGHT][/COLOR][CR]Would you like to continue ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db), yeslabel = ('[COLOR %s]Clean Database[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel Clean[/COLOR]' % TEXT_HIGHLIGHT))

	if not addons_choice:
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Cancelled (addons database: //database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		return False # replaced sys.exit()

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		cursor.execute('DELETE FROM addonlinkrepo;')
		cursor.execute('DELETE FROM addons;')
		cursor.execute('DELETE FROM package;')
		cursor.execute('DELETE FROM repo;')
		cursor.execute('DELETE FROM update_rules;')

		connection.commit()
		success = True

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to clean addons database: [COLOR %s]%s[/COLOR][CR]The database is locked or may not exist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '%s read error %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return False

	finally:
		try:
			if cursor is not None:
				try:
					cursor.close()
				except Exception as e:
					Log(Log_Title + Addons + '%s cursor close error %s' % (addons_db, str(e)), xbmc.LOGERROR)
		finally:
			try:
				if connection is not None:
					try:
						connection.close()
					except Exception as e:
						Log(Log_Title + Addons + '%s connection close error %s' % (addons_db, str(e)), xbmc.LOGERROR)
			except Exception:
				pass

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		cursor.execute('VACUUM;')

		connection.commit()
		Log(Log_Title + Addons + 'Clean Addons Database: vacuumed [LIGHT] (%s)[/LIGHT]' % addons_db, xbmc.LOGINFO)

	except sqlite3.Error as e:
		Log(Log_Title + Addons + '%s vacuum error %s' % (addons_db, str(e)), xbmc.LOGERROR)

	finally:
		if cursor is not None:
			try:
				cursor.close()
			except Exception:
				pass
		if connection is not None:
			try:
				connection.close()
			except Exception:
				pass

	if success:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Cleaned addons database: [COLOR %s]%s[/COLOR][CR]Kodi will need to close without cleanup.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Finished (addons database: //database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		xbmc.executebuiltin('Quit')
#	replaced os._exit(1) with xbmc.executebuiltin('Quit') could use return True
	return False

# ============================================================
# FUNCTION: Clean_Database
# ============================================================

def Clean_Database(database_selected):

	Log(Log_Title + Clean_db + '[COLOR %s][LIGHT]Started (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)

	if not os.path.exists(database_selected):
		Log(Log_Title + Clean_db + '%s not found' % database_selected, xbmc.LOGERROR)
		return False

	database_path = database_selected.replace('\\', '/').split('/')
	database_name = database_path[-1]
	database_text = ('[COLOR %s] > %s > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, database_path[-2] if len(database_path) >= 2 else '', TEXT_DARK, database_name))

	database_bytes = os.path.getsize(database_selected)
	database_size = Size_Convert(database_bytes)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(database_selected)
		cursor = connection.cursor()

		cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
		tables = [row[0] for row in cursor.fetchall()]

		if not tables:
			Log(Log_Title + Clean_db + '%s no user tables found' % database_selected, xbmc.LOGINFO)
			return True

		for table in tables:
			if table == 'version':
				Log(Log_Title + Clean_db + '%s table skipped' % table, xbmc.LOGINFO)
				continue

			if not table.replace('_', '').isalnum():
				Log(Log_Title + Clean_db + '%s invalid table name skipped' % table, xbmc.LOGERROR)
				continue

			try:
				safe_table = table.replace('"', '""')
				sql = 'DELETE FROM "{}"'.format(safe_table)
				cursor.execute(sql)
				Log(Log_Title + Clean_db + '%s table cleaned [LIGHT](emptied)[/LIGHT]' % table, xbmc.LOGINFO)

			except Exception as e:
				Log(Log_Title + Clean_db + '%s remove table error %s' % (table, str(e)), xbmc.LOGERROR)

		connection.commit()

	except sqlite3.Error as e:
		Log(Log_Title + Clean_db + '%s connection error %s' % (database_selected, str(e)), xbmc.LOGERROR)
		return False

	finally:
		if cursor is not None:
			try:
				cursor.close()
			except Exception as e:
				Log(Log_Title + Clean_db + '%s cursor close error %s' % (database_selected, str(e)), xbmc.LOGERROR)
		if connection is not None:
			try:
				connection.close()
			except Exception as e:
				Log(Log_Title + Clean_db + '%s connection close error %s' % (database_selected, str(e)), xbmc.LOGERROR)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(database_selected)
		cursor = connection.cursor()

		cursor.execute("VACUUM;")

		connection.commit()

		Log(Log_Title + Clean_db + 'vacuumed %s' % database_name, xbmc.LOGINFO)

	except sqlite3.Error as e:
		Log(Log_Title + Clean_db + '%s vacuum error %s' % (database_selected, str(e)), xbmc.LOGERROR)

	finally:
		try:
			if cursor is not None:
				cursor.close()
		except Exception:
			pass
		try:
			if connection is not None:
				connection.close()
		except Exception:
			pass

	database_bytes_after = os.path.getsize(database_selected)
	database_size_after = Size_Convert(database_bytes_after)

	Log(Log_Title + Clean_db + 'vacuumed reduction %s [LIGHT](start %s  finish %s)[/LIGHT]' % (Size_Convert(database_bytes - database_bytes_after), database_size, database_size_after), xbmc.LOGINFO)

	if ADDON.getSetting('notifications') == 'true':
		Notification(Addon_Title, '[COLOR %s]Clean Database: %s[/COLOR]' % (TEXT_GENERAL, database_text))
	if ADDON.getSetting('dialogue_boxes') == 'true':
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]%s[/COLOR]%s[COLOR %s][LIGHT] (%s)[/LIGHT][/COLOR][CR]%s[/COLOR]' % (TEXT_GENERAL, (TEXT_VALUE if database_bytes_after < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size_after, database_text, TEXT_DARK, database_size, database_selected))

	Log(Log_Title + Clean_db + '[COLOR %s][LIGHT]Finished (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)
	return True

# ============================================================
# FUNCTION: Delete_Database
# ============================================================

def Delete_Database(database_selected):

	Log(Log_Title + Delete_db + '[COLOR %s][LIGHT]Started (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)

	database_path = database_selected.replace('\\', '/').split('/')
	database_name = database_path[-1]
	database_text = ('[COLOR %s] > %s > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, database_path[-2] if len(database_path) >= 2 else '', TEXT_DARK, database_name))

	database_bytes = os.path.getsize(database_selected)
	database_size = Size_Convert(database_bytes)

	if not os.path.exists(database_selected):
		Log(Log_Title + Delete_db + '%s not found' % database_selected, xbmc.LOGERROR)
		return False

	try:
		os.remove(database_selected)

		Log(Log_Title + Delete_db + '//%s deleted' % database_selected, xbmc.LOGINFO)

		if ADDON.getSetting('notifications') == 'true':
			Notification(Addon_Title, '[COLOR %s]Delete Database: %s[/COLOR]' % (TEXT_GENERAL, database_text))
		if ADDON.getSetting('dialogue_boxes') == 'true':
			Dialogue.ok(Addon_Title, '[COLOR %s]Delete Database: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]0.00 B[/COLOR]%s[COLOR %s][LIGHT] (%s)[/LIGHT][/COLOR][CR]%s[/COLOR]' % (TEXT_GENERAL, TEXT_VALUE, database_text, TEXT_DARK, database_size, database_selected))

	except OSError as e:
		Log(Log_Title + Delete_db + 'Delete Database: error %s %s' % (database_name, str(e)), xbmc.LOGINFO)

	Log(Log_Title + Delete_db + '[COLOR %s][LIGHT]Finished (//%s)[/LIGHT][/COLOR]' % (TEXT_DARK, database_selected), xbmc.LOGINFO)
	return True

# ============================================================
# FUNCTION: Select_Database
# ============================================================

def Select_Database(folder_path, mode):

	databases = []

	for root, dirs, files in os.walk(xbmcvfs.translatePath(folder_path)):
		for file in fnmatch.filter(files, '*.db'):
			if file == 'Thumbs.db':
				continue

			database_path = os.path.join(root, file)
			database_bytes = os.path.getsize(database_path)
			database_size = Size_Convert(database_bytes)
			path = database_path.replace('\\', '/').split('/')
			display = '[COLOR %s]%s > [/COLOR]%s [COLOR %s]> [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, path[-2], path[-1], TEXT_DIM, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size)
			databases.append((display, database_path))

	databases.sort(key = lambda t: t[0].upper())
	database_paths = [t[0] for t in databases]
	database_files = [t[1] for t in databases]

	choice = Dialogue.multiselect(Addon_Title + "[COLOR %s][LIGHT]   (select one or more from the list)[/LIGHT][/COLOR]" % TEXT_GENERAL, database_paths, 0, [], False)

	if not choice:
		return

	for database_selected in choice:
		if mode == 'clean_database':
			Clean_Database(database_files[database_selected])
		elif mode == 'delete_database':
			Delete_Database(database_files[database_selected])