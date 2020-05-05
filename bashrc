musicdirectory="/home/macjam/Music"
programdirectory="/home/macjam/Programs"
musicscrapedirectory="/home/macjam/Programs/py/NewScrap/Scraping"

mus()
{
	WD="$(pwd)"
	cd $musicdirectory/!!!Downloaded;
	youtube-dl -o "$1.mp3" -x --audio-format mp3 $2
	cd $WD
}

musa()
{
	WD="$(pwd)"
	cd $musicdirectory/!!!Downloaded;
	youtube-dl -o "%(title)s.%(ext)s" -x --audio-format mp3 $1
	cd $WD
}

musp()
{
	WD="$(pwd)"
	youtube-dl -o "%(title)s.%(ext)s" -x --audio-format mp3 $1
	cd $musicdirectory/!!!Downloaded;
	youtube-dl --geo-bypass --yes-playlist -x --audio-format mp3 -o "%(title)s.%(ext)s" $1
	cd $WD
}

spoti()
{
	WD="$(pwd)"
	python $musicscrapedirectory/spotifyyoutubescraping.py $1  # THIS LINE IS BROKEN, IT NEEDS TO CALL main.py and then the function spotofyyoutubescraping with arg $1
	cd $musicdirectory/HoldingZone
	PLAYLISTNAME="$(ls)"
	echo $PLAYLISTNAME
	youtube-dl --geo-bypass --max-filesize 20M -i -x --audio-format mp3 -o "%(autonumber)s.%(ext)s" -a "$PLAYLISTNAME"
	#youtube-dl --geo-bypass -x --audio-format mp3 -o "%(id)s.%(ext)s" -a "$PLAYLISTNAME"
	python $musicscrapedirectory/mp3tagging.py
	mkdir $musicdirectory/"$PLAYLISTNAME"
	mv {*,.*} $musicdirectory/"$PLAYLISTNAME"
	cd $WD
}

artist()
{
	WD="$(pwd)"
	python $musicscrapedirectory/wikipediayoutubescraping.py "$1"  # THIS LINE IS BROKEN, IT NEEDS TO CALL main.py and then the function wikipediayoutubescraping with arg $1
	cd ~/Music/HoldingZone
	ARTISTNAME="$(ls)"
