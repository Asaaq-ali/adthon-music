
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import Message

from pyrogram.errors.exceptions.flood_420 import FloodWait
from . import *


@Client.on_message(filters.command("cدعوة", [""]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("دعوة", "") & filters.me)
async def inviteee(client: Client, message: Message):
    mg = await message.reply_text("`Adding Users!`")
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("`أعطني مستخدمين لإضافتهم! تحقق من قائمة الاوامر لمزيد من المعلومات!`")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"`تعذر إضافة مستخدمين!! \nالسبب : {e}`")
        return
    await mg.edit(f"تمت الاضافة بنجاح {len(user_list)} لهذه المجموعة او القناة!`")


@Client.on_message(filters.command("cاضافة", [""]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("اضافة", "") & filters.me)
async def inv(client: Client, message: Message):
    ex = await message.reply_text("`جاري التنفيذ . . .`")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await ex.edit_text(f"دعوة المستخدمين من {chat.username}")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        zxb = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in zxb:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except FloodWait as e:
                return
            except Exception as e:
                pass

@Client.on_message(filters.command("الرابط", "") & filters.me)
async def invite_link(client: Client, message: Message):
    um = await message.reply_text("`انتظر...`")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await um.edit(f"**الرابط الخاص:** {link}")
        except Exception:
            await um.edit("الإذن مرفوض")


add_command_help(
    "الدعوة",
    [
        [f"الرابط","يطلعرابط المجموعة الخاص. [لازم تكون مشرف]",],
        [f"دعوة @username", "اضافة المستخدم إلى المجموعة."],
        [f"اضافة @username", "سرقة اعضاء (يمكن يحظر حسابك انتبه)."],
    ],
)
