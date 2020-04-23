import sciolyid as bot

bot.setup(
    bot_description = "Star ID - A SciOly Discord Bot for aspiring astronomers",
    bot_signature = "Star ID - An Astronomy Bot",
    prefixes = ["s!", "s.", "s*", "S!", "S.", "S*"],
    id_type = "star",
    short_id_type = "st",
    name = "star-id",

    github_image_repo_url = "https://github.com/tctree333/Reach-For-The-Stars-Images.git",
    list_dir = "lists",
    wikipedia_file = "wikipedia.txt",
    alias_file = "aliases.txt",

    backups_channel = 703001356591693835,
    local_redis = False,

    logs = True,
    log_dir = "logs",
    file_folder = "bot_files",
    data_dir = "data",

    invite = "This bot is currently not avaliable outside the support server.",
    support_server = "https://discord.gg/Y2xwJSh",
    authors = "person_v1.32, with code from hmmm and EraserBird, and with help from Naddle and whaledemon",
    source_link = "https://github.com/tctree333/Reach-For-The-Stars-Bot",

    id_groups = True,
    category_name = "Space Thing",
    category_aliases = {"constellations": ["constellations", "constellation", "cst", "c"],
    "dsos": ["dsos", "dso", "d"],
    "stars": ["stars", "star", "s"]},

)

bot.start()