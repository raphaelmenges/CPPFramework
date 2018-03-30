import os
import sys
import subprocess

# Defines
THIRD_PARTY_BUILD = os.path.abspath("./build_third_party")
THIRD_PARTY_INSTALL = os.path.abspath("./install_third_party")
BUILD_DIR = os.path.abspath("./build")

# Create third party build and install folder
if not os.path.exists(THIRD_PARTY_BUILD):
    os.makedirs(THIRD_PARTY_BUILD)
if not os.path.exists(THIRD_PARTY_INSTALL):
    os.makedirs(THIRD_PARTY_INSTALL)
		
# Create build folder
if not os.path.exists(BUILD_DIR):
    os.makedirs(BUILD_DIR)

# Generate OpenCV project in third party build folder
os.chdir(THIRD_PARTY_BUILD) # change into build folder for third party projects
cmakeCmd = [
	"cmake.exe", # cmake
	"-G", "Visual Studio 14 Win64", # compiler
	"-Wno-dev", # supress developer warnings
	"-D", "CMAKE_INSTALL_PREFIX=" + THIRD_PARTY_INSTALL, # set installation folder
	"-D", "BUILD_TESTS=OFF",
	"-D", "BUILD_opencv_python_bindings_generator=OFF",
	"../ThirdParty/opencv"] # source code folder
retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=False)

# Build OpenCV project in third party build folder
cmakeCmd = [
	"cmake.exe", # cmake
	"--build", ".",
	"--config", "Debug",
	"--target", "install"]
retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=False)

# Build own project