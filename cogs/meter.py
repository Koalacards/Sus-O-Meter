import asyncio
import random
import math
from typing import Dict

import discord
import nltk
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from nltk.tokenize import word_tokenize

import db.dbfunc as dbfunc
import utils
from vars import *

nltk.download("punkt")


class Meter(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @app_commands.command(name="sus-o-meter")
    @app_commands.describe(
        num_messages_to_search="Number of messages the bot will search in the channel, up to 5000 (default: 1000)"
    )
    async def sus_o_meter(
        self, interaction: discord.Interaction, num_messages_to_search: int = 1000
    ):
        """Who is the most sus in this channel?"""
        print("Sus-O-Meter command called")
        await interaction.response.defer()
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)

        if num_messages_to_search > 5000 or num_messages_to_search < 0:
            title = ""
            description = ""
            colour = discord.Color.red()
            if language == "English":
                title = "Error!"
                description = (
                    "The number of messages to search must be between 0 and 5000!"
                )
            elif language == "Español":
                title = "¡Error!"
                description = (
                    "¡El número de mensajes a buscar debe estar entre 0 y 5000!"
                )

            embed = utils.create_embed(title, description, colour)
            await utils.followup_send(
                interaction=interaction, embed=embed, view=url_row
            )

            return

        sus_channel = interaction.channel
        list_type = dbfunc.get_server_list_type(guild_id)
        title = f"Sus-O-Meter Evaluation for channel #{sus_channel.name}"
        if language == "Español":
            title = f"Evaluación Sus-O-Meter para canal #{sus_channel.name}"
        colour = discord.Color.orange()
        sus_dict = await self.most_sus_users_count(sus_channel, num_messages_to_search)
        description = ""

        if language == "English":
            description += (
                f"List type used: **{list_type}** (Use `/list-type` to change)\n\n"
            )
        elif language == "Español":
            description += f"Tipo de lista utilizado: **{utils.translate_list_type(list_type)}** (Usa `/list-type` para cambiar)\n\n"

        if len(sus_dict.values()) == 0:
            if language == "English":
                description += f"To my surprise, there are no sus words in this channel for the past {num_messages_to_search} messages! Everyone must be a crewmate :angel:"
            elif language == "Español":
                description += f"Para mi sorpresa, ¡no hay sus palabras en este canal para los últimos {num_messages_to_search} mensajes! Todos deben ser compañeros de tripulación :angel:"
        else:
            if language == "English":
                description += f"In the last {num_messages_to_search} sent messages to #{sus_channel.name}, the most sus users are:\n\n"
            elif language == "Español":
                description += f"En los últimos {num_messages_to_search} mensajes enviados a #{sus_channel.name}, la mayoría de sus usuarios son:\n\n"

        count = 1

        for author_name, sus_words in sus_dict.items():
            if count > 10:
                break

            if language == "English":
                description += f"{count}. **{author_name}** with a total of **{sus_words}** sus words!\n"
            elif language == "Español":
                description += f"{count}. **{author_name}** con un total de **{sus_words}** sus palabras!\n"

            count += 1

        embed = utils.create_embed(title, description, colour)

        if len(sus_dict.values()) > 0:
            embed.set_image(
                url=kinda_sus_pictures[random.randint(0, len(kinda_sus_pictures) - 1)]
            )
        # Update leaderboard
        self.update_leaderboard_dict(sus_dict)

        await utils.followup_send(interaction=interaction, embed=embed, view=url_row)
        print("sus-o-meter embed sent")

    @app_commands.command(name="sus-words")
    async def sus_words(self, interaction: discord.Interaction):
        """Find out what words make people sus!"""
        print("sus words command called")
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        list_type = dbfunc.get_server_list_type(guild_id)

        title = "Sus Words List"
        description = ""
        if language == "English":
            addition = ""
            if list_type == "Custom":
                addition = ", or `/custom-list-add` and `/custom-list-remove` to change the words"
            description += f"List type used: **{list_type}** (Use `/list-type` to change lists{addition})\n\n"
        elif language == "Español":
            addition = ""
            if list_type == "Custom":
                addition = ", o `/custom-list-add` y `/custom-list-remove` para cambiar las palabras"
            description += f"Tipo de lista utilizado: **{utils.translate_list_type(list_type)}** (Usa `/list-type` para cambiar listas{addition})\n\n"

        if list_type == "Custom":
            custom_list = utils.get_custom_list(guild_id)
            description += ", ".join(custom_list)
        else:
            if language == "English":
                sus_list = utils.get_sus_list()
                description += ", ".join(sus_list)
            elif language == "Español":
                title = "Lista de sus palabras"
                sus_list_spanish = utils.get_sus_list_spanish()
                description += ", ".join(sus_list_spanish)
        colour = discord.Color.purple()

        await utils.send(
            interaction=interaction,
            embed=utils.create_embed(title, description, colour),
            view=url_row,
        )

    @app_commands.command(name="suggest-sus-word")
    @app_commands.describe(
        word="A word that should be considered sus (can't contain spaces)!"
    )
    async def suggest_sus_word(self, interaction: discord.Interaction, word: str):
        """Send a sus word suggestion straight to the developer! (can't contain spaces!)"""
        print("suggest sus word command called")
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        suggestion_channel = self.client.get_channel(SUGGESTION_CHANNEL)
        split = word.split()
        if suggestion_channel is None:
            if language == "English":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Sus-O-Meter Error",
                        "Sus-O-Meter could not find the internal suggestion channel. Please report this in our support server if you can!",
                        discord.Color.red(),
                    ),
                    view=url_row,
                )
            elif language == "Español":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Error de Sus-O-Meter",
                        "Sus-O-Meter no pudo encontrar el canal de sugerencias interno. ¡Informe esto en nuestro servidor de soporte si puede!",
                        discord.Color.red(),
                    ),
                    view=url_row,
                )
        elif split[0] != word:
            if language == "English":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Error!",
                        'Your word cannot contain spaces or it will not be seen by Sus-O-Meter. If you wish to suggest a phrase, suggest the words individually (for example, instead of "sussy baka" suggest "sussy" and "baka")',
                        discord.Color.red(),
                    ),
                    view=url_row,
                )
            elif language == "Español":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "¡Error!",
                        'Su palabra no puede contener espacios o Sus-O-Meter no la verá. Si desea sugerir una frase, sugiera las palabras individualmente (por ejemplo, en lugar de "sussy baka" sugiera "sussy" y "baka")',
                        discord.Color.red(),
                    ),
                    view=url_row,
                )
        else:
            if language == "English":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Success!",
                        "Your (kinda) sus word has been send to the developer. Thank you!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
            elif language == "Español":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Éxito!",
                        "Su (un poco) palabra de Sus ha sido enviada al desarrollador. ¡Gracias!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )

            blacklist = utils.get_blacklist()
            for blacklisted_word in blacklist:
                if blacklisted_word.lower() in word.lower():
                    return

            await suggestion_channel.send(
                embed=utils.create_embed(
                    f"New Sus word suggestion by {interaction.user.name}",
                    f"Language: {language}\n Word: {word}",
                    discord.Color.green(),
                )
            )

    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """View all of the commands and learn a bit about Sus-O-Meter!"""
        print("help command called")
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)

        title = "Sus-O-Meter Help Page"
        description = (
            f"Welcome to Sus-O-Meter! This is a very simple bot that determines the most sus users in a channel based on how many sus words each user has said in a certain number of past messages to the channel.\n\n The commands are as follows:\n\n"
            "**/sus-o-meter**: Runs the Sus-O-Meter on the channel the command is called in to see who is the most sus. Gives the top 10 sus users.\n\n"
            "**/sus-o-meter-server**: Runs the Sus-O-Meter across all channels in a server, using an equally distributed number of messages per channel (with overflow, if one channel doesnt have a lot of messages). Gives the top 10 sus users.\n\n"
            "**/sus-words**: Shows all of the sus words that the Sus-O-Meter checks for (Shows Community or Custom list based on list type chosen).\n\n"
            "**/suggest-sus-word**: Allows you to input a suggestion for a sus word that should be added to the sus list! Word goes directly to the developer for consideration.\n\n"
            "**/user-sus-words**: Shows the top 50 sus words a user has said in this channel!\n\n"
            "**/leaderboard**: Shows a top 10 list of most sus words seen by Sus-O-Meter in a channel/server (updates on `/sus-o-meter` and `sus-o-meter-server` calls)\n\n"
            "**/help**: Shows this page.\n\n"
            "**/language**: Changes the language to English or Spanish!\n\n"
            "**AUTO SUS COMMANDS:**\n\n"
            "**/auto_sus**: Allows you to opt into the auto sus feature of Sus-O-Meter! This feature tells you when you have sent a sus word in your new messages and ejects you as the sussy impostor!\n\n"
            "**CUSTOM LIST COMMANDS** (moderator-only):\n\n"
            "**/list-type**: Changes the type of list between Community (the original list made by community members) and Custom (one that you can make yourself)!\n\n"
            "**/custom-list-add**: Adds a word to your custom list!\n\n"
            "**/custom-list-remove**: Removes a word from your custom list! (if it exists)\n\n"
            "I hope you enjoy the Sus-O-Meter, and don't be too sus!"
        )

        if language == "Español":
            title = "Página de ayuda de Sus-O-Meter"
            description = (
                f"¡Bienvenido a Sus-O-Meter! Este es un bot muy simple que determina la mayor cantidad de sus usuarios en un canal en función de la cantidad de sus palabras que cada usuario ha dicho en un cierto número de mensajes pasados ​​al canal.\n\n Los comandos son los siguientes:\n\n"
                "**/sus-o-meter**: Ejecuta el Sus-O-Meter en el canal en el que se llama al comando para ver quién es el más sus. Da los 10 mejores usuarios de sus.\n\n"
                "**/sus-o-meter-server**: Ejecuta el Sus-O-Meter a través de todos los canales en un servidor, usando un número igualmente distribuido de mensajes por canal (con desbordamiento, si un canal no tiene muchos mensajes). Ofrece los 10 mejores usuarios de sus.\n\n"
                "**/sus-words**: Muestra todas las sus palabras que busca el Sus-O-Meter (Muestra la comunidad o la lista personalizada según el tipo de lista elegido).\n\n"
                "**/suggest-sus-word**: ¡Le permite ingresar una sugerencia para una palabra sus que debe agregarse a la lista de sus! Word va directamente al desarrollador para su consideración.\n\n"
                "**/user-sus-words**: !Muestra las 50 principales palabras suspensivas que ha dicho un usuario en este canal!\n\n"
                "**/leaderboard**: Muestra una lista de las 10 principales de la mayoría de las palabras sus vistas por Sus-O-Meter en un canal/servidor (actualizaciones en las llamadas `/sus-o-meter` y `sus-o-meter-server`)\n\n"
                "**/help**: Muestra esta página.\n\n"
                "**/language**: ¡Cambia el idioma a inglés o español!\n\n"
                "**COMANDOS DE AUTOSUS:**\n\n"
                "**/auto_sus**: ¡Le permite optar por la función de autosus de Sus-O-Meter! ¡Esta función le indica cuándo ha enviado una palabra suss en sus nuevos mensajes y lo expulsa como el impostor sussy!\n\n"
                "**COMANDOS DE LISTA PERSONALIZADOS** (solo moderador):\n\n"
                "**/list-type**: ¡Cambia el tipo de lista entre Comunidad (la lista original hecha por miembros de la comunidad) y Personalizada (una que puede hacer usted mismo)!\n\n"
                "**/custom-list-add**: ¡Agrega una palabra a tu lista personalizada!\n\n"
                "**/custom-list-remove**: ¡Elimina una palabra de tu lista personalizada! (si existiera)\n\n"
                "Espero que disfrutes del Sus-O-Meter, ¡y no seas demasiado suspensivo!"
            )

        colour = discord.Color.purple()

        await utils.send(
            interaction=interaction,
            embed=utils.create_embed(title, description, colour),
            view=url_row,
        )

    @app_commands.command(name="language")
    @app_commands.describe(language="The language of the bot")
    @app_commands.choices(language=language_choices)
    async def language(self, interaction: discord.Interaction, language: Choice[int]):
        """Set the language of Sus-O-Meter"""
        print("language command called")
        author = interaction.user
        if (
            author.guild_permissions.administrator == True
            or author.guild_permissions.manage_guild == True
        ):
            guild_id = interaction.guild_id
            dbfunc.set_server_language(guild_id, language.name)
            title = ""
            description = ""
            colour = discord.Color.green()
            if language.name == "English":
                title = "Success!"
                description = "Language Set to `English` Successfully!"
            elif language.name == "Español":
                title = "¡Éxito!"
                description = "¡Idioma configurado en `Español` correctamente!"

            await utils.send(
                interaction=interaction,
                embed=utils.create_embed(title, description, colour),
                view=url_row,
            )
        else:
            await utils.need_permissions_embed(interaction, language.name)

    @app_commands.command(name="user-sus-words")
    @app_commands.describe(user="The user you want to get their sus information from")
    @app_commands.describe(
        num_messages_to_search="Number of messages the bot will search in the channel, up to 5000 (default: 1000)"
    )
    async def user_sus_words(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        num_messages_to_search: int = 1000,
    ):
        """Get the top 50 sus words a user has said!"""
        print("user_sus_words command")
        await interaction.response.defer()
        author = user
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)

        if num_messages_to_search > 5000 or num_messages_to_search < 0:
            title = ""
            description = ""
            colour = discord.Color.red()
            if language == "English":
                title = "Error!"
                description = (
                    "The number of messages to search must be between 0 and 5000!"
                )
            elif language == "Español":
                title = "¡Error!"
                description = (
                    "¡El número de mensajes a buscar debe estar entre 0 y 5000!"
                )

            embed = utils.create_embed(title, description, colour)
            await utils.followup_send(
                interaction=interaction, embed=embed, view=url_row
            )

            return

        sus_channel = interaction.channel
        list_type = dbfunc.get_server_list_type(guild_id)
        title = f"Sus words said from user {author.name} in channel #{sus_channel.name}"
        if language == "Español":
            title = f"Sus palabras dijeron para la usuaria {author.name} en el canal #{sus_channel.name}"
        colour = discord.Color.orange()
        word_dict = await self.sus_words_for_user(
            sus_channel, author, num_messages_to_search
        )

        description = ""

        if language == "English":
            description += (
                f"List type used: **{list_type}** (Use `/list-type` to change)\n\n"
            )
        elif language == "Español":
            description += f"Tipo de lista utilizado: **{utils.translate_list_type(list_type)}** (Usa `/list-type` para cambiar)\n\n"

        if len(word_dict.values()) == 0:
            if language == "English":
                description += f"User {author.name} has said no sus words in this channel for the past {num_messages_to_search} messages!"
            elif language == "Español":
                description += f"Usuaria {author.name} no ha dicho sus palabras en este canal en el pasado {num_messages_to_search} mensajes!"
        else:
            if language == "English":
                description += f"In the last {num_messages_to_search} sent messages to #{sus_channel.name}, user {author.name} has said:\n\n"
            elif language == "Español":
                description += f"En los últimos {num_messages_to_search} mensajes enviados a #{sus_channel.name}, usuaria {author.name} ha dicho:\n\n"

        count = 1

        for sus_word, word_count in word_dict.items():
            if count > 50:
                break
            eng_times = "times" if word_count > 1 else "time"
            esp_times = "veces" if word_count > 1 else "vez"
            if language == "English":
                description += f"**{sus_word}**: {word_count} {eng_times}!\n"
            elif language == "Español":
                description += f"¡**{sus_word}**: {word_count} {esp_times}!\n"

            count += 1

        embed = utils.create_embed(title, description, colour)

        if len(word_dict.values()) > 0:
            embed.set_image(
                url=kinda_sus_pictures[random.randint(0, len(kinda_sus_pictures) - 1)]
            )
        await utils.followup_send(interaction=interaction, embed=embed, view=url_row)

    @app_commands.command(name="sus-o-meter-server")
    async def sus_o_meter_server(self, interaction: discord.Interaction):
        """Who is the most sus user in your server? This command may take up to a minute to run."""
        print("sus-o-meter-server command")
        await interaction.response.defer()
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        channels = interaction.guild.text_channels

        messages_per_channel = math.floor(server_messages_to_search / len(channels))
        total_dictionary = {}
        overflow = 0
        for channel in channels:
            try:
                channel_sus_dict, messages_searched = await self.most_sus_users_count(
                    channel,
                    messages_per_channel + overflow,
                    return_messages_searched=True,
                )
                total_dictionary = utils.concat_dict(total_dictionary, channel_sus_dict)
                overflow += messages_per_channel - messages_searched
            except:
                pass

        sorted_total_dict = utils.sort_dict(total_dictionary)

        name = interaction.guild.name

        list_type = dbfunc.get_server_list_type(guild_id)
        title = f"Sus-O-Meter Evaluation for server {name} (using {messages_per_channel} messages per channel, with overflow)"
        if language == "Español":
            title = f"Evaluación Sus-O-Meter para servidor {name} (usando {messages_per_channel} mensajes por canal, con rebosadero)"
        colour = discord.Color.orange()

        description = ""

        if language == "English":
            description += (
                f"List type used: **{list_type}** (Use `/list-type` to change)\n\n"
            )
        elif language == "Español":
            description += f"Tipo de lista utilizado: **{utils.translate_list_type(list_type)}** (Usa `/list-type` para cambiar)\n\n"

        if len(sorted_total_dict.values()) == 0:
            if language == "English":
                description += f"To my surprise, there are no sus words in this server! Everyone must be a crewmate :angel:"
            elif language == "Español":
                description += f"Para mi sorpresa, ¡no hay sus palabras en este servidor! Todos deben ser compañeros de tripulación :angel:"
        else:
            if language == "English":
                description += f"In the last {messages_per_channel} messages per channel in server {name}, the most sus users are:\n\n"
            elif language == "Español":
                description += f"En los últimos {messages_per_channel} mensajes por canal en servidor {name}, la mayoría de sus usuarios son:\n\n"

        count = 1

        for author_name, sus_words in sorted_total_dict.items():
            if count > 10:
                break

            if language == "English":
                description += f"{count}. **{author_name}** with a total of **{sus_words}** sus words!\n"
            elif language == "Español":
                description += f"{count}. **{author_name}** con un total de **{sus_words}** sus palabras!\n"

            count += 1

        embed = utils.create_embed(title, description, colour)

        if len(sorted_total_dict.values()) > 0:
            embed.set_image(
                url=kinda_sus_pictures[random.randint(0, len(kinda_sus_pictures) - 1)]
            )
        # Update leaderboard
        self.update_leaderboard_dict(sorted_total_dict)
        await utils.followup_send(interaction=interaction, embed=embed, view=url_row)

    @app_commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        """Returns a leaderboard of the most sus words seen by the bot (updated when other commands are run)"""
        print("leaderboard command called")
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        leaderboard_dict = dbfunc.get_leaderboard_as_dict()
        title = (
            f"Leaderboard for the top 10 most sus words seen by the Sus-O-Meter bot:"
        )
        if language == "Español":
            title = f"Tabla de clasificación de las 10 palabras más suspicaces vistas por el bot Sus-O-Meter:"
        colour = discord.Color.orange()

        description = ""

        top3_str = {
            0: ":first_place:",
            1: ":second_place:",
            2: ":third_place:",
        }

        for index, username in enumerate(leaderboard_dict):
            if language == "English":
                description += f"{top3_str.get(index, index+1)}: **{username}**, with a total of **{leaderboard_dict.get(username)}** sus words!\n\n"
            if language == "Español":
                description += f"¡{top3_str.get(index, index+1)}: **{username}**, con un total de **{leaderboard_dict.get(username)}** sus palabras!\n\n"

        embed = utils.create_embed(title, description, colour)

        await utils.send(interaction=interaction, embed=embed, view=url_row)

    @app_commands.command()
    @app_commands.describe(
        opt_in="Opt in or out to the sus_o_meter telling you when you have a sus word in your messages!"
    )
    @app_commands.choices(opt_in=opt_in_choices)
    async def auto_sus(self, interaction: discord.Interaction, opt_in: Choice[int]):
        """This command allows you to opt into the auto-sus feature, which will let you know when you say sus words in your messages! Works for your user across all servers."""
        print("auto_sus command called")
        author_id = interaction.user.id
        guild_id = interaction.guild.id
        language = dbfunc.get_server_language(guild_id)
        title = ""
        description = ""
        colour = discord.Color.green()

        if opt_in.name == "yes":
            dbfunc.auto_sus_add(author_id)
            if language == "English":
                title = "Success!"
                description = "You have successfully opted into the auto sus feature!"

            if language == "Español":
                title = "¡Éxito!"
                description = "¡Ha optado con éxito por la función de autosus!"

        if opt_in.name == "no":
            dbfunc.auto_sus_remove(author_id)
            if language == "English":
                title = "Success!"
                description = "You have successfully opted out of the auto sus feature!"

            if language == "Español":
                title = "¡Éxito!"
                description = "¡Ha cancelado con éxito la función de autosus!"

        embed = utils.create_embed(title, description, colour)
        await utils.send(interaction=interaction, embed=embed, view=url_row)

    # Finds the total number of messages a user has sent in the guild with a keyword in them (if keyword is empty, get total number of messages)
    async def most_sus_users_count(
        self,
        channel,
        num_messages_to_search: int,
        return_messages_searched: bool = False,
    ):
        print("in most sus users function")
        language = dbfunc.get_server_language(channel.guild.id)
        list_type = dbfunc.get_server_list_type(channel.guild.id)

        word_list = utils.get_sus_list()
        if language == "Español":
            word_list = utils.get_sus_list_spanish()
        if list_type == "Custom":
            word_list = utils.get_custom_list(channel.guild.id)
        sus_dict = {}
        counter = 0
        print(f"Before looping through the {num_messages_to_search} messages")
        # For each message, check how many sus words are in there are attribute them all to the author
        async for message in channel.history(limit=num_messages_to_search):

            author = message.author
            content = message.content.lower()
            counter += 1
            if content != "":
                try:
                    content_words = word_tokenize(content)
                    sus_content_filter = filter(
                        lambda word: word in word_list, content_words
                    )
                    sus_content = len(list(sus_content_filter))
                    if sus_content > 0:
                        previous_sus_amount = sus_dict.get(author.name, 0)
                        sus_dict[author.name] = previous_sus_amount + sus_content
                except:
                    pass

        print(f"After looping through the {num_messages_to_search} messages")

        # Sort the authors by how many sus words they have
        sorted_sus_dict = utils.sort_dict(sus_dict)

        print("Returning the sorted dict")
        if return_messages_searched is False:
            return sorted_sus_dict
        else:
            return sorted_sus_dict, counter

    # Finds the sus words a user has sent in the channel
    async def sus_words_for_user(
        self, channel, user: discord.User, num_messages_to_search: int
    ):
        language = dbfunc.get_server_language(channel.guild.id)
        list_type = dbfunc.get_server_list_type(channel.guild.id)

        word_list = utils.get_sus_list()
        if language == "Español":
            word_list = utils.get_sus_list_spanish()
        if list_type == "Custom":
            word_list = utils.get_custom_list(channel.guild.id)
        word_dict = {}

        # For each message, check how many sus words are in there are attribute them all to the author
        async for message in channel.history(limit=num_messages_to_search):

            author = message.author
            if author == user:
                content = message.content.lower()
                if content != "":
                    try:
                        content_words = word_tokenize(content)
                        sus_content_filter = filter(
                            lambda word: word in word_list, content_words
                        )
                        sus_words_in_message = list(sus_content_filter)
                        for word in sus_words_in_message:
                            previous_word_amount = word_dict.get(word, 0)
                            word_dict[word] = previous_word_amount + 1
                    except:
                        pass

        # Sort the authors by how many sus words they have
        sorted_sus_dict = utils.sort_dict(word_dict)

        return sorted_sus_dict


    def update_leaderboard_dict(self, new_sus_dict: dict) -> Dict:
        leaderboard_dict = dbfunc.get_leaderboard_as_dict()

        for username, sus_words in new_sus_dict.items():
            if self.username_lower_in_keys(leaderboard_dict.keys(), username):
                if sus_words >= leaderboard_dict.get(username, 0):
                    leaderboard_dict[username] = sus_words
            else:
                leaderboard_dict[username] = sus_words
        new_sorted_leaderboard = utils.sort_dict(leaderboard_dict)

        top_10_leaderboard = {
            k: new_sorted_leaderboard[k] for k in list(new_sorted_leaderboard)[:10]
        }

        dbfunc.set_new_leaderboard_from_dict(top_10_leaderboard)

    def username_lower_in_keys(self, leaderboard_keys: list, username: str) -> bool:
        for key in leaderboard_keys:
            if key.lower() == username.lower():
                return True
        return False


async def setup(bot):
    await bot.add_cog(Meter(bot))
