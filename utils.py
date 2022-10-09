import json

import discord

import db.dbfunc as dbfunc
from vars import url_row


def get_sus_list():
    sus_list_str = dbfunc.get_sus_words_str()
    json_compatible = sus_list_str.replace("'", '"')
    sus_list = json.loads(json_compatible)
    return sus_list


def get_sus_list_spanish():
    sus_list_str = dbfunc.get_sus_words_spanish()
    json_compatible = sus_list_str.replace("'", '"')
    sus_list = json.loads(json_compatible)
    return sus_list


def get_custom_list(id):
    custom_list_str = dbfunc.get_server_custom_list(id)
    json_compatible = custom_list_str.replace("'", '"')
    custom_list = json.loads(json_compatible)
    return custom_list


def get_blacklist():
    blacklist_str = dbfunc.get_blacklisted_words_str()
    json_compatible = blacklist_str.replace("'", '"')
    blacklist = json.loads(json_compatible)
    return blacklist


def create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed


def translate_list_type(list_type):
    if list_type == "Community":
        return "Comunidad"
    else:
        return "Personalizada"


async def need_permissions_embed(interaction: discord.Interaction, language):
    title = ""
    description = ""
    colour = discord.Color.red()

    if language == "English":
        title = "Error!"
        description = "You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
    elif language == "Español":
        title = "¡Error!"
        description = "Debe tener los permisos `ADMINISTRATOR` o` MANAGE_GUILD` para ejecutar este comando."

    await send(
        interaction=interaction,
        embed=create_embed(title, description, colour),
        view=url_row,
    )


async def send(
    interaction: discord.Interaction, embed: discord.Embed, view: discord.ui.View
):
    await interaction.response.send_message(embed=embed, view=view)


async def followup_send(
    interaction: discord.Interaction, embed: discord.Embed, view: discord.ui.View
):
    await interaction.followup.send(embed=embed, view=view)
