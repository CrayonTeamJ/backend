from __future__ import unicode_literals
import youtube_dl
from pytube import YouTube
from moviepy.editor import *
import ssl
from pytube.cli import on_progress
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context



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
    try:
        yt = YouTube(youtube_url)
    except:
        return False
    
    title = yt.title
    length = yt.length
    video_name = "./data/video" + str(file_number) + ".mp4"
    after_cutting_name = "./data/video" + str(file_number) + "-0.mp4"
    yt.streams.filter(res="720p" ,file_extension="mp4").order_by('resolution').desc().first().download('./data', filename= 'video' + str(file_number))
    ffmpeg_extract_subclip(video_name, 0, length, targetname= after_cutting_name)

    pass


