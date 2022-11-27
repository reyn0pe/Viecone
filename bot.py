import os, logging, asyncio

from telegraph import Telegraph, upload_file, exceptions
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.events import NewMessage



logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

moment_worker = []


#start
@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("Halo bocah kontol, Welcome Buat Lo Di Bot Nya Paradox Universe\nOiya Gue Bisa Bantu Lo Buat Tag Anak Anak Kontol Biar Pada Muncul\nButuh Bantuan? /help ",
                    buttons=(
                      [
                         Button.url('Group', 'https://t.me/paradoxuniverse'), 
                         Button.url('Channel', 'https://t.me/urcessaword'), 
                      ], 
                      [
                        Button.url('Add Me Baby', 'https://t.me/prdxrthcldsxbot?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#help
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Buat Lo Semua Beban Kayak Kontol Yang Gak Tau Apa Apa**\n\nPrintah: /all \n Anda dapat menggunakan perintah ini dengan teks yang ingin Anda sampaikan kepada orang lain. \n`Contoh: /all Paradox Kece Cuiii Kata Yael!` \nAnda dapat menggunakan perintah ini sebagai jawaban. setiap pesan Bot akan menandai pengguna untuk menjawab pesan"
  await event.reply(helptext,
                    buttons=(
                      [
                         Button.url('Group', 'https://t.me/paradoxuniverse'), 
                         Button.url('Channel', 'https://t.me/urcessaword'), 
                      ], 
                      [
                        Button.url('Add Me Baby', 'https://t.me/VieconeBot?startgroup=true'),   
                      ]
                   ), 
                    link_preview=False
                   )

#Wah bhaiya full ignorebazzi

#bsdk credit de dena verna maa chod dege

#tag
@client.on(events.NewMessage(pattern="^/tagall|/call|/tall|/all|#all|@all?(.*)"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("Gunakan Ini Di Saluran atau Grup!")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("Woii Kontol Mau Ngapain Lo Jelas Jelas Lo Tuh Bukan Admin Inget Lo Tu Cuman Beban Ortu Lo.")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("Saya tidak dapat menyebutkan Anggota untuk Posting Lama!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Beri aku Argumen. Contoh: `/tag Diago Ganteng Kata Anak Paradox`")
  else:
    return await event.respond("Balas Pesan atau Berikan Beberapa Teks Untuk Disebutkan!")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped!")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("Stopped")
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


#yaha kuch kachra tha ya fr extra features 🥲🥲removed now

print("Mulai Berhasil Bergabung dengan Dukungan")
print("¯\_(ツ)_/¯ Butuh Bantuan Tanyakan Sama Bos Yael @yaelxz")
client.run_until_disconnected()
