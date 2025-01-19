from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext

from core.crud import create_action
from core.models.db_helper import db_helper
from state import UserState
from tg_bot.tg_bott.answers import notification_of_instruction, notification_about_guide, \
    notification_about_guide_additional, notification_final_main, notification_final_additional
from tg_bot.tg_bott.keyboards.reply_keyboards import end_reply_keyboard, start_reply_keyboard

action_remind_instruction = 'action_remind_instruction'
action_remind_of_guide = 'action_remind_guide'
action_remind_of_final = 'action_remind_of_final'


class SchedulerSendMessage:
    def __init__(self, scheduler: AsyncIOScheduler, chat_id: int, state: FSMContext, bot):
        self.scheduler = scheduler
        self.chat_id = chat_id
        self.state = state
        self.bot = bot

    async def send_notification_about_instruction(self):

        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=15),
                               kwargs={"type_action": action_remind_instruction})

    async def send_notification_about_guide(self):
        self.scheduler.add_job(self.send_message, 'date', run_date=datetime.now() + timedelta(minutes=30),
                               kwargs={"type_action": action_remind_of_guide})



    async def send_message(self, type_action):
        async with db_helper.session_factory() as session:
            now_state = await self.state.get_state()
            user = await self.state.get_data()
            user = user['user']
        if type_action == action_remind_instruction:
            print('Я туту')

            if now_state == UserState.get_start:
                await self.bot.send_message(chat_id=self.chat_id, text=notification_of_instruction,
                                            reply_markup=start_reply_keyboard)
                await create_action(user_id=user.id, type_action='send_notif_instruction', session=session)
                self.scheduler.shutdown()
            else:
               pass
        if type_action == action_remind_of_guide:
            if now_state == UserState.get_instruction:
                await self.bot.send_message(chat_id=self.chat_id, text=notification_about_guide)
                await self.bot.send_message(chat_id=self.chat_id, reply_markup=end_reply_keyboard,
                                            text=notification_about_guide_additional)
                await create_action(user_id=user.id, type_action='send_notif_guide', session=session)
                self.scheduler.shutdown()
