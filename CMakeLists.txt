### SETUP ###
cmake_minimum_required(VERSION 3.0)
set(CMAKE_CONFIGURATION_TYPES Debug Release)
project(CPPFramework)

# Activate C++11 standard
if(NOT MSVC)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")
endif(NOT MSVC)

# Code
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Link to executable
# target_link_libraries(${PROJECT_NAME} ${OPENGL_LIBRARIES} glfw)

# Filtering for Visual Studio
if(MSVC)

	foreach(f ${CODE})
		# Get the path of the file relative to ${CMAKE_CURRENT_SOURCE_DIR},
		# then alter it (not compulsory)
		file(RELATIVE_PATH SRCGR "${CMAKE_SOURCE_DIR}" ${f})
		set(SRCGR "${PROJECT_NAME}/${SRCGR}")

		# Extract the folder, i.e., remove the filename part
		string(REGEX REPLACE "(.*)(/[^/]*)$" "\\1" SRCGR ${SRCGR})

		# Source_group expects \\ (double antislash), not / (slash)
		string(REPLACE / \\ SRCGR ${SRCGR})
		source_group("${SRCGR}" FILES ${f})
	endforeach()

endif(MSVC)