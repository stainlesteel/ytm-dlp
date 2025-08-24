import ytmusicapi
import yt_dlp
from ytmusicapi import YTMusic
import os


ytdls = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join('music', '%(title)s.%(ext)s'),
    'keepvideo': False,
    'quiet': True,
}

burl = 'https://music.youtube.com/watch?v='

ytm = YTMusic()

def pls(pl):
    answer = str(input("""A new 'music' folder will be created and all\navailable music will be downloaded there.\nContinue? [Y/n]"""))
                 
    if answer.lower() == 'n':
        raise SystemExit()

    if not os.path.exists('music'):
        os.mkdir('music', 0o755)

    plis = ytm.get_playlist(pl)
    tracks = plis['tracks']

    lens = len(tracks)

    print(f'{lens} songs found.')
    num = 0
    for track in tracks:
        num += 1

        title = track['title']
        id = track['videoId']
        url = f'{burl}{id}'
        if os.path.exists(f'music/{title}.mp3'):
            pass
            print(f"{title}.mp3 already exists.")
        else:
            with yt_dlp.YoutubeDL(ytdls) as ydl:
                print(f'[{num}/{lens}] Downloading {title}')
                ydl.download([url])
                print(f'[{num}/{lens}] Downloaded {title}')

            if os.path.exists(f'music/{title}.mp4'):
                os.remove(f'music/{title}.mp4')

try:
   pls('PLoIoZsCilFJINI0N41NS5xnUAU1BVdfw6')
except KeyboardInterrupt:
   raise SystemExit()
