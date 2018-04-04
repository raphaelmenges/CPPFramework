# CPPFramework
Generic C++ framework for my own purposes.

## Requirements
Generation and compiling have been tested on Windows 10 with Visual Studio 2015 and Debian 8.8 with the software listed below.

### Windows
Install the following software:
- *Git*
- *Python 3*
- *cmake 2.8* or higher
- *Visual Studio 2015* or *2017*

### Debian 8.8 (similar on Ubuntu)
Install the following packages through the packet manager:
- *git*
- *build-essential*
- *cmake*
- optional: *libgtk2.0-dev* or *libgtk3.0-dev* (for visual debug)

## Procedure
Open _cmd_/_terminal_ in the directory where the project should be placed and execute the following commands:
```sh
git clone --recursive https://github.com/raphaelmenges/CPPFramework.git
cd CPPFramework
python .
```
This assumes Python 3 to be the standard Python environment on your system. There are arguments available for the Python call:
* `-c` (`--configuration`): build configuration, either 'release' or 'debug'
* `-g` (`--generator`): generator, either 'MSVC2015' or 'MSVC2017' on Windows or 'Make' on Linux

## TODO
- Decide on highgui module / win32ui / gtk: visual_debug flag?
- Machine Learning Library?
