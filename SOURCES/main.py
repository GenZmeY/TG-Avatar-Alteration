# tg-avatar-alteration is a service that automatically changes
# your telegram avatar during the day 
# Copyright (C) 2021 GenZmeY
# mailto: genzmey@gmail.com
#
# tg-avatar-alteration is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
import datetime
import sys
import pytz
import runpy

config = {}

config_path = "/etc/tg-avatar-alteration/config.py"
session_path = "/var/cache/tg-avatar-alteration/"

def init_config(path):
    global config
    conf_dict = runpy.run_path(sys.argv[1])
    conf_dict.setdefault("TIMEZONE", "Europe/Moscow")
    conf_dict.setdefault("OFFSET", 0)
    conf_dict.setdefault("IMG_EXT", "jpg")
    config = type("config", (dict,), conf_dict)(conf_dict)
    if int(config.OFFSET) < 0:
        config.OFFSET = int(config.OFFSET) % -1440
    else:
        config.OFFSET = int(config.OFFSET) % 1440

def minutes_total():
    current_datetime = datetime.datetime.now(pytz.timezone(config.TIMEZONE))
    current_time = current_datetime.replace(microsecond=0)
    start_of_the_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    offset = current_time - start_of_the_day
    seconds = offset.total_seconds()
    return int((seconds - (seconds % 60)) / 60)

async def main():
    index = minutes_total() + int(config.OFFSET)
    if index < 0:
        index = index + 1440
    elif index >= 1440:
        index = index - 1440
    filename = config.IMG_DIR + f'/{index:04}.' + config.IMG_EXT
    await client(DeletePhotosRequest(await client.get_profile_photos('me')))
    await client(UploadProfilePhotoRequest(await client.upload_file(filename)))
    print('Avatar changed: ' + filename)


if len(sys.argv) == 2:
    config_path = sys.argv[1]
elif len(sys.argv) >= 2:
    config_path = sys.argv[1]
    session_path = sys.argv[2]

init_config(config_path)
client = TelegramClient(session_path + '/' + config.PHONE, config.API_ID, config.API_HASH).start(phone=config.PHONE)

with client:
    client.loop.run_until_complete(main())

