# ============================================================
#################################
# clear_thumbnails.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.openwizard > resources > libs > clear.py (drinfernoo)
# location: plugin.program.maintenance-toolbox > resources > lib > clear_thumbnails.py
# type: clear
# functionality: clear thumbnails history or delete Textures*.db & Thumbnails folders + create empty Thumbnails folders
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
import os, shutil, sqlite3, time

from datetime import datetime
from pathlib import Path

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Count_Files, Dialogue, Log, Log_Title, Notification, Now, Size_Convert, Size_Total

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
DATABASE = configuration.DATABASE
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_ITEM = configuration.TEXT_ITEM
THUMBNAILS = configuration.THUMBNAILS

# ============================================================
# Textures_db / Textures_db_path / Thumbs
# ============================================================

Textures_db = 'Textures%s.db' % ADDON.getSetting('textures_database_version')
Textures_db_path = os.path.join(DATABASE, Textures_db)
Thumbs = ('[COLOR %s]thumbs > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# CONTROL FUNCTION: Clear_Thumbnails
# ============================================================

def Clear_Thumbnails():

	if ADDON.getSetting('clear_thumbnails_choice') == 'true':
		clear_days = int(ADDON.getSetting('clear_thumbnails_history'))
		if clear_days > 0:
			if os.path.isfile(Textures_db_path):
				ADDON.setSetting('clear_thumbnails_last_ran', Now())
				ADDON.setSetting('epoch_thumbnails_last_ran', str(int(time.time())))
				Clear_Thumbnails_History(clear_days)
				Clear_Textures_History(clear_days)
				if ADDON.getSetting('clear_thumbnails_textures') == 'true':
					if ADDON.getSetting('clear_thumbnails_textures_items') == 'true':
						Clear_Thumbnails_Textures(True)
					else:
						Clear_Thumbnails_Textures(False)
				if ADDON.getSetting('clear_textures_path') == 'true':
					Clear_Textures_Path()
				else:
					Count_Textures_Path()
			else:
				Dialogue.ok(Addon_Title, '[COLOR %s]Clear Thumbnails History: [LIGHT](User Information)[CR][COLOR %s][LIGHT]%s thumbnails database not found.[CR]See User Information before changing Main Settings.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, Textures_db))
				Log(Log_Title + Thumbs + 'Clear Thumbnails History: %s not found' % Textures_db_path, xbmc.LOGINFO)
		else:
			Log(Log_Title + Thumbs + 'Clear Thumbnails History: increase days[LIGHT] (age in days = 0 in Clear Settings)[/LIGHT]', xbmc.LOGINFO)
			Dialogue.ok(Addon_Title, '[COLOR %s]Clear Thumbnails History: [LIGHT](User Information)[CR][COLOR %s][LIGHT]Age in days must be greater than zero.[CR]Change the value in Clear Settings or select clear all.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
	else:
		ADDON.setSetting('clear_thumbnails_last_ran', Now())
		Clear_Thumbnails_Folders()
		Create_Thumbnails_Folders()
	if ADDON.getSetting('clear_thumbnails_count') == 'true':
		Count_Thumbnails()

# ============================================================
# CONTROL FUNCTION: Clear_Thumbnails_Startup
# ============================================================

def Clear_Thumbnails_Startup():

	if ADDON.getSetting('startup_thumbnails_choice') == 'true':
		startup_days = int(ADDON.getSetting('startup_thumbnails_history'))
		if startup_days > 0:
			if os.path.isfile(Textures_db_path):
				ADDON.setSetting('startup_thumbnails_last_ran', Now())
				ADDON.setSetting('epoch_thumbnails_last_ran', str(int(time.time())))
				Clear_Thumbnails_History(startup_days)
				Clear_Textures_History(startup_days)
				if ADDON.getSetting('startup_thumbnails_textures') == 'true':
					if ADDON.getSetting('startup_thumbnails_textures_items') == 'true':
						Clear_Thumbnails_Textures(True)
					else:
						Clear_Thumbnails_Textures(False)
				if ADDON.getSetting('startup_textures_path') == 'true':
					Clear_Textures_Path()
				else:
					Count_Textures_Path()
			else:
				Dialogue.ok(Addon_Title, '[COLOR %s]Clear Thumbnails History: [LIGHT](User Information)[CR][COLOR %s][LIGHT]%s thumbnails database not found.[CR]See User Information before changing Main Settings.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, Textures_db))
				Log(Log_Title + Thumbs + 'Clear Thumbnails History: %s not found' % Textures_db_path, xbmc.LOGINFO)
		else:
			Log(Log_Title + Thumbs + 'Clear Thumbnails History: increase days[LIGHT] (age in days = 0 in Clear Startup)[/LIGHT]', xbmc.LOGINFO)
			Notification(Addon_Title, '[COLOR %s]Clear Thumbnails History: increase days[/COLOR]' % TEXT_GENERAL)
	else:
		ADDON.setSetting('startup_thumbnails_last_ran', Now())
		Clear_Thumbnails_Folders()
		Create_Thumbnails_Folders()
	if ADDON.getSetting('startup_thumbnails_count') == 'true':
		Count_Thumbnails()

# ============================================================
# FUNCTION: Clear_Textures_History
# ============================================================

def Clear_Textures_History(age_days):

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (textures history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)

	deleted_db_sizes = 0
	deleted_db_texture = 0
	errors = []
	total_items = 0

	# Compute cutoff once as TEXT: "YYYY-MM-DD HH:MM:SS"
	batch_size = 50
	cutoff_age = int(ADDON.getSetting('epoch_thumbnails_last_ran')) - (age_days * 86400)
	cutoff_date = datetime.fromtimestamp(cutoff_age).strftime("%Y-%m-%d %H:%M:%S")
	Textures_db_bytes = os.path.getsize(Textures_db_path)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(Textures_db_path, timeout = 30)
		connection.execute("PRAGMA foreign_keys = OFF")
		cursor = connection.cursor()

	except sqlite3.Error as e:
		errors.append('error opening %s %s' % (Textures_db, str(e)))
		Log(Log_Title + Thumbs + 'Clear Textures History: %s %s' % (Textures_db, str(e)), xbmc.LOGERROR)
		Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
		return deleted_db_sizes, deleted_db_texture, errors, total_items

	try:
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
		tables = [row[0] for row in cursor.fetchall()]
		if 'sizes' not in tables or 'texture' not in tables:
			errors.append('%s %s not found' % (Textures_db, sorted(tables)))
			Log(Log_Title + Thumbs + 'Clear Textures History: %s %s not found' % (Textures_db, sorted(tables)), xbmc.LOGERROR)
			Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
			return deleted_db_sizes, deleted_db_texture, errors, total_items

		cursor.execute("PRAGMA table_info(sizes)")
		sizes_columns = [column[1].lower() for column in cursor.fetchall()]
		cursor.execute("PRAGMA table_info(texture)")
		texture_columns = [column[1].lower() for column in cursor.fetchall()]

		if not all(column in sizes_columns for column in ('idtexture', 'lastusetime')):
			Log(Log_Title + Thumbs + 'Clear Textures History: %s sizes table %s not found' % (Textures_db, sizes_columns), xbmc.LOGERROR)
			errors.append(sizes_columns)
			Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
			return deleted_db_sizes, deleted_db_texture, errors, total_items

		if 'id' not in texture_columns or 'cachedurl' not in texture_columns:
			Log(Log_Title + Thumbs + 'Clear Textures History: %s sizes table %s not found' % (Textures_db, texture_columns), xbmc.LOGERROR)
			errors.append(texture_columns)
			Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
			return deleted_db_sizes, deleted_db_texture, errors, total_items

		# Select id, cachedurl and the MIN(lastusetime) from sizes for that idtexture where MIN(lastusetime) < cutoff_date
		cursor.execute("SELECT texture.id AS idtexture, texture.cachedurl, x.lastusetime FROM texture JOIN (SELECT idtexture, MIN(lastusetime) AS lastusetime FROM sizes GROUP BY idtexture HAVING MIN(lastusetime) < ?) AS x ON x.idtexture = texture.id ORDER BY x.lastusetime ASC", (cutoff_date,))
		distinct_rows = cursor.fetchall()
		# Keep full tuples for logging of cachedurl and id
		items = [(row[0], row[1], row[2]) for row in distinct_rows]
		total_items = len(items)

		Log(Log_Title + Thumbs + 'Clear Textures History: %s older than %s [LIGHT] %s day(s)[/LIGHT]' % (total_items, cutoff_date, age_days), xbmc.LOGINFO)

		for start in range(0, total_items, batch_size):
			batch = items[start:start + batch_size]
			if not batch:
				continue

			if ADDON.getSetting('log_details_for_clears') == 'true':
				for idtexture, cachedurl, lastusetime in batch:
					Log(Log_Title + Thumbs + 'item id: %s  cachedurl: %s deleted' % (idtexture, cachedurl), xbmc.LOGINFO)

			try:
				batch_ids = [row[0] for row in batch]
				placeholders = ",".join(["?"] * len(batch_ids))

				delete_sizes_sql = "DELETE FROM sizes WHERE idtexture IN (%s)" % placeholders
				cursor.execute(delete_sizes_sql, batch_ids)
				deleted_sizes = cursor.rowcount or 0
				delete_texture_sql = "DELETE FROM texture WHERE id IN (%s)" % placeholders
				cursor.execute(delete_texture_sql, batch_ids)
				deleted_texture = cursor.rowcount or 0

				connection.commit()

				Log(Log_Title + Thumbs + 'Clear Textures History: batch %s-%s deleted[LIGHT] (row(s): sizes %s  texture %s)[/LIGHT]' % (start + 1, start + len(batch), deleted_sizes, deleted_texture), xbmc.LOGINFO)

				deleted_db_sizes += deleted_sizes
				deleted_db_texture += deleted_texture

			except sqlite3.Error as e:
				connection.rollback()
				errors.append('batch %s-%s error %s' % (start + 1, start + len(batch), str(e)))
				Log(Log_Title + Thumbs + 'Clear Textures History: batch %s-%s error %s' % (start + 1, start + len(batch), str(e)), xbmc.LOGERROR)

		if deleted_db_sizes or deleted_db_texture:
			try:
				if cursor:
					cursor.close()
					cursor = None
				# Setting isolation_level to None causes sqlite3 to autocommit so VACUUM runs outside transactions
				connection.isolation_level = None
				connection.execute("VACUUM")
				Log(Log_Title + Thumbs + 'Clear Textures History: vacuumed %s' % Textures_db, xbmc.LOGINFO)

			except sqlite3.Error as e:
				errors.append('vacuum error %s' % str(e))
				Log(Log_Title + Thumbs + 'Clear Textures History: vacuum error %s' % str(e), xbmc.LOGERROR)

	except sqlite3.Error as e:
		errors.append('sql error %s' % str(e))
		Log(Log_Title + Thumbs + 'Clear Textures History: sql error %s' % str(e), xbmc.LOGERROR)

	except Exception as e:
		errors.append('exception %s' % str(e))
		Log(Log_Title + Thumbs + 'Clear Textures History: exception %s' % str(e), xbmc.LOGERROR)

	finally:
		try:
			if cursor is not None:
				cursor.close()
		except Exception as e:
			Log(Log_Title + Thumbs + 'Clear Textures History: cursor exception %s' % str(e), xbmc.LOGERROR)
			pass
		try:
			if connection is not None:
				connection.close()
		except Exception as e:
			Log(Log_Title + Thumbs + 'Clear Textures History: connection exception %s' % str(e), xbmc.LOGERROR)
			pass

	Textures_db_bytes_after = os.path.getsize(Textures_db_path)
	Textures_db_reduction = Size_Convert(Textures_db_bytes - Textures_db_bytes_after)
	total_errors = len(errors)

	if total_items > 0:
		Log(Log_Title + Thumbs + 'Clear Textures History: start size %s  finish size %s' % (Size_Convert(Textures_db_bytes), Size_Convert(Textures_db_bytes_after)), xbmc.LOGINFO)
	if Textures_db_bytes > Textures_db_bytes_after:
		Log(Log_Title + Thumbs + 'Clear Textures History: reduction %s' % Textures_db_reduction, xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Textures History: %s reduction[LIGHT] (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Textures_db_reduction, Textures_db))
	if total_errors > 0:
		Log(Log_Title + Thumbs + 'Clear Textures History: errors %s' % total_errors, xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Textures History: %s errors[LIGHT] (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_errors, Textures_db))

	Log(Log_Title + Thumbs + 'Clear Textures History: %s item(s) deleted[LIGHT] (row(s): sizes %s  texture %s)[/LIGHT]' % (total_items, deleted_db_sizes, deleted_db_texture), xbmc.LOGINFO)
	if total_items > 0:
		Notification(Addon_Title, '[COLOR %s]Clear Textures History: %s[LIGHT] item(s) (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_items, Textures_db))
	else:
		if ADDON.getSetting('skip_notifications_for_clears') == 'false':
			Notification(Addon_Title, '[COLOR %s]Clear Textures History: %s[LIGHT] item(s) (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_items, Textures_db))

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
	return deleted_db_sizes, deleted_db_texture, errors, total_items

# ============================================================
# FUNCTION: Clear_Textures_Path
# ============================================================

def Clear_Textures_Path():

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (textures path: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)

	deleted = 0
	errors = []
	path_count = 0

	batch_size = 50
	Textures_db_bytes = os.path.getsize(Textures_db_path)

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(Textures_db_path, timeout = 30)
		connection.execute("PRAGMA foreign_keys = OFF")
		cursor = connection.cursor()

		cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='path'")
		if not cursor.fetchone():
			Log(Log_Title + Thumbs + 'Clear Textures Path: %s path table not found' % Textures_db, xbmc.LOGERROR)
			Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures path: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
			return deleted, errors, path_count

		cursor.execute("SELECT COUNT(*) FROM path")
		row = cursor.fetchone()
		path_count = row[0] if row else 0

		if path_count == 0:
			Log(Log_Title + Thumbs + 'Clear Textures Path: 0 rows in path table', xbmc.LOGINFO)
			if ADDON.getSetting('skip_notifications_for_clears') == 'false':
				Notification(Addon_Title, '[COLOR %s]Clear Textures Path: 0[LIGHT] item(s) (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Textures_db))
			Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures path: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
			return deleted, errors, path_count

		cursor.execute("SELECT id FROM path")
		items = [row[0] for row in cursor.fetchall()]
		total_items = len(items)
		Log(Log_Title + Thumbs + 'Clear Textures Path: %s rows in path table[LIGHT] (%s)[/LIGHT]' % (total_items, Textures_db), xbmc.LOGINFO)

		deleted_db_total = connection.total_changes

		for start in range(0, total_items, batch_size):
			batch = items[start:start + batch_size]
			if not batch:
				continue

			try:
				placeholders = ",".join(["?"] * len(batch))
				delete_path_sql = "DELETE FROM path WHERE id IN (%s)" % placeholders
				cursor.execute(delete_path_sql, tuple(batch))
				deleted_path = cursor.rowcount if cursor.rowcount and cursor.rowcount > 0 else 0

				connection.commit()

				Log(Log_Title + Thumbs + 'Clear Textures Path: batch %s-%s deleted[LIGHT] (row(s): path %s)[/LIGHT]' % (start + 1, start + len(batch), deleted_path), xbmc.LOGINFO)

			except sqlite3.Error as e:
				connection.rollback()
				errors.append('batch %s-%s error %s' % (start + 1, start + len(batch), str(e)))
				Log(Log_Title + Thumbs + 'Clear Textures Path: batch %s-%s error %s' % (start + 1, start + len(batch), str(e)), xbmc.LOGERROR)
				continue

		deleted_db_total_after = connection.total_changes
		deleted = max(0, deleted_db_total_after - deleted_db_total)

		if deleted > 0:
			try:
				if cursor:
					cursor.close()
					cursor = None
				# Setting isolation_level to None causes sqlite3 to autocommit so VACUUM runs outside transactions
				connection.isolation_level = None
				connection.execute("VACUUM")
				Log(Log_Title + Thumbs + 'Clear Textures Path: vacuumed %s' % Textures_db, xbmc.LOGINFO)

			except sqlite3.Error as e:
				errors.append('vacuum error %s' % str(e))
				Log(Log_Title + Thumbs + 'Clear Textures Path: vacuum error %s' % str(e), xbmc.LOGERROR)

	except sqlite3.Error as e:
		errors.append('sql error %s' % str(e))
		Log(Log_Title + Thumbs + 'Clear Textures Path: sql error %s' % str(e), xbmc.LOGERROR)

	except Exception as e:
		errors.append('exception %s' % str(e))
		Log(Log_Title + Thumbs + 'Clear Textures Path: exception %s' % str(e), xbmc.LOGERROR)

	finally:
		try:
			if cursor is not None:
				cursor.close()
		except Exception as e:
			Log(Log_Title + Thumbs + 'Clear Textures Path: cursor exception %s' % str(e), xbmc.LOGERROR)
			pass
		try:
			if connection is not None:
				connection.close()
		except Exception as e:
			Log(Log_Title + Thumbs + 'Clear Textures Path: connection exception %s' % str(e), xbmc.LOGERROR)
			pass

	Textures_db_bytes_after = os.path.getsize(Textures_db_path)
	Textures_db_reduction = Size_Convert(Textures_db_bytes - Textures_db_bytes_after)
	total_errors = len(errors)

	Log(Log_Title + Thumbs + 'Clear Textures Path: start size %s  finish size %s' % (Size_Convert(Textures_db_bytes), Size_Convert(Textures_db_bytes_after)), xbmc.LOGINFO)
	if Textures_db_bytes > Textures_db_bytes_after:
		Log(Log_Title + Thumbs + 'Clear Textures Path: reduction %s' % Textures_db_reduction, xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Textures Path: %s reduction[LIGHT] (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Textures_db_reduction, Textures_db))
	if total_errors > 0:
		Log(Log_Title + Thumbs + 'Clear Textures Path: errors %s' % total_errors, xbmc.LOGINFO)
		Notification(Addon_Title, '[COLOR %s]Clear Textures Path: %s errors[LIGHT] (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_errors, Textures_db))

	Log(Log_Title + Thumbs + 'Clear Textures Path: %s item(s) deleted' % deleted, xbmc.LOGINFO)
	Notification(Addon_Title, '[COLOR %s]Clear Textures Path: %s[LIGHT] item(s) (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, deleted, Textures_db))

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (textures path: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
	return deleted, errors, path_count

# ============================================================
# FUNCTION: Clear_Thumbnails_Folders
# ============================================================

def Clear_Thumbnails_Folders():

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (thumbnails folders: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)

	thumbnail_count = Count_Files(THUMBNAILS)
	thumbnail_size = Size_Convert(Size_Total(THUMBNAILS))

	file_pattern = "Textures*.db"

	for file_path in Path(DATABASE).glob(file_pattern):
		try:
			file_path.unlink()
			textures = file_path.name

			Log(Log_Title + Thumbs + 'Clear Thumbnails: //database/%s deleted' % textures, xbmc.LOGINFO)
			Notification(Addon_Title, '[COLOR %s]Clear Thumbnails: %s deleted[/COLOR]' % (TEXT_GENERAL, textures))

		except OSError as e:
			Log(Log_Title + Thumbs + 'Clear Thumbnails: error %s %s' % (textures, str(e)), xbmc.LOGINFO)

	try:
		if os.path.exists(THUMBNAILS):
			shutil.rmtree(THUMBNAILS)
			Log(Log_Title + Thumbs + 'Clear Thumbnails Folders: //userdata/Thumbnails/ deleted', xbmc.LOGINFO)
		else:
			Log(Log_Title + Thumbs + 'Clear Thumbnails Folders: //userdata/Thumbnails/ not found', xbmc.LOGINFO)

	except OSError as e:
		Log(Log_Title + Thumbs + 'Clear Thumbnails Folders: error %s' % str(e), xbmc.LOGINFO)

	Log(Log_Title + Thumbs + 'Clear Thumbnails Folders: %s / %s file(s) deleted' % (thumbnail_size, thumbnail_count), xbmc.LOGINFO)
	Notification(Addon_Title, '[COLOR %s]Clear Thumbnails Folders: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, thumbnail_size, thumbnail_count))

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (thumbnails folders: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Thumbnails_History
# ============================================================

def Clear_Thumbnails_History(age_days):

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (thumbnails history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)

	age_seconds = int(age_days) * 86400
	cutoff_age = int(ADDON.getSetting('epoch_thumbnails_last_ran')) - age_seconds
	cutoff_date = datetime.fromtimestamp(cutoff_age).strftime("%Y-%m-%d %H:%M:%S")
	file_extensions = (".tbn", ".jpg", ".png")
	now = float(ADDON.getSetting('epoch_thumbnails_last_ran'))
	roots = THUMBNAILS if isinstance(THUMBNAILS, (list, tuple, set)) else [THUMBNAILS]

	thumbnail_delete = []

	for root in roots:
		root_path = Path(root)
		if not root_path.exists():
			continue
		for thumbnail_file in root_path.rglob('*'):
			try:
				if not thumbnail_file.is_file():
					continue
			except OSError:
				continue
			if not thumbnail_file.name.lower().endswith(file_extensions):
				continue
			try:
				thumbnail_stat = thumbnail_file.stat()
			except OSError:
				continue

			if (now - thumbnail_stat.st_mtime) >= age_seconds:
				thumbnail_delete.append((thumbnail_file, thumbnail_stat.st_size))

	Log(Log_Title + Thumbs + 'Clear Thumbnails History: %s older than %s [LIGHT] %s day(s)[/LIGHT]' % (len(thumbnail_delete), cutoff_date, age_days), xbmc.LOGINFO)

	thumbnail_count = 0
	thumbnail_bytes = 0

	for thumbnail_file, thumbnail_stat_size in thumbnail_delete:
		try:
			thumbnail_file.unlink()
			thumbnail_count += 1
			thumbnail_bytes += thumbnail_stat_size
			if ADDON.getSetting('log_details_for_clears') == 'true':
				Log(Log_Title + Thumbs + '%s deleted' % thumbnail_file, xbmc.LOGINFO)

		except OSError as e:
			Log(Log_Title + Thumbs + 'Clear Thumbnails History: %s delete failed %s' % (thumbnail_file, str(e)), xbmc.LOGINFO)

	Log(Log_Title + Thumbs + 'Clear Thumbnails History: %s / %s file(s) deleted' % (Size_Convert(thumbnail_bytes), thumbnail_count), xbmc.LOGINFO)
	Notification(Addon_Title, '[COLOR %s]Clear Thumbnails History: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Size_Convert(thumbnail_bytes), thumbnail_count))

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (thumbnails history: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)

# ============================================================
# FUNCTION: Clear_Thumbnails_Textures
# ============================================================

def Clear_Thumbnails_Textures(delete_db_items):

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (thumbnails textures: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)

	file_extensions = (".tbn", ".jpg", ".png")
	hex_sub_folders = '0123456789abcdef'
	roots = THUMBNAILS if isinstance(THUMBNAILS, (list, tuple, set)) else [THUMBNAILS]

	thumbnails = set()
	thumbnails_file_map = {}

	for root in roots:
		root_path = Path(root)
		if not root_path.exists():
			continue
		for sub_folder in hex_sub_folders:
			thumbnail_folder = root_path / sub_folder
			if not thumbnail_folder.exists():
				continue
			try:
				for thumbnail_file in thumbnail_folder.iterdir():
					try:
						if not thumbnail_file.is_file():
							continue
					except OSError:
						continue
					if not thumbnail_file.name.lower().endswith(file_extensions):
						continue
					key = "%s/%s" % (sub_folder, thumbnail_file.name)
					thumbnails.add(key)
					thumbnails_file_map[key] = thumbnail_file
			except OSError:
				continue

	deleted_db_sizes = 0
	deleted_db_texture = 0
	errors = []
	total_items = 0
	texture_cachedurl_set = set()

	batch_size = 50

	try:
		Textures_db_bytes = os.path.getsize(Textures_db_path)
	except OSError:
		Textures_db_bytes = 0

	if not Path(Textures_db_path).exists():
		errors.append('db missing %s' % Textures_db_path)
		Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: db missing %s' % Textures_db_path, xbmc.LOGERROR)

	else:
		connection = None
		cursor = None

		try:
			connection = sqlite3.connect(Textures_db_path, timeout = 30)
			connection.execute("PRAGMA foreign_keys = OFF")
			cursor = connection.cursor()

			cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
			tables = [row[0] for row in cursor.fetchall()]
			if 'sizes' not in tables or 'texture' not in tables:
				errors.append("%s %s not found" % (Textures_db, sorted(tables)))
				Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: %s %s not found' % (Textures_db, sorted(tables)), xbmc.LOGERROR)

			else:
				cursor.execute("PRAGMA table_info(sizes)")
				sizes_columns = [column[1].lower() for column in cursor.fetchall()]
				cursor.execute("PRAGMA table_info(texture)")
				texture_columns = [column[1].lower() for column in cursor.fetchall()]

				if 'id' not in texture_columns or 'cachedurl' not in texture_columns or 'idtexture' not in sizes_columns:
					errors.append('unexpected schema %s' % Textures_db)
					Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: unexpected schema %s' % Textures_db, xbmc.LOGERROR)

				else:
					cursor.execute("SELECT id, cachedurl FROM texture WHERE cachedurl IS NOT NULL AND cachedurl != ''")
					texture_rows = cursor.fetchall()
					total_texture = len(texture_rows)

					items = []

					for texture_id, texture_cachedurl in texture_rows:
						cachedurl = (texture_cachedurl or '').lstrip('/')
						if '/' not in cachedurl:
							continue
						texture_cachedurl_set.add(cachedurl)
						if cachedurl not in thumbnails:
							items.append((texture_id, cachedurl))

					total_items = len(items)
					matched = total_texture - total_items
					Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: %s item(s) [LIGHT](matched %s  fileless %s)[/LIGHT]' % (total_texture, matched, total_items), xbmc.LOGINFO)

					deleted_sizes = 0
					deleted_texture = 0

					if delete_db_items and items:
						for start in range(0, total_items, batch_size):
							batch = items[start:start + batch_size]
							if not batch:
								continue

							batch_ids = [item[0] for item in batch]
							placeholders = ",".join("?" * len(batch_ids))

							try:
								cursor.execute("DELETE FROM sizes WHERE idtexture IN (%s)" % placeholders, tuple(batch_ids))
								deleted_sizes += cursor.rowcount or 0
								cursor.execute("DELETE FROM texture WHERE id IN (%s)" % placeholders, tuple(batch_ids))
								deleted_texture += cursor.rowcount or 0

								connection.commit()

								if ADDON.getSetting('log_details_for_clears') == 'true':
									for texture_id, cachedurl in batch:
										Log(Log_Title + Thumbs + 'item id: %s  cachedurl: %s deleted' % (texture_id, cachedurl), xbmc.LOGINFO)
								Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: batch %s-%s deleted[LIGHT] (row(s): sizes %s  texture %s)[/LIGHT]' % (start + 1, start + len(batch), deleted_sizes, deleted_texture), xbmc.LOGINFO)

							except sqlite3.Error as e:
								connection.rollback()
								errors.append('batch %s-%s error %s' % (start + 1, start + len(batch), str(e)))
								Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: batch %s-%s error %s' % (start + 1, start + len(batch), str(e)), xbmc.LOGERROR)

						deleted_db_sizes += deleted_sizes
						deleted_db_texture += deleted_texture

						if deleted_sizes or deleted_texture:
							try:
								try:
									cursor.close()
								except Exception:
									pass
								cursor = None

								connection.commit()
								# Setting isolation_level to None causes sqlite3 to autocommit so VACUUM runs outside transactions
								connection.isolation_level = None
								connection.execute("VACUUM")
								Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: vacuumed %s' % Textures_db, xbmc.LOGINFO)

							except sqlite3.Error as e:
								errors.append('vacuum error %s' % str(e))
								Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: vacuum error %s' % str(e), xbmc.LOGERROR)

		except sqlite3.Error as e:
			errors.append('error opening %s %s' % (Textures_db, str(e)))
			Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: %s %s' % (Textures_db, str(e)), xbmc.LOGERROR)

		except Exception as e:
			errors.append('exception %s' % str(e))
			Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: exception error %s' % str(e), xbmc.LOGERROR)

		finally:
			try:
				if cursor is not None:
					cursor.close()
			except Exception as e:
				Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: cursor exception %s' % str(e), xbmc.LOGERROR)
			try:
				if connection is not None:
					connection.close()
			except Exception as e:
				Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: connection exception %s' % str(e), xbmc.LOGERROR)

	try:
		Textures_db_bytes_after = os.path.getsize(Textures_db_path)
	except OSError:
		Textures_db_bytes_after = Textures_db_bytes

	Textures_db_reduction = Size_Convert(max(0, Textures_db_bytes - Textures_db_bytes_after))
	total_errors = len(errors)

	if delete_db_items:
		if total_items > 0:
			Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: start size %s  finish size %s' % (Size_Convert(Textures_db_bytes), Size_Convert(Textures_db_bytes_after)), xbmc.LOGINFO)
			if Textures_db_bytes > Textures_db_bytes_after:
				Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: reduction %s' % Textures_db_reduction, xbmc.LOGINFO)
				Notification(Addon_Title, '[COLOR %s]Clear Thumbnails Textures: %s reduction[LIGHT] (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Textures_db_reduction, Textures_db))
		if total_errors > 0:
			Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: errors %s' % total_errors, xbmc.LOGINFO)
			Notification(Addon_Title, '[COLOR %s]Clear Thumbnails Textures: %s errors[LIGHT] (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_errors, Textures_db))

		Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: %s item(s) deleted[LIGHT] (row(s): sizes %s  texture %s)[/LIGHT]' % (total_items, deleted_db_sizes, deleted_db_texture), xbmc.LOGINFO)
		if total_items > 0:
			Notification(Addon_Title, '[COLOR %s]Clear Thumbnails Textures: %s[LIGHT] item(s) (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_items, Textures_db))
		else:
			if ADDON.getSetting('skip_notifications_for_clears') == 'false':
				Notification(Addon_Title, '[COLOR %s]Clear Thumbnails Textures: %s[LIGHT] item(s) (%s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, total_items, Textures_db))

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (thumbnails textures: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, Textures_db_path), xbmc.LOGINFO)
	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (thumbnails textures: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)

	Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: %s / %s file(s) [LIGHT](matched %s  orphans %s)[/LIGHT]' % (Size_Convert(Size_Total(THUMBNAILS)), Count_Files(THUMBNAILS), matched, Count_Files(THUMBNAILS) - matched), xbmc.LOGINFO)

	deleted_file_count = 0
	deleted_file_bytes = 0

	for key, thumbnail_file in thumbnails_file_map.items():
		if key not in texture_cachedurl_set:
			try:
				size = thumbnail_file.stat().st_size
			except OSError:
				size = 0

			try:
				thumbnail_file.unlink()
				deleted_file_count += 1
				deleted_file_bytes += size
				if ADDON.getSetting('log_details_for_clears') == 'true':
					Log(Log_Title + Thumbs + '%s deleted' % thumbnail_file, xbmc.LOGINFO)

			except OSError as e:
				errors.append('file delete failed %s %s' % (thumbnail_file, str(e)))
				Log(Log_Title + Thumbs + 'Delete failed %s %s' % (thumbnail_file, str(e)), xbmc.LOGERROR)

	Log(Log_Title + Thumbs + 'Clear Thumbnails Textures: %s / %s file(s) deleted' % (Size_Convert(deleted_file_bytes), deleted_file_count), xbmc.LOGINFO)
	Notification(Addon_Title, '[COLOR %s]Clear Thumbnails Textures: %s / %s[LIGHT] file(s)[/LIGHT][/COLOR]' % (TEXT_GENERAL, Size_Convert(deleted_file_bytes), deleted_file_count))

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (thumbnails textures: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)
	return deleted_db_sizes, deleted_db_texture, errors, total_items

# ============================================================
# FUNCTION: Count_Thumbnails
# ============================================================

def Count_Thumbnails():

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Started (count thumbnails: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)

	errors = []
	path_count = 0
	sizes_count = 0
	texture_count = 0

	connection = None
	cursor = None

	try:
		connection = sqlite3.connect(Textures_db_path, timeout=30)
		connection.execute("PRAGMA foreign_keys = OFF")
		cursor = connection.cursor()

		cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
		tables = [row[0] for row in cursor.fetchall()]
		if 'path' not in tables or 'sizes' not in tables or 'texture' not in tables:
			errors.append("%s %s not found" % (Textures_db, sorted(tables)))
			Log(Log_Title + Thumbs + 'Count Thumbnails: %s %s not found' % (Textures_db, sorted(tables)), xbmc.LOGERROR)
			return 0, 0, 0

		cursor.execute("SELECT COUNT(*) FROM path")
		row = cursor.fetchone()
		path_count = row[0] if row else 0
		cursor.execute("SELECT COUNT(*) FROM sizes")
		row = cursor.fetchone()
		sizes_count = row[0] if row else 0
		cursor.execute("SELECT COUNT(*) FROM texture")
		row = cursor.fetchone()
		texture_count = row[0] if row else 0

	except Exception as e:
		Log(Log_Title + Thumbs + 'Count Thumbnails: %s exception %s' % (Textures_db, str(e)), xbmc.LOGERROR)
		return 0, 0, 0

	finally:
		try:
			if cursor is not None:
				cursor.close()
		except Exception as e:
			Log(Log_Title + Thumbs + 'Count Thumbnails: cursor exception %s' % str(e), xbmc.LOGERROR)
		try:
			if connection is not None:
				connection.close()
		except Exception as e:
			Log(Log_Title + Thumbs + 'Count Thumbnails: connection exception %s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Thumbs + 'Count Thumbnails: row(s)  path %s  sizes %s  texture %s[LIGHT] (%s)[/LIGHT]' % (path_count, sizes_count, texture_count, Textures_db), xbmc.LOGINFO)
	Log(Log_Title + Thumbs + 'Count Thumbnails: %s / %s file(s)' % (Size_Convert(Size_Total(THUMBNAILS)), Count_Files(THUMBNAILS)), xbmc.LOGINFO)

	Log(Log_Title + Thumbs + '[COLOR %s][LIGHT]Finished (count thumbnails: //%s)[/LIGHT][/COLOR]' % (TEXT_DARK, THUMBNAILS), xbmc.LOGINFO)
	return path_count, sizes_count, texture_count

# ============================================================
# FUNCTION: Create_Thumbnails_Folders
# ============================================================

def Create_Thumbnails_Folders():

	if not os.path.exists(THUMBNAILS):
		os.makedirs(THUMBNAILS)

	thumbnail_folders = '0123456789abcdef'
	video = os.path.join(THUMBNAILS, 'Video', 'Bookmarks')

	for item in thumbnail_folders:
		folder_name = os.path.join(THUMBNAILS, item)

		if not os.path.exists(folder_name):
			os.makedirs(folder_name)

	if not os.path.exists(video):
		os.makedirs(video)