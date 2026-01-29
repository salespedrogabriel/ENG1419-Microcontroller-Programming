from datetime import datetime, timedelta
import serial
import time
import numpy

musica = "[00:09.85]Come on over in my direction\n[00:12.36]So thankful for that it's such a blessin' yeah\n[00:15.07]Turn every situation into heaven yeah\n[00:18.30]Oh you are\n[00:20.82]My sunrise on the darkest day\n[00:23.49]Got me feelin' some kind of way\n[00:26.13]Make me wanna savor every moment slowly slowly\n[00:31.28]You fit me tailor made love how you put it on\n[00:33.86]Got the only key know how to turn it on\n[00:36.38]The way you nibble on my ear the only words I wanna hear\n[00:39.51]Baby take it slow so we can last long\n[00:40.76]Oh tú tú eres el imán y yo soy el metal\n[00:44.71]Me voy acercando y voy armando el plan\n[00:47.37]Sólo con pensarlo se acelera el pulso\n[00:51.27]Oh yeah ya ya me está gustando más de lo normal\n[00:55.65]Todos mis sentidos van pidiendo má s\n[00:58.26]Esto hay que tomarlo sin ningún apuro\n[01:02.05]Despacito\n[01:04.41]Quiero respirar tu cuello despacito\n[01:06.93]Deja que te diga cosas al oído\n[01:09.52]Para que te acuerdes si no estás conmigo\n[01:13.06]Despacito\n[01:15.08]Quiero desnudarte a besos despacito\n[01:17.55]Firmo en las paredes de tu laberinto\n[01:20.37]Y hacer de tu cuerpo todo un manuscrito\n[01:22.73]Sube sube sube\n[01:23.99]Sube sube\n[01:25.17]Quiero ver bailar tu pelo\n[01:26.81]Quiero ser tu ritmo\n[01:28.99]Que le enseñes a mi boca\n[01:31.68]Tus lugares favoritos\n[01:33.93]Favorito favorito baby\n[01:35.75]Dé jame sobrepasar tus zonas de peligro\n[01:39.73]Hasta provocar tus gritos\n[01:42.52]Y que olvides tu apellido\n[01:45.56]Si te pido un beso ven dámelo\n[01:47.18]Yo sé que estás pensándolo\n[01:48.56]Llevo tiempo intentándolo\n[01:49.75]Mami esto es dando y dándolo\n[01:51.23]Sabes que tu corazón conmigo te hace bang bang\n[01:54.06]Sabes que esa beba está buscando de mi bang bang\n[01:56.67]Ven prueba de mi boca para ver có mo te sabe\n[01:59.40]Quiero quiero quiero ver cuá nto amor a ti te cabe\n[02:02.08]Yo no tengo prisa yo me quiero dar el viaje\n[02:04.77]Empecemos lento después salvaje\n[02:07.58]Pasito a pasito suave suavecito\n[02:10.12]Nos vamos pegando poquito a poquito\n[02:12.84]Cuando tú me besas con esa destreza\n[02:15.51]Veo que eres malicia con delicadeza\n[02:18.26]Pasito a pasito suave suavecito\n[02:20.85]Nos vamos pegando poquito a poquito\n[02:23.54]Y es que esa belleza es un rompecabezas\n[02:26.23]Pero pa' montarlo aquí tengo la pieza\n[02:29.28]Oye\n[02:29.95]Despacito\n[02:31.57]Quiero respirar tu cuello despacito\n[02:34.39]Deja que te diga cosas al oí do\n[02:37.00]Para que te acuerdes si no está s conmigo\n[02:40.67]Despacito\n[02:42.58]Quiero desnudarte a besos despacito\n[02:45.13]Firmo en las paredes de tu laberinto\n[02:47.93]Y hacer de tu cuerpo todo un manuscrito\n[02:50.37]Sube sube sube\n[02:51.72]Sube sube\n[02:52.76]Quiero ver bailar tu pelo\n[02:54.47]Quiero ser tu ritmo\n[02:56.56]Que le enseñ es a mi boca\n[02:59.32]Tus lugares favoritos\n[03:01.55]Favorito favorito baby\n[03:03.35]Dé jame sobrepasar tus zonas de peligro\n[03:07.33]Hasta provocar tus gritos\n[03:10.11]Y que olvides tu apellido\n[03:12.49]Despacito\n[03:15.12]This is how we do it down in puerto rico\n[03:17.58]I just wanna hear you screaming  ay bendito\n[03:20.30]I can move foreverm se quede contigo\n[03:23.72]Bailalo\n[03:24.55]Pasito a pasito suave suavecito\n[03:27.16]Nos vamos pegando poquito a poquito\n[03:29.33]Que le enseñ es a mi boca\n[03:31.78]Tus lugares favoritos\n[03:33.60]Favorito favorito baby\n[03:35.54]Pasito a pasito suave suavecito\n[03:37.87]Nos vamos pegando poquito a poquito\n[03:40.20]Hasta provocar tus gritos fonsi\n[03:42.89]Y que olvides tu apellido d y\n[03:45.30]Despacito\n"
#musica = {"00:00.000": " \u4f5c\u8bcd : John Martin Lindstr\u00f6m/Michel Henry Allan Zitron/Axel Christofer Hedfors/Sebastian Ingrosso/Steve Angello", "00:01.000": " \u4f5c\u66f2 : John Martin Lindstr\u00f6m/Michel Henry Allan Zitron/Axel Christofer Hedfors/Sebastian Ingrosso/Steve Angello", "00:06.58": "There was a time  I used to look into my father's eyes", "00:13.83": "In a happy home  I was a king I had a gold throne", "00:21.46": "Those days are gone  now the memories are on the wall", "00:28.95": "I hear the sounds from the places where I was born", "00:38.89": "Up on the hill across the blue lake", "00:42.58": "Thats where I had my first heart break", "00:46.20": "I still remember how it all changed", "00:51.45": "My father said", "00:53.89": "Don't you worry  don't you worry child", "00:57.76": "See heaven's got a plan for you", "01:01.14": "Don't you worry  don't you worry now", "01:05.33": "Yeah", "01:23.89": "Don't you worry  don't you worry child", "01:27.58": "See heaven's got a plan for you", "01:30.89": "Don't you worry  don't you worry now", "01:35.02": "Yeah", "01:39.38": "There was a time  I met a girl of a different kind", "01:46.88": "We ruled the world", "01:49.38": "I Thought I'll never lose her out of sight  we were so young", "01:57.26": "I think of her now and then", "02:01.44": "I Still hear the song reminding me of when", "02:11.82": "Up on the hill across the blue lake", "02:15.51": "Thats where I had my first heart break", "02:19.13": "I still remember how it all changed", "02:24.32": "My father said", "02:26.94": "Don't you worry  don't you worry child", "02:30.69": "See heaven's got a plan for you", "02:34.13": "Don't you worry  don't you worry now", "02:38.26": "Yeah", "02:56.82": "Don't you worry  don't you worry child", "03:00.51": "See heaven's got a plan for you", "03:03.95": "Don't you worry  don't you worry now", "03:07.95": "Yeah", "03:12.51": "Ooh ooh ooh ooooh"}

n=0
i=0

lista_frase=[]
lista_tempo=[]
tempo_inicial = datetime.now()
tempo_inicial = tempo_inicial.minute*60 + tempo_inicial.second + tempo_inicial.microsecond/1000000

def separar_strings(musica):
    global n, j, quantidade
    
    lista_versos= musica.split("\n")
    quantidade=len(lista_versos)     #quantidade versos
    print("total de versos:",quantidade)
    print(lista_versos)
    
    while n<quantidade:
        tempo = lista_versos[n][:10]      
        frase = lista_versos[n][10:]
        
        lista_tempo.append(tempo)
        lista_frase.append(frase)
        
        #print(prox_verso)
        print(tempo)
        print(frase)
        #print(n)
        #print("\n")  # para ver no shell
        n=n+1

    
separar_strings(musica)  #roda em menos de 1s e cria listas de tempo e os versos


def enviar_serial(tempo_inicial):
        ser = serial.Serial() 
        ser.baudrate = 9600 
        ser.port = 'COM16' # write port on which you connected your Arduino
        global i
        agora = datetime.now()
        agora = agora.minute*60 + agora.second + agora.microsecond/1000000
        dif = agora-tempo_inicial 
        while i<quantidade:
            minuto = int(lista_tempo[i][1:3])
            segundo = int(lista_tempo[i][4:6])
            milesimo = int(lista_tempo[i][7:9])
            instante = minuto*60 + segundo + milesimo/1000
            #ser.write("letra")
            while dif < instante:
                print("enviado pela serial")
                ser.write("letra " + lista_frase[i])
                agora = datetime.now()
                agora = agora.minute*60 + agora.second + agora.microsecond/1000000
                dif = agora-tempo_inicial         
            i=i+1
        ser.close()
        
enviar_serial(tempo_inicial)



    
