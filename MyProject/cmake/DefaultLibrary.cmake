cmake_minimum_required(VERSION 2.8)

# Name the project by folder
get_filename_component(TARGET_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" TARGET_NAME ${TARGET_NAME})

# Remember library in parent scope list
set(INTERNAL_LIBRARIES ${INTERNAL_LIBRARIES} ${TARGET_NAME} PARENT_SCOPE)

# Code
file(GLOB_RECURSE LOCAL_CODE *.h *.cpp)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Combine local code with global code
set(CODE ${LOCAL_CODE} ${GLOBAL_CODE})

# Create library
add_library(${TARGET_NAME} STATIC ${CODE} )

# Set label of project
set_property(TARGET ${TARGET_NAME} PROPERTY PROJECT_LABEL lib_${TARGET_NAME})

# Linking (link only to external libraries and not among each other)
target_link_libraries(${TARGET_NAME} ${EXTERNAL_LIBRARIES})

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