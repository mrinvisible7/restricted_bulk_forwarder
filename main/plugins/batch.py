#Tg:mister_invisible/save_restricted
#Github. com/187dasharath

"""
Plugin for both public & private channels!
...................
"""
import logging
import time, os, asyncio

from .. import bot as Drone
from .. import userbot, Bot, AUTH, SUDO_USERS
#from .. import FORCESUB as fs
from main.plugins.pyroplug import check, get_bulk_msg
from main.plugins.helpers import get_link, screenshot

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

#from ethon.pyfunc import video_metadata
#from main.plugins.helpers import force_sub
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)
#ft = f"To use this bot you've to join @{fs}."

batch = []
ids = []

'''async def get_pvt_content(event, chat, id):
    msg = await userbot.get_messages(chat, ids=id)
    await event.client.send_message(event.chat_id, msg) 
'''   
@Drone.on(events.NewMessage(incoming=True, from_users=SUDO_USERS, pattern='/batch'))
async def _batch(event):
    '''
    #if not event.is_private:
    #    return
    # wtf is the use of fsub here if the command is meant for the owner? 
    # well am too lazy to clean 
    #s, r = await force_sub(event.client, fs, event.sender_id, ft) 
    #if s == True:
    #   await event.reply(r)
    #  return       
    '''
    s = False
    if f'{event.sender_id}' in batch:
        return await event.reply("You've already started one batch, wait for it to complete you dumbfuck owner!")
    async with Drone.conversation(event.chat_id) as conv: 
        if not s:
            await conv.send_message("Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("No link found.")
            except Exception as e:
                #print(e)
                logger.info(e)
                return await conv.send_message("Cannot wait more longer for your response!")
            await conv.send_message("Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                logger.info(e)
                #print(e)
                return await conv.send_message("Cannot wait more longer for your response!")
            try:
                value = int(_range.text)
                if value > 10000:
                    return await conv.send_message("You can only get upto 10000 files in a single batch.")
            except ValueError:
                return await conv.send_message("Range must be an integer!")
            for i in range(value):
                ids.append(i)
            s, r = await check(userbot, Bot, _link)
            if s != True:
                await conv.send_message(r)
                return
            batch.append(f'{event.sender_id}')
            cd = await conv.send_message("**Batch process ongoing.**\n\nProcess completed: ", 
                                    buttons=[[Button.inline("CANCEL❌", data="cancel")]])
            co = await run_batch(userbot, Bot, event.sender_id, cd, _link) 
            try: 
                if co == -2:
                    await Bot.send_message(event.sender_id, "Batch successfully completed!")
                    await cd.edit(f"**Batch process ongoing.**\n\nProcess completed: {value} \n\n Batch successfully completed! ")
            except:
                await Bot.send_message(event.sender_id, "ERROR!\n\n maybe last msg didnt exist yet")
            conv.cancel()
            ids.clear()
            batch.clear()

@Drone.on(events.callbackquery.CallbackQuery(data="cancel"))
async def cancel(event):
    ids.clear()
    
async def run_batch(userbot, client, sender, countdown, link):
    for i in range(len(ids)):
        timer = 60
        if i < 25:
            timer = 6
        elif i < 50 and i > 25:
            timer = 11
        elif i < 100 and i > 50:
            timer = 24
        elif i < 1250 and i > 1000:
            timer = 17
        elif i < 1500 and i > 1250:
            timer = 27
        elif i < 2000 and i > 1500:
            timer = 13
        elif i < 2500 and i > 2000:
            timer = 31
        elif i < 3000 and i > 2500:
            timer = 14
        elif i < 3500 and i > 3000:
            timer = 24
        elif i < 4000 and i > 3500:
            timer = 17
        elif i < 4500 and i > 4000:
            timer = 27
        elif i < 5000 and i > 4500:
            timer = 13
        elif i < 5500 and i > 5000:
            timer = 27
        elif i < 6000:
            timer = 11
        elif i < 6500:
            timer = 25
        elif i < 7000:
            timer = 17
        elif i < 7500:
            timer = 40
        elif i < 8000: 
            timer = 14
        elif i < 8500: 
            timer = 17
        elif i < 9000:
            timer = 15
        elif i < 9500: 
            timer = 32
        elif i < 10000: 
            timer = 17
        
        
        if 't.me/c/' not in link:
            timer = 2 if i < 25 else 3
        try: 
            count_down = f"**Batch process ongoing.**\n\nProcess completed: {i+1}"
            #a =ids[i]
            try:
                msg_id = int(link.split("/")[-1])
            except ValueError:
                if '?single' not in link:
                    return await client.send_message(sender, "**Invalid Link! .**")
                link_ = link.split("?single")[0]
                msg_id = int(link_.split("/")[-1])
            integer = msg_id + int(ids[i])
            await get_bulk_msg(userbot, client, sender, link, integer)
            protection = await client.send_message(sender, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
            await countdown.edit(count_down, 
                                 buttons=[[Button.inline("CANCEL❌", data="cancel")]])
            await asyncio.sleep(timer)
            await protection.delete()
        except IndexError as ie:
            await client.send_message(sender, f" {i}  {ie}  \n\nBatch ended completed!")
            await countdown.delete()
            break
        except FloodWait as fw:
            if int(fw.value) > 300:
                await client.send_message(sender, f'You have floodwaits of {fw.value} seconds, cancelling batch') 
                ids.clear()
                break
            else:
                fw_alert = await client.send_message(sender, f'Sleeping for {fw.value + 5} second(s) due to telegram flooodwait.')
                ors = fw.value + 5
                await asyncio.sleep(ors)
                await fw_alert.delete()
                try:
                    await get_bulk_msg(userbot, client, sender, link, integer)
                except Exception as e:
                    #print(e)
                    logger.info(e)
                    if countdown.text != count_down:
                        await countdown.edit(count_down, buttons=[[Button.inline("CANCEL❌", data="cancel")]])
        except Exception as e:
            #print(e)
            logger.info(e)
            await client.send_message(sender, f"An error occurred during cloning, batch will continue.\n\n**Error:** {str(e)}")
            if countdown.text != count_down:
                await countdown.edit(count_down, buttons=[[Button.inline("CANCEL❌", data="cancel")]])
        n = i + 1
        if n == len(ids):
            return -2
