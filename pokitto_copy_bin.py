Import("env")

import os
import shutil

# Copy files
def copy_bin(target, source, env):
	# os.path.join is a Temporary work around
	# until I can find a way to evaluate env['BUILD_DIR']

	# Project build directory
	build_directory = os.path.join(env['PROJECTBUILD_DIR'], env['PIOENV'])

	# Project root directory
	project_directory = env['PROJECT_DIR']

	for source_file in source:
		# Get the file name
		file_name = source_file.name

		# Find the file in build
		build_bin = os.path.join(build_directory, file_name)

		# Find the destination in project root
		project_bin = os.path.join(project_directory, file_name)

		# Copy file
		shutil.copy(build_bin, project_bin)

# Queue action for after program build
env.AddPostAction("buildprog", copy_bin)