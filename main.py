import os
import io
import re

from telethon import TelegramClient, events
from telethon.events import newmessage
from telethon.tl.types import DocumentAttributeFilename
from dotenv import load_dotenv
from icecream import ic

from utils import log
import yandex_parser

MANDATORY_ENVIRONMENTS = ["APP_ID", "APP_HASH", "BOT_TOKEN"]


def load_environment():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        for var in MANDATORY_ENVIRONMENTS:
            if var not in os.environ:
                log.error(".env doesn't contain required settings")
                exit(-1)
    else:
        log.error(".env file doesn't exist")
        exit(-1)


load_environment()

api_id = int(os.getenv('APP_ID'))
api_hash = os.getenv('APP_HASH')
bot_token = os.getenv('BOT_TOKEN')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event: newmessage.NewMessage.Event):
    bot.parse_mode = 'html'
    await event.respond("Music Bot v. 0.1\n\n"
                        "Get Yandex Music Playlist:\n"
                        "<code>/ym user=[user id] playlist=[number]</code>")


@bot.on(events.NewMessage(pattern='/ym'))
async def start(event: newmessage.NewMessage.Event):
    arguments_string = re.sub(r'\s+=\s+', '=', event.message.text.replace("/ym", "")).split()
    ic(arguments_string)
    try:
        arguments_dict = dict(s.split('=', 1) for s in arguments_string)
    except:
        arguments_dict = {}

    if not {"user", "playlist"} <= arguments_dict.keys():
        bot.parse_mode = 'html'
        await event.respond("Get Yandex Music Playlist:\n"
                            "<code>/ym user=[user id] playlist=[number]</code>")
        return

    playlist, tracks_count = yandex_parser.get_yandex_music_playlist(arguments_dict["user"], arguments_dict["playlist"])

    if tracks_count > 0:
        bytes_file = io.BytesIO(playlist.encode())
        att = [DocumentAttributeFilename(file_name='playlist.txt')]
        await bot.send_file(event.input_sender, caption=f'Tracks: {tracks_count}', file=bytes_file, attributes=att)
    else:
        await event.respond("Can't fetch a playlist")


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()


