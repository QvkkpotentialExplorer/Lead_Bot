import pytz
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaDocument, InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from core.crud import create_user, create_action, get_last_iteration, get_instuct_user, get_full_instruct_user, \
    users_for_sub, user_get_first_instructions, get_first_notific, check_activity, delete_user, \
    get_user_by_tg_id_for_app, user_list_for_thanks, get_new_user, get_user, get_user_by_tg_id
from core.models.db_helper import db_helper
from google_api import GoogleSheetApi
from google_api_config import service, user_spreadsheet_id, user_spreadsheet_action_id
from state import UserState

from tg_bot.tg_bott.keyboards.reply_keyboards import start_reply_keyboard, \
    second_step_reply_keyboard
from tg_bot.tg_bott.scheduler.scheduler_message import SchedulerSendMessage
import aiogram.utils.markdown as fmt

router = Router()

CHANNEL_ID = -1002243326484

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    now_state = await state.get_state()
    await message.answer('Готовы забрать инструкцию?',
                         reply_markup=start_reply_keyboard)
    async with db_helper.session_factory() as session:
        user = await create_user(tg_id=message.chat.id, phone='',
                                 username=message.from_user.username,
                                 account_url=f'https://t.me/{message.from_user.username}', session=session)
    async with db_helper.session_factory() as session:
        await get_new_user(user=user, session=session)

    print('Я здесть')



    await state.set_state(UserState.get_start)
    print(user)
    await state.update_data(user=user)
        # scheduler = AsyncIOScheduler()
        # scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=message.chat.id, bot=message.bot,
        #                                               state=state)
        # scheduler.start()

        # await scheduler_instructions.send_notification_about_instruction()

    async with db_helper.session_factory() as session:
        action = await create_action(type_action='click_start', user_id=user.id, session=session)


@router.callback_query(F.data == 'instruc')
async def get_first_instructions(call: types.CallbackQuery, state: FSMContext):
    try:
        user = await state.get_data()
        user = user['user']
        async with db_helper.session_factory() as session:
            now_state = await state.get_state()
            user = await get_user(session=session, user_id=user.id)
    except:
        async with db_helper.session_factory() as session:
            user = await get_user_by_tg_id(session=session, tg_id=call.chat_id)

    async with db_helper.session_factory() as session:
        # action = await create_action(type_action='click_get_instruction', user_id=user.id, session=session)
        await user_get_first_instructions(session=session, user=user)

    now_state = await state.get_state()
    await state.set_state(UserState.get_instruction)
    file_path = r"tg_bot/tg_bott/handlers/Гайд по чертам.pdf"  # Укажите свой путь к файлу
    flag = await check_sub(chat_id=user.tg_id, channel_chat_id=CHANNEL_ID, bot=call.bot)
    if flag:
        file2_path = r"tg_bot/tg_bott/handlers/Эксклюзивный гайд.pdf"  # Укажите свой путь к файлу
        second_file = FSInputFile(file2_path)
        media = [InputMediaDocument(media=second_file,
                                    caption='Спасибо за проявленный интерес к моему каналу. Вот ваш Эксклюзивный гайд')]
        await call.bot.send_media_group(media=media, chat_id=user.tg_id)

        async with db_helper.session_factory() as session:
            await get_full_instruct_user(session=session, user_id=user.id)
        scheduler = AsyncIOScheduler()

        scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=call.message.chat.id,
                                                      bot=call.message.bot, state=state)
        print("Аээээээээээээээээээээээээээээээээээээээээ")

        await scheduler_instructions.send_for_pred_sub()
        scheduler.start()
    else:
        # Загружаем файл
        file_to_send = FSInputFile(file_path)

        # Отгыук = правка файла пользователю
        await call.message.bot.send_document(chat_id=user.tg_id,
                                             document=file_to_send,
                                             caption="Вот ваша инструкция!")
        await call.answer()
        await state.set_state(UserState.get_instruction)
        scheduler = AsyncIOScheduler()

        scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=call.message.chat.id,
                                                      bot=call.message.bot, state=state)
        print('Я  В INSTRUC')
        await scheduler_instructions.first_send_notification_about_instruction()
        scheduler.start()
        await state.update_data(user=user)
        # await call.message.answer(
        #    text = 'Понравился гайд? подпишись на мой канал и получишь Эксклюзивную инструкцю с дополнителными советами!\nПоверьте, вы не пожалеете',
        #     reply_markup=second_step_reply_keyboard)
        #
        # if now_state == UserState.get_start:
        #
        #     async with db_helper.session_factory() as session:
        #
        #         await get_instuct_user(session=session, user=user)
        #         await get_first_instruct(session=session, action=action, user=user)
        #         await state.set_state(UserState.get_instruction)

        #
        # scheduler.start()
        # await scheduler_instructions.send_notification_about_guide()
        # else:
        #     pass


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    now_user = await get_user_by_tg_id_for_app(tg_id=event.from_user.id)
    if now_user != None:
        if now_user.send_full == False:
            sub_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text='Хочу бесплатную консультацию',
                    url=f'https://consult.tylerdurden.eu.org/track/free_consult/{now_user.tg_id}/')],
                [InlineKeyboardButton(
                    text='Хочу описание',
                    url=f'https://consult.tylerdurden.eu.org/track/description/{now_user.tg_id}/')]])

            flag_activity = await check_activity(user=now_user)

            bot = event.from_user.bot
            file_path = r"tg_bot/tg_bott/handlers/Эксклюзивный гайд.pdf"  # Укажите свой путь к файлу

            file_to_send = FSInputFile(file_path)
            if event.chat.id == CHANNEL_ID and event.new_chat_member.status == "member":
                if now_user.send_notification == True and now_user.is_first_instruction == True:
                    caption = "Вот эксклюзивная инструкция с дополнительными советами. Изучите и подумайте насколько вам это знакомо и откликается"
                    await event.bot.send_document(chat_id=now_user.tg_id,
                                                  document=file_to_send,
                                                  caption=caption,
                                                  reply_markup=sub_reply_keyboard)
                else:
                    caption = 'Спасибо за проявленный интерес к моему каналу. Вот ваш Эксклюзивный гайд'
                    await event.bot.send_document(chat_id=now_user.tg_id,
                                                  document=file_to_send,
                                                  caption=caption)
                    scheduler = AsyncIOScheduler()

                    scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=now_user.tg_id,
                                                                  bot=bot)
                    print("Аээээээээээээээээээээээээээээээээээээээээ")

                    await scheduler_instructions.send_for_pred_sub()
                    scheduler.start()


                if flag_activity:
                    await event.bot.send_message(chat_id=now_user.tg_id,
                                                 text='Спасибо за проявленный интерес. Надеюсь, гайд получился полезным и увлекательным!')
                    await delete_user(user_id=now_user.id)
                else:
                    scheduler = AsyncIOScheduler()
                    scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=now_user.tg_id,
                                                                  bot=bot)

                    await scheduler_instructions.first_notification_about_success_butoton()
                    scheduler.start()
                async with db_helper.session_factory() as session:

                    await get_full_instruct_user(session=session, user_id=now_user.id)




async def check_sub(chat_id, channel_chat_id, bot):
    member = await bot.get_chat_member(chat_id=channel_chat_id, user_id=chat_id)

    return member.status == 'member' or member.status == "creator" or member.status == "administrator"
