import pathlib
from pathlib import Path
from pytube import Playlist
from moviepy.editor import *
import tqdm
from os import listdir
from os.path import isfile, join


current_dir = pathlib.Path().resolve()
new_folder = current_dir / Path("dir")
playlist_link = "YOUR_YOUTUBE_PLAYLIST_FULL_URL"

p = Playlist(playlist_link)
print(f"Downloading: {p.title}")
for video in tqdm.tqdm(p.videos):
    video.streams.filter(file_extension="mp4").desc().first().download()

print(f"Creating dictionary {new_folder.name}")
if not os.path.exists(new_folder):
    os.mkdir(new_folder)

print(f"Converting mp4 files to mp3 audio files")
for file in listdir(current_dir):
    mp4 = Path(str(file))
    if isfile(join(current_dir, mp4)) and mp4.name.endswith("mp4"):
        f = AudioFileClip(str(current_dir / mp4))
        f.write_audiofile(new_folder / Path(mp4.with_suffix(".mp3")))
        f.close()
        os.remove(current_dir / mp4)
