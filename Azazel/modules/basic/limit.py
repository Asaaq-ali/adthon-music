
import asyncio
from pyrogram import Client, filters, raw
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.helper.basic import edit_or_reply


@Ubot(["تحقق"], "")
async def spamban(client: Client, m: Message):
    await client.unblock_user("SpamBot")
    response = await client.send(
        raw.functions.messages.StartBot(
            bot=await client.resolve_peer("SpamBot"),
            peer=await client.resolve_peer("SpamBot"),
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    mm = await m.reply_text("`انتظر شوي بشوف حسابك...`")
    await asyncio.sleep(1)
    spambot_msg = response.updates[1].message.id + 1
    status = await client.get_messages(chat_id="SpamBot", message_ids=spambot_msg)
    await mm.delete()
    await m.edit_text(f"~ {status.text}")

add_command_help(
    "تحقق الحساب",
    [
        [f"تحقق", "يشوف حسابك محظور او لا"],
    ],
)