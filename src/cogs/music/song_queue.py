import asyncio
import queue
import time

from src.cogs.music.song import Song
from src.cogs.music.ytdl import ytdl
from src.cogs.music.ytdl_downloader import YTDLDownloader


class SongQueue():

    def __init__(self, stream):
        self.queue = queue.Queue()
        self.last_song: Song = None
        self.downloader = YTDLDownloader()
        self.stream = stream

    async def add(self, input, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(input, download=False))
        songs = []

        if 'entries' in data:
            # loop playlist and take add every song
            for entry in data['entries']:
                song = self.add_song_from_youtube_data(input, entry)
                songs.append(song)

        else:
            song = self.add_song_from_youtube_data(input, data)
            songs.append(song)
            
        return songs

    async def get(self):
        self.last_song = self.queue.get()
        await self.ensure_downloaded(self.last_song)
        return self.last_song

    def clear(self):
        with self.queue.mutex:
            self.queue.queue.clear()

    def get_songs(self):
        with self.queue.mutex:
            return self.queue.queue

    def not_empty(self):
        return self.queue.qsize() > 0

    def add_song_from_youtube_data(self, input, data):
        song = Song()
        song.input = input
        song.url = "https://www.youtube.com/watch?v=" + data["id"]
        song.raw_url = data['url']
        song.title = data['title']

        if self.stream:
            song.file_path = data['url']
            song.downloaded = True
        else:
            self.downloader.queue_download(song)

        self.queue.put(song)
        return song

    async def ensure_downloaded(self, song: Song):
        if not song.downloaded:
            print("Song [" + song.title + "] not yet downloaded... Waiting for download to finish.")
            await asyncio.sleep(3)
            await self.ensure_downloaded(song)


