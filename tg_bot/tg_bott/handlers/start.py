import pytz
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from core.crud import create_user, create_action, get_last_iteration, users_for_final, get_instuct_user, \
    get_first_instruct, get_final_user
from core.models.db_helper import db_helper
from google_api import GoogleSheetApi
from google_api_config import service, user_spreadsheet_id, user_spreadsheet_action_id
from state import UserState
from tg_bot.tg_bott.answers import notification_final_main, notification_final_additional
from tg_bot.tg_bott.keyboards.reply_keyboards import start_reply_keyboard, end_reply_keyboard
from tg_bot.tg_bott.scheduler.scheduler_message import SchedulerSendMessage
import aiogram.utils.markdown as fmt
router = Router()

scheduler = AsyncIOScheduler()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    now_state = await state.get_state()
    await message.answer('Привет!👋 Забери обещанную инструкцию — она поможет решить твою задачу. Жми на кнопку!',
                         reply_markup=start_reply_keyboard)
    if now_state == None:
        async with db_helper.session_factory() as session:


            user = await create_user(tg_id=message.chat.id, phone='',
                                     username=message.from_user.username,
                                     account_url=f'https://t.me/{message.from_user.username}', session=session)

        await state.set_state(UserState.get_start)
        await state.update_data(user= user)
        scheduler = AsyncIOScheduler()
        scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=message.chat.id, bot=message.bot,
                                                      state=state)
        scheduler.start()

        await scheduler_instructions.send_notification_about_instruction()
    else:
        user = await state.get_data()
        user = user['user']

        async with db_helper.session_factory() as session:
                action = await create_action(type_action='click_start', user_id=user.id, session=session)




@router.callback_query(F.data == 'instruc')
async def get_instructions(call: types.CallbackQuery, state: FSMContext):
    user = await state.get_data()
    print(user)
    user = user['user']
    async with db_helper.session_factory() as session:
        action = await create_action(type_action='click_get_instruction', user_id=user.id, session=session)
    print(action)
    await    call.message.delete()
    now_state = await state.get_state()
    await call.message.answer("Вот твоя <a href= 'https://example.com'>инструкция</a>. Надеюсь, она будет полезной!",parse_mode=ParseMode.HTML)
    await call.message.answer(
        'А если хочешь, запишись на бесплатную консультацию или купи наш продукт, чтобы получить максимум 🚀 ',
        reply_markup=end_reply_keyboard)

    if now_state == UserState.get_start:

        async with db_helper.session_factory() as session:

            await get_instuct_user(session=session, user=user)
            await get_first_instruct(session=session, action=action, user=user)
            await state.set_state(UserState.get_instruction)
            scheduler = AsyncIOScheduler()

            scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=call.message.chat.id,
                                                          bot=call.message.bot, state=state)

            scheduler.start()
            await scheduler_instructions.send_notification_about_guide()
    else:
        pass


async def send_final_message(bot):
    async with db_helper.session_factory() as session:
        users = await users_for_final(session=session)
        users_list = []
        for user in users:
            now_user = user[0]

            last_iteration = await get_last_iteration(user=now_user, session=session)



            moscow_tz = datetime.now(pytz.utc).astimezone(pytz.timezone('Europe/Moscow'))

            # Предположим, что last_iteration[0].time — это naive datetime
            last_iteration_time_naive = last_iteration[0].time_action  # Предположим, это naive datetime (без временной зоны)

            # Локализуем его в Московскую временную зону
            last_iteration_time_aware = pytz.timezone('Europe/Moscow').localize(last_iteration_time_naive)
            print(last_iteration_time_aware,moscow_tz)
            if last_iteration_time_aware + timedelta(minutes=30) < moscow_tz:
                await bot.send_message(chat_id=now_user.tg_id, text=notification_final_main)
                await bot.send_message(chat_id=now_user.tg_id, text=notification_final_additional,
                                       reply_markup=end_reply_keyboard)
                users_list.append(user)
        async with db_helper.session_factory() as session:
            await get_final_user(users=users_list,session=session)
