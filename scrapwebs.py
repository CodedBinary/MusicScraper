import requests
from bs4 import BeautifulSoup
from scrapbase import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def youtubescraping(yts_queries,yts_require,yts_disallow,yts_type,yts_verbosity):
    '''A function (yts) to return the first playlist og a query containing a substring

    Desc: This function will search youtube by appending strings to a base url
    and scraping using the requests package, avoiding using a driver. It will
    then take the first video with a certain string in it

    Args:
        yts_queries         (list)  : A list of queries to search
        yts_require         (list)  : List of required strings to be in video title
        yts_disallow        (list)  : List of non allowed strings to be in video title
        yts_type            (str)   : Whether youtube should be searched for a "playlist" or a "video"
        yts_verbosity       (int)   : The level of verbosity to be used with print statements

    Out:
        yts_urllist         (list)  : A list of urls of the videos
        yts_videolist       (list)  : A list of video titles
        yts_IDlist          (list)  : A list of the video IDs
        yts_videonumlist    (list)  : A list of the number of videos. Is blank if yts_type="video"
    '''
    if yts_verbosity >= 1:
        print("Scraping the song data from youtube...")

    yts_urllist      = []
    yts_videolist    = []
    yts_IDlist       = []
    yts_videonumlist = []
    yts_preurls      = []
    # For progressbar only:
    i=0
    for query in yts_queries:
        # Turning search query into a url.
        query = query.replace(" ","+")
        if yts_type == "video":
            yts_filter = "&sp=EgIQAQ%253D%253D"
        elif yts_type == "playlist":
            yts_filter = "&sp=EgIQAw%253D%253D"

        url = "https://www.youtube.com/results?search_query="+query+yts_filter

        if yts_verbosity >= 3:
            print("(",i+1,"/",len(yts_queries),") Searching for: ", query)
            print("(",i+1,"/",len(yts_queries),") Navigating to: ", url)

        # Scraping web page for data (remember the page is not the one a browser sees)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        yts_videodata = soup.find_all('a', class_="yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link")
        yts_prevideonames = [yts_videodata[video].get('title') for video in range(len(yts_videodata))]
        yts_prehrefs = [yts_videodata[video].get('href') for video in range(len(yts_videodata))]
        if yts_type == "playlist":
            # We want to take only the playlist, coming after the ;. We also want it to be a full link
            yts_prehrefs = [string[string.find("list"):] for string in yts_prehrefs]

        #Search for first playlist name containing yts_require in yts_prevideonames
        correctvideo = searchthrough(yts_prevideonames,yts_require,yts_disallow)
        print(correctvideo, len(yts_prevideonames))

        if yts_type == "video":
            yts_urllist += ["https://www.youtube.com" + yts_prehrefs[correctvideo]]
        elif yts_type == "playlist":
            # Gives the number of videos as a string like "10 videos", then extracts the 10 and appends it to an array
            yts_totalvideos = soup.find_all('span', class_="formatted-video-count-label")[correctvideo].get_text()
            yts_totalvideos = yts_totalvideos[0:yts_totalvideos.find(" ")]
            yts_videonumlist += [yts_totalvideos]

            yts_urllist  += ["https://www.youtube.com/playlist?" + yts_prehrefs[correctvideo]]

        yts_videolist += [yts_prevideonames[correctvideo]]
        yts_IDlist += [yts_prehrefs[correctvideo][5:]]

        # For progress bar only:
        i += 1

    #Print outputs
    if yts_verbosity >= 2:
        print("Urls:", yts_urllist)
        print("Videos: ", yts_videolist)
        print("Video IDs:", yts_IDlist)
        print("Video Counts:", yts_videonumlist)

    return [yts_urllist, yts_videolist, yts_IDlist, yts_videonumlist]

def spotifyscraping(spotsc_url,spotsc_verbosity):
    ''' A function (spotsc) to scrape data from spotify playlists

    Desc: This uses an automated web browser with selenium
    to scrape the information from a spotify playlist. It requires the driver
    already be started, and does not close it after use.

    Args:
        spotsc_url       (str)   : The url of the spotify playlist
        spotsc_verbosity (int)   : The level of spotsc_verbosity to be used with print statements
    Out:
        spotsc_playlistname    (str)   : The name of the spotify playlist
        spotsc_songnames       (list)  : A list of the song names, in the playlist's order
        spotsc_artistnames     (list)  : A list of the artist names, in the playlist's order, including duplicates
        spotsc_albumnames      (list)  : A list of the album names, in the playlist's order, including duplicates
    '''
    # Access and prepare website for scraping

    # Opening a chrome driver with selenium
    if spotsc_verbosity >= 1:
        print("Scraping spotify for data...")
        print("Opening web driver...")
    driver = webdriver.Chrome()

    driver.get(spotsc_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # We need the number of songs to know when to stop scrolling down
    numberofsongs = soup.find('p', class_="TrackListHeader__text-silence TrackListHeader__entity-additional-info").get_text()[:-6]
    body = driver.find_element_by_css_selector('body')
    body.click()

    loadedsongs = len(soup.find_all('div', class_="tracklist-name ellipsis-one-line")) 
    while loadedsongs < int(numberofsongs):
        body.send_keys(Keys.END)
        print(loadedsongs, " < ", numberofsongs)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        loadedsongs = len(soup.find_all('div', class_="tracklist-name ellipsis-one-line"))


    # Search for the title of the album
    spotsc_playlistname = soup.find('div', class_="mo-info-name").get("title")
    if spotsc_verbosity >= 2:
        print("Playlist name: ", spotsc_playlistname)

    # Searching for the list of songs
    presongnames = soup.find_all('div', class_="tracklist-name ellipsis-one-line")
    spotsc_songnames = [song.get_text() for song in presongnames]
    if spotsc_verbosity >= 2:
        print("Song names: ",spotsc_songnames)

    # Searching for the list of artists
    preartistnames = soup.find_all('span', class_="TrackListRow__artists ellipsis-one-line")
    spotsc_artistnames = [crap.find('span').get_text() for crap in preartistnames]
    if spotsc_verbosity >= 2:
        print("Artist names: ",spotsc_artistnames)

    # Searching for the list of albums
    prealbumnames = soup.find_all('a', class_="tracklist-row__album-name-link")
    spotsc_albumnames = [album.get_text() for album in prealbumnames]
    if spotsc_verbosity >= 2:
        print("Album names:",spotsc_albumnames)

    if spotsc_verbosity >= 1:
        print("Writing spotify data...")
    driver.quit()
    return [spotsc_playlistname,spotsc_songnames,spotsc_artistnames,spotsc_albumnames]

def wikipediascraping(wks_artist,wks_verbosity):
    '''Returns a list of albums released by an wks_artist according to wikipedia

    Desc: Searches duckduckgo for the wks_artist name + "band" with a web driver,
    then accesses the wikipedia page for it and scraped it for the list of
    albums under discography.

    Args:
        wks_artist      (str)   : The name of the artist whose albums should be retrieved
        wks_verbosity   (int)   : The level of verbosity to be used with print statements

    Out:
        albumlist       (list)  : A list of albums produced by the artist
    '''
    # Prepare to search duckduckgo. A webdriver is used here because duckduckgo
    # just throws errors when requests gets the page
    url = "https://duckduckgo.com/html/?q=" + wks_artist.replace(" ","+") + "+band"
    if wks_verbosity >= 2:
        print("Navigating to: ", url)
    driver = webdriver.Chrome()
    page = driver.get(url)

    # Search and Scrape duckduckgo
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    preresults = soup.find_all(class_="result__a")
    results = [url.get("href") for url in preresults]
    if wks_verbosity >= 3:
        print("Search results: ", results)

    url = results[searchthrough(results,"en.wikipedia.org",[])]
    if wks_verbosity >= 2:
        print("Navigating to: ", url)
    driver.close()

    # Search Wikipedia. We can't search wikipedia directly because some
    # bands like Anthrax need to have "band" appended, but some like Megadeth won't
    # work if you do that.
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    prealbumlist = soup.find(id="Discography").parent.find_next('ul').find_all('i')
    # The information is stored as text inside a <ul><li><i> coming soon after Discography
    albumlist = [album.text for album in prealbumlist]
    if wks_verbosity >= 2:
        print("Album list: ", albumlist)

    if wks_verbosity >= 1:
        print("Writing album name list...")

    return albumlist
