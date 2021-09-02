import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.cog_ext import manage_commands
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from confidential import RUN_ID, SUGGESTION_CHANNEL
from vars import kinda_sus_pictures
import dbfunc
import json
import random

guild_ids=[876103457407385661]

client = commands.Bot(".")
slash= SlashCommand(client, sync_commands=True, override_type=True)

invite_button = create_button(label="Invite", style=ButtonStyle.URL, url="https://discord.com/oauth2/authorize?client_id=876097748255014932&permissions=2147567616&scope=bot%20applications.commands")
support_button = create_button(label="Support", style=ButtonStyle.URL, url="https://discord.gg/5Jn32Upk4M")


buttons = [invite_button, support_button]

action_row = create_actionrow(*buttons)

num_messages_to_search = 1000


suggest_sus_word_options=[
    manage_commands.create_option(
        name="word",
        description="A word that should be considered sus!",
        option_type=3,
        required=True
    )
]

language_options=[
    manage_commands.create_option(
        name="language",
        description="The language of the bot",
        option_type=3,
        required=True,
        choices=[
            "English",
            "Spanish"
        ]
    )
]

def get_sus_list():
    sus_list_str = dbfunc.get_sus_words_str()
    json_compatible= sus_list_str.replace("'", "\"")
    sus_list = json.loads(json_compatible)
    return sus_list

sus_list = get_sus_list()

@client.event
async def on_ready():
    print("ready")

@slash.slash(name='sus-o-meter', guild_ids=guild_ids, description="Who is the most sus in this channel?")
async def sus_o_meter(ctx):
    await ctx.defer()
    sus_channel= ctx.channel
    title=f"Sus-O-Meter Evaluation for channel #{sus_channel.name}"
    colour=discord.Color.orange()
    sus_dict = await most_sus_users_count(sus_channel)

    description=""

    if len(sus_dict.values()) == 0:
        description+=f"To my surprise, there are no sus words in this channel for the past {num_messages_to_search} messages! Everyone must be a crewmate :angel:"
    else:
        description+=f"In the last {num_messages_to_search} sent messages to #{sus_channel.name}, the most sus users are:\n\n"

    count = 1

    for author_name, sus_words in sus_dict.items():
        if count > 10:
            break

        description+=f"{count}. **{author_name}** with a total of **{sus_words}** sus words!\n"
        
        count+=1 

    embed = _create_embed(title, description, colour)

    if len(sus_dict.values()) > 0:
        embed.set_image(url=kinda_sus_pictures[random.randint(0, len(kinda_sus_pictures) - 1)])

    await ctx.send(embed=embed, components=[action_row])

@slash.slash(name='sus-words', guild_ids=guild_ids, description="Find out what words make people sus!")
async def sus_words(ctx):
    title="Sus Words List"
    description=", ".join(sus_list)
    colour=discord.Color.purple()

    await ctx.send(embed=_create_embed(title, description, colour), components=[action_row])

@slash.slash(name='suggest-sus-word', guild_ids=guild_ids, description='Send a sus word suggestion straight to the developer!', options=suggest_sus_word_options)
async def suggest_sus_word(ctx, word:str):
    suggestion_channel=client.get_channel(SUGGESTION_CHANNEL)
    if suggestion_channel is None:
        await ctx.send(embed=_create_embed('Sus-O-Meter Error', 'Sus-O-Meter could not find the internal suggestion channel. Please report this in our support server if you can!', discord.Color.red()), components=[action_row])
    else:
        await ctx.send(embed=_create_embed('Success!', 'Your (kinda) sus word has been send to the developer. Thank you!', discord.Color.green()), components=[action_row])

        await suggestion_channel.send(embed=_create_embed(f"New Sus word suggestion by {ctx.author.name}", f"{word}", discord.Color.green()))

def _create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

@slash.slash(name='help', guild_ids=guild_ids, description='View all of the commands and learn a bit about Sus-O-Meter!')
async def help(ctx):
    title="Sus-O-Meter Help Page"
    description=f"Welcome to Sus-O-Meter! This is a very simple bot that determines the most sus users in a channel based on how many sus words each user has said in the past {num_messages_to_search} messages sent in the channel.\n\n The commands are as follows:\n\n" \
        "**/sus-o-meter**: Runs the Sus-O-Meter on the channel the command is called in to see who is the most sus. Gives the top 10 sus users.\n\n" \
        "**/sus-words**: Shows all of the sus words that the Sus-O-Meter checks for.\n\n" \
        "**/suggest-sus-word**: Allows you to input a suggestion for a sus word that should be added to the sus list! Word goes directly to the developer for consideration.\n\n" \
        "**/help**: Shows this page.\n\n"\
        "I hope you enjoy the Sus-O-Meter, and don't be too sus!"

    colour=discord.Color.purple()

    await ctx.send(embed=_create_embed(title, description, colour), components=[action_row])

@slash.slash(name='language', guild_ids=guild_ids, description='Set the language of Sus-O-Meter', options=language_options)
async def language(ctx, language:str):
    author = ctx.author
    if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
        guild_id = ctx.guild.id
        dbfunc.set_server_language(guild_id, language)
        title=""
        description=""
        colour=discord.Color.green()
        if language == "English":
            title="Success!"
            description="Language Set to `English` Successfully!"
        elif language == "Spanish":
            title="¡Éxito!"
            description="¡Idioma configurado en `español` correctamente!"

        await ctx.send(embed=_create_embed(title, description, colour), components=[action_row])
    else:
        title=""
        description=""
        colour=discord.Color.red()
        
        if language =="English":
            title="Error!"
            description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
        elif language == "Spanish":
            title="¡Error!"
            description="Debe tener los permisos `ADMINISTRATOR` o` MANAGE_GUILD` para ejecutar este comando."

        await ctx.send(embed=_create_embed(title, description, colour), components=[action_row])



#Finds the total number of messages a user has sent in the guild with a keyword in them (if keyword is empty, get total number of messages)
async def most_sus_users_count(channel):

    sus_dict = {}

    #For each message, check how many sus words are in there are attribute them all to the author
    async for message in channel.history(limit=num_messages_to_search):
        author = message.author
        content = message.content.lower()
        content_words = content.split()
        for word in content_words:
            if word in sus_list:
                previous_sus_amount = sus_dict.get(author.name, 0)
                sus_dict[author.name] = previous_sus_amount + 1

    #Sort the authors by how many sus words they have
    sorted_sus_list = sorted(sus_dict.items(), key=lambda x: x[1], reverse=True)

    sorted_sus_dict = {}

    for item in sorted_sus_list:
        sorted_sus_dict[item[0]] = item[1]

    return sorted_sus_dict

@client.command()
async def add_sus_word(ctx, *, word:str):
    if ctx.author.id == 264034992970006528:
        sus_list.append(word)
        dbfunc.set_sus_words(sus_list)
        await ctx.send(":thumbsup:")

@client.command()
async def refresh_sus_list(ctx):
    if ctx.author.id == 264034992970006528:
        global sus_list
        sus_list = get_sus_list()
        await ctx.send(":thumbsup:")


@client.command()
async def servers(ctx):
    await ctx.send(str(len(client.guilds)))

client.run(RUN_ID)
