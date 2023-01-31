import pathlib
from pathlib import Path
from pytube import Playlist
from moviepy.editor import *
import tqdm
from os import listdir
from os.path import isfile, join


new_folder = pathlib.Path().resolve() / Path("dir")
playlist_link = "YOUR_YOUTUBE_PLAYLIST_FULL_URL"

p = Playlist(playlist_link)

print(f"Creating dictionary {new_folder.name}")
if not os.path.exists(new_folder):
    os.mkdir(new_folder)

print(f"Downloading: {p.title}")
for video in tqdm.tqdm(p.videos):
    video.streams.filter(file_extension="mp4").desc().first().download(output_path=new_folder)

print(f"Converting mp4 files to mp3 audio files")
for mp4 in map(Path, listdir(new_folder)):
    if isfile(join(new_folder, mp4)) and mp4.name.endswith("mp4"):
        with AudioFileClip(str(new_folder / mp4)) as f:
            f.write_audiofile(new_folder / mp4.with_suffix(".mp3"))
        os.remove(new_folder / mp4)
