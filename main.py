import os
import discord
from discord_components import Button
from discord.ext import commands
from pyrule_compendium import compendium, exceptions
import utils

client = commands.Bot(command_prefix='!')

comp = compendium()

data_order = ['description', 'attack', 'defense', 'drops', 'hearts_recovered', 'cooking_effect', 'common_locations']

client.remove_command('help')
commandsHelpList = ['!help', '!search [item]', '!invite']
descriptionHelpList = ['View the message you\'re seeing right now.',
                       'Search for an entry in the Hyrule Compendium.',
                       'Get the invite link for this bot to invite it to more servers!']


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='!help and explore Hyrule'))
    print('Bot is ready!')


@client.command(aliases=['inv', 'i'])
async def invite(ctx):
    inv_button = Button(
        url='https://discord.com/oauth2/authorize?client_id=926198736907034624&permissions=509952&scope=bot',
        label='Click Me 🤖',
        style=5)

    await ctx.send('Invite Link:',
                   components=[
                       inv_button])


@client.command(aliases=['h', 'help'])
async def help_(ctx):
    embed = discord.Embed(colour=discord.Colour.red(), title='Discord Sheikah Slate', description='This discord bot gives you access to the Hyrule Compendium from here on discord!')
    for command, description in zip(commandsHelpList, descriptionHelpList):
        embed.add_field(name=command, value=description, inline=False)
    embed.add_field(name='Other Links', value='[GitHub](https://github.com/shaunikm/HyruleCompendium-Bot)'
                                              '\u200b \u200b \u200b [Data API](https://gadhagod.github.io/Hyrule-Compendium-API/#/)'
                                              '\u200b \u200b \u200b [Author](https://github.com/shaunikm)')
    await ctx.send(embed=embed)


@client.command(aliases=['s'])
async def search(ctx, *, term):
    try:
        data = comp.get_entry(term.lower())
    except exceptions.NoEntryError:
        closest_match = utils.format_closest_match(term, utils.indexed_dict)
        if closest_match:
            await ctx.send(f'Item `{term}` not found!\nDid you mean: `{closest_match}`?')
        else:
            await ctx.send(f'Item `{term}` not found!')
        return

    embed = discord.Embed(colour=discord.Colour.gold(), title=utils.cap_all(data['name']))
    embed.set_thumbnail(url=data['image'])
    for i in data_order:
        try:
            value_ = data[i]
            title = utils.get_key_from_value(data, value_)
            head = utils.cap_all(title.replace('_', ' '))
            if isinstance(value_, list):
                if 'Greater Hyrule' in value_:
                    value_ = u'\u2022 Everywhere'
                else:
                    value_ = '\n'.join(u'\u2022 ' + i.title() for i in value_)
            if head == 'Common Locations' and not value_:
                embed.add_field(name=head, value='_???_', inline=False)
            if value_:
                if value_ == data['description']:
                    embed.add_field(name=head, value=str(value_), inline=False)
                else:
                    embed.add_field(name=head, value=str(value_).title(), inline=False)
        except KeyError:
            pass

    await ctx.send(embed=embed)


@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send(f'Pong!\nClient Latency: `{round(client.latency * 1000)}ms`')


client.run(os.getenv('HYRULE_COMPENDIUM_BOT_TOKEN'))
