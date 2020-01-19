# data.py | import data from lists
# Copyright (C) 2019  EraserBird, person_v1.32, hmmm

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

import logging
import logging.handlers
import os
import sys

import redis
from discord.ext import commands

import config

# define database for one connection
database = redis.Redis(host='localhost', port=6379, db=0)


# Database Format Definitions

# github:commit : sha

# prevJ - makes sure it sends a diff image
# prevB - makes sure it sends a diff bird (img)
# prevS - makes sure it sends a diff bird (sounds)
# prevK - makes sure it sends a diff sound

# server format = {
# channel:channel_id : { "bird", "answered", "sBird", "sAnswered",
#                     "goatsucker", "gsAnswered",
#                     "prevJ", "prevB", "prevS", "prevK" }
# }

# session format:
# session.data:user_id : {"start": 0, "stop": 0,
#                         "correct": 0, "incorrect": 0, "total": 0,
#                         "bw": bw, "state": state, "addon": addon}
# session.incorrect:user_id : [bird name, # incorrect]

# race format:
# race.data:ctx.channel.id : { 
#                    "start": 0
#                    "stop": 0,
#                    "limit": 10,
#                    "bw": bw,
#                    "state": state,
#                    "addon": addon,
#                    "media": media
# }
# race.scores:ctx.channel.id : [ctx.author.id, #correct]

# leaderboard format = {
#    users:global : [user id, # of correct]
#    users.server:server_id : [user id, # of correct]
# }

# streaks format = {
#    streak:global : [user id, current streak]
#    streak.max:global : [user id, max streak]
# }

# incorrect birds format = {
#    incorrect:global : [bird name, # incorrect]
#    incorrect.server:server_id : [bird name, # incorrect]
#    incorrect.user:user_id: : [bird name, # incorrect]
# }

# channel score format = {
#   score:global : [channel id, # of correct]
# }

# ban format:
#   banned:global : [user id, 0]


# setup logging
logger = logging.getLogger(config.NAME)
logger.setLevel(logging.DEBUG)
os.makedirs("logs", exist_ok=True)

file_handler = logging.handlers.TimedRotatingFileHandler(
    "logs/log.txt", backupCount=4, when="midnight")
file_handler.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(logging.Formatter(
    "{asctime} - {filename:10} -  {levelname:8} - {message}", style="{"))
stream_handler.setFormatter(logging.Formatter(
    "{filename:10} -  {levelname:8} - {message}", style="{"))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# log uncaught exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


class GenericError(commands.CommandError):
    """A custom error class.

    Error codes: (can add more if needed)\n
        0 - no code
        111 - Index Error
        201 - HTTP Error
        999 - Invalid
        990 - Invalid Input
        100 - Blank
        842 - Banned User
        666 - No output error
    """
    def __init__(self, message=None, code=0):
        self.code = code
        super().__init__(message=message)

# Error codes: (can add more if needed)
# 0 - no code
# 111 - Index Error
# 201 - HTTP Error
# 999 - Invalid
# 990 - Invalid Input
# 100 - Blank
# 842 - Banned User
# 666 - No output error

def _wiki_urls():
    logger.info("Working on wiki urls")
    urls = {}
    with open(f'data/wikipedia.txt', 'r') as f:
        for line in f:
            item = line.strip().split(',')[0].lower()
            url = line.strip().split(',')[1]
            urls[item] = url
    logger.info("Done with wiki urls")
    return urls


def get_wiki_url(item):
    item = item.lower()
    return wikipedia_urls[item]


def _generate_aliases():
    logger.info("Working on aliases")
    aliases = {}
    with open(f'data/dsos.txt', 'r') as f:
        for line in f:
            item = line.strip().split(',')[0].lower()
            try:
                alias = line.strip().split(',')[1].lower()
            except IndexError:
                alias = item
            aliases[item] = alias
    logger.info("Done with wiki urls")
    return aliases


def get_alias(item):
    item = item.lower()
    try:
        alias = aliases[item]
    except KeyError:
        alias = item
    return alias


def get_item_type(item: str):
    item = item.lower()
    if item in constellations:
        return "constellations"
    elif item in dsos:
        return "dsos"
    elif item in stars:
        return "stars"
    else:
        return None


def _lists():
    """Converts txt files of data into lists."""
    filenames = ("constellations", "dsos", "stars")
    # Converts txt file of data into lists
    lists = []
    for filename in filenames:
        logger.info(f"Working on {filename}")
        with open(f'data/{filename}.txt', 'r') as f:
            lists.append([line.strip().split(",")[0].lower() for line in f])
        logger.info(f"Done with {filename}")
    logger.info("Done with lists!")
    return lists

def _all_lists():
    """Compiles lists into master lists."""
    lists = (constellations, dsos, stars)
    master = []
    for data in lists:
        for item in data:
            master.append(item)
    return master


constellations, dsos, stars = _lists() # pylint: disable=unbalanced-tuple-unpacking
id_list = _all_lists()
wikipedia_urls = _wiki_urls()
aliases = _generate_aliases()
logger.info(
    f"List Lengths: {len(id_list)}")

logger.info("Done importing data!")
