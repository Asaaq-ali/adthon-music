# Credits : Ayiin

from pyrogram import Client
from pyrogram.types import Message
from . import *
from ubotlibs.ubot.helper import get_arg

arguments = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8"
]

fonts = [
    "smallcap",
    "monospace",
    "outline",
    "script",
    "blackbubbles",
    "bubbles",
    "bold",
    "bolditalic"
]

_default = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_smallcap = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
_monospace = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
_outline = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
_script = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
_blackbubbles = "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
_bubbles = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
_bold = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
_bolditalic = "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"


def gen_font(text, new_font):
    new_font = " ".join(new_font).split()
    for q in text:
        if q in _default:
            new = new_font[_default.index(q)]
            text = text.replace(q, new)
    return text

@Ubot(["زخرفة"], "")
async def font_ubot(client, message):
    if message.reply_to_message or get_arg(message):
        font = get_arg(message)
        text = message.reply_to_message.text
        if not font:
            return await message.reply(f"<code>{font} فضلا تأكد من الصيغة مثل: زخرفة 1</code>")
        if font == "1":
            nan = gen_font(text, _smallcap)
        elif font == "2":
            nan = gen_font(text, _monospace)
        elif font == "3":
            nan = gen_font(text, _outline)
        elif font == "4":
            nan = gen_font(text, _script)
        elif font == "5":
            nan = gen_font(text, _blackbubbles)
        elif font == "6":
            nan = gen_font(text, _bubbles)
        elif font == "7":
            nan = gen_font(text, _bold)
        elif font == "8":
            nan = gen_font(text, _bolditalic)
        await message.reply(nan)
    else:
        return await message.reply("تمت الزخرفة!!!")


@Ubot(["الخطوط", "خط"], "")
async def fonts(client, message):
    await message.reply(
        "<b>قائمة الخطوط</b>\n\n"
        "<b>• 1 : ʏᴀʜʏᴀ</b>\n"
        "<b>• 2 : 𝚢𝚊𝚑𝚢𝚊</b>\n"
        "<b>• 3 : 𝕪𝕒𝕙𝕪𝕒</b>\n"
        "<b>• 4 : 𝓎𝒶𝒽𝓎𝒶</b>\n"
        "<b>• 5 : 🅨🅐🅗🅨🅐</b>\n"
        "<b>• 6 : ⓨⓐⓗⓨⓐ</b>\n"
        "<b>• 7 : 𝘆𝗮𝗵𝘆𝗮</b>\n"
        "<b>• 8 : 𝙮𝙖𝙝𝙮𝙖</b>\n\n"
    )


add_command_help(
    "الزخرفة",
    [
        [f"زخرفة + رقم من 1 - 8 [بالرد على الرسالة]", "يزخرف اي كلمة او اسم لعرض الخطوط اكب خط او خطوط"],
        [f"خط", "لعرض خطوط الزخرفة."],
        [f"خطوط", "لعرض خطوط الزخرفة."],
    ],
)
