import os
import sys
import subprocess
import argparse

"""
Script to generate framework. Please execute this instead of manual CMake calls.

Remarks:
- 64bit, only
- TODO: switch to enable visual_debug (aka whether to build highlevel GUI module or not)
"""

# #########################
# ######## Defines ########
# #########################
DEBUG_SUBDIR = "/debug"
RELEASE_SUBDIR = "/release"
GENERATED_DIR = "./_generated"
GENERATED_OPEN_CV_SUBDIR = "/opencv"
GENERATED_BUILD_SUBDIR = "/build"
GENERATED_INSTALL_SUBDIR = "/install"
BUILD_DIR = "./_build"

# #########################
# ######## Classes ########
# #########################

# Available generators
class Generator:
	MSVC2015, MSVC2017, Make = range(3)
	def to_string(generator):
		if(generator == Generator.MSVC2015):
			return "Visual Studio 14 Win64"
		elif(generator == Generator.MSVC2017):
			return "Visual Studio 15 Win64"
		else:
			return "Unix Makefiles"

# Available configurations
class Configuration:
	Debug, Release = range(2)
	def to_string(config):
		if(config == Configuration.Debug):
			return "Debug"
		else:
			return "Release"
			
# ########################################
# ######## Command Line Arguments ########
# ########################################
			
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configuration", help="build configuration, either 'release' or 'debug'")
parser.add_argument("-g", "--generator", help="generator, either 'MSVC2015' or 'MSVC2017' on Windows or 'Make' on Linux")
args = parser.parse_args()

# #########################################
# ######## Platform Specific Setup ########
# #########################################

# Retrieve platform
cmake_exe = "cmake"
generator = Generator.Make
if sys.platform == "linux" or sys.platform == "linux2": # Linux
	
	# CMake exe path
	cmake_exe = "cmake"

    # Generator
	generator = Generator.Make # ignore command line argument, as there is only one generator supported
	
elif sys.platform == "win32": # Windows

	# CMake exe path
	cmake_exe = "C:/Program Files/CMake/bin/cmake.exe" # TODO: might fail for 32bit CMake on 64bit systems
    
	# Generator
	if args.generator:
		if(args.generator == "MSVC2015"):
			generator = Generator.MSVC2015
		elif(args.generator == "MSVC2017"):
			generator = Generator.MSVC2017
		else:
			generator = Generator.MSVC2015
			print("Provided generator unknown. Applying fallback to 'MSVC2015'.")
	else:
		generator = Generator.MSVC2015
		print("No generator provided. Applying fallback to 'MSVC2015'.")
		
# ###############################
# ######## Configuration ########
# ###############################

# Retrieve configuration
config = Configuration.Release
if args.configuration:
	if(args.configuration == "debug"):
		config = Configuration.Debug
	elif(args.configuration == "release"):
		config = Configuration.Release
	else:
		config = Configuration.Release
		print("Provided configuration unknown. Applying fallback to 'release'.")
else:
	config = Configuration.Release
	print("No configuration provided. Applying fallback to 'release'.")
		
# #############################
# ######## Directories ########
# #############################

# Function to create directory if not yet existing
def create_dir(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)

# Create directory structure for framework
config_subdir = ""
if config == Configuration.Debug: # debug configuration
	config_subdir = DEBUG_SUBDIR
else: # release configuration
	config_subdir = RELEASE_SUBDIR
	
# Top-level folders
create_dir(GENERATED_DIR)
create_dir(BUILD_DIR)

# Generated
create_dir(GENERATED_DIR + config_subdir)
create_dir(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR)
create_dir(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_BUILD_SUBDIR)
create_dir(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_INSTALL_SUBDIR)

# Own project
create_dir(BUILD_DIR + config_subdir)

# Generate absolute paths before going into directories to execute cmake
open_cv_build_dir = os.path.abspath(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_BUILD_SUBDIR)
open_cv_install_dir = os.path.abspath(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_INSTALL_SUBDIR)
build_dir = os.path.abspath(BUILD_DIR + config_subdir)

# ########################
# ######## OpenCV ########
# ########################

# Generate OpenCV project
os.chdir(open_cv_build_dir) # change into build directory of OpenCV
cmake_cmd = [
	cmake_exe, # cmake
	"-G", Generator.to_string(generator), # compiler
	"-Wno-dev", # supress CMake developer warnings
	"-D", "CMAKE_INSTALL_PREFIX=" + open_cv_install_dir, # set installation directory
	
	# ### OpenCV build setup ###
	
	# General TODO: incomplete. Probably more is built than necessary
	"-D", "BUILD_DOCS=OFF", # no documentation
	"-D", "BUILD_EXAMPLES=OFF", # no examples
	"-D", "BUILD_TESTS=OFF", # no tests
	"-D", "BUILD_PERF_TESTS=OFF",
	"-D", "BUILD_PACKAGE=OFF",
	"-D", "BUILD_SHARED_LIBS=ON", # build shared libs
	"-D", "BUILD_WITH_STATIC_CRT=OFF", # only for MSVC
	"-D", "BUILD_USE_SYMLINKS=OFF",
	"-D", "BUILD_WITH_DEBUG_INFO=OFF",
	"-D", "BUILD_WITH_DYNAMIC_IPP=OFF",
	"-D", "ENABLE_CXX11=ON",
	"-D", "ENABLE_PRECOMPILED_HEADERS=ON",
	"-D", "ENABLE_PYLINT=OFF",
	"-D", "ENABLE_SOLUTION_FOLDERS=OFF",
	"-D", "INSTALL_CREATE_DISTRIB=OFF",
	"-D", "INSTALL_C_EXAMPLES=OFF",
	"-D", "INSTALL_PYTHON_EXAMPLES=OFF",
	"-D", "INSTALL_TESTS=OFF",
	
	# Support
	"-D", "WITH_CUDA=OFF",
	"-D", "WITH_DIRECTX=OFF",
	"-D", "WITH_DSHOW=ON",
	"-D", "WITH_EIGEN=ON", # conversion functionality between OpenCV and EIGEN
	"-D", "WITH_FFMPEG=ON",
	"-D", "WITH_GSTREAMER=OFF",
	"-D", "WITH_JPEG=ON",
	"-D", "WITH_MATLAB=OFF",
	"-D", "WITH_LAPACK=OFF",
	"-D", "WITH_OPENCL=OFF",
	"-D", "WITH_OPENCLAMDBLAS=OFF",
	"-D", "WITH_OPENCLAMDFFT=OFF",
	"-D", "WITH_OPENCL_SVM=OFF",
	"-D", "WITH_OPENEXR=OFF",
	"-D", "WITH_OPENGL=OFF",
	"-D", "WITH_OPENMP=OFF",
	"-D", "WITH_OPENNI=OFF",
	"-D", "WITH_OPENNI2=OFF",
	"-D", "WITH_OPENVX=OFF",
	"-D", "WITH_PNG=ON",
	"-D", "WITH_PROTOBUF=OFF",
	"-D", "WITH_PVAPI=OFF",
	"-D", "WITH_QT=OFF",
	"-D", "WITH_TBB=OFF",
	"-D", "WITH_TIFF=OFF",
	"-D", "WITH_VFW=OFF",
	"-D", "WITH_VTK=OFF",
	"-D", "WITH_WEBP=OFF",
	"-D", "WITH_WIN32UI=ON", # TODO: deactivate this under linux or just let it be ignored? under linux, gtk3 would be required...
	"-D", "WITH_XIMEA=OFF",
	"-D", "mdi=OFF",
	"-D", "next=OFF",
	"-D", "old-jpeg=OFF",
	"-D", "opencv_dnn_PERF_CAFFE=OFF",
	"-D", "opencv_dnn_PERF_CLCAFFE=OFF",
	"-D", "packbits=OFF",
	"-D", "thunder=OFF",

	# Libraries
	"-D", "BUILD_JPEG=ON",
	"-D", "BUILD_OPENEXR=OFF",
	"-D", "BUILD_PNG=ON",
	"-D", "BUILD_PROTOBUF=OFF",
	"-D", "BUILD_TBB=OFF",
	"-D", "BUILD_TIFF=OFF",
	"-D", "BUILD_WEBP=OFF",
	"-D", "BUILD_ZLIB=ON",
	
	# Other
	"-D", "BUILD_CUDA_STUBS=OFF", # no CUDA stubs
	# "-D", "EIGEN_INCLUDE_PATH=" + "", # not required to set for EIGEN and OpenCV compatibility....
	
	# Modules
	"-D", "BUILD_opencv_apps=OFF",
	"-D", "BUILD_opencv_calib3d=OFF",
	"-D", "BUILD_opencv_core=ON",
	"-D", "BUILD_opencv_dnn=OFF",
	"-D", "BUILD_opencv_features2d=ON",
	"-D", "BUILD_opencv_flann=OFF",
	"-D", "BUILD_opencv_highgui=ON", # required for imshow (so rather 'debugging')
	"-D", "BUILD_opencv_imgcodecs=ON",
	"-D", "BUILD_opencv_imgproc=ON",
	"-D", "BUILD_opencv_ml=ON",
	"-D", "BUILD_opencv_objdetect=OFF",
	"-D", "BUILD_opencv_photo=ON",
	"-D", "BUILD_opencv_shape=OFF",
	"-D", "BUILD_opencv_stitching=OFF",
	"-D", "BUILD_opencv_superres=OFF",
	"-D", "BUILD_opencv_ts=OFF", # test module
	"-D", "BUILD_opencv_video=ON",
	"-D", "BUILD_opencv_videoio=ON",
	"-D", "BUILD_opencv_videostab=OFF",
	"-D", "BUILD_opencv_world=OFF",
	
	# Bindings
	"-D", "BUILD_JAVA=OFF", # no java support
	"-D", "BUILD_opencv_java_bindings_generator=OFF",
	"-D", "BUILD_opencv_python_bindings_generator=OFF",
	"-D", "BUILD_opencv_python3=OFF",
	"-D", "BUILD_opencv_js=OFF",
	"-D", "BUILD_opencv_js=OFF",
	
	# ##########################
	
	"../../../../third_party/opencv"] # source code directory
retCode = subprocess.check_call(cmake_cmd, stderr=subprocess.STDOUT, shell=False)

# Build and install OpenCV project
cmake_cmd = [
	cmake_exe, # cmake
	"--build", ".",
	"--config", Configuration.to_string(config),
	"--target", "install"]
retCode = subprocess.check_call(cmake_cmd, stderr=subprocess.STDOUT, shell=False)

# #########################
# ######## Project ########
# #########################

# Build own project
os.chdir(build_dir) # change into build directory of project
cmake_cmd = [
	cmake_exe, # cmake
	"-G", Generator.to_string(generator), # compiler
	"-D", "CONFIG=" + Configuration.to_string(config),
	"../../MyProject"] # source code directory
retCode = subprocess.check_call(cmake_cmd, stderr=subprocess.STDOUT, shell=False)