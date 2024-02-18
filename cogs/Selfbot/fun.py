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
import json
import random
import asyncio

def bot_owner_only():
    def is_owner(ctx: commands.Context):
        return ctx.author.id == ownerid
    return commands.check(is_owner)

def delete_messages():
    if del_messages is not None:
        return del_messages
    return None


class Fun(commands.Cog):
    """A class with Fun commands."""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.imitate_user = set()
        self.stalk_user = set()
        self._imitate_loop = False
        self._stalk_loop = False

    @commands.command(name="8ball", aliases=["ask"], brief="The famous 8ball")
    @bot_owner_only()
    async def _8ball(self, ctx, *, question:str=None):
        """
        Ask a question which can be answered with yes/no

        Parameters
        -----------
        question: str
            Ask your question
        """

        await ctx.message.delete()

        if question is None:
            return await ctx.send("I need a question.", delete_after=delete_messages)
        
        with open("cogs\\Selfbot\\Fun\\responses.json", "r") as file:
            data = json.load(file)
            possibilities = data['possibilities']

        response = random.choice(possibilities)
        x = "\n"
        content = f"{ctx.author} asked: {question}{x}My answer: {response}"
        
        await ctx.send(f"```css{x}{content}{x}```", delete_after=delete_messages())

    @commands.command(brief="Imitate a user")
    @bot_owner_only()
    async def imitate(self, ctx, member: discord.Member=None):
        """
        Imitate a user by sending the same messages or replies as the target

        Parameters
        -----------
        member: discord.Member
            Specify your target [mention, ID]
        """

        await ctx.message.delete()
        if member is None:
            return await ctx.send("Specify the target.")
        elif member == self.client.user:
            return await ctx.send("You cannot imitate yourself.", delete_after=delete_messages())
        elif self._imitate_loop == False:
            self._imitate_loop = True
            self.imitate_user.add(member.id)
            
        else:
            self._imitate_loop = False
            self.imitate_user.remove(member.id)
        return await ctx.send(f"Imitating *{member}* is now {('enabled :white_check_mark:' if self._imitate_loop else 'disabled')}", delete_after=delete_messages())
    

    @commands.command(brief="Stalk a user")
    @bot_owner_only()
    async def stalk(self, ctx, member: discord.Member=None):
        """
        Stalk a users messages or replies and print them

        Parameters
        -----------
        member: discord.Member
            Specify your target [mention, ID]
        """

        await ctx.message.delete()
        if member is None:
            return await ctx.send("Specify the target.")
        elif member == self.client.user:
            return await ctx.send("You cannot stalk yourself.", delete_after=delete_messages())
        
        elif self._stalk_loop == False:
            self._stalk_loop = True
            self.stalk_user.add(member.id)
            return await ctx.send(f"Stalking *{member}* now :face_in_clouds:", delete_after=delete_messages())
            
        else:
            self._stalk_loop = False
            self.stalk_user.remove(member.id)
            return await ctx.send(f"Not stalking *{member}* anymore :slight_smile:", delete_after=delete_messages())


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id in self.imitate_user and self._imitate_loop == True:
            if message.reference:
                if message.reference.resolved:
                    reply_message = await message.channel.fetch_message(message.reference.message_id)
                    if reply_message.author.id == self.client.user.id:
                        return
                    async with message.channel.typing():
                        await asyncio.sleep(3)
                        return await reply_message.reply(message.content)
                    
            async with message.channel.typing():
                await asyncio.sleep(3)
            return await message.channel.send(message.content)
        
        elif message.author.id in self.stalk_user and self._stalk_loop == True:
            if message.reference:
                if message.reference.resolved:
                    reply_message = await message.channel.fetch_message(message.reference.message_id)
                    if reply_message.author.id == self.client.user.id:
                        return
                    rprint(f"[cyan3]{message.author} replied to {reply_message.author} in #{message.channel}")
                    return

            rprint(f"[cyan3]{message.author} sent a message in #{message.channel}")
                    
            

async def setup(client: commands.Bot):
    await client.add_cog(Fun(client))
