import datetime
from datetime import timedelta,datetime

import pytz
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, ActionWay, Action

from google_api import GoogleSheetApi
from google_api_config import service, user_spreadsheet_id, user_spreadsheet_action_id


user_sheet_api = GoogleSheetApi(service = service,spreadsheet_id=user_spreadsheet_id)
user_action_sheet = GoogleSheetApi(service = service,spreadsheet_id=user_spreadsheet_action_id)
async def create_user(tg_id: int, phone: str, username: str, account_url: str, session: AsyncSession):
    user_exist = select(User).filter(User.tg_id == tg_id)
    user_exist = await session.execute(user_exist)
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
        user_sheet_api.add_user(tg_id = tg_id,username=username,account_url=account_url,phone= phone,id = user.id)
        user_action_sheet.create_user_action(user_id = user.id,type_action='/start',time=f"{action.time_action.strftime('%Y-%m-%dT%H:%M:%S')}")
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
async def users_for_final(session:AsyncSession):
    users = select(User,ActionWay).filter(ActionWay.get_instruct==True,User.send_final==False)

    users = await session.execute(users)
    users = users.all()
    return users
async def get_instuct_user(user,session:AsyncSession):

    stmt = (update(ActionWay).where(ActionWay.user_id==user.id).values(get_instruct=True))
    await session.execute(stmt)
    await session.commit()

async def get_complete_user(tg_id,session:AsyncSession):
    user = select(User).filter(User.tg_id == tg_id)
    user = await session.execute(user)
    user = user.scalar()
    stmt = (update(ActionWay).where(ActionWay.user_id==user.id).values(get_complete=True))
    await session.execute(stmt)
    await session.commit()

async def get_first_instruct(session:AsyncSession,user,action):
    user_sheet_api.get_instruction(id = user.id)
    user_action_sheet.create_user_action(user_id=user.id,type_action='/get_instructions', time = action.time_action.strftime('%Y-%m-%dT%H:%M:%S'))
    user_sheet_api.get_instruction(id = user.id)
    await get_instuct_user(session=session,user=user)

async def get_final_user(users,session:AsyncSession):
    for  user in users:
        stmt = (update(User).where(User.id == user[0].id).values(send_final = True))

        await session.execute(stmt)
        await session.commit()

