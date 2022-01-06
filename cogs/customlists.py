import discord
import db.dbfunc as dbfunc
from discord.ext import commands
from discord_slash import cog_ext
import vars
from vars import action_row
import utils

class CustomLists(commands.Cog):

    @cog_ext.cog_slash('list-type',
    #guild_ids=guild_ids,
    description="Select your list type between Community and Custom! (Default: Community)",
    options=vars.list_type_options)
    async def set_list_type(self, ctx, list_type:str):
        print("list_type command called")
        author = ctx.author
        language = dbfunc.get_server_language(ctx.guild.id)
        if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
            pass
        else:
            await utils.need_permissions_embed(ctx, language)


def setup(bot):
    bot.add_cog(CustomLists(bot))
