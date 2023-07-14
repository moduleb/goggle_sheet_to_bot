from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, Message
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import config
from app.keyboard import markup
from app.service.google_sheets_service import sheet_service


scheduler = AsyncIOScheduler(timezone="Europe/Samara")

class Handler():
    def __init__(self, bot: Bot):
        self.bot = bot

    async def time_is_over(self, sheet_obj):
        print("run: time_is_over")
        chat_member = await self.bot.get_chat_member(chat_id=sheet_obj.tel_id, user_id=sheet_obj.tel_id)

        first_name = chat_member.user.first_name
        last_name = chat_member.user.last_name

        await self.bot.send_message(
            chat_id=config.ADMIN_TEL_ID,
            text=f"{first_name} {last_name} не успел выполнить задание.")
        await self.bot.send_message(
            chat_id=sheet_obj.tel_id,
            text="Время на выполнение задания истекло"
        )

    async def start_task_timer(self, sheet_obj, datetime_):
        await self.send_task(sheet_obj)
        timer_str = sheet_obj.answer_time.split(':')
        timer_hour = int(timer_str[0])
        timer_min = int(timer_str[1])
        scheduler.add_job(
            self.time_is_over,
            next_run_time=datetime_ + timedelta(hours=timer_hour, minutes=timer_min),
            kwargs={"sheet_obj": sheet_obj},
            id="time_is_over"
        )
        scheduler.print_jobs()

    async def process_load_task_handler(self, msg: Message):
        if msg.from_user.id != config.ADMIN_TEL_ID:
            return
        await msg.reply('ok')

        sheet_obj = sheet_service.get_sheet_obj()
        datetime_str = f"{sheet_obj.date} {sheet_obj.time}"
        datetime_ = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S")
        scheduler.add_job(
            self.start_task_timer,
            next_run_time=datetime_,
            kwargs={"sheet_obj": sheet_obj, "datetime_": datetime_}
        )
        scheduler.start()
        scheduler.print_jobs()

    async def process_get_result(self, call: CallbackQuery):

        job: Job = scheduler.get_job('time_is_over')

        if not job:
            return

        job.remove()

        call_ = call.data.split('_')[-1]

        first_name = call.from_user.first_name
        last_name = call.from_user.last_name

        if call_ == "true":
            text = f"{first_name} {last_name} выполнил задание."
        if call_ == "false":
            text = f"{first_name} {last_name} не выполнил задание."

        await self.bot.send_message(
            chat_id=config.ADMIN_TEL_ID,
            text=text)

        await call.message.reply("Задание завершено")

    async def process_start_command(self, msg: Message):
        await msg.reply(
            f"👋 Здравствуйте {msg.from_user.first_name}!\n\n"
            f"Как только появиться задание - мы вас уведомим.\n"
            f"Ожидайте сообщения...",
            reply=False)

    async def send_task(self, sheet_obj):

        text = f"Получено новое задание:\n" \
               f"{sheet_obj.text}\n" \
               f"Время выполнения: {sheet_obj.answer_time} "

        await self.bot.send_message(
            chat_id=sheet_obj.tel_id,
            text=text,
            reply_markup=markup)


def register_handlers(dp: Dispatcher):
    handler = Handler(dp.bot)
    dp.register_message_handler(handler.process_load_task_handler, commands="load_task", state="*")
    dp.register_callback_query_handler(handler.process_get_result, text_startswith="done_", state='*')
    dp.register_message_handler(handler.process_start_command, commands="start", state='*')
