import ytmusicapi
import yt_dlp
from ytmusicapi import YTMusic
import os
import argparse

par = argparse.ArgumentParser(prog='ytm-dlp', description="Download musics from YouTube easily.")
spar = par.add_subparsers(dest="command", help="All available commands")
pl_par = spar.add_parser('playlist', help='Download a playlist')
pl_par.add_argument('playlist_id', help='The id of the playlist (usually a hash at the end of the url.)')
son = spar.add_parser('song', help='Download one song')
son.add_argument('song_id', help='The id of the song (usually a hash at the end of the url.)')
args = par.parse_args()

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



def songs(pl):
    ## TODO // finish this function

    ytdll = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'keepvideo': False,
        'quiet': True,
    }

    url = f'{burl}{pl}'

    plis = ytm.get_song(pl)
    det = plis['videoDetails']

    title = det['title']
    id = det['videoId']

    if os.path.exists(f'{title}.mp3'):
        print("This song already exists.")
        raise SystemExit()
    else:
            with yt_dlp.YoutubeDL(ytdll) as ydl:
                print(f'Downloading {title}')
                ydl.download([url])
                print(f' Downloaded {title}')

            if os.path.exists(f'{title}.mp4'):
                os.remove(f'{title}.mp4')

    
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
    if args.command == 'playlist':
        try:
          pls(args.playlist_id)
        except KeyError as err:
            print("Can't download a playlist from that id.")
            print("Unable to find songs from that playlist id.")
            raise SystemExit()
    elif args.command == 'song':
        try:
          songs(args.song_id)
        except KeyError as err:
            print("Unable to find a song from that id.")
            raise SystemExit()
    else:
        print("No correct argument found, type -h to list commands.")
except KeyboardInterrupt:
   raise SystemExit()
