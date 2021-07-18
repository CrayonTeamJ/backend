from __future__ import unicode_literals
import youtube_dl
from moviepy.editor import *



def mp4_to_mp3(file_path, file_number):
    mp4_file = file_path
    mp3_file = "./data/audio"+ str(file_number) + ".mp3"
    videoClip = VideoFileClip(mp4_file)
    audioclip = videoClip.audio
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoClip.close()
    pass

def download_audio(youtube_url, file_number):
    ydl_opts = {
        'nocheckcertificate': True,
      	'outtmpl': './data/audio' + str(file_number) + '.mp3',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
        pass

def download_video(youtube_url, file_number):
    ydl_opts = {
        'nocheckcertificate': True,
        'videoformat' : "mp4",
      	'outtmpl': './data/video' + str(file_number) + '.mp4',
        'format': 'bestvideo/best[height<=720]',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
        pass

