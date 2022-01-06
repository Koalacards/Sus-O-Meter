import db.dbfunc as dbfunc
from discord.ext import commands
import utils
from sus_lists import sus_list, sus_list_spanish

class AdminCommands(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def add_sus_word(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            sus_list.append(word)
            dbfunc.set_sus_words(sus_list)
            await ctx.send(":thumbsup:")

    @commands.command()
    async def add_sus_word_spanish(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            sus_list_spanish.append(word)
            dbfunc.set_sus_words_spanish(sus_list_spanish)
            await ctx.send(":thumbsup:")

    @commands.command()
    async def refresh_sus_list(self, ctx):
        if ctx.author.id == 264034992970006528:
            sus_list = utils.get_sus_list()
            sus_list_spanish = utils.get_sus_list_spanish()
            await ctx.send(":thumbsup:")
    
    @commands.command()
    async def remove_sus_word(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            try:
                sus_list.remove(word)
                dbfunc.set_sus_words(sus_list)
                await ctx.send(":thumbsup:")
            except:
                await ctx.send("word does not exist in list")

    @commands.command()
    async def remove_sus_word_spanish(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            try:
                sus_list_spanish.remove(word)
                dbfunc.set_sus_words_spanish(sus_list_spanish)
                await ctx.send(":thumbsup:")
            except:
                await ctx.send("word does not exist in list")


    @commands.command()
    async def servers(self, ctx):
        await ctx.send(str(len(self.client.guilds)))

def setup(bot):
    bot.add_cog(AdminCommands(bot))