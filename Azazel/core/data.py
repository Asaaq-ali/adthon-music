from pyrogram.types import InlineKeyboardButton, WebAppInfo
from Azazel import CMD_HNDLR as cmds
class Data:

    text_help_menu = (
        f"**قائمة المساعدة**\n** • البادئات** : `None`"
    )
    reopen = [[InlineKeyboardButton("Open", callback_data="reopen")]]
