
import os
import shutil

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message
from py_extract import Video_tools
from . import *


# Help
mod_name = os.path.basename(__file__)[:-3]


@Ubot(["صوت"], "")
async def extract_all_aud(client: Client, message: Message):
    replied_msg = message.reply_to_message
    geez = await message.reply("`تحميل الفيديو . . .`")
    ext_out_path = os.getcwd() + "/" + "downloads/py_extract/audios"
    if not replied_msg:
        await geez.edit("**الرجاء الرد على الفيديو**")
        return
    if not replied_msg.video:
        await geez.edit("**الرجاء الرد على الفيديو**")
        return
    if os.path.exists(ext_out_path):
        await geez.edit("جري المعالجة.....")
        return
    replied_video = replied_msg.video
    try:
        await geez.edit("`يتم التحميل...`")
        ext_video = await client.download_media(message=replied_video)
        await geez.edit("`يتم استخراج الصوت...`")
        exted_aud = Video_tools.extract_all_audio(input_file=ext_video, output_path=ext_out_path)
        await geez.edit("`يتم الرفع...`")
        for nexa_aud in exted_aud:
            await message.reply_audio(audio=nexa_aud, caption=f"`بواسطة` {(await client.get_me()).mention}")
        await geez.edit("`انتهى الاستخراج`")
        shutil.rmtree(ext_out_path)
    except Exception as e:
        await geez.edit(f"**خطأ:** `{e}`")
        
add_command_help(
    "الصيغ",
    [
        [f"صوت <بالرد على الفيديو>", "تحويل الفيديو الى صوت"],
    ],
)
