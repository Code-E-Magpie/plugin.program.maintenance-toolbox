# ============================================================
#################################
# reorder_favourites.py by Code-E-Magpie
#################################
# ============================================================

# ============================================================
# File information
# ============================================================

# sourced from: plugin.program.reorder-favourites > reorder_favourites.py
# location: plugin.program.maintenance-toolbox > resources > lib > footer > reorder_favourites.py
# type: footer
# functionality: reorder favourites in favourites.xml

# ============================================================
# Import
# ============================================================

import xbmc, xbmcgui, xbmcvfs
import math, re, sys

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Addon_Title, Dialogue, Count_Favourites, Log, Log_Title

try:

	# Python 2.x
	from HTMLParser import HTMLParser
	PARSER = HTMLParser()
	DECODE_STRING = lambda val: val.decode('utf-8')
except ImportError as e:

	# Python 3.4+ (see https://stackoverflow.com/a/2360639)
	import html
	PARSER = html
	DECODE_STRING = lambda val: val # Pass-through.

# ============================================================
# File used by
# ============================================================

# footer_menu.py

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
FAVOURITES = configuration.FAVOURITES
FAVOURITES_RESULT = 'ordfav.result'
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
TEXT_DARK = configuration.TEXT_DARK
TEXT_DIM = configuration.TEXT_DIM
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_HIGHLIGHT = configuration.TEXT_HIGHLIGHT
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE
THUMBNAILS_FORMAT = 'special://thumbnails/{folder}/{file}'

# ============================================================
# Favourites
# ============================================================

Favourites = ('[COLOR %s]favourites > [/COLOR]' % TEXT_GENERAL)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# User Interface
# ------------------------------------------------------------
# ============================================================

# ============================================================
# CLASS: ReorderFavourites
# ============================================================

class ReorderFavourites(xbmcgui.WindowXMLDialog):

# ============================================================
# FUNCTION: __init__
# ============================================================

	# Initializes the class and maps control IDs and action IDs to custom handler methods.
	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)

		# Map control IDs to custom handler methods. IDs in /resources/skins/default/1080i/ReorderFavourites.xml
		self.idHandlerDict = {
			8320: self.doSelect,
			8500: self.close,
			8501: self.startAgain,
		}

		# Map action IDs to custom handler methods.
		# See https://github.com/xbmc/xbmc/blob/master/xbmc/input/actions/ActionIDs.h
		self.actionHandlerDict = {
			# All click / select actions are already handled by 'idHandlerDict' above.
			# 7: self.doSelect, # ACTION_SELECT_ITEM
			9: self.doUnselectClose, # ACTION_PARENT_DIR
			10: self.doUnselectClose, # ACTION_PREVIOUS_MENU
			92: self.doUnselectClose, # ACTION_NAV_BACK
			# 100: self.doSelect, # ACTION_MOUSE_LEFT_CLICK
			# 108: self.doSelect, # ACTION_MOUSE_LONG_CLICK
			110: self.doUnselectClose, # ACTION_BACKSPACE
			8320: self.doUnselectClose, # ACTION_MOUSE_RIGHT_CLICK
		}
		self.noop = lambda: None

# ============================================================
# FUNCTION: doCustomModal
# ============================================================

	def doCustomModal(self, favouritesGen):

		allItems = [ ]
		artDict = {'thumb': None}

		for index, data in enumerate(favouritesGen):
			# Every ListItem contains the original favourite (label, thumb and URL).
			# Favourites are written back to the xml file when saving (only the order changes).
			listitem = xbmcgui.ListItem(data[0], path=data[2])
			artDict['thumb'] = data[1] # Slightly faster than recreating a dict on every item.
			listitem.setArt(artDict)
			listitem.setProperty('index', str(index)) # Helps resetting.
			allItems.append(listitem)

		self.allItems = allItems
		self.indexFrom = None # Integer index of the source item (or None when nothing is selected).
		self.isDirty = False # Bool indicating if there are any changes.
		self.doModal()

		return self.makeResult() if self.isDirty else ''

# ============================================================
# FUNCTION: doSelect
# ============================================================

	def doSelect(self):

		selectedPosition = self.panel.getSelectedPosition()
		if self.indexFrom == None:
			# Select a new item to reorder.
			self.indexFrom = selectedPosition
			self.panel.getSelectedItem().setProperty('selected', '1')

		else:
			# Reorder if item already selected.
			if self.indexFrom != selectedPosition:
				# Reorder uses the .pop() and .insert() methods of the 'self.allItems' list.
				itemFrom = self.allItems.pop(self.indexFrom)
				self.allItems.insert(selectedPosition, itemFrom)
				self.isDirty = True

				# Reset the selection state.
				self.indexFrom = None
				itemFrom.setProperty('selected', '')

				# Update the panel by clearing it and reloading all the items.
				self.panel.reset()
				self.panel.addItems(self.allItems)
				self.panel.selectItem(selectedPosition)

			else: # Unselect item if its reselected.
				self.indexFrom = None
				self.panel.getSelectedItem().setProperty('selected', '')

# ============================================================
# FUNCTION: doUnselectClose
# ============================================================

	def doUnselectClose(self):

		# Unselect item if one is selected, otherwise close it.
		if self.indexFrom != None:
			self.allItems[self.indexFrom].setProperty('selected', '')
			self.indexFrom = None

		else:
			self.close()

# ============================================================
# FUNCTION: makeResult
# ============================================================

	def makeResult(self):

		INDENT_STRING = ' ' * 4
		return '<favourites>\n' + '\n'.join((INDENT_STRING + listitem.getPath()) for listitem in self.allItems) + '\n</favourites>\n'

# ============================================================
# FUNCTION: onAction
# ============================================================

	def onAction(self, action):
		self.actionHandlerDict.get(action.getId(), self.noop)()

# ============================================================
# FUNCTION: onClick
# ============================================================

	def onClick(self, controlId):
		self.idHandlerDict.get(controlId, self.noop)()

# ============================================================
# FUNCTION: onInit
# ============================================================

	def onInit(self):

		header = '[B]%s[/B][CR][COLOR %s]Favourites: [COLOR %s]%s  [/COLOR][LIGHT]Rows: [COLOR %s]%s[/COLOR][/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, Count_Favourites(FAVOURITES), TEXT_VALUE, math.ceil(Count_Favourites(FAVOURITES)/5))
		close = '[COLOR %s][B]%s[/B][/COLOR]' % (TEXT_GENERAL, ' '.join('Close'))
		start_again = '[COLOR %s][B]%s[CR][CR]%s[/B][/COLOR]' % (TEXT_GENERAL, ' '.join('Start'), ' '.join('Again'))

		self.title = self.getControl(8200).setLabel(header)
		self.panel = self.getControl(8320)
		self.panel.reset()
		self.panel.addItems(self.allItems)
		self.setFocusId(8310) # Focus on the group containing the panel, not the panel itself.
		self.close = self.getControl(8500).setLabel(close)
		self.startAgain = self.getControl(8501).setLabel(start_again)

# ============================================================
# FUNCTION: startAgain
# ============================================================

	def startAgain(self):

		# Reload favourites in the original order.
		if Dialogue.yesno(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Start Again)[/LIGHT][CR]Start again ?[CR][COLOR %s]Changes will be lost.[CR]Favourites will reload in the original order.[/COLOR][/COLOR]' % (TEXT_GENERAL, TEXT_DIM), yeslabel = ('[COLOR %s]Start Again[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel[/COLOR]' % TEXT_HIGHLIGHT)):

			self.indexFrom = None
			self.allItems = sorted(self.allItems, key = lambda listitem: int(listitem.getProperty('index')))
			self.panel.reset()
			self.panel.addItems(self.allItems)

			Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Start Again[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

#####################################################################################

# ============================================================
# FUNCTION: Data_Generator_Favourites
# ============================================================

def Data_Generator_Favourites():

	file = xbmcvfs.File(FAVOURITES)
	contents = DECODE_STRING(file.read())
	file.close()

	namePattern = re.compile('name="([^"]+)')
	thumbPattern = re.compile('thumb="([^"]+)')

	for entryMatch in re.finditer('(<favourite\s[^<]+</favourite>)', contents):
		entry = entryMatch.group(1)

		match = namePattern.search(entry)
		name = PARSER.unescape(match.group(1)) if match else ''

		match = thumbPattern.search(entry)

		if match:
			thumb = PARSER.unescape(match.group(1))
			cacheFilename = xbmc.getCacheThumbName(thumb)

			if 'ffffffff' not in cacheFilename:
				if '.jpg' in thumb:
					cacheFilename = cacheFilename.replace('.tbn', '.jpg', 1)
				if '.png' in thumb:
					cacheFilename = cacheFilename.replace('.tbn', '.png', 1)
				thumb = THUMBNAILS_FORMAT.format(folder = cacheFilename[0], file = cacheFilename)

		else:
			thumb = ''

		# Yield a 3-tuple of name, thumb-url and the original favourite.
		yield name, thumb, entry

# ============================================================
# FUNCTION: Save_Favourites
# ============================================================

def Save_Favourites(xmlText):

	if not xmlText:
		return False

	try:
		file = xbmcvfs.File(FAVOURITES, 'w')
		file.write(xmlText)
		file.close()

	except Exception as e:
		Log(Log_Title + Favourites + 'Save Favourites: exception[CR]%s' % str(e), xbmc.LOGERROR)

	return True

# ============================================================
# FUNCTION: Window_Property_Clear
# ============================================================

def Window_Property_Clear(prop):
	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	window.clearProperty(prop)

# ============================================================
# FUNCTION: Window_Property_Get
# ============================================================

def Window_Property_Get(prop):
	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	return window.getProperty(prop)

# ============================================================
# FUNCTION: Window_Property_Set
# ============================================================

def Window_Property_Set(prop, data):
	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	window.setProperty(prop, data)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# Exit options
# ------------------------------------------------------------
# ============================================================

# ============================================================
# FUNCTION: Exit_Only
# ============================================================

def Exit_Only():
	Window_Property_Clear(FAVOURITES_RESULT)
	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Finished (Exit Only)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

# ============================================================
# FUNCTION: Save_Exit
# ============================================================

def Save_Exit():
	try:
		if Save_Favourites(Window_Property_Get(FAVOURITES_RESULT)):
			Window_Property_Clear(FAVOURITES_RESULT)
			Dialogue.ok(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Save + Exit)[/LIGHT][CR]Changes to favourites saved.[CR][COLOR %s]Exit and restart Kodi for the changes to take effect.[CR]Do not make further changes until Kodi is restarted.[/COLOR][/COLOR]' % (TEXT_GENERAL, TEXT_VALUE))

	except Exception as e:
		Log(Log_Title + Favourites + 'Save + Exit: exception[CR]%s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Finished (Save + Exit)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
# ============================================================

# ============================================================
# FUNCTION: Reorder_Favourites
# ============================================================

def Reorder_Favourites():

	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Started[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
	User_Interface = ReorderFavourites('ReorderFavourites.xml', ADDON.getAddonInfo('path'), 'default', '1080i')

	try:
		result = User_Interface.doCustomModal(Data_Generator_Favourites())
		Window_Property_Set(FAVOURITES_RESULT, result)

	except Exception as e:
		Log(Log_Title + Favourites + 'User Interface: exception[CR]%s' % str(e), xbmc.LOGERROR)

		Window_Property_Clear(FAVOURITES_RESULT)

	finally:
		if Dialogue.yesno(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Exit Options)[/LIGHT][CR]Save changes ?[CR][COLOR %s] > Save + Exit: Changes will be saved. Kodi restart required.[CR] > Exit Only: Changes will be lost.[/COLOR][/COLOR]' % (TEXT_GENERAL, TEXT_DIM), yeslabel = ('[COLOR %s]Save + Exit[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Exit Only[/COLOR]' % TEXT_HIGHLIGHT)):
			Save_Exit()

		else:
			Exit_Only()

		del User_Interface

if __name__ == "__main__":
	Reorder_Favourites()