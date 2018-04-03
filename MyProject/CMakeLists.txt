cmake_minimum_required(VERSION 2.8)
project(CPPFramework)

# Configuration
set(CONFIG "Debug" CACHE STRING "Build configuration (Debug / Release).")
set_property(CACHE CONFIG PROPERTY STRINGS Debug Release)
string(COMPARE EQUAL "${CONFIG}" "Debug" cmp)
if(cmp)
	set(CMAKE_CONFIGURATION_TYPES "Debug" CACHE INTERNAL "" FORCE)
else()
	set(CMAKE_CONFIGURATION_TYPES "Release" CACHE INTERNAL "" FORCE)
endif()
message(STATUS "Build Configuration='${CMAKE_CONFIGURATION_TYPES}'")
string(TOLOWER "${CMAKE_CONFIGURATION_TYPES}" CONFIG_LOWER_CASE)

# Set root directory of framework
set(FRAMEWORK_DIR "${CMAKE_SOURCE_DIR}/..")

# Activate C++11 standard
if(NOT MSVC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
endif(NOT MSVC)

# Paths
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake CACHE INTERNAL "Path to CMake modules.")
set(RES_PATH ${CMAKE_SOURCE_DIR}/res CACHE PATH "Path to resources.")

# Defines for C++ side
add_definitions(-DRES_PATH="${RES_PATH}")

# Outputs
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/exe CACHE PATH "Output path for executables.")
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib CACHE PATH "Output path for libraries.")

# Macros
include(${CMAKE_MODULE_PATH}/macros.cmake)

# Global code
set(GLOBAL_CODE ${UTIL})

# OpenCV
include_directories("${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install/include") # include dir
file(GLOB OPENCV_LIBS "${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install/x64/vc14/lib/*.lib") # linked libraries

# Copy shared libraries to output folder of executable binaries
file(GLOB OPENCV_SHARED_LIBS "${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install/x64/vc14/bin/*.dll")
foreach(LIB ${OPENCV_SHARED_LIBS})

	# Get filename of shared lib
	get_filename_component(LIB_FILENAME ${LIB} NAME)
	
	# Workaround for MCVC, where binaries are stored in subfolder named after configuration
	if(MSVC)
		set(LIB_FILENAME ${CONFIG_LOWER_CASE}/${LIB_FILENAME})
	endif(MSVC)
	
	# Copy shared library to same folder as executable binaries
	configure_file(${LIB} ${EXECUTABLE_OUTPUT_PATH}/${LIB_FILENAME} COPYONLY)
endforeach()

# Projects
SUBDIRLIST(SUBDIRS ${CMAKE_SOURCE_DIR}/src/exe)
foreach(SUBDIR ${SUBDIRS})
    message(STATUS ${SUBDIR})
    add_subdirectory(${CMAKE_SOURCE_DIR}/src/exe/${SUBDIR})
endforeach()