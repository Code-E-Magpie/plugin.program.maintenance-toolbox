# ============================================================
#################################
# sources.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > wizard.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab2 > sources.py
# type: connection
# functionality: check sources excluding storage locations
# development:
#	- file content formatted
#	- some functions and variables renamed
#	- reworked Dialogue, Log and Notification
#	- last checked date and totals captured using ADDON.setSetting
#	- formatting of source name retained in notifications and dialogue boxes (colour, bold etc.)
#	- connection error handling added when network is "Not connected" or internet not "Connected"
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

import xbmc, xbmcgui
import os, re

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, DialogueProgress, Log, Log_Title, Notification, Now

import html.parser, urllib.error, urllib.parse, urllib.request
from sqlite3 import dbapi2 as database

try:
	from urllib.request import urlopen, Request
	from urllib.error import HTTPError, URLError
except ImportError:
	from urllib2 import urlopen, Request, HTTPError, URLError

try:
	import xml.etree.cElementTree as ET
except ImportError:
	try:
		import xml.etree.ElementTree as ET
	except ImportError:
		from xml.dom import minidom as DOM
		ET = None

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
SOURCES = configuration.SOURCES
SOURCES_TXT = configuration.SOURCES_TXT
TEXT_DARK = configuration.TEXT_DARK
TEXT_DIM = configuration.TEXT_DIM
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
URL_ATTEMPTS = int(ADDON.getSetting('URL_ATTEMPTS'))
URL_DELAY = int(ADDON.getSetting('URL_DELAY'))
USER_AGENT = configuration.USER_AGENT

# ============================================================
# Sources
# ============================================================

Sources = ('[COLOR %s]sources > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Check_URL_Status
# ============================================================

def Check_URL_Status(URL_path):

	if URL_path in ['http://', 'https://', '']:
		return False

	check = 0; URL_status = ''
	while check < URL_ATTEMPTS:
		check += 1

		try:
			request = urllib.request.Request(URL_path)
			request.add_header('User-Agent', USER_AGENT)
			response = urllib.request.urlopen(request)
			response.close()
			URL_status = True
			break

		except Exception as e:
			URL_status = str(e)

			Log(Log_Title + Sources + 'Check URL Status: %s [%s]' % (e, URL_path), xbmc.LOGINFO)
			xbmc.sleep(URL_DELAY)

	return URL_status

# ============================================================
# FUNCTION: Check_Sources
# ============================================================

def Check_Sources():

	if not os.path.exists(SOURCES):
		Notification(Addon_Title, '[COLOR %s]Check Sources: no sources.xml[/COLOR]' % TEXT_GENERAL)
		return False

	NETWORK_STATE = xbmc.getInfoLabel('Network.LinkState').replace('Link: ', '')
	network_state = NETWORK_STATE
	if network_state == 'Not connected':
		Notification(Addon_Title, '[COLOR %s]Check Sources: check network / refresh tab & try again[/COLOR]' % TEXT_GENERAL)
		return False

	INTERNET_STATE = xbmc.getInfoLabel('System.InternetState')	
	internet_state = str(INTERNET_STATE).replace('. Check network settings.','')
	if internet_state != 'Connected':
		Notification(Addon_Title, '[COLOR %s]Check Sources: check internet / refresh tab & try again[/COLOR]' % TEXT_GENERAL)
		return False

	Dialogue.ok(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](User Information)[CR][COLOR %s]Storage locations will be retained but not displayed.[CR]The format of source names will be retained and displayed.[/LIGHT][CR][/COLOR]e.g.[COLOR %s] × Official :[/COLOR][COLOR %s] Kodi Add-on repository[/COLOR][COLOR %s][I] (official kodi.tv mirror)[/I][/COLOR][/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_DARK, TEXT_ITEM, TEXT_DIM))
	Log(Log_Title + Sources + '[COLOR %s][LIGHT]Started (check sources: special://userdata/sources.xml)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

	sources = 0
	broken = []
	removed = []
	http_count = 0

	file = open(SOURCES, encoding = 'utf-8')
	string = file.read()
	string_replace = string.replace('\r','').replace('\n','').replace('\t','')
	extract = re.compile('<files>.+?</files>').findall(string_replace)
	file.close()

	if len(extract) > 0:

		sources_xml = re.compile('<source>.+?<name>(.+?)</name>.+?<path pathversion="1">(.+?)</path>.+?<allowsharing>(.+?)</allowsharing>.+?</source>').findall(extract[0])

		DialogueProgress.create(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](Cancel Button Deactivated)[/LIGHT][/COLOR]' % TEXT_GENERAL)

		for name, path, sharing in sources_xml:
			sources += 1

			sources_count = len(sources_xml)
			percentage = int(100 * (float(sources) /float(sources_count)))
			removed_count = int()

			DialogueProgress.update(percentage, '[COLOR %s]Check Sources: [LIGHT](Cancel Button Deactivated)[/COLOR][CR][COLOR %s]Storage locations will be retained but not displayed.[/LIGHT][/COLOR][CR]%s' % (TEXT_GENERAL, TEXT_ITEM, name) + '[CR][COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, path))

			if path.startswith('http'):
				http_count += 1

				not_working = len(broken)
				http_working = http_count - len(broken)
				other = sources_count - http_count
				working = sources_count - not_working

				status = Check_URL_Status(path)
				if not status == True:
					broken.append([name, path, sharing, status])

		DialogueProgress.close()

		if len(broken) > 0:

			Dialogue.ok(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](Check Information)[CR][COLOR %s]Sources may not work due to internet connectivity issues;[CR]or the host server being unavailable (maintenance etc.)[/LIGHT][/COLOR][CR]Run at different times on different days before removing.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

			choice = Dialogue.yesno(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](Check Summary)[/LIGHT][CR][COLOR %s] > Sources in xml file: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]	(Working: %s = %s http + %s other)[/COLOR][CR]Would you like to [COLOR %s]Keep[/COLOR] the [COLOR %s]%s[/COLOR] http sources not working ?[CR]Or [COLOR %s]Review Each One[/COLOR] and choose which to keep or remove ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, sources_count, TEXT_DIM, working, http_working, other, TEXT_HIGHLIGHT, TEXT_HIGHLIGHT, not_working, TEXT_VALUE), yeslabel = ('[COLOR %s]Review Each One[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep[/COLOR]' % TEXT_HIGHLIGHT))

			if choice == 0:
				removed == 0

			else:
				for name, path, sharing, status in broken:

					if Dialogue.yesno(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](Review Each One)[/LIGHT][/COLOR][CR]%s' % (TEXT_GENERAL, name) + '[CR][COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, path) + '[CR][COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, status), yeslabel = ('[COLOR %s]Remove Source[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Keep Source[/COLOR]' % TEXT_HIGHLIGHT)):

						removed.append([name, path, sharing, status])

						Log(Log_Title + Sources + '%s %s removed' % (name, path), xbmc.LOGINFO)
					else:
						Log(Log_Title + Sources + '%s %s kept' % (name, path), xbmc.LOGINFO)

			if len(removed) > 0:
				for name, path, sharing, status in removed: 
					string = string.replace('\n        <source>\n            <name>%s</name>\n            <path pathversion="1">%s</path>\n            <allowsharing>%s</allowsharing>\n        </source>' % (name, path, sharing), '')

				file = open(SOURCES, mode = 'w', encoding = 'utf-8')
				file.write(str(string))
				file.close()

				removed_count = len(removed)

				Dialogue.ok(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](Remove Summary)[/LIGHT][CR][COLOR %s] > Sources in xml file: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]	(Working: %s = %s http + %s other)[/COLOR][CR][COLOR %s] > Sources not working removed: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]	(Remove Source)[/COLOR][CR][COLOR %s] > Sources not working but kept: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]	(Keep Source)[/COLOR][/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, (sources_count - removed_count), TEXT_DIM, working, http_working, other, TEXT_ITEM, TEXT_VALUE, removed_count, TEXT_DIM, TEXT_ITEM, TEXT_VALUE, (not_working - removed_count), TEXT_DIM))

			else:
				Log(Log_Title + Sources + 'Check Sources: all sources kept', xbmc.LOGINFO)

			Dialogue.ok(Addon_Title, '[COLOR %s]Check Sources: [LIGHT](Final Summary)[/LIGHT][CR][COLOR %s] > Sources in xml file: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]	=  %s http + %s other[/COLOR][CR][COLOR %s] > Working: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]			=  %s http + %s other[/COLOR][CR][COLOR %s] > Not working: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]		=  %s http[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, (sources_count - removed_count), TEXT_DIM, (http_count - removed_count), other, TEXT_ITEM, TEXT_VALUE, working, TEXT_DIM, http_working, other, TEXT_ITEM, TEXT_VALUE, (not_working - removed_count), TEXT_DIM, (not_working - removed_count)))
			Log(Log_Title + Sources + '%s in file: %s working (%s http + %s other) + %s not working (%s http)' % ((sources_count - removed_count), working, http_working, other, (not_working - removed_count),  (not_working - removed_count)), xbmc.LOGINFO)
			ADDON.setSetting('sources_last_checked', Now())
			ADDON.setSetting('sources_not_working', (str(not_working - removed_count)))
			ADDON.setSetting('sources_working', (str(working)))

		else:
			Notification(Addon_Title, '[COLOR %s]Check Sources: %s sources (all working)  [/COLOR]' % (TEXT_GENERAL, sources_count))
			Log(Log_Title + Sources + 'Check Sources: %s sources (all working: %s http + %s other)' % (sources_count, http_working, other), xbmc.LOGINFO)
			ADDON.setSetting('sources_last_checked', Now())
			ADDON.setSetting('sources_not_working', '0')
			ADDON.setSetting('sources_working', str(sources_count))

	else:
		Notification(Addon_Title, '[COLOR %s]Check Sources: no sources in file[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Sources + 'Check Sources: no sources in file', xbmc.LOGINFO)
		ADDON.setSetting('sources_last_checked', Now())
		ADDON.setSetting('sources_not_working', '0')
		ADDON.setSetting('sources_working', '0')

	try:
		with open(SOURCES_TXT, "w") as file:
			file.write('Maintenance Toolbox > sources\n\nCreated: %s\n\nSource file: %s\nOutput file: %s\n\nSources in finished file: %s\nWorking: %s\nNot working: %s\n\nRemoved: %s\n%s\n\nNot working: %s\n%s\n\nSources in original file: %s\n%s\n\n' % (Now(), SOURCES, SOURCES_TXT, (sources_count - removed_count), working, (not_working - removed_count), removed_count, List_Clean(removed), not_working, List_Clean(broken), sources_count, List_Clean(List_Check(sources_xml))))

	except IOError as e:
		Log(Log_Title + Sources + '%s' % str(e), xbmc.LOGERROR)

	except Exception as e:
		Log(Log_Title + Sources + '%s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Sources + '[COLOR %s][LIGHT]Finished (check sources: special://userdata/sources.xml)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

# ============================================================
# FUNCTION: List_Check
# ============================================================

def List_Check(input_list):

	if isinstance(input_list, tuple): # Check if current element is a tuple
		return [List_Check(item) for item in input_list] # Convert to list

	elif isinstance(input_list, list): # If it's already a list, process each item
		return [List_Check(item) for item in input_list]

	else:
		return input_list # Return item if it's neither a tuple nor a list

# ============================================================
# FUNCTION: List_Clean
# ============================================================

def List_Clean(input_list):

	output_list = []

	for element in input_list:
		if isinstance(element, list):
			clean_list = str(element)[1:-1].replace(", ", " | ").replace("'", "")
			output_list.append(clean_list)

	return "\n".join(output_list)