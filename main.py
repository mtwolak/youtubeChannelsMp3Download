import json
import os
import subprocess

from googleapiclient.discovery import build


def download_mp3s_from_channel_after_date(music_info):
    published_after = get_date_from_settings()
    videos_per_page = get_videos_per_page(music_info[0], published_after)
    download_videos_from_page(videos_per_page, music_info[1])
    next_page_token = get_next_page_token(videos_per_page)
    while next_page_token:
        download_videos_from_page(videos_per_page, music_info[1])
        videos_per_page = get_videos_per_page(music_info[0], published_after, next_page_token)
        next_page_token = get_next_page_token(videos_per_page)


def get_videos_per_page(channel_id, published_after, page_token=None):
    return youtubeClient.search().list(part='id,snippet', channelId=channel_id,
                                       publishedAfter=published_after, pageToken=page_token).execute()


def download_videos_from_page(videos_per_page, target_folder_for_save):
    size = len(videos_per_page["items"])
    for itemId in range(0, size):
        video_name = videos_per_page["items"][itemId]['snippet']['title']
        youtube_link = "http://youtube.com/watch?v=" + videos_per_page["items"][itemId]["id"]["videoId"]
        download_video(youtube_link, video_name, target_folder_for_save)


def download_video(youtube_link, video_name, target_folder_for_save):
    if not os.path.exists(target_folder_for_save):
        os.makedirs(target_folder_for_save)
    if not os.path.isfile(target_folder_for_save + "/" + video_name + ".mp3"):
        subprocess.call("youtube-dl " + youtube_link, shell=True)
        subprocess.call("mv *.mp3 '" + target_folder_for_save + "'/", shell=True)


def get_next_page_token(videos_per_page):
    if "nextPageToken" in videos_per_page:
        next_page_token = videos_per_page["nextPageToken"]
    else:
        next_page_token = False
    return next_page_token


def get_channel_id_by_name(channel_name, youtube_client):
    youtube_channels_by_name = youtube_client.channels().list(part="id", forUsername=channel_name).execute()
    if len(youtube_channels_by_name["items"]) > 0:
        return youtube_channels_by_name["items"][0]["id"]
    else:
        print("Channel " + channel_name + " not found")
        return ""


def create_music_info_for_download(channel_from_music_will_be_downloaded):
    youtube_music_info = []
    for item in channel_from_music_will_be_downloaded:
        if "id" in item:
            youtube_music_info.append([item["id"], item['folderName']])
        elif "name" in item:
            channel_id = get_channel_id_by_name(item["name"], youtubeClient)
            youtube_music_info.append([channel_id, item['folderName']])
    return youtube_music_info


def get_settings():
    with open("settings.json") as file:
        return json.load(file)


def get_date_from_settings():
    return settings["settings"]["startDate"] + "T00:00:00Z"


def get_channel_ids_from_file():
    return create_music_info_for_download(settings["channels"])


settings = get_settings()
youtubeClient = build("youtube", "v3", developerKey=settings["settings"]["developerKey"])
for music_info in get_channel_ids_from_file():
    download_mp3s_from_channel_after_date(music_info)
