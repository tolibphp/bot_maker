"""Reply klaviaturalar."""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from templates.pro_kino_bot.utils.premium_emoji import (
    ID_SEARCH, ID_FIRE, ID_SPARKLE, ID_INFO, ID_CROWN, ID_CROSS
)


def get_main_menu_kb() -> ReplyKeyboardMarkup:
    """Foydalanuvchi asosiy menyu."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=" Kino qidirish",
                    icon_custom_emoji_id=ID_SEARCH,
                    style="success"
                ),
                KeyboardButton(
                    text=" Mashhur kinolar",
                    icon_custom_emoji_id=ID_FIRE,
                    style="success"
                ),
            ],
            [
                KeyboardButton(
                    text=" Yangi kinolar",
                    icon_custom_emoji_id=ID_SPARKLE,
                    style="primary"
                ),
                KeyboardButton(
                    text=" Biz haqimizda",
                    icon_custom_emoji_id=ID_INFO,
                    style="primary"
                ),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Kino kodini yuboring...",
    )


def get_admin_menu_kb() -> ReplyKeyboardMarkup:
    """Admin asosiy menyu (qo'shimcha Admin panel tugmasi)."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=" Admin panel",
                    icon_custom_emoji_id=ID_CROWN,
                    style="primary"
                ),
            ],
            [
                KeyboardButton(
                    text=" Kino qidirish",
                    icon_custom_emoji_id=ID_SEARCH,
                    style="success"
                ),
                KeyboardButton(
                    text=" Mashhur kinolar",
                    icon_custom_emoji_id=ID_FIRE,
                    style="success"
                ),
            ],
            [
                KeyboardButton(
                    text=" Yangi kinolar",
                    icon_custom_emoji_id=ID_SPARKLE,
                    style="primary"
                ),
                KeyboardButton(
                    text=" Biz haqimizda",
                    icon_custom_emoji_id=ID_INFO,
                    style="primary"
                ),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Kino kodini yuboring...",
    )


def get_cancel_kb() -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=" Bekor qilish",
                    icon_custom_emoji_id=ID_CROSS,
                    style="danger"
                )
            ],
        ],
        resize_keyboard=True,
    )


remove_kb = ReplyKeyboardRemove()
