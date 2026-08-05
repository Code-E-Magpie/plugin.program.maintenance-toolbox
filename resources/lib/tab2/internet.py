# ============================================================
#################################
# internet.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > wizard.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab2 > internet.py
# type: data source
# functionality: API (Application Programming Interface) internet information e.g. ISP, external IP address etc.
# development:
#	- new configuration using single data source (original dual source failed testing)
#	- user interface indicates when internet.py file needs updating i.e. when internet is connected but no data returned
#	- added notification when network "Not connected"
#	- functions consolidated to plugin.program.maintenance-toolbox > resources > lib > common > function.py
#	- variables consolidated to plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
#	- code debugged and reengineered if required using https://aipy.dev/tools

# ============================================================
# File used by
# ============================================================

# information.py (API only)
# interface.py

# ============================================================
# Import
# ============================================================

import xbmc
import json, os

from urllib.error import URLError, HTTPError
import urllib.request

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Log, Log_Title, Notification

# ============================================================
# Variables
# ============================================================

ADDON_DATA = configuration.ADDON_DATA
API = 'http://ip-api.com/json'
TEXT_GENERAL = configuration.TEXT_GENERAL
USER_AGENT = configuration.USER_AGENT

# ============================================================
# Internet
# ============================================================

Internet = ('[COLOR %s]internet > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: writejson(specs)
# ============================================================

jsonfile = os.path.join(ADDON_DATA, 'var.json')

def writejson(data):

	try:
		with open(jsonfile, 'w', encoding='utf-8') as file:
			json.dump(data, file, indent = 2)

	except (IOError, OSError, json.JSONDecodeError) as e:
		Log(Log_Title + Internet + 'Show Internet Information: writejson file error[CR]%s' % str(e), xbmc.LOGERROR)

# ============================================================
# FUNCTION: Data_Internet
# ============================================================

def Data_Internet():

	NETWORK_STATE = xbmc.getInfoLabel('Network.LinkState').replace('Link: ', '')
	network_state = NETWORK_STATE
	if network_state == 'Not connected':
		Notification(Addon_Title, '[COLOR %s]Show Internet Information: check network / refresh tab & try again[/COLOR]' % TEXT_GENERAL)

		return None, None, None, None, None, None, None, None, None

	try:
		request = urllib.request.Request(API)
		request.add_header('User-Agent', USER_AGENT)
		with urllib.request.urlopen(request) as response:
			response = json.load(response)

	# Handle the case where the response does not contain the expected keys or values
	except (KeyError, TypeError, ValueError) as e:
		Log(Log_Title + Internet + 'Show Internet Information: file content error[CR]%s' % str(e), xbmc.LOGERROR)

		return None, None, None, None, None, None, None, None, None

	# Handle the case where the URL is not accessible or the response is not in the expected format
	except (URLError, HTTPError) as e:
		Log(Log_Title + Internet + 'Show Internet Information: URL not accessible or unexpected format[CR]%s' % str(e), xbmc.LOGERROR)

		return None, None, None, None, None, None, None, None, None

	IP_REQUEST = response.get('status', 'None')
	COUNTRY = response.get('country', 'None')
	COUNTRY_CODE = response.get('countryCode', 'None')
	REGION = response.get('region', 'None')
	REGION_NAME = response.get('regionName', 'None')
	CITY = response.get('city', 'None')
	ZIP = response.get('zip', 'None')
	LATITUDE = response.get('lat', 'None')
	LONGITUDE = response.get('lon', 'None')
	TIMEZONE = response.get('timezone', 'None')
	ISP = response.get('isp', 'None')
	ORGANISATION = response.get('org', 'None')
	AS_NUMBER = response.get('as', 'None')
	INTERNET_IP = response.get('query', 'None')

	return (IP_REQUEST, COUNTRY, REGION_NAME, CITY, ZIP, TIMEZONE, ISP, AS_NUMBER, INTERNET_IP)