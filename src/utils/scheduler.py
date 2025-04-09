from apscheduler.schedulers.asyncio import AsyncIOScheduler

def schedule_func(func):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=func, trigger="cron", hour=12, minute=5)
    scheduler.start()