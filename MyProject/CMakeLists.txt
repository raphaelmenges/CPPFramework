cmake_minimum_required(VERSION 2.8)

# TODO
# - for deploying, res_path must be relative to executables

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

# Set project name
project(CPPFramework_${CONFIG_LOWER_CASE})

# Set root directory of framework
set(FRAMEWORK_DIR "${CMAKE_SOURCE_DIR}/..")

# Activate C++11 standard
if(NOT MSVC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
endif(NOT MSVC)

# Paths
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake CACHE INTERNAL "Path to CMake modules.")
set(RES_PATH ${CMAKE_SOURCE_DIR}/res CACHE PATH "Path to resources.")
set(EXE_PATH ${CMAKE_SOURCE_DIR}/src/exe)
set(LIB_PATH ${CMAKE_SOURCE_DIR}/src/lib)

# Defines for C++ side
add_definitions(-DRES_PATH="${RES_PATH}")

# Outputs
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/exe CACHE PATH "Output path for executables.")
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib CACHE PATH "Output path for libraries.")

# Macros
include(${CMAKE_MODULE_PATH}/macros.cmake)

# Include path to own libraries folder
include_directories(${LIB_PATH})

# Global code (empty, as of now)
# set(GLOBAL_CODE)

# External libraries
set(EXTERNAL_LIBRARIES "")

# OpenCV
include_directories("${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install/include") # include dir
file(GLOB OPENCV_LIBS "${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install/x64/vc14/lib/*.lib") # linked libraries
set(EXTERNAL_LIBRARIES ${EXTERNAL_LIBRARIES} ${OPENCV_LIBS})

# Copy shared libraries to output folder of executable binaries
file(GLOB OPENCV_SHARED_LIBS "${FRAMEWORK_DIR}/_generated/${CONFIG_LOWER_CASE}/opencv/install/x64/vc14/bin/*.dll")
foreach(LIB ${OPENCV_SHARED_LIBS})

	# Get filename of shared lib
	get_filename_component(LIB_FILENAME ${LIB} NAME)
	
	# Workaround for MSVC, where binaries are stored in subfolder named after configuration
	if(MSVC)
		set(LIB_FILENAME ${CONFIG_LOWER_CASE}/${LIB_FILENAME})
	endif(MSVC)
	
	# Copy shared library to same folder as executable binaries
	configure_file(${LIB} ${EXECUTABLE_OUTPUT_PATH}/${LIB_FILENAME} COPYONLY)
endforeach()

# Libraries
set(INTERNAL_LIBRARIES "") # collect them to link later into executable
message(STATUS "# Search for libraries")
SUBDIRLIST(SUBDIRS ${LIB_PATH})
foreach(SUBDIR ${SUBDIRS})
    message(STATUS ${SUBDIR})
    add_subdirectory(${LIB_PATH}/${SUBDIR})
endforeach()
message(STATUS "# Done")

# Executables
message(STATUS "# Search for executables")
SUBDIRLIST(SUBDIRS ${EXE_PATH})
foreach(SUBDIR ${SUBDIRS})
    message(STATUS ${SUBDIR})
    add_subdirectory(${EXE_PATH}/${SUBDIR})
endforeach()
message(STATUS "# Done")