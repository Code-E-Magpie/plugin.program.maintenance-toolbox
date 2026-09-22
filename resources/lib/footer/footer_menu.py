# ============================================================
#################################
# footer_menu.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > footer > footer_menu.py
# type: footer
# functionality: access to settings, addons database information, folder information and other functionality
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
import fnmatch, os, re, sqlite3

from information import Database_User_Information, Favourites_User_Information
from resources.lib.common.configuration import configuration
from resources.lib.common.function import Add_Blank, Addon_Title, Addons_Db, Count_Folders, Dialogue, Log, Log_Title, Now, Size_Convert, Size_Total, TextBox, Warning

from resources.lib.footer.database_toolbox import Clean_Addons_Database, Clean_Databases
from resources.lib.footer.reorder_favourites import Reorder_Favourites
from resources.lib.tab1.addon import Data_Addon, Data_Addon_Builtin

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
ADDON_DATA = configuration.ADDON_DATA
ADDONS = configuration.ADDONS
DATABASE = configuration.DATABASE
HOME = configuration.HOME
SIZE_HIGHLIGHT = ADDON.getSetting('size_highlight')
SOURCES = configuration.SOURCES
SOURCES_TXT = configuration.SOURCES_TXT
TEXT_DARK = configuration.TEXT_DARK
TEXT_DIM = configuration.TEXT_DIM
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
USERDATA = configuration.USERDATA
XBMCBINADDONS = configuration.XBMCBINADDONS

# ============================================================
# Arrow / Footer
# ============================================================

Arrow = '[COLOR %s] > [/COLOR]' % TEXT_DIM
Footer = ('[COLOR %s]footer menu > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: DialogueSelect
# ============================================================

def DialogueSelect(list, title = Addon_Title):
	return Dialogue.select(title, list)

#####################################################################################

# ============================================================
# FUNCTION: Addon_Files
# ============================================================

def Addon_Files(file_type):

	files_mapping = {"cache": HOME, "database": HOME, "fanart": ADDONS, "icon": ADDONS, "thumbs": HOME}
	files_mapping_type = {"cache": '*cache*.db', "database": '*.db', "fanart": 'fanart.jpg', "icon": 'icon.png'}
	files_type = {"cache": 'CACHE DATABASES', "database": 'DATABASE FILES', "fanart": 'FANART FILES', "icon": 'ICON FILES'}

	try:
		path = files_mapping[file_type]
		pattern = files_mapping_type[file_type]
		title = files_type[file_type]

	except KeyError:
		Log(Log_Title + Footer + 'add-on files name error: %s' % file_type, xbmc.LOGERROR)
		return

	database_count, thumbs_count = Database_Count()
	file_paths = []

	for root, _, files in os.walk(path):
		for fname in fnmatch.filter(files, pattern):
			file_path = os.path.join(root, fname)
			file_bytes = os.path.getsize(file_path)
			file_size = Size_Convert(file_bytes)
			file_paths.append('[COLOR %s]%s[/COLOR]%s[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, file_path, Arrow, (TEXT_VALUE if file_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), file_size))

	file_count = len(file_paths)
	file_paths.sort(key = lambda v: v.upper())

	blank = Add_Blank()
	column_text = '[COLOR %s]Path %s Size[/COLOR]' % (TEXT_GENERAL, Arrow)
	column = column_text + "\n\n" if blank == 'true' else column_text + "\n"
	file = "\n\n".join(file_paths) if blank == 'true' else "\n".join(file_paths)

	Files_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s)[/LIGHT][/COLOR][CR][CR]%s[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(title), TEXT_VALUE, path, '' if file_count == 0 else column, TEXT_GENERAL, ('None found.' if file_count == 0 else file))
	TextBox('[B]%s[/B][CR][COLOR %s]%s: [/COLOR][COLOR %s]%s  [/COLOR]' % (Addon_Title, TEXT_ITEM, title.title(), TEXT_VALUE, file_count) + ('[COLOR %s][LIGHT]Thumbs.db files: [/COLOR][COLOR %s]%s[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_VALUE, thumbs_count) if file_type == 'database' else ''), Files_Text)

# ============================================================
# FUNCTION: Addon_Folders
# ============================================================

def Addon_Folders(folder_path, title):

	Size_Bytes = Size_Total(folder_path)

	folders = []

	for folder in os.listdir(folder_path):
		if os.path.isdir(os.path.join(folder_path, folder)):

			folder_bytes = Size_Total(os.path.join(folder_path, folder))
			folder_size = Size_Convert(folder_bytes)

			folders.append('[COLOR %s]%s[/COLOR]%s[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, folder, Arrow, (TEXT_VALUE if folder_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), folder_size))

	folders.sort(key = lambda v: v.upper())

	blank = Add_Blank()
	folders = "\n\n".join(folders) if blank == 'true' else "\n".join(folders)
	column_text = '[COLOR %s]%s %s Size[/COLOR]' % (TEXT_GENERAL, 'Folder' if title == 'Home Folders' else 'Add-on ID', Arrow)
	column = column_text + "\n\n" if blank == 'true' else column_text + "\n"

	Addon_Folders_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s)[/LIGHT][/COLOR][CR][CR]%s[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(title).upper(), TEXT_VALUE, folder_path, column, TEXT_GENERAL, folders)
	TextBox('[B]%s[/B][CR][COLOR %s]%s: [/COLOR][COLOR %s]%s  [/COLOR][COLOR %s]Total Size: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, title, TEXT_VALUE, Count_Folders(folder_path), TEXT_ITEM, TEXT_VALUE, Size_Convert(Size_Bytes)), Addon_Folders_Text)

# ============================================================
# FUNCTION: Addon_Pycache_Folders
# ============================================================

def Addon_Pycache_Folders(folder_path, title):

	Size_Bytes = 0

	folders = []

	for root, directories, _ in os.walk(folder_path):
		if "__pycache__" in directories:
			pycache_path = os.path.join(root, "__pycache__")

			folder_bytes = Size_Total(pycache_path)
			folder_size = Size_Convert(folder_bytes)
			Size_Bytes += folder_bytes

			folders.append((pycache_path, folder_bytes, '[COLOR %s]%s[/COLOR]%s[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, pycache_path, Arrow, (TEXT_VALUE if folder_bytes < int(SIZE_HIGHLIGHT) else TEXT_HIGHLIGHT), folder_size)))

	folders.sort(key = lambda v: v[0].upper())

	blank = Add_Blank()
	folders_text = "\n\n".join([info[2] for info in folders]) if blank == 'true' else "\n".join([info[2] for info in folders])
	column_text =  '[COLOR %s]Path %s Size[/COLOR]' % (TEXT_GENERAL, Arrow)
	column = column_text + "\n\n" if blank == 'true' else column_text + "\n"

	Addon_Pycache_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s)[/LIGHT][/COLOR][CR][CR]%s[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(title).upper(), TEXT_VALUE, folder_path, column, TEXT_GENERAL, folders_text)
	TextBox('[B]%s[/B][CR][COLOR %s]%s: [/COLOR][COLOR %s]%s  [/COLOR][COLOR %s]Total Size: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, title, TEXT_VALUE, len(folders), TEXT_ITEM, TEXT_VALUE, Size_Convert(Size_Bytes)), Addon_Pycache_Text)

# ============================================================
# FUNCTION: Addon_Type
# ============================================================

addon_folders, exception, game, inputstream, metadata, music, other, others, picture, program, repository, resource, service, skin, video, weather, user_addons = Data_Addon()
builtin_skin, builtin_repository = Data_Addon_Builtin()

def Addon_Type(addon_type, title):

	addon_type.sort(key = lambda v: v.upper())

	blank = Add_Blank()
	addons = "\n\n".join(addon_type) if blank == 'true' else "\n".join(addon_type)

	Addon_Type_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(title).upper(), TEXT_VALUE, ADDONS, TEXT_GENERAL, addons if int(str(len(addon_type))) != 0 else 'None found.')
	TextBox('[B]%s[/B][CR][COLOR %s]%s: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, title, TEXT_VALUE, int(str(len(addon_type)))), Addon_Type_Text)

# ============================================================
# FUNCTION: Addons_Disabled
# ============================================================

def Addons_Disabled():

	addons_db = Addons_Db()

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		installed_count = "SELECT COUNT (*) FROM installed"
		cursor.execute(installed_count)
		installed_count = cursor.fetchall()
		installed_count = int(str(installed_count)[2: -3])

		disabled_count = "SELECT COUNT (*) FROM installed WHERE enabled = 0"
		cursor.execute(disabled_count)
		disabled_count = cursor.fetchall()
		disabled_count = int(str(disabled_count)[2: -3])
		enabled_count = installed_count - disabled_count

		disabled = "SELECT CASE disabledReason WHEN 0 THEN 'None        ' WHEN 1 THEN 'User        ' WHEN 2 THEN 'Incompatible' WHEN 3 THEN 'Failure     ' ELSE NULL END AS disabled_reason, installDate, addonID || ' (' || CASE origin WHEN 'b6a50484-93a0-4afb-a01c-8d17e059feda' THEN 'system built-in add-on' WHEN '' THEN 'manual zip file / package / development build' ELSE origin END || ')' AS display FROM installed WHERE enabled = 0 ORDER BY LOWER(addonID) ASC"
		cursor.execute(disabled)
		disabled = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	disabled = str(disabled).replace("[('","Reason', 'Date Installed', '\tAdd-on ID (Install Method: manual / repository / system)'), ('").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '","\t\t\t")

	Disabled_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('DISABLED ADD-ONS'), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, (disabled if disabled_count != 0 else 'All add-ons enabled.'))
	TextBox('[B]%s[/B][CR][COLOR %s]Enabled Add-ons: [COLOR %s]%s  [/COLOR]Disabled Add-ons: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, enabled_count, TEXT_VALUE, disabled_count), Disabled_Text)

# ============================================================
# FUNCTION: Addons_Disabled_Updates
# ============================================================

def Addons_Disabled_Updates():

	addons_db = Addons_Db()

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		updates_count = "SELECT COUNT (*) FROM update_rules"
		cursor.execute(updates_count)
		updates_count = cursor.fetchall()
		updates_count = int(str(updates_count)[2: -3])

		updates = "SELECT CASE updateRule WHEN 0 THEN 'System Disabled ' WHEN 1 THEN 'User Disabled   ' WHEN 2 THEN 'Install Disabled' ELSE NULL END AS updateRule, addonID FROM update_rules ORDER BY LOWER(addonID) ASC"
		cursor.execute(updates)
		updates = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	updates = str(updates).replace("[('","Method', '\tAdd-on ID'), ('").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '","\t\t\t")

	Updates_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('ADD-ONS DISABLED AUTO-UPDATE'), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, (updates if updates_count != 0 else 'Auto-update enabled for all add-ons.'))
	TextBox('[B]%s[/B][CR][COLOR %s]Add-ons Disabled Auto-Update: [COLOR %s]%s[/COLOR][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, updates_count), Updates_Text)

# ============================================================
# FUNCTION: Addons_Installed
# ============================================================

def Addons_Installed(installed_name):

	last_updated = "SELECT installDate, lastUpdated, lastUsed, addonID FROM installed WHERE lastUpdated IS NOT NULL ORDER BY lastUpdated DESC"
	last_updated_count = "SELECT COUNT (*) FROM installed WHERE lastUpdated IS NOT NULL"
	last_used = "SELECT installDate, lastUpdated, lastUsed, addonID FROM installed WHERE lastUsed IS NOT NULL ORDER BY lastUsed ASC"
	last_used_count = "SELECT COUNT (*) FROM installed WHERE lastUsed IS NOT NULL"
	never_used = "SELECT installDate, lastUpdated, lastUsed, addonID FROM installed WHERE lastUsed IS NULL AND addonID NOT LIKE 'repository.%' ORDER BY LOWER(addonID) ASC"
	never_used_count = "SELECT COUNT (*) FROM installed WHERE lastUsed IS NULL AND addonID NOT LIKE 'repository.%'"
	origin = "SELECT installDate, lastUpdated, lastUsed, addonID FROM installed WHERE origin IS '' ORDER BY LOWER(addonID) ASC"
	origin_count = "SELECT COUNT (*) FROM installed WHERE origin IS ''"

	addons_db = Addons_Db()
	installed_mapping = {"last updated": last_updated, "last used": last_used, "never used": never_used, "origin": origin}
	installed_mapping_count = {"last updated": last_updated_count, "last used": last_used_count, "never used": never_used_count, "origin": origin_count}
	installed_mapping_title = {"last updated": 'INSTALLED ADD-ONS LAST UPDATED', "last used": 'INSTALLED ADD-ONS LAST USED', "never used": 'INSTALLED ADD-ONS NEVER USED', "origin": 'INSTALLED ADD-ONS ORIGIN NOT SET'}

	try:
		installed = installed_mapping[installed_name]
		installed_count = installed_mapping_count[installed_name]
		installed_title = installed_mapping_title[installed_name]

	except KeyError:
		Log(Log_Title + Footer + 'installed name error: %s' % installed_name, xbmc.LOGERROR)

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		cursor.execute(installed_count)
		installed_count = cursor.fetchall()
		installed_count = int(str(installed_count)[2: -3])

		cursor.execute(installed)
		installed = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Origin: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	installed = str(installed).replace("None", "'None                       '").replace("[('","Install Date             ', 'Last Updated           ', 'Last Used              ', 'Add-on ID'), ('").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '","\t\t")

	Installed_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(installed_title), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, installed)
	TextBox('[B]%s[/B][CR][COLOR %s]%s: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, installed_title.title(), TEXT_VALUE, installed_count), Installed_Text)

# ============================================================
# FUNCTION: Addons_Packages
# ============================================================

def Addons_Packages():

	addons_db = Addons_Db()

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		package_count = "SELECT COUNT (*) FROM package"
		cursor.execute(package_count)
		package_count = cursor.fetchall()
		package_count = int(str(package_count)[2: -3])

		package_table = "SELECT addonID, filename FROM package ORDER BY LOWER(addonID) ASC, LOWER(filename) DESC"
		cursor.execute(package_table)
		package_table = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	column_text = '[COLOR %s]Add-on ID %s Filename[/COLOR]' % (TEXT_GENERAL, Arrow)
	column = column_text + "\n\n" if blank == 'true' else column_text + "\n"
	package_table = str(package_table).replace("[('","").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '", Arrow)

	Package_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR]%s[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('PACKAGES'), TEXT_VALUE, DATABASE, addons_db, column, TEXT_GENERAL, package_table)
	TextBox('[B]%s[/B][CR][COLOR %s]Packages: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, package_count), Package_Text)

# ============================================================
# FUNCTION: Addons_Repositories
# ============================================================

def Addons_Repositories(repositories_name):

	addons_db = Addons_Db()

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		repositories_count = "SELECT COUNT (*) FROM repo" if repositories_name == "repositories" else "SELECT COUNT(*) FROM repo WHERE NOT EXISTS (SELECT 1 FROM addonlinkrepo JOIN addons ON addonlinkrepo.idAddon = addons.id JOIN installed ON addons.addonID = installed.addonID WHERE addonlinkrepo.idRepo = repo.id AND NOT (installed.addonID LIKE 'repository.%' OR installed.addonID LIKE 'script.module%'))"
		cursor.execute(repositories_count)
		repositories_count = cursor.fetchall()
		repositories_count = int(str(repositories_count)[2: -3])

		not_working = "SELECT COUNT (*) FROM repo WHERE checksum IS NULL"
		cursor.execute(not_working)
		not_working = cursor.fetchall()
		not_working = int(str(not_working)[2: -3])
		working = str(repositories_count - not_working)

		repositories = "SELECT CASE WHEN checksum IS NULL THEN 'Bad     ' ELSE 'Good    ' END AS status, lastcheck, nextcheck, CASE WHEN length(version) >= 8 THEN version ELSE substr(version || '        ', 1, 8) END AS version, addonID FROM repo ORDER BY LOWER(addonID) ASC" if repositories_name == "repositories" else "SELECT CASE WHEN repo.checksum IS NULL THEN 'Bad     ' ELSE 'Good    ' END AS status, repo.lastcheck, repo.nextcheck, CASE WHEN length(repo.version) >= 8 THEN repo.version ELSE substr(repo.version || '        ', 1, 8) END AS version, repo.addonID FROM repo WHERE NOT EXISTS (SELECT 1 FROM addonlinkrepo JOIN addons ON addonlinkrepo.idAddon = addons.id JOIN installed ON addons.addonID = installed.addonID WHERE addonlinkrepo.idRepo = repo.id AND NOT (installed.addonID LIKE 'repository.%' OR installed.addonID LIKE 'script.module%')) ORDER BY LOWER(addonID) ASC"
		cursor.execute(repositories)
		repositories = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Repositories: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	repositories_no = '[COLOR %s]No repositories without add-ons identified.[/COLOR]' % TEXT_GENERAL
	repositories = str(repositories).replace("[('","Status', 'Kodi Last Checked  ', 'Kodi Next Check    ', 'Version ', 'Add-on ID'), ('").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '","\t\t").replace("[]", repositories_no)

	Repositories_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join(repositories_name).upper(), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, repositories)
	No_Addons_Text = '' if repositories_count == 0 else '[COLOR %s][CR][CR][CR]The repositories shown above may be surplus to requirements as they have no significant add-ons installed.[CR][CR]The repositories may have other repositories and / or script.module.* add-ons installed.[CR][CR]Please check the repositories before removing.[/COLOR]' % TEXT_GENERAL
	TextBox('[B]%s[/B][CR][COLOR %s]Repositories: [/COLOR][COLOR %s]%s  [/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, repositories_count) + ('[COLOR %s][LIGHT]Not working: [/COLOR][COLOR %s]%s[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_VALUE, not_working) if repositories_name == 'repositories' else ''), Repositories_Text if repositories_name == 'repositories' else (Repositories_Text + No_Addons_Text))

# ============================================================
# FUNCTION: Addons_Repository
# ============================================================

def Addons_Repository(sort_by):

	addons_db = Addons_Db()

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		addon_count = "SELECT addons.addonID, COUNT (*) as addons_count FROM repo LEFT JOIN addonlinkrepo alr ON repo.id = alr.idRepo LEFT JOIN addons ON alr.idAddon = addons.id INNER JOIN installed ON addons.addonID = installed.addonID GROUP BY addons.addonID"
		cursor.execute(addon_count)
		addon_count = cursor.fetchall()
		addon_count = len(addon_count)

		addons_count = "SELECT addons.addonID, COUNT (*) as addons_count FROM repo LEFT JOIN addonlinkrepo alr ON repo.id = alr.idRepo LEFT JOIN addons ON alr.idAddon = addons.id INNER JOIN installed ON addons.addonID = installed.addonID WHERE NOT installed.addonID LIKE 'script.module%' GROUP BY addons.addonID"
		cursor.execute(addons_count)
		addons_count = cursor.fetchall()
		addons_count = len(addons_count)

		repositories_count = "SELECT repo.addonID, COUNT (*) as repository_count FROM repo LEFT JOIN addonlinkrepo alr ON repo.id = alr.idRepo LEFT JOIN addons ON alr.idAddon = addons.id INNER JOIN installed ON addons.addonID = installed.addonID GROUP BY repo.addonID"
		cursor.execute(repositories_count)
		repositories_count = cursor.fetchall()
		repositories_count = len(repositories_count)

		repository_count = "SELECT repo.addonID, COUNT (*) as repository_count FROM repo LEFT JOIN addonlinkrepo alr ON repo.id = alr.idRepo LEFT JOIN addons ON alr.idAddon = addons.id INNER JOIN installed ON addons.addonID = installed.addonID WHERE NOT installed.addonID LIKE 'script.module%' GROUP BY repo.addonID"
		cursor.execute(repository_count)
		repository_count = cursor.fetchall()
		repository_count = len(repository_count)

		addons_repository = "SELECT repo.addonID, addons.addonID || ' (' || addons.version || ')' AS addonID FROM repo LEFT JOIN addonlinkrepo alr ON repo.id = alr.idRepo LEFT JOIN addons ON alr.idAddon = addons.id INNER JOIN installed ON addons.addonID = installed.addonID WHERE NOT installed.addonID LIKE 'script.module%' ORDER BY LOWER(repo.addonID) ASC, LOWER(addons.addonID) ASC, LOWER(addons.version) ASC" if sort_by == "repository" else "SELECT addons.addonID || ' (' || addons.version || ')' AS addonID, repo.addonID FROM repo LEFT JOIN addonlinkrepo alr ON repo.id = alr.idRepo LEFT JOIN addons ON alr.idAddon = addons.id INNER JOIN installed ON addons.addonID = installed.addonID ORDER BY LOWER(addons.addonID) ASC, LOWER(addons.version) ASC, LOWER(repo.addonID) ASC"
		cursor.execute(addons_repository)
		addons_repository = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Repository: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	addons_repository = str(addons_repository).replace("[('","Repository Add-on ID ', ' Add-on ID (Add-on Version)'), ('" if sort_by == "repository" else "Add-on ID (Add-on Version) ', ' Repository Add-on ID'), ('").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '", Arrow)

	Addons_Repository_Text = '[COLOR %s][B]%s[/B]%s[/COLOR][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('ADD-ONS REPOSITORY'), ('  (excludes script.module.* add-ons)' if sort_by == "repository" else ''), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, addons_repository)
	TextBox('[B]%s[/B][CR][COLOR %s]Add-ons: [COLOR %s]%s  [/COLOR]Repositories: [COLOR %s]%s[/COLOR][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, addons_count if sort_by == "repository" else addon_count, TEXT_VALUE, repositories_count if sort_by == "repository" else repository_count), Addons_Repository_Text)

# ============================================================
# FUNCTION: Addons_Tables
# ============================================================

def Addons_Tables(table_name):

	table_addonlinkrepo = "SELECT * FROM addonlinkrepo ORDER BY idRepo ASC, idAddon ASC"
	table_addons = "SELECT id, addonID, version FROM addons ORDER BY LOWER(addonID) ASC, id ASC"
	table_installed = "SELECT * FROM installed ORDER BY LOWER(addonID) ASC"
	table_package = "SELECT * FROM package ORDER BY LOWER(addonID) ASC, LOWER(filename) DESC"
	table_repo = "SELECT * FROM repo ORDER BY LOWER(addonID) ASC"
	table_update_rules = "SELECT * FROM update_rules ORDER BY LOWER(addonID) ASC"
	table_version = "SELECT * FROM version ORDER BY LOWER(idVersion) ASC"

	addons_db = Addons_Db()
	table_mapping = {"addonlinkrepo": table_addonlinkrepo, "addons": table_addons, "installed": table_installed, "package": table_package, "repo": table_repo, "update_rules": table_update_rules, "version": table_version}

	try:
		table = table_mapping[table_name]

	except KeyError:
		Log(Log_Title + Footer + 'table name error: %s' % table_name, xbmc.LOGERROR)

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		table_count = "SELECT COUNT (*) FROM %s" % table_name
		cursor.execute(table_count)
		table_count = cursor.fetchall()
		table_count = int(str(table_count)[2: -3])

		cursor.execute("PRAGMA table_info(%s);" % table_name)
		columns_info = cursor.fetchall()

		cursor.execute(table)
		table = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Addons Database: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Footer + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Footer + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	blank = Add_Blank()
	column_text = [column[1] for column in columns_info]
	column = str(column_text).replace("['", "").replace("']", ("\n\n" if blank == 'true' else "\n")).replace("', '", (" " + Arrow + " "))
	column_addons_text =  '[COLOR %s]id %s addonID %s version[/COLOR]' % (TEXT_GENERAL, Arrow, Arrow)
	column_addons = column_addons_text + "\n\n" if blank == 'true' else column_addons_text + "\n"
	table = str(table).replace("[('","").replace("[(","").replace("')]","").replace(")]","").replace("'), (",("\n\n" if blank == 'true' else "\n")).replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("), ('",("\n\n" if blank == 'true' else "\n")).replace("), (",("\n\n" if blank == 'true' else "\n")).replace("', '", Arrow).replace("', ", Arrow).replace(", '", Arrow).replace(", ", Arrow)

	Tables_Text = '[COLOR %s][B]%s[/B][/COLOR][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s%s[/COLOR]' % (TEXT_ITEM, ' '.join(table_name).upper(), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, column if table_name != 'addons' else column_addons, table if table_count != 0 else 'No lines in %s table.' % table_name)
	TextBox('[B]%s[/B][CR][COLOR %s]%s table: [/COLOR][COLOR %s]%s[LIGHT] lines[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, table_name, TEXT_VALUE, table_count), Tables_Text)

# ============================================================
# FUNCTION: Database_Count
# ============================================================

def Database_Count():

	database_count = 0
	thumbs_count = 0

	for _, _, files in os.walk(HOME):
		database_count += sum(1 for file in files if file.endswith('.db'))
		thumbs_count += files.count('Thumbs.db')

	return database_count, thumbs_count

# ============================================================
# FUNCTION: Sources_File
# ============================================================

def Sources_File():

	if not os.path.exists(SOURCES):
		Notification(Addon_Title, '[COLOR %s]Sources Files: no sources.xml[/COLOR]' % TEXT_GENERAL)
		return False

	sources = 0
	http_count = 0

	file = open(SOURCES, encoding = 'utf-8')
	string = file.read()
	string_replace = string.replace('\r','').replace('\n','').replace('\t','')
	extract = re.compile('<files>.+?</files>').findall(string_replace)
	file.close()

	if len(extract) > 0:
		sources_xml = re.compile('<source>.+?<name>(.+?)</name>.+?<path pathversion="1">(.+?)</path>.+?<allowsharing>(.+?)</allowsharing>.+?</source>').findall(extract[0])
		sources_xml.sort(key = lambda x: x[0].lower())

		for name, path, sharing in sources_xml:
			sources += 1

			sources_count = len(sources_xml)

			if path.startswith('http'):
				http_count += 1

	blank = Add_Blank()
	column_text =  '[COLOR %s]Name %s Path %s Allow Sharing[/COLOR]' % (TEXT_GENERAL, Arrow, Arrow)
	column = column_text + "\n\n" if blank == 'true' else column_text + "\n"
	sources_xml = str(sources_xml).replace("[('","").replace("')]","").replace("('","").replace("'), ",("\n\n" if blank == 'true' else "\n")).replace("', '", Arrow)

	Sources_File_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s)[/LIGHT][/COLOR][CR][CR]%s[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('SOURCES FILE'), TEXT_VALUE, SOURCES, column, TEXT_GENERAL, sources_xml)
	TextBox('[B]%s[/B][CR][COLOR %s]Sources: [/COLOR][COLOR %s]%s  [/COLOR][COLOR %s][LIGHT]locations: [COLOR %s]%s  [/COLOR]http: [COLOR %s]%s[/COLOR][/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, sources_count, TEXT_ITEM, TEXT_VALUE, (sources_count - http_count), TEXT_VALUE, http_count), Sources_File_Text)

# ============================================================
# FUNCTION: The_Footer_Menu
# ============================================================

def The_Footer_Menu():

	footer_menu = ['Settings', 'Add-on Checks [COLOR %s]+ Repository [/COLOR][COLOR %s][LIGHT] (%s database)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM, Addons_Db()), 'Add-on Folders + Files [COLOR %s][LIGHT] (add-on ID / path + size)[/LIGHT][/COLOR]' % TEXT_DIM, 'Add-on Information [COLOR %s]Check [/COLOR][COLOR %s][LIGHT] (Tab: System + Add-on)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'Repositories [COLOR %s][LIGHT] (installed)[/LIGHT][/COLOR]' % TEXT_DIM, 'Sources File [COLOR %s][LIGHT] (sources.xml)[/LIGHT][/COLOR]' % TEXT_DIM, '[COLOR %s]Database Toolbox: [/COLOR]User Information' % TEXT_DARK, 'Database Toolbox [COLOR %s][LIGHT] (.db file list + clean .db files)[/LIGHT][/COLOR]' % TEXT_DIM, '[COLOR %s]Reorder Favourites: [/COLOR]User Information' % TEXT_DARK, 'Reorder Favourites [COLOR %s][LIGHT] (favourites.xml)[/LIGHT][/COLOR]' % TEXT_DIM]

	addons_menu = ['< < <  [COLOR %s][LIGHT]back to Footer Menu[/LIGHT][/COLOR]' % TEXT_DIM, '[COLOR %s]Add-ons[/COLOR] Disabled' % TEXT_DARK, '[COLOR %s]Add-ons[/COLOR] Disabled Auto-Update' % TEXT_DARK, '[COLOR %s]Add-ons[/COLOR] Origin Not Set [COLOR %s][LIGHT] (no repository assigned)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), '[COLOR %s]Add-ons[/COLOR] Last Updated [COLOR %s][LIGHT] (last updated set)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), '[COLOR %s]Add-ons[/COLOR] Last Used [COLOR %s][LIGHT] (last used set)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), '[COLOR %s]Add-ons[/COLOR] Never Used [COLOR %s][LIGHT] (last used not set excludes repos)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), '[COLOR %s]Add-ons[/COLOR] Packages' % TEXT_DARK, '[COLOR %s]Add-ons[/COLOR] Repository [COLOR %s][LIGHT] (sort repo excludes script.module.*)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'No Add-on [COLOR %s]Repositories[/COLOR]' % TEXT_DARK]

	sort_menu = ['< < <  [COLOR %s][LIGHT]back to Footer Menu[/LIGHT][/COLOR]' % TEXT_DIM,  '[COLOR %s]Add-ons[/COLOR] Repository [COLOR %s][LIGHT] (sort add-on Add-on ID asc)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), '[COLOR %s]Add-ons[/COLOR] Repository [COLOR %s][LIGHT] (sort repository Add-on ID asc)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM)]

	size_menu = ['< < <  [COLOR %s][LIGHT]back to Footer Menu[/LIGHT][/COLOR]' % TEXT_DIM, 'Add-on Data [COLOR %s]Folders + Size [/COLOR][COLOR %s][LIGHT] (5 seconds or less)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'Add-on [COLOR %s]Folders + Size [/COLOR][COLOR %s][LIGHT] (10 seconds or less)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'Built-in Add-on [COLOR %s]Folders + Size [/COLOR][COLOR %s][LIGHT] (5 seconds or less)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'Home [COLOR %s]Folders + Size [/COLOR][COLOR %s][LIGHT] (5 seconds or less)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'Python Cache [COLOR %s]Folders + Size [/COLOR][COLOR %s][LIGHT] (__pycache__ folder list)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), 'Database Files [COLOR %s][LIGHT] (.db file list)[/LIGHT][/COLOR]' % TEXT_DIM, 'Cache Databases [COLOR %s][LIGHT] (cache.db list)[/LIGHT][/COLOR]' % TEXT_DIM, '[COLOR %s]Add-on [/COLOR]Fanart Files [COLOR %s][LIGHT] (fanart.jpg list)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM), '[COLOR %s]Add-on [/COLOR]Icon Files [COLOR %s][LIGHT] (icon.png list)[/LIGHT][/COLOR]' % (TEXT_DARK, TEXT_DIM)]

	type_menu = ['< < <  [COLOR %s][LIGHT]back to Footer Menu[/LIGHT][/COLOR]' % TEXT_DIM, 'Exception [COLOR %s][LIGHT] (addon.xml: provides is non standard)[/LIGHT][/COLOR]' % TEXT_DIM, 'Game Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'InputStream Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Metadata [COLOR %s][LIGHT] (Information Providers folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Music Add-ons [COLOR %s][LIGHT] (addon.xml: provides = audio)[/LIGHT][/COLOR]' % TEXT_DIM, 'Other Add-ons [COLOR %s][LIGHT] (other folder name starts)[/LIGHT][/COLOR]' % TEXT_DIM, 'Others Add-ons [COLOR %s][LIGHT] (addon.xml: provides not set)[/LIGHT][/COLOR]' % TEXT_DIM, 'Picture Add-ons [COLOR %s][LIGHT] (addon.xml: provides = image)[/LIGHT][/COLOR]' % TEXT_DIM, 'Program Add-ons [COLOR %s][LIGHT] (addon.xml: provides = executable)[/LIGHT][/COLOR]' % TEXT_DIM, 'Repository Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Resource Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Service Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Skin Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Video Add-ons [COLOR %s][LIGHT] (addon.xml: provides = video)[/LIGHT][/COLOR]' % TEXT_DIM, 'Weather Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Built-in Repository Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM, 'Built-in Skin Add-ons [COLOR %s][LIGHT] (folder name starts with)[/LIGHT][/COLOR]' % TEXT_DIM]

	database_menu = ['< < <  [COLOR %s][LIGHT]back to Footer Menu[/LIGHT][/COLOR]' % TEXT_DIM, '[COLOR %s]Clean Addons Database: [/COLOR]%s' % (TEXT_DARK, Addons_Db()), '[COLOR %s]Clean Databases (folder): [/COLOR]addon_data' % TEXT_DARK, '[COLOR %s]Clean Databases (folder): [/COLOR]addons' % TEXT_DARK, '[COLOR %s]Clean Databases (folder): [/COLOR]database' % TEXT_DARK, '[COLOR %s]Clean Databases (folder): [/COLOR]home [COLOR %s](all databases)[/COLOR]' % (TEXT_DARK, TEXT_DARK), '[COLOR %s]Clean Databases (folder): [/COLOR]userdata [COLOR %s](all excluding addons)[/COLOR]' % (TEXT_DARK, TEXT_DARK), 'Database Files [COLOR %s][LIGHT] (.db file list)[/LIGHT][/COLOR]' % TEXT_DIM, 'Database Tables [COLOR %s][LIGHT] (%s raw tables for analysis)[/LIGHT][/COLOR]' % (TEXT_DIM, Addons_Db()), '[COLOR %s]Database Toolbox: [/COLOR]User Information' % TEXT_DARK]

	table_menu = ['< < <  [COLOR %s][LIGHT]back to Footer Menu[/LIGHT][/COLOR]' % TEXT_DIM, 'addonlinkrepo [COLOR %s][LIGHT] (sort idRepo asc > idAddon asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'addons [COLOR %s][LIGHT] (only 3 columns sort addonID asc > id asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'installed [COLOR %s][LIGHT] (sort addonID asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'package [COLOR %s][LIGHT] (sort addonID asc > filename desc)[/LIGHT][/COLOR]' % TEXT_DIM, 'repo [COLOR %s][LIGHT] (sort addonID asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'update_rules [COLOR %s][LIGHT] (sort addonID asc)[/LIGHT][/COLOR]' % TEXT_DIM, 'version [COLOR %s][LIGHT] (sort idVersion asc)[/LIGHT][/COLOR]' % TEXT_DIM] 

	footer = DialogueSelect(footer_menu)
	if footer == 0: ADDON.openSettings()
	elif footer == 1: # Add-on Checks + Repository (Addons#.db database)
		addons = DialogueSelect(addons_menu)
		if addons == 0: The_Footer_Menu() # < < <  back to Footer Menu
		elif addons == 1: Addons_Disabled()
		elif addons == 2: Addons_Disabled_Updates()
		elif addons == 3: Addons_Installed('origin')
		elif addons == 4: Addons_Installed('last updated')
		elif addons == 5: Addons_Installed('last used')
		elif addons == 6: Addons_Installed('never used')
		elif addons == 7: Addons_Packages()
		elif addons == 8: # Add-ons Repository (excludes script.module.* add-ons)
			sort = DialogueSelect(sort_menu)
			if sort == 0: The_Footer_Menu() # < < <  back to Footer Menu
			elif sort == 1: Addons_Repository('add-on')
			elif sort == 2: Addons_Repository('repository')
		elif addons == 9: Addons_Repositories('no add-on repositories')
	elif footer == 2: # Add-on Folders + .db Files (names / paths + sizes)
		size = DialogueSelect(size_menu)
		if size == 0: The_Footer_Menu() # < < <  back to Footer Menu
		elif size == 1: Addon_Folders(ADDON_DATA, 'Add-on Data Folders')
		elif size == 2: Addon_Folders(ADDONS, 'Add-on Folders')
		elif size == 3: Addon_Folders(XBMCBINADDONS, 'Built-in Add-on Folders')
		elif size == 4: Addon_Folders(HOME, 'Home Folders')
		elif size == 5: Addon_Pycache_Folders(ADDONS, 'Python Cache Folders')
		elif size == 6: Addon_Files('database')
		elif size == 7: Addon_Files('cache')
		elif size == 8: Addon_Files('fanart')
		elif size == 9: Addon_Files('icon')
	elif footer == 3: # Add-on Information Check (Tab: System + Add-on)
		type = DialogueSelect(type_menu)
		if type == 0: The_Footer_Menu() # < < <  back to Footer Menu
		elif type == 1: Addon_Type(exception, 'Exception Add-ons')
		elif type == 2: Addon_Type(game, 'Game Add-ons')
		elif type == 3: Addon_Type(inputstream, 'InputStream Add-ons')
		elif type == 4: Addon_Type(metadata, 'Metadata (Information Providers) Add-ons')
		elif type == 5: Addon_Type(music, 'Music Add-ons')
		elif type == 6: Addon_Type(other, 'Other Add-ons')
		elif type == 7: Addon_Type(others, 'Others Add-ons')
		elif type == 8: Addon_Type(picture, 'Picture Add-ons')
		elif type == 9: Addon_Type(program, 'Program Add-ons')
		elif type == 10: Addon_Type(repository, 'Repository Add-ons')
		elif type == 11: Addon_Type(resource, 'Resource Add-ons')
		elif type == 12: Addon_Type(service, 'Service Add-ons')		
		elif type == 13: Addon_Type(skin, 'Skin Add-ons')
		elif type == 14: Addon_Type(video, 'Video Add-ons')
		elif type == 15: Addon_Type(weather, 'Weather Add-ons')
		elif type == 16: Addon_Type(builtin_repository, 'Built-in Repository Add-ons')
		elif type == 17: Addon_Type(builtin_skin, 'Built-in Skin Add-ons')
	elif footer == 4: Addons_Repositories('repositories')
	elif footer == 5: Sources_File()
	elif footer == 6: Database_User_Information()
	elif footer == 7: # Database Toolbox (clean .db files)
		database = DialogueSelect(database_menu)
		if database == 0: The_Footer_Menu() # < < <  back to Footer Menu
		elif database == 1: Clean_Addons_Database()
		elif database == 2: Clean_Databases(ADDON_DATA)
		elif database == 3: Clean_Databases(ADDONS)
		elif database == 4: Clean_Databases(DATABASE)
		elif database == 5: Clean_Databases(HOME)
		elif database == 6: Clean_Databases(USERDATA)
		elif database == 7: Addon_Files('database')
		elif database == 8: # Addons#.db Tables
			table = DialogueSelect(table_menu)
			if table == 0: The_Footer_Menu() # < < <  back to Footer Menu
			elif table == 1: Addons_Tables('addonlinkrepo')
			elif table == 2: Addons_Tables('addons')
			elif table == 3: Addons_Tables('installed')
			elif table == 4: Addons_Tables('package')
			elif table == 5: Addons_Tables('repo')
			elif table == 6: Addons_Tables('update_rules')
			elif table == 7: Addons_Tables('version')
		elif database == 9: Database_User_Information()
	elif footer == 8: Favourites_User_Information()
	elif footer == 9: Reorder_Favourites()