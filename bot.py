import discord
from discord.ext import commands
from discord_slash import SlashCommand
from confidential import RUN_ID

client = commands.Bot("~")
slash= SlashCommand(client, sync_commands=True, override_type=True)

client.load_extension('cogs.admincommands')
client.load_extension('cogs.meter')
client.load_extension('cogs.customlists')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/help | Now with nltk tokenization!"))
    print("ready")

@client.command()
async def reloadCog(ctx, cog):
    if ctx.author.display_name == 'Koalacards':
        client.reload_extension(cog)
        await ctx.send("Cog has been reloaded")
    else:
        await ctx.send("You are not my creator")

client.run(RUN_ID)
