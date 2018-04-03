cmake_minimum_required(VERSION 2.8)

# Name the project by folder
get_filename_component(TARGET_NAME ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" TARGET_NAME ${TARGET_NAME})

# Prefix target name with 't_'
set(TARGET_NAME t_${TARGET_NAME})

# Remember test in parent scope list
set(TESTS ${TESTS} ${TARGET_NAME} PARENT_SCOPE)

# Code
file(GLOB_RECURSE LOCAL_CODE *.h *.cpp)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Combine local code with global code
set(CODE ${LOCAL_CODE} ${GLOBAL_CODE})

# Create executable
add_executable(${TARGET_NAME} ${CODE})

# Linking
target_link_libraries(${TARGET_NAME} ${INTERNAL_LIBRARIES} ${EXTERNAL_LIBRARIES} ${TEST_LIBRARIES})

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