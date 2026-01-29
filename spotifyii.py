#Importação de bibliotecas
import numpy
import librosa
from os import system
import os
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
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

print("Sentimentos:" + danceability + "," + energy + "," + valence)

