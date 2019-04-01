Import("env")

import os
import shutil

# Copy files
def copy_bin(target, source, env):
	build_bin = env['BUILD_DIR']
	project_bin = env['PROJECT_DIR']
	for source_file in source:
		file_name = source_file.name
		source = os.path.join(build_bin, file_name)
		shutil.copy(source, project_bin)

# Queue action for after program build
env.AddPostAction("buildprog", copy_bin)