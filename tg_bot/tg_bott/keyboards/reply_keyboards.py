from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    InputMediaPhoto, InputMedia, Voice, LabeledPrice, WebAppInfo

start_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Получить инструкцию',callback_data='instruc')]])
end_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text = 'Получить бесплатную консультацию',callback_data='cons')],[InlineKeyboardButton(text='Купить продукт', callback_data='product')]])