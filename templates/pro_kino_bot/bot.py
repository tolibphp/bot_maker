"""
Kino Bot - Asosiy ishga tushirish fayli (Bot Maker Template).
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from templates.base_template import BaseTemplate
from templates.pro_kino_bot.database.db import Database
from templates.pro_kino_bot.handlers.admin import router as admin_router
from templates.pro_kino_bot.handlers.user import router as user_router
from templates.pro_kino_bot.middlewares.subscription import SubscriptionMiddleware
from templates.pro_kino_bot.utils.scheduler import setup_scheduler
from templates.pro_kino_bot.utils.context import current_admin_id

logger = logging.getLogger(__name__)


class AdminContextMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        admin_id = data.get("admin_id")
        token = current_admin_id.set(admin_id)
        try:
            return await handler(event, data)
        finally:
            current_admin_id.reset(token)


class KinoBot(BaseTemplate):
    def __init__(self, bot_token: str, admin_id: int, db_path: str, bot_id: int):
        super().__init__(bot_token, admin_id, db_path, bot_id)
        
        self.bot = Bot(
            token=self.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db = Database(self.db_path)
        
        # Inject dependencies
        self.dp["db"] = self.db
        self.dp["admin_id"] = self.admin_id
        
        # Context Middleware
        self.dp.message.outer_middleware(AdminContextMiddleware())
        self.dp.callback_query.outer_middleware(AdminContextMiddleware())
        
        # Subscription Middleware
        self.dp.message.middleware(SubscriptionMiddleware(self.db))
        self.dp.callback_query.middleware(SubscriptionMiddleware(self.db))
        
        # Routers
        self.dp.include_router(admin_router)
        self.dp.include_router(user_router)
        
        # Scheduler
        self.scheduler = setup_scheduler(self.bot, self.admin_id, self.db_path)
        self.dp['scheduler'] = self.scheduler
        # Add admin_id to scheduler since it runs outside of standard update handling
        self.scheduler.admin_id = self.admin_id 
        
        # Hook up a wrapper to pass admin_id into context for scheduler
        # We need to monkey-patch or handle context carefully if scheduler sends messages
        # But scheduler.py only sends to the admin_id directly!

    async def setup(self):
        """Setup bot (implemented in init)"""
        pass

    async def start(self):
        await self.db.connect()
        logger.info(f"ProKinoBot #{self.bot_id} started polling")
        
        # We need to manually set the context for the scheduler task if needed.
        # But scheduler just runs every day and uses current_admin_id.
        # However, APScheduler runs in a separate context!
        # So in scheduler.py, we should replace current_admin_id with bot.admin_id maybe?
        
        await self.bot.delete_webhook(drop_pending_updates=True)
        self.polling_task = asyncio.create_task(
            self.dp.start_polling(self.bot, allowed_updates=self.dp.resolve_used_update_types())
        )

    async def stop(self):
        if hasattr(self, 'polling_task'):
            self.polling_task.cancel()
        if hasattr(self, 'scheduler') and self.scheduler:
            self.scheduler.shutdown(wait=False)
        await self.db.close()
        await self.bot.session.close()
        logger.info(f"ProKinoBot #{self.bot_id} stopped")
