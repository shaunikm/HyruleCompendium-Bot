import os
import discord
from discord_components import Button
from discord.ext import commands
from pyrule_compendium import compendium, exceptions

client = commands.Bot(command_prefix='!')

comp = compendium()

data_order = ['description', 'attack', 'defense', 'drops', 'hearts_recovered', 'cooking_effect', 'common_locations']

client.remove_command('help')
commandsHelpList = ['!help', '!search', '!invite']
descriptionHelpList = ['View the message you\'re seeing right now.',
                       'Search for an entry in the Hyrule Compendium.',
                       'Get the invite link for this bot to invite it to more servers!']


def get_key_from_value(dict_, value):
    dict_keys = list(dict_.keys())
    dict_values = list(dict_.values())
    key = dict_keys[dict_values.index(value)]
    return key


def cap_all(in_str: str):
    term_list = [i for i in in_str.split()]
    for i in term_list:
        term_list[term_list.index(i)] = term_list[term_list.index(i)].capitalize()
    return ' '.join(i for i in term_list)


@client.event
async def on_ready():
    print('Bot is ready!')


@client.command(aliases=['inv', 'i'])
async def invite(ctx):
    inv_button = Button(
        url='https://discord.com/api/oauth2/authorize?client_id=795444152443207680&permissions=509952&scope=bot',
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
    await ctx.send(embed=embed)


@client.command(aliases=['s'])
async def search(ctx, *, term):
    try:
        data = comp.get_entry(term.lower())
    except exceptions.NoEntryError:
        await ctx.send(f'Item `{term}` not found!')
        return

    embed = discord.Embed(colour=discord.Colour.gold(), title=cap_all(data['name']))
    embed.set_thumbnail(url=data['image'])
    for i in data_order:
        try:
            value_ = data[i]
            title = get_key_from_value(data, value_)
            head = cap_all(title.replace('_', ' '))
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
