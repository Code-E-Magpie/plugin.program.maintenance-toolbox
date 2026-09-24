# ============================================================
#################################
# function.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > wizard.py
# location: plugin.program.maintenance-toolbox > resources > lib > common > function.py
# type: common
# functionality: common functions - counts, lists, log, notification, now (datestamp / timestamp), sizes, textbox
# development:
#	- functions consolidated to plugin.program.maintenance-toolbox > resources > lib > common > function.py
#	- variables consolidated to plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
#	- code debugged and reengineered if required using https://aipy.dev/tools

# ============================================================
# File used by
# ============================================================

# see individual functions

# ============================================================
# Import
# ============================================================

import xbmc, xbmcgui, xbmcvfs
import glob, os, re

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
ADDON_ICON = configuration.ADDON_ICON
ADDON_NAME = configuration.ADDON_NAME
DATABASE = configuration.DATABASE
NOTIFICATION_DURATION = ADDON.getSetting('notification_duration')
TEXT_ADDON = configuration.TEXT_ADDON
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE

# ============================================================
# Addon_Title / Dialogue / DialogueProgress / Function / Log_Title
# ============================================================

Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ' '.join((ADDON_NAME).strip(' '))))
Dialogue = xbmcgui.Dialog()
DialogueProgress = xbmcgui.DialogProgress()
Function = ('[COLOR %s]function > [/COLOR]' % TEXT_GENERAL)
Log_Title = ('[COLOR %s]%s [/COLOR]' % (TEXT_ADDON, ADDON_NAME))

# ============================================================
# FUNCTION: Add_Blank
# ============================================================

# used by:
# footer.footer_menu.py
# tab2.repositories.py

def Add_Blank():

	choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Common Function: [LIGHT](Add Blank)[CR][COLOR %s] > Add Blank row between each new line.[CR] > No Blank row between each new line.[/LIGHT][/COLOR][CR]Add a blank row between each new line ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]No Blank[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Add Blank[/COLOR]' % TEXT_HIGHLIGHT))

	if choice == 0:
		blank = 'true'
	else:
		blank = 'false'

	return blank

# ============================================================
# FUNCTION: Addons_Db
# ============================================================

# used by:
# information.py
# footer.database_toolbox.py
# footer.footer_menu.py
# tab1.addon.py
# tab2.repositories.py

def Addons_Db():
	
	pattern = re.compile(r'Addons(\d+)\.db$', re.IGNORECASE)
	matches = glob.glob(os.path.join(DATABASE, 'Addons*.db'))
	highest = 0

	for file in matches:
		basename = os.path.basename(file)
		file_match = pattern.search(basename)
		if file_match:
			try:
				number = int(file_match.group(1))
			except ValueError:
				continue
			if number > highest:
				highest = number

	addons_db = "Addons%s.db" % highest
	return addons_db

# ============================================================
# FUNCTION: Count_Favourites
# ============================================================

# used by:
# interface.py
# footer.reorder_favourites.py

def Count_Favourites(file_path):

	try:
		with open(file_path, 'r', encoding = 'utf-8') as file:
			content = file.read()
			temp = content.replace('\r', '').replace('\n', '').replace('\t', '')
			count_favourites = len(re.compile(r'<favourite.+?</favourite>').findall(temp))

			return count_favourites

	except FileNotFoundError:
		return 0

	except IOError:
		Log(Log_Title + Function + 'Count Favourites: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except re.error as e:
		Log(Log_Title + Function + 'Count Favourites: file content error[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: Count_File
# ============================================================

# used by:
# interface.py

def Count_File(file_path):

	try:
		if os.path.isfile(file_path):
			return 1

		else:
			return 0

	except (OSError, IOError):
		Log(Log_Title + Function + 'Count File: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: Count_Files
# ============================================================

# used by:
# interface.py
# tab1.clear_surplus.py
# tab1.clear_temp.py
# tab1.clear_thumbnails.py

def Count_Files(folder_path):

	count_files = 0

	for root, dirs, files in os.walk(folder_path):
		count_files += len(files)

	return count_files

# ============================================================
# FUNCTION: Count_Folders
# ============================================================

# used by:
# interface.py
# footer.footer_menu.py

def Count_Folders(folder_path):

	if not os.path.exists(folder_path):
		return 0

	else:
		count_folders = len([folders for folders in xbmcvfs.listdir(folder_path)[0]])

		return count_folders

# ============================================================
# FUNCTION: Count_Lines
# ============================================================

# used by:
# interface.py

def Count_Lines(file_path):

	try:
		with open(file_path, 'r') as file:
			file_content = file.read()
			lines = file_content.splitlines()
			count_lines = len(lines)

			return count_lines

	except FileNotFoundError:
		return 0

	except IOError:
		Log(Log_Title + Function + 'Count Lines: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except Exception as e:
		Log(Log_Title + Function + 'Count Lines: file content error[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except UnicodeDecodeError:
		Log(Log_Title + Function + 'Count Lines: file contains non-ASCII characters', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Non-ASCII[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: Count_Log_Errors
# ============================================================

# used by:
# interface.py
# tab1.system_log_errors.py

def Count_Log_Errors(file_path):

	try:
		with open(file_path, 'r', encoding = 'utf-8', errors = 'ignore') as file:
			content = file.read()
			content = content.replace('\n', '[CR]').replace('\r', '')
			pattern = r"-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--"
			count_log_errors = len(re.findall(pattern, content))

			return count_log_errors

	except FileNotFoundError:
		return 0

	except IOError:
		Log(Log_Title + Function + 'Count Log Errors: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except re.error as e:
		Log(Log_Title + Function + 'Count Log Errors: %s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except Exception as e:
		Log(Log_Title + Function + 'Count Log Errors: %s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: Count_Log_Files (excludes subfolders)
# ============================================================

# used by:
# interface.py
# tab1.clear_temp.py

def Count_Log_Files(folder_path):

	try:
		files = os.listdir(folder_path)

	except OSError:
		return 0

	count_log_files = 0

	for file in files:
		file_path = os.path.join(folder_path, file)
		if os.path.isfile(file_path):
			if file.endswith('.log'):

				count_log_files += 1

	return count_log_files

# ============================================================
# FUNCTION: Count_Log_Lines
# ============================================================

# Count the number of lines including lines with ASCII errors but excluding blank lines
# used by:
# interface.py
# tab1.system_log.py
# tab1.system_log_errors.py

def Count_Log_Lines(file_path):

	if not os.path.exists(file_path):
		return 0

	count_log_lines = 0

	try:
		with open(file_path, 'r', encoding = 'utf-8', errors = 'replace') as file:
			for line in file:
				if line.strip():

					count_log_lines += 1

	except UnicodeDecodeError:
		with open(file_path, 'r', encoding = 'latin-1', errors = 'replace') as file:
			for line in file:
				if line.strip():

					count_log_lines += 1

	return count_log_lines

# ============================================================
# FUNCTION: Count_Sources
# ============================================================

# used by:
# interface.py

def Count_Sources(file_path):

	try:
		with open(file_path, 'r', encoding = 'utf-8') as file:
			content = file.read()
			temp = content.replace('\r', '').replace('\n', '').replace('\t', '')
			count_sources = len(re.compile('<name>.+?</name>').findall(temp))

			return count_sources

	except FileNotFoundError:
		return 0

	except IOError:
		Log(Log_Title + Function + 'Count Sources: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except re.error as e:
		Log(Log_Title + Function + 'Count Sources: file content error[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: List_Files
# ============================================================

# used by:
# service.py
# tab4.userdata.py

def List_Files(folder_path, output):

	file_paths = []
	count_files = 0

	for root, dirs, files in os.walk(folder_path):
		for file in files:
			file_path = os.path.join(root, file)
			file_paths.append(file_path)

			count_files += 1

	file_paths.sort()
	files_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	try:
		with open(output, "w") as file:
			file.write('Maintenance Toolbox > function > List Files\n\nCreated: %s\n\nSource folder: %s\nOutput file: %s\n\nItems in list: %s\n\n' % (files_datetime, folder_path, output, count_files))
			for file_path in file_paths:
				file.write(file_path + "\n")

	except IOError as e:
		Log(Log_Title + Function + 'List Files: %s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Function + '[COLOR %s][LIGHT]List Files: %s[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)
	Log(Log_Title + Function + 'List: %s' % output, xbmc.LOGINFO)

# ============================================================
# FUNCTION: List_Folders
# ============================================================

# used by:
# service.py
# tab4.addon_data.py
# tab4.addons.py

def List_Folders(folder_path, output):

	folders = []

	for folder in os.listdir(folder_path):
		if os.path.isdir(os.path.join(folder_path, folder)):
			folders.append(folder)

	count_folders = len([folders for folders in xbmcvfs.listdir(folder_path)[0]])
	folders.sort()
	folders_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	try:
		with open(output, "w") as file:
			file.write('Maintenance Toolbox > function > List Folders\n\nCreated: %s\n\nSource folder: %s\nOutput file: %s\n\nItems in list: %s\n\n' % (folders_datetime, folder_path, output, count_folders))
			for folder in folders:
				file.write(folder + "\n")

	except IOError as e:
		Log(Log_Title + Function + 'List Folders: %s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Function + '[COLOR %s][LIGHT]List Folders: %s[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)
	Log(Log_Title + Function + 'List: %s' % output, xbmc.LOGINFO)

# ============================================================
# FUNCTION: List_Logs
# ============================================================

# used by:
# service.py
# tab4.logs.py

def List_Logs(folder_path, output):

	log_files = []
	count_log_files = 0

	for log_file in os.listdir(folder_path):
		file_path = os.path.join(folder_path, log_file)
		if os.path.isfile(file_path) and file_path.endswith('.log'):
			log_files.append(log_file)

			count_log_files += 1

	log_files.sort()
	logs_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	try:
		with open(output, "w") as file:
			file.write('Maintenance Toolbox > function > List Logs\n\nCreated: %s\n\nSource folder: %s\nOutput file: %s\n\nItems in list: %s\n\n' % (logs_datetime, folder_path, output, count_log_files))
			for log_file in log_files:
				file.write(log_file + "\n")

	except IOError as e:
		Log(Log_Title + Function + 'List Logs: %s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Function + '[COLOR %s][LIGHT]List Logs: %s[/LIGHT][/COLOR]' % (TEXT_DARK, folder_path), xbmc.LOGINFO)
	Log(Log_Title + Function + 'List: %s' % output, xbmc.LOGINFO)

# ============================================================
# FUNCTION: Log
# ============================================================

# used by:
# service.py
# footer.database_toolbox.py
# footer.reorder_favourites.py
# tab1.addon.py
# tab1.clear_cache.py
# tab1.clear_surplus.py
# tab1.clear_temp.py
# tab1.clear_thumbnails.py
# tab1.system_log.py
# tab1.system_log_errors.py
# tab2.internet.py
# tab2.repositories.py
# tab2.sources.py
# tab2.speedtest.py
# tab3.favourites_xml.py
# tab3.guisettings_xml.py
# tab3.profiles_xml.py
# tab3.sources_xml.py
# tab4.addon_data.py
# tab4.addons.py
# tab4.logs.py
# tab4.userdata.py

def Log(message, level = xbmc.LOGDEBUG):

	xbmc.log(message, level = level)

# ============================================================
# FUNCTION: Notification
# ============================================================

# used by:
# interface.py
# service.py
# footer.database_toolbox.py
# tab1.addon.py
# tab1.clear_cache.py
# tab1.clear_surplus.py
# tab1.clear_temp.py
# tab1.clear_thumbnails.py
# tab1.system_log.py
# tab1.system_log_errors.py
# tab2.internet.py
# tab2.sources.py
# tab2.speedtest.py
# tab3.favourites_xml.py
# tab3.guisettings_xml.py
# tab3.profiles_xml.py
# tab3.sources_xml.py
# tab4.addon_data.py
# tab4.addons.py
# tab4.logs.py
# tab4.userdata.py

def Notification(title, message, times = NOTIFICATION_DURATION, icon = ADDON_ICON, sound = False):

	Dialogue.notification(title, message, icon, int(times), sound)

# ============================================================
# FUNCTION: Now
# ============================================================

# used by:
# tab2.repositories.py
# tab2.sources.py
# tab2.speedtest.py
# tab3.favourites_xml.py
# tab3.guisettings_xml.py
# tab3.profiles_xml.py
# tab3.sources_xml.py
# tab4.addon_data.py
# tab4.addons.py
# tab4.logs.py
# tab4.userdata.py

def Now():

	now = datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")

# ============================================================
# FUNCTION: Now_Decimal
# ============================================================

# used by:
# service.py
# tab1.clear_cache.py
# tab1.clear_surplus.py
# tab1.clear_temp.py
# tab1.clear_thumbnails.py

def Now_Decimal():

	now = datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S.%f")[:22] # 2nd digit is number of decimal places

# ============================================================
# FUNCTION: Size_Convert
# ============================================================

# used by:
# interface.py
# footer.database_toolbox.py
# footer.footer_menu.py
# tab1.clear_cache.py
# tab1.clear_surplus.py
# tab1.clear_temp.py
# tab1.clear_thumbnails.py
# tab1.database_information.py
# tab1.storage.py

def Size_Convert(num, suffix = 'B'):

	for unit in ['', 'K', 'M', 'G']:
		if abs(num) < 1024.0:
			return "%3.02f %s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.02f %s%s" % (num, 'G', suffix)

# ============================================================
# FUNCTION: Size_File
# ============================================================

# used by:
# interface.py

def Size_File(file_path):

	size_file = 0

	try:
		if os.path.exists(file_path):
			size_file += os.path.getsize(file_path)

		else:
			return 0

	except (OSError, IOError) as e:
		Log(Log_Title + Function + 'Size File: error reading file[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	return size_file

# ============================================================
# FUNCTION: Size_Log_Files (excludes subfolders)
# ============================================================

# used by:
# interface.py
# tab1.clear_temp.py

def Size_Log_Files(folder_path):

	try:
		files = os.listdir(folder_path)

	except OSError as e:
		Log(Log_Title + Function + 'Size Log Files: error reading folder[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Folder Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	size_log_files = 0

	for file in files:
		file_path = os.path.join(folder_path, file)
		if os.path.isfile(file_path):
			if file.endswith('.log'):
				file_size = os.path.getsize(file_path)
				size_log_files += file_size

	return size_log_files

# ============================================================
# FUNCTION: Size_Total
# ============================================================

# used by:
# interface.py
# footer.footer_menu.py
# tab1.clear_cache.py
# tab1.clear_surplus.py
# tab1.clear_temp.py
# tab1.clear_thumbnails.py

def Size_Total(folder_path):

	size_total = 0

	for root, dirs, files in os.walk(folder_path):
		for file in files:
			file_path = os.path.join(root, file)
			size_total += os.path.getsize(file_path)

	return size_total

# ============================================================
# FUNCTION: TextBox
# ============================================================

# information.py
# footer.footer_menu.py
# tab1.addon.py
# tab1.database_information.py
# tab1.system_log.py
# tab1.system_log_errors.py
# tab2.repositories.py

ACTION_BACKSPACE = 110 # Backspace
ACTION_MOUSE_LEFT_CLICK = 100 # Mouse click
ACTION_MOUSE_LONG_CLICK = 108 # Mouse long click
ACTION_MOUSE_WHEEL_DOWN = 105 # Mouse wheel down
ACTION_MOUSE_WHEEL_UP = 104 # Mouse wheel up
ACTION_MOVE_DOWN = 4 # Down arrow key
ACTION_MOVE_LEFT = 1 # Left arrow key
ACTION_MOVE_MOUSE = 107 # Down arrow key
ACTION_MOVE_RIGHT = 2 # Right arrow key
ACTION_MOVE_UP = 3 # Up arrow key
ACTION_NAV_BACK = 92 # Backspace action
ACTION_PREVIOUS_MENU = 10 # ESC action
ACTION_SELECT_ITEM = 7 # Number Pad Enter

def TextBox(title, text):
	class TextBoxes(xbmcgui.WindowXMLDialog):

		def onAction(self, action):
			if action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

		def onClick(self, controlId):
			if (controlId == self.close_button):
				self.close()
			elif controlId != self.close_button:
				self.noop = lambda: None

		def onInit(self): # group = 8000, background = 8100, noop = 8181
			self.title = 8200
			self.text = 8300
			self.scrollbar = 8400
			self.close_button = 8500
			self.noop = lambda: None
			self.showDialog()

		def showDialog(self):
			close = '[COLOR %s]Close[/COLOR]' % TEXT_GENERAL
			self.getControl(self.title).setLabel(title)
			self.getControl(self.close_button).setLabel(close)
			self.getControl(self.text).setText(text)
			self.setFocusId(self.scrollbar)

	textbox = TextBoxes("Textbox.xml", ADDON.getAddonInfo('path'), 'default')
	textbox.doModal()
	del textbox

# ============================================================
# FUNCTION: Warning
# ============================================================

# used by:
# interface.py
# footer.footer_menu.py

def Warning():

		choice = Dialogue.ok(Addon_Title, '[COLOR %s]Common Function: [LIGHT](Warning Notice)[CR][COLOR %s] > This function works but has not been fully optimised.[CR] > Code-E-Magpie magic to follow in the near future.[/LIGHT][/COLOR][CR]Press OK to continue.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))