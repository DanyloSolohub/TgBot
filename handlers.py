from main import bot, dp
from config import admin_id
from aiogram import types
import datetime
import requests
import time


async def send_to_admin_start(*args):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


async def send_to_admin_shut(*args):
    await bot.send_message(chat_id=admin_id, text='Бот отключен')


@dp.message_handler(commands=['start', 'help'])
async def start_info(message: types.Message):
    await message.reply(
        text='To start using this bot, you should: \n1) Enter a currency to view the exchange rate\n'
             'Example:<b> USD </b> \n'
             '2) /exchange to exchange 2 currencies\n'
             '3) /list to view all available currencies\n'
             '4) /history to view history per last 7 days', reply=False)


@dp.message_handler(commands=['exchange'])
async def exchange_info(message: types.Message):
    await message.answer(text='Enter number and 2 currencies: \nExample: 10 USD to CAD', reply=False)


@dp.message_handler(lambda message: message.text[0].isdigit())
async def exchange(message: types.Message):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    r = requests.get(url=url)
    response = r.json()
    mess = ''.join([i if not i.isspace() else '' for i in message.text])
    mess_split = mess.split('to')
    digit = int(''.join([i for i in mess_split[0] if i.isdigit()]))
    first_curr = ''.join([i for i in mess_split[0] if i.isalpha()]).upper()
    second_curr = ''.join([i for i in mess_split[-1] if i.isalpha()]).upper()
    for i in response:
        if i.get('cc') == first_curr:
            digit *= i.get('rate')
        if i.get('cc') == second_curr:
            digit /= i.get('rate')
    await message.reply(
        text=f"{message.text} = {round(digit, 2)}", reply=False)


@dp.message_handler(commands=['history'])
async def exchange_info(message: types.Message):
    await message.answer(text='Enter "history {currency}"\nExample: history USD', reply=False)


@dp.message_handler(lambda message: message.text.startswith('history'))
async def history(message: types.Message):
    now = str(datetime.datetime.now().date())
    value_history = ''
    msg = message.text.split(' ')[1]
    date = ''.join(now.split('-'))
    for i in range(7):
        new_date = int(date) - i
        url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={msg}&date={new_date}&json'
        r = requests.get(url=url)
        response = r.json()
        value_history += f'{response[0].get("exchangedate")}:<b>{round(response[0].get("rate"), 2)}</b> \n'
    await message.answer(text=value_history, reply=False)


start_time = 0
send = ''


@dp.message_handler(commands=['list'])
async def list_view(message: types.Message):
    global send
    global start_time
    if start_time != 0 & (time.time() - start_time > 600):
        send = ''
    if not send:
        start_time = time.time()
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        r = requests.get(url=url)
        response = r.json()
        for i in response:
            send += f"{i.get('txt')} (<b>{i.get('cc')}</b>), rate: {round(float(i.get('rate')), 2)} \n"
    await message.reply(
        text=f"{send}", reply=False)


@dp.message_handler()
async def request_value(message: types.Message):
    val_code = message.text.upper().strip()
    url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={val_code}&json'
    r = requests.get(url=url)
    response = r.json()
    if response:
        await message.reply(text=f"<b>{response[0].get('cc')}: {round(float(response[0].get('rate')), 2)} </b>",
                            reply=False)
