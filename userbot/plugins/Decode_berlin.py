# berlin @UAETHON
""" Userbot module containing commands related to QR Codes. """

import os
import asyncio
import time
from datetime import datetime
import qrcode
import barcode
from barcode.writer import ImageWriter

from bs4 import BeautifulSoup

from userbot import CMD_HELP
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern=r"decode$", outgoing=True))
async def parseqr(qr_e):
    """ For .decode command, get QR Code/BarCode content from the replied photo. """
    downloaded_file_name = await qr_e.client.download_media(
        await qr_e.get_reply_message())
    # klanraloosh @aaaDa @telethon
    command_to_exec = [
        "curl", "-X", "POST", "-F", "f=@" + downloaded_file_name + "",
        "https://zxing.org/w/decode"
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
       
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
   
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    os.remove(downloaded_file_name)
    if not t_response:
        logger.info(e_response)
        logger.info(t_response)
        await qr_e.edit("Failed to decode.")
        return
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await qr_e.edit(qr_contents)


@borg.on(admin_cmd(pattern="barcode ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("...")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.barcode <long text to include>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await borg.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        os.remove(filename)
    except Exception as e:
        await event.edit(str(e))
        return
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Created BarCode in {} seconds".format(ms))
    await asyncio.sleep(5)
    await event.delete()

@borg.on(admin_cmd(pattern=r"makeqr(?: |$)([\s\S]*)", outgoing=True))
async def make_qr(makeqr):
    """ For .makeqr command, make a QR Code containing the given content. """
    input_str = makeqr.pattern_match.group(1)
    message = "SYNTAX: `.makeqr <long text to include>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(
                previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = ""
            for media in m_list:
                message += media.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await makeqr.client.send_file(makeqr.chat_id,
                                  "img_file.webp",
                                  reply_to=reply_msg_id)
    os.remove("img_file.webp")
    await makeqr.delete()


CMD_HELP.update({
    'barqrcodes':
    ".makeqr <content>\
\nUsage: Make a QR Code from the given content.\
\nExample: .makeqr www.google.com\n\n"
".barcode <content>\
\nUsage: Make a BarCode from the given content.\
\nExample: .barcode www.google.com\
\n\n**Note**: use .decode <reply to barcode/qrcode> to get decoded content."
})
