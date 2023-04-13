
from pyrogram import Client, filters
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.helper import edit_or_reply



@Ubot(["buat", "انشاء"], "")
async def create(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply(f"**buat gc => لانشاء قروب, buat ch => لانشاء قناة**"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    xd = await message.edit("`[حاري المعالجة]...`")
    desc = "اهلا بي " + ("Group" if group_type == "gc" else "Group")
    if group_type == "gc":  # for supergroup
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"**تم إنشاء مجموعة Telegram بنجاح: [{group_name}]({link.invite_link})**",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":  # for channel
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"**تم إنشاء قناة Telegram بنجاح: [{group_name}]({link.invite_link})**",
            disable_web_page_preview=True,
        )




add_command_help(
    "الانشاء",
    [
        [f" اكتب buat gc او ch", "لانشاء قناة او مجموعة تلقائيا"],
    ],
)
