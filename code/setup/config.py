import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "."

EMBED_COLOR = 16566995

STAFF = ["owner", "dev", "staff"]

SUCCESS = "<:blue_thumbs_up:1488855820027428934>"
ERROR = "<:nailbite:1490755652333731870>"
WARNING = "<:Angry:1488856055717822524>"
LOADING = "<:loading:1490220248475893892>"
