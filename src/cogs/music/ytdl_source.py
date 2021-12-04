import discord

from src.cogs.music.song import Song

ffmpeg_executable = "C:/ffmpeg/ffmpeg.exe"
ffmpeg_options = {
    'options': '-vn'
}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, song: Song, volume=0.5):
        self.song = song
        source = discord.FFmpegPCMAudio(song.file_path, executable=ffmpeg_executable, **ffmpeg_options)
        super().__init__(source, volume)
