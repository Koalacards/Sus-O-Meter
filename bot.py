import discord
import topgg
from discord import app_commands
from discord.ext import commands, tasks

from confidential import DBL_TOKEN, RUN_ID


class SusBot(commands.AutoShardedBot):
    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        await sus_bot.load_extension("cogs.admincommands")
        await sus_bot.load_extension("cogs.meter")
        await sus_bot.load_extension("cogs.customlists")
        await sus_bot.load_extension("cogs.listeners")
        await self.tree.sync()
        sus_bot.topggpy = topgg.DBLClient(sus_bot, DBL_TOKEN)

    async def on_ready(self):
        guild_count = str(len(sus_bot.guilds))
        await sus_bot.change_presence(
            activity=discord.Game(
                name=f"/help in {guild_count} servers | Now with sus-o-meter-server and leaderboard commands!"
            )
        )
        self.update_stats.start()
        print("ready")

    @tasks.loop(minutes=30)
    async def update_stats(self):
        guild_count = str(len(sus_bot.guilds))
        await sus_bot.change_presence(
            activity=discord.Game(
                name=f"/help in {guild_count} servers | Now with auto_sus commands!"
            )
        )
        try:
            await sus_bot.topggpy.post_guild_count()
            print(f"Posted server count ({sus_bot.topggpy.guild_count})")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
sus_bot = SusBot(command_prefix="~~~", intents=intents)


sus_bot.run(RUN_ID)
