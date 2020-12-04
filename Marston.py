'''
Version:     Python 3.7.2
Author:      James Grove
Description: Discord bot used to track key information for the online board game diplomacy.
'''
# Standard Libraries
import os
import time
# Third-Party Libraries
import requests
import discord
from discord.ext import commands
from PIL import Image
from bs4 import BeautifulSoup

# Global variables (WIP)
GAMEID = '303444'
GAMEURL = str(f'https://webdiplomacy.net/board.php?gameID={GAMEID}')
TOKEN = 'NzI2Nzg0MTI1MDk2Mjk2NDY5.XviUxA.PXOqO9RaB4fvfRG2wUg-k1jiUbI'
bot = commands.Bot(command_prefix='!')

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! \n')

@bot.command(name = 'map', help = 'View the current Diplomacy map')
async def map(ctx):

    author = ctx.message.author.mention

    # start user feedback
    start = time.time()
    print('command "map" initialising...')

    # name and path variables.
    image_name = 'diplomacy_map.png'
    image_path = str(f'{os.getcwd()}\{image_name}')

    # web scraping to download map.
    response = requests.get(GAMEURL)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.findAll('img')
    image = images[3]
    image_url = image['src']

    # posts map to discord and then deletes from disk.
    d_map = Image.open(requests.get((f'https://webdiplomacy.net/{image_url}'),
                       stream = True).raw)
    d_map.save(image_name)
    
    await ctx.send(file=discord.File(image_name))
    await ctx.send(f'{author}')
    
    os.remove(image_path)

    # end user feedback
    end = time.time()
    print(f'command "map" complete \nTime:{end-start} \n')

@bot.command(name = 'link', help = 'Posts the current Diplomacy URL')
async def link(ctx):

    author = ctx.message.author.mention

    # start user feedback
    start = time.time()
    print('command "link" initialising...')

    response = (GAMEURL)

    await ctx.send(f'{response} {author}')

    # end user feedback
    end = time.time()
    print(f'command "link" complete \nTime:{end-start} \n')

@bot.command(name = 'ready', help = 'Number of remaining players to ready up')
async def ready(ctx):

    author = ctx.message.author.mention

    # start user feedback
    start = time.time()
    print('command "ready" initialising...')

    # total players who have either saved or not submitted
    total = 0
    
    # web scrapes to scan ready status
    response = requests.get(GAMEURL)
    soup = BeautifulSoup(response.content, 'html.parser')
    members = soup.findAll('img')

    for member in members:
        if member['src'] == 'images/icons/alert.png' \
        or member['src'] == 'images/icons/tick_faded.png':
            total += 1

    await ctx.send(f'{total} players need to ready up! {author} @everyone')
    
    # end user feedback
    end = time.time()
    print(f'command "ready" complete \nTime:{end-start} \n')

@bot.command(name = 'help')
async def help(ctx):

    author = ctx.message.author.mention
    
    # start user feedback
    start = time.time()
    print('command "help" initialising...')

    await ctx.send(f'Here are my commands {author}! \n'
                   f'!ready: number of idle players. \n'
                   f'!map: view the current diplomacy map. \n'
                   f'!link: posts the current game URL.'
                   )

    # end user feedback
    end = time.time()
    print(f'command "help" complete \nTime:{end-start} \n')

@bot.event
async def on_command_error(ctx, error):

    author = ctx.message.author.mention
    
    if isinstance(error, commands.error.CheckFailure):
        await ctx.send(f'ERROR {author}')

bot.run(TOKEN)