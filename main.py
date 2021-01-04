import os
import discord
from discord.ext import commands
from HyruleCompendium import getEntry

client = commands.Bot(command_prefix='!')

client.remove_command('help')
commandsHelpList = ['!help', '!invite', '!search']
descriptionHelpList = ['View the message you\'re seeing right now.',
                       'Get the invite link for this bot to invite it to more servers!',
                       'Search for an entry in the Hyrule Compendium']


def capAll(inStr: str):
    termList = [i for i in inStr.split()]
    for i in termList:
        termList[termList.index(i)] = termList[termList.index(i)].capitalize()
    return ' '.join(i for i in termList)


@client.event
async def on_ready():
    print('Bot is ready!')


@client.command(aliases=['inv', 'i'])
async def invite(ctx):
    embed = discord.Embed(colour=discord.Colour.light_gray())
    embed.add_field(name='Invite Link',
                    value='\
                    [Click here](https://discord.com/api/oauth2/authorize?client_id=795444152443207680&permissions=509952&scope=bot)')
    await ctx.send(embed=embed)


@client.command(aliases=['h'])
async def help(ctx):
    embed = discord.Embed(colour=discord.Colour.red())
    for command, description in zip(commandsHelpList, descriptionHelpList):
        embed.add_field(name=command, value=description, inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['s'])
async def search(ctx, *, term):
    embed = discord.Embed(colour=discord.Colour.gold())
    try:
        data = getEntry(term.lower())
    except ValueError:
        await ctx.send('Invalid search term!')
        return
    if not data:
        await ctx.send('Invalid search term!')
        return
    term = capAll(term)
    embed.set_author(name=term)
    embed.add_field(name='Category', value=capAll(data['category']), inline=False)
    embed.add_field(name='ID', value=data['id'], inline=False)
    embed.add_field(name='Description', value=data['description'], inline=False)
    embed.add_field(name='Drops', value='\n'.join(' - ' + capAll(i) for i in data['drops']), inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send(f'Pong!\nClient Latency: `{round(client.latency*1000)}ms`')


client.run(os.getenv('HYRULE_COMPENDIUM_BOT_TOKEN'))
