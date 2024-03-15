import os
from pytube import Playlist
from pytube import YouTube
from tqdm import tqdm
import re

def download_playlist_videos(playlist_link):
    playlist = Playlist(playlist_link)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    playlist._video_urls = [f'https://www.youtube.com{url.group(1)}' for url in playlist._video_regex.finditer(playlist.html)]
    
    playlist_title = playlist.title
    os.makedirs(playlist_title, exist_ok=True)

    counter = 0

    for video_url in tqdm(playlist._video_urls, desc="Downloading"):
        video = YouTube(video_url)
        title = video.title
        stream = video.streams.filter(res="720p").first()
        # print(video.streams.filter(res="720p"))
        if stream:
            stream.download(output_path=playlist_title, filename=f"video_{counter}.mp4")
            print(f"Downloaded: {title}")
        else:
            print(f"Skipping {title} - 720p version not available")
        counter = counter + 1

playlist_link = input("Enter the link of the YouTube playlist: ")

print("Downloading playlist...")

download_playlist_videos(playlist_link)
