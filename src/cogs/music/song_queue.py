import asyncio
import queue
from song import Song
import ytdl


class SongQueue(queue.Queue):

    async def load_songs_from_youtube_url(self, url, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.instance.extract_info(url, download=True))

        if 'entries' in data:
            # loop playlist and take add every song
            for entry in data['entries']:
                self.add(Song.create_from_youtube_data(entry, url))

        else:
            self.add(Song.create_from_youtube_data(data))

