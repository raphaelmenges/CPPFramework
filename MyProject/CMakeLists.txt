cmake_minimum_required(VERSION 2.8)

# Override install macro to prohibit any installation
macro(install)
endmacro()

# TODO
# - For deploying, res_path must be relative to executables

# Preprocessor commands
add_definitions(-DEIGEN_MPL2_ONLY) # include no LGPL code from EIGEN

# Configuration
set(CONFIG "Debug" CACHE STRING "Build configuration (Debug / Release).")
set_property(CACHE CONFIG PROPERTY STRINGS Debug Release) # valus config can be assigned
string(COMPARE EQUAL "${CONFIG}" "Debug" cmp)
if(cmp)
	set(CMAKE_CONFIGURATION_TYPES "Debug" CACHE INTERNAL "" FORCE)
else()
	set(CMAKE_CONFIGURATION_TYPES "Release" CACHE INTERNAL "" FORCE) # fallback
endif()
message(STATUS "Build Configuration = '${CMAKE_CONFIGURATION_TYPES}'")
string(TOLOWER "${CMAKE_CONFIGURATION_TYPES}" CONFIG_LOWER_CASE)

# Set project name
project(CPPFramework_${CONFIG_LOWER_CASE})

# Set root directory of framework
set(FRAMEWORK_DIR "${CMAKE_SOURCE_DIR}/..")

# Activate C++11 standard
if(NOT MSVC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
endif(NOT MSVC)

# Visual debugging (whether GUI through OpenCV is available or not)
set(VISUAL_DEBUG "Visual Debug" CACHE BOOL "Whether GUI through OpenCV is used (ON) or not (OFF).")

# Paths
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
set(EXT_PATH ${CMAKE_SOURCE_DIR}/ext)
set(RES_PATH ${CMAKE_SOURCE_DIR}/res)
set(EXE_PATH ${CMAKE_SOURCE_DIR}/src/exe)
set(LIB_PATH ${CMAKE_SOURCE_DIR}/src/lib)
set(TEST_PATH ${CMAKE_SOURCE_DIR}/src/test)

# Defines for C++ side
if(${VISUAL_DEBUG})
	add_definitions(-DVISUAL_DEBUG)
endif()
add_definitions(-DRES_PATH="${RES_PATH}")

# Outputs
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/exe)
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)

# Macros
include(${CMAKE_MODULE_PATH}/macros.cmake)

# Include path to internal libraries folder
include_directories(${LIB_PATH})

# Global code (empty, as of now)
# set(GLOBAL_CODE)

# External libraries
set(EXTERNAL_LIBRARIES "")

# Final libraries, linked in the end
set(FINAL_LIBRARIES "")

# OpenCV
set(OPEN_CV_PATH ${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install)
include_directories(${OPEN_CV_PATH}/include) # include dir

# Find static OpenCV libraries
if(MSVC)
	file(GLOB OPENCV_LIBS ${OPEN_CV_PATH}/x64/vc*/staticlib/*.lib) # assumes that only one Visual Studio version was used to build libraries
else() # probably GCC

	# GCC requires certain order at linking. Remember to add further OpenCV modules here
	set(OPENCV_LIBS "")
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_core.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_imgcodecs.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_imgproc.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_videoio.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_highgui.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_video.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_photo.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_ml.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_features2d.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_features2d.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/share/OpenCV/3rdparty/lib/libippicv.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/share/OpenCV/3rdparty/lib/libippiw.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/share/OpenCV/3rdparty/lib/libittnotify.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/share/OpenCV/3rdparty/lib/liblibjpeg.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/share/OpenCV/3rdparty/lib/liblibpng.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/share/OpenCV/3rdparty/lib/libzlib.a)
	list(APPEND OPENCV_LIBS ${OPEN_CV_PATH}/lib/libopencv_core.a)
	
	# GTK2
	if(${VISUAL_DEBUG})
		find_package(PkgConfig REQUIRED)
		pkg_check_modules(GTK REQUIRED gtk+-2.0)
		list(APPEND FINAL_LIBRARIES ${GTK_LIBRARIES})
	endif()

	# Some libraries required by OpenCV
	list(APPEND FINAL_LIBRARIES pthread)
	list(APPEND FINAL_LIBRARIES dl)
	
endif()
set(EXTERNAL_LIBRARIES ${EXTERNAL_LIBRARIES} ${OPENCV_LIBS}) # collect libraries to link into

# EIGEN
set(EIGEN_PATH ${EXT_PATH}/eigen-git-mirror)
include_directories(${EIGEN_PATH})

# Libraries
set(INTERNAL_LIBRARIES "") # collect libraries to link later into executable
message(STATUS "Collecting Libraries")
SUBDIRLIST(SUBDIRS ${LIB_PATH})
foreach(SUBDIR ${SUBDIRS})
    message(STATUS "- ${SUBDIR}")
    add_subdirectory(${LIB_PATH}/${SUBDIR})
endforeach()

# Executables
message(STATUS "Collecting Executables")
SUBDIRLIST(SUBDIRS ${EXE_PATH})
foreach(SUBDIR ${SUBDIRS})
    message(STATUS "- ${SUBDIR}")
    add_subdirectory(${EXE_PATH}/${SUBDIR})
endforeach()

# Google Test
set(GTEST_PATH ${EXT_PATH}/googletest)
set(BUILD_GMOCK ON CACHE INTERNAL "")
set(BUILD_GTEST OFF CACHE INTERNAL "")
set(BUILD_SHARED_LIBS OFF CACHE INTERNAL "")
set(gmock_build_tests OFF CACHE INTERNAL "")
set(gtest_build_samples OFF CACHE INTERNAL "")
set(gtest_build_tests OFF CACHE INTERNAL "")
set(gtest_disable_pthreads OFF CACHE INTERNAL "")
set(gtest_force_shared_crt ON CACHE INTERNAL "")
set(gtest_hide_internal_symbols ON CACHE INTERNAL "")
add_subdirectory(${GTEST_PATH})
set(INSTALL_GMOCK OFF CACHE INTERNAL "" FORCE) # must be called after add_subdirectory with force (as not set with 'set' but with other function)
set(INSTALL_GTEST OFF CACHE INTERNAL "" FORCE) # must be called after add_subdirectory with force (as not set with 'set' but with other function)
include_directories(${GTEST_PATH}/googlemock/include)
include_directories(${GTEST_PATH}/googletest/include)
set(TEST_LIBRARIES gmock_main gtest_main) # use the versions that provide main function

# Tests
set(TESTS "") # collect tests
message(STATUS "Collecting Tests")
SUBDIRLIST(SUBDIRS ${TEST_PATH})
foreach(SUBDIR ${SUBDIRS})
    message(STATUS "- ${SUBDIR}")
    add_subdirectory(${TEST_PATH}/${SUBDIR})
endforeach()

# CTest
enable_testing()
foreach(TEST ${TESTS})

	# Accumulate path to tests
	set(TEST_PATH ${EXECUTABLE_OUTPUT_PATH})
	
	# Workaround for MSVC, where binaries are stored in subfolder named after configuration
	if(MSVC)
		set(TEST_PATH ${TEST_PATH}/${CONFIG_LOWER_CASE})
	endif(MSVC)

	# Add test
    add_test(GeneralTest ${TEST_PATH}/${TEST})
	
endforeach()