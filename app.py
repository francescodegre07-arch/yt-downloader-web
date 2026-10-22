import streamlit as st
import yt_dlp
import os

st.title("YouTube Downloader")

video_url = st.text_input("Inserisci l'URL del video di YouTube:")
formato = st.selectbox(
    "Scegli il formato da scaricare",
    ["1 - Video + Audio (MP4)", "2 - Solo Video (MP4)", "3 - Solo Audio (MP3)"]
)

if st.button("Avvia Download"):
    if video_url:
        with st.spinner("Scaricamento ed elaborazione in corso sul server..."):
            modalita = formato[0]
            
            # Parametri aggiornati per aggirare il blocco 403 di YouTube
            ydl_opts = {
                'outtmpl': 'download_temporaneo.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'extractor_args': {'youtube': ['player_client=ios,android,web']},
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
                }
            }
            
            if modalita == "3":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
                estensione = 'mp3'
            elif modalita == "2":
                ydl_opts['format'] = 'bestvideo/best'
                ydl_opts['merge_output_format'] = 'mp4'
                estensione = 'mp4'
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
                estensione = 'mp4'

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    nome_file_finale = f"download_temporaneo.{estensione}"
                
                with open(nome_file_finale, "rb") as file:
                    st.download_button(
                        label="✅ Clicca qui per scaricare il file",
                        data=file,
                        file_name=f"{info.get('title', 'video')}.{estensione}",
                        mime=f"video/{estensione}" if estensione == 'mp4' else "audio/mpeg"
                    )
                
                os.remove(nome_file_finale)
                
            except Exception as e:
                st.error(f"Si è verificato un errore: {e}")
    else:
        st.warning("Inserisci un URL valido prima di procedere.")
