
import pafy, os, platform
from moviepy.editor import *

def mostra_nome_programma():
    print(r"""

 -------------------------------------- × YOUTUBE × -----------------------------------------
                                                                               
  #####      ####    ##      ##   ###   ##  ##      ####    ######  #####    ######  #####
  ######    ##  ##   ##      ##  ##  #  ##  ##     ##  ##   ##  ##  ######   ##      ##  ##
  ##  ###  ##    ##  ##      ##  ##  #  ##  ##    ##    ##  ##  ##  ##  ###  ##      ##   ##
  ##   ##  ##    ##  ##      ##  ##  #  ##  ##    ##    ##  ######  ##   ##  ####    ######
  ##   ##  ##    ##  ##  ##  ##  ##  #  ##  ##    ##    ##  ##  ##  ##   ##  ##      ## ##
  ##  ##    ##  ##   ##  ##  ##  ##  #  ##  ##     ##  ##   ##  ##  ##  ##   ##      ##  ##
  #####      ####     ###  ###   ##  ####   #####   ####    ##  ##  #####    ######  ##   ##
  
 ---------------------------------- ( NO MORE VIRUSES ) -------------------------------------

      Digitare il comando 'help' per ottenere informazioni sul corretto funzionamento
  del programma. Tutta la documentazione: https://github.com/Darkenar94/youtube_downloader

 --------------------------------------------------------------------------------------------""")

def mostra_separatore():
    print(" --------------------------------------------------------------------------------------------")

def mostra_spiegazione():
    print("""            Breve spiegazione sull'utilizzo del programma youtube_downloader:
 --------------------------------------------------------------------------------------------
      Copiare l'url di un video su youtube incollare quindi il testo copiato nella
       finestra del programma youtube_downloader e premere invio si riceveranno
      successivamente le varie opzioni disponibili ora digitare 1 e premere invio
          dopo una conversione del file in formato mp3 questo verrà scaricato
                         in breve tempo e in totale sicurezza.
 --------------------------------------------------------------------------------------------
    Per segnalare bug o consigliare possibili miglioramenti: darkenarnovequattro@libero.it
 --------------------------------------------------------------------------------------------""")

def url_esistente(possibile_url):
    try:
        info_video = pafy.new(possibile_url)
    except:
        mostra_messaggio("  Informazione rifiutata, riprovare.")
    else:
        return True

def mostra_messaggio(frase):
    print(frase)
    mostra_separatore()

def operazione_effettuata(frase, percorso):
    mostra_separatore()
    print(frase + percorso)
    mostra_separatore()

def ottieni_info_video(possibile_url):
    info_video = pafy.new(possibile_url)
    return info_video

def mostra_opzioni():
    print("""  Opzioni disponibili:
 --------------------------------------------------------------------------------------------
  1. Conversione (file video > file audio) + avvio download. [best quality]
  2. Eseguire download file video integrale. [best quality]
  3. Download file video. (no audio) [best quality]
  4. Scegliere manualmente uno stream. (sconsigliato)
  5. Chiudere il programma.
 --------------------------------------------------------------------------------------------""")

def gestisci_audio(percorso, file, file_migliore):
    if file_migliore.mediatype == "audio":
        file_audio = file_migliore.title + ".mp3"
        if not file_audio in os.listdir(percorso):
            converti(percorso, file_migliore)
        else:
            os.remove(os.path.join(percorso, file))

def gestione_file(percorso, file_migliore):
    file = file_migliore.title + "." + file_migliore.extension
    if not file in os.listdir(percorso):
        mostra_messaggio("  Operazione download avviata..")
        file_migliore.download(filepath=percorso)
        gestisci_audio(percorso, file, file_migliore)
        operazione_effettuata("  Operazione effettuata. Posizione file: ", percorso)
    else:
        mostra_messaggio("  File già scaricato, impossibile eseguire il download.")
        if file_migliore.mediatype == "audio":
            converti(percorso, file_migliore)
            operazione_effettuata("  Operazione effettuata. Posizione file: ", percorso)

def scarica_file(info_video, metodo):
    percorso = os.getenv("USERPROFILE") + "\\Downloads"
    file_migliore = eval("info_video" + metodo)
    if not file_migliore == None:
        gestione_file(percorso, file_migliore)
    else:
        mostra_messaggio("  Download non disponibile.")

def ottieni_streams(info_video):
    streams = []
    mostra_messaggio("         Digitare il numero corrispondente allo stream che si preferisce utilizzare.")
    mostra_messaggio("            Legenda: [normal=audio+video] [video=solo_video] [audio=solo_audio]")
    for i in range(len(info_video.allstreams)):
        streams.append(str(i))
        stream = info_video.allstreams[i]
        if stream.mediatype != "audio":
            print("  " + str(i) + ". tipo: " + stream.mediatype + " titolo: " + stream.title[0:5] + "[...] estensione: "
                  + stream.extension + " risoluzione: " + stream.resolution)
            continue
        print("  " + str(i) + ". tipo: " + stream.mediatype + " titolo: " + stream.title[0:5] + "[...] estensione: "
              + stream.extension + " bitrate: " + stream.bitrate)
    print("  " + str(i + 1) + ". Annulla operazione.")
    mostra_separatore()
    return streams

def converti(percorso, stream):
    vecchia_estensione = "." + stream.extension
    audio = AudioFileClip(percorso + "\\" + stream.title + vecchia_estensione)
    mostra_separatore()
    print("  Conversione file in corso..")
    audio.write_audiofile(percorso + "\\" + stream.title + ".mp3", logger=None)
    os.remove(os.path.join(percorso, stream.title + vecchia_estensione))

def scarica_stream_specifico(info_video):
    streams = ottieni_streams(info_video)
    percorso = os.getenv("USERPROFILE") + "\\Downloads"
    in_esecuzione = True
    while in_esecuzione:
        numero = input("  > ")
        mostra_separatore()
        if numero == str(len(streams)):
            in_esecuzione = False
        elif numero in streams:
            stream = info_video.allstreams[int(numero)]
            gestione_file(percorso, stream)
            in_esecuzione = False
        else:
            mostra_messaggio("  Informazione rifiutata, riprovare.")
            
def termina_programma():
    quit()

def richiesta_proseguimento():
    in_esecuzione = True
    while in_esecuzione:
        risposta = input("  Eseguire altre operazioni sulla traccia corrente? [S/n] ").lower()
        mostra_separatore()
        if risposta == "s":
            mostra_opzioni()
            return True
        elif risposta == "n":
            mostra_messaggio("  Digitare 'help' o inserire una Url valida.")
            return False
        mostra_messaggio("  Informazione rifiutata, riprovare.")

def avvio_downloader(possibile_url):
    mostra_messaggio(" "*71 + ">> URL CONVALIDATA.")
    info_video = ottieni_info_video(possibile_url)
    mostra_opzioni()
    in_esecuzione = True
    while in_esecuzione:
        opzione = input("  > ")
        mostra_separatore()
        if opzione == "1":
            scarica_file(info_video, ".getbestaudio()")
        elif opzione == "2":
            scarica_file(info_video, ".getbest()")
        elif opzione == "3":
            scarica_file(info_video, ".getbestvideo()")
        elif opzione == "4":
            scarica_stream_specifico(info_video)
        elif opzione == "5":
            termina_programma()
        else:
            mostra_messaggio("  Informazione rifiutata, riprovare.")
            continue
        in_esecuzione = richiesta_proseguimento()

def main():
    mostra_nome_programma()
    in_esecuzione = True
    while in_esecuzione:
        info_ricevuta = input("  > ")
        mostra_separatore()
        if info_ricevuta.lower() == "help":
            mostra_spiegazione()  
        elif url_esistente(info_ricevuta):
            avvio_downloader(info_ricevuta)

if __name__ == "__main__":
    main()
