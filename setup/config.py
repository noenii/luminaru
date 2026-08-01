import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "."

E_C_1 = 0xf2e9e4
E_C_2 = 0xc9ada7
E_C_3 = 0x9a8c98
E_C_4 = 0x4a4e69
E_C_5 = 0x22223b

EMBED_COLOR = 16566995
# 0x242429
# 16566995
# 0x36393F is embed color i think

DEV = ["owner", "dev", "staff"]

SUCCESS = "<:blue_thumbs_up:1488855820027428934>"
ERROR = "<:nailbite:1490755652333731870>"
WARNING = "<:Angry:1488856055717822524>"
LOADING = "<:loading:1490220248475893892>"

IMP_ROLES = {
    "owner": 1488555248795783208,
    "dev": 1494548120317595650,
    "admin": 1488558448512598037,
    "mod": 1488557110206922893,
    "pm": 1489828092888486059,
    "im": 1489650271452790885,
    "staff": 1488557028141170718,
    "botp": 1488553447253868726,
    "vip": 1488777445078204462,
    "og": 1425691136198184960,
    "pooks": 1488863033978650624
}
