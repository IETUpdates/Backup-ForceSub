# (C) Arunkumar Shibu 

# January 15th 2022

import asyncio
from info import DB_CHANNEL, FSUB_CHANNEL, CHANNEL_LINK, LIST
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

async def copy_msg(msg):
    file = msg.document or msg.video
    name = file.file_name.split(".")[-1]
    if name in LIST: 
       return
    else:
       try:
           await msg.copy(DB_CHANNEL)
       except FloodWait as e:
           await asyncio.sleep(e.x)
           await msg.copy(DB_CHANNEL)

async def force_sub(bot, msg):
       try:
          member = await bot.get_chat_member(FSUB_CHANNEL, msg.from_user.id)
          if member.status == "banned":
            await msg.reply(f"Sorry {msg.from_user.mention}!\n You are banned in our channel, you will be banned from here within 10 seconds. Please Inform at @IET_Support")
            await asyncio.sleep(10)
            await bot.ban_chat_member(msg.chat.id, msg.from_user.id)
       except UserNotParticipant:
            await bot.restrict_chat_member(chat_id=msg.chat.id, 
                                           user_id=msg.from_user.id,
                                           permissions=ChatPermissions(can_send_messages=False)
                                           )
            await msg.reply(f"<b>Hello {msg.from_user.mention}😍!</b>\n\n<i>You have to join in our Leech Dump to message here and get files</i>", 
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Channel 🔥", url=CHANNEL_LINK)],
                                                               [InlineKeyboardButton("♻️ Try Again ♻️", callback_data="checksub")]])
                            )
       except Exception as e:
            print(e)

async def auto_delete(Bot, msg):
    chat, msg_id = msg.chat.id, msg.message_id
    try:       
       await asyncio.sleep(6000) # not tested, edit if you need
       await Bot.delete_messages(chat, msg_id)
    except Exception as e:
       print(e)

async def check_fsub(bot, update):
    try:
       user=update.message.reply_to_message.from_user.id
    except:
       user=update.from_user.id
    if update.from_user.id==user:
       try:
          member = await bot.get_chat_member(FSUB_CHANNEL, user)          
       except UserNotParticipant:
          await update.answer("Nice Try... പോടാ... :(", show_alert=True)
       except Exception as e:
            print(e)
       else:
           await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                          user_id=user,
                                          permissions=ChatPermissions(can_send_messages=True,
                                                                      can_send_media_messages=True,
                                                                      can_send_other_messages=True)
                                          )
           await update.message.edit(f"Hello {update.from_user.mention}💕!\nWelcome to {update.message.chat.title}\nDo Must Join Our @IET_Updates To Get Instant Updates")
    else:
       await update.answer("That's not for you bruh 😂 നിനക്ക് വേറെ ഉണ്ടല്ലോടാ..", show_alert=True)
 
# Kangers stay away 😒
