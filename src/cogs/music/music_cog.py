
import discord
import asyncio
from src.cogs.music.ytdl_source import YTDLSource
from src.cogs.music.song_queue import SongQueue

from discord.ext import commands

class Music(commands.Cog):

    def __init__(self, bot, stream):
        self.bot = bot
        self.queue = SongQueue(stream)

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel"""

        if channel is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel

        if channel is None:
            raise commands.CommandError("User not connected to a voice channel or channel not given!")

        print("Joined voice channel: " + channel.name)

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        
    @commands.command()
    async def leave(self, ctx):
        """Leaves a voice channel"""

        if ctx.voice_client is not None:
            print("Left voice channel.")
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url = None):
        """Plays a song from youtube"""

        await self.ensure_voice(ctx)

        if url is None:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                return
            await ctx.send("Enter the YouTube URL or search term after !play")
            return

        async with ctx.typing():
            songs = await self.queue.add(url, self.bot.loop)

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
            else:
                for song in songs:
                    await ctx.send("Added [{}] to the queue!".format(song.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops the bot from voice"""

        await self.clear_queue(ctx)
        ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        """Pauses the bot from voice"""

        await ctx.voice_client.pause()
        
    @commands.command()
    async def skip(self, ctx):
        """Skips a song"""

        ctx.voice_client.stop()

    @commands.command("queue")
    async def show_queue(self, ctx):
        """Displays the current queue"""
        if not self.queue.not_empty():
            await ctx.send("No songs in queue!")
            return
        i = 1
        for song in self.queue.get_songs():
            await ctx.send("{}. {}".format(i, song.title))
            i += 1

    @commands.command("clear-queue")
    async def clear_queue(self, ctx):
        """Clears the queue"""
        self.queue.clear()
        await ctx.send("Queue cleared!")

    async def ensure_voice(self, ctx):
        """Ensures that the bot is connected to a voice channel before playing music"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

    async def play_next(self, ctx):
        """Plays the next song in queue"""
        if not self.queue.not_empty():
            await ctx.send('No more songs in queue!')
            return

        async with ctx.typing():
            song = await self.queue.get()
            source = YTDLSource(song)
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

        await ctx.send('Now playing: [{}]'.format(song.title))