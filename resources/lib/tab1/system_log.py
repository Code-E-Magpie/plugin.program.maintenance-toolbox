# ============================================================
#################################
# system_log.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab1 > system_log.py
# type: log
# functionality: view system log
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
import re

from collections import deque

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Count_Log_Files, Count_Log_Lines, Dialogue, Log, Log_Title, Notification, TextBox

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
HOME = configuration.HOME
LOG_NEW = configuration.LOG_NEW
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
VIEW_LOG_LIMIT = int(ADDON.getSetting('view_log_limit'))

# ============================================================
# System
# ============================================================

System = ('[COLOR %s]log > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: System_Log
# ============================================================

def System_Log(log_file):
	
	New_Old = 'New' if log_file == LOG_NEW else 'Old'

	if Count_Log_Lines(log_file) == 0:
		Notification(Addon_Title, '[COLOR %s]%s System Log: 0 lines in log[/COLOR]' % (TEXT_GENERAL, New_Old))
		return False

	system_log = []

	try:
		with open(log_file, 'r', encoding = 'utf-8', errors = 'ignore') as file:
			last_lines = deque(file, maxlen = VIEW_LOG_LIMIT)
			content = ''.join(last_lines)
			content = content.replace('\n', '[NL]')
			content = ('[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, content))
			matches = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--", re.S).findall(content)
			for item in matches:
				string = '-->Python callback/script returned the following error<--%s-->End of Python script error report<--' % item
				content = content.replace(string, '[COLOR %s]%s[/COLOR]' % (TEXT_VALUE, string))
			content = content.replace('WARNING', '[COLOR %s]WARNING[/COLOR]' % TEXT_HIGHLIGHT).replace('ERROR', '[COLOR %s]ERROR[/COLOR]' % TEXT_VALUE).replace('[NL]', '\n').replace(': EXCEPTION Thrown (PythonToCppException) :', '[COLOR %s]: EXCEPTION Thrown (PythonToCppException) :[/COLOR]' % TEXT_ITEM)
			content = content.replace('\\\\', '\\').replace(HOME, '')

			if content:
				system_log.append((log_file, content))

	except (OSError, UnicodeDecodeError) as e:
		Log(Log_Title + System + 'System Log: file error[CR]%s' % (New_Old, e), xbmc.LOGINFO)

	for log_file, content in system_log:
		TextBox('[B]%s[/B][COLOR %s][CR]%s System Log: [COLOR %s]%s[LIGHT] lines[/COLOR] (Limit: %s lines)[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, New_Old, TEXT_VALUE, Count_Log_Lines(log_file), VIEW_LOG_LIMIT), content)