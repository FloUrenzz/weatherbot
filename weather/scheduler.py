from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_all_users, get_user_settings
from weather_api import get_current_weather
from aiogram import Bot

scheduler = AsyncIOScheduler()


async def send_daily_weather(bot: Bot, user_id: int):
    """Отправляет ежедневное уведомление с погодой."""
    city, _ = get_user_settings(user_id)
    if not city:
        return
    weather_text = await get_current_weather(city)
    try:
        await bot.send_message(chat_id=user_id, text=weather_text, parse_mode="Markdown")
    except Exception:
        pass


def schedule_jobs(bot: Bot):
    """Добавляет задания для всех пользователей с установленным notify_time."""
    users = get_all_users()
    for user_id, city, notify_time in users:
        if notify_time:
            job_id = f"user_{user_id}"
            try:
                scheduler.remove_job(job_id)
            except:
                pass
            hour, minute = notify_time.split(":")
            scheduler.add_job(
                send_daily_weather,
                trigger='cron',
                hour=int(hour),
                minute=int(minute),
                args=[bot, user_id],
                id=job_id,
                replace_existing=True
            )


def start_scheduler():
    scheduler.start()
