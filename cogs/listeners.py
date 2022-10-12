import math
import os

import discord
from discord.ext import commands
from nltk.tokenize import word_tokenize
from PIL import Image, ImageDraw, ImageFont

import db.dbfunc as dbfunc
import utils
from vars import url_row


class Listeners(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        author_id, name = message.author.id, message.author.name
        if not dbfunc.auto_sus_id_on_list(author_id):
            return

        words = _sus_words_in_message(message)
        if words == {}:
            return

        guild_id = message.guild.id
        embed = _craft_embed(words, guild_id, name)

        img_path = _process_picture(name)
        file = discord.File(img_path, filename="image.png")
        embed.set_image(url=f"attachment://image.png")

        channel = message.channel
        await channel.send(file=file, embed=embed, view=url_row)

        await self.client.process_commands(message)

        _remove_picture(name)


def _craft_embed(words, guild_id, name):
    language = dbfunc.get_server_language(guild_id)
    title = ""
    description = ""
    colour = discord.Color.dark_orange()
    if language == "English":
        title = f"{name} is a sussy baka! :flushed:"
        description += f"In their last message, {name} said:\n\n"
    elif language == "Español":
        title = f"¡{name} es una sussy baka! :flushed:"
        description += f"En su último mensaje, {name} dijo:\n\n"

    count = 1

    for sus_word, word_count in words.items():
        if count > 50:
            break
        eng_times = "times" if word_count > 1 else "time"
        esp_times = "veces" if word_count > 1 else "vez"
        if language == "English":
            description += f"**{sus_word}**: {word_count} {eng_times}!\n"
        elif language == "Español":
            description += f"**{sus_word}**: {word_count} {esp_times}!\n"

        count += 1

    if language == "English":
        description += "**Type `/auto_sus` to enable/disable this feature!**"
    elif language == "Español":
        description += (
            "**¡Escriba `/auto_sus` para habilitar/deshabilitar esta característica!**"
        )

    embed = utils.create_embed(title, description, colour)

    return embed


def _sus_words_in_message(message: discord.Message):
    language = dbfunc.get_server_language(message.guild.id)
    list_type = dbfunc.get_server_list_type(message.guild.id)

    word_list = utils.get_sus_list()
    if language == "Español":
        word_list = utils.get_sus_list_spanish()
    if list_type == "Custom":
        word_list = utils.get_custom_list(message.guild.id)

    word_dict = {}
    content = message.content.lower()
    if content != "":
        try:
            content_words = word_tokenize(content)
            sus_content_filter = filter(lambda word: word in word_list, content_words)
            sus_words_in_message = list(sus_content_filter)
            for word in sus_words_in_message:
                previous_word_amount = word_dict.get(word, 0)
                word_dict[word] = previous_word_amount + 1
        except:
            return {}

    return utils.sort_dict(word_dict)


def _process_picture(name: str):
    length = len(name)
    font_size = 18 - math.ceil(length / 4)
    multiplier = font_size - 4

    img = Image.open("img/was_the_impostor.png")

    edit = ImageDraw.Draw(img)

    font = ImageFont.truetype("img/varela-round.regular.ttf", font_size)

    edit.text((200 - (length * multiplier), 152), name, font=font, fill=(255, 255, 255))

    base_width = 400
    wpercent = base_width / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.ANTIALIAS)

    img_path = f"img/{name}_was_the_impostor.png"

    img.save(img_path)

    return img_path


def _remove_picture(name: str):
    os.remove(f"img/{name}_was_the_impostor.png")


async def setup(bot):
    await bot.add_cog(Listeners(bot))
