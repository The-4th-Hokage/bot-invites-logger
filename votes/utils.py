from datetime import datetime
import traceback
from django.conf import settings

from .discord import request_discord
from .discord.color import Color
from .discord.embeds import Embed
from .discord.naruto_api import naruto_api
import pytz

list_dict = {
    "Top.GG": "https://top.gg/images/dblnew.png",
    "Discordlist Space": "https://discordlist.space/img/apple-touch-icon.png",
    "Bots For Discord": "https://discords.com/bots/img/favicons/apple-touch-icon-57x57.png",
    "Discord Bot List": "https://discordbotlist.com/ms-icon-144x144.png",
    "Fates List": "https://fateslist.xyz/static/botlisticon.webp",
    "Blade Bot List": "https://bladebotlist.xyz/img/logo.png",
    "Void Bots": "https://voidbots.net/assets/img/logo.png",
    "Infinity": "https://i.imgur.com/d7rG4HS.png",
    "Discord Labs":"https://cdn.discordlabs.org/logo200.png",
    "Radar Bot Directory": "https://mcfacts.xyz/Images/RBD/botlistlogo.png",
    "Blist": "https://blist.xyz/main_site/staticfiles/main/assets/blist.png",
    "Botlist Me": "https://botlist.me/_nuxt/icons/icon_512x512.c1b789.png",
    "Motiondevelopment": "https://motiondevelopment.top/favicon.ico",
    "Rovelstars": "https://discord.rovelstars.com/assets/img/bot/logo-512.png",
    "Discord Services": "https://discordservices.net/icon.webp",
    "Discordz": "https://cdn.discordz.xyz/img/logo.png",

    "LOCAL": "https://i.imgur.com/vlBPK30.png",
}
site_dict = {
    "Top.GG": f"https://top.gg/bot/{settings.DISCORDBOTID}",
    "Discordlist Space": f"https://discordlist.space/bot/{settings.DISCORDBOTID}",
    "Bots For Discord": f"https://discords.com/bots/bot/{settings.DISCORDBOTID}",
    "Discord Bot List": f"https://discordbotlist.com/bots/{settings.DISCORDBOTID}",
    "Fates List": f"https://fateslist.xyz/bot/{settings.DISCORDBOTID}",
    "Blade Bot List": f"https://bladebotlist.xyz/bot/{settings.DISCORDBOTID}",
    "Void Bots": f"https://voidbots.net/bot/{settings.DISCORDBOTID}/",
    "Infinity": f"https://botlist.site/bots/{settings.DISCORDBOTID}",
    "Discord Labs":f"https://bots.discordlabs.org/bot/{settings.DISCORDBOTID}",
    "Radar Bot Directory": f"https://radarbotdirectory.xyz/bot/{settings.DISCORDBOTID}",
    "Blist": f"https://blist.xyz/bot/{settings.DISCORDBOTID}",
    "Botlist Me": f"https://botlist.me/bots/{settings.DISCORDBOTID}",
    "Motiondevelopment": f"https://motiondevelopment.top/bots/{settings.DISCORDBOTID}",
    "Rovelstars": f'https://discord.rovelstars.com/bots/{settings.DISCORDBOTID}',
    "Discord Services": f"https://discordservices.net/bot/{settings.DISCORDBOTID}",
    "Discordz": f"https://discordz.xyz/bot/{settings.DISCORDBOTID}",

    "LOCAL": "https://minato-namikaze.readthedocs.io/",
}


def message_me(voterid: int, site: str):
    IST = pytz.timezone("Asia/Kolkata")
    try:
        a = request_discord.discord_api_req("/users/@me/channels", "post", data={"recipient_id": int(voterid)})
        json = a.json()
        if json.get('message') is not None:
            return
        user_pfp = f'https://cdn.discordapp.com/avatars/{voterid}/{json["recipients"][0]["avatar"]}.gif?size=1024'
        embed = Embed(
            title=f"Thanks for voting me! on {site}",
            color=Color.random(),
            description=f'Thanks **<@!{json["recipients"][0]["id"]}>** (`{json["recipients"][0]["username"]}#{json["recipients"][0]["discriminator"]}`) for voting me! :heart: <:uzumaki:940993645593632808>',
            timestamp=datetime.now(IST),
        )
        embed.set_author(name=site,
                         url=site_dict[site],
                         icon_url=list_dict[site])
        embed.set_thumbnail(url=user_pfp)

        naruto_img = naruto_api()
        #DM
        request_discord.discord_api_req(
            f'/channels/{a.json()["id"]}/messages',
            "post",
            data={"embeds": [embed.to_dict(), naruto_img]},
        )
        
        #In the vote log channel
        request_discord.discord_api_req(
            f"/channels/{settings.CHANNEL_ID}/messages",
            "post",
            data={"embeds": [embed.to_dict()]},
        )
    except Exception as e:
        request_discord.discord_api_req(
            f"/channels/{settings.CHANNEL_ID}/messages",
            "post",
            data={"content": f"Error at vote webhook in **{e}**\n```\n{str(traceback.format_exc()).encode()}\n```"},
        )
