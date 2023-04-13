
import asyncio
from asyncio import gather
from random import choice
from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from ubotlibs.ubot.helper import edit_or_reply, ReplyCheck
from . import *
from config import *


@Ubot(["asupan"], "")
async def asupan(client: Client, message: Message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    ky = await message.edit("`Mencari asupan... 🔎`")
    await gather(
        ky.delete(),
        client.send_video(
            message.chat.id,
            choice(
                [
                    asupan.video.file_id
                    async for asupan in client.search_messages(
                        "punyakenkan", filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )

# WARNING PORNO VIDEO THIS !!!

@Ubot(["Bokep"], "")
async def asupin(client: Client, message: Message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    ran = await message.edit("`Mencari bahan... 🔎`")
    await gather(
        ran.delete(),
        client.send_video(
            message.chat.id,
            choice(
                [
                    asupan.video.file_id
                    async for asupan in client.search_messages(
                        "bahaninimah", filter=enums.MessagesFilter.VIDEO
                    )
                ]
            ),
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Ubot(["Ayang"], "")
async def ay(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**لا يمكن استخدامه في قروب الدعم**")
    rizky = await message.edit("🔎 `البحث Ayang...`")
    await message.reply_photo(
        choice(
            [
                rz.photo.file_id
                async for rz in client.search_messages(
                    "CeweLogoPack", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"التحميل من : {client.me.mention}قناة جميلة : @L6_G6 ",
    )

    await rizky.delete()


@Ubot(["ppcp"], "")
async def pcp(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    darmi = await message.edit("🔎 `hgfpe PPCP...`")
    await message.reply_photo(
        choice(
            [
                ky.photo.file_id
                async for ky in client.search_messages(
                    "ppcpcilik", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"التحميل من : {client.me.mention}قناة جميلة : @L6_G6",
    )

    await darmi.delete()
    
    
@Ubot(["ppcp2"], "")
async def cp(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    dar = await message.edit("🔎 `البحث Ppcp 2...`")
    await message.reply_photo(
        choice(
            [
                cot.photo.file_id
                async for cot in client.search_messages(
                    "mentahanppcp", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"التحميل من : {client.me.mention}قناة جميلة : @L6_G6",
    )

    await dar.delete()
    
    
@Ubot(["anime"], "")
async def anim(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    iis = await message.edit("🔎 `البحث Anime...`")
    await message.reply_photo(
        choice(
            [
                jir.photo.file_id
                async for jir in client.search_messages(
                    "animehikarixa", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"التحميل من : {client.me.mention}قناة جميلة : @L6_G6",
    )

    await iis.delete()
    
   
@Ubot(["anime2"], "")
async def nimek(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    erna = await message.edit("🔎 `البحث Anime...`")
    await message.reply_photo(
        choice(
            [
                tai.photo.file_id
                async for tai in client.search_messages(
                    "Anime_WallpapersHD", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"التحميل من : {client.me.mention}قناة جميلة : @L6_G6",
    )

    await erna.delete()
    
    
@Ubot(["Bugil"], "")
async def bgst(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    nyet = await message.edit("🔎 `Search PP Bugil...`")
    await message.reply_photo(
        choice(
            [
                til.photo.file_id
                async for til in client.search_messages(
                    "durovbgst", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"Upload by {client.me.mention}",
    )

    await nyet.delete()
    
@Ubot(["pap"], "")
async def bugil(client, message):
    if message.chat.id in BL_UBOT:
        return await message.reply("**Tidak bisa di gunakan di Group Support**")
    kazu = await message.edit("🔎 `Nih PAP Nya...`")
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in client.search_messages(
                    "mm_kyran", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption="**Buat Kamu..**",
    )

    await kazu.delete()


add_command_help(
    "الصور", 
    [
        [f"pap", "صور عشوائية",],
        [f"ayang", "صور عشوائية."],
        [f"ppcp", "تطقيمات."],
        [f"ppcp2", "تطقيمات 2."],
        [f"anime", "صور انمي."],
        [f"anime2", "صور انمي 2."],
    ],
)
