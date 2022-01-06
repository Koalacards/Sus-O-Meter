import json
import discord
import db.dbfunc as dbfunc
from vars import action_row
def get_sus_list():
    sus_list_str = dbfunc.get_sus_words_str()
    json_compatible= sus_list_str.replace("'", "\"")
    sus_list = json.loads(json_compatible)
    return sus_list

def get_sus_list_spanish():
    sus_list_str = dbfunc.get_sus_words_spanish()
    json_compatible= sus_list_str.replace("'", "\"")
    sus_list = json.loads(json_compatible)
    return sus_list

def create_embed(title, description, colour):
    embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

async def need_permissions_embed(ctx, language):
    title=""
    description=""
    colour=discord.Color.red()
    
    if language =="English":
        title="Error!"
        description="You must have `ADMINISTRATOR` or `MANAGE_GUILD` permissions to run this command."
    elif language == "Español":
        title="¡Error!"
        description="Debe tener los permisos `ADMINISTRATOR` o` MANAGE_GUILD` para ejecutar este comando."

    await ctx.send(embed=create_embed(title, description, colour), components=[action_row])