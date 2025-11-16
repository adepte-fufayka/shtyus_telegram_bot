import os

import telebot
import re
import time
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from PIL import Image, ImageDraw
import emoji
import CONFIG
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Classes import User, Place, Raid_poll, Raid, Map

print('включен')
ADMIN_ID = 850966027
RAID_RECIPIENTS = CONFIG.RAID_RECIPIENTS
RAID_GROUP = CONFIG.RAID_GROUP
polls = []
TOKEN = CONFIG.TOKEN
bot = AsyncTeleBot(TOKEN)
scheduler = AsyncIOScheduler()

# полезные названия
las_emojies = ['🎂', '🏕️', '🎪', '🏙️', '🏛️', '💃', '🌳', '🏚️', '🏜️', '🏰', '🏤', '🏭', '⛲', '🛕', '🏘️', '👨‍🎤', '🧜‍♀️', '🗿',
               '🏞️', '🧿',
               '⭕', '🏢','👹', '🌴', '⛏️', '🏣', '🐇', '🏫', '⛩️', '🎰', '✨', '🕸️', '🏟️', '🗼', '🦄', '🌒', '💒', '🐺']
las_emojies_png = []
roles = ['newbie', 'user', 'наш_слон', 'officer', 'nачальник']
cities = [["🏛", "Александрия"], ["🏭", "Порт-Романтик"], ["🏢", "Эндимион"], ["🏣", "Китс"]]
zones = ['Безопасные земли', 'Дикие земли', 'Городской зоопарк', 'Квартал Коми-Конщиков', 'Азиатское гетто',
         'Фантастические твари']
short_zones = ['БЗ', "ДЗ", "ГЗ", "ККК", "АГ", "ФТ"]
telegi = ['🛒 в 🏛 Александрию', '🛒 в дикие земли', '🛒 в городской зоопарк', '🛒 в Квартал Коми-Конщиков',
          '🛒 в азиатское гетто',
          '🛒 к фантастическим тварям']
shmot_quality = ['Качество: ▫️ Плохое', 'Качество: ▪️ Обычное', 'Качество: 🔹 Необычное', 'Качество: 🔸 Редкое',
                 'Качество: 🔺 Эпическое']
shmot_dops = [['Шанс выпадения вещей:', 0.3], ['Вампиризм:', 0.25], ['Игнор. брони в PVP:', 0.4],
              ['Восстановление 🔮:', 0.1],
              ['Отражение урона:', 1],
              ['Увеличение скорости восстановления энергии:', -0.5],
              ['Увеличение прочности:', 5], ['Доп. 💰 с продажи вещей:', 1], ['Доп. 🌟 с мобов:', 0.25],
              ['Качество дропа:', 0.5], ['Доп. 🔮:'], ['Доп. ❤️:'], ['Доп. 💪:']]
profs = [['Оружие', '🗡'], ['Чары', '✨'], ['Перчатки', '🧤'], ['Штаны', '👖'], ['Броня', '👕'], ['Шлемы', '🧢']]
raid_zone = ["ⁿ", "¹", "²", "³", "⁴", "⁵"]
# клавиатуры
lab_kb = telebot.types.InlineKeyboardMarkup(row_width=2)
# lab_kb.add(telebot.types.InlineKeyboardButton(text='🔼 Качество', callback_data='+quality'),
#        telebot.types.InlineKeyboardButton(text='🔽 Качество', callback_data='-quality'))
lab_kb.add(telebot.types.InlineKeyboardButton(text='🔼 Тюнинг', callback_data='+tuning'),
           telebot.types.InlineKeyboardButton(text='🔽 Тюнинг', callback_data='-tuning'))
lab_kb.add(telebot.types.InlineKeyboardButton(text='🔼 Заточка', callback_data='+sharpening'),
           telebot.types.InlineKeyboardButton(text='🔽 Заточка', callback_data='-sharpening'))
prof_kb = telebot.types.InlineKeyboardMarkup()
prof_kb.add(telebot.types.InlineKeyboardButton(text='🧢', callback_data='shapki'),
            telebot.types.InlineKeyboardButton(text='👕', callback_data='bronya'),
            telebot.types.InlineKeyboardButton(text='👖', callback_data='shtany'),
            telebot.types.InlineKeyboardButton(text='🧤', callback_data='perchi'),
            telebot.types.InlineKeyboardButton(text='✨', callback_data='magi'),
            telebot.types.InlineKeyboardButton(text='🗡', callback_data='pushki'))
res_kb = telebot.types.InlineKeyboardMarkup()
res_kb.add(telebot.types.InlineKeyboardButton(text='🔩', callback_data='iron'),
           telebot.types.InlineKeyboardButton(text='✨', callback_data='dust'),
           telebot.types.InlineKeyboardButton(text='🌲', callback_data='lumber'),
           telebot.types.InlineKeyboardButton(text='💎', callback_data='diamond'),
           telebot.types.InlineKeyboardButton(text='🧧', callback_data='krasnaya_shtuka'),
           telebot.types.InlineKeyboardButton(text='💰', callback_data='money'))
maps_kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                            input_field_placeholder='Выбери зону:', row_width=3)
maps_kb.add("🗺БЗ", "🗺ДЗ", "🗺ГЗ", "🗺ККК", "🗺АГ", "🗺ФТ")
maps_kb.add('🔙 Назад')
empty_kb = telebot.types.ReplyKeyboardRemove()

# начальные считывания из файлов
users = []
f = open("SHTYUS/users.txt", "r")
s = f.readlines()
k = 20
for i in range(len(s) // k):
    users.append(
        User(int(s[i * k]), s[i * k + 1][:-1], s[i * k + 2][:-1], s[i * k + 3][:-1], int(s[i * k + 4][:-1]),
             int(s[i * k + 5][:-1]), int(s[i * k + 6][:-1]), int(s[i * k + 7][:-1]), int(s[i * k + 8][:-1]),
             int(s[i * k + 9][:-1]),
             int(s[i * k + 10][:-1]), s[i * k + 11][:-1], False if (s[i * k + 12][:-1]) == 'False' else True,
             s[i * k + 13][:-1],
             s[i * k + 14][:-1], int(s[i * k + 15][:-1]), int(s[i * k + 16][:-1]), int(s[i * k + 17][:-1]),
             int(s[i * k + 18][:-1]), False if (s[i * k + 19][:-1]) == 'False' else True))
f.close()
raids = []
places = []
maps = []
f = open('SHTYUS/places.txt', encoding='utf-8')
s = f.readlines()
k = 6
for i in range(len(s) // k):
    places.append(
        Place(s[i * k][:-1], int(s[i * k + 1]), False if (s[i * k + 2][:-1]) == 'False' else True,
              int(s[i * k + 3]),
              int(s[i * k + 4]),
              int(s[i * k + 5])))
    # print(s[i * k + 2][:-1])
    if places[-1]._type == 2:
        raids.append(Raid(places[-1].name, -1, places[-1].zone if places[-1].found else 0))
f.close()
f = open('SHTYUS/raids.txt')
k = 5
s = f.readlines()
for i in range(len(s) // k):
    for j in raids:
        if j.name == s[i * k][:-1]:
            j.IsValid = False if (s[i * k + 1][:-1]) == 'False' else True or j.IsValid
            j.IsUnderAttack = False if (s[i * k + 2][:-1]) == 'False' else True
            j.time = int(s[i * k + 3])
            j.city = s[i * k + 4][:-1]
f.close()
places.sort(key=lambda Place: (Place.zone, Place.length))

f = open('SHTYUS/maps.txt', encoding='utf-8')
g = 21 * 2
s = f.readlines()
for i in range(len(s) // g):
    l = []
    for j in range(g // 2):
        l.append([int(k) for k in s[i * g + j][:-1]])
    u = []
    for j in range(g // 2):
        u.append([emoji.emojize(f':{k}:') for k in re.split('::|:', emoji.demojize(s[i * g + j + g // 2][:-1]))[1:-1]])
    maps.append(Map(l, u))
f.close()
f = sorted(os.listdir("SHTYUS/emojies"))
for file in f:
    image = Image.open(f'SHTYUS/emojies/{file}')
    image = image.resize((30, 30))
    las_emojies_png.append(image)
print('начинаю работу')


@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(call):
    # print(111)
    print('получил ответ от кнопки:', call.data)
    try:
        match (call.data):
            case "boss_ping":
                if call.message.date + 300 <= time.time():
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"{call.message.text}\n\nОтряд не собран(")
                else:
                    kb = telebot.types.InlineKeyboardMarkup(row_width=1)
                    btn1 = telebot.types.InlineKeyboardButton(text="✅ я готов", callback_data='boss_ping')
                    kb.add(btn1)
                    # print(call.message.message_id, call.message.chat.id)
                    edited_text = call.message.text.split('\n')
                    this_usrname = call.from_user.username
                    for i in range(len(edited_text)):
                        if edited_text[i].count(this_usrname) == 1:
                            edited_text[i] = '✅ ' + '@' + this_usrname
                            break
                    edir = ''
                    for i in range(len(edited_text)):
                        edir += edited_text[i] + '\n'
                    if edir.count('✅') == 5:
                        edir += '\nОтряд собран!\n'
                        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    text=edir)
                        await bot.reply_to(call.message, 'Запускайте босса!')
                    else:
                        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    text=edir,
                                                    reply_markup=kb)
            case 'settings_boss_ping':
                message = call.message
                # print(message.text)
                ind = await ind_check(message, call.from_user.id)
                if ind != -1:
                    users[ind].boss_ping = not (users[ind].boss_ping)
                    s = '✅Я пингую вас на боссов' if users[ind].boss_ping else '⛔️Я не пингую вас на боссов'
                    kb = telebot.types.InlineKeyboardMarkup(row_width=1)
                    btn1 = telebot.types.InlineKeyboardButton(text=f"{s}",
                                                              callback_data='settings_boss_ping')
                    kb.add(btn1)
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                text='настройки, которые вы можете изменить:',
                                                reply_markup=kb)

                    await update_data_users()
            case '+tuning':
                await lab_tun(call.message)
            case '-tuning':
                await lab_tun(call.message, -1)
            case '-quality':
                await lab_qual(call.message, -1)
            case '+quality':
                await lab_qual(call.message)
            case '+sharpening':
                await lab_sharp(call.message)
            case '-sharpening':
                await lab_sharp(call.message, -1)
            case 'shapki':
                await send_prof(call.message, "Шлемы")
            case 'bronya':
                await send_prof(call.message, "Броня")
            case 'shtany':
                await send_prof(call.message, "Штаны")
            case 'perchi':
                await send_prof(call.message, "Перчатки")
            case 'magi':
                await send_prof(call.message, "Чары")
            case 'pushki':
                await send_prof(call.message, "Оружие")
            case 'iron':
                await res_command_send(call.message, '🔩', call.from_user.id)
            case 'dust':
                await res_command_send(call.message, '✨', call.from_user.id)
            case 'lumber':
                await res_command_send(call.message, '🌲', call.from_user.id)
            case 'diamond':
                await res_command_send(call.message, '💎', call.from_user.id)
            case 'krasnaya_shtuka':
                await res_command_send(call.message, '🧧', call.from_user.id)
            case 'money':
                await res_command_send(call.message, '💰', call.from_user.id)
        if call.data[:6] == 'raids_':
            _text = call.message.text.split('\n')
            _time = int(_text[0].split(' ')[2])
            _substring = ''
            for i in _text[1].split(' ')[1:]:
                _substring += i + ' '
            _substring += '\n'
            for j in _text[2:-1]:
                for i in j.split(' '):
                    _substring += i + ' '
                _substring += '\n'
            slash_n = '\n\n'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'рейд выбран:{places[int(call.data[6:])].name}\nВремя: {time.strftime("%H:%M", time.localtime(time.time() + 3600 * 3 + _time * 60))}\nПодпись: {_substring}')
            # print(f'"{_substring}"')
            s = f'Рейд в {time.strftime("%H:%M", time.localtime(time.time() + 3600 * 3 + _time * 60 + 59))}\n\n{places[int(call.data[6:])].name} ↕️: {places[int(call.data[6:])].y} ↔️: {places[int(call.data[6:])].x}\n\n<code>{telegi[places[int(call.data[6:])].zone]}</code>{slash_n if _substring == f" {slash_n[:1]}" else f"{slash_n}{_substring}{slash_n[:1]}"}'
            s += f'Рейдовод: {"@" + call.from_user.username if call.from_user.username != None else str(call.from_user.id) + slash_n[:1] + "Сделай себе юзерку пожалуйста"}\n#raid'
            for i in RAID_RECIPIENTS:
                await bot.send_message(i, s, parse_mode='HTML')
            polls.append([call.from_user.id, _time])
    except AttributeError:
        print('', end='')


# комманды + сообщения
@bot.message_handler(commands=['set_role'])
async def set_role_message(message):
    await setting_role(message)


@bot.message_handler(commands=['maps'])
async def set_role_message(message):
    await bot.reply_to(message, 'Выбери зону:', reply_markup=maps_kb)


@bot.message_handler(commands=['kk_pin'])
async def pin_kk(message):
    ind = await ind_check(message)
    if ind != -1:
        users[ind].kk = not users[ind].kk
        await bot.reply_to(message, '✅Я пингую вас на Круг Крови сегодня' if users[
            ind].kk else '⛔️Я не пингую вас на Круг Крови сегодня')
        await update_data_users()


@bot.poll_answer_handler(None)
async def poll_update(poll):
    # print(polls)
    for i in range(len(polls)):
        if poll.poll_id == polls[i].raid_poll_id:
            _user = poll.user.username if poll.user.username != None else poll.user.first_name
            if _user in polls[i].idu:
                polls[i].idu.pop(polls[i].idu.index(_user))
            if _user in polls[i].v_shage:
                polls[i].v_shage.pop(polls[i].v_shage.index(_user))
            if _user in polls[i].na_tochke:
                polls[i].na_tochke.pop(polls[i].na_tochke.index(_user))
            if _user in polls[i].opazdyvayu:
                polls[i].opazdyvayu.pop(polls[i].opazdyvayu.index(_user))
            if len(poll.option_ids) > 0:
                option = poll.option_ids[0]
                if option == 0:
                    polls[i].idu.append(_user)
                if option == 1:
                    polls[i].v_shage.append(_user)
                if option == 2:
                    polls[i].na_tochke.append(_user)
                if option == 3:
                    polls[i].opazdyvayu.append(_user)
        # print(str(polls[i]))


@bot.message_handler(commands=['reset'])
async def reset_message(message):
    if message.from_user.id == ADMIN_ID:
        await reseting()
        await bot.reply_to(message, 'сбросил')
    else:
        await bot.reply_to(message, 'не для тебя команда')


@bot.message_handler(commands=['update'])
async def update_message(message):
    # print(message.text)
    if message.from_user.id == ADMIN_ID:
        await update_data_users()
        await update_data_places()
        await update_data_maps()
        await update_data_rc()
        await bot.reply_to(message, 'обновил')
    else:
        await bot.reply_to(message, 'не для тебя команда')


@bot.message_handler(commands='timer')
async def timer(message):
    _t = message.text.split(' ')
    if len(_t) > 1:
        try:
            _time = float(_t[1])
            await bot.reply_to(message, 'Таймер запущен')
            await asyncio.sleep(_time * 60)
            _com = ''
            if len(_t) > 2:
                for i in _t[2:]:
                    _com += i + ' '
            await bot.reply_to(message, f'Таймер завершен!💅\n{f"Комментарий: {_com}" if _com != "" else ""}')
        except:
            await bot.reply_to(message,
                               'Что-то пошло не так, возможно ты ввел не число. К примеру, если ты хочешь поставить таймер на 60 минут, то введи: /timer 60 комментарий')


@bot.message_handler(commands='newraid')
async def new_raid_message(message):
    if message.from_user.id == message.chat.id:
        await send_new_raid(message)


@bot.message_handler(commands=['news'])
async def news_message(message):
    print(message.text)
    ind = await ind_check(message)
    if ind != -1:
        if roles.index(users[ind].role) >= roles.index('nачальник'):
            _text = message.text.split('/news ')
            for i in users:
                try:
                    await bot.send_message(i.uid, _text[1] + '\n\nИ помните: Ноготочки💅 заботится о вас!', parse_mode='HTML')
                except:
                    print(i.uid)


@bot.message_handler(commands=['set_timezone'])
async def time_zone_reply_message(message):
    if message.chat.id != message.from_user.id:
        await bot.reply_to(message, 'работает только в личке')
    else:
        ind = await ind_check(message)
        if ind != -1:
            try:
                k = int(message.text.split('/set_timezone')[1])
                users[ind].timezone = k
                await bot.reply_to(message, 'Записал')
            except:
                await bot.reply_to(message,
                                   "Ты что то не так сделал, попробуй еще раз.\nНапример, чтобы у тебя показывало по московскому времени - отправь /set_timezone 3, так как время по МСК - UTC+3")
            # await bot.reply_to(message,
            #                     'окей, отправь мне свою (зону времени?). Например чтобы у тебя показывало по МСК - отправь 3, так как время по МСК - UTC+3')
            # await bot.(sent, setting_time_zone)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
async def send_welcome_message(message):
    await bot.reply_to(message, """\
Добро пожаловать в Маникюрный Салон💅!
я - бот, который поможет вам взаимодействовать с нашей группой.
отправь мне свой профиль с игры @HyperionGameBot.
""")


@bot.message_handler(commands=['help'])
async def send_welcom_message(message):
    await bot.reply_to(message, """\
известная мне информация на данный момент:
/help - вызов меню с информацией
/me - информация о вас(желательно обновлять ее как можно чаще)
/settings - настройки (работает только в личных сообщениях бота)
/res - время до сбора ресурсов
/set_timezone - установить временную зону по UTC (работает только в личных сообщениях бота)
""")


@bot.message_handler(commands=['res'])
async def res_command_message(message):
    await res_time(message, False)


@bot.message_handler(commands=['rest'])
async def rest(message):
    ind = await ind_check(message)
    if ind != -1:
        t = int(time.time() - users[ind].rest)
        if t < 301:
            t = 300 - t
            await bot.reply_to(message,
                               f'Ты сможешь отдохнуть через {t // 60}м. {t % 60}с.\nТочное время: {time.strftime("%H:%M:%S", time.localtime(int(time.time() + t + (users[ind].timezone) * 3600)))}')
        else:
            await bot.reply_to(message, 'По моим данным ты уже можешь отдохнуть в святе')


@bot.message_handler(commands=['trap'])
async def trap(message):
    ind = await ind_check(message)
    if ind != -1:
        t = int(time.time() - users[ind].trap)
        if t < 601:
            t = 600 - t
            await bot.reply_to(message,
                               f'Ты освободишься через {t // 60}м. {t % 60}с.\nТочное время: {time.strftime("%H:%M:%S", time.localtime(int(time.time() + t + (users[ind].timezone) * 3600)))}')
        else:
            await bot.reply_to(message, 'По моим данным ты уже можешь двигаться')


@bot.message_handler(commands=['prof_who'])
async def prof_who_message(message):
    await bot.reply_to(message, 'У нас есть все, и даже больше. Что тебя интересует?', reply_markup=prof_kb)


@bot.message_handler(commands=['me'])
async def send_me_message(message):
    await send_profile(message)


@bot.message_handler(commands=['raids'])
async def send_raids_message(message):
    await send_point(message, 2)


@bot.message_handler(commands=['dng'])
async def send_dng_message(message):
    await send_point(message, 0)


@bot.message_handler(commands=['bosses'])
async def send_bosses_message(message):
    await send_point(message, 1)


@bot.message_handler(content_types=['photo'])
async def message_pocessing(message):
    await message_processing(message, False)


@bot.message_handler(commands=['settings'])
async def settings_processing(message):
    if message.chat.id == message.from_user.id:
        ind = await ind_check(message)
        if ind != -1:
            kb = telebot.types.InlineKeyboardMarkup(row_width=1)
            s = '✅Я пингую вас на боссов' if users[ind].boss_ping else '⛔️Я не пингую вас на боссов'
            btn1 = telebot.types.InlineKeyboardButton(text=f"{s}", callback_data='settings_boss_ping')
            kb.add(btn1)
            await bot.reply_to(message, 'настройки, которые вы можете изменить:', reply_markup=kb)
    else:
        await bot.reply_to(message, 'работает только в личке!')


@bot.message_handler(commands=['rc'])
async def send_rc(message):
    _t = int(time.time())
    ind = await ind_check(message)
    if ind >= 0:
        raids.sort(key=lambda Raid: (not Raid.IsValid, Raid.city, Raid.zone))
        _s = ''
        nam = raids[0].city
        s = nam if nam != '🕧None' else 'Не контролируются:'
        s += '\n'
        for i in raids:
            if i.city != nam:
                if s != f"\n{nam if nam != '🕧None' else 'Не контролируются:'}\n" and s != f"{nam if nam != '🕧None' else 'Не контролируются:'}\n":
                    _s += s
                nam = i.city
                s = '\n'
                s += nam if nam != '🕧None' else 'Не контролируются:'
                s += '\n'
            if i.IsValid and nam != '🕧None':
                m = 'м'
                c = 'с'
                h = 'ч'
                s += f'{raid_zone[i.zone]}{i.name} ({"⚔️ " + time.strftime(f"%M{m} %S{c}", time.localtime(max(0, 15 * 60 - (_t - i.time)))) if i.IsUnderAttack else "🛡 " + time.strftime(f"%H{h} %M{m}", time.localtime(max(0, int(3600 * 1.5) - (_t - i.time)))) if _t - i.time < 5400 else "⏳ " + time.strftime(f"%H{h} %M{m}", time.localtime(max(0, 12 * 3600 - (_t - i.time))))})\n'
            else:
                if i.IsValid:
                    m = 'м'
                    c = 'с'
                    h = 'ч'
                    s += f'{raid_zone[i.zone]}{i.name} {"(⚔️ " + time.strftime(f"%M{m} %S{c}", time.localtime(max(0, 15 * 60 - (_t - i.time)))) + ")" if i.IsUnderAttack else ""}\n'
        if s != f"\n{nam if nam != '🕧None' else 'Не контролируются:'}\n":
            _s += s
        if _s == '':
            _s = 'С момента перетряса ничего не произошло'
        await bot.reply_to(message, _s)


@bot.message_handler(commands=['time'])
async def sending_time(message):
    await bot.reply_to(message, time.strftime('%H:%M:%S', time.localtime()))


@bot.message_handler()
async def messag_pocessing(message):
    # await bot.reply_to(message, 'абоба2')
    await message_processing(message, True)


async def send_new_raid(message):
    ind = await ind_check(message)
    if ind != -1:
        try:
            j = message.text.split(" ")
            if roles.index(users[ind].role) >= roles.index('officer'):
                raids_kb = telebot.types.InlineKeyboardMarkup()
                for i in places:
                    if i.found and i._type == 2:
                        raids_kb.add(
                            telebot.types.InlineKeyboardButton(text=f'{i.name} 🔄: {i.zone} ↕️: {i.y} ↔️: {i.x}',
                                                               callback_data=f'raids_{places.index(i)}'))
                if int(j[1]) > 0:
                    _substring = ''
                    if len(j) > 2:
                        for i in j[2:]:
                            _substring += i + ' '
                    await bot.reply_to(message,
                                       f'Рейд через {int(j[1])} минут.\nПодпись: {_substring}\nВыбери точку:',
                                       reply_markup=raids_kb)
                else:
                    await bot.reply_to(message, 'Сории, но люди еще не развились настолько, чтобы прыгать в прошлое')
        except:
            await bot.reply_to(message, 'Что-то пошло не так, возможно ты ввел не число')


async def send_prof(message, _prof):
    # kb = telebot.types.InlineKeyboardMarkup()
    # kb.add(telebot.types.InlineKeyboardButton(text='⬅️', callback_data='prof_nazad'))
    _emoji = ''
    for i in profs:
        if i[0] == _prof:
            _emoji = i[1]
    s = f'Мастера с профессией {_emoji}{_prof}:\n'

    for i in users:
        if _prof in i.prof:
            s += f"{_emoji}<code>@{i.username if i.username != None else i.name}</code> - {i.prof.split('|Уровень: ')[1]}\n"
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                text=s, parse_mode='HTML')


async def res_command_send(message, _type, uid):
    _text = message.text.split('\n')[0].split(' ')
    if int(_text[2]) == uid:
        if _type != '💰' or _text[0] != '/pay_squad':
            _text[1] = _type
            s = '`'
            for i in _text:
                s += i + ' '
            s += '`'
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                        text=s,
                                        parse_mode='Markdown')
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                        text=f'`/pms {_text[2]} {_text[3]}`',
                                        parse_mode='Markdown')
async def money_send(message, uid, quantity, city):
    if city:
        await bot.reply_to(message, f'`/pay_city 💰 {uid} {quantity}`', parse_mode='Markdown')
    else:
        await bot.reply_to(message, f'`/pms {uid} {quantity}`',parse_mode='Markdown')


async def message_processing(message, flag):
    try:
        _text = message.text if flag else message.caption
        if message.chat.id == RAID_GROUP:
            if '#raid' in _text:
                raid_poll = telebot.types.Poll('Рейд:',
                                               [telebot.types.PollOption("Иду"),
                                                telebot.types.PollOption("Стою в шаге"),
                                                telebot.types.PollOption("На точке"),
                                                telebot.types.PollOption("Опаздываю")], is_anonymous=False)
                p = await bot.send_poll(message.chat.id, raid_poll.question, raid_poll.options, raid_poll.is_anonymous,
                                        reply_to_message_id=message.id)
                for i in range(len(polls)):
                    if len(polls[i]) == 2:
                        _I = polls[i]
                        polls.pop(i)
                        polls.append(Raid_poll(p.poll.id, _I[0]))
                        # print(str(polls[-1]))
                        await asyncio.sleep(_I[1] * 60 - 45)
                        await pin_na_meste(p.poll.id)
                        await asyncio.sleep(35)
                        await check_raid_poll(p)
                        # print(p.poll.id)
        if message.from_user.id == 589732215 and int((random.randint(1, 1000))) == 7:
            await bot.reply_to(message, 'АААААААААААААААА, ЖЕНЩИНА')
        if message.forward_from.id == 820567103:
            if _text.count('Если ты не хочешь слышать других игроков - нажми /toggle_radio') == 0:
                if _text.count('Группа отряда ') == 1:
                    if message.forward_date + 300 >= time.time():
                        s1 = 'Пинг!\n'
                        _text = re.split('Группа отряда | собралась.|Записавшиеся игроки:\n|\n', _text)[6:]
                        # print(_text)
                        # for i in range(len(users.txt)):
                        # print(users.txt[i].name)
                        kb = telebot.types.InlineKeyboardMarkup(row_width=1)
                        btn1 = telebot.types.InlineKeyboardButton(text="✅ я готов", callback_data='boss_ping')
                        kb.add(btn1)
                        for i in range(len(_text)):
                            fl = True
                            for j in range(len(users)):
                                if users[j].name in _text[i]:
                                    s1 += '@' + users[j].username + '\n'
                                    fl = False
                                    break
                            if fl:
                                s1 += _text[i] + '\n'
                        await bot.reply_to(message, s1, reply_markup=kb)
                    else:
                        await bot.reply_to(message, 'Вспомнил тоже, когда это было то?')
                elif 'Требуемые характеристики:' in _text and 'Качество: ' in _text:
                    if message.chat.id == message.from_user.id:
                        ind = await ind_check(message)
                        if ind != -1:
                            await lab_func_st(message)
                elif _text.count('UID') == 1 and _text.count('Событие') == 1:
                    _text = re.split('👤 |, | \| |👨\u200d👨\u200d👧\u200d👦: |\n\n🗺:|UID: |\n', _text)
                    # print(_text)
                    if int(_text[-1]) != message.from_user.id:
                        await bot.reply_to(message, 'скинь мне свой профиль, а не кого-то другого')
                    elif message.forward_date + 300 < time.time():
                        await bot.reply_to(message, 'этому профилю больше 5 минут, я его не приму!')
                    else:
                        uid = int(_text[-1])
                        name = _text[3]
                        squad_name = _text[6]
                        # print(name, squad_name, uid)
                        hp, pp, mp, at, df = 0, 0, 0, 0, 0
                        for klol in _text:
                            if klol.count('🔮: ') == 1:
                                mp = int(re.split('🔮: |/', klol)[2])
                            if klol.count('❤️: ') == 1:
                                hp = int(re.split('❤️: |/', klol)[2])
                            if klol.count('💪: ') == 1:
                                pp = int(klol.split('💪: ')[1])
                            if klol.count('🛡: ') == 1:
                                df = int(klol.split('🛡: ')[1])
                            if klol.count('⚔️: ') == 1:
                                at = int(klol.split('⚔️: ')[1])
                        new = True
                        # print(_text)
                        for j in range(len(users)):
                            if users[j].uid == uid:
                                new = False
                                users[j].name = name
                                users[j].squad_name = squad_name
                                users[j].username = message.from_user.username
                                users[j].time = int(message.forward_date)
                                users[j].mana_p = mp
                                users[j].health_p = hp
                                users[j].power_p = pp
                                users[j].attack = at
                                users[j].deff = df
                                # print(_text[4][1:])
                                users[j].city = _text[4][2:]
                                await bot.reply_to(message, 'Профиль обновлен!')
                                await update_data_users()
                                break
                        if new:
                            users.append(
                                User(message.from_user.id, message.from_user.username, name, squad_name,
                                     int(message.forward_date), 1, df, at, hp, pp, mp, 'newbie', True,
                                     _text[4][2:], 'Неизвестно', 1, 3, 1, 1, False))
                            print(str(users[-1]))
                            await update_data_users()
                            await bot.reply_to(message,
                                               'Добро пожаловать! Твой профиль добавлен в мою базу данных.\n/help - покажет доступные команды')
                elif _text.count('Здесь собираются игроки из отряда ') == 1:
                    if message.forward_date + 300 >= time.time():
                        _text = re.split(
                            'Здесь собираются игроки из отряда |, желающие победить |\n|Записавшиеся игроки:',
                            _text)
                        # print(_text)
                        s = [[]]
                        ind = 0
                        cnt = 0
                        _squad = _text[1]
                        for i in users:
                            fl = True
                            for j in _text:
                                if i.name in j:
                                    fl = False
                            if fl and _squad in i.squad_name:
                                if i.boss_ping:
                                    s[ind].append('@' + i.username)
                                else:
                                    s[ind].append(
                                        i.name if i.name != None else "Еблан без юзерки с выключенным пингом на боссов")
                                cnt += 1
                                if cnt == 5:
                                    cnt = 0
                                    ind += 1
                                    s.append([])
                        for i in s:
                            strin = _squad + ', пишемся на босса ' + _text[2] + '\n\n'
                            if len(i) > 0:
                                for k in i:
                                    strin += k + '\n'
                                await bot.reply_to(message, strin)
                    else:
                        await bot.reply_to(message, 'слишком старое сообщение')
                elif 'Собрано ' in _text:
                    await res_time(message, True)
                elif 'Ты не записан на боссов' in _text:
                    await bot.reply_to(message, 'Этот грех Аллах не простит')
                elif 'Сбросить: /reset_spec' in _text:
                    ind = await ind_check(message)
                    if ind != -1:
                        fl = False
                        for i in users:
                            if i.prof_time == int(message.forward_date):
                                fl = True
                        if fl:
                            await bot.reply_to(message, 'где-то я такое уже видел')
                        else:
                            if message.forward_date + 3600 >= int(time.time()):
                                _text = _text.split('\n')
                                s = ''
                                for i in _text:
                                    if 'Специализация: ' in i:
                                        s += i[16:] + '|'
                                    if 'Уровень: ' in i:
                                        s += i + ' '
                                    if 'Прогресс: ' in i:
                                        s += str(i.count('#'))
                                users[ind].prof = s
                                users[ind].prof_time = int(message.forward_date)
                                await bot.reply_to(message, 'сохранил')
                                users.sort(key=lambda User: len(User), reverse=True)
                                await update_data_users()
                            else:
                                await bot.reply_to(message,
                                                   'информация малость устарела, попробуй уложиться в 1 час')
                elif 'С криком: "Разбежавшись прыгну на кровать", ты укутался в одеялко из шерсти Ходжека и прекрасно отдохнул.' in _text:
                    ind = await ind_check(message)
                    if ind != -1:
                        users[ind].rest = int(message.forward_date)
                        t = time.time() - users[ind].rest
                        await update_data_users()
                        if t < 301:
                            t = int(300 - t)
                            await bot.reply_to(message,
                                               f'Ты сможешь отдохнуть через {t // 60}м. {t % 60}с.\nТочное время: {time.strftime("%H:%M:%S", time.localtime(time.time() + t + (users[ind].timezone) * 3600))}')
                            await asyncio.sleep(t)
                            await bot.reply_to(message, 'Сез ял итә аласыз')
                        else:
                            await bot.reply_to(message, 'По моим данным ты уже можешь отдохнуть в святе')
                elif 'и не можешь идти 10 минут' in _text:
                    ind = await ind_check(message)
                    if ind != -1:
                        users[ind].trap = int(message.forward_date)
                        t = time.time() - users[ind].trap
                        await update_data_users()
                        if t < 601:
                            t = int(600 - t)
                            await bot.reply_to(message,

                                               f'Ты освободишься через {t // 60}м. {t % 60}с.\nТочное время: {time.strftime("%H:%M:%S", time.localtime(time.time() + t + (users[ind].timezone) * 3600))}')
                            await asyncio.sleep(t)
                            await bot.reply_to(message, 'Сез бара аласыз')
                        else:
                            await bot.reply_to(message, 'По моим данным ты уже можешь двигаться')
                elif 'Принять участие в Круге Крови (0/1)' in _text:
                    ind = await ind_check(message)
                    if ind != -1:
                        users[ind].kk = True
                        await update_data_users()
                        await bot.reply_to(message, '✅Я пингую вас на Круг Крови сегодня')
                elif 'Ты находишься где-то тут:' in _text and '↕️:' in _text and '↔️:' in _text and '🗺:' in _text:
                    if await last_peretryas(message.forward_date) > 0:
                        l = _text.split('\n')
                        _map = l[5:-5]
                        # await bot.reply_to(message, "".join([i + '\n' for i in _map]))
                        size = len(_map) // 2
                        o = l[2]
                        zone = -1
                        for j in range(len(zones)):
                            if zones[j] in o:
                                zone = j
                        k = ''
                        o = re.split('↕️: |  ↔️: ', l[3])
                        y, x = int(o[1]), int(o[2])
                        for i in range(len(_map)):
                            z = re.split('::|:', emoji.demojize(_map[i]))[1:-1]
                            for j in range(len(z)):
                                g_i = y + size - i
                                g_j = x + +j - size
                                if abs(g_j) <= 10 and abs(g_i) <= 10:
                                    g_i = 10 - g_i
                                    g_j = 10 + g_j
                                    gneg = emoji.emojize(f':{z[j]}:')
                                    maps[zone].colors[g_i][
                                        g_j] = 2 if gneg != '🧝‍♂️' and gneg != '🌫️' and gneg != '🏕' and gneg != '💢' and gneg != '⛲' else \
                                        maps[zone].colors[g_i][g_j]
                                    if zone != 0:
                                        maps[zone].objects[g_i][
                                            g_j] = gneg if gneg != '🧝‍♂️' and gneg != '🌫️' and gneg != '🏕' and gneg != '💢' and gneg != '⛲' else \
                                            maps[zone].objects[g_i][g_j]
                                    else:
                                        maps[zone].objects[g_i][
                                            g_j] = gneg if gneg != '🏰' and gneg != '🧝‍♂️' and gneg != '🌫️' and gneg != '🏕' and gneg != '💢' and gneg != '⛲' else \
                                            maps[zone].objects[g_i][g_j]
                        await update_data_maps()
                        if message.chat.id == message.from_user.id:
                            await send_map(message, zone)
                    else:
                        await bot.reply_to(message, 'Слишком старый форвард карты')
                elif '❗️ Ты в дороге, тебе еще предстоит идти' in _text:
                    t=time.time()
                    s=await text_to_time(re.split('⏱ | \.',_text)[1])+message.forward_date-t
                    if s>0:
                        s+=t
                        await bot.reply_to(message, f"Ты дотопаешь в {time.strftime('%H:%M:%S', time.localtime(s+3*3600))}МСК")
                    else:
                        await bot.reply_to(message, 'По моим данным, ты уже приехал')

                else:
                    for i in range(len(places)):
                        # print(places[i].name)
                        if places[i].name in _text and '↕️' in _text and '↔️' in _text and '🗺' in _text:
                            if await last_peretryas(message.forward_date) > 0:
                                # print(str(places[i]))
                                if places[i].found:
                                    await bot.reply_to(message, 'Уже нашли(')
                                else:
                                    places[i].found = True
                                    for l in range(len(zones)):
                                        if zones[l] in _text:
                                            places[i].zone = l
                                    zwyx = re.split('↕️: |  ↔️: |   🗺: |\n', _text)
                                    places[i].x = int(zwyx[3])
                                    places[i].y = int(zwyx[2])
                                    places[i].length = max(abs(places[i].x), abs(places[i].y))
                                    if places[i]._type == 2:
                                        for g in raids:
                                            if g.name == places[i].name:
                                                g.IsValid = True
                                                g.zone = places[i].zone
                                    await bot.send_message(ADMIN_ID,
                                                           f'#log_scouts\n{places[i].name}\n↕️: {places[i].y} ↔️: {places[i].x} {zones[places[i].zone]}\nНашел: @{message.from_user.username}\nUID:{message.from_user.id}')
                                    places.sort(key=lambda Place: (Place.zone, Place.length))
                                    await update_data_places()
                                    await bot.reply_to(message, 'Записал')
                            else:
                                await bot.reply_to(message, 'форвард малость староват, попробуй перезайти на точку')
    except AttributeError:
        _text = message.text if flag else message.caption
        if _text == 'Штыус, профиль':
            # print('huy52')
            await send_profile(message)
        elif _text == 'Штыус, рейды':
            await send_point(message, 2)
        elif _text == 'Штыус, телеги':
            s = 'Телега (нажмите на нужное чтобы скопировать)\n\n`🛒 в 🏛 Александрию`\n\n`🛒 в дикие земли`\n\n`🛒 в городской зоопарк`\n\n`🛒 в Квартал Коми-Конщиков`\n\n`🛒 в азиатское гетто`\n\n`🛒 к фантастическим тварям`'
            await bot.reply_to(message, s, parse_mode='markdown')
        elif _text == 'Штыус, данжи':
            await send_point(message, 0)
        elif _text == 'Штыус, боссы':
            await send_point(message, 1)
        elif _text[:12] == 'Штыус, отряд' or _text[:12] == 'Штыус, город':
            try:
                k = int(_text[12:])
                await bot.reply_to(message,
                                   f'/{"pay_squad" if _text[:12] == "Штыус, отряд" else "pay_city"} _ {message.from_user.id} {k}\nвыбери ресурс:',
                                   reply_markup=res_kb)
            except:
                if 'к' in _text.lower() or 'k' in _text.lower():
                    try:
                        k = int(_text[12:-1]) * 1000
                        await money_send(message, message.from_user.id, k, _text[:12] == "Штыус, город")
                    except:
                        await bot.reply_to(message,
                                           'Что-то пошло не так, возможно, после слов город/отряд было введено не число')
                else:
                    await bot.reply_to(message,
                                       'Что-то пошло не так, возможно, после слов город/отряд было введено не число')
    match _text:
            case '🗺БЗ':
                await send_map(message, 0)
            case '🗺ДЗ':
                await send_map(message, 1)
            case '🗺ГЗ':
                await send_map(message, 2)
            case '🗺ККК':
                await send_map(message, 3)
            case '🗺АГ':
                await send_map(message, 4)
            case '🗺ФТ':
                await send_map(message, 5)
            case '🔙 Назад':
                await bot.reply_to(message, 'назад, так назад', reply_markup=empty_kb)

    if message.from_user.id == 2070148382:
        if 'начал захват' in _text:
            _text = _text.split('\n')
            _s = _text[0].split(' начал захват локации ')
            k = int(float(_text[1]))
            for i in raids:
                if i.name == _s[1]:
                    i.IsValid = True
                    i.IsUnderAttack = True
                    i.time = k
                    await update_data_rc()
            t = ''
            for i in places:
                if i.name == _s[1] and i.found:
                    t = f' ({short_zones[i.zone]} {i.y};{i.x})'
            g = _text[
                    0] + t + f"\nВремя окончания: {time.strftime('%H:%M:%S', time.localtime(k + 15 * 60 + 3 * 3600))}"
            for i in CONFIG.raid_chats:
                await bot.send_message(i, g)
        if 'Контроль над локацией' in _text:
            _trext = _text.split('\"')
            for i in raids:
                if i.name == _trext[1]:
                    i.city = '🕧None'
                    await update_data_rc()
            for i in CONFIG.raid_chats:
                await bot.send_message(i, _text)
        if 'Рейд на локации ' in _text:
            _text = _text.split('\n')
            for i in raids:
                if i.name == _text[0].split('\"')[1]:
                    i.city = _text[2].split("🏆 ")[1]
                    i.IsUnderAttack = False
                    i.time = int(float(_text[-1]))
                    await update_data_rc()
            for i in CONFIG.raid_chats:
                await bot.send_message(i, ''.join([i + '\n' for i in _text[:-1]]))


async def ind_check(message, fl=1):
    uid = message.from_user.id if fl == 1 else fl
    ind = -1
    for j in range(len(users)):
        if uid == users[j].uid:
            if int(time.time() - users[j].time) // 3600 > 4 * 7 * 24:
                await bot.reply_to(message, 'Твой профиль устарел на месяц, обнови его и потом поговорим.')
                ind = -2
            elif users[j].role == 'наш_слон':
                ind = j
            elif users[j].city != 'Александрия':
                await bot.reply_to(message, 'Шпоням слово не давали')
                ind = -2
            else:
                ind = j
            break
    if ind == -1:
        await bot.reply_to(message, 'Для того, чтобы что-то тыкать, нужно быть в моей базе!\n/start')
    if ind == -2:
        ind = -1
    return ind


async def send_point(message, type):
    s = '' if type == 2 else f'*{zones[0]}:*\n🕸 Логово Шелоб:  ↕️: -2 ↔️: -5\n🐺 Волчья стая:  ↕️: 10 ↔️: 0\n' if type == 1 else f'*{zones[0]}:*\n⛏ Шахта кобольдов:  ↕️: 2  ↔️: 4\n👹 Логово троллей:  ↕️: 6  ↔️: -8\n'
    ind = await ind_check(message)
    pt=-1
    if ind != -1:
        if users[ind].role != 'newbie':
            for i in places:
                if i.found and i._type == type:
                    if i.zone==pt:
                        s += f'{i.name}:  ↕️: {i.y} ↔️: {i.x}\n'
                    else:
                        s+=f'\n*{zones[i.zone]}:*\n{i.name}:  ↕️: {i.y} ↔️: {i.x}\n'
                        pt=i.zone
            if s == '':
                s = 'Рейдов еще не нашли :('
            await bot.reply_to(message, s, parse_mode='Markdown')


async def send_map(message, zone):
    ind = await ind_check(message)
    if ind != -1:
        if users[ind].role != 'newbie':
            img_size = 40  # pixels
            st = img_size
            img = Image.new('RGBA', (st + 21 * img_size + 1, st + 21 * img_size + 1), 'white')
            idraw = ImageDraw.Draw(img)
            idraw.rectangle((0, 0, st, st), fill=(165, 137, 104, 255), outline=(0, 0, 0))
            for j in range(21):
                idraw.rectangle((0, st + j * img_size, img_size, st + (j + 1) * img_size), fill=(255, 255, 255, 255),
                                outline=(0, 0, 0))
                idraw.text((5, st + j * img_size), text=f'{10 - j}', fill=(173, 31, 64, 255), font_size=20)
                idraw.rectangle((st + j * img_size, 0, st + (j + 1) * img_size, img_size), fill=(255, 255, 255, 255),
                                outline=(0, 0, 0))
                idraw.text((5 + st + j * img_size, 0), text=f'{j - 10}', fill=(173, 31, 64, 255), font_size=20)
                for i in range(21):
                    if maps[zone].colors[j][i] == 0:
                        idraw.rectangle(
                            (st + i * img_size, st + j * img_size, st + (i + 1) * img_size, st + (j + 1) * img_size),
                            fill=(255, 255, 255, 255), outline=(0, 0, 0))
                    if maps[zone].colors[j][i] == 1:
                        idraw.rectangle(
                            (st + i * img_size, st + j * img_size, st + (i + 1) * img_size, st + (j + 1) * img_size),
                            fill=(82, 175, 255, 85), outline=(0, 0, 0))
                    if maps[zone].colors[j][i] == 2:
                        idraw.rectangle(
                            (st + i * img_size, st + j * img_size, st + (i + 1) * img_size, st + (j + 1) * img_size),
                            fill=(82, 255, 138, 85), outline=(0, 0, 0))
                    if not ('🌫️' == maps[zone].objects[j][i] or '◻️' == maps[zone].objects[j][i]):
                        # idraw.rectangle(
                        #     (st + i * img_size, st + j * img_size, st + (i + 1) * img_size, st + (j + 1) * img_size),
                        #     fill=(235, 255, 59, 255), outline=(0, 0, 0))
                        img.paste(las_emojies_png[las_emojies.index(maps[zone].objects[j][i])],
                                  (st + i * img_size + 5, st + j * img_size + 5),
                                  las_emojies_png[las_emojies.index(maps[zone].objects[j][i])])
                    else:
                        idraw.text((15 + st + i * img_size, 5 + st + j * img_size), text=f'{10 - j}', font_size=12,
                                   fill=(62, 62, 62, 255))
                        idraw.text((15 + st + i * img_size, 20 + st + j * img_size), text=f'{i - 10}', font_size=12,
                                   fill=(62, 62, 62, 255))
            img.save('map.png')
            img = open('SHTYUS/map.png', 'rb')
            await bot.send_photo(message.chat.id, img, reply_to_message_id=message.id, reply_markup=empty_kb)


async def send_profile(message):
    # s = 'Тебя нет в моей базе данных! Отправь профиль от @HyperionGameBot'
    ind = await ind_check(message)
    if ind != -1:
        s2 = '✅Я пингую вас на боссов' if users[
            ind].boss_ping else '⛔️Я не пингую вас на боссов'
        s3 = ''
        fl = True
        for j in cities:
            if users[ind].city == j[1]:
                s3 = j[0]
                fl = False
        if fl:
            s3 = '❓'
        k = '\n'
        s = f'👤: {users[ind].name}, {s3} {users[ind].city}\n👨‍👨‍👧‍👦: {users[ind].squad_name}\nUID: `{users[ind].uid}`\n\n💪: {users[ind].power_p}, ❤️: {users[ind].health_p}, 🔮: {users[ind].mana_p}\n⚔️: {users[ind].attack}, 🛡: {users[ind].deff}\nПрофиль обновлен: {(int(time.time()) - users[ind].time + 1799) // 3600} часов назад\n\nПрофессия: {users[ind].prof.split("|")[0] + k + users[ind].prof.split("|")[1] if users[ind].prof != "Неизвестно" else users[ind].prof}\nОбновлена: {(int(time.time()) - users[ind].prof_time + 1799) // 3600} часов назад\n\n{s2}'
        await bot.reply_to(message, s, parse_mode='Markdown')


async def update_data_users():
    f = open('SHTYUS/users.txt', 'w')
    for i in range(len(users)):
        f.write(str(users[i]))
    f.close()


async def update_data_maps():
    f = open('SHTYUS/maps.txt', 'w', encoding='utf-8')
    for i in range(len(maps)):
        f.write(str(maps[i]))
    f.close()


async def update_data_rc():
    f = open('SHTYUS/raids.txt', 'w', encoding='utf-8')
    for i in raids:
        f.write(str(i))
    f.close()


async def setting_role(message):
    ind = await ind_check(message)
    if ind != -1:
        _text = message.text.split(' ')
        print(_text)
        role = _text[2]
        if role in roles:
            ui = int(_text[1])
            _ind = -1
            for i in range(len(users)):
                if users[i].uid == ui:
                    _ind = i
            if _ind != -1:
                setter = roles.index(users[ind].role)
                getter = roles.index(role)
                # fl=True
                if message.from_user.id != ADMIN_ID:
                    if setter > roles.index(users[_ind].role) and getter < setter:
                        users[_ind].role = role
                        await update_data_users()
                        await bot.reply_to(message, 'Установил')
                    else:
                        await bot.reply_to(message, 'Маловато у тебя прав для этого')
                else:
                    users[_ind].role = role
                    await update_data_users()
                    await bot.reply_to(message, 'Установил')
            else:
                await bot.reply_to(message, 'Не нашел такого пользователя')
        else:
            await bot.reply_to(message, 'Такую роль нельзя установить')


async def update_data_places():
    f = open('SHTYUS/places.txt', 'w', encoding='utf-8')
    for i in range(len(places)):
        f.write(str(places[i]))
    f.close()


async def res_time(message, fl):
    now_time = int(time.time())
    time_res = 8 * 60 * 60  # 8 часов в секундах
    ind = await ind_check(message)
    if ind != -1:
        if fl:
            users[ind].res_time = message.forward_date
            await update_data_users()
        if users[ind].res_time + time_res < now_time:
            await bot.reply_to(message,
                               'По моим данным, ты уже можешь собрать ресурсы, либо пришли мне актуальный сбор ресурсов' if not fl else 'Судя по этим данным, ты уже можешь собрать ресурсы')
        else:
            _time = users[ind].res_time + time_res - now_time
            await bot.reply_to(message,
                               f"Ты сможешь собрать ресурсы через {int(_time) // 3600} часов, {int(_time) % 3600 // 60} минут\nТочное время: {time.strftime('%H:%M:%S', time.localtime(users[ind].res_time + time_res + users[ind].timezone * 3600))}\n\n`⚒️ Собрать ресурсы`",
                               parse_mode='markdown')
            if fl:
                if _time > 3600:
                    await asyncio.sleep(_time - 3600)
                    await bot.reply_to(message, 'Остался час до сбора ресов!')
                    await asyncio.sleep(3600)
                    await bot.reply_to(message, 'Ты можешь собрать ресурсы!')
                else:
                    await asyncio.sleep(_time)
                    await bot.reply_to(message, 'Ты можешь собрать ресурсы!')
        # else:
    #     await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEMFodmPnuIXkaOMzpHeXsv-JOg7ChStwACpSUAAulB4EuYHdg8OtIqejUE',
    #                      protect_content=True)


async def lab_func_st(message):
    _text = message.text.split('\n')
    # print(_text)
    koef = 1 if '✅ Надето' in message.text or '⛔️ Недостаточно характеристик' in message.text else 0
    _hp = int(_text[-7 + koef][:-2])
    s = f'{_text[0]}\n{_text[1]}\n{_text[3]}\n\n{_text[6]}\n'
    for i in _text:
        for j in shmot_dops:
            if j[0] in i:
                s += i
                if j[0] == j[-1]:
                    _stat = int(i.split(j[0])[1])
                    ed_stat = _hp / 200
                    low = int((_stat - 0.5) / ed_stat)
                    high = int((_stat + 0.5) / ed_stat)
                    if high > 25:
                        high = 25
                    if low == high:
                        s += f'   🔄: {high}\n'
                    else:
                        s += f'   🔄: {low}-{high}\n'
                else:
                    _stat = float(i.split(j[0])[1][:-1])
                    s += f'   🔄: {int(_stat / j[1])}\n'
    s += f'\n{_text[-8 + koef]}\n{_text[-7 + koef]}\n{_text[-5 + koef]}'
    await bot.reply_to(message, s, reply_markup=lab_kb)


async def reseting():
    for i in places:
        i.found = False
    for i in raids:
        i.IsValid = False
        i.city = '🕧None'
        i.zone = 0
    for i in maps[1:]:
        for j in i.colors:
            for k in range(len(j)):
                j[k] = 0
        for j in i.objects:
            for k in range(len(j)):
                j[k] = "🌫️"
    await update_data_users()
    await update_data_places()
    await update_data_rc()
    await update_data_maps()


async def check_raid_poll(message_with_poll):
    for i in polls:
        if i.raid_poll_id == message_with_poll.poll.id:
            _s = 'Идут:\n'
            for j in i.idu:
                _s += f'@{j}, '
            # await bot.send_message(i.off_id, _s)
            _s += '\n\nНа точке:\n'
            for j in i.na_tochke:
                _s += f'@{j}, '
            # await bot.send_message(i.off_id, _s)
            _s += '\n\nВ шаге:\n'
            for j in i.v_shage:
                _s += f'@{j}, '
            # await bot.send_message(i.off_id, _s)
            _s += '\n\nОпаздывают:\n'
            for j in i.opazdyvayu:
                _s += f'@{j}, '
            await bot.send_message(i.off_id, _s)
            polls.pop(polls.index(i))
            # print(polls)


async def pin_na_meste(id_poll):
    for i in polls:
        if i.raid_poll_id == id_poll:
            # print(str(i))
            k = 0
            s = 'Шаг на точку!\n'
            for j in i.v_shage:
                s += f'@{j}\n'
                k += 1
                if k == 5:
                    k = 0
                    await bot.send_message(RAID_GROUP, s)
                    s = 'Шаг на точку!\n'
            if k != 0:
                await bot.send_message(RAID_GROUP, s)


async def lab_tun(message, mn=+1):
    # print(str(mn) + 'tun')
    _text = message.text.split('\n')
    s = f'{_text[0]}\n{_text[1]}\n'
    now_tun = int(_text[-1].split('Тюнинг: ')[1][:-1])
    next_tun = now_tun + mn * 5 if now_tun + mn * 5 >= -95 else -95
    s += f'+{round(int(_text[2][:-1] if not ("⚔️" in _text[2]) else _text[2][:-2]) / (100 + now_tun) * (100 + next_tun))}{_text[2][-1:] if not ("⚔️" in _text[2]) else _text[2][-2:]}\n\n{_text[4]}\n'
    for i in _text:
        for j in shmot_dops:
            if j[0] in i:
                if j[0] == j[-1]:
                    s += f'{j[0]} +{round(int(re.split(f"   🔄|{j[0]}", i)[1]) / (100 + now_tun) * (100 + next_tun))}   🔄: {i.split("   🔄: ")[1]}\n'
                else:
                    s += i + '\n'
    _hp = round(int(_text[-2][:-1]) / (100 + now_tun) * (100 + next_tun))
    s += f'\n{_text[-3]}\n{_hp} {_text[-2][-1]}\nТюнинг: {"+" if next_tun >= 0 else ""}{next_tun}%'
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=s, reply_markup=lab_kb)
    # print(now_tun)


async def lab_sharp(message, mn=+1):
    _text = message.text.split('\n')
    _s = re.split('\(|✨\)', _text[0])
    s = _s[0]
    # print(_s)
    sharp = 0 if len(_s) == 1 else int(_s[1])
    # print(sharp)
    s += '\n' if sharp + mn <= 0 else f'(+{sharp + mn}✨)\n'
    s += _text[1] + '\n'
    if mn + sharp >= 0:
        s += f'+{round(int(_text[2][:-1] if not ("⚔️" in _text[2]) else _text[2][:-2]) * ((1.05) ** mn))}{_text[2][-1:] if not ("⚔️" in _text[2]) else _text[2][-2:]}\n'
    else:
        s += _text[2] + '\n'
    for i in range(3, len(_text)):
        s += _text[i] + '\n'

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=s, reply_markup=lab_kb)

async def text_to_time(text):
    """2мин 59сек"""
    a=re.split('мин |сек', text)
    t=0
    if 'мин ' in text:
        t+=int(a[0])*60
    if 'сек' in text:
        t+=int(a[-2])
    return t

async def points_reset():
    if int(time.strftime('%w', time.gmtime())) == 0:
        await reseting()
        for i in users:
            try:
                await bot.send_message(i.uid, "Перетряс!\nНе забудьте также обновить профиль!")
            except:
                print(i.uid)
        await bot.send_message(ADMIN_ID, 'сбросил бд')
    else:
        await bot.send_message(ADMIN_ID, 'фальшстарт')


async def kk_pin_2_h():
    for i in users:
        if i.kk:
            try:
                await bot.send_message(i.uid, "Осталось 2 часа до круга крови!")
            except:
                print(i.uid)


async def kk_pin_1_h():
    for i in users:
        if i.kk:
            try:
                await bot.send_message(i.uid, "Остался 1 час до круга крови!")
            except:
                print(i.uid)


async def kk_pin_30_m():
    for i in users:
        if i.kk:
            try:
                await bot.send_message(i.uid, "Осталось полчаса до круга крови!")
            except:
                print(i.uid)


async def kk_pin_3_m():
    for i in users:
        if i.kk:
            try:
                await bot.send_message(i.uid, "Осталось 3 минуты до круга крови!")
                i.kk = False
            except:
                print(i.uid)


async def zel_to_sin():
    for i in maps:
        for j in i.colors:
            for l in range(len(j)):
                if j[l] == 2:
                    j[l] = 1
        for j in i.objects:
            for l in range(len(j)):
                if j[l] == '🧿':
                    j[l] = '◻️'


async def last_peretryas(r):
    # 315000, 604800
    t = time.time()
    return r - (t - (t - 315000) % 604800)


async def lab_qual(message, mn=+1):
    _text = message.text.split('\n')


async def main():
    scheduler.add_job(zel_to_sin, "cron", minute=30)
    scheduler.add_job(points_reset, "cron", hour=15, minute=30)
    scheduler.add_job(kk_pin_2_h, "cron", hour=12, minute=30)
    scheduler.add_job(kk_pin_1_h, "cron", hour=13, minute=30)
    scheduler.add_job(kk_pin_30_m, "cron", hour=14, minute=0)
    scheduler.add_job(kk_pin_3_m, "cron", hour=14, minute=27)
    scheduler.start()
    await bot.polling()


asyncio.run(main())
