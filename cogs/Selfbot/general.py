'''
MIT License

Copyright (c) 2024 BÖZ @535i

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 
'''



import discord
from discord.ext import commands
from config import ownerid, del_messages
import sys, os
from rich import print as rprint
import platform
import psutil
import datetime

def bot_owner_only():
    def is_owner(ctx: commands.Context):
        return ctx.author.id ==  ownerid
    return commands.check(is_owner)

def delete_messages():
    if del_messages is not None:
        return del_messages
    return None


class General(commands.Cog):
    """A class with General commands."""

    def __init__(self, client: commands.Bot):
        self.client = client


    def clear_screen(self):
        os.system('cls' if os.name == "nt" else 'clear')
        rprint("[green] Cleared the console.")


    @commands.command(aliases=["up"], brief="Shows uptime")
    @bot_owner_only()
    async def uptime(self, ctx):
        """
        Shows how long the selfbot is running 
        """

        await ctx.message.delete()
        time = f"<t:{self.client.runtime}:f>"
        return await ctx.send(time, delete_after=delete_messages())
    
    @commands.command(breif="Exit")
    @bot_owner_only()
    async def exit(self, ctx):
        """
        Exits the program
        """

        await ctx.message.delete()
        await ctx.send("Shutting down..")
        sys.exit(0)

    @commands.command(brief="Bump a server")
    @bot_owner_only()
    async def bump(self, ctx):
        """
        Bump a channel without using a slash command.
        Just type the command inside the channel
        """

        await ctx.message.delete()
        channel = self.client.get_channel(ctx.channel.id)
        async for command in channel.slash_commands():
            if command.id == 947088344167366698:
                await command(channel)

    @commands.command(aliases=["clc"], brief="Clear the terminal")
    @bot_owner_only()
    async def clear_console(self, ctx):
        """
        Clears the terminal
        """

        await ctx.message.delete()
        await ctx.send("Cleared the console :white_check_mark:", delete_after=delete_messages())
        self.clear_screen()

    @commands.command(aliases=["status", "chs"], brief="Change your status")
    @bot_owner_only()
    async def change_status(self, ctx, status:str, custom_status: str = None):
        """
        Change your status

        Parameters
        -----------
        status: str
            Specify your status [online, offline, idle, dnd, invisible]
        custom_status: str
            Custom status displayed as your activity [Playing...]
        """

        await ctx.message.delete()
        if status is None:
            return await ctx.send("Specify your status.\nChoose between [online, offline, idle, dnd, invisible]")
        
        status_list = [
            "online",
            "offline",
            "idle",
            "dnd",
            "invisible"        
            ]
        
        if status in status_list:
            if custom_status is None:
                await self.client.change_presence(status=discord.Status(status))
            else: 
                await self.client.change_presence(activity=discord.Game(custom_status))

    @commands.command(brief="Shows stats")
    @bot_owner_only()
    async def stats(self, ctx):
        """
        Shows statistics about the selfbot, including some more information
        """

        await ctx.message.delete()
        x = "\n"
        pyVersion = platform.python_version()
        guilds = len(self.client.guilds)
        all_members = len(self.client.users)
        dpy_self_version = discord.__version__
        uptime = datetime.datetime.fromtimestamp(self.client.runtime)
        content = f"Python Version: {pyVersion}{x}Guilds: {guilds}{x}All Members: {all_members}{x}Discord.py-self Version: {dpy_self_version}{x}CPU Usage: {psutil.cpu_percent()}%{x}RAM Usage: {psutil.virtual_memory().percent}%{x}Running since: {uptime}"

        await ctx.send(f" ## Statistics for **{self.client.user}**{x}```css{x}{content}{x}```", delete_after=delete_messages())


async def setup(client: commands.Bot):
    await client.add_cog(General(client))

