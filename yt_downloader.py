import yt_dlp

url = input("Enter YouTube URL: ")
with yt_dlp.YoutubeDL({'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}) as ydl:
    ydl.download([url])