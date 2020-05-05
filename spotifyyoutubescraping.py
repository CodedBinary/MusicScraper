import os
import sys
from selenium import webdriver
from scrapbase import *
from scrapwebs import *

# The goal of this program is to write the data about youtube videos that correspond to songs from a spotify album
verbosity = 3

# We put data in HoldingZone so other scripts can edit it without knowledge of the folder name
directory = "/home/smoljam/Music/HoldingZone"
os.chdir(directory)
if verbosity >= 1:
    print("Changing working directory to ", directory)

# Scrape spotify for the playlist name, song names, artist names, and album names
url = sys.argv[1]
spotifydata = spotifyscraping(url,verbosity)
filewrite([spotifydata[1],spotifydata[2],spotifydata[3]],[".songnames", ".artistnames", ".albumnames"])

# Generate a list of queries to search on youtube
if verbosity >= 1:
    print("Generating list of queries...")
queries = [spotifydata[1][songnumber]+" "+spotifydata[2][songnumber]+" lyric" for songnumber in range(len(spotifydata[2]))]
if verbosity >= 2:
    print("Queries: ", queries)

# Ripping the songs off youtube.
youtubedata = youtubescraping(queries,["lyric"],["live","cover"],"video",verbosity)
filewrite([youtubedata[0],youtubedata[1],youtubedata[2],[url]],[str(spotifydata[0]), ".videonames",".href",".playlisturl"])
