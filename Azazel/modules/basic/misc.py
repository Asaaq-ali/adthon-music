
import asyncio
import random
from datetime import datetime
from platform import python_version
from . import *
from ubotlibs.ubot.helper.PyroHelpers import ReplyCheck
from pyrogram import __version__, filters, Client
from pyrogram.types import Message
from config import ALIVE_PIC, ALIVE_TEXT
from Azazel import START_TIME, SUDO_USER, app
from Azazel.modules.bot.inline import get_readable_time, BOT_VER


alive_logo = ALIVE_PIC or ""

if ALIVE_TEXT:
   txt = ALIVE_TEXT
else:
    txt = (
         f"▰▱▰▱°▱▱°▱▰▱▰\n"
        f" ◉ **معلومات**\n\n"
        f" ◉ **فارات**: `{BOT_VER}`\n"
        f" ◉ **الوقت**: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f" ◉ **بايثون**: `{python_version()}`\n"
        f" ◉ **بايرو جرام**: `{__version__}`\n"
        f" ▰▱▰▱°▱▱°▱▰▱▰\n"
    )

@Client.on_message(filters.command(["حسابي"], "") & filters.me)
async def alive(client: Client, message: Message):
    bot_username = (await app.get_me()).username
    try:
        shin = await client.get_inline_bot_results(bot=bot_username, query=f"حسابي {id(message)}")
        await asyncio.gather(
            client.send_inline_bot_result(
                message.chat.id, shin.query_id, shin.results[0].id, reply_to_message_id=message.id
            )
        )
    except Exception as e:
        print(f"{e}")


@Ubot(["ايدي"], "")
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**ايدي الملف**: `{rep.audio.file_id}`"
            file_id += "**نوع الملف**: `صوتي`"

        elif rep.document:
            file_id = f"**ايدي الملف**: `{rep.document.file_id}`"
            file_id += f"**نوع الملف**: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"**ايدي الملف**: `{rep.photo.file_id}`"
            file_id += "**نوع الملف**: `صورة`"

        elif rep.sticker:
            file_id = f"**ايدي الملصق**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**حزمة الملصقات**: `{rep.sticker.set_name}`\n"
                file_id += f"**ايموجي**: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"** ملصق متحرك**: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "*** ملصق متحرك**: `False`\n"
            else:
                file_id += "**حزمة الملصقات**: __None__\n"
                file_id += "**ايموجي الملصق**: __None__"

        elif rep.video:
            file_id = f"**ايدي الملف**: `{rep.video.file_id}`\n"
            file_id += "**نوع الملف**: `فيديو`"

        elif rep.animation:
            file_id = f"**ايدي الملف**: `{rep.animation.file_id}`\n"
            file_id += "**نوع الملف**: `متحركة`"

        elif rep.voice:
            file_id = f"**ايدي الملف**: `{rep.voice.file_id}`\n"
            file_id += "**نوع الملف**: `فويس`"

        elif rep.video_note:
            file_id = f"**ايدي الملف**: `{rep.animation.file_id}`\n"
            file_id += "**نوع الملف**: `ملاحظة فيديو`"

        elif rep.location:
            file_id = "**الموقع**:\n"
            file_id += f"**خط الطول**: `{rep.location.longitude}`\n"
            file_id += f"**خط العرض**: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "**الموقع**:\n"
            file_id += f"**خط الطول**: `{rep.venue.location.longitude}`\n"
            file_id += f"**خط العرض**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**العنوان**:\n"
            file_id += f"**العنوان**: `{rep.venue.title}`\n"
            file_id += f"**مفصل**: `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = (
                f"**معرف المستخدم المعاد توجيهه**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"*الايدي**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**ايدي الرسالة**: `{message.reply_to_message.id}`"
        await message.reply(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                f"**معرف المستخدم المعاد توجيهه**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**الايدي**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**ايدي الرسالة**: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        await message.edit(user_detail)

    else:
        await message.edit(f"**ايدي الشات**: `{message.chat.id}`")
