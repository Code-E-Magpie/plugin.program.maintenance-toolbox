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
# Addons / Clean / Db
# ============================================================

Addons = ('[COLOR %s]addons > [/COLOR]' % TEXT_GENERAL)
Clean = ('[COLOR %s]clean > [/COLOR]' % TEXT_GENERAL)
Db = ('[COLOR %s]db > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Clean_Addons_Database
# ============================================================

def Clean_Addons_Database():

	addons_db = Addons_Db()

	Log(Log_Title + Addons + '[COLOR %s][LIGHT]Started (addons database: special://database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
	success = False

	Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Close other add-ons and save any changes.[CR]Restart Kodi if required.[/LIGHT][/COLOR][CR]Backup %s database before proceeding.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db))

	addons_choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Kodi will need to close without cleanup at the end.[/LIGHT][/COLOR][CR][CR]Would you like to continue ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Clean Database[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel Clean[/COLOR]' % TEXT_HIGHLIGHT))

	if not addons_choice:
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Cancelled (addons database: special://database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		return # sys.exit() replaced by return

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()
		cursor.execute('DELETE FROM addonlinkrepo;',)
		cursor.execute('DELETE FROM addons;',)
		cursor.execute('DELETE FROM package;',)
		cursor.execute('DELETE FROM repo;',)
		cursor.execute('DELETE FROM update_rules;',)
		cursor.execute('DELETE FROM version;',)
		connection.commit()
		success = True

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to clean addons database: [COLOR %s]%s[/COLOR][CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Addons + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()
		cursor.execute('VACUUM;',)
		connection.commit()

	except sqlite3.Error as e:
		Log(Log_Title + Addons + '%s table error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	finally:
		try:
			if connection:
				connection.close()

		except sqlite3.Error:
			pass

	if success is True:
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Addons Database: [LIGHT](User Information)[CR][COLOR %s]Cleaned addons database: [COLOR %s]%s[/COLOR][CR]Kodi will need to close without cleanup.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addons + '[COLOR %s][LIGHT]Finished (addons database: special://database/%s)[/LIGHT][/COLOR]' % (TEXT_DARK, addons_db), xbmc.LOGINFO)
		os._exit(1)

# ============================================================
# FUNCTION: Clean_Databases
# ============================================================

def Clean_Databases(folder_path):

	Log(Log_Title + Clean + '[COLOR %s][LIGHT]Started (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

	database = []; database_paths = []

	for root, dirs, files in os.walk(xbmcvfs.translatePath(folder_path)):
		for file in fnmatch.filter(files, '*.db'):
			if file != 'Thumbs.db':
				database_path = os.path.join(root, file)
				database_bytes = os.path.getsize(database_path)
				database_size = Size_Convert(database_bytes)
				path = database_path.replace('\\', '/').split('/')
				database.append(database_path)
				database_paths.append('[COLOR %s]%s > [/COLOR]%s [COLOR %s]> [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, path[len(path)-2], path[len(path)-1], TEXT_DIM, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size))
				database_paths.sort(key = lambda v: v.upper())

	choice = Dialogue.multiselect(Addon_Title + "[COLOR %s][LIGHT]   (select one or more from the list)[/LIGHT][/COLOR]" % TEXT_GENERAL, database_paths, 0, [], False)

	if choice == None:
		Log(Log_Title + Clean + '[COLOR %s][LIGHT]Cancelled (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

	elif len(choice) == 0:
		Log(Log_Title + Clean + '[COLOR %s][LIGHT]Cancelled (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

	else:
		for database_selected in choice:
			Database_Cleaner(database[database_selected])

		Log(Log_Title + Clean + '[COLOR %s][LIGHT]Finished (clean databases: %s)[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Database_Cleaner
# ============================================================

def Database_Cleaner(database_selected):
	
	Log(Log_Title + Db + 'clean: %s' % database_selected, xbmc.LOGINFO)

	if os.path.exists(database_selected):
		database_size_before = Size_Convert(os.path.getsize(database_selected))
		try:
			textdb = sqlite3.connect(database_selected)
			textexe = textdb.cursor()

		except Exception as e:
			Log(Log_Title + Db + '%s connection error: %s' % (database_selected, str(e)), xbmc.LOGERROR)
			return False

	else:
		Log(Log_Title + Db + '%s not found' % database_selected, xbmc.LOGERROR)
		return False

	textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	for table in textexe.fetchall():
		if table[0] == 'version':
			Log(Log_Title + Db + '%s table skipped' % table[0], xbmc.LOGINFO)

		else:
			try:
				textexe.execute("DELETE FROM %s" % table[0])
				textdb.commit()
				Log(Log_Title + Db + '%s table data cleared' % table[0], xbmc.LOGINFO)

			except Exception as e:
				Log(Log_Title + Db + '%s remove table error: %s' % (table[0], str(e)), xbmc.LOGERROR)

	database_path = database_selected.replace('\\', '/').split('/')
	database = ('[COLOR %s] > %s > [/COLOR][COLOR %s]%s[/COLOR]' % (TEXT_DIM, database_path[len(database_path)-2], TEXT_DARK, database_path[len(database_path)-1]))
	textexe.close()
	database_bytes = os.path.getsize(database_selected)
	database_size = Size_Convert(database_bytes)

	if ADDON.getSetting('notifications') == 'true':
		Notification(Addon_Title, '[COLOR %s]Clean Databases: %s[/COLOR]' % (TEXT_GENERAL, database))
	if ADDON.getSetting('dialogue_boxes') == 'true':
		Dialogue.ok(Addon_Title, '[COLOR %s]Clean Databases: [LIGHT](User Information)[/LIGHT][CR][COLOR %s]%s[/COLOR]%s[COLOR %s][LIGHT] (%s)[/LIGHT][/COLOR][CR]%s[/COLOR]' % (TEXT_GENERAL, (TEXT_VALUE if database_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), database_size, database, TEXT_DARK, database_size_before, database_selected))
	Log(Log_Title + Db + 'clean: %s done' % database_selected, xbmc.LOGINFO)