import datetime
from datetime import timedelta,datetime

import pytz
from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, ActionWay, Action
from core.models.db_helper import db_helper

from google_api import GoogleSheetApi
from google_api_config import service, user_spreadsheet_id, user_spreadsheet_action_id


user_sheet_api = GoogleSheetApi(service = service,spreadsheet_id=user_spreadsheet_id)
user_action_sheet = GoogleSheetApi(service = service,spreadsheet_id=user_spreadsheet_action_id)
async def create_user(tg_id: int, phone: str, username: str, account_url: str, session: AsyncSession):
    user_exist = select(User).filter(User.tg_id == tg_id)
    user_exist = await session.execute(user_exist)
    print(user_exist)
    user_exist = user_exist.scalar()
    if not user_exist:
        user = User(tg_id=tg_id, phone=phone, username=username, account_url=account_url)

        session.add(user)
        await session.commit()
        action_way = ActionWay(user_id=user.id, start_click=True)
        action = Action(type_action='click_start',user_id = user.id ,time_action = datetime.now(pytz.utc).astimezone(pytz.timezone('Europe/Moscow')))
        session.add(action_way)
        session.add(action)
        await session.commit()
        # user_sheet_api.add_user(tg_id = tg_id,username=username,account_url=account_url,phone= phone,id = user.id)
        # user_action_sheet.create_user_action(user_id = user.id,type_action='/start',time=f"{action.time_action.strftime('%Y-%m-%dT%H:%M:%S')}")
    else:
        user = user_exist
    return user


async def create_action(user_id, type_action, session: AsyncSession):
    user_action = Action(user_id=user_id, type_action=type_action,time_action = datetime.now(pytz.utc).astimezone(pytz.timezone('Europe/Moscow')))
    session.add(user_action)
    await session.commit()
    return user_action


async def get_last_iteration(user,session:AsyncSession):
    last_iteration =  select(Action).filter(Action.user_id == user.id)
    last_iteration = await session.execute(last_iteration)
    last_iteration = last_iteration.all()[-1]

    return last_iteration
    # Преобразуем в нужную временную зону, например, в Московское время
async def users_for_sub(session:AsyncSession):
    users = select(User).filter(User.send_notification==True,User.is_first_instruction==True,User.is_sub==False,User.send_full == False)

    users = await session.execute(users)
    users = users.all()
    return users
async def get_instuct_user(user,session:AsyncSession):

    stmt = (update(ActionWay).where(ActionWay.user_id==user.id).values(get_instruct=True,))
    await session.execute(stmt)
    await session.commit()

async def get_full_instruct_user(user_id,session:AsyncSession):
    print('Я здесть')
    stmt = (update(User).where(User.id==user_id).values(is_sub = True,send_full = True))
    print(stmt)
    print('ЧТО ЗА НАХУЙ')
    await session.execute(stmt)
    await session.commit()

# async def get_first_instruct(session:AsyncSession,user,action):
#     user_sheet_api.get_instruction(id = user.id)
#     user_action_sheet.create_user_action(user_id=user.id,type_action='/get_instructions', time = action.time_action.strftime('%Y-%m-%dT%H:%M:%S'))
#     user_sheet_api.get_instruction(id = user.id)
#     await get_instuct_user(session=session,user=user)




async def get_first_notific(user):
    async with db_helper.session_factory() as session:
        print(user.id)
        stmt = (update(User).where(User.id == user.id).values(send_notification = True))
        print(stmt)

        await session.execute(stmt)
        print('яя туту')
        await session.commit()
        print('Я под комитом')


async def user_get_first_instructions(session:AsyncSession,user):
    stmt = (update(User).where(User.id==user.id).values(is_first_instruction = True))


    await session.execute(stmt)
    await session.commit()

async def get_user(session:AsyncSession,user_id):
    user = select(User).where(User.id == user_id)
    user = await session.execute(user)
    return user.scalar()

async def get_user_by_tg_id(session:AsyncSession,tg_id):
    user = select(User).where(User.tg_id == tg_id)
    user = await session.execute(user)
    return user.scalar()

async def get_user_by_tg_id_for_app( tg_id):
    async with db_helper.session_factory() as session:
        user = select(User).where(User.tg_id == tg_id)
        user = await session.execute(user)
        return user.scalar()
async def get_free_consult(user):
    async with db_helper.session_factory() as session:
        stmt = (update(User).where(User.id == user.id).values(get_free_consult=True))
        await session.execute(stmt)
        await session.commit()

async def get_description(user):
    async with db_helper.session_factory() as session:
        stmt = (update(User).where(User.id == user.id).values(get_free_description=True))
        await session.execute(stmt)
        await session.commit()


async def get_second_instruction(session:AsyncSession,user):
    stmt = (update(User).where(User.id == user.id).values(send_second_notification=True))
    await session.execute(stmt)
    await session.commit()
#функция проверки перешл ли пользователь по сслыки описания или бесплатной консультации
async def check_activity(user):
    print(user)
    if user.get_free_consult == True or user.get_free_description==True:
        return True
    else:
        return False

async def delete_user(user_id: int):
    async with db_helper.session_factory() as session:
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()


async def user_list_for_thanks(session:AsyncSession):

    user = select(User).where(User.send_full == True, or_(
    User.get_free_consult == True,
    User.get_free_description == True
))
    user = await session.execute(user)
    return user.all()
