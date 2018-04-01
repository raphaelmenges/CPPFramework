# Setup
cmake_minimum_required(VERSION 2.8)
set(CMAKE_CONFIGURATION_TYPES Debug Release)
project(CPPFramework)

# Activate C++11 standard
if(NOT MSVC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
endif(NOT MSVC)

# Paths
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake CACHE INTERNAL "Project specific path. Set manually if it was not found.")

# Outputs
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/exe CACHE PATH "Output path for executables.")
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib CACHE PATH "Output path for libraries.")

# Macros
include(${CMAKE_MODULE_PATH}/macros.cmake)

# Utilities
set(UTIL_PATH ${CMAKE_SOURCE_DIR}/src/util)
file(GLOB_RECURSE UTIL ${UTIL_PATH}/*.h ${UTIL_PATH}/*.cpp)
# TODO: include util path?

# Global code
set(GLOBAL_CODE ${UTIL})

# Projects
SUBDIRLIST(SUBDIRS ${CMAKE_SOURCE_DIR}/src/exe)
foreach(SUBDIR ${SUBDIRS})
    message(STATUS ${SUBDIR})
    add_subdirectory(${CMAKE_SOURCE_DIR}/src/exe/${SUBDIR})
endforeach()