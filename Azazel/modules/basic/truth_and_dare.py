

import asyncio
import random

import Azazel.modules.basic.truth_and_dare_string as tod

from . import *


# LU GABISA CODING LU KONTOL
# BELAJAR CODING DARI NOL
@Ubot(["سؤال"], "")
async def apakah(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.AP)}")



@Ubot(["سؤال2"], "")
async def kenapa(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.KN)}")


@Ubot(["سؤال3"], "")
async def bagaimana(client, message):
    split_text = message.text.split(None, 1)
    if len(split_text) < 2:
        return await message.reply("Berikan saya pertanyaan 😐")
    cot = split_text[1]
    await message.reply(f"{random.choice(tod.BG)}")


@Ubot(["تحدي"], "")
async def dare(client, message):
    try:        
        await message.edit(f"{random.choice(tod.DARE)}")
    except BaseException:
        pass


@Ubot(["كت"], "")
async def truth(client, message):
    try:
        await message.edit(f"{random.choice(tod.TRUTH)}")
    except Exception:
        pass


add_command_help(
    "الالعاب",
    [
        [f"تحدي", "جربه بنفسك"],
        [f"كت", "جربه بنفسك"],
        [f"سؤال [سؤال]", "جربه بنفسك"],
        [f"سؤال2 [سؤال]", "جربه بنفسك"],
        [f"سؤال3 [سؤال]", "جربه بنفسك"],
    ],
)

add_command_help(
    "سؤال",
    [
         [f"سؤال [سؤال]", "جربه بنفسك"],
        [f"سؤال2 [سؤال]", "جربه بنفسك"],
        [f"سؤال3 [سؤال]", "جربه بنفسك"],
    ],
)
        
