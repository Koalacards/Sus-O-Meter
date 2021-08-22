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
import random
from timeit import default_timer as timer

client = commands.Bot(".")
slash= SlashCommand(client, sync_commands=True, override_type=True)

invite_button = Button(label="Invite", style=ButtonStyle.URL, url="https://discord.com/oauth2/authorize?client_id=876097748255014932&permissions=2147567616&scope=bot%20applications.commands")
support_button = Button(label="Support", style=ButtonStyle.URL, url="https://discord.gg/5Jn32Upk4M")\

kinda_sus_pictures=["https://i.etsystatic.com/26195327/r/il/b9103b/2797002083/il_fullxfull.2797002083_t400.jpg",
 "https://imgix.bustle.com/uploads/image/2020/10/31/31aa14f0-bc99-4e6b-b785-26ae420971dd-screen-shot-2020-10-31-at-52151-pm.png?w=1200&h=630&fit=crop&crop=faces&fm=jpg",
 "https://image-cdn.neatoshop.com/styleimg/113537/none/black/default/477968-20;1605375643x.jpg",
 "https://ih1.redbubble.net/image.1042054698.6192/st,small,507x507-pad,600x600,f8f8f8.jpg",
 "https://cdn.shopify.com/s/files/1/0324/7941/2283/products/LookinKindaSus1_740x.jpg?v=1607627480",
 "http://www.rogueduck.art/uploads/1/2/4/7/124740057/s829560345432686266_p124_i1_w450.png",
 "https://imageproxy.ifunny.co/crop:x-20,resize:640x,quality:90x75/images/109afed84e8549231a40801bc7071ba2e2eaffb52863c22cafd6d5c631839d10_1.jpg",
 "https://i1.sndcdn.com/artworks-BZOdK0DGnlFHa23y-jG4Vcw-t500x500.jpg",
 "https://i.etsystatic.com/25325402/r/il/39e5de/2600613663/il_570xN.2600613663_mmum.jpg",
 "https://res.cloudinary.com/teepublic/image/private/s--g97Q4qXJ--/t_Resized%20Artwork/c_fit,g_north_west,h_954,w_954/co_000000,e_outline:35/co_000000,e_outline:inner_fill:35/co_ffffff,e_outline:35/co_ffffff,e_outline:inner_fill:35/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1601510568/production/designs/14563420_0.jpg"
 "https://i.imgflip.com/4kg413.jpg",
 "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsKHUFDoYcyODaSg9NOS_gbHrUvx428plJ0w&usqp=CAU",
 "https://res.cloudinary.com/teepublic/image/private/s--WaNQLAIU--/t_Resized%20Artwork/c_fit,g_north_west,h_1054,w_1054/co_ffffff,e_outline:53/co_ffffff,e_outline:inner_fill:53/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1606090299/production/designs/9596239_1.jpg",
 "https://images.fineartamerica.com/images/artworkimages/mediumlarge/3/among-us-being-very-sus-trung-dinh-art.jpg",
 "https://pbs.twimg.com/media/E2IGViFXMAAyldO.png"]

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

    await ctx.send(embed=embed, components=buttons)

@slash.slash(name='sus-words', description="Find out what words make people sus!")
async def sus_words(ctx):
    title="Sus Words List"
    description=", ".join(sus_list)
    colour=discord.Color.purple()

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

@slash.slash(name='help', description='View all of the commands and learn a bit about Sus-O-Meter!')
async def help(ctx):
    title="Sus-O-Meter Help Page"
    description=f"Welcome to Sus-O-Meter! This is a very simple bot that determines the most sus users in a channel based on how many sus words each user has said in the past {num_messages_to_search} messages sent in the channel.\n\n The commands are as follows:\n\n" \
        "**/sus-o-meter**: Runs the Sus-O-Meter on the channel the command is called in to see who is the most sus. Gives the top 10 sus users.\n\n" \
        "**/sus-words**: Shows all of the sus words that the Sus-O-Meter checks for.\n\n" \
        "**/suggest-sus-word**: Allows you to input a suggestion for a sus word that should be added to the sus list! Word goes directly to the developer for consideration.\n\n" \
        "**/help**: Shows this page.\n\n"\
        "I hope you enjoy the Sus-O-Meter, and don't be too sus!"

    colour=discord.Color.purple()

    await ctx.send(embed=_create_embed(title, description, colour), components=buttons)


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


@client.command()
async def servers(ctx):
    await ctx.send(str(len(client.guilds)))

client.run(RUN_ID)
