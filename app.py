import streamlit as st
import yt_dlp
import os

st.title("YouTube Downloader Avanzato")

video_url = st.text_input("Inserisci l'URL del video di YouTube:")
formato = st.selectbox(
    "Scegli il formato da scaricare",
    ["1 - Video + Audio (MP4)", "2 - Solo Video (MP4)", "3 - Solo Audio (MP3)"]
)

if st.button("Avvia Download"):
    if video_url:
        with st.spinner("Scaricamento ed elaborazione in corso sul server..."):
            modalita = formato[0]
            
            ydl_opts = {
                'outtmpl': 'download_temporaneo.%(ext)s',
                'noplaylist': True,
                'quiet': True
            }
            
            if modalita == "3":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
            elif modalita == "2":
                ydl_opts['format'] = 'bestvideo[ext=mp4]/best'
            else:
                ydl_opts['format'] = 'best[ext=mp4]/best'

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    estensione = 'mp3' if modalita == "3" else 'mp4'
                    nome_file_finale = f"download_temporaneo.{estensione}"
                
                # Prepara il file elaborato per il download verso l'utente
                with open(nome_file_finale, "rb") as file:
                    st.download_button(
                        label="✅ Clicca qui per salvare il file sul dispositivo",
                        data=file,
                        file_name=f"{info.get('title', 'video')}.{estensione}",
                        mime=f"video/{estensione}" if estensione == 'mp4' else "audio/mpeg"
                    )
                
                # Pulizia del file dal server dopo aver preparato il bottone
                os.remove(nome_file_finale)
                
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")
    else:
        st.warning("Inserisci un URL valido prima di procedere.")