from ftplib import FTP
from pytube import YouTube, Channel
import os


ftp_client = FTP("ip address")
channels = []

ftp_client.login("username", "password")

with open("channels.txt") as file:
    for line in file:
        channels.append(line)

def latest_video(channel_url):
    c = Channel(channel_url)
    for video in c.video_urls[:1]:
        return video

def upload_file(file, youtuber, title):
    ftp_client.cwd("/media/Youtube/")
    if youtuber in ftp_client.nlst():
        ftp_client.cwd("/media/Youtube/%s" % youtuber)
    else:
        ftp_client.mkd(youtuber)
        ftp_client.cwd("/media/Youtube/%s" % youtuber)
    with open(file, "rb") as f:
       ftp_client.storbinary("STOR %s" % title + ".mp4", f)

def download_video(link):
    url = YouTube(link)
    video = url.streams.get_highest_resolution()
    video.download("", "video.mp4")
    upload_file("video.mp4", url.author, url.title)
    os.remove("video.mp4")

for channel in channels:
    latest = latest_video(channel)
    print(latest)
    print(channel)
    download_video(latest)

print("Upload Success!")

ftp_client.quit()
