from core.crud import user_list_for_thanks, delete_user
from core.models.db_helper import db_helper


async def send_thanks_message(bot):
    async with db_helper.session_factory() as session:
        user_list = await user_list_for_thanks(session=session)
        print(user_list)
        for user in user_list:
            await bot.send_message(chat_id = user[0].tg_id,text = 'Спасибо за проявленный интерес. Надеюсь, гайд получился полезным и увлекательным!' )
            await delete_user(user_id=user[0].id)