
from asyncio import gather
from os import remove
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.helper.PyroHelpers import ReplyCheck
from ubotlibs.ubot.utils import extract_user


@Ubot(["ايديه"], "")
async def who_is(client: Client, message: Message):
    user_id = await extract_user(message)
    ex = await message.edit_text("`انتظر . . .`")
    if not user_id:
        return await ex.edit(
            "**قم بتوفير اليوزر /الايدي/ الرد للحصول على معلومات هذا المستخدم .**"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>معلوماته:</b>

🆔 <b>ايديه:</b> <code>{user.id}</code>
👤 <b>اسمه:</b> {first_name}
🗣️ <b>اسم العائلة:</b> {last_name}
🌐 <b>يوزره:</b> {username}
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🤖 <b>هو بوت؟:</b> <code>{user.is_bot}</code>
🚷 <b>محتال؟:</b> <code>{user.is_scam}</code>
🚫 <b>مقيد؟:</b> <code>{user.is_restricted}</code>
✅ <b>تحقق:</b> <code>{user.is_verified}</code>
⭐ <b>بريميوم:</b> <code>{user.is_premium}</code>
📝 <b>البايو:</b> {bio}

👀 <b>قروبات مشتركة:</b> {len(common)}
👁️ <b>اخر ظهور:</b> <code>{status}</code>
🔗 <b>رابط دائم للوصول له:</b> <a href='tg://user?id={user.id}'>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                ex.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await ex.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await ex.edit(f"**معلوماته:** `{e}`")


@Ubot(["كشف"], "")
async def chatinfo_handler(client: Client, message: Message):
    ex = await message.edit_text("`Processing...`")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.edit(
                    f"Use this command within a group or use .chatinfo [group username or id]`"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>CHAT INFORMATION:</b>

🆔 <b>ايدي:</b> <code>{chat.id}</code>
👥 <b>العنوان:</b> {chat.title}
👥 <b>اليوزر:</b> {username}
📩 <b>النوع:</b> <code>{type}</code>
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🗣️ <b>الغش:</b> <code>{chat.is_scam}</code>
🎭 <b>مزيف:</b> <code>{chat.is_fake}</code>
✅ <b>التحقق:</b> <code>{chat.is_verified}</code>
🚫 <b>مقيد:</b> <code>{chat.is_restricted}</code>
🔰 <b>محمي:</b> <code>{chat.has_protected_content}</code>

🚻 <b>عدد الاعضاء:</b> <code>{chat.members_count}</code>
📝 <b>البايو:</b>
<code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                ex.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await ex.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await ex.edit(f"**معلومات:** `{e}`")


add_command_help(
    "معلومات",
    [
        [f"ايديه <اليوزر/الايدي/المعرف>",
            "يجلب لك كل المعلومات عن الشخص.",
        ],
        [f"كشف <يوزر/ايدي/بالرد>",
            "يجلب لك كل معلومات القروب او القناة.",
        ],
    ],
)
