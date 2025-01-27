from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    InputMediaPhoto, InputMedia, Voice, LabeledPrice, WebAppInfo

start_reply_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Получить инструкцию', callback_data='instruc')]])

second_step_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(
        text='Подписаться и получить Эксклюзивную инструкцию',
        url='https://t.me/Test_lead_channel')],
    [InlineKeyboardButton(
        text='Хочу бесплатную консультацию',
        url=f'https://consult.tylerdurden.eu.org/task/free_consult//')],
    [InlineKeyboardButton(
        text='Хочу описание',
        url=f'https://consult.tylerdurden.eu.org/task/description//')],

])

only_sub_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text='Подписаться и получить Эксклюзивную инструкцию',
        url='https://t.me/Test_lead_channel')]])


strr = 'https://t.me/neurotipology_warrior'#консультация
strr2 = 'https://t.me/D_Dorogov'#описание
