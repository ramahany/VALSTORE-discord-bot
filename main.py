import re
import asyncio
import os
import requests
import json
import discord
from discord.ext import commands
import base64
from valorant_data import get_guns_dic, get_store

guns_dic = get_guns_dic()

# start by prep the discord bot
TOKEN = '<YOUR_DISCORD_TOKEN>'
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'working?':
        await message.channel.send(f'working fine! thanks @{message.author}')

    if message.content == 'store':
        await message.channel.send('get_store {username} {password}')

    if message.content.find('get_store ') != -1:
        await message.delete()
        user_and_pass = message.content[10:].split(' ', 2)
        store, valorant_points = get_store(user_and_pass[0], user_and_pass[1])
        if store == 0:
            await message.channel.send('error')
        else:
            for store_item in store:
                await message.channel.send(guns_dic[store_item][1])
                await message.channel.send(guns_dic[store_item][0])
    
            await message.channel.send(f'you have {valorant_points}VP')


client.run(TOKEN)
