import discord
from discord.ext import commands
from discord.ext import tasks
from discord_slash import SlashCommand
from confidential import RUN_ID, DBL_TOKEN
import topgg

client = commands.Bot("~~~")
slash= SlashCommand(client, sync_commands=True, override_type=True)
client.topggpy = topgg.DBLClient(client, DBL_TOKEN)

client.load_extension('cogs.admincommands')
client.load_extension('cogs.meter')
client.load_extension('cogs.customlists')

@client.event
async def on_ready():
    guild_count = str(len(client.guilds))
    await client.change_presence(activity=discord.Game(name=f"/help in {guild_count} servers | Now with user-sus-words command!"))
    update_stats.start()
    print("ready")

@client.command()
async def reloadCog(ctx, cog):
    if ctx.author.display_name == 'Koalacards':
        client.reload_extension(cog)
        await ctx.send("Cog has been reloaded")
    else:
        await ctx.send("You are not my creator")

@tasks.loop(minutes=30)
async def update_stats():
    guild_count = str(len(client.guilds))
    await client.change_presence(activity=discord.Game(name=f"/help in {guild_count} servers | Now with user-sus-words command!"))
    try:
        await client.topggpy.post_guild_count()
        print(f"Posted server count ({client.topggpy.guild_count})")
    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

client.run(RUN_ID)
