# ============================================================
#################################
# configuration.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.openwizard > resources > libs > common > config.py (drinfernoo)
# location: plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
# type: common
# functionality: paths and variables
# development:
#	- functions consolidated to plugin.program.maintenance-toolbox > resources > lib > common > function.py
#	- variables consolidated to plugin.program.maintenance-toolbox > resources > lib > common > configuration.py
#	- code debugged and reengineered if required using https://aipy.dev/tools

# ============================================================
# File used by
# ============================================================

# information.py
# interface.py
# service.py
# common.addonwindow.py
# common.function.py
# common.textbox.py
# footer.database_toolbox.py
# footer.footer_menu.py
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

# ============================================================
# Import
# ============================================================

import xbmc, xbmcaddon, xbmcvfs
import os

# ============================================================
# CLASS: Configuration
# ============================================================

class Configuration:

# ============================================================
# FUNCTION: __init__
# ============================================================

	def __init__(self):

		self.init_metadata()
		self.init_paths()
		self.init_interface()
		self.init_text()

# ============================================================
# FUNCTION: init_metadata
# ============================================================

	def init_metadata(self):

		self.ADDON_ID = xbmcaddon.Addon().getAddonInfo('id') # id in addons.xml
		self.ADDON = xbmcaddon.Addon(self.ADDON_ID)
		self.ADDON_DEVELOPER = self.ADDON.getAddonInfo('author') # provider-name in addons.xml (developer)
		self.ADDON_FANART = self.ADDON.getAddonInfo('fanart')
		self.ADDON_ICON = self.ADDON.getAddonInfo('icon')
		self.ADDON_NAME = self.ADDON.getAddonInfo('name') # name in addons.xml
		self.ADDON_PATH = self.ADDON.getAddonInfo('path')
		self.ADDON_PROFILE = self.ADDON.getAddonInfo('profile') # addon_data folder for addon_id
		self.ADDON_VERSION = self.ADDON.getAddonInfo('version') # version in addons.xml

# ============================================================
# FUNCTION: init_paths
# ============================================================

# Library paths / Source paths / Special paths sourced from https://kodi.wiki/view/Special_protocol

	def init_paths(self):

		# Library paths
		self.LIBRARY_MUSIC = xbmcvfs.translatePath('library://music/')
		self.LIBRARY_VIDEO = xbmcvfs.translatePath('library://video/')

		# Source paths
		self.SOURCES_MUSIC = xbmcvfs.translatePath('sources://music')
		self.SOURCES_VIDEO = xbmcvfs.translatePath('sources://video')

		# Special paths
		self.CDRIPS = xbmcvfs.translatePath('special://cdrips/')
		self.DATABASE = xbmcvfs.translatePath('special://database/') # normally special://masterprofile/Database
		self.HOME = xbmcvfs.translatePath('special://home/') # Kodi_data_folder
		self.HOME_ADDONS = xbmcvfs.translatePath('special://home/addons') # excludes builtin addons
		self.HOME_MEDIA = xbmcvfs.translatePath('special://home/media') # points to media folder in Kodi_data_folder
		self.HOME_MEDIA_FONTS = xbmcvfs.translatePath('special://home/media/Fonts') # user defined fonts in media folder in Kodi_data_folder
		self.LOGPATH = xbmcvfs.translatePath('special://logpath/') # points to log file location
		self.MASTERPROFILE = xbmcvfs.translatePath('special://masterprofile/') # normally located at special://home/userdata
		self.MUSICARTISTSINFO = xbmcvfs.translatePath('special://musicartistsinfo') # points to the Artist_information_folder if set
		self.MUSICPLAYLISTS = xbmcvfs.translatePath('special://musicplaylists/') # normally special://profile/playlists/music.
		self.PROFILE = xbmcvfs.translatePath('special://profile/') # points to special://masterprofile/profile_name (or special://masterprofile if no profile in use)
		self.PROFILE_ADDON_DATA = xbmcvfs.translatePath('special://profile/addon_data') # addon_data folder located in the Userdata folder
		self.PROFILE_PLAYLISTS = xbmcvfs.translatePath('special://profile/playlists') # access to Mixed playlist folder
		self.RECORDINGS = xbmcvfs.translatePath('special://recordings/') # saved PVR recordings
		self.SCREENSHOTS = xbmcvfs.translatePath('special://screenshots/') # Kodi screenshots
		self.SKIN = xbmcvfs.translatePath('special://skin/') # currently active skin's root directory
		self.SUBTITLES = xbmcvfs.translatePath('special://subtitles/') # user defined custom path - set in video settings
		self.TEMP = xbmcvfs.translatePath('special://temp/') # normally special://home/temp
		self.TEMP_FONTS = xbmcvfs.translatePath('special://temp/fonts') # MKV fonts extracted and temporarily stored
		self.THUMBNAILS = xbmcvfs.translatePath('special://thumbnails/') # normally special://masterprofile/Thumbnails
		self.USERDATA = xbmcvfs.translatePath('special://userdata/') # alias from special://masterprofile
		self.VIDEOPLAYLISTS = xbmcvfs.translatePath('special://videoplaylists/') # normally special://profile/playlists/video
		self.XBMC = xbmcvfs.translatePath('special://xbmc/') # special://kodi/ does not exist
		self.XBMC_MEDIA_FONTS = xbmcvfs.translatePath('special://xbmc/media/Fonts') # Kodi bundled fonts files
		self.XBMC_SYSTEM = xbmcvfs.translatePath('special://xbmc/system') # system folder in installation root directory
		self.XBMCBINADDONS = xbmcvfs.translatePath('special://xbmcbinaddons') # built-in add-ons folder in installation root directory

		# Folder paths
		self.ADDON_DATA = os.path.join(self.USERDATA, 'addon_data')
		self.ADDON_DATA_ID = os.path.join(self.ADDON_DATA, self.ADDON_ID)
		self.ADDONS = os.path.join(self.HOME, 'addons')
		self.ADDONS_PACKAGES = os.path.join(self.ADDONS, 'packages')
		self.ADDONS_TEMP = os.path.join(self.ADDONS, 'temp')
		self.ARCHIVE_CACHE = os.path.join(self.HOME, 'temp', 'archive_cache')
		self.SKINS_MEDIA = os.path.join(self.ADDON_PATH, 'resources', 'skins', 'defaultSkin', 'media')

		# File paths
		self.ADVANCED = os.path.join(self.USERDATA, 'advancedsettings.xml')
		self.FAVOURITES = os.path.join(self.USERDATA, 'favourites.xml')
		self.GUISETTINGS = os.path.join(self.USERDATA, 'guisettings.xml')
		self.LOG_NEW = os.path.join(self.LOGPATH, 'kodi.log')
		self.LOG_OLD = os.path.join(self.LOGPATH, 'kodi.old.log')
		self.PROFILES = os.path.join(self.USERDATA, 'profiles.xml')
		self.SOURCES = os.path.join(self.USERDATA, 'sources.xml')

# ============================================================
# FUNCTION: init_interface
# ============================================================

	def init_interface(self):

		# Backup paths for files and folders
		self.BACKUPLOCATION = self.ADDON.getSetting('backup_location') if not self.ADDON.getSetting('backup_location') == '' else '/storage/emulated/0/Download/Kodi'

		# Tab: Network + Internet
		self.REPOSITORIES_TXT = os.path.join(self.BACKUPLOCATION, 'MT_repositories.txt')
		self.SOURCES_TXT = os.path.join(self.BACKUPLOCATION, 'MT_sources.txt')

		# Tab: Backup + Restore
		self.FAVOURITES_FILE = os.path.join(self.BACKUPLOCATION, 'MT_favourites', 'favourites.xml')
		self.FAVOURITES_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_favourites')
		self.GUISETTINGS_FILE = os.path.join(self.BACKUPLOCATION, 'MT_guisettings', 'guisettings.xml')
		self.GUISETTINGS_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_guisettings')
		self.PROFILES_FILE = os.path.join(self.BACKUPLOCATION, 'MT_profiles', 'profiles.xml')
		self.PROFILES_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_profiles')
		self.SOURCES_FILE = os.path.join(self.BACKUPLOCATION, 'MT_sources', 'sources.xml')
		self.SOURCES_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_sources')

		# Tab: Backup + Delete
		self.ADDON_DATA_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_addon_data')
		self.ADDON_DATA_LIST = os.path.join(self.BACKUPLOCATION, 'MT_addon_data.txt')
		self.ADDONS_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_addons')
		self.ADDONS_LIST = os.path.join(self.BACKUPLOCATION, 'MT_addons.txt')
		self.LOG_NEW_BACKUP = os.path.join(self.BACKUPLOCATION, 'MT_logs', 'kodi.log')
		self.LOG_OLD_BACKUP = os.path.join(self.BACKUPLOCATION, 'MT_logs', 'kodi.old.log')
		self.LOGS_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_logs')
		self.LOGS_LIST = os.path.join(self.BACKUPLOCATION, 'MT_logs.txt')
		self.USERDATA_FOLDER = os.path.join(self.BACKUPLOCATION, 'MT_userdata')
		self.USERDATA_LIST = os.path.join(self.BACKUPLOCATION, 'MT_userdata.txt')
		self.XBMCBINADDONS_LIST = os.path.join(self.BACKUPLOCATION, 'MT_addons_builtin.txt')

# ============================================================
# FUNCTION: init_text
# ============================================================

	def init_text(self):

		# Text colour variables
		self.TEXT_ADDON = self.ADDON.getSetting('text_addon')
		self.TEXT_COLUMN = self.ADDON.getSetting('text_column')
		self.TEXT_DARK = self.ADDON.getSetting('text_dark')
		self.TEXT_DIM = self.ADDON.getSetting('text_dim')
		self.TEXT_GENERAL = self.ADDON.getSetting('text_general')
		self.TEXT_HIGHLIGHT = self.ADDON.getSetting('text_highlight')
		self.TEXT_INDICATOR = self.ADDON.getSetting('text_indicator')
		self.TEXT_ITEM = self.ADDON.getSetting('text_item')
		self.TEXT_VALUE = self.ADDON.getSetting('text_value')

# ============================================================
# configuration = Configuration()
# ============================================================

configuration = Configuration()