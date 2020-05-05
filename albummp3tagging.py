import sys
import os
from mutagen.easyid3 import EasyID3
from math import log10, ceil

#I know this is gonna be inefficient but it seems easy and not the bottleneck here
#I'm just gonna do a search for the video title in the video title to find the
#index I'm meant to use

# First we import the data from before

os.chdir("/home/smoljam/Music/HoldingZone")

file = open(".href", "r")
playlistIDs = file.read().splitlines()

file = open(".videonumbers", "r")
videonumbers = file.read().splitlines()

file = open(".albumnames", "r")
albumnames = file.read().splitlines()

artistname = sys.argv[1]

for playlistindex in range(len(playlistIDs)):
    length = len(str(videonumbers[playlistindex]))
    for videoindex in range(int(videonumbers[playlistindex])):
        number = (length-ceil(log10(videoindex+2)))*"0"+str(videoindex+1)
        try:
            audio = EasyID3(playlistIDs[playlistindex]+"["+number+"].mp3")
            audio['artist'] = artistname
            audio['album'] = albumnames[playlistindex]
            audio['tracknumber'] = str(int(videoindex)+1)
            audio.save()
            print(artistname,albumnames[playlistindex],videoindex+1)
        except:
            pass
