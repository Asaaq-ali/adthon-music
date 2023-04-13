
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from sqlalchemy.exc import IntegrityError

from . import *
from Azazel import TEMP_SETTINGS
from Azazel.core.SQL.botlogsql import *
from Azazel.core.SQL.globals import *
from ubotlibs.ubot.utils.tools import get_arg
from .help import edit_or_reply

PMPERMIT = False

DEF_UNAPPROVED_MSG = (
"╔═════════════════════╗\n"
"ㅤ   ⚡️ اهلا بك ⚡️\n"
"╚═════════════════════╝\n"
"➣ انا مشغول حاليا\n"
"➣ سأرد عليك في اقرب وقت\n"
"╔═════════════════════╗\n"
"  ㅤ     ⚡@adthon⚡\n"
"     ㅤ  ✮سورس ادثون✮ㅤㅤ  \n"
"╚═════════════════════╝"
)


@Client.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def incomingpm(client: Client, message: Message):
    try:
        from Azazel.core.SQL.globals import gvarstatus
        from Azazel.core.SQL.pm_permit_sql import is_approved
    except BaseException:
        pass
      
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return
    if await auto_accept(client, message) or message.from_user.is_self:
        message.continue_propagation()
    if message.chat.id != 777000:
        PM_LIMIT = gvarstatus(str(user_id), "PM_LIMIT") or 5
        getmsg = gvarstatus(str(user_id), "unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

        apprv = is_approved(message.chat.id)
        if not apprv and message.text != UNAPPROVED_MSG:
            if message.chat.id in TEMP_SETTINGS["PM_LAST_MSG"]:
                prevmsg = TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                if message.text != prevmsg:
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=5,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    if TEMP_SETTINGS["PM_COUNT"][message.chat.id] < (int(PM_LIMIT) - 1):
                        ret = await message.reply_text(UNAPPROVED_MSG)
                        TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            else:
                ret = await message.reply_text(UNAPPROVED_MSG)
                if ret.text:
                    TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            if message.chat.id not in TEMP_SETTINGS["PM_COUNT"]:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = 1
            else:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = (
                    TEMP_SETTINGS["PM_COUNT"][message.chat.id] + 1
                )
            if TEMP_SETTINGS["PM_COUNT"][message.chat.id] > (int(PM_LIMIT) - 1):
                await message.reply("**Maaf anda Telah Di Blokir Karna Spam Chat**")
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                await client.block_user(message.chat.id)

    message.continue_propagation()


async def auto_accept(client, message):
    try:
        from Azazel.core.SQL.pm_permit_sql import approve, is_approved
    except BaseException:
        pass

    if message.chat.id in DEVS:
        try:
            approve(message.chat.id)
            await client.send_message(
                message.chat.id,
                f"<b>Menerima Pesan!!!</b>\n{message.from_user.mention} <b>Terdeteksi Developer Azazel-Project</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except IntegrityError:
            pass
    if message.chat.id not in [client.me.id, 777000]:
        if is_approved(message.chat.id):
            return True

        async for msg in client.get_chat_history(message.chat.id, limit=1):
            if msg.from_user.id == client.me.id:
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                try:
                    approve(chat.id)
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=5,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    return True
                except BaseException:
                    pass

    return False


@Ubot(["قبول", "y"], "")
async def approvepm(client, message):
    try:
        from Azazel.core.SQL.pm_permit_sql import approve
    except BaseException:
        await message.edit("شغل وضع الحماية اولا!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("لا يمكنك الموافقة على نفسك.")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit(
                "انت لست في وضع الحماية او ترد على رسالة احدهم."
            )
            return
        name0 = aname.first_name
        uid = aname.id

    try:
        approve(uid)
        await message.edit(f"**تم السماح بتلقي الرسائل من** [{name0}](tg://user?id={uid})!")
    except IntegrityError:
        await message.edit(
            f"[{name0}](tg://user?id={uid}) تمت الموافقة عليه كمن قبل."
        )
        return


@Ubot(["رفض", "n"], "")
async def disapprovepm(client, message):
    try:
        from Azazel.core.SQL.pm_permit_sql import dissprove
    except BaseException:
        await message.edit("فعل وضع الحماية اولا!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("لا يمكنك رفض نفسك.")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit(
                "انت لست في وضع الحماية او ترد على رسالة احدهم.."
            )
            return
        name0 = aname.first_name
        uid = aname.id

    dissprove(uid)

    await message.edit(
        f"**تم رفضه** [{name0}](tg://user?id={uid}) **يرجى عدم ارسال رسائل غير مرغوب بها!**"
    )


@Ubot(["تحذير"], "")
async def setpm_limit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.edit(
            f"**يجب عليك تعيين فار** `PM_AUTO_BAN` **ل** `True`\n\n**إذا كنت تريد تفعيل الحماية , يرجى كتابة:** `{cmd}setvar PM_AUTO_BAN True`"
        )
    try:
        from Azazel.core.SQL.globals import addgvar
    except AttributeError:
        await message.edit("**تأكد من وضع الحماية!**")
        return
    input_str = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not input_str:
        return await message.edit("**الرجاء إدخال رقم لـ PM_LIMIT.**")
    biji = await message.reply("`Processing...`")
    if input_str and not input_str.isnumeric():
        return await biji.edit("**الرجاء إدخال رقم لـ PM_LIMIT.**")
    addgvar(str(user_id), "PM_LIMIT", input_str)
    await biji.edit(f"**تم وضع عدد التحذيرات ل** `{input_str}`")


@Ubot(["الحماية", ""], "")
async def onoff_pmpermit(client: Client, message: Message):
    input_str = get_arg(message)
    user_id = client.me.id
    
    if not input_str:
        await edit_or_reply(message, "**استخدم الامر**: `الحماية` تفعيل او نعطيل")
        return
    
    if input_str == "تعطيل":
        h_type = False
    elif input_str == "تفعيل":
        h_type = True
        
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        PMPERMIT = False
    else:
        PMPERMIT = True
        
    if PMPERMIT and h_type:
        await edit_or_reply(message, "**الحمايى مفعلة بالفعل**")
    elif PMPERMIT and not h_type:
        delgvar(str(user_id), "PMPERMIT")
        await edit_or_reply(message, "**الحماية تم الاغلاق بنجاح**")
    elif not PMPERMIT and h_type:
        addgvar(str(user_id), "PMPERMIT", h_type)
        await edit_or_reply(message, "**الحماية تم تفعيله بنجاح**")
    else:
        await edit_or_reply(message, "**الحماية تم إيقاف تشغيله**")


@Ubot(["وضعر"], "")
async def setpmpermit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.reply(
            "**يجب عليك تعيين فار** `PM_AUTO_BAN` **ل** `True`\n\n**إذا كنت تريد تنشيط الحماية أرجوك أكتب:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import Azazel.core.SQL.globals as sql
    except AttributeError:
        await message.edit("**تأكد من تشغيل الحماية!**")
        return
    tai = await message.reply("`انتظر...`")
    nob = sql.gvarstatus(str(user_id), "unapproved_msg")
    message = message.reply_to_message
    if nob is not None:
        sql.delgvar(str(user_id), "unapproved_msg")
    if not message:
        return await tai.edit("**الرجاء الرد على الرسالة**")
    msg = message.text
    sql.addgvar(str(user_id), "unapproved_msg", msg)
    
    await tai.edit("**تم حفظ الرسالة بنجاح**")


@Ubot(["جلبر"], "")
async def get_pmermit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.edit(
            "**يجب عليك تعيين فار** `PM_AUTO_BAN` **ل** `True`\n\n**إذا كنت تريد تنشيط الحماية أرجوك أكتب:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import Azazel.core.SQL.globals as sql
    except AttributeError:
        await message.edit("***تأكد من تشغيل الحماية!**")
        return
    zel = await message.reply("`انتظر...`")
    nob = sql.gvarstatus(str(user_id), "unapproved_msg")
    if nob is not None:
        await zel.edit("**Pesan PMPERMIT Yang Sekarang:**" f"\n\n{nob}")
    else:
        
        await zel.edit(
            "**لم تقم باعداد رسالة حماية مخصصة,**\n"
            f"**رسالة الحماية الاساسية:**\n\n{DEF_UNAPPROVED_MSG}"
        )


@Ubot(["ريست"], "")
async def reset_pmpermit(client, message):
    user_id = client.me.id
    if gvarstatus(str(user_id), "PMPERMIT") and gvarstatus(str(user_id), "PMPERMIT") == "false":
        return await message.edit(
            f"**يجب عليك تعيين فار** `PM_AUTO_BAN` **ل** `True`\n\n**إذا كنت تريد تنشيط الحماية أرجوك أكتب:** `{cmd}setvar PM_AUTO_BAN True`"
        )
    try:
        import Azazel.core.SQL.globals as sql
    except AttributeError:
        await message.edit("**تأكد من الحماية!**")
        return
    sok = await message.reply("`انتظر...`")
    nob = sql.gvarstatus(str(user_id), "unapproved_msg")

    if nob is None:
        await sok.edit("**تم اعادة رسالة الحماية الافتراضية**")
    else:
        sql.delgvar(str(user_id), "unapproved_msg")
        
        await sok.edit("**تم تغيير رسالة الحماية بنجاح**")


add_command_help(
    "الحماية",
    [
        [
            f"قبول او y",
            "للسماح للشخص بالتحدث",
        ],
        [
            f"رفض او g",
            "برفض الشخص من التحدث",
        ],
        [
            "تحذير والرقم",
            "لوضع عدد الرسائل للشخص قبل القبول",
        ],
        [
            "وضعر بالرد على الرسالة>",
            "لوضع رسالة الحماية.",
        ],
        [
            "جلبر",
            "لعرض رسالة الحماية",
        ],
        [
            "ريست",
            "لاعادة تعيين رسالة الحماية",
        ],
        [
            "الحماية [تفعيل/تعطيل]",
            "لتشغيل او ايقاف الحماية",
        ],
    ],
)
