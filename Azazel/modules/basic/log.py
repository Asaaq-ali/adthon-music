
import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from . import *
from Azazel.core.SQL import no_log_pms_sql
from Azazel.core.SQL.botlogsql import *
from Azazel.core.SQL.globals import *
from ubotlibs.ubot.utils.tools import get_arg



class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@Client.on_message(
    filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot
)
async def monito_p_m_s(client, message):
    chat_id = message.chat.id
    user_id = client.me.id
    botlog_group_id = get_botlog(str(user_id))
    if not botlog_group_id:
        return
    if gvarstatus(str(user_id), "PMLOG") and gvarstatus(str(user_id), "PMLOG") == "false":
        return
    if not no_log_pms_sql.is_approved(message.chat.id) and message.chat.id != 777000:
        if LOG_CHATS_.RECENT_USER != message.chat.id:
            LOG_CHATS_.RECENT_USER = message.chat.id
            if LOG_CHATS_.NEWPM:
                await LOG_CHATS_.NEWPM.edit(
                    LOG_CHATS_.NEWPM.text.replace(
                        "**💌 رسالة جديدة**",
                        f" • `{LOG_CHATS_.COUNT}` **رسالة**",
                    )
                )
                LOG_CHATS_.COUNT = 0
            LOG_CHATS_.NEWPM = await client.send_message(
                botlog_group_id,
                f"💌 <b><uالرسائل الجديدة التالية</u></b>\n<b> • من :</b> {message.from_user.mention}\n<b> • الايدي:</b> <code>{message.from_user.id}</code>",
                parse_mode=enums.ParseMode.HTML,
            )
        try:
            async for pmlog in client.search_messages(message.chat.id, limit=1):
                await pmlog.forward(botlog_group_id)
            LOG_CHATS_.COUNT += 1
        except BaseException:
            pass


@Client.on_message(filters.group & filters.mentioned & filters.incoming & ~filters.bot & ~filters.via_bot)
async def log_tagged_messages(client, message):
    chat_id = message.chat.id
    user_id = client.me.id
    botlog_group_id = get_botlog(str(user_id))
    if not botlog_group_id:
        return
    if gvarstatus(str(user_id), "GRUPLOG") and gvarstatus(str(user_id), "GRUPLOG") == "false":
        return
    if (no_log_pms_sql.is_approved(message.chat.id)):
        return
    result = f"📨<b><u>تم المنشن</u></b>\n<b> • من : </b>{message.from_user.mention}"
    result += f"\n<b> • القروب : </b>{message.chat.title}"
    result += f"\n<b> • 👀 </b><a href = '{message.link}'>عرض الرسائل</a>"
    result += f"\n<b> • الرسالة : </b><code>{message.text}</code>"
    await asyncio.sleep(0.5)
    await client.send_message(
        botlog_group_id,
        result,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@Ubot(["حفظ الخاص"], "")
async def set_pmlog(client, message):
    cot = get_arg(message)
    if cot == "off":
        noob = False
    elif cot == "on":
        noob = True
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMLOG") and gvarstatus(str(user_id), "PMLOG").value == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if noob:
            await message.edit("*تم تشغيل سجل الخاص*")
        else:
            delgvar(str(user_id), "PMLOG")
            await message.edit("**تم ايقاف سجل الخاص*")
    elif noob:
        addgvar(str(user_id), "PMLOG", noob)
        await message.edit("*تم ايقاف سجل الخاص**")
    else:
        await message.edit("**تم تشغيل سجل الخاص**")

@Ubot(["تخزين القروبات"], "")
async def set_gruplog(client, message):
    cot = get_arg(message)
    if cot == "off":
        noob = False
    elif cot == "on":
        noob = True
    user_id = client.me.id
    if gvarstatus(str(user_id), "GRUPLOG") and gvarstatus(str(user_id), "GRUPLOG").value == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if noob:
            await message.edit("**تم تشغيل سجل القروبات***")
        else:
            delgvar(str(user_id), "GRUPLOG")
            await message.edit("**تم ايقاف سجل القروبات***")
    elif noob:
        addgvar(str(user_id), "GRUPLOG", noob)
        await message.edit("**تم ايقاف سجل القروبات***")
    else:
        await message.edit("**تم تشغيل سجل القروبات***")

@Ubot("تخزين", "")
async def set_log(client, message):
    try:
        group_id = int(message.text.split(" ")[1])
    except (ValueError, IndexError):
        await message.reply_text("عليك تحديد قروب التخزين بالصيغة التالية : تخزين + ايدي القروب`.")
        return
    user_id = client.me.id
    chat_id = message.chat.id
    set_botlog(str(user_id), group_id)
    await message.reply_text(f"تم تعيين معرف مجموعة السجل على {group_id} لهذه المجموعة.")


add_command_help(
    "الحفظ",
    [
        [
            "تخزين",
            "قبل تشغيل سجل الخاص او تخزين القروبات ضع قروب التخزين بالامر : تخزين + ايدي القروب .",
        ],

    ],
)
