import sys
import os
from mutagen.easyid3 import EasyID3

# First we import the data from before
os.chdir("/home/smoljam/Music/HoldingZone")

metadata = ['filenames','title','artist','album']
filenames = ['.filenames','.songnames', '.artistnames', '.albumnames']
arraynames = [name[1:] for name in filenames]

# Open files in filenames and save data to arraynames

for i in range(len(filenames)):
    try:
        file = open(filenames[i])
        arraynames[i] = file.read().splitlines()
    except:
        pass

# Write the data from the lists onto the files
for songnum in range(len(filenames)):
    audio = EasyID3(filenames[songnum])
    for i in range(len(filenames)):
        try:
            audio[metadata[i]]=arraynames[i][songnum]
        except:
            pass
    audio.save()
