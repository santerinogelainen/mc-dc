from discord.ext import commands
from src.settings import MCDCSettings

from src.cogs.music.music_cog import Music

class MCDCBot(commands.Bot):

    def __init__(self, settings: MCDCSettings):
        self.settings = settings

        print("Bot is running!")
        super().__init__(commands.when_mentioned_or("!"))
        self.add_cog(Music(self, settings.stream_music))