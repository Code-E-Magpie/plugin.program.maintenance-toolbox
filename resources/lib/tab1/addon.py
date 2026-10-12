# ============================================================
#################################
# addon.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > default.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab1 > addon.py
# type: data source
# functionality: user installed add-on count by type and total + built-in add-on count for repository and skin
# development:
#	- user installed add-ons count folders in special://home/addons location (includes "packages" and "temp" folders)
#	- user installed add-ons count split into more types e.g. skin, weather etc. (excludes "packages" and "temp" folders)
#	- type derived from <provides> in addon.xml and folder name (Add-on ID) of user installed add-ons
#		see https://kodi.wiki/view/Addon.xml#%3Cprovides%3E_element
#	- Kodi built-in add-on count for repository and skin (Estuary skin and Kodi Add-on repository)
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
import glob, os, re, sqlite3

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Addons_Db, Dialogue, Log, Log_Title, TextBox

# ============================================================
# Variables
# ============================================================

ADDONS = configuration.ADDONS
DATABASE = configuration.DATABASE
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
XBMCBINADDONS = configuration.XBMCBINADDONS

# ============================================================
# Addon
# ============================================================

Addon = ('[COLOR %s]addon > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Check_Addon
# ============================================================

def Check_Addon():

	addons_folders, exception, game, inputstream, metadata, music, other, others, picture, program, repository, resource, service, skin, video, weather, user_addons = Data_Addon()

	# check folders and <provides> reconcile (User Information for Add-on Information column runs check)
	check_folders = int(str(len(game))) + int(str(len(inputstream))) + int(str(len(metadata))) + int(str(len(other))) + int(str(len(repository))) + int(str(len(resource))) + int(str(len(service))) + int(str(len(skin))) + int(str(len(weather)))
	provides = int(str(len(exception))) + int(str(len(music))) + int(str(len(others))) + int(str(len(picture))) + int(str(len(program))) + int(str(len(video)))

	if check_folders != provides:
		Dialogue.ok(Addon_Title, '[COLOR %s]Check Addon: [LIGHT](User Information)[CR][COLOR %s]Add-on Information reconciliation error.[CR]The folders and <provides> figures do not match.[/LIGHT][/COLOR][CR]Check resources.lib.tab1.addon.py[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
		return 'check addon.py'

# ============================================================
# FUNCTION: Data_Addon
# ============================================================

def Data_Addon():

	# User installed add-ons count folders in special://home/addons location (includes "packages" and "temp" folders)
	addons = glob.glob(os.path.join(ADDONS, '*/'))
	addons_folders = len(addons)

	# User installed add-ons count by type based on folder name (excludes "packages" and "temp" folders)
	game = []; inputstream = []; metadata = []; other = []; repository = []; resource = []; service = []; skin = []; weather = []

	for folder in sorted(addons, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]

		# Exclude "packages" and "temp" folders
		if foldername in ('packages', 'temp'): continue

		# User installed add-ons count by type based on folder name (excludes "packages" and "temp" folders)
		if foldername.startswith('game'): game.append(foldername)
		elif foldername.startswith('inputstream'): inputstream.append(foldername)
		elif foldername.startswith('metadata'): metadata.append(foldername)
		elif foldername.startswith('repository'): repository.append(foldername)
		elif foldername.startswith('resource'): resource.append(foldername)
		elif foldername.startswith('service'): service.append(foldername)
		elif foldername.startswith('skin'): skin.append(foldername)
		elif foldername.startswith('weather'): weather.append(foldername)
		else: other.append(foldername)

	# User installed add-ons count by type based on <provides> (excludes "packages" and "temp" folders)
	exception = []; music = []; others = []; picture = []; program = []; video = []

	# User installed add-ons count (excludes "packages" and "temp" folders)
	user_addons = 0
	
	for folder in sorted(addons, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		
		# Exclude "packages" and "temp" folders
		if foldername in ('packages', 'temp'): continue
					
		# Read <provides> in addon.xml (does not exist in all addon.xml files and excludes "packages" and "temp" folders)
		addon_xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addon_xml):
			try:
				with open(addon_xml, 'r', encoding='utf-8') as file:
					addon_xml_content = file.read()
					provides = re.findall(r'<provides>(.+?)</provides>', addon_xml_content)
					
					# User installed add-ons count by type derived from <provides> in addon.xml
					# (excludes "packages" and "temp" folders)
					if provides:
						providers = provides[0].split('|')
						for provides in providers:   
							if 'video' in providers[0]: video.append(foldername)
							elif 'audio' in providers[0]: music.append(foldername)
							elif 'image' in providers[0]: picture.append(foldername)
							elif 'executable' in providers[0]: program.append(foldername)

							# User installed add-ons count where <provides> in addon.xml value is non standard
							# (excludes "packages" and "temp" folders)
							else: exception.append(foldername)

					# User installed add-ons count where <provides> in addon.xml does not exist
					# (excludes "packages" and "temp" folders)
					else: others.append(foldername)

				# User installed add-ons count (excludes "packages" and "temp" folders)
				user_addons += 1

			except (OSError, UnicodeDecodeError) as e:
				Log(Log_Title + Addon + 'Add-on Information: error accessing or reading addon_xml[CR]%s' % str(e), xbmc.LOGERROR)

	return addons_folders, exception, game, inputstream, metadata, music, other, others, picture, program, repository, resource, service, skin, video, weather, user_addons

# ============================================================
# FUNCTION: Data_Addon_Builtin
# ============================================================

def Data_Addon_Builtin():

	try:
		# Check if the 'skin' and 'repository' folders exist in the XBMCBINADDONS directory
		builtin_skin = [folder for folder in os.listdir(XBMCBINADDONS) if folder.startswith('skin')]
		builtin_repository = [folder for folder in os.listdir(XBMCBINADDONS) if folder.startswith('repository')]

		return builtin_skin, builtin_repository

	except FileNotFoundError:

		Log(Log_Title + 'Add-on Information: built-in add-ons folder not found' % xbmc.LOGERROR)
		return 0, 0

	except OSError as e:

		Log(Log_Title + Addon + 'Add-on Information: built-in add-ons folder not accessible[CR]%s' % str(e), xbmc.LOGERROR)
		return 0, 0

# ============================================================
# FUNCTION: Disabled_Addons
# ============================================================

def Disabled_Addons():

	try:
		addons_db = Addons_Db()
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		disabled_count = 'SELECT COUNT (*) FROM installed WHERE enabled = 0'
		cursor.execute(disabled_count)
		disabled_count = cursor.fetchall()
		disabled_count = int(str(disabled_count)[2: -3])

		updates_count = "SELECT COUNT (*) FROM update_rules"
		cursor.execute(updates_count)
		updates_count = cursor.fetchall()
		updates_count = int(str(updates_count)[2: -3])

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Disabled Addons: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Addon + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Addon + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

		return disabled_count, updates_count