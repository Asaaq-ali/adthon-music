

import html
import time
import asyncio
from pyrogram import Client, enums
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.helper.basic import edit_or_reply
from ubotlibs.ubot.helper.parser import mention_html, mention_markdown


@Ubot(["ادمن"], "")
async def adminlist(client: Client, message: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    creator = []
    admin = []
    badmin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == enums.ChatMemberStatus.ADMINISTRATOR:
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == enums.ChatMemberStatus.OWNER:
            creator.append(mention_markdown(a.user.id, nama))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = "**قائمة الادن {}**\n".format(grup.title)
    teks += "**المالك**\n"
    for x in creator:
        teks += "• {}\n\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "\n**{} الادمنية**\n".format(len(admin))
    for x in admin:
        teks += "• {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "\n**{} ادمنية بوت**\n".format(len(badmin))
    for x in badmin:
        teks += "• {}\n".format(x)
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += "\n**عدد {} الادمن**".format(totaladmins)
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.reply(teks)


@Ubot(["زومبي"], "")
async def kickdel_cmd(client: Client, message: Message):
    kk = await message.reply("<b>Membersihkan akun depresi...</b>")
    try:
        values = [
            await message.chat.ban_member(
                member.user.id, datetime.now() + timedelta(seconds=31)
            )
            async for member in client.get_chat_members(message.chat.id)
            if member.user.is_deleted
        ]
    except Exception as e:
        return await message.edit(format_exc(e))
    await asyncio.sleep(0.1)
    await kk.delete()
    await message.edit(
        f"<b>Berhasil ditendang {len(values)} akun depresi (s)</b>"
    )


@Ubot("ابلاغ", "")
async def report_admin(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = None
    grup = await client.get_chat(message.chat.id)
    admin = []
    async for a in client.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        if (
            a.status == enums.ChatMemberStatus.ADMINISTRATOR
            or a.status == enums.ChatMemberStatus.OWNER
        ):
            if not a.user.is_bot:
                admin.append(mention_html(a.user.id, "\u200b"))
    if message.reply_to_message:
        if text:
            teks = "{}".format(text)
        else:
            teks = "{} أبلغت إلى المشرفين.".format(
                mention_html(
                    message.reply_to_message.from_user.id,
                    message.reply_to_message.from_user.first_name,
                )
            )
    else:
        if text:
            teks = "{}".format(html.escape(text))
        else:
            teks = " المشرفين {}.".format(grup.title)
    teks += "".join(admin)
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            teks,
            reply_to_message_id=message.reply_to_message.id,
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        await client.send_message(
            message.chat.id, teks, parse_mode=enums.ParseMode.HTML
        )


@Ubot("تاك", "")
async def tag_all_users(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = "اشتقنا🙃"
    kek = client.get_chat_members(message.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, "\u200b")
    if message.reply_to_message:
        await client.send_message(
            message.chat.id,
            text,
            reply_to_message_id=message.reply_to_message.id,
            parse_mode=enums.ParseMode.HTML,
        )
    else:
        await client.send_message(
            message.chat.id, text, parse_mode=enums.ParseMode.HTML
        )


@Ubot(["البوتات"], "")

async def get_list_bots(client: Client, message: Message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
        grup = await client.get_chat(chat)
    else:
        chat = message.chat.id
        grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.id
    getbots = client.get_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = a.user.first_name + " " + a.user.last_name
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, nama))
    teks = "**البوتات {}**\n".format(grup.title)
    teks += "بوتات\n"
    for x in bots:
        teks += "• {}\n".format(x)
    teks += "موجود في المجوعة {} من البوتات".format(len(bots))
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.reply(teks)

add_command_help(
    "الاعضاء",
    [
        [f"الادمن", "Get chats Admins list."],
        [f"زومبي", "To Kick deleted Accounts."],
        [f"البوتات","To get Chats Bots list"],
    ],
)