#Importação de bibliotecas
import numpy
import librosa
from os import system
import os
import spleeter
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import spotipy
from datetime import datetime, timedelta
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

#Chaves de acesso a API do Spotify
client_id= "9b13712054834eaba19cf6b8e506faa2"
client_secret= "bceb6248d6a14c04a7558c3bbb7b6075"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

#Inputs que precisam me mandar
nomedamusica = "Glamurosa"
artistamusica = "MC Marcinho"
id_musica = nomedamusica + "," + artistamusica
nome_arq_musica = "Glamurosa"

---------------------------------------
path = f"{os.getenv('USERPROFILE')}\\Downloads"
path_mus = path + "\\" + nome_arq_musica
#print(path)
print(path_mus)
lista = ['vocals','drums','bass','other']

print(nome_arq_musica+".mp3")

system("python -m spleeter separate -o audio_output -p spleeter:4stems "+ path_mus+".mp3")

print("será?")


#system("python -m spleeter separate -o audio_output3 -p spleeter:4stems MrJones.mp3 ")
caminho = "C:\\Users\\Fernanda\\Desktop\\PUC - 2022.2\\prog de micro\\Projeto Robo Musical\\audio_output3\\MrJones\\"
lista = ['vocals','drums','bass','other']
for arq_esc in lista:
    print("----------------------------------------------")
    x1, sr1 = librosa.load(caminho + arq_esc + ".wav")
    #print(sr1)
    dur = librosa.get_duration(x1,sr1)
    print("duração da musica:"+ str(dur) + "segundos")
    hop_length = int(len(x1)/512)
    frame_length = 512
    energy = numpy.array([sum(abs(x1[i:i+frame_length]**2)) for i in range(0, len(x1), hop_length)])
    #print("tamanho do vetor energia:"+str(len(energy)))
    
    
    tempo, beat_frames = librosa.beat.beat_track(y=x1, sr=sr1) #tempo em batidas/min
    beat_times = librosa.frames_to_time(beat_frames, sr=sr1)  #print the frames corresponding to beats as timestamps
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))  
    print(beat_times)
    
    file = open('C:\\Users\\Fernanda\\Desktop\\PUC - 2022.2\\prog de micro\\Projeto Robo Musical\\audio_output3\\energy_'+ arq_esc +'.txt','w+')
    for pos, elem in enumerate(energy):
        tempo = dur/frame_length * pos
        minut = tempo//60
        seg = tempo%60
        file.write("horario: %.0f:%.0f - energy:"%(minut, seg)  + "%.2f"%(elem) + "\n" )
    file.close()


#system("python -m spleeter separate -o audio_output3 -p spleeter:4stems MrJones.mp3 ")
caminho = "C:\\Users\\Fernanda\\Desktop\\PUC - 2022.2\\prog de micro\\Projeto Robo Musical\\audio_output3\\MrJones\\"
lista = ['vocals','drums','bass','other']
for arq_esc in lista:
    print("----------------------------------------------")
    x1, sr1 = librosa.load(caminho + arq_esc + ".wav")
    #print(sr1)
    dur = librosa.get_duration(x1,sr1)
    print("duração da musica:"+ str(dur) + "segundos")
    hop_length = int(len(x1)/512)
    frame_length = 512
    energy = numpy.array([sum(abs(x1[i:i+frame_length]**2)) for i in range(0, len(x1), hop_length)])
    #print("tamanho do vetor energia:"+str(len(energy)))
    
    
    tempo, beat_frames = librosa.beat.beat_track(y=x1, sr=sr1) #tempo em batidas/min
    beat_times = librosa.frames_to_time(beat_frames, sr=sr1)  #print the frames corresponding to beats as timestamps
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))  
    print(beat_times)
    
    file = open('C:\\Users\\Fernanda\\Desktop\\PUC - 2022.2\\prog de micro\\Projeto Robo Musical\\audio_output3\\energy_'+ arq_esc +'.txt','w+')
    for pos, elem in enumerate(energy):
        tempo = dur/frame_length * pos
        minut = tempo//60
        seg = tempo%60
        file.write("horario: %.0f:%.0f - energy:"%(minut, seg)  + "%.2f"%(elem) + "\n" )
    file.close()