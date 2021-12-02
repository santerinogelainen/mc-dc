from discord.ext import commands

from cogs.music import Music

class MCDCBot(commands.Bot):

    def __init__(self):
        print("Bot is running!")
        super().__init__(commands.when_mentioned_or("!"))
        self.add_cog(Music(self))