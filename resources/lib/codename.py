# ============================================================
#################################
# codename.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > default.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab1 > codename.py
# type: data source
# functionality: codename derived from Kodi build version code
# development:
#	- file content formatted
#	- some functions and variables renamed
#	- new configuration including error handling
#	- user interface indicates when codename.py file needs updating i.e. when new version of Kodi is not in list
#		see https://kodi.wiki/view/Codename_history
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

# ============================================================
# FUNCTION:  Data_Codename
# ============================================================

def Data_Codename():

	try:
		xbmc_version = xbmc.getInfoLabel('System.BuildVersionCode')
		if len(xbmc_version) >= 4:
			version = float(xbmc_version[:4])
			if 8.0 <= version < 9.0:
				return 'Atlantis'
			elif 9.0 <= version < 9.1:
				return 'Babylon'
			elif 9.1 <= version < 10.0:
				return 'Camelot'
			elif 10.0 <= version < 11.0:
				return 'Dharma'
			elif 11.0 <= version < 12.0:
				return 'Eden'
			elif 12.0 <= version < 13.0:
				return 'Frodo'
			elif 13.0 <= version < 14.0:
				return 'Gotham'
			elif 14.0 <= version < 15.0:
				return 'Helix'
			elif 15.0 <= version < 16.0:
				return 'Isengard'
			elif 16.0 <= version < 17.0:
				return 'Jarvis'
			elif 17.0 <= version < 18.0:
				return 'Krypton'
			elif 18.0 <= version < 19.0:
				return 'Leia'
			elif 19.0 <= version < 20.0:
				return 'Matrix'
			elif 20.0 <= version < 21.0:
				return 'Nexus'
			elif 21.0 <= version < 22.0:
				return 'Omega'
			elif 22.0 <= version < 23.0:
				return 'Piers'
			else:
				return 'Update codename.py'
		else:
			return 'Update codename.py'
	except (ValueError, IndexError):
		return 'Update codename.py'