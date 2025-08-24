import ytmusicapi
import yt_dlp
from ytmusicapi import YTMusic
import os

if not os.path.exists('music'):
    os.mkdir('music', 0o755)

ytdls = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join('music', '%(title)s.%(ext)s'),
    'keepvideo': False,
}

burl = 'https://music.youtube.com/watch?v='

ytm = YTMusic()

def pls(pl):
    plis = ytm.get_playlist(pl)
    tracks = plis['tracks']
    for track in tracks:
        title = track['title']
        id = track['videoId']
        url = f'{burl}{id}'
        if os.path.exists(f'music/{title}.mp3'):
            pass
            print(f"{title}.mp3 already exists.")
        else:
            with yt_dlp.YoutubeDL(ytdls) as ydl:
                print(f'Downloading {title}')
                ydl.download([url])
                print(f'Downloaded {title}')

            if os.path.exists(f'music/{title}.mp4'):
                os.remove(f'music/{title}.mp4')


pls('PLoIoZsCilFJINI0N41NS5xnUAU1BVdfw6')
