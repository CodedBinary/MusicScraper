import os
import sys

from scrapbase import *
from scrapwebs import *

# The goal of this program is to create a folder containing the first youtube
# search results for each song produced by an artist

verbosity = 3

# We put data in HoldingZone so other scripts can edit it without knowledge of the folder name
directory = "/home/smoljam/Music/HoldingZone"
os.chdir(directory)
if verbosity >= 1:
    print("Changing working directory to ", directory)

# Scrape wikipedia for a list of album names
artist = sys.argv[1]
albumlist = wikipediascraping(artist,verbosity)
filewrite([albumlist], [".albumnames"])

# Generate a list of queries to search on youtube
if verbosity >= 1:
    print("Generating list of queries...")
queries = [artist+" "+album+" full album" for album in albumlist]
if verbosity >= 2:
    print("Queries: ", queries)

# Ripping songs off youtube.
youtubedata = youtubescraping(queries,[],[],"playlist",verbosity)
filewrite([youtubedata[0],youtubedata[1],youtubedata[2],youtubedata[3]],[artist,".playlistnames",".href",".videonumbers"])
