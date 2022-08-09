import db.dbfunc as dbfunc
from discord.ext import commands
import utils

class AdminCommands(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command()
    async def add_sus_word(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            sus_list = utils.get_sus_list()
            if word in sus_list:
                await ctx.send("word in sus list")
                return
            sus_list.append(word)
            dbfunc.set_sus_words(sus_list)
            await ctx.send(":thumbsup:")


    @commands.command()
    async def add_sus_word_spanish(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            sus_list_spanish = utils.get_sus_list_spanish()
            if word in sus_list_spanish:
                await ctx.send("word in spanish sus list")
                return
            sus_list_spanish.append(word)
            dbfunc.set_sus_words_spanish(sus_list_spanish)
            await ctx.send(":thumbsup:")
    
    @commands.command()
    async def remove_sus_word(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            try:
                sus_list = utils.get_sus_list()
                sus_list.remove(word)
                dbfunc.set_sus_words(sus_list)
                await ctx.send(":thumbsup:")
            except:
                await ctx.send("word does not exist in list")

    @commands.command()
    async def remove_sus_word_spanish(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            try:
                sus_list_spanish = utils.get_sus_list_spanish()
                sus_list_spanish.remove(word)
                dbfunc.set_sus_words_spanish(sus_list_spanish)
                await ctx.send(":thumbsup:")
            except:
                await ctx.send("word does not exist in list")
    
    @commands.command()
    async def add_blacklisted_word(self, ctx, *, word:str):
        if ctx.author.id == 264034992970006528:
            blacklist = utils.get_blacklist()
            if word in blacklist:
                await ctx.send("word in blacklist")
                return
            blacklist.append(word)
            dbfunc.set_blacklisted_words(blacklist)
            await ctx.send(":thumbsup:")
    
    @commands.command()
    async def remove_blacklisted_word(self, ctx, * , word:str):
        if ctx.author.id == 264034992970006528:
            try:
                blacklist = utils.get_blacklist()
                blacklist.remove(word)
                dbfunc.set_blacklisted_words(blacklist)
                await ctx.send(":thumbsup:")
            except:
                await ctx.send("word does not exist in list")
    
    @commands.command()
    async def view_blacklisted_words(self, ctx):
        if ctx.author.id == 264034992970006528:
            blacklist = utils.get_blacklist()
            await ctx.send(", ".join(blacklist))

    @commands.command()
    async def clear(self, ctx, number:int):
        await ctx.channel.purge(limit=number)

    @commands.command()
    async def servers(self, ctx):
        await ctx.send(str(len(self.client.guilds)))

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))