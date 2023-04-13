

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from . import *


@Ubot(["dm", "ارسال"], "")
async def dm(coli: Client, memek: Message):
    Ubot = await memek.reply("` جاري الارسال.....`")
    quantity = 1
    inp = memek.text.split(None, 2)[1]
    user = await coli.get_chat(inp)
    spam_text = ' '.join(memek.command[2:])
    quantity = int(quantity)

    if memek.reply_to_message:
        reply_to_id = memek.reply_to_message.message_id
        for _ in range(quantity):
            await Ubot.edit("تم الارسال !")
            await coli.send_message(user.id, spam_text,
                                      reply_to_messsge_id=reply_to_id)
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await coli.send_message(user.id, spam_text)
        await Ubot.edit("تم الارسال !")
        await asyncio.sleep(0.15)


add_command_help(
    "رسالة",
    [
        [f"dm @username الرسالة", "يرسل رسالة للمحادثة بدون ما تروح لها.",],
          [f"ارسال @username الرسالة", "يرسل رسالة للمحادثة بدون ما تروح لها.",],
    ],
)
