Import("env")

import requests
import os
import filecmp
import shutil

from platformio import util
from requests.exceptions import Timeout, ConnectionError

# Get the latest file
def update_file(url_base, base_path, file_name):
	# Split file name
	name, extension = os.path.splitext(file_name)

	# Prepare paths
	file_path = base_path + file_name
	tmp_path = base_path + name + '.tmp'
	bak_path = base_path + name + '.bak'

	# Download the most recent file
	print 'Fetching', file_name
	url = url_base + file_name
	request_result = requests.get(url, allow_redirects = True, headers = {'Cache-Control': 'no-cache'}, timeout = 1)

	# Save it to a .tmp file
	file = open(tmp_path, 'wb')
	file.write(request_result.content)
	file.close()

	print 'Comparing', file_name

	# If file doesn't already exist
	if not os.path.exists(file_path):
		# Create file
		print('Saving %(file_name)')
		file = open(file_path, 'wb')
		file.write(request_result.content)
		file.close()

		# And create a backup file
		shutil.copyfile(file_path, bak_path)

	# Else if file exists
	# and it is different to the temp file
	elif not filecmp.cmp(tmp_path, file_path):
		print('New version found.')

		# Create a backup file
		print 'Creating backup of original', file_name
		#os.rename(file_path, bak_path)
		shutil.copyfile(file_path, bak_path)

		# Overwrite the original file
		print 'Saving new version as', file_name
		file = open(file_path, 'wb')
		file.write(request_result.content)
		file.close()

	# Delete tmp file
	if os.path.exists(tmp_path):
		os.remove(tmp_path)

	return True

# Check if platformio.ini is configured to check for update
def main():
	try:
		config = util.load_project_config()
		disable_ld_auto_update = config.get("env:pokitto", "disable_ld_auto_update")
		do_update = not bool(disable_ld_auto_update)
	except:
		# Couldn't find 'disable_ld_auto_update' entry, assume True
		do_update = True

	platformio_home = env['PIOHOME_DIR']
	patch_path = platformio_home + '/packages/framework-mbed/targets/TARGET_NXP/TARGET_LPC11U6X/device/TOOLCHAIN_GCC_ARM/TARGET_LPC11U68/'
	url_base = 'https://raw.githubusercontent.com/pokitto/PokittoIO/master/src/hal/LPC11U68/mbed_patches/arm_gcc/'

	# If platformio.ini is configured to check for update
	if do_update:
		try:
			update_file(url_base, patch_path, 'startup_LPC11U68.cpp')
			update_file(url_base, patch_path, 'LPC11U68.ld')
		except ConnectionError:
			print('Could not connect')
			return False
		except Timeout:
			print('Request timed out')
			return False
		except:
			print('Unexpected error')
			return False

	return True

main()

#env['CPPSUFFIXES'].append('.ino')