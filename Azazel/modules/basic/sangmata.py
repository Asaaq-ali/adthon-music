

import asyncio
from pyrogram import Client
from pyrogram.errors import YouBlockedUser
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.utils import extract_user

@Ubot(["سجل"], "")
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await message.edit_text("`انتظر...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"`الرجاء تحديد مستخدم صالح!`")
    bot = "SangMata_beta_bot"
    try:
        await client.send_message(bot, f"/search_id {user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"/search_id {user.id}")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot, query="Name", limit=1):
        if not stalk:
            await message.edit_text("**لم يغير اسمه ابدا**")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()

    async for stalk in client.search_messages(bot, query="Username", limit=1):
        if not stalk:
            return
        elif stalk:
            await message.reply(stalk.text)
            await stalk.delete()


add_command_help(
    "السجل",
    [
        [f"سجل [بالرد/الايدي/المعرف]",
            "استرداد معلومات سجل المستخدم.",
        ],
    ],
)
