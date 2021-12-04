import threading
import queue
from src.cogs.music.song import Song
from src.cogs.music.ytdl import ytdl

class YTDLDownloader(threading.Thread):

    def __init__(self):
        super().__init__(name="Song downloader")
        self.queue = queue.Queue()
        self.daemon = True

    def queue_download(self, song: Song):
        self.queue.put(song)

        if not self.is_alive():
            self.start()

    def __download_next(self):
        song = self.queue.get()
        data = ytdl.extract_info(song.url, download=True)
        song.file_path = ytdl.prepare_filename(data)
        song.downloaded = True

        if self.queue.not_empty:
            self.__download_next()

    def run(self):
        self.__download_next()
        