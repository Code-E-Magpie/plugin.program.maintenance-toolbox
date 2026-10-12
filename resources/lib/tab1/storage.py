# ============================================================
#################################
# storage.py by Code-E-Magpie
#################################
# ============================================================

# sourced from: plugin.program.aliundek19gui.maintenance.wizardz > default.py
# location: plugin.program.maintenance-toolbox > resources > lib > tab1 > storage.py
# type: data source
# functionality: storage size (free, used and total space) for /storage/emulated/0/
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

import os

from resources.lib.common.function import Size_Convert

# ============================================================
# Variables
# ============================================================

stat = os.statvfs('/storage/emulated/0/')

# ============================================================
# FUNCTION: Data_Storage
# ============================================================

def Data_Storage():
	
	size = stat.f_frsize * stat.f_blocks/1024/1024
	free = stat.f_frsize * stat.f_bfree/1024/1024
	used = size - free

	total_storage = Size_Convert(int(float(size))*1024*1024)
	free_storage = Size_Convert(int(float(free))*1024*1024)
	used_storage = Size_Convert(int(float(used))*1024*1024)

	return total_storage, free_storage, used_storage