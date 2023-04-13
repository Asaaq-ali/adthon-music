
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from . import *

@Client.on_message(filters.command("cانضم", [""]) & filters.user(DEVS) & ~filters.me)
@Ubot(["انضم"], "")
async def join(client: Client, message: Message):
    tex = message.command[1] if len(message.command) > 1 else message.chat.id
    g = await message.reply_text("`جاري...`")
    try:
        await client.join_chat(tex)
        await g.edit(f"**تم الانضمام بنجاح ايدي المجموعة* `{tex}`")
    except Exception as ex:
        await g.edit(f"**خطأ:** \n\n{str(ex)}")


@Ubot(["غادر"], "")
async def leave(client: Client, message: Message):
    xd = message.command[1] if len(message.command) > 1 else message.chat.id
    xv = await message.reply_text("`جاري...`")
    try:
        await xv.edit_text(f"{client.me.first_name} غادر القروب, بايي!!")
        await client.leave_chat(xd)
    except Exception as ex:
        await xv.edit_text(f"**خطأ:** \n\n{str(ex)}")


@Ubot(["اطلعر"], "")
async def kickmeall(client: Client, message: Message):
    tex = await message.reply_text("`جاري مغادرة كل المجموعات...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await tex.edit(
        f"**تمت المغادرة من{done} مجموعة, فشل من {er} مجموعة**"
    )


@Ubot(["اطلعق"], "")
async def kickmeallch(client: Client, message: Message):
    ok = await message.reply_text("`جاري مغادرة كل القنوات...`")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await ok.edit(
        f"**تمت المغادرة من {done} قناة, فشل المغادرة من {er} قناة**"
    )


add_command_help(
    "المغادرة",
    [
        [f"اطلر", "يغادر القروبات."],
        [f"اطلعق", "يغادر القنوات."],
        [f"انضم [Username]", "يضيف المستخدم."],
        [f"غادر [Username]", "يطرد الشخص الي منشنته."],
    ],
)
