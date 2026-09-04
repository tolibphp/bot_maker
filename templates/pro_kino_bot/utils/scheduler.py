import os
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.types import FSInputFile
from templates.pro_kino_bot.utils.premium_emoji import PE_CHECK, PE_INFO

logger = logging.getLogger(__name__)

async def send_db_backup(bot: Bot, admin_id: int, db_path: str) -> None:
    """Ma'lumotlar bazasini adminlarga yuboradi."""
    if not os.path.exists(db_path):
        logger.error(f"Zaxira fayli topilmadi: {db_path}")
        return

    try:
        document = FSInputFile(db_path)
        await bot.send_document(
            admin_id,
            document,
            caption=(
                f"{PE_CHECK} <b>Avtomatik zaxira nusxasi (Backup)</b>\n\n"
                f"{PE_INFO} Bu xabar har kuni soat 23:59 da (Toshkent vaqti) "
                f"bazani xavfsiz saqlash uchun yuboriladi."
            ),
            parse_mode="HTML"
        )
        logger.info(f"Backup yuborildi: {admin_id}")
    except Exception as e:
        logger.error(f"Backup yuborishda xatolik ({admin_id}): {e}")

def setup_scheduler(bot: Bot, admin_id: int, db_path: str) -> AsyncIOScheduler:
    """Scheduler ni sozlash va ishga tushirish."""
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    
    # Har kuni soat 23:59 da ishlaydi (Toshkent vaqti bilan)
    scheduler.add_job(
        send_db_backup,
        trigger="cron",
        hour=23,
        minute=59,
        kwargs={"bot": bot, "admin_id": admin_id, "db_path": db_path}
    )
    
    scheduler.start()
    return scheduler
