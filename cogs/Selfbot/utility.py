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
from rich import print as rprint
import asyncio

def bot_owner_only():
    def is_owner(ctx: commands.Context):
        return ctx.author.id == ownerid
    return commands.check(is_owner)

def delete_messages():
    if del_messages is not None:
        return del_messages
    return None


class Utility(commands.Cog):
    """A class with Utility commands."""

    __slots__ = ('client')
    
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["cl"], brief="Clear your messages")
    @bot_owner_only()
    async def clear(self, ctx, amount:int=None, channelid:int=None):
        """
        Clear your messages

        Parameters
        -----------
        amount: int
            The amount of messages to delete
        channelid: int
            the channel ID [guild or dm channel]
            If None the channel will be the channel where you invoke the command
        """

        await ctx.message.delete()
        if amount is None:
            return await ctx.send("Specify the amount of messages to delete.")
        elif channelid is None:
            channelid = ctx.channel.id
        channel = self.client.get_channel(channelid)
        async for message in channel.history(limit=amount):
            if message.author == ctx.author:
                if message.type == discord.MessageType.default or message.type == discord.MessageType.reply:
                    await message.delete()
                    await asyncio.sleep(0.9)
        rprint(f"[green]Cleared all messages in {channel}.")
    
    @commands.command(brief="Show userinfo")
    @bot_owner_only()
    async def userinfo(self, ctx, member: discord.Member=None):
        """
        Shows userinfo of a guild member
        Only works in a guild channel

        Parameters
        -----------
        member: discord.Member
            Specify your target [mention, ID]
            If you provide no member it will show your
            userinfo
        """

        await ctx.message.delete()

        if member is None:
            member = ctx.author

        username = member
        display_name = member.display_name
        id = member.id
        discrim = member.discriminator
        avatar = member.avatar.url
        created = member.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')
        joined = member.joined_at.__format__('%A, %d. %B %Y at %H:%M:%S')
        status = str(member.status).title()
        role_string = ' '.join(reversed([r.name for r in (member.roles)][1:]))
        top_role = member.top_role.name
        x = "\n"

        text = f"ID: {id}{x}Servername: {display_name}{x}Created at: {created}{x}Joined at: {joined}{x}Status: {status}{x}Top Role: {top_role}{x}Roles: {role_string}"
        await ctx.send(f'**Userinfo for {username}**{x}```py{x}{text}{x}```{avatar}', delete_after=delete_messages())

    @commands.command(brief="Show serverinfo")
    @bot_owner_only()
    async def serverinfo(self, ctx):
        """
        Shows information about a guild
        """

        await ctx.message.delete()
        name = str(ctx.guild.name)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)

        member_count = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon)
        list_of_bots = [bot.name for bot in ctx.guild.members if bot.bot]
        bot_names = ' '.join(list_of_bots)
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        online = len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members)))
        channel_count = len(ctx.guild.channels)
        voice_channel_count = len(ctx.guild.voice_channels)
        category_count = len(ctx.guild.categories)
        created_at = ctx.guild.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')
        verification_level = str(ctx.guild.verification_level)
        x = "\n"

        text = f"Owner: {owner}{x}ID: {id}{x}Members: {member_count}{x}Humans: {humans}{x}Online: {online}{x}Channels: {channel_count}{x}Voice Channels: {voice_channel_count}{x}Categories: {category_count}{x}Bots: {bot_names}{x}Created at: {created_at}{x}Verification: {verification_level}"

        await ctx.send(f"Serverinfo for **{name}**{x}```py{x}{text}{x}```{icon}", delete_after=delete_messages())

    @commands.command(aliases=["av"], brief="Show a member's avatar")
    @bot_owner_only()
    async def avatar(self, ctx, member: discord.Member=None):
        """
        Show the avatar of a member

        Parameters
        -----------
        member: discord.Member
            Specify your target [mention, ID]
            If you provide no member it will show your
            avatar
        """

        await ctx.message.delete()
        if member is None:
            member = ctx.author
        
        avatar = member.avatar.url
        x = "\n"
        content = f"> **{member}**'s Avatar{x}{avatar}"
        await ctx.send(content, delete_after=delete_messages())

    @commands.command(breif="Show a member's banner")
    @bot_owner_only()
    async def banner(self, ctx, member: discord.Member=None):
        """
        Show the banner of a member

        Parameters
        -----------
        member: discord.Member
            Specify your target [mention, ID]
            If you provide no member it will show your
            banner
        """

        await ctx.message.delete()
        if member is None:
            member = ctx.author

        try:
            user = await self.client.fetch_user(member.id)
            banner = user.banner
            x = "\n"
            content = f"> **{member}**'s Banner{x}{banner}"
            await ctx.send(content, delete_after=delete_messages())

        except Exception as e:
            await ctx.send("User has no banner.", delete_after=delete_messages())

    @commands.command(brief="Block a user")
    @bot_owner_only()
    async def block(self, ctx, user: discord.User):
        """
        Block a user quickly

        Parameters
        -----------
        user: discord.User
            Specify your target [mention, ID]
        """

        await ctx.message.delete()
        if user is None:
            return await ctx.send("Specify the target.")
        try:
            await user.block()
            await ctx.send(f"> Blocked user **{user.id}**", delete_after=delete_messages())
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(f"> Blocking user **{user.id}** failed", delete_after=delete_messages())

    @commands.command(brief="Unblock a user")
    @bot_owner_only()
    async def unblock(self, ctx, user: discord.User):
        """
        Unblock a user quickly

        Parameters
        -----------
        user: discord.User
            Specify your target [mention, ID]
        """

        await ctx.message.delete()
        if user is None:
            return await ctx.send("Specify the target.")
        try:
            await user.unblock()
            await ctx.send(f"> Unblocked user **{user.id}**", delete_after=delete_messages())
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send(f"> Unblocking user **{user.id}** failed", delete_after=delete_messages())



async def setup(client: commands.Bot):
    await client.add_cog(Utility(client))
