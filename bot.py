import discord
from discord.ext import commands
from discord_components.interaction import Interaction
from discord_slash import SlashCommand
from discord_slash.cog_ext import manage_commands
from discord_components import ButtonStyle, Button
from discord_slash_components import DiscordComponents
from confidential import RUN_ID, SUGGESTION_CHANNEL
import dbfunc
import json
from timeit import default_timer as timer

client = commands.Bot(".")
slash= SlashCommand(client, sync_commands=True, override_type=True)

invite_button = Button(label="Invite", style=ButtonStyle.URL, url="https://discord.com/oauth2/authorize?client_id=876097748255014932&permissions=2147567616&scope=bot%20applications.commands")
support_button = Button(label="Support", style=ButtonStyle.URL, url="https://discord.gg/5Jn32Upk4M")

buttons = [invite_button, support_button]

num_messages_to_search = 1000


suggest_sus_word_options=[
    manage_commands.create_option(
        name="word",
        description="A word that should be considered sus!",
        option_type=3,
        required=True
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
    DiscordComponents(client, slash)

@slash.slash(name='sus-o-meter', description="Who is the most sus in this channel?")
async def sus_o_meter(ctx):
    await ctx.defer()
    sus_channel= ctx.channel
    title=f"Sus-O-Meter Evaluation for channel {sus_channel.name}"
    colour=discord.Color.orange()
    sus_dict = await most_sus_users_count(sus_channel)

    description=""

    if len(sus_dict.values()) == 0:
        description+=f"To my surprise, there are no sus messages in this channel for the past {num_messages_to_search} messages! Everyone must be a crewmate :angel:"
    else:
        description+=f"In the last {num_messages_to_search} words of {sus_channel.name}, the most sus people are:\n\n"

    count = 1

    for author_name, sus_words in sus_dict.items():
        if count > 10:
            break

        description+=f"{count}. **{author_name}** with a total of **{sus_words}** sus words!\n"
        
        count+=1 

    await ctx.send(embed=_create_embed(title, description, colour), components=buttons)

@slash.slash(name='sus-words', description="Find out what words make people sus!")
async def sus_words(ctx):
    title="Sus Words List"
    description=", ".join(sus_list)
    colour=discord.Color.orange()

    await ctx.send(embed=_create_embed(title, description, colour), components=buttons)

@slash.slash(name='suggest-sus-word', description='Send a sus word suggestion straight to the developer!', options=suggest_sus_word_options)
async def suggest_sus_word(ctx, word:str):
    suggestion_channel=client.get_channel(SUGGESTION_CHANNEL)
    if suggestion_channel is None:
        await ctx.send(embed=_create_embed('Sus-O-Meter Error', 'Sus-O-Meter could not find the internal suggestion channel. Please report this in our support server if you can!', discord.Color.red()), components=buttons)
    else:
        await ctx.send(embed=_create_embed('Success!', 'Your (kinda) sus word has been send to the developer. Thank you!', discord.Color.green()), components=buttons)

        await suggestion_channel.send(embed=_create_embed(f"New Sus word suggestion by {ctx.author.name}", f"{word}", discord.Color.green()))

def _create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed


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
async def add_sus_word(ctx, word:str):
    if ctx.author.id == 264034992970006528:
        sus_list.append(word)
        dbfunc.set_sus_words(sus_list)
        await ctx.send(":thumbsup:")


client.run(RUN_ID)
