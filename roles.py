import math

import discord
from discord.ext import commands

r_channel_id = 809339141791809568

c_palette  = {
    'red': 0xED254E,
    'black': 0x040404,
    'white': 0xEBEBEB,
    'green': 0x04D243,
    'yellow': 0xFFA400,
    'blue': 0x4A7B9D,
    'grey': 0x747474

}

#Displays a list as an embed
def list2embed(in_list, title = "Title", color = 'green'):
    msg = ""

    for i, r in enumerate(in_list):
        msg += "{0}. {1} \n ".format(i + 1, r)

    return discord.Embed(title = title, description = msg, color=c_palette[color])

def get_categories(ctx):

    #All assignable roles
    all_a_roles = ctx.guild.roles
    all_a_role_names = [role.name.lower() for role in all_a_roles]

    #All assignable categories
    all_a_cats = [role for role in all_a_roles if '<cat>' in role.name]

    cat_dict = {}

    for a_cat in all_a_cats:

        #print(a_cat.name)

        cat_name = a_cat.name.replace("<cat>", "").lower()
        cat_roles = all_a_roles[all_a_role_names.index("<c_end>" + cat_name) + 1 : all_a_role_names.index("<cat>" + cat_name)]
        cat_dict[a_cat.name.replace("<cat>", "").lower()] = cat_roles

    #print(cat_dict)

    return cat_dict
             


class Roles(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name = 'list', aliases = ['l'])
    async def _list_roles(self, ctx:commands.Context):
        
        await ctx.message.delete()

        if ctx.message.channel.id == r_channel_id:            
            #Lists all roles
            if "all" in ctx.message.content:

                role_names = [role.name for role in ctx.guild.roles if "<cat>" not in role.name and "<c_end>" not in role.name]
                role_names = role_names[role_names.index("<end>") + 1 : role_names.index("<start>")]

                embed = list2embed(role_names, title = "All available roles", color = 'red')

                await ctx.channel.send(embed = embed)

            #Lists all categories
            if "cats" in ctx.message.content:

                cat_names = [key.replace("_", " ") for key in get_categories(ctx).keys()]

                embed = list2embed(cat_names, title = "Categories ", color = 'yellow')

                await ctx.channel.send(embed = embed)

            elif "cat" in ctx.message.content:
                msg = ctx.message
                cat = msg.content[msg.content.index("cat") + len("cat"):]
                cat = cat.replace(" ", "")

                cat_roles = get_categories(ctx)[cat.lower()]
                cat_roles = [role.name for role in cat_roles]

                #Embed Message
                embed = list2embed(cat_roles, title = "Roles in " + cat, color = 'blue')

                await ctx.channel.send(embed = embed)

        
        else:
            ch = self.bot.get_channel(r_channel_id)
            await ctx.channel.send("Please go to {} to use that command".format(ch.mention))


    @commands.command(name = 'getroles', aliases = ['gr'])
    async def _get_roles(self, ctx:commands.Context):
        
        user = ctx.message.author
        await user.send('👀')

        cat_list = get_categories(ctx)