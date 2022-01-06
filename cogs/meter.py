import discord
from discord.ext import commands
from discord_slash import cog_ext
import utils
import db.dbfunc as dbfunc
import random
import nltk
from nltk.tokenize import word_tokenize
from vars import kinda_sus_pictures, num_messages_to_search, action_row, suggest_sus_word_options, language_options, SUGGESTION_CHANNEL

from sus_lists import sus_list, sus_list_spanish

nltk.download('punkt')

class Meter(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client

    @cog_ext.cog_slash(name='sus-o-meter',
    #guild_ids=guild_ids,
    description="Who is the most sus in this channel?")
    async def sus_o_meter(self, ctx):
        print("Sus-O-Meter command called")
        await ctx.defer()
        language = dbfunc.get_server_language(ctx.guild.id)
        sus_channel= ctx.channel
        title=f"Sus-O-Meter Evaluation for channel #{sus_channel.name}"
        if language == "Español":
            title=f"Evaluación Sus-O-Meter para canal #{sus_channel.name}"
        colour=discord.Color.orange()
        sus_dict = await self.most_sus_users_count(sus_channel)

        description=""

        if len(sus_dict.values()) == 0:
            if language == "English":
                description+=f"To my surprise, there are no sus words in this channel for the past {num_messages_to_search} messages! Everyone must be a crewmate :angel:"
            elif language == "Español":
                description+=f"Para mi sorpresa, ¡no hay sus palabras en este canal para los últimos {num_messages_to_search} mensajes! Todos deben ser compañeros de tripulación :angel:"
        else:
            if language == "English":
                description+=f"In the last {num_messages_to_search} sent messages to #{sus_channel.name}, the most sus users are:\n\n"
            elif language == "Español":
                description+=f"En los últimos {num_messages_to_search} mensajes enviados a #{sus_channel.name}, la mayoría de sus usuarios son:\n\n"

        count = 1

        for author_name, sus_words in sus_dict.items():
            if count > 10:
                break
            
            if language == "English":
                description+=f"{count}. **{author_name}** with a total of **{sus_words}** sus words!\n"
            elif language == "Español":
                description+=f"{count}. **{author_name}** con un total de **{sus_words}** sus palabras!\n"
            
            count+=1 

        embed = utils.create_embed(title, description, colour)

        if len(sus_dict.values()) > 0:
            embed.set_image(url=kinda_sus_pictures[random.randint(0, len(kinda_sus_pictures) - 1)])
        await ctx.send(embed=embed, components=[action_row])
        print("sus-o-meter embed sent")

    @cog_ext.cog_slash(name='sus-words',
    #guild_ids=guild_ids,
    description="Find out what words make people sus!")
    async def sus_words(self, ctx):
        print("sus words command called")
        language = dbfunc.get_server_language(ctx.guild.id)

        title="Sus Words List"
        description=""
        if language == "English":
            description=", ".join(sus_list)
        elif language == "Español":
            title="Lista de sus palabras"
            description=", ".join(sus_list_spanish)
        colour=discord.Color.purple()

        await ctx.send(embed=utils.create_embed(title, description, colour), components=[action_row])

    @cog_ext.cog_slash(name='suggest-sus-word',
    #guild_ids=guild_ids,
    description='Send a sus word suggestion straight to the developer!', options=suggest_sus_word_options)
    async def suggest_sus_word(self, ctx, word:str):
        print("suggest sus word command called")
        language = dbfunc.get_server_language(ctx.guild.id)
        suggestion_channel=self.client.get_channel(SUGGESTION_CHANNEL)
        if suggestion_channel is None:
            if language == "English":
                await ctx.send(embed=utils.create_embed('Sus-O-Meter Error', 'Sus-O-Meter could not find the internal suggestion channel. Please report this in our support server if you can!', discord.Color.red()), components=[action_row])
            elif language == "Español":
                await ctx.send(embed=utils.create_embed('Error de Sus-O-Meter', 'Sus-O-Meter no pudo encontrar el canal de sugerencias interno. ¡Informe esto en nuestro servidor de soporte si puede!', discord.Color.red()), components=[action_row])
        else:
            if language == "English":
                await ctx.send(embed=utils.create_embed('Success!', 'Your (kinda) sus word has been send to the developer. Thank you!', discord.Color.green()), components=[action_row])
            elif language == "Español":
                await ctx.send(embed=utils.create_embed('Éxito!', 'Su (un poco) palabra de Sus ha sido enviada al desarrollador. ¡Gracias!', discord.Color.green()), components=[action_row])

            await suggestion_channel.send(embed=utils.create_embed(f"New Sus word suggestion by {ctx.author.name}", f"Language: {language}\n Word: {word}", discord.Color.green()))

    @cog_ext.cog_slash(name='help',
    #guild_ids=guild_ids,
    description='View all of the commands and learn a bit about Sus-O-Meter!')
    async def help(self, ctx):
        print("help command called")
        language = dbfunc.get_server_language(ctx.guild.id)

        title="Sus-O-Meter Help Page"
        description=f"Welcome to Sus-O-Meter! This is a very simple bot that determines the most sus users in a channel based on how many sus words each user has said in the past {num_messages_to_search} messages sent in the channel.\n\n The commands are as follows:\n\n" \
            "**/sus-o-meter**: Runs the Sus-O-Meter on the channel the command is called in to see who is the most sus. Gives the top 10 sus users.\n\n" \
            "**/sus-words**: Shows all of the sus words that the Sus-O-Meter checks for.\n\n" \
            "**/suggest-sus-word**: Allows you to input a suggestion for a sus word that should be added to the sus list! Word goes directly to the developer for consideration.\n\n" \
            "**/help**: Shows this page.\n\n"\
            "**/language**: Changes the language to English or Spanish!\n\n" \
            "I hope you enjoy the Sus-O-Meter, and don't be too sus!"

        if language == "Español":
            title="Página de ayuda de Sus-O-Meter"
            description=f"¡Bienvenido a Sus-O-Meter! Este es un bot muy simple que determina la mayor cantidad de sus usuarios en un canal en función de la cantidad de sus palabras que cada usuario ha dicho en el pasado {num_messages_to_search} mensajes enviados en el canal.\n\n Los comandos son los siguientes:\n\n" \
            "**/sus-o-meter**: Ejecuta el Sus-O-Meter en el canal en el que se llama al comando para ver quién es el más sus. Da los 10 mejores usuarios de sus.\n\n" \
            "**/sus-words**: Muestra todas las sus palabras que busca el Sus-O-Meter.\n\n" \
            "**/suggest-sus-word**: ¡Le permite ingresar una sugerencia para una palabra sus que debe agregarse a la lista de sus! Word va directamente al desarrollador para su consideración.\n\n" \
            "**/help**: Muestra esta página.\n\n"\
            "**/language**: ¡Cambia el idioma a inglés o español!\n\n" \
            "Espero que disfrutes del Sus-O-Meter, ¡y no seas demasiado suspensivo!"


        colour=discord.Color.purple()

        await ctx.send(embed=utils.create_embed(title, description, colour), components=[action_row])

    @cog_ext.cog_slash(name='language',
    #guild_ids=guild_ids,
    description='Set the language of Sus-O-Meter', options=language_options)
    async def language(self,ctx, language:str):
        print("language command called")
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
            elif language == "Español":
                title="¡Éxito!"
                description="¡Idioma configurado en `Español` correctamente!"

            await ctx.send(embed=utils.create_embed(title, description, colour), components=[action_row])
        else:
            await utils.need_permissions_embed(ctx, language)



    #Finds the total number of messages a user has sent in the guild with a keyword in them (if keyword is empty, get total number of messages)
    async def most_sus_users_count(self, channel):
        print("in most sus users function")
        language = dbfunc.get_server_language(channel.guild.id)
        sus_list_language = sus_list
        if language == "Español":
            sus_list_language = sus_list_spanish
        sus_dict = {}

        print("Before looping through the 1000 messages")
        #For each message, check how many sus words are in there are attribute them all to the author
        async for message in channel.history(limit=num_messages_to_search):

            author = message.author
            content = message.content.lower()
            if content != "":
                try:
                    content_words = word_tokenize(content)
                    for word in content_words:
                        if word in sus_list_language:
                            previous_sus_amount = sus_dict.get(author.name, 0)
                            sus_dict[author.name] = previous_sus_amount + 1
                except:
                    pass
        
        print("After looping through the 1000 messages")

        #Sort the authors by how many sus words they have
        sorted_sus_list = sorted(sus_dict.items(), key=lambda x: x[1], reverse=True)

        print("Completed sorting sus list")

        sorted_sus_dict = {}

        for item in sorted_sus_list:
            sorted_sus_dict[item[0]] = item[1]

        print("Returning the sorted dict")
        return sorted_sus_dict
    

def setup(bot):
    bot.add_cog(Meter(bot))