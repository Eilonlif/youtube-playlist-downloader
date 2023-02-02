import argparse
import pathlib
from pathlib import Path
from pytube import Playlist
from moviepy.editor import *
import tqdm
from os import listdir
from os.path import isfile


playlist_link = "YOUR_YOUTUBE_PLAYLIST_FULL_URL"
folder_name = "dir"

parser = argparse.ArgumentParser(description='Download YouTube files')
parser.add_argument('-u', '--url', const=playlist_link, default="YOUR_YOUTUBE_PLAYLIST_FULL_URL", nargs="?", required=False, help="YouTube Playlist URL")
parser.add_argument('-f', '--folder-name', const=folder_name, default="dir", nargs="?", required=False, help="New folder name")
args = parser.parse_args()
playlist_link = args.url

new_folder = pathlib.Path().resolve() / Path(folder_name)
p = Playlist(playlist_link)

if not p:
    print("Playlist is empty or the link is wrong")
    exit()

if not os.path.exists(new_folder):
    print(f"Creating new dictionary {new_folder.name}")
    os.mkdir(new_folder)

print(f"Downloading: {p.title}")
for video in tqdm.tqdm(p.videos):
    video.streams.filter(file_extension="mp4").desc().first().download(output_path=new_folder)

print(f"Converting mp4 files to mp3 audio files")
for mp4 in map(Path, listdir(new_folder)):
    new_folder_mp4 = new_folder / mp4
    if isfile(new_folder_mp4) and mp4.name.endswith(".mp4"):
        with AudioFileClip(str(new_folder_mp4)) as f:
            f.write_audiofile(new_folder_mp4.with_suffix(".mp3"))
        os.remove(new_folder_mp4)
