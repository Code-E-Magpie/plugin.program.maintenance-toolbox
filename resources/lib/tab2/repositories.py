# ============================================================
#################################
# repositories.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: new development
# location: plugin.program.maintenance-toolbox > resources > lib > tab2 > repositories.py
# type: connection
# functionality: check repositories in the repo table of the Addons#.db database (Addons33.db for Kodi Omega 21.2)
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
import os, sqlite3

from resources.lib.common.configuration import configuration
from resources.lib.common.function import Add_Blank, Addon_Title, Addons_Db, Dialogue, Log, Log_Title, Now, TextBox

# ============================================================
# Variables
# ============================================================

ADDON = configuration.ADDON
DATABASE = configuration.DATABASE
TEXT_DARK = configuration.TEXT_DARK
TEXT_GENERAL = configuration.TEXT_GENERAL
TEXT_ITEM = configuration.TEXT_ITEM
TEXT_VALUE = configuration.TEXT_VALUE

# ============================================================
# Repositories
# ============================================================

Repositories = ('[COLOR %s]repositories > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Check_Repositories
# ============================================================

def Check_Repositories():

	addons_db = Addons_Db()

	Dialogue.ok(Addon_Title, '[COLOR %s]Check Repositories: [LIGHT](Check Information)[CR][COLOR %s]Repositories may not work due to internet connectivity issues;[CR]or the host server being unavailable (maintenance etc.)[/LIGHT][/COLOR][CR]Run at different times on different days before removing.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	Log(Log_Title + Repositories + '[COLOR %s][LIGHT]Started (check repositories: %s%s)[/LIGHT][/COLOR]' % (TEXT_DARK, DATABASE, addons_db), xbmc.LOGINFO)

	try:
		connection = sqlite3.connect(os.path.join(DATABASE, addons_db))
		cursor = connection.cursor()

		repository_count = "SELECT COUNT (*) FROM repo"
		cursor.execute(repository_count)
		repository_count = cursor.fetchall()
		repository_count = int(str(repository_count)[2: -3])

		not_working = "SELECT COUNT (*) FROM repo WHERE checksum IS NULL"
		cursor.execute(not_working)
		not_working = cursor.fetchall()
		not_working = int(str(not_working)[2: -3])
		working = str(repository_count - not_working)

		if not_working == 0:
			repo_table = "SELECT CASE WHEN checksum IS NULL THEN 'Bad     ' ELSE 'Good    ' END AS status, lastcheck, nextcheck, CASE WHEN length(version) >= 8 THEN version ELSE substr(version || '        ', 1, 8) END AS version, addonID FROM repo ORDER BY LOWER(addonID) ASC"
		if not_working != 0:
			repo_table = "SELECT CASE WHEN checksum IS NULL THEN 'Bad     ' ELSE 'Good    ' END AS status, lastcheck, nextcheck, CASE WHEN length(version) >= 8 THEN version ELSE substr(version || '        ', 1, 8) END AS version, addonID FROM repo WHERE checksum IS NULL ORDER BY LOWER(addonID) ASC"

		cursor.execute(repo_table)
		repo_table = cursor.fetchall()

		connection.commit()

	except sqlite3.Error as e:
		Dialogue.ok(Addon_Title, '[COLOR %s]Check Repositories: [LIGHT](User Information)[CR][COLOR %s]Unable to access: [COLOR %s]%s[/COLOR] database.[CR]The database may not exsist.[/LIGHT][/COLOR][CR]See Kodi System Log for details.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, TEXT_VALUE, addons_db))
		Log(Log_Title + Repositories + '%s read error: %s' % (addons_db, str(e)), xbmc.LOGERROR)
		return ''

	finally:
		try:
			if connection:
				connection.close()

		except UnboundLocalError as e:
			Log(Log_Title + Repositories + '%s connection error: %s' % (addons_db, str(e)), xbmc.LOGERROR)

	ADDON.setSetting('repositories_last_check', Now())
	ADDON.setSetting('repositories_not_work', str(not_working))
	ADDON.setSetting('repositories_work', working)
	Log(Log_Title + Repositories + '%s in %s database: %s working + %s not working' % (repository_count, addons_db, working, not_working), xbmc.LOGINFO)

	blank = Add_Blank()
	repo_table = str(repo_table).replace("[('","Status', 'Kodi Last Checked  ', 'Kodi Next Check    ', 'Version ', 'Add-on ID'), ('").replace("')]","").replace("'), ('",("\n\n" if blank == 'true' else "\n")).replace("', '","\t\t")
	
	if not_working == 0:
		Dialogue.ok(Addon_Title, '[COLOR %s]Check Repositories: [LIGHT](Check Information)[CR][COLOR %s]No repository issues identified in %s database.[CR]All the repositories appear to be working.[/LIGHT][/COLOR][CR]Press OK for a list of all the repositories.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM, addons_db))
		Working_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('REPOSITORIES ALL WORKING'), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, repo_table)
		TextBox('[B]%s[/B][CR][COLOR %s]Repositories: [/COLOR][COLOR %s]%s[/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, repository_count), Working_Text)

	elif not_working != 0:
		Not_Working_Text = '[COLOR %s][B]%s[/B][COLOR %s][LIGHT][CR](Data Source: %s%s)[/LIGHT][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('REPOSITORIES NOT WORKING'), TEXT_VALUE, DATABASE, addons_db, TEXT_GENERAL, repo_table)
		TextBox('[B]%s[/B][CR][COLOR %s]Repositories: [/COLOR][COLOR %s]%s  [/COLOR][COLOR %s][LIGHT]Not working: [/COLOR][COLOR %s]%s[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, repository_count, TEXT_ITEM, TEXT_VALUE, not_working), Not_Working_Text)
		Dialogue.ok(Addon_Title, '[COLOR %s]Check Repositories: [LIGHT](Check Information)[CR][COLOR %s]Check My add-ons for updates. Select repository > versions.[CR]A new source for the repository may be needed.[/LIGHT][/COLOR][CR]Run at different times on different days before removing.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))

	Log(Log_Title + Repositories + '[COLOR %s][LIGHT]Finished (check repositories: %s%s)[/LIGHT][/COLOR]' % (TEXT_DARK, DATABASE, addons_db), xbmc.LOGINFO)