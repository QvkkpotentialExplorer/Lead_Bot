from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext

import bot
from core.crud import create_action, get_first_notific, get_user, get_user_by_tg_id, get_second_instruction, \
    get_last_user_action
from core.models.db_helper import db_helper
from state import UserState
from tg_bot.tg_bott.answers import *

from tg_bot.tg_bott.keyboards.reply_keyboards import start_reply_keyboard, \
    second_step_reply_keyboard, only_sub_reply_keyboard

first_action_remind_instruction = 'first_action_remind_instruction'
second_action_remind_instruction = 'second_action_remind_instruction'
third_action_remind_instruction = 'third_action_remind_guide'
fourth_action_remind_instruction = 'fourth_action_remind_of_final'
first_notification_about_button = 'first_notification_about_button'
last_action_remind_button = 'last_action_remind_button'
notification_for_pred_sub = 'notification_for_pred_sub'

class SchedulerSendMessage:
    def __init__(self, scheduler: AsyncIOScheduler, chat_id: int, bot, state: FSMContext = None):
        self.scheduler = scheduler
        self.chat_id = chat_id
        self.state = state
        self.bot = bot

    async def first_send_notification_about_instruction(self):

        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=5),
                               kwargs={"type_action": first_action_remind_instruction})

    async def second_send_notification_about_instruction(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=5),
                               kwargs={"type_action": second_action_remind_instruction})

    async def third_send_notification_about_instruction(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=5),
                               kwargs={"type_action": third_action_remind_instruction})

    async def fourth_send_notification_about_instruction(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=5),
                               kwargs={"type_action": fourth_action_remind_instruction})

    async def first_notification_about_success_butoton(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=10),
                               kwargs={"type_action": first_notification_about_button})

    async def last_no_button_user_notification(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=10),
                               kwargs={"type_action": last_action_remind_button})
    async def last_from_pred_last(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=10),
                               kwargs={"type_action": last_action_remind_button})
    async def send_for_pred_sub(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=10),
                               kwargs={"type_action": notification_for_pred_sub})

    async def send_message(self, type_action):

        try:
            user = await self.state.get_data()
            user = user['user']
            async with db_helper.session_factory() as session:
                now_state = await self.state.get_state()
                user = await get_user(session=session, user_id=user.id)
        except:
            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)

        if type_action == first_action_remind_instruction:

            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)
                action = await get_last_user_action(user=user, session=session)
            print('Я В ПЕРВОМ ГАЙДЕ')
            print(action[0].time_action+timedelta(minutes=5),'время клика')
            print(datetime.now(), ' время сейчас')
            if action[0].time_action + timedelta(minutes=5) <= datetime.now()+timedelta(hours=3):
                if now_state == UserState.get_instruction and user.is_sub == False:

                    sub_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                        text='Получить Эксклюзивную инструкцию', url='https://t.me/dorogov_ntofficial')],
                       [InlineKeyboardButton(
                           text='Хочу бесплатную консультацию',
                           url=f'https://consult.tylerdurden.eu.org/track/free_consult/{user.tg_id}/')],
                       [InlineKeyboardButton(
                           text='Хочу описание',
                           url=f'https://consult.tylerdurden.eu.org/track/description/{user.tg_id}/')]])

                    await get_first_notific(user=user)
                    print('Я здесь')
                    await self.bot.send_message(chat_id=self.chat_id, text=notification_of_instruction,
                                                reply_markup=sub_reply_keyboard)
                    self.scheduler.shutdown()

                    scheduler = AsyncIOScheduler()
                    scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=self.chat_id,
                                                                  bot=self.bot, state=self.state)

                    await scheduler_instructions.second_send_notification_about_instruction()
                    scheduler.start()
        if type_action == second_action_remind_instruction:
            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)
            if user.send_full == False and user.send_notification == True:
                await get_second_instruction(user=user)
                await self.bot.send_message(chat_id=self.chat_id, text=second_notification_about_instruction,
                                            reply_markup=only_sub_reply_keyboard)
                self.scheduler.shutdown()
                scheduler = AsyncIOScheduler()
                scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=self.chat_id,
                                                              bot=self.bot, state=self.state)



                await scheduler_instructions.third_send_notification_about_instruction()
                scheduler.start()

        if type_action == first_notification_about_button:
            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)
                action = await get_last_user_action(user=user, session=session)
            if action[0].time_action + timedelta(minutes=10 ) <= datetime.now()+timedelta(hours=3):
                if user.send_full ==True:
                    sub_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                            text='Хочу бесплатную консультацию',
                            url=f'https://consult.tylerdurden.eu.org/track/free_consult/{user.tg_id}/')],
                        [InlineKeyboardButton(
                            text='Хочу описание',
                            url=f'https://consult.tylerdurden.eu.org/track/description/{user.tg_id}/')]])
                    await self.bot.send_message(chat_id=self.chat_id, text=notification_about_guide,
                                                reply_markup=sub_reply_keyboard)
                    self.scheduler.shutdown()
                    scheduler = AsyncIOScheduler()
                    scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=self.chat_id,
                                                                  bot=self.bot, state=self.state)

                    await scheduler_instructions.last_no_button_user_notification()
                    scheduler.start()

        if type_action == third_action_remind_instruction:
            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)
            if user.send_second_notification == True:
                print('Я в third_action')
                sub_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text='Хочу бесплатную консультацию',
                        url=f'https://consult.tylerdurden.eu.org/track/free_consult/{user.tg_id}/')]])
                if user.send_full == False:
                    await self.bot.send_message(chat_id=self.chat_id, text=third_notification_about_instruction,
                                                reply_markup=only_sub_reply_keyboard)
                    await self.bot.send_message(chat_id=self.chat_id, text=fourth_notification_about_instruction,
                                                reply_markup=sub_reply_keyboard)
                    self.scheduler.shutdown()
                    scheduler = AsyncIOScheduler()
                    scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=self.chat_id,
                                                                  bot=self.bot, state=self.state)

                    await scheduler_instructions.last_no_button_user_notification()
                    scheduler.start()

        if type_action == notification_for_pred_sub:
            print("АЛЛЛЛЕЕЕЕЕ БЛЧТЬ")
            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)
                action = await get_last_user_action(user=user, session=session)
            print(action[0].time_action + timedelta(minutes=10), 'время клика')
            print(datetime.now(), ' время сейчас')
            if action[0].time_action + timedelta(minutes=10) <= datetime.now() :
                if user.send_full == True and user.is_sub == True:
                   await self.bot.send_message(text = 'Надеюсь гайд получился полезным и увлекательным.',chat_id = self.chat_id)


        if type_action == fourth_action_remind_instruction:
            if user.is_first_instruction == True and user.send_full == False:
                await self.bot.send_message(chat_id=self.chat_id, text=third_notification_about_instruction,
                                            reply_markup=only_sub_reply_keyboard)
                scheduler = AsyncIOScheduler()
                scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=self.chat_id,
                                                              bot=self.bot, state=self.state)
                await scheduler_instructions.last_no_button_user_notification()
                free_cons_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
                    text='Хочу бесплатную консультацию',
                    url=f'https://consult.tylerdurden.eu.org/task/free_consult/{user.tg_id}/')]])
                await self.bot.send_message(chat_id=self.chat_id, text=fourth_notification_about_instruction,
                                            reply_markup=free_cons_reply_keyboard)
                self.scheduler.shutdown()
                scheduler = AsyncIOScheduler()
                scheduler_instructions = SchedulerSendMessage(scheduler=scheduler, chat_id=self.chat_id,
                                                              bot=self.bot, state=self.state)

                await scheduler_instructions.last_no_button_user_notification()
                scheduler.start()

        if type_action == last_action_remind_button:
            async with db_helper.session_factory() as session:
                user = await get_user_by_tg_id(session=session, tg_id=self.chat_id)
                action = await get_last_user_action(user=user,session=session)
            if action[0].time_action+ timedelta(minutes=14)<=datetime.now()+timedelta(hours=3):
                if user.send_notification == True:
                    sub_reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                            text='Хочу бесплатную консультацию',
                            url=f'https://consult.tylerdurden.eu.org/track/free_consult/{user.tg_id}/')],
                        [InlineKeyboardButton(
                            text='Хочу описание',
                            url=f'https://consult.tylerdurden.eu.org/track/description/{user.tg_id}/')]])
                    await self.bot.send_message(chat_id=self.chat_id, text=last_notification_no_button_user,
                                                reply_markup=sub_reply_keyboard)
                else:
                    pass
    # async def first_remind_sub(self):
    #     self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=30),
    #                            kwargs={"type_action": action_remind_of_guide})
