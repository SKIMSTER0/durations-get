import os
import sys
import math
import argparse
from decimal import Decimal
from array import *
from pymediainfo import MediaInfo
from pathlib import Path

#add up total time of all media files recursively in 'durations.txt' file
#requires pymediainfo wrapper installed through pip
#requires python3.4> for pathlib

parser = argparse.ArgumentParser(description='Recursively find total duration of audio files in folder')

parser.add_argument('startDir', default='./',  help="Starting directory to search from, default is current directory")

parser.add_argument('-f', '--inputFile', required=False, metavar='', dest='inputFile', help="Obtain media filepaths from File")

parser.add_argument('-o', '--outputFile', required=False, metavar='', dest='outputFile', help="Write mediainfo to file")

#parser.add_argument('-x', '--excludedExt', required=False, metavar='', dest='excludedExt', nargs='+', help="Choose excluded media extensions")

#parser.add_argument('-i', '--includeExt', required=False, metavar='', dest='includedExt', nargs='+', help="Choose included media extensions")

#parser.add_argument('-v', required=False, default=False, action="store_true", help="Output verbosely")

args = parser.parse_args()

audioExt = [
  '.aif',
  '.cda',
  '.mid',
  '.midi',
  '.mp3',
  '.mpa',
  '.ogg',
  '.wav'
  '.wma',
  '.wpl'
]

videoExt = [
  '.3g2',
  '.3gp',
  '.avi',
  '.flv',
  '.h264',
  '.m4v',
  '.mkv',
  '.mov',
  '.mp4',
  '.mpg',
  '.mpeg',
  '.rm',
  '.swf',
  '.vob',
  '.wmv'
]

def main():
  mediaDurations = searchMedia(args.startDir)
  totalMilli = getTotalDuration(mediaDurations)

  if (args.outputFile is not None):
    outputFileOpt(args.outputFile, mediaDurations)

  totalMin = totalMilli/60000
  totalSec = (Decimal(totalMin) % 1) * 100

  print("Total duration time of media files in ", args.startDir)
  print("min: " + str(math.floor(totalMin)))
  print("sec: " + str(math.floor(totalSec)))

#recursively search for media files to find their durations
def searchMedia(startDir):
  mediaDurations = {}

  for root, subdirs, files in os.walk(startDir):
    for filename in files:
      filepath = os.path.join(root, filename)

      if (Path(filepath).suffix in audioExt, videoExt):
        mediainfo = MediaInfo.parse(filepath)

        #extract duration from each media track/stream
        #does not account for multiple audio tracks
        for track in mediainfo.tracks:
          if (track.track_type == 'Audio'):
            #mediasize = track._data()["file_size"]
            mediaDurations[filepath] = track.duration
            break

  return mediaDurations

def getTotalDuration(mediaDurations):
  totalMilli = 0
  for media in mediaDurations:
    totalMilli += mediaDurations[media]

  return totalMilli

#write CSV filename/duration to output file, duration in milliseconds
def outputFileOpt(outputFile, mediaDurations):
    try:
      with open(outputFile, "w+") as f:
          for filename in mediaDurations:
            f.write(filename + "," + str(mediaDurations[filename]))
    except IOError as io:
      print("Could not write durations to file: " + str(io))

def inputFileOpt(inputFile, mediaDurations):
  return None

if __name__ ==  "__main__":
  main()

