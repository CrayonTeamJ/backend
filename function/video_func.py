from moviepy.editor import *

def mp4_to_mp3(file_path):

    mp4_file = file_path

    mp3_file = "./data/audio.mp3"

    videoClip = VideoFileClip(mp4_file)

    audioclip = videoClip.audio

    audioclip.write_audiofile(mp3_file)

    audioclip.close()

    videoClip.close()
    pass