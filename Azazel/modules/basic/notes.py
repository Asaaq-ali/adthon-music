from asyncio import sleep
from pyrogram import Client, filters
from Azazel.core.SQL.notesql import *
from Azazel.core.SQL.botlogsql import *
from pyrogram.types import Message
from ubotlibs.ubot.utils.tools import *
from . import *





@Ubot(["حفظ"], "")
async def simpan_note(client, message):
    keyword = get_arg(message)
    user_id = message.from_user.id
    msg = message.reply_to_message
    botlog_group_id = get_botlog(str(user_id))
    if not msg:
        return await message.reply("اكتب النص")
    anu = await msg.forward(botlog_group_id)
    msg_id = anu.id
    await client.send_message(botlog_group_id,
        f"#الملاحظات\nKEYWORD: {keyword}"
        "\n\nيتم تخزين الرسالة التالية كبيانات رد سجل للمحادثة , يرجى عدم حذفها !!!!",
    )
    await sleep(1)
    add_note(str(user_id), keyword, msg_id)
    await message.reply(f"Berhasil menyimpan note {keyword}")


@Ubot(["احضر"], "")
async def panggil_notes(client, message):
    notename = get_arg(message)
    user_id = message.from_user.id
    note = get_note(str(user_id), notename)
    botlog_group_id = get_botlog(str(user_id))
    if not note:
        return await message.reply("لا يوجد مثل هذا السجل.")
    msg_o = await client.get_messages(botlog_group_id, int(note.f_mesg_id))
    await msg_o.copy(message.chat.id, reply_to_message_id=message.id)


@Ubot(["حذف"], "")
async def remove_notes(client, message):
    notename = get_arg(message)
    user_id = message.from_user.id
    if rm_note(str(user_id), notename) is False:
        return await message.reply(
            "لا يمكن العثور على الملاحظة: {}".format(notename)
        )
    return await message.reply("تم حذف الملاحظة بنجاح: {}".format(notename))


@Ubot(["الملاحظات"], "")
async def list_notes(client, message):
    user_id = message.from_user.id
    notes = get_notes(str(user_id))
    if not notes:
        return await message.reply("لا ملاحظة.")
    msg = f"**قائمة الملاحظات**\n\n"
    for note in notes:
        msg += f"• {note.keyword}\n"
    await message.reply(msg)


add_command_help(
    "الملاحظات",
    [
        [f" حفظ [النص/الرد]",
            "احفظ الرسالة في المجموعة. (يمكن استخدام الملصقات)"],
        [f" احضر [الاسم]",
            "استرداد الملاحظات لحفظها"],
        [f" الملاحظات",
            "عرض قائمة الملاحظات"],
        [f" احذف [الاسم]",
            "حذف أسماء الملاحظات"],
    ],
)
