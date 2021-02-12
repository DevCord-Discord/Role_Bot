#!/usr/bin/env python3
import discord
import json
import os

from discord.ext import commands

import roles 

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    activity = discord.Game(name='>help Roles')
    await bot.change_presence(activity=activity)
    print(f'Logged in as {bot.user.name}')
    bot.add_cog(roles.Roles(bot))

def main():
    # with open('config.json') as fh:
    #     bot.config = json.load(fh)

    # bot.run(bot.config['token'])
    bot.run(os.environ['token'])
    


if __name__ == "__main__":
    main()