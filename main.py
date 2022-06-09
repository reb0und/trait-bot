import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import discord
from discord import Embed
from discord.ext import commands
import numpy as np

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("INITIALIZED")


class Info:
    def __init__(self, asset_id, token_id):
        self.asset_id = asset_id
        self.token_id = token_id

    @bot.command()
    async def trait(ctx, arg):
        url = "https://api.opensea.io/api/v1/asset/{}/{}/".format(
            PurePosixPath(unquote(urlparse(arg).path)).parts[2], PurePosixPath(
                unquote(urlparse(arg).path)).parts[3])

        r = requests.request("GET", url)
        data = json.loads(r.text)
        ctx.embed = discord.Embed(
            title=data['name'], url=data['permalink'], color=0000000)
        ctx.embed.set_thumbnail(url=data['image_url'])

        ctx.embed.set_footer(text='OpenSea - {}'.format(data['collection']['name']),
                             icon_url='https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png')

        total = data['collection']['stats']['total_supply']
        for i in data['traits']:
            trait_name = i['trait_type']
            trait_value = i['value']
            trait_count = i['trait_count'] / total
            trait_percent = trait_count * 100

            ctx.embed.add_field(
                name=trait_name, value='{} - `{}%`'.format(trait_value, trait_percent))

        await ctx.send(embed=ctx.embed)


bot.run("your token here")
