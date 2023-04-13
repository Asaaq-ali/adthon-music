
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.helper.basic import edit_or_reply
from ubotlibs.ubot.helper.PyroHelpers import ReplyCheck


@Ubot("ب", "")
async def salamone(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "السلام عليكم...",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Ubot("بي", "")
async def salamdua(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "السلام عليكم ورحمة الله وبركاته",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Ubot("l", "")
async def jwbsalam(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "وعليكم السلام...",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Ubot("ب1", "")
async def jwbsalamlngkp(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "وعليكم السلام ورحمة الله وبركاته",
            reply_to_message_id=ReplyCheck(message),
        ),
    )



@Ubot("اس", "")
async def salamarab(client: Client, message: Message):
    xx = await edit_or_reply(message, "تحياتي قبل الكهف..")
    await asyncio.sleep(2)
    await xx.edit("السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ")

add_command_help(
    "السلام",
    [
        [f"ب", "السلام عليكم."],
        [f"بي", "السلام عليكم ورحمة الله وبركاته."],
        [f"l", "وعليكم السلام."],
        [f"ب1", "وعليكم السلام ورحمة الله وبركاته."],
        [f"اس", "السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُه."],
    ]
)