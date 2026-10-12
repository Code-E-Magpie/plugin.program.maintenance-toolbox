# ============================================================
#################################
# system_log_errors.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab1 > system_log_errors.py
# type: log
# functionality: view system log errors
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

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Count_Log_Errors, Count_Log_Lines, Log, Log_Title, Notification, TextBox

# ============================================================
# Variables
# ============================================================

HOME = configuration.HOME
LOG_NEW = configuration.LOG_NEW
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE

# ============================================================
# System_Errors
# ============================================================

System_Errors = ('[COLOR %s]log errors > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: System_Log_Errors
# ============================================================

def System_Log_Errors(log_file):

	New_Old = 'New' if log_file == LOG_NEW else 'Old'

	if Count_Log_Lines(log_file) == 0:
		Notification(Addon_Title, '[COLOR %s]%s System Log Errors: 0 lines in log[/COLOR]' % (TEXT_GENERAL, New_Old))
		return False

	system_log_errors = []

	try:
		with open(log_file, 'r', encoding = 'utf-8', errors = 'ignore') as file:
			content = file.read()
			content = content.replace('\n', '[CR]').replace('\r', '')
			matches = re.compile(r"-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(content)[::-1]

			if matches:
				system_log_errors.append(log_file)

	except (OSError, UnicodeDecodeError) as e:
		Log(Log_Title + System_Errors + '%s System Log Errors: file error %s' % (New_Old, e), xbmc.LOGINFO)

	if system_log_errors:
		string = ''

		index = 0

		for match in matches:
			print(index, match)

			index += 1			

			string += '[COLOR %s]%s System Log Error: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]%s[/COLOR][CR]' % (TEXT_ITEM, New_Old, TEXT_VALUE, str(index), TEXT_GENERAL, match.replace(HOME, '/').replace('										', ''))

		TextBox('[B]%s[/B][COLOR %s][CR]%s System Log Errors: [COLOR %s]%s[/COLOR][LIGHT] (newest at the top)[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, New_Old, TEXT_VALUE, Count_Log_Errors(log_file)), string)

	else:
		Notification(Addon_Title, '[COLOR %s]%s System Log Errors: 0 errors found[/COLOR]' % (TEXT_GENERAL, New_Old))