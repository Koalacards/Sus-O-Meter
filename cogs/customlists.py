import discord
import db.dbfunc as dbfunc
from discord.commands import slash_command, Option
from discord.ext import commands
import vars
from vars import ButtonRow, guild_ids
import utils

class CustomLists(commands.Cog):

    @slash_command(name='list-type',
    #guild_ids=guild_ids,
    description="Select your list type between Community and Custom! (Default: Community)")
    async def set_list_type(self, ctx, list_type:Option(str, "The type of list the server will use (Community is a premade list, Custom is your own!)", choices=["Community", "Custom"])):
        print("list_type command called")
        author = ctx.author
        language = dbfunc.get_server_language(ctx.guild.id)
        if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
            dbfunc.set_server_list_type(ctx.guild.id, list_type)
            if language =="English":
                await ctx.respond(embed=utils.create_embed("Success!", f"List type set to `{list_type}`!", discord.Color.green()), view=ButtonRow())
            elif language == "Español":
                await ctx.respond(embed=utils.create_embed("¡Éxito!", f"¡El tipo de lista se estableció en `{utils.translate_list_type(list_type)}`!", discord.Color.green()), view=ButtonRow())
        else:
            await utils.need_permissions_embed(ctx, language)

    @slash_command(name='custom-list-add',
    #guild_ids=guild_ids,
    description="Add a word to your custom list (can't contain spaces!)")
    async def custom_list_add(self, ctx, word:str):
        print("custom_list_add command called")
        author = ctx.author
        language = dbfunc.get_server_language(ctx.guild.id)
        if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
            split = word.split()
            if split[0] != word:
                if language =="English":
                    await ctx.respond(embed=utils.create_embed("Error!", "Your word cannot contain spaces or it will not be seen by Sus-O-Meter. If you wish to add a phrase, add the words individually (for example, instead of \"sussy baka\" add \"sussy\" and \"baka\")", discord.Color.red()), view=ButtonRow())
                elif language == "Español":
                    await ctx.respond(embed=utils.create_embed("¡Error!", "Su palabra no puede contener espacios o Sus-O-Meter no la verá. Si desea agregar una frase, agregue las palabras individualmente (por ejemplo, en lugar de \"sussy baka\" agregue \"sussy\" y \"baka\")", discord.Color.red()), view=ButtonRow())
                return
            
            custom_list = utils.get_custom_list(ctx.guild.id)
            if word in custom_list:
                if language =="English":
                    await ctx.respond(embed=utils.create_embed("Error!", f"`{word}` is already in your custom list!", discord.Color.red()), view=ButtonRow())
                elif language == "Español":
                    await ctx.respond(embed=utils.create_embed("¡Error!", f"¡`{word}` ya está en su lista personalizada!", discord.Color.red()), view=ButtonRow())
                return

            blacklist = utils.get_blacklist()
            if word in blacklist:
                if language =="English":
                    await ctx.respond(embed=utils.create_embed("Error!", f"The word you entered is blacklisted by Sus-O-Meter for being derrogatory or inappropriate.", discord.Color.red()), view=ButtonRow())
                elif language == "Español":
                    await ctx.respond(embed=utils.create_embed("¡Error!", f"Sus-O-Meter pone en la lista negra la palabra que ingresó por ser despectiva o inapropiada.", discord.Color.red()), view=ButtonRow())
                return

            custom_list.append(word)
            dbfunc.set_server_custom_list(ctx.guild.id, custom_list)
            if language =="English":
                await ctx.respond(embed=utils.create_embed("Success!", f"`{word}` has been added to your custom list!", discord.Color.green()), view=ButtonRow())
            elif language == "Español":
                await ctx.respond(embed=utils.create_embed("¡Éxito!", f"¡`{word}` se ha agregado a su lista!", discord.Color.green()), view=ButtonRow())
        else:
            await utils.need_permissions_embed(ctx, language)
    
    @slash_command(name='custom-list-remove',
    #guild_ids=guild_ids,
    description="Remove a word from your custom list!")
    async def custom_list_remove(self, ctx, word:str):
        print("custom_list_remove command called")
        author = ctx.author
        language = dbfunc.get_server_language(ctx.guild.id)
        if author.guild_permissions.administrator == True or author.guild_permissions.manage_guild == True:
            custom_list = utils.get_custom_list(ctx.guild.id)
            if word not in custom_list:
                if language =="English":
                    await ctx.respond(embed=utils.create_embed("Error!", f"`{word}` is not in your custom list!", discord.Color.red()), view=ButtonRow())
                elif language == "Español":
                    await ctx.respond(embed=utils.create_embed("¡Error!", f"¡`{word}` no está en su lista personalizada!", discord.Color.red()), view=ButtonRow())
                return

            custom_list.remove(word)
            dbfunc.set_server_custom_list(ctx.guild.id, custom_list)
            if language =="English":
                await ctx.respond(embed=utils.create_embed("Success!", f"`{word}` has been removed your custom list!", discord.Color.green()), view=ButtonRow())
            elif language == "Español":
                await ctx.respond(embed=utils.create_embed("¡Éxito!", f"¡`{word}` se ha eliminado de tu lista personalizada!", discord.Color.green()), view=ButtonRow())
        else:
            await utils.need_permissions_embed(ctx, language)

def setup(bot):
    bot.add_cog(CustomLists(bot))
