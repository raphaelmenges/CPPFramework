cmake_minimum_required(VERSION 2.8)

# Name the project by folder
get_filename_component(TARGET_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" TARGET_NAME ${TARGET_NAME})

# Code
file(GLOB_RECURSE SOURCES *.cpp)
file(GLOB_RECURSE HEADER *.h)
file(GLOB_RECURSE LOCAL_CODE *.h *.cpp)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Combine local code with global code
set(CODE ${LOCAL_CODE} ${GLOBAL_CODE})

# Create executable
add_executable(${TARGET_NAME} ${CODE})

# Link to executable
target_link_libraries(${TARGET_NAME})

# Filtering for Visual Studio
if(MSVC)

	foreach(f ${LOCAL_CODE})
		
		# Relative path from folder to file
		file(RELATIVE_PATH SRCGR "${CMAKE_CURRENT_SOURCE_DIR}" ${f})
		set(SRCGR "src/${SRCGR}")
		
		# Extract the folder, i.e., remove the filename part
		string(REGEX REPLACE "(.*)(/[^/]*)$" "\\1" SRCGR ${SRCGR})

		# Source_group expects \\ (double antislash), not / (slash)
		string(REPLACE / \\ SRCGR ${SRCGR})
		source_group("${SRCGR}" FILES ${f})
		
	endforeach()

endif(MSVC)