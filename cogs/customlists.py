from ctypes import util

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

import db.dbfunc as dbfunc
import utils
from vars import *


class CustomLists(commands.Cog):
    @app_commands.command(name="list-type")
    @app_commands.describe(
        list_type="The type of list the server will use (Community is a premade list, Custom is your own!)"
    )
    @app_commands.choices(list_type=list_choices)
    async def list_type(self, interaction: discord.Interaction, list_type: Choice[int]):
        """Select your list type between Community and Custom! (Default: Community)"""
        print("list_type command called")
        author = interaction.user
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        if (
            author.guild_permissions.administrator == True
            or author.guild_permissions.manage_guild == True
        ):
            dbfunc.set_server_list_type(guild_id, list_type.name)
            if language == "English":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Success!",
                        f"List type set to `{list_type.name}`!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
            elif language == "Español":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "¡Éxito!",
                        f"¡El tipo de lista se estableció en `{utils.translate_list_type(list_type.name)}`!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
        else:
            await utils.need_permissions_embed(interaction, language)

    @app_commands.command(name="custom-list-add")
    @app_commands.describe(word="The word to add to your custom list")
    async def custom_list_add(self, interaction: discord.Interaction, word: str):
        """Add a word to your custom list (can't contain spaces!)"""
        print("custom_list_add command called")
        author = interaction.user
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        if (
            author.guild_permissions.administrator == True
            or author.guild_permissions.manage_guild == True
        ):
            split = word.split()
            if split[0] != word:
                if language == "English":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "Error!",
                            'Your word cannot contain spaces or it will not be seen by Sus-O-Meter. If you wish to add a phrase, add the words individually (for example, instead of "sussy baka" add "sussy" and "baka")',
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                elif language == "Español":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "¡Error!",
                            'Su palabra no puede contener espacios o Sus-O-Meter no la verá. Si desea agregar una frase, agregue las palabras individualmente (por ejemplo, en lugar de "sussy baka" agregue "sussy" y "baka")',
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                return

            custom_list = utils.get_custom_list(guild_id)
            if word in custom_list:
                if language == "English":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "Error!",
                            f"`{word}` is already in your custom list!",
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                elif language == "Español":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "¡Error!",
                            f"¡`{word}` ya está en su lista personalizada!",
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                return

            blacklist = utils.get_blacklist()
            if word in blacklist:
                if language == "English":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "Error!",
                            f"The word you entered is blacklisted by Sus-O-Meter for being derrogatory or inappropriate.",
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                elif language == "Español":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "¡Error!",
                            f"Sus-O-Meter pone en la lista negra la palabra que ingresó por ser despectiva o inapropiada.",
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                return

            custom_list.append(word)
            dbfunc.set_server_custom_list(guild_id, custom_list)
            if language == "English":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Success!",
                        f"`{word}` has been added to your custom list!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
            elif language == "Español":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "¡Éxito!",
                        f"¡`{word}` se ha agregado a su lista!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
        else:
            await utils.need_permissions_embed(interaction, language)

    @app_commands.command(name="custom-list-remove")
    @app_commands.describe(word="Word to remove from your custom list")
    async def custom_list_remove(self, interaction: discord.Interaction, word: str):
        """Remove a word from your custom list!"""
        print("custom_list_remove command called")
        author = interaction.user
        guild_id = interaction.guild_id
        language = dbfunc.get_server_language(guild_id)
        if (
            author.guild_permissions.administrator == True
            or author.guild_permissions.manage_guild == True
        ):
            custom_list = utils.get_custom_list(guild_id)
            if word not in custom_list:
                if language == "English":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "Error!",
                            f"`{word}` is not in your custom list!",
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                elif language == "Español":
                    await utils.send(
                        interaction=interaction,
                        embed=utils.create_embed(
                            "¡Error!",
                            f"¡`{word}` no está en su lista personalizada!",
                            discord.Color.red(),
                        ),
                        view=url_row,
                    )
                return

            custom_list.remove(word)
            dbfunc.set_server_custom_list(guild_id, custom_list)
            if language == "English":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "Success!",
                        f"`{word}` has been removed your custom list!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
            elif language == "Español":
                await utils.send(
                    interaction=interaction,
                    embed=utils.create_embed(
                        "¡Éxito!",
                        f"¡`{word}` se ha eliminado de tu lista personalizada!",
                        discord.Color.green(),
                    ),
                    view=url_row,
                )
        else:
            await utils.need_permissions_embed(interaction, language)


async def setup(bot):
    await bot.add_cog(CustomLists(bot))
