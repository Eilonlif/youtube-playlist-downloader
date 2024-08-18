import argparse
import pathlib
from pathlib import Path
from pytube import Playlist
from pytube import YouTube
from pydub import AudioSegment
from moviepy.editor import *
import tqdm
from os import listdir
from os.path import isfile
import os
import sys

class Convertor:
    def __init__(self,
                 playlist_link,
                 folder_name = "dir"):
        self.playlist_link = playlist_link
        self.output_path = pathlib.Path().resolve() / Path(folder_name)
        self.playlist = Playlist(self.playlist_link)
        if not self.playlist:
            print("Playlist is empty or the link is wrong")
            exit()

        if not os.path.exists(self.output_path):
            print(f"Creating new dictionary {self.output_path.name}")
            os.mkdir(self.output_path)

    def _download_playlist(self):
        print(f"[+] Downloading: {self.playlist.title}")
        
        for video_url in tqdm.tqdm(self.playlist.video_urls):
            self.download_video_as_mp3(video_url, self.output_path)


        # for video in tqdm.tqdm(self.playlist.videos):
        #     video.streams.filter(file_extension="mp4").desc().first().download(output_path=output_path)
    
    def download_video_as_mp3(self, video_url, output_path):
        try:
            yt = YouTube(video_url)
            # Download the highest resolution audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file = audio_stream.download(output_path=output_path)
            
            # Convert to MP3
            base, ext = os.path.splitext(audio_file)
            mp3_file = base + '.mp3'
            AudioSegment.from_file(audio_file).export(mp3_file, format='mp3')
            
            # Remove the original file
            os.remove(audio_file)
            print(f"Downloaded and converted: {yt.title}")
        except Exception as e:
            print(f"Failed to download {video_url}: {str(e)}")

    def process(self):
        print("[+] Starting converstion process")
        self._download_playlist()
        # self._convert_mp4_to_mp3()
        print("[+] Done!")

def main(args):
    for playlist_link in args:
        convertor = Convertor(playlist_link)
        convertor.process()


if __name__ == "__main__":
    args = None
    if len(sys.argv) < 2:
        args = input("[!] please enter a vaild youtube playlist URL\n> ").split()
    else:
        args = sys.argv[1:]
    main(args)




"""
https://www.youtube.com/watch?v=anTv1H2oYdU&list=PLQOJuTv0vLBDiNHIgbEj0dUC64_WOkcqB
"""