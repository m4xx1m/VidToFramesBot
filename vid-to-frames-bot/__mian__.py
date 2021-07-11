import io
import os
import random
import string
import aiogram
import asyncio
import subprocess
TOKEN = ""
USERS: list[int] = [821461129, 704477361, 892616770, 374323262, 1772861589, 898331044]

bot = aiogram.Bot(TOKEN)
dp = aiogram.Dispatcher(bot)
loop = asyncio.get_event_loop()


async def do_process(file: io.BytesIO):
    dir_name = "".join(
        random.choice(string.ascii_uppercase+string.ascii_uppercase+string.digits) for _ in range(8)
    )
    os.mkdir(dir_name)
    _input_file = open(f"{dir_name}/input.mp4", "wb")
    _input_file.write(file.read())
    subprocess.Popen(
        args="ffmpeg"
    )


async def user_filter(message: aiogram.types.Message, func):
    if message.chat.id in USERS:
        await func()


async def do_chat_action(chat_id, action: str):
    while True:
        await bot.send_chat_action(chat_id, action)
        await asyncio.sleep(5)


async def start(message: aiogram.types.Message):
    await message.reply("<b>Hello</b>\nSend gif and wait zip file with frames")


async def go_process(message: aiogram.types.Message):
    if message.document.mime_type != "video/mp4":
        return
    file = io.BytesIO()
    file.name = "vid.mp4"

    # if message.document.file_size > 52428800:
    #     await message.reply("File > 50MB")
    #     return

    ms = await message.reply("<b>Downloading...</b>")
    await message.document.download(file)
    await ms.edit_text("<b>Processing...</b>")
    # out_file = await do_process(file)
    await ms.edit_text("<b>Uploading...</b>")
    task = loop.create_task(do_chat_action(message.chat.id, "upload_document"))
    await message.reply_video(file)
    await ms.delete()
    task.cancel()


async def main():
    dp.register_message_handler(go_process, chat)

if __name__ == '__main__':
    loop.run_until_complete(main)