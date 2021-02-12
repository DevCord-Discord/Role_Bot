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

bot.run('ODA5NjYzNjQ4MTYzMTY4Mjg3.YCYYCA.XeB6xEnSMOHVyCorcVWk6ej1HKA')

'''@bot.command()
async def l_roles(ctx):
    await ctx.send(ctx.guild.roles)
'''