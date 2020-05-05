import os
from selenium import webdriver
from scrapbase import *
from scrapwebs import *

def spotifyyoutubescraping(url):
    ''' Scrapes a spotify playlist for the list of songs

    Args:
        url     (str)   : The url of a spotify playlist

    Return:
        Does not return a value

    Write:
        <playlistname>  : The name of the spotify playlist
        .playlisturl    : The url of the spotify playlist
        .songnames      : The names of the songs on the playlist
        .artistnames    : The artist corresponding to each song in .songnames
        .albumnames     : The album corresponding to each song in .songnames
        .videonames     : The list of names of the youtube videos corresponding to each song in .songnames
        .href           : The list of urls of the youtube songs corresponding to each song in .songnames

    '''
    # The goal of this program is to write the data about youtube videos that correspond to songs from a spotify album
    verbosity = 3

    # We put data in HoldingZone so other scripts can edit it without knowledge of the folder name
    directory = "/home/smoljam/Music/HoldingZone"
    os.chdir(directory)
    if verbosity >= 1:
        print("Changing working directory to ", directory)

    # Scrape spotify for the playlist name, song names, artist names, and album names
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
    filewrite([youtubedata[0],youtubedata[1],youtubedata[2],[url]] , [str(spotifydata[0]), ".videonames",".href",".playlisturl"])


def wikipediascraping(artist):
    """ Returns a list of album names and links to youtube playlists of the albums

    Args: 
        artist  (str)   : The artist's name

    Return:
        

    Write:
        .albumnames     : the names of the artists albums
        <artistname>    : the name of the artist
        .playlistnames  : the names of the youtube playlists
        .href           : the url corresponding to the youtube playlists in .playlistnames
        .videonumbers   : the number of videos on each playlist in .playlistnames
    """
    verbosity = 3

    # We put data in HoldingZone so other scripts can edit it without knowledge of the folder name
    directory = "/home/smoljam/Music/HoldingZone"
    os.chdir(directory)
    if verbosity >= 1:
        print("Changing working directory to ", directory)

    # Scrape wikipedia for a list of album names
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
