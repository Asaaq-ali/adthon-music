
from pyrogram import Client, filters
from pyrogram.types import Message
from telegraph import Telegraph, exceptions, upload_file
import os
from . import *
from ubotlibs.ubot.utils.tools import *


telegraph = Telegraph()
r = telegraph.create_account(short_name="telegram")
auth_url = r["auth_url"]


@Ubot(["tg", "تلي"], "")
async def uptotelegraph(client: Client, message: Message):
    tex = await message.edit_text("`انتظر . . .`")
    if not message.reply_to_message:
        await tex.edit(
            "**رد على الملف!**"
        )
        return
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await tex.edit(f"**ERROR:** `{exc}`")
            os.remove(m_d)
            return
        U_done = (
            f"**Uploaded on ** [Telegraph](https://telegra.ph/{media_url[0]})"
        )
        await tex.edit(U_done)
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await tex.edit(f"**خطأ:** `{exc}`")
            return
        wow_graph = f"**التحميل من ** [Telegraph](https://telegra.ph/{response['path']})"
        await tex.edit(wow_graph)


add_command_help(
    "تليجراف",
    [
        [
            f"تلي `او` tg",
            "للرفع على تليجراف.",
        ],
    ],
)
