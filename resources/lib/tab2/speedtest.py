# ============================================================
#################################
# speedtest.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: script.ezmaintenanceplus > default.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab2 > speedtest.py
# type: connection
# functionality: function to run speedtest_ookla.py
# development:
#	- last checked date captured using ADDON.setSetting and visible in Settings
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
import csv, os, urllib.parse

from datetime import date, datetime, timedelta

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, Log, Log_Title, Notification, Now

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
ADDON_DATA_ID = configuration.ADDON_DATA_ID
SPEEDTEST_TXT = os.path.join(ADDON_DATA_ID, 'speedtest.txt')
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_ITEM = configuration.TEXT_ITEM

# ============================================================
# Speedtest
# ============================================================

Speedtest = ('[COLOR %s]speedtest > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Data_Speedtest
# ============================================================

def Data_Speedtest():

	try:
		with open(SPEEDTEST_TXT, 'r') as file:
			lines = file.readlines()
			if len(lines) < 14:
				Log(Log_Title + Speedtest + 'Data Speedtest: speedtest.txt contains too few rows', xbmc.LOGERROR)

				return None, None, None, None, 0, 0, 0, 0, None, None

			data = lines[11].strip().split(',')
			if len(data) != 10:
				Log(Log_Title + Speedtest + 'Data Speedtest: speedtest.txt items in row incorrect', xbmc.LOGERROR)

				return None, None, None, None, 0, 0, 0, 0, None, None

			ID, SPONSOR, NAME, TIMESTAMP, DATA, PING, DOWNLOAD, UPLOAD, URL, IP = data

			TIMESTAMP = datetime.fromisoformat(TIMESTAMP)
			TIMESTAMP = TIMESTAMP.strftime('%Y-%m-%d %H:%M:%S')
			PING = round(float(PING), 2)
			PING = '%.02f' % (PING)
			DOWNLOAD = round(float(DOWNLOAD) * 0.000001, 2)
			DOWNLOAD = '%.02f' % (DOWNLOAD)
			UPLOAD = round(float(UPLOAD) * 0.000001, 2)
			UPLOAD = '%.02f' % (UPLOAD)

			return (ID, SPONSOR, NAME, TIMESTAMP, DATA, PING, DOWNLOAD, UPLOAD, URL, IP)

	except FileNotFoundError:
		Log(Log_Title + Speedtest + 'Data Speedtest: speedtest.txt not found', xbmc.LOGERROR)

		return None, None, None, None, 0, 0, 0, 0, None, None

	except (IndexError, ValueError) as e:
		Log(Log_Title + Speedtest + 'Data Speedtest: speedtest.txt unexpected data format[CR]%s' % str(e), xbmc.LOGERROR)

		return None, None, None, None, 0, 0, 0, 0, None, None

	except Exception as e:
		Log(Log_Title + Speedtest + 'Data Speedtest: unexpected error[CR]%s' % str(e), xbmc.LOGERROR)

		return None, None, None, None, 0, 0, 0, 0, None, None

# ============================================================
# FUNCTION: Speedtest_Ookla
# ============================================================

def Speedtest_Ookla():

	NETWORK_STATE = xbmc.getInfoLabel('Network.LinkState').replace('Link: ', '')
	network_state = NETWORK_STATE
	if network_state == 'Not connected':
		Notification(Addon_Title, '[COLOR %s]Speedtest by Ookla: check network / refresh tab & try again[/COLOR]' % TEXT_GENERAL)
		return False

	INTERNET_STATE = xbmc.getInfoLabel('System.InternetState')
	internet_state = str(INTERNET_STATE).replace('. Check network settings.','')
	if internet_state != 'Connected':
		Notification(Addon_Title, '[COLOR %s]Speedtest by Ookla: check network / refresh tab & try again[/COLOR]' % TEXT_GENERAL)
		return False

	try:
		Dialogue.ok(Addon_Title, '[COLOR %s]Speedtest by Ookla: [LIGHT](User Information)[CR][COLOR %s][LIGHT]The next dialogue box shows the test running.[CR]The summary will follow the download figure.[/LIGHT][/COLOR][CR]Press summary OK for Speedtest Report.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
		Log(Log_Title + Speedtest + '[COLOR %s][LIGHT]Started (Speedtest by Ookla)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
		ADDON.setSetting('speedtest_last_checked', Now())

		xbmc.executebuiltin('RunScript("special://home/addons/plugin.program.maintenance-toolbox/resources/lib/tab2/speedtest_ookla.py")')

	except Exception as e:
		Notification(Addon_Title, '[COLOR %s]Speedtest by Ookla: error[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Speedtest + '[COLOR %s]Speedtest by Ookla: error[CR] %s[/COLOR]' % (TEXT_GENERAL, str(e)), xbmc.LOGERROR)
		return False

	return True

# ============================================================
# FUNCTION: Speedtest_Report
# ============================================================

def Speedtest_Report():
	
	ID, SPONSOR, NAME, TIMESTAMP, DATA, PING, DOWNLOAD, UPLOAD, URL, IP = Data_Speedtest()
	
	# extract the filename from the URL
	parsed = urllib.parse.urlparse(URL)
	basename = os.path.basename(parsed.path) # e.g. "18386195535.png"

	# ensure basename looks ok and has a .png extension; otherwise fallback
	if not basename or not basename.lower().endswith('.png'):
		basename = 'speedtest.png'
	else:
		basename = 'speedtest_' + basename

	speedtest_png = os.path.join(ADDON_DATA_ID, basename)

	if os.path.isfile(speedtest_png):
		try:
			speedtest_report = xbmcgui.WindowDialog()
			speedtest_report.addControl(xbmcgui.ControlImage(265, 200, 750, 400, speedtest_png))
			speedtest_report.doModal()

		except Exception as e:
			Log(Log_Title + Speedtest + '[COLOR %s]Speedtest Reportby Ookla: failed to display image[CR] %s[/COLOR]' % (TEXT_GENERAL, str(e)), xbmc.LOGERROR)
			Notification(Addon_Title, '[COLOR %s]Speedtest by Ookla Report: failed to display image[/COLOR]' % TEXT_GENERAL)

	else:
		Notification(Addon_Title, '[COLOR %s]Speedtest by Ookla Report: unavailable / run Speedtest by Ookla  	[/COLOR]' % TEXT_GENERAL)
		Log(Log_Title + Speedtest + 'Speedtest by Ookla Report: speedtest.png not found', xbmc.LOGINFO)