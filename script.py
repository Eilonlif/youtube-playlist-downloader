import argparse
import pathlib
from pathlib import Path
from pytube import Playlist
from moviepy.editor import *
import tqdm
from os import listdir
from os.path import isfile, join

DEBUG = 1

def debug(str):
    if DEBUG:
        print(str)

playlist_link = ""

parser = argparse.ArgumentParser(description='Download YouTube files')
parser.add_argument('-u', '--url', const=playlist_link, default="YOUR_YOUTUBE_PLAYLIST_FULL_URL", nargs="?", required=False, help="YouTube Playlist URL")
args = parser.parse_args()
playlist_link = args.url

new_folder = pathlib.Path().resolve() / Path("dir")

p = Playlist(playlist_link)
try:
    if p.length == 0:
        print("Playlist length is 0")
        exit()
except:
    print(f"Unable to get playlist from URL: {playlist_link}")
    exit()

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
