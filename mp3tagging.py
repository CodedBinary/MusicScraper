import sys
import os
from mutagen.easyid3 import EasyID3

#I know this is gonna be inefficient but it seems easy and not the bottleneck here
#I'm just gonna do a search for the video title in the video title to find the
#index I'm meant to use

# First we import the data from before
#os.chdir("/home/smoljam/Music/"+sys.argv[1])
os.chdir("/home/smoljam/Music/HoldingZone")

metadata = ['title','artist','album']
filenames = ['.songnames', '.artistnames', '.albumnames']
arraynames = [name[1:] for name in filenames]
iterator = range(len(filenames))

# Open files in filenames and save data to arraynames
for i in iterator:
    try:
        file = open(filenames[i])
        arraynames[i] = file.read().splitlines()
    except:
        pass

# Write the data from the lists onto the files
for filenumber in range(len(arraynames[0])):
    filenumber=filenumber+1
    audio = EasyID3(f"{filenumber:05d}.mp3")
    audio['tracknumber']=int(filenumber)
    for datatype in iterator:
        try:
            audio[metadata[datatype]]=arraynames[datatype][filenumber-1]
        except
            pass
    audio.save()
