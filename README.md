# MP3 Player

MP3 Player for Microcontroller Programming - ENG1419 at Pontifical Catholic University of Rio de Janeiro


## What it is?

This is a .mp3 music player that will support a robot to dance and sing. 

## How it works?

This Player will help a robot play songs that are stored in the program. There will be some already stored for demonstration purposes (located in the "songs" folder), but if you prefer to add some of your own it is possible to do it too, however the format must be .mp3 obligatorily. 

To enable a specific song in the player, click "Add Songs" > "Add One Song" or "Add Many Songs" if you want to add multiple songs to the player. 
If you want to remove a specific song, just select it and go to the "Remove Songs" tab > "Delete a song from playlist" or "Delete all songs from playlist" if you want to delete all loaded songs

When playing a song, the central horizontal bar can be controlled to fast forward the song or rewind the song.

## Running The Project

- Clone this project in your C driver
- Run `pip install pygame` or `pip install pygame --pre`` in your bash / command line
- Run `pip install mutagen` in your bash / command line
- Run `pip install requests` in your bash / command line
- Run `player.py`

## Dependencies

- [Pygame](https://www.pygame.org/wiki/GettingStarted)
- [Mutagen](https://mutagen.io/documentation/introduction/installation)