import ytdl


class Song():

    def __init__(self):
        self.url = None
        self.playlist_url = None
        self.title = None
        self.file_path = None

    @classmethod
    def create_from_youtube_data(data, playlistUrl):
        song = Song()
        song.url = data['url']
        song.playlist_url = playlistUrl
        song.title = data['title']
        song.file_path = ytdl.instance.prepare_filename(data)

        return song


    