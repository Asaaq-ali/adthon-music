
import asyncio
from pyrogram.types import *
from pyrogram import *

from . import *
from ubotlibs.ubot.helper import edit_or_reply

@Ubot(["ss"], "")
async def webshot(client, message):
    await message.edit("`انتظر...`")
    try:
        user_link = message.command[1]
        try:
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**لقطة شاشة للصفحة** {user_link}",
            )
        except Exception as dontload:
            await message.edit(f"Error! `{dontload}`\nحاول مرة أخرى لعمل لقطة شاشةr...")
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await client.send_photo(
                message.chat.id,
                full_link,
                caption=f"**لقطة شاشة للصفحة** `{user_link}`",
            )
        await ren.delete()
    except Exception as error:
        await ren.delete()
        await client.send_message(
            message.chat.id, f"**هناك شيء خاطئ\nالسجل:`{error}`...**"
        )

add_command_help(
    "ويبشوت",
    [
        [f"ss <الرابط'>", "للحصول على لقطة شاشة لصفحة ويب معينة",],
    ],
)
