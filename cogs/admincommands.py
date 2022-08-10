import discord
from discord import app_commands
from discord.ext import commands

import db.dbfunc as dbfunc
import utils


class AdminCommands(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.id = 264034992970006528

    def check_if_it_is_me(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 264034992970006528

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def add_sus_word(self, interaction: discord.Interaction, word: str):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            sus_list = utils.get_sus_list()
            if word in sus_list:
                await interaction.response.send_message(
                    "word in sus list", ephemeral=True
                )
                return
            sus_list.append(word)
            dbfunc.set_sus_words(sus_list)
            await interaction.response.send_message(":thumbsup:", ephemeral=True)

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def add_sus_word_spanish(self, interaction: discord.Interaction, word: str):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            sus_list_spanish = utils.get_sus_list_spanish()
            if word in sus_list_spanish:
                await interaction.response.send_message(
                    "word in spanish sus list", ephemeral=True
                )
                return
            sus_list_spanish.append(word)
            dbfunc.set_sus_words_spanish(sus_list_spanish)
            await interaction.response.send_message(":thumbsup:", ephemeral=True)

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def remove_sus_word(self, interaction: discord.Interaction, word: str):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            try:
                sus_list = utils.get_sus_list()
                sus_list.remove(word)
                dbfunc.set_sus_words(sus_list)
                await interaction.response.send_message(":thumbsup:", ephemeral=True)
            except:
                await interaction.response.send_message(
                    "word does not exist in list", ephemeral=True
                )

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def remove_sus_word_spanish(
        self, interaction: discord.Interaction, word: str
    ):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            try:
                sus_list_spanish = utils.get_sus_list_spanish()
                sus_list_spanish.remove(word)
                dbfunc.set_sus_words_spanish(sus_list_spanish)
                await interaction.response.send_message(":thumbsup:", ephemeral=True)
            except:
                await interaction.response.send_message(
                    "word does not exist in list", ephemeral=True
                )

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def add_blacklisted_word(self, interaction: discord.Interaction, word: str):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            blacklist = utils.get_blacklist()
            if word in blacklist:
                await interaction.response.send_message(
                    "word in blacklist", ephemeral=True
                )
                return
            blacklist.append(word)
            dbfunc.set_blacklisted_words(blacklist)
            await interaction.response.send_message(":thumbsup:", ephemeral=True)

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def remove_blacklisted_word(
        self, interaction: discord.Interaction, word: str
    ):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            try:
                blacklist = utils.get_blacklist()
                blacklist.remove(word)
                dbfunc.set_blacklisted_words(blacklist)
                await interaction.response.send_message(":thumbsup:", ephemeral=True)
            except:
                await interaction.response.send_message(
                    "word does not exist in list", ephemeral=True
                )

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def view_blacklisted_words(self, interaction: discord.Interaction):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            blacklist = utils.get_blacklist()
            await interaction.response.send_message(
                ", ".join(blacklist), ephemeral=True
            )

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def servers(self, interaction: discord.Interaction):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        await interaction.response.send_message(
            str(len(self.client.guilds)), ephemeral=True
        )

    @app_commands.command()
    @app_commands.check(check_if_it_is_me)
    async def reloadCog(self, interaction: discord.Interaction, cog):
        """DEV COMMAND: Only useable by the creator of Sus-O-Meter"""
        if interaction.user.id == self.id:
            self.client.reload_extension(cog)
            await interaction.response.send_message(
                "Cog has been reloaded", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
