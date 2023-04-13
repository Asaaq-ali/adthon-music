
import os
import sys
from re import sub
import asyncio
from time import time
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from . import *
from ubotlibs.ubot.helper.basic import eor
from .profile import extract_user, extract_userid

admins_in_chat = {}

unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason

@Client.on_message(filters.command(["وضع قر"], "") & filters.me)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.reply("ليس لديك الاذن لتغير الصورة!")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit("قم بالرد على الصورة يا ذكي!")



@Client.on_message(filters.command(["طرد", "سماش"], "") & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ky = await message.reply("`جاري طدر هذا الغبي...`")
    if not user_id:
        return await ky.edit("والله شكلك انت الغبي تأكد من المعرف.")
    if user_id == client.me.id:
        return await ky.edit("صدق انك غبي بتطرد نفسك؟!.")
    if user_id in DEVS:
        return await ky.edit("حدودك ما تقدر تحظر المطور!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ky.edit("ما تقدر تحظر ادمن يا حلو.")
    try:
        
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    msg = f"المحظور:** {mention}\n**الي حاظره :** {message.from_user.mention}\n"
    if reason:
        msg += f"**السبب:** {reason}"
    try:
        await message.chat.ban_member(user_id)
        await ky.edit(msg)
    except ChatAdminRequired:
        return await ky.edit("**تأكد من صلاحياتك !**")



@Client.on_message(filters.command(["الغاء حظر"], "رجعه") & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    zz = await message.reply("`انتظر...`")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await zz.edit("مو قادر الغي حظره")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await zz.edit(
            "حبيب حط اليوزر صح او رد على رسالة من المحظور."
        )
    try:
        await message.chat.unban_member(user)
        await asyncio.sleep(0.1)
        
        umention = (await client.get_users(user)).mention
        await zz.edit(f"متأكد انه محظور! {umention}")
    except ChatAdminRequired:
        return await zz.edit("**لا تسوي خوي تراك مو ادمن !**")



@Client.on_message(filters.command(["تث", "غتث"], "") & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await message.reply("حبيبي رد على اي رسالة بكلمة تث عشان تثبتها او غتث لالغاء تثبينها .")
    await message.edit("`انتظر...`")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.edit(
            f"**تم الغاء تثبيت [this]({r.link}) الرسالة.**",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await message.edit(
            f"**تم تثبيت [this]({r.link}) الرسالة.**",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await message.edit("**لا تسوي خوي تراك مو ادمن !**")


@Client.on_message(filters.command(["اخرس"], "كتم") & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    nay = await message.reply("`انتظر...`")
    if not user_id:
        return await nay.edit("تأكد من المعرف .")
    if user_id == client.me.id:
        return await nay.edit("ايش هذا ايش انت؟ بتكم نفسك.")
    if user_id in DEVS:
        return await nay.edit("حدودك على المطور!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await nay.edit("ياخي تعبتني تراه ادمن.")
    
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**الي خرسته:** {mention}\n"
        f"**الي خلاني اخرسه:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**السبب:** {reason}"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await nay.edit(msg)
    except ChatAdminRequired:
        return await nay.edit("**كم مرة قلت لك لا تسوي خوي صير ادمن واستخدم الامر !**")



@Client.on_message(filters.command(["الغاء كتم"], "تكلم") & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    kl = await message.reply("`انتظر...`")
    if not user_id:
        return await kl.edit("لم يتم العثور على المستخدم.")
    try:
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)
        
        umention = (await client.get_users(user_id)).mention
        await kl.edit(f"مو مكتوم! {umention}")
    except ChatAdminRequired:
        return await kl.edit("**لا تسوي خوي تراك مو ادمن  !**")


@Client.on_message(filters.command(["طرد", "انقلع"], "") & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    ny = await message.reply("`انتظر...`")
    if not user_id:
        return await ny.edit("تأكد من المعرف.")
    if user_id == client.me.id:
        return await ny.edit("بتطرد نفسك؟.")
    if user_id == DEVS:
        return await ny.edit("تراه مطوري😑!.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ny.edit("ما اقدر اطرد ادمن.")
    
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**طردته:** {mention}
**الي امرني اطرده:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**السبب:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await ny.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await ny.edit("**لا تسوي خوي تراك مو ادمن  !**")


@Client.on_message(
    filters.group & filters.command(["مشرف", "رفع"], "") & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    biji = await message.reply("`انتظر...`")
    if not user_id:
        return await biji.edit("تأكد من من المعرف.")
    rd = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    try: 
        if message.command[0][0] == "f":
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            await asyncio.sleep(1)
            
            umention = (await client.get_users(user_id)).mention
            return await biji.edit(f"تم رفعه بكل الصلاحيات! {umention}")

        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await asyncio.sleep(1)
        
        umention = (await client.get_users(user_id)).mention
        await biji.edit(f"تم رفعه! {umention}")
    except ChatAdminRequired:
        return await biji.edit("**لا تسوي خوي تراك مو ادمن  !**")


@Client.on_message(
    filters.group
    & filters.command(["تنزيل"], [""])
    & filters.user(DEVS)
    & ~filters.me
)
@Client.on_message(filters.group & filters.command(["تنزيل"], "") & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    sempak = await message.reply("`انتظار...`")
    if not user_id:
        return await sempak.edit("تأكد من المعرف")
    if user_id == client.me.id:
        return await sempak.edit("يا غبي ما تقدر تنزل نفسك.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)
    
    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"نم التنزيل من الاشراف! {umention}")


add_command_help(
    "الادمن",
    [
        [f"حظر[بالرد/المعرف/الايدي]", "حظر الشخص."],
        [f"الغاء حظر[بالرد/المعرف/الايدي]", "الغاء الحظر عن الشخص.",],
        [f"طرد[بالرد/المعرف/الايدي]", "لطرد الشخص بدون حظر."],
        [f"مشرف او رفع .","لرفع الشخص مشرف بدون صلاحية اضافة مشرفين او مع الصلاحية .",],
        [f"تنزيل", "لتنزيل الشخص من الاشراف."],
        [f"كتم [بالرد/المعرف/الايدي]","لكتم الشخص.",],
        [f"الغاء كتم [بالرد/المعرف/الايدي]","لالغاء الكتم عن الشخص.",],
        [f"تث [بالرد]","لتثبيت الرسالة.",],
        [f"غتث [بالرد]","لالغاء تثبيت الرسالة.",],
        [f"وضع قر [بالرد على الصورة]","لوضع او تغيير صورة القروب",],
    ],
)
