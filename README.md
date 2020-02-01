# get-duration
Recursively find total duration of all media files in directory

## dependencies

Requires Python3.7+
pip3 install pymediainfo
pip3 install mediainfo

## usage
durations.py [-h] [-f] [-o] startDir

positional arguments:
  startDir - starting directory to search from, default is '.' current dir
 
 optional arguments:
  -o, --outputFile  write CSV (media filepath, duration) to File
  -h, --help        show this message and exit

## todo
  -f, --inputFile   obtain mediafilepaths from File
  include/exclude media extensions
 
  
