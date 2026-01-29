###########################################################
# Importing & Initializing
###########################################################

from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import random
import requests
import json
import re
from serial import Serial

###########################################################
# Importing Fernanda's Package
###########################################################
import numpy
import librosa
from os import system
import os
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import spotipy
from datetime import datetime, timedelta
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify
###########################################################
# Importing Rafael's Package
###########################################################
from datetime import datetime, timedelta
import numpy
###########################################################
# Global Variables
###########################################################

global count
global time_sub
global index_t 
global song_fixer
global name_artists
global name_song
global serial_lyric
global vocals_energy
global drums_energy
global bass_energy
global other_energy
global vocal_bar_spleeter
global drums_bar_spleeter
global bass_bar_spleeter
global other_bar_spleeter

vocal_bar_spleeter= [0]*600
drums_bar_spleeter= [0]*600
bass_bar_spleeter= [0]*600
other_bar_spleeter= [0]*600
count = 0
name_artists = ''
index_t = 0
time_sub = {}
###########################################################
#                       Setup Serial
###########################################################
#global myserial
#myserial = Serial("COM10", baudrate=9600)
###########################################################
#                       Tkinter Setup
###########################################################
root = Tk()

root.title("MP3 Player")
root.geometry("500x500")

#Initialize Pygame
pygame.mixer.init()

###########################################################
#                       Functions
###########################################################

###########################################################
#                       Time Functions
###########################################################

def play_time():

    global vocal_level
    global guitar_level
    global bass_level
    global piano_level
    global other_level
    global count

    # Check to see if song is stopped
    if stopped:
        return

    # Grab Current Song Time
    current_time = pygame.mixer.music.get_pos() / 1000

    #Convert Song Time To Time Format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # Reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = song.replace(" ", "_")
    song = f'C:/Users/micro1/Downloads/interface/songs/{song}.mp3'

    # Find Current Song Length
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length

    # Convert to Time Format
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # Check to see if song is over
    if int(song_slider.get()) == int(song_length):
        stop()

    elif paused:
        # Check to see if paused, if so > pass
        pass

    else:
        
        # Move Slider Along 1 Second At A Time
        next_time = int(song_slider.get()) + 1
        next_time_m = next_time // 60
        next_time_s = next_time % 60
        print(next_time)

        global time_sub
        times = time_sub.keys()

        global index_t

        for t in times:
            min, sec, ms = string_to_time(t)
            if min == next_time_m and (sec+1) == next_time_s:

                if index_t != t:
                    index_t = t
                    lyric_bar.delete('all')
                    lyric_bar.create_rectangle(3, 15, 415, 40, outline="#A0A0A0")
                lyric_bar.create_text(210, 28, text=time_sub[t], fill="#303841", font=('Helvetica','9'))
              #  lyric_send_serial(time_sub[t])
                #print(time_sub[t])


        # Output new time value to slider, and to length of Song
        song_slider.config(to=song_length, value=next_time)

        # Convert Slider Position to Time Format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

        # Output Slider
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
        
        time_str_bar.config(text=f'{converted_current_time}', bd=1, relief=GROOVE)
        
        time_end_bar.config(text=f'{converted_song_length}', bd=1, relief=GROOVE)

     
        create_bars(vocal_bar, vocal_bar_spleeter[next_time])
        create_bars(guitar_bar, drums_bar_spleeter[next_time])
        create_bars(bass_bar, bass_bar_spleeter[next_time])
      #  create_bars(piano_bar, piano_level[next_time])
        create_bars(other_bar, other_bar_spleeter[next_time])
     
     #   create_bars(vocal_bar, vocal_level[next_time])
     #   create_bars(guitar_bar, guitar_level[next_time])
     #   create_bars(bass_bar, bass_level[next_time])
     #   create_bars(piano_bar, piano_level[next_time])
     #   create_bars(other_bar, other_level[next_time])
    
    #Add Current Time To Status Bar
    if current_time > 0:
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
        time_str_bar.config(text=f'{converted_current_time}', bd=1, relief=GROOVE)
        time_end_bar.config(text=f'{converted_song_length}', bd=1, relief=GROOVE)

        create_bars(vocal_bar, vocal_bar_spleeter[next_time])
        create_bars(guitar_bar, drums_bar_spleeter[next_time])
        create_bars(bass_bar, bass_bar_spleeter[next_time])
    #    create_bars(piano_bar, piano_level[next_time])
        create_bars(other_bar, other_bar_spleeter[next_time])

      #  create_bars(vocal_bar, vocal_level[next_time])
     #   create_bars(guitar_bar, guitar_level[next_time])
      #  create_bars(bass_bar, bass_level[next_time])
      #  create_bars(piano_bar, piano_level[next_time])
      #  create_bars(other_bar, other_level[next_time])
    
    #Create Loop To Check the Time Every Second
    my_label.after(1000, play_time)

###########################################################
#                       Subtitles Functions
###########################################################

#Show IDs and Durations for the song_name
def search_id_song(song_name):
    global song_fixer
    song_fixer = song_name
    request = requests.get(f'https://music.xianqiao.wang/neteaseapiv2/search?type=1&keywords={song_name}')
    if request.status_code == 200:
      r = request.json()
      api_songs = {}
      for song  in r['result']['songs']:
        id = song['id']
        duration = song['duration']
        api_songs[id] = duration
      return api_songs
    else:
      return request.status_code

#Check if this song has subtitles
def is_subtitle(id):
  request = requests.get(f'https://music.xianqiao.wang/neteaseapiv2/lyric?id={id}')
  request = request.json()
  subtitle = request['lrc']['lyric']

  if len(subtitle) > 200 and len(re.findall('\[\d[0-9]\:\d[0-9]\.\d[0-9]\]', subtitle))>5:
    return True
  else:
    return False

#Seach the best id and duration 
def search_song(song_name, duration):
  time = duration
  min = time
  api_songs = search_id_song(song_name)
  for id in api_songs.keys():
    if abs(api_songs[id] - time) < min:
      if is_subtitle(id) :
        min = abs(api_songs[id] - time)
        id_min = id
  return (id_min, api_songs[id_min])

def show_subtitle(id):
  request = requests.get(f'https://music.xianqiao.wang/neteaseapiv2/lyric?id={id}')
  r = request.json()
  return r['lrc']['lyric']


def time_and_song(id):

  search_artists_song(id)
  
  subtitle = show_subtitle(id)
  subtitle = subtitle.split('\n')
  time_music = {}

  for line in subtitle:
    try:
      if len(line)>7:
        time, music = line.split(']')
        time = time.replace('[', '')
        time_music[time] = music
    except ValueError:
      print('Bad subtitle')
  return time_music

def seconds_for_minutes_and_seconds(time):
  minutes = time // 60
  seconds = time % 60
  return (minutes, seconds)

def string_to_time(s_time):
  minutes, seconds = s_time.split(':')
  seconds, miliseconds = seconds.split('.')
  return (int(minutes), int(seconds), int(miliseconds))
###########################################################
#                       Serial Functions
###########################################################

"""def send_serial(message):
    print(message)
    message+='\n'
    myserial.write(message.encode("UTF-8"))
    
def lyric_send_serial(message):
    print(message)
    message+='\n'
    new_message= 'letra' + message
    myserial.write(new_message.encode("UTF-8"))"""

###########################################################
#                       Send Team Functions
###########################################################

# Function to Send Fernanda Name File + Name Song + Artist Name
def search_artists_song(id):
    global song_fixer
    global name_song
    global name_artists
    i=0
    request = requests.get(f'https://music.xianqiao.wang/neteaseapiv2/search?type=1&keywords={song_fixer}')
    if request.status_code == 200:
      r = request.json()
      api_songs = {}
      for song  in r['result']['songs']:
        if (id == song['id']):
            name_song = song['name']
            artists = song['artists']
            for art in artists:
                if (i%2 == 0):
                    name_artists += art['name'] + ', '
            i=i+1        
    i=0 
    name_artists=name_artists[:-2] 

    # Prints
    print('-------------------------------------------------')
    print('--------- Start Fernandas Prints ----------------')
    print('--------------- Music Loaded --------------------')
    print('Song file name = ' + song_fixer)
    print('Song Name = ' + name_song)
    print('Song Artists = ' + name_artists)
    print('--------------- End Prints ----------------------')
    print('-------------------------------------------------')
    
    

# Function to create and send file to Rafael with Lyrics
def create_and_send_lyric():
    with open('lyrics.txt', 'w') as convert_file:
     convert_file.write(json.dumps(time_sub))
     
def clean_lyric_data():
    global time_sub
    global serial_lyric
    serial_lyric = str(time_sub)
    # Prints
    print('-------------------------------------------------')
    print('------------ Start Rafaels Prints ---------------')
    print('--------------- Lyrics --------------------------')
    print('Lyrics = ' + serial_lyric)
#    send_serial(serial_lyric)
    print('--------------- End Prints ----------------------')
    print('-------------------------------------------------')
    
def read_instrument_data():
    global vocals_energy
    global drums_energy
    global bass_energy
    global other_energy
    
    with open('energy_vocals.txt', 'r') as file:
        vocals_energy = file.readlines()
    with open('energy_drums.txt', 'r') as file:
        drums_energy = file.readlines()
    with open('energy_bass.txt', 'r') as file:
        bass_energy = file.readlines()
    with open('energy_other.txt', 'r') as file:
        other_energy = file.readlines()
        
def clear_instrument_data():
    global vocals_energy
    global drums_energy
    global bass_energy
    global other_energy
    global vocal_bar_spleeter
    global drums_bar_spleeter
    global bass_bar_spleeter
    global other_bar_spleeter
    j=0
    k=0
    vocal_bar_min =[0]*600
    vocal_bar_sec = [0]*600
    drums_bar_min =[0]*600
    drums_bar_sec = [0]*600
    bass_bar_min =[0]*600
    bass_bar_sec = [0]*600
    other_bar_min =[0]*600
    other_bar_sec = [0]*600
    
    for item in vocals_energy:
        
        vocal_bar_spleeter[j] = int(float(item.partition("-")[2][:-2])*100)
        vocal_bar_min[j] = int(item.partition(":")[0])
        vocal_bar_sec[j] = int(item.partition(":")[2][:-7])
        if (vocal_bar_min[j] == vocal_bar_min[j-1] and vocal_bar_sec[j]== vocal_bar_sec[j-1]):
            if (vocal_bar_spleeter[j]>vocal_bar_spleeter[j-1]):
                #print('entrou em m:'+vocal_bar_min[j]+'e em s:'+vocal_bar_sec[j])
                if(vocal_bar_spleeter[k]==0):
                    vocal_bar_spleeter[k]=0
                elif(vocal_bar_spleeter[k]<21):
                    vocal_bar_spleeter[k]=1
                elif(vocal_bar_spleeter[k]<41):
                    vocal_bar_spleeter[k]=2
                elif(vocal_bar_spleeter[k]<61):
                    vocal_bar_spleeter[k]=3
                elif(vocal_bar_spleeter[k]<81):
                    vocal_bar_spleeter[k]=4
                else:
                    vocal_bar_spleeter[k]=5
                j=j+1
        else:
            if(vocal_bar_spleeter[k]==0):
                vocal_bar_spleeter[k]=0
            elif(vocal_bar_spleeter[k]<21):
                vocal_bar_spleeter[k]=1
            elif(vocal_bar_spleeter[k]<41):
                vocal_bar_spleeter[k]=2
            elif(vocal_bar_spleeter[k]<61):
                vocal_bar_spleeter[k]=3
            elif(vocal_bar_spleeter[k]<81):
                vocal_bar_spleeter[k]=4
            else:
                vocal_bar_spleeter[k]=5
            j=j+1
            k=k+1
    j=0
    k=0
    print(vocal_bar_spleeter)
    for item in drums_energy:
        
        drums_bar_spleeter[j] = int(float(item.partition("-")[2][:-2])*100)
        drums_bar_min[j] = int(item.partition(":")[0])
        drums_bar_sec[j] = int(item.partition(":")[2][:-7])
        if (drums_bar_min[j] == drums_bar_min[j-1] and drums_bar_sec[j]== drums_bar_sec[j-1]):
            drums_bar_spleeter[j] = (drums_bar_spleeter[j]+drums_bar_spleeter[j-1])/2
            if(drums_bar_spleeter[k]==0):
                drums_bar_spleeter[k]=0
            elif(drums_bar_spleeter[k]<21):
                drums_bar_spleeter[k]=1
            elif(drums_bar_spleeter[k]<41):
                drums_bar_spleeter[k]=2
            elif(drums_bar_spleeter[k]<61):
                drums_bar_spleeter[k]=3
            elif(drums_bar_spleeter[k]<81):
                drums_bar_spleeter[k]=4
            else:
                drums_bar_spleeter[k]=5
            j=j+1
        else:
            if(drums_bar_spleeter[k]==0):
                drums_bar_spleeter[k]=0
            elif(drums_bar_spleeter[k]<21):
                drums_bar_spleeter[k]=1
            elif(drums_bar_spleeter[k]<41):
                drums_bar_spleeter[k]=2
            elif(drums_bar_spleeter[k]<61):
                drums_bar_spleeter[k]=3
            elif(drums_bar_spleeter[k]<81):
                drums_bar_spleeter[k]=4
            else:
                drums_bar_spleeter[k]=5
            j=j+1
            k=k+1
    j=0
    k=0
    for item in bass_energy:
        
        bass_bar_spleeter[j] = int(float(item.partition("-")[2][:-2])*100)
        bass_bar_min[j] = int(item.partition(":")[0])
        bass_bar_sec[j] = int(item.partition(":")[2][:-7])
        if (bass_bar_min[j] == bass_bar_min[j-1] and bass_bar_sec[j]== bass_bar_sec[j-1]):
            bass_bar_spleeter[j] = (bass_bar_spleeter[j]+bass_bar_spleeter[j-1])/2
            if(bass_bar_spleeter[k]==0):
                bass_bar_spleeter[k]=0
            elif(bass_bar_spleeter[k]<21):
                bass_bar_spleeter[k]=1
            elif(bass_bar_spleeter[k]<41):
                bass_bar_spleeter[k]=2
            elif(bass_bar_spleeter[k]<61):
                bass_bar_spleeter[k]=3
            elif(bass_bar_spleeter[k]<81):
                bass_bar_spleeter[k]=4
            else:
                bass_bar_spleeter[k]=5
            j=j+1
        else:
            if(bass_bar_spleeter[k]==0):
                bass_bar_spleeter[k]=0
            elif(bass_bar_spleeter[k]<21):
                bass_bar_spleeter[k]=1
            elif(bass_bar_spleeter[k]<41):
                bass_bar_spleeter[k]=2
            elif(bass_bar_spleeter[k]<61):
                bass_bar_spleeter[k]=3
            elif(bass_bar_spleeter[k]<81):
                bass_bar_spleeter[k]=4
            else:
                bass_bar_spleeter[k]=5
            j=j+1
            k=k+1
    j=0
    k=0
    for item in other_energy:
        
        other_bar_spleeter[j] = int(float(item.partition("-")[2][:-2])*100)
        other_bar_min[j] = int(item.partition(":")[0])
        other_bar_sec[j] = int(item.partition(":")[2][:-7])
        if (other_bar_min[j] == other_bar_min[j-1] and other_bar_sec[j]== other_bar_sec[j-1]):
            other_bar_spleeter[j] = (other_bar_spleeter[j]+other_bar_spleeter[j-1])/2
            if(other_bar_spleeter[k]==0):
                other_bar_spleeter[k]=0
            elif(other_bar_spleeter[k]<21):
                other_bar_spleeter[k]=1
            elif(other_bar_spleeter[k]<41):
                other_bar_spleeter[k]=2
            elif(other_bar_spleeter[k]<61):
                other_bar_spleeter[k]=3
            elif(other_bar_spleeter[k]<81):
                other_bar_spleeter[k]=4
            else:
                other_bar_spleeter[k]=5
            j=j+1
        else:
            if(other_bar_spleeter[k]==0):
                other_bar_spleeter[k]=0
            elif(other_bar_spleeter[k]<21):
                other_bar_spleeter[k]=1
            elif(other_bar_spleeter[k]<41):
                other_bar_spleeter[k]=2
            elif(other_bar_spleeter[k]<61):
                other_bar_spleeter[k]=3
            elif(other_bar_spleeter[k]<81):
                other_bar_spleeter[k]=4
            else:
                other_bar_spleeter[k]=5
            j=j+1
            k=k+1
    j=0
    k=0
        
        
    
###########################################################
#                       Fernanda's Functions
###########################################################
# Function to get the feelings
def defining_feelings():
    #Chaves de acesso a API do Spotify
    client_id= "9b13712054834eaba19cf6b8e506faa2"
    client_secret= "bceb6248d6a14c04a7558c3bbb7b6075"

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

    #Inputs que precisam me mandar
    nomedamusica = name_song
    artistamusica = name_artists
    id_musica = nomedamusica + "," + artistamusica
    nome_arq_musica = song_fixer

    #Data Querying
    artist_name = []
    track_name = []
    track_popularity = []
    artist_id = []
    track_id = []


    for i in range(0,50,20):
        track_results = sp.search(q=id_musica, type='track', limit=1,offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            artist_name.append(t['artists'][0]['name'])
            artist_id.append(t['artists'][0]['id'])
            track_name.append(t['name'])
            track_id.append(t['id'])
            track_popularity.append(t['popularity'])
            
    track_df = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'id' : track_id, 'track_popularity' : track_popularity, 'artist_id' : artist_id})
    #print(track_df.shape)
    track_df = track_df.head(1)
    #print(track_df)

    #Fetch Track's Features
    track_features = []
    for t_id in track_df['id']:
      af = sp.audio_features(t_id)
      track_features.append(af)  
    tf_df = pd.DataFrame(columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature'])
    for item in track_features:
      for feat in item:
        tf_df = tf_df.append(feat, ignore_index=True)
        
    df_result = pd.merge(track_df, tf_df)
    #df_result.head()

    df_result['artist_name'] = df_result['artist_name'].astype("string")
    df_result['track_name'] = df_result['track_name'].astype("string")
    df_result['id'] = df_result['id'].astype("string")
    df_result['track_popularity'] = pd.to_numeric(df_result['track_popularity'])
    df_result['artist_id'] = df_result['artist_id'].astype("string")
    df_result['danceability'] = pd.to_numeric(df_result['danceability'])
    df_result['energy'] = pd.to_numeric(df_result['energy'])
    df_result['key'] = pd.to_numeric(df_result['key'])
    df_result['loudness'] = pd.to_numeric(df_result['loudness'])
    df_result['mode'] = pd.to_numeric(df_result['mode'])
    df_result['speechiness'] = pd.to_numeric(df_result['speechiness'])
    df_result['acousticness'] = pd.to_numeric(df_result['acousticness'])
    df_result['instrumentalness'] = pd.to_numeric(df_result['instrumentalness'])
    df_result['liveness'] = pd.to_numeric(df_result['liveness'])
    df_result['valence'] = pd.to_numeric(df_result['valence'])
    df_result['tempo'] = pd.to_numeric(df_result['tempo'])
    df_result['type'] = df_result['type'].astype("string")
    df_result['uri'] = df_result['uri'].astype("string")
    df_result['track_href'] = df_result['track_href'].astype("string")
    df_result['analysis_url'] = df_result['analysis_url'].astype("string")
    df_result['duration_ms'] = pd.to_numeric(df_result['duration_ms'])
    df_result['time_signature'] = df_result['time_signature'].astype("category")
    #print(tf_df.info())
    #print(track_df.info())
    df_result.head()

    #Caso tenha a necessidade de tirar algum atributo:
    cols_to_drop2 = ['id','track_popularity','artist_id','key','loudness','mode','speechiness', 'acousticness','instrumentalness','liveness','tempo', 'type', 'uri','track_href','analysis_url','duration_ms','time_signature']
    tf_df = df_result.drop(columns=cols_to_drop2)
    #print(track_df.info())
    #print(tf_df.info())
    tf_df.head()

    danceability = str(tf_df.loc[:,"danceability"].values[0])
    energy = str(tf_df.loc[:,"energy"].values[0])
    valence = str(tf_df.loc[:,"valence"].values[0])
    feelings = ("Sentimentos:" + danceability + "," + energy + "," + valence)
    
    # Prints
    print('-------------------------------------------------')
    print('--------- Start Fernandas Prints ----------------')
    print('--------------- Feelings Loaded -----------------')
    print("Sentimentos:" + danceability + "," + energy + "," + valence)
#    send_serial(feelings)
    print('--------------- End Prints ----------------------')
    print('-------------------------------------------------')

###########################################################
#                       Rafael's Functions
###########################################################



###########################################################
#                       Tab Functions
###########################################################

# Create Function To Add One Song To Playlist
def add_song():
    playlist_box.delete(0, END)
    song = filedialog.askopenfilename(initialdir='songs/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    song_mut = MP3(song)
    song_length = song_mut.info.length * 1000

    # Strip out directory structure and .mp3 from Song Title
    song = song.replace("C:/Users/micro1/Downloads/interface/songs/", "")
    song = song.replace(".mp3", "")
    id , duration = search_song(song, song_length)
    
    global time_sub 
    time_sub = time_and_song(id)
    
    defining_feelings()
    clean_lyric_data()
    read_instrument_data()
    clear_instrument_data()
    

    playlist_box.insert(END,song)

# Create Function To Add Many Songs To Playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='songs/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))

    #Loop through song list and replace directory structure and .mp3 from Song Title
    for song in songs:

        # Strip out directory structure and .mp3 from Song Title
        song = song.replace("C:/Users/micro1/Downloads/interface/songs/", "")
        song = song.replace(".mp3", "")
        song = song.replace("_", " ")

        #Add To End To Playlist
        playlist_box.insert(END,song)

# Create Function To Delete One Song From Playlist
def delete_song():
    # Delete Highlighted Song From Playlist
    playlist_box.delete(ANCHOR)
    

# Create Function To Delete All Songs From Playlist
def delete_all_songs():
    # Delete All Songs 
    playlist_box.delete(0, END)

###########################################################
#                       Buttons Functions
###########################################################

# Create Play Function
def play():

    # Set Stopped to False since a song is nwo playing
    global stopped
    stopped = False

    # Reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = song.replace(" ", "_")
    song = f'C:/Users/micro1/Downloads/interface/songs/{song}.mp3'

    # Load song with pygame mixer
    pygame.mixer.music.load(song)

    # Play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    create_and_send_lyric()
    

    # Get Song Time
    play_time()

# Create Stopped Variable
global stopped
stopped = False

# Create Stop Function
def stop():
    
    time_str_bar.config(text='0:00', bd=1, relief=GROOVE)
    time_end_bar.config(text='0:00', bd=1, relief=GROOVE)
    
    # Stop the song
    pygame.mixer.music.stop()

    # Clear Playlist Bar
    playlist_box.selection_clear(ACTIVE)

    status_bar.config(text='')

    # Set Our Slider to Zero
    song_slider.config(value=0)

    #Set Stop Variable To True
    global stopped
    stopped = True

    vocal_bar.delete("all")
    guitar_bar.delete("all")
    bass_bar.delete("all")
  #  piano_bar.delete("all")
    other_bar.delete("all")

    vocal_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
    guitar_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
    bass_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
 #   piano_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
    other_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")

    lyric_bar.delete('all')
    lyric_bar.create_rectangle(3, 15, 415, 40, outline="#A0A0A0")

# Create Paused Variable
global paused
paused = False

# Create Pause Function
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused= False

    else:
        #Pause
        pygame.mixer.music.pause()
        paused= True

# Create Function To Play The Next Song
def next_song():
    # Reset Slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)

    # Get current song number
    next_one = playlist_box.curselection()

    # Add One To The Current Song Number Tuple
    next_one = next_one[0] + 1

    # Grab the song title from the playlist
    song = playlist_box.get(next_one)

    # Reconstruct song with directory structure
    song = song.replace(" ", "_")
    song = f'C:/Users/micro1/Downloads/interface/songs/{song}.mp3'

    # Load song with pygame mixer
    pygame.mixer.music.load(song)

    # Play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    # Clear Ative Bar in Playlist
    playlist_box.selection_clear(0, END)

    # Move Active Bar To Next Song
    playlist_box.activate(next_one)

    # Set Active Bar To Next Song
    playlist_box.selection_set(next_one,last=None)

# Create Function to Play Previous Song
def previous_song():
    # Reset Slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)

    # Get current song number
    next_one = playlist_box.curselection()

    # Add One To The Current Song Number Tuple
    next_one = next_one[0] -1

    # Grab the song title from the playlist
    song = playlist_box.get(next_one)

    # Reconstruct song with directory structure
    song = song.replace(" ", "_")
    song = f'C:/Users/micro1/Downloads/interface/songs/{song}.mp3'

    # Load song with pygame mixer
    pygame.mixer.music.load(song)

    # Play song with pygame mixer
    pygame.mixer.music.play(loops=0)

    # Clear Ative Bar in Playlist
    playlist_box.selection_clear(0, END)

    # Move Active Bar To Next Song
    playlist_box.activate(next_one)

    # Set Active Bar To Next Song
    playlist_box.selection_set(next_one,last=None)

###########################################################
#                       Volume Functions
###########################################################

# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

###########################################################
#                       Generate Functions
###########################################################

global vocal_level
global guitar_level
global bass_level
global piano_level
global other_level

vocal_level = [0] * 300
guitar_level = [0] * 300
bass_level = [0] * 300
piano_level = [0] * 300
other_level = [0] * 300

def generate_level():
    global vocal_level
    global guitar_level
    global bass_level
    global piano_level
    global other_level

    for i in range(300):
        global vocal_level
        vocal_level[i]=random.randint(0,5)
        guitar_level[i]=random.randint(0,5)
        bass_level[i]=random.randint(0,5)
        piano_level[i]=random.randint(0,5)
        other_level[i]=random.randint(0,5)


###########################################################
#                       Create Bar Functions
###########################################################

def create_bars(canvas, i):
    canvas.delete("all")
    canvas.create_rectangle(3, 20, 50, 118, outline="#A0A0A0")

    if i>=1:
        canvas.create_rectangle(5, 100, 50, 115, fill="red")

    if i>=2:
        canvas.create_rectangle(5, 80, 50, 95, fill="red")
    
    if i>=3:
        canvas.create_rectangle(5, 60, 50, 75, fill="red")

    if i>=4:
        canvas.create_rectangle(5, 40, 50, 55 , fill="red")

    if i>=5:
        canvas.create_rectangle(5, 20, 50, 35, fill="red")

###########################################################
#                       Volume Functions
###########################################################
# Create Slider Function For Song Positioning
def slide(x):
    # Reconstruct song with directory structure
    song = playlist_box.get(ACTIVE)
    song = song.replace(" ", "_")
    song = f'C:/Users/micro1/Downloads/interface/songs/{song}.mp3'

    # Load song with pygame mixer
    pygame.mixer.music.load(song)

    # Play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())


###########################################################
#                       Interface
###########################################################

# Create Main Frame
main_frame = Frame(root)
main_frame.pack(pady=10)

############################################################
################### Row 0 - Search #########################
############################################################

# Create Button Frame
music_frame = Frame(main_frame)
music_frame.grid(row=0, column=0)

# Label to Choose name
choose_music = Label(music_frame, text="Escolha a Música:")
choose_music.grid(row=0, column=0, pady=20)

# Label to Choose name
choose_music = Label(music_frame, text="Selecione o MP3")
choose_music.grid(row=1, column=0)

# Create Playlist Box
playlist_box = Listbox(music_frame, bg="black", fg="green", width=40,height=1, selectbackground="green", selectforeground="black")
playlist_box.grid(row=2, column=0)

#Create Search Button
btn_search = Button(music_frame, text="Buscar", command=add_song)
btn_search.grid(row=2,column=2)

############################################################
################### Row 1 - Controls #######################
############################################################

#Define Button Images For Controls

back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play25.png')
pause_btn_img = PhotoImage(file='images/pause25.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

# Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# Create Play/Stop Buttons

play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
stop_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=stop)

play_button.grid(row=0,column=0, padx=0)
stop_button.grid(row=0,column=1, padx=0)

# Create Song Slider
song_slider = ttk.Scale(control_frame, from_ = 0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=0, column=3, pady=10)

time_str_bar = Label(control_frame, text='0:00', bd=1, relief=GROOVE)
time_str_bar.grid(row=0,column=2)

time_end_bar = Label(control_frame, text='0:00', bd=1, relief=GROOVE)
time_end_bar.grid(row=0,column=4)

############################################################
#################### Row 2 - Lyrics ########################
############################################################

# Create Lyric Frame
lyric_frame = Frame(main_frame)
lyric_frame.grid(row=2,column=0)

# Create Lyrics Bar
actual_lyric_frame = Label(lyric_frame, text='Letra:')
actual_lyric_frame.grid(row=0,column=0)

lyric_bar = Canvas(lyric_frame, width=420, height=50)
lyric_bar.grid(row=0,column=1)

lyric_bar.create_rectangle(3, 15, 415, 40, outline="#A0A0A0")

# Text Lyric
#lyric_bar.create_text(210, 28, text="Billie Jean is not my lover", fill="#303841", font=('Helvetica','9'))

############################################################
################# Row 3 - Volume Slider ####################
############################################################

# Create Volume Slider Frame
volume_frame = LabelFrame(main_frame, text='Volume')
volume_frame.grid(row=3,column=0, padx=0 )

# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_ = 0, to=1, orient=HORIZONTAL, length=125, value=0.5, command=volume)
volume_slider.pack(pady=10)

############################################################
################ Row 4 - Instruments Bar ###################
############################################################

# Create Instruments Volume Bar Frame

instrument_frame = Frame(main_frame)
instrument_frame.grid(row=4, column=0)

# Create Instruments Bars

vocal_frame = Label(instrument_frame, text='vocals')
vocal_frame.grid(row=5,column=0, padx= 30)

guitar_frame = Label(instrument_frame,text="drums")
guitar_frame.grid(row=5,column=1, padx= 30)

bass_frame = Label(instrument_frame,text="bass")
bass_frame.grid(row=5,column=2, padx= 30)

#piano_frame = Label(instrument_frame,text="piano")
#piano_frame.grid(row=5,column=3,  padx= 30)

other_frame = Label(instrument_frame,text="other")
other_frame.grid(row=5,column=4,  padx= 30)

#Bar Images For Instrument Levels

bar_level_img = PhotoImage(file='images/bar.png')
bar_clean_level_img = PhotoImage(file='images/graybar.png')

vocal_bar = Canvas(instrument_frame, width=50,height=125)
guitar_bar = Canvas(instrument_frame, width=50,height=125)
bass_bar = Canvas(instrument_frame, width=50,height=125)
#piano_bar = Canvas(instrument_frame, width=50,height=125)
other_bar = Canvas(instrument_frame, width=50,height=125)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)

generate_level()

vocal_bar.grid(row=0,column=0)
guitar_bar.grid(row=0,column=1)
bass_bar.grid(row=0,column=2)
#piano_bar.grid(row=0,column=3)
other_bar.grid(row=0,column=4)

vocal_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
guitar_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
bass_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
#piano_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")
other_bar.create_rectangle(3, 20, 50, 120, outline="#A0A0A0")

############################################################
#################### Status Bar ############################
############################################################

# Create Status Bar
status_bar = Label(root, text='nothing', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

root.mainloop()
