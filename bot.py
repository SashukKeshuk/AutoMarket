import asyncio
import translators as tr
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, web_app_info
from config import API
from db import get_balance, edit_balance, select_good, select_goods, get_history, get_good, edit_history, get_user, add_user
from crypto import init, check

bot = Bot(token=API)
dp = Dispatcher(bot)


markup = InlineKeyboardMarkup()
goods = InlineKeyboardButton('Товары', callback_data='goods')
prof = InlineKeyboardButton('Профиль', callback_data='prof')
pay = InlineKeyboardButton('Пополнение', callback_data='pay')
support = InlineKeyboardButton('Техническая поддержка', callback_data='support')
lng = InlineKeyboardButton('RU/ENG', callback_data='language')
about = InlineKeyboardButton('О нас', callback_data='about')

markup.add(goods).add(prof).add(pay).add(support).add(lng).add(about)

goods_markup = InlineKeyboardMarkup()
markup2 = InlineKeyboardMarkup()
buy = InlineKeyboardButton('Купить', callback_data='buy')
markup2.add(buy)

markup3 = InlineKeyboardMarkup()
markup3.add(pay)


Emarkup = InlineKeyboardMarkup()
Egoods = InlineKeyboardButton('Products', callback_data='goods')
Eprof = InlineKeyboardButton('Profile', callback_data='prof')
Epay = InlineKeyboardButton('Payment', callback_data='pay')
Esupport = InlineKeyboardButton('Technical support', callback_data='support')
Elng = InlineKeyboardButton('RU/ENG', callback_data='language')
Eabout = InlineKeyboardButton('About us', callback_data='about')

Emarkup.add(Egoods).add(Eprof).add(Epay).add(Esupport).add(Elng).add(Eabout)

Egoods_markup = InlineKeyboardMarkup()
Emarkup2 = InlineKeyboardMarkup()
Ebuy = InlineKeyboardButton('Buy', callback_data='buy')
markup2.add(Ebuy)

markup3 = InlineKeyboardMarkup()
markup3.add(Epay)


goods_list = []
i = 0
lng = 'RU'

async def on_startup(_):
    print('bot online')

@dp.message_handler(commands=['start'])
async def start(msg : types.Message):
    print(f'current user id - {msg.from_user.id}')
    if (get_user(msg.from_user.id) == False):
        add_user(msg.from_user.id)
    if (lng == 'RU'):
        await bot.send_message(msg.from_user.id, 'хай', parse_mode='html', reply_markup=markup)
    else:
        await bot.send_message(msg.from_user.id, 'hi', parse_mode='html', reply_markup=Emarkup)

@dp.callback_query_handler(text='goods')
async def goods(msg : types.Message):
    global goods_list
    goods_list = select_goods()
    for i in range(0, len(goods_list)):
        btn = InlineKeyboardButton(goods_list[i]['name'], callback_data=f'good {i}')
        goods_markup.add(btn)
    if (lng == 'RU'):
        await bot.send_message(msg.from_user.id, f"Наши товары", parse_mode='html', reply_markup=goods_markup)
    else:
        await bot.send_message(msg.from_user.id, f"Our products", parse_mode='html', reply_markup=goods_markup)

@dp.callback_query_handler(text='prof')
async def prof(msg : types.Message):
    balance = get_balance(msg.from_user.id)
    bal = balance[0]['balance']
    history_get = get_history(msg.from_user.id)
    history = []
    history = history_get[0]['history'].split(' ')
    s = "Были куплены следующие товары:\n\n\n"
    s1 = "Ваш баланс"
    s2 = "История покупок пока пуста.."
    p = "за"
    if (lng == 'ENG'):
        s = "Next products where bought:\n\n\n"
        s1 = "Your balance"
        s2 = "History of purchases is still empty.."
        p = "for"
    f = 0
    for h in history:
        if (h.isnumeric()):
            f = 1
            print(str(h))
            data = get_good(h)
            s += '<b>' + str(data[0]['name']) + '</b> ' + p + ' <i>' + str(data[0]['cost']) + '$</i>\n\n'
    if (f == 0):
        await bot.send_message(msg.from_user.id, f'{s1} - <b><u>{bal}$</u></b>\n\n{s2}', parse_mode='html', reply_markup=markup3)
    else:
        await bot.send_message(msg.from_user.id, f'{s1} - <b><u>{bal}$</u></b>\n\n{s}', parse_mode='html', reply_markup=markup3)

@dp.callback_query_handler(text='pay')
async def pay(msg : types.Message):
    wallet = init()
    await bot.send_message(msg.from_user.id, f"Внимание!\n"
                                             f"Нужно перевести средства в течении часа, в противном случае они не будут зачислены\n"
                                             f"На выполнение транзакции в Blockchain требуется время (до 30 мин)\n"
                                             f"Кошелек:")
    await bot.send_message(msg.from_user.id, wallet['addr'])
    payment = check(wallet['addr'], wallet['balance'])
    await bot.send_message(msg.from_user.id, f"Адрес был закрыт, ваш баланс был пополнен на {payment}")

@dp.callback_query_handler(text='support')
async def support(msg : types.Message):
    if (lng == 'RU'):
        await bot.send_message(msg.from_user.id, 'Техническая поддержка', parse_mode='html')
    else:
        await bot.send_message(msg.from_user.id, 'technical support', parse_mode='html')

@dp.callback_query_handler(text='language')
async def language(msg : types.Message):
    global lng
    if (lng == 'RU'):
        lng = 'ENG'
    else:
        lng = 'RU'
    #await bot.send_message(msg.from_user.id, f'current language - {lng}', parse_mode='html')

@dp.callback_query_handler(text='about')
async def about(msg : types.Message):
    if (lng == 'RU'):
        await bot.send_message(msg.from_user.id, 'Статья о нас')
    else:
        await bot.send_message(msg.from_user.id, 'Article about us')

@dp.callback_query_handler(text='buy')
async def buy(msg : types.Message):
    global goods_list
    global i
    balance = get_balance(msg.from_user.id)
    bal = balance[0]['balance']
    if (goods_list[i]['cost'] > bal):
        await bot.send_message(msg.from_user.id, 'Недостаточно средств', parse_mode='html')
    elif (goods_list[i]['cost'] <= bal):
        await buy_process(msg.from_user.id, bal, goods_list[i]['cost'], goods_list[i]['good_id'])
        await bot.send_message(msg.from_user.id, 'Товар заказан', parse_mode='html')
    print(f"buy - good {i} with cost - {goods_list[i]['cost']} with balance - {bal}")

@dp.callback_query_handler()
async def query(msg : types.Message):
    if (msg['data'][0]=='g'):
        good_id = int(msg['data'][5:])
        await description(good_id, msg.from_user.id)

async def description(good_id, user_id):
    global goods_list
    global i
    i = good_id
    operator = Bot(API)
    s = goods_list[good_id]['text']
    if (lng == 'ENG'):
        s = tr.google(s, from_language='ru', to_language='en')
    await operator.send_message(user_id, s, parse_mode='html', reply_markup=markup2)

async def buy_process(user_id, bal, cost, good_id):
    edit_balance(user_id, (bal-cost))
    edit_history(user_id, good_id)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)