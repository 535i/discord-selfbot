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



from discord.ext import commands
from discord.ext.commands import Bot, Context
from config import prefix
import os
import time
import re
from rich import print as rprint
from rich.panel import Panel
import requests



client = Bot(command_prefix=prefix, self_bot=True, chunk_guilds_at_startup=False)
client.runtime = int(time.time())
client.version = "0.1.0"

def main_menu():
    title = ("""[cyan]
    ███████╗███████╗██╗     ███████╗    ██████╗  ██████╗ ████████╗
    ██╔════╝██╔════╝██║     ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
    ███████╗█████╗  ██║     █████╗█████╗██████╔╝██║   ██║   ██║   
    ╚════██║██╔══╝  ██║     ██╔══╝╚════╝██╔══██╗██║   ██║   ██║   
    ███████║███████╗███████╗██║         ██████╔╝╚██████╔╝   ██║   
    ╚══════╝╚══════╝╚══════╝╚═╝         ╚═════╝  ╚═════╝    ╚═╝             
    """)
    
    info = ("""[green]
          ╔══════════════════════════════════════════════╗
          ║   Created by @BÖZ https://github.com/535i    ║   
          ╚══════════════════════════════════════════════╝
    """)
    rprint(title)
    rprint(info)

def show_infos():
    guilds = len(client.guilds)
    rprint(Panel(f"""Guilds: [green]{guilds} [white]Username: [green]{client.user.name} [white]Commands: [green]{len(client.commands)} [white]Friends: [green]{len(client.friends)} [white]Version: [green]{client.version}""", expand=False))


def load_token_locally():
    """
    This function loads your user token from your computer, 
    so make sure you are logged in on Firefox or Chrome with your discord account.
    May take a while to load your token.
    """
    roaming = os.getenv("appdata")
    appdata = os.getenv("localappdata")
    firefox = 'Mozilla\\Firefox\\Profiles' 
    chrome = 'Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb'

    if os.path.exists(f'{roaming}\\{firefox}'):
        for root, dirs, files in os.walk(f'{roaming}\\{firefox}'):
            for file in files:
                if file.endswith('.sqlite'):
                    for line in (x.strip() for x in open(f'{root}\\{file}', 'r', errors='ignore') if x.strip()):
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line):
                            if check_token(token):
                                return token
                            
    elif os.path.exists(f'{appdata}\\{chrome}'):
        for file in os.listdir(f'{appdata}\\{chrome}'):
            if file.endswith(('log', 'ldb')):
                for line in (x.strip() for x in open(f'{appdata}\\{chrome}\\{file}', 'r', errors='ignore') if x.strip()):
                        for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line):
                            if check_token(token):
                                return token


    
                                                 
            
def check_token(token: str):
    headers = {
        'Authorization': f'{token}'
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        return True
    elif response.status_code == 401:
        return False
    else:
        return False        


async def load_cogs(dir: str) -> None:

    for file in os.listdir(f"./cogs/{dir}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await client.load_extension(f"cogs.{dir}.{extension}")

            except Exception as e:
                print(f"Failed to load the file {extension}\n{type(e).__name__}\n{e}")

main_menu()

@client.event
async def on_ready():
    await load_cogs("Selfbot")
    show_infos()
    

@client.event
async def on_command_error(context: Context, error) -> None:

    if isinstance(error, commands.CommandNotFound):
        await context.message.delete()
        rprint("[red][!] Command not found")

    elif isinstance(error, commands.CommandOnCooldown):
        await context.message.delete()
        rprint(f'[red][!] You are on cooldown, you can use it in {round(error.retry_after, 2)} seconds.')
        

token = load_token_locally()
client.run(token, log_handler=None)

