import os
import sys
import subprocess
import argparse

# 64bit, only
# TODO: decide generator (vs 2015/2017 on windows, gcc? on linux) as argument

# Defines
DEBUG_SUBDIR = "/debug"
RELEASE_SUBDIR = "/release"
GENERATED_DIR = "./_generated"
GENERATED_OPEN_CV_SUBDIR = "/opencv"
GENERATED_BUILD_SUBDIR = "/build"
GENERATED_INSTALL_SUBDIR = "/install"
BUILD_DIR = "./build"

# Available configurations
class Configuration:
	Debug, Release = range(2)
	def to_string(config):
		if(config == Configuration.Debug):
			return "Debug"
		else:
			return "Release"
			
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configuration", help="build configuration, either 'release' or 'debug'")
args = parser.parse_args()

# Apply command line arguments
config = Configuration.Release
if args.configuration:
	if(args.configuration == "debug"):
		config = Configuration.Debug
	elif(args.configuration == "release"):
		config = Configuration.Release
	else:
		print("Provided configuration unkown. Applying fallback to 'release'.")

# Function to create folder if not yet existing
def create_folder(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

# Create folder structure for framework
config_subdir = ""
if config == Configuration.Debug: # debug configuration
	config_subdir = DEBUG_SUBDIR
else: # release configuration
	config_subdir = RELEASE_SUBDIR
create_folder(GENERATED_DIR)
create_folder(BUILD_DIR)

# Generated
create_folder(GENERATED_DIR + config_subdir)
create_folder(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR)
create_folder(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_BUILD_SUBDIR)
create_folder(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_INSTALL_SUBDIR)

# Own project
create_folder(BUILD_DIR + config_subdir)

# Generate absolute paths before going into folders to execute cmake
open_cv_build_dir = os.path.abspath(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_BUILD_SUBDIR)
open_cv_install_dir = os.path.abspath(GENERATED_DIR + config_subdir + GENERATED_OPEN_CV_SUBDIR + GENERATED_INSTALL_SUBDIR)
project_build_dir = os.path.abspath(BUILD_DIR + config_subdir)

# Generate OpenCV project
os.chdir(open_cv_build_dir) # change into build folder of OpenCV
cmakeCmd = [
	"cmake.exe", # cmake
	"-G", "Visual Studio 14 Win64", # compiler
	"-Wno-dev", # supress CMake developer warnings
	"-D", "CMAKE_INSTALL_PREFIX=" + open_cv_install_dir, # set installation folder
	
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
	"-D", "WITH_EIGEN=ON",
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
	"-D", "BUILD_opencv_python_bindings_generator=OFF", # no python bindings
	"-D", "BUILD_opencv_python3=OFF",
	"-D", "BUILD_opencv_js=OFF",
	"-D", "BUILD_opencv_js=OFF",
	
	# ##########################
	
	"../../../../third_party/opencv"] # source code folder
retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=False)

# Build and install OpenCV project
cmakeCmd = [
	"cmake.exe", # cmake
	"--build", ".",
	"--config", Configuration.to_string(config),
	"--target", "install"]
retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=False)

# Build own project
os.chdir(project_build_dir) # change into build folder of project
cmakeCmd = [
	"cmake.exe", # cmake
	"-G", "Visual Studio 14 Win64", # compiler
	"-D", "CONFIG=" + Configuration.to_string(config),
	"../../MyProject"] # source code folder
retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=False)