import math
import asyncio
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
def list2embed(in_list, title = "Title", color = 'green', msg = ''):
    msg += '\n '

    for i, r in enumerate(in_list):
        msg += "{0}. **{1}** \n ".format(i + 1, r)

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
            embed = list2embed(role_names, title = "Roles in " + cat, color = 'green', msg = '**Hey {1}, please select your {0} from the ones below by writing the role name or the number:**'.format(cat.replace('_', ' '), user.mention))
            role_msg = await ch.send(embed = embed)

            msg = await self.bot.wait_for('message', check = check(user), timeout=60*3)

            try:
                role_ind = 0

                if int(msg.content) - 1 in range(len(role_list)):
                    role_ind = int(msg.content) - 1
                else:
                    role_ind = role_names.index(msg.content)

                await user.add_roles(role_list[role_ind])

            except:
                await ch.send('Sorry {}, we couldn\'t find that role.'.format(user.mention))
                await asyncio.sleep(2)

            await msg.delete()
            await role_msg.delete()

        print(ctx.guild.members)
        user = self.bot.get_user([mem for mem in ctx.guild.members if mem.id == user.id][0])
        print(user)
        usr_roles = user.roles
        usr_roles.reverse()
        usr_roles = [role.mention for role in usr_roles[:-1]]

        embed = list2embed(usr_roles , title = "Updated roles for {0}".format(user.name), color = 'red', msg = '**{0} now has the roles :**'.format(user.mention))
        role_msg = await ch.send(embed = embed)
        await asyncio.sleep(10)
        await role_msg.delete()
        