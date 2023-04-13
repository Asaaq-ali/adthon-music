# if you can read this, this meant you use code from Geez Ram Project
# this code is from somewhere else
# please dont hestitate to steal it
# because Geez and Ram doesn't care about credit
# at least we are know as well
# who Geez and Ram is
#
#
# kopas repo dan hapus credit, ga akan jadikan lu seorang developer
# ©2023 Geez & Ram Team
import time
import random
import speedtest
import asyncio
import re
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
from datetime import datetime
from . import DEVS, Ubot
from ubotlibs.ubot.helper.PyroHelpers import *
from Azazel import *

from Azazel.modules.bot.inline import get_readable_time

async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await apa(*args, **kwargs)


eor = edit_or_reply


class WWW:
    SpeedTest = (
        "بدأ قياس السرعة `{start}`\n"
        "البينج ➠ `{ping}` ms\n"
        "التنزيل ➠ `{download}`\n"
        "الرفع ➠ `{upload}`\n"
        "ISP ➠ __{isp}__"
    )

    NearestDC = "Country: `{}`\n" "Nearest Datacenter: `{}`\n" "This Datacenter: `{}`"
    
kopi = [
    "**يقدم السيد** 😍",
    "**اممموحح** 😘",
    "**حاضر** 🤗",
    "**لماذا السيد** 🥰",
    "**نعم سيدي لماذا?** 😘",
    "**السيد دالم** 🤗",
    "**انا السيد ?**",
]
    
    
@Ubot(["السرعة"], "")
async def speed_test(client: Client, message: Message):
    new_msg = await message.reply_text("`يتم قياس السرعة . . .`")
    try:
       await message.delete()
    except:
       pass
    spd = speedtest.Speedtest()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`الحصول على أفضل خادم يعتمد على البينج . . .`"
    )
    spd.get_best_server()

    new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "`اختبار سرعة التنزيل . . .`")
    spd.download()

    new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "`اختبار سرعة الرفع . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`الحصول على النتائج وإعداد التنسيق. . .`"
    )
    results = spd.results.dict()

    await new_msg.edit(
        WWW.SpeedTest.format(
            start=results["الزمن"],
            ping=results["البينج"],
            download=SpeedConvert(results["التنزيل"]),
            upload=SpeedConvert(results["الرفع"]),
            isp=results["client"]["isp"],
        )
    )

@Client.on_message(
    filters.command(["absen"], "") & filters.user(DEVS) & ~filters.me
)
async def absen(client: Client, message: Message):
    await message.reply_text(random.choice(kopi))


@Client.on_message(
    filters.command(["naya"], "") & filters.user(DEVS) & ~filters.me
)
async def naya(client, message):
    await message.reply_text("**Naya Punya Nya Kynan**🤩")

@Client.on_message(
    filters.command("بينج", [""]) & filters.user(DEVS) & ~filters.me
)
async def cpingme(client: Client, message: Message):
    """بينج المساعد"""
    mulai = time.time()
    akhir = time.time()
    await message.reply_text(
      f"**🏓 البينج!**\n`{round((akhir - mulai) * 1000)}ms`"
      )
      
@Client.on_message(
    filters.command(["cبينج"], "") & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["بينج"], "") & filters.me)
async def pingme(client, message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    ping_ = await client.send_message(client.me.id, "😈")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await message.reply_text(
        f"**Pong!**\n`%sms`\n" % (duration)
        )
    await ping_.delete()
  