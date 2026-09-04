"""Majburiy kanal obuna tekshirish middleware."""

from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, TelegramObject

from templates.pro_kino_bot.utils.context import current_admin_id
from templates.pro_kino_bot.database.db import Database
from templates.pro_kino_bot.keyboards.inline_kb import get_subscription_kb
from templates.pro_kino_bot.utils.premium_emoji import (
    PE_CHANNEL,
    PE_CROSS,
    PE_INFO,
    PE_LOCK,
    PE_WARNING,
)


class SubscriptionMiddleware(BaseMiddleware):
    """Foydalanuvchi majburiy kanallarga obuna bo'lganini tekshiradi."""

    def __init__(self, db: Database) -> None:
        self.db = db
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            # "check_subscription" callback'ini blokirovka qilmaslik
            if event.data == "check_subscription":
                return await handler(event, data)
            user = event.from_user

        if user is None:
            return await handler(event, data)

        # Adminlarni o'tkazib yuborish
        if user.id in ADMIN_IDS:
            return await handler(event, data)

        # Kanallarni tekshirish
        channels = await self.db.get_channels()
        if not channels:
            return await handler(event, data)

        bot: Bot = data["bot"]
        not_subscribed: list[dict] = []

        for row in channels:
            ch = dict(row) if hasattr(row, "keys") else row
            try:
                member = await bot.get_chat_member(
                    chat_id=ch["channel_id"], user_id=user.id
                )
                if member.status in ("left", "kicked"):
                    # Zayavka tashlaganligini tekshiramiz
                    has_req = await self.db.has_join_request(user.id, ch["channel_id"])
                    if not has_req:
                        not_subscribed.append(
                            {
                                "channel_id": ch["channel_id"],
                                "channel_username": ch.get("channel_username"),
                                "channel_title": ch.get("channel_title"),
                                "invite_link": ch.get("invite_link"),
                            }
                        )
            except Exception:
                # Agar user topilmasa yoki xatolik bersa, demak obuna emas!
                # Lekin zayavka tashlagan bo'lsa o'tkazib yuboramiz
                has_req = await self.db.has_join_request(user.id, ch["channel_id"])
                if not has_req:
                    not_subscribed.append(
                        {
                            "channel_id": ch["channel_id"],
                            "channel_username": ch.get("channel_username"),
                            "channel_title": ch.get("channel_title"),
                            "invite_link": ch.get("invite_link"),
                        }
                    )

        if not_subscribed:
            text = (
                f"{PE_LOCK} <b>Obuna talab qilinadi</b>\n"
                f"{'━' * 24}\n\n"
                f"{PE_INFO} Botdan foydalanish uchun quyidagi "
                f"kanallarga obuna bo'ling:\n\n"
            )
            for ch_info in not_subscribed:
                name = ch_info["channel_title"] or ch_info["channel_username"]
                text += f"  {PE_CHANNEL} {name}\n"

            text += (
                f"\n{'━' * 24}\n"
                f"{PE_WARNING} Obuna bo'lgach, "
                f"<b>Tekshirish</b> tugmasini bosing."
            )

            kb = get_subscription_kb(not_subscribed)

            if isinstance(event, Message):
                await event.answer(text, reply_markup=kb, parse_mode="HTML")
            elif isinstance(event, CallbackQuery):
                await event.message.edit_text(
                    text, reply_markup=kb, parse_mode="HTML"
                )
                await event.answer()
            return None

        return await handler(event, data)
