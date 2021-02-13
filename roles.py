import math
import asyncio
import discord
import os
import json
from discord.ext import commands

#Get channel id 
#Local ----------
# with open('config.json') as fh:
#      config = json.load(fh)

# r_channel_id = config['r_channel_id']

#Server ---------
r_channel_id = os.environ['r_channel_id']

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
def list2embed(in_list, title = "Title", color = 'green', msg = '', extra = ''):
    msg += '\n '

    for i, r in enumerate(in_list):
        msg += ("{0}. **{1}** \n " + extra).format(i + 1, r)

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
             
def check(author):
    def inner_check(message):
        print('too gay')
        return message.author == author 
    return inner_check

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

        if ctx.message.channel.id == r_channel_id:
                
            user = ctx.message.author
            ch = ctx.channel
            await ctx.message.delete()
            #msg = await self.bot.wait_for('message', check = self.check(user), timeout=30)
            
            cat_dict = get_categories(ctx)

            cat_keys = list(cat_dict.keys())
            cat_keys.reverse()

            #print(user.mention)

            for cat in cat_keys:
                role_list = cat_dict[cat]
                role_names = [role.name for role in role_list]
                embed = list2embed(role_names, title = "Roles in " + cat, color = 'red', msg = '**Hey {1}, please select your {0} from the ones below by writing the role name or the number:**'.format(cat.replace('_', ' '), user.mention))
                role_msg = await ch.send(embed = embed)

                msg = await self.bot.wait_for('message', check = check(user), timeout=60*3)

                await self.get_cat_roles(cat, msg, user, role_list, role_names, role_msg)

            print(user.id)
            user = [mem for mem in ctx.guild.members if mem.id == user.id][0]
            print(user)
            usr_roles = user.roles
            usr_roles.reverse()
            usr_roles = [role.mention for role in usr_roles[:-1]]

            embed = list2embed(usr_roles , title = "Updated roles for {0}".format(user.name), color = 'blue', msg = '**{0} now has the roles :** \n'.format(user.mention), extra = '\n')
            role_msg = await ch.send(embed = embed)
            await asyncio.sleep(10)
            await role_msg.delete()

        else:
            
            await ctx.message.delete()
            ch = self.bot.get_channel(r_channel_id)
            await ctx.channel.send("Please go to {} to use that command".format(ch.mention))

    async def get_cat_roles(self, cat, msg, user, role_list, role_names, role_msg):    
        try:
            role_ind = 0

            if int(msg.content) - 1 in range(len(role_list)):
                role_ind = int(msg.content) - 1
            else:
                role_ind = role_names.index(msg.content)

            await user.add_roles(role_list[role_ind])

        except:
            await msg.delete()
            bot_msg = await msg.channel.send('Sorry {}, we couldn\'t find that role, Would you like to try again? y/n.'.format(user.mention))
            msg = await self.bot.wait_for('message', check = check(user), timeout=60*3)

            if msg.content.lower() == 'y' or msg.content.lower() == 'yes':
                await msg.delete()
                await bot_msg.delete()

                msg = await self.bot.wait_for('message', check = check(user), timeout=60*3)
                await self.get_cat_roles(cat, msg, user, role_list, role_names, role_msg)
            
            elif msg.content.lower() == 'n' or msg.content.lower() == 'no':
                await msg.delete()

                bot_msg = await msg.channel.send('Skipping to the next category')

                await asyncio.sleep(3)
                await bot_msg.delete()

        try:
            await msg.delete()
        except:
            print("fuck your life")
        try:            
            await role_msg.delete()
        except:
            print("fuck my life")

    @commands.command(name = 'embed', aliases = ['emb'])
    async def _embed(self, ctx:commands.Context):

        await ctx.message.delete()

        if ctx.message.channel.id == r_channel_id:
            embed = list2embed([] , title = "How to use this channel", color = 'green', msg = 'Hey everyone, to initiate the role-assignment process, just type ```>getroles``` or ```>gr``` ', extra = '')
            role_msg = await ctx.message.channel.send(embed = embed)
