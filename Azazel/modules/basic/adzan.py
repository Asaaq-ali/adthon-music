# Bacot Mulu Anjeng
import json
import requests
from pyrogram import Client
from pyrogram.types import Message
from . import *

@Ubot("اذان", "")
async def adzan_shalat(client: Client, message: Message):
    gay = message.text.split(" ", 1)[1]
    if not gay:
        await message.reply("<i>ادخل اسم مدينتك</i>")
        return True
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        await message.reply(f"<b>اسف لم اجد المدينة<code>{LOKASI}</code>")
    result = json.loads(request.text)
    bacot_kau = f"""
<b>جدول الصلاة {LOKASI}</b>
<b>تاريخ</b> <code>{result['items'][0]['date_for']}</code>
<b>مدينة</b> <code>{result['query']} | {result['country']}</code>

<b>الشروق  :</b> <code>{result['items'][0]['shurooq']}</code>
<b>الفجر :</b> <code>{result['items'][0]['fajr']}</code>
<b>الظهر  :</b> <code>{result['items'][0]['dhuhr']}</code>
<b>العصر  :</b> <code>{result['items'][0]['asr']}</code>
<b>المغرب :</b> <code>{result['items'][0]['maghrib']}</code>
<b>العشاء :</b> <code>{result['items'][0]['isha']}</code>
"""
    await message.reply(bacot_kau)

add_command_help(
    "الاذان",
    [
        [f"اذان <اسم المدينة بالانجليزي>", "لعرض اوقات الصلاة"],
    ],
)
