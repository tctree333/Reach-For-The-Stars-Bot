# media.py | commands for getting images
# Copyright (C) 2019-2020  EraserBird, person_v1.32, hmmm

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import itertools
import random

from discord.ext import commands

import config
from core import send_image
from data import database, id_list, logger, constellations, dsos, stars
from functions import channel_setup, error_skip, user_setup

ARG_MESSAGE = "**Recongnized arguments:** *Space Thing*: `{space_thing}`"

IMAGE_MESSAGE = (
    f"*Here you go!* \n**Use `{config.PREFIXES[0]}pic` again to get a new image of the same {config.ID_TYPE}, " +
    f"or `{config.PREFIXES[0]}skip` to get a new {config.ID_TYPE}. Use `{config.PREFIXES[0]}check [guess]` to check your answer. " +
    f"Use `{config.PREFIXES[0]}hint` for a hint.**"
)
aliases = {"constellations": ["constellations", "constellation", "cst", "c"],
           "dsos": ["dsos", "dso", "d"],
           "stars": ["stars", "star", "s"]}

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_pic_(self, ctx, space_thing):

        logger.info(f"{config.ID_TYPE}: " + str(database.hget(f"channel:{str(ctx.channel.id)}", "item"))[2:-1])

        answered = int(database.hget(f"channel:{str(ctx.channel.id)}", "answered"))
        logger.info(f"answered: {answered}")
        # check to see if previous item was answered
        if answered:  # if yes, give a new item
            space_thing = space_thing.lower()
            choices = []
            if space_thing in aliases["constellations"]:
                choices += constellations
                await ctx.send(ARG_MESSAGE.format(space_thing="Constellations"))
            elif space_thing in aliases["dsos"]:
                choices += dsos
                await ctx.send(ARG_MESSAGE.format(space_thing="Deep Sky Object"))
            elif space_thing in aliases["stars"]:
                choices += stars
                await ctx.send(ARG_MESSAGE.format(space_thing="Stars"))
            else:
                choices += id_list
                await ctx.send(ARG_MESSAGE.format(space_thing="None"))
            currentItem = random.choice(choices)
            prevB = str(database.hget(f"channel:{str(ctx.channel.id)}", "prevI"))[2:-1]
            while currentItem == prevB:
                currentItem = random.choice(choices)
            database.hset(f"channel:{str(ctx.channel.id)}", "prevI", str(currentItem))
            database.hset(f"channel:{str(ctx.channel.id)}", "item", str(currentItem))
            logger.info("currentItem: " + str(currentItem))
            database.hset(f"channel:{str(ctx.channel.id)}", "answered", "0")
            await send_image(ctx, currentItem, on_error=error_skip, message=IMAGE_MESSAGE)
        else:  # if no, give the same item
            await send_image(
                ctx,
                str(database.hget(f"channel:{str(ctx.channel.id)}", "item"))[2:-1],
                on_error=error_skip,
                message=IMAGE_MESSAGE
            )


    # Pic command - no args
    # help text
    @commands.command(help='- Sends a random image for you to ID', aliases=["p"])
    # 5 second cooldown
    @commands.cooldown(1, 5.0, type=commands.BucketType.channel)
    async def pic(self, ctx, space_thing=""):
        logger.info("command: pic")

        await channel_setup(ctx)
        await user_setup(ctx)

        
        await self.send_pic_(ctx, space_thing)


def setup(bot):
    bot.add_cog(Media(bot))
