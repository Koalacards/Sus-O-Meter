import discord
from discord.ext import commands, tasks
from confidential import RUN_ID, DBL_TOKEN
import topgg

intents = discord.Intents.default()
intents.messages = True

client = commands.Bot(command_prefix=".", intents=intents)
client.topggpy = topgg.DBLClient(client, DBL_TOKEN)

client.load_extension('cogs.admincommands')
client.load_extension('cogs.meter')
client.load_extension('cogs.customlists')

@client.event
async def on_ready():
    guild_count = str(len(client.guilds))
    await client.change_presence(activity=discord.Game(name=f"/help in {guild_count} servers | Now with custom lists!"))
    update_stats.start()
    print("ready")

@client.command()
async def reloadCog(ctx, cog):
    if ctx.author.display_name == 'Koalacards':
        client.reload_extension(cog)
        await ctx.respond("Cog has been reloaded")
    else:
        await ctx.respond("You are not my creator")

@tasks.loop(minutes=30)
async def update_stats():
    guild_count = str(len(client.guilds))
    await client.change_presence(activity=discord.Game(name=f"/help in {guild_count} servers | Now with custom lists!"))
    try:
        await client.topggpy.post_guild_count()
        print(f"Posted server count ({client.topggpy.guild_count})")
    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

client.run(RUN_ID)
