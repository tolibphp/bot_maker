"""Inline klaviaturalar - Foydalanuvchi va Admin uchun."""

from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from templates.pro_kino_bot.utils.premium_emoji import (
    ID_FORWARD, ID_CHECK, ID_SEARCH, ID_FIRE, ID_SPARKLE, 
    ID_CLAPPER, ID_BACK, ID_HOME, ID_ADD, ID_DELETE, 
    ID_FOLDER, ID_CHART, ID_MEGAPHONE, ID_CHANNEL, ID_CROSS, ID_SEND
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOYDALANUVCHI KLAVIATURALARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def get_subscription_kb(
    channels: list,
) -> InlineKeyboardMarkup:
    """Majburiy obuna kanallar klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for row in channels:
        ch = dict(row) if hasattr(row, "keys") else row
        username = ch.get("channel_username")
        title = ch.get("channel_title") or username or "Kanal"
        invite_link = ch.get("invite_link")
        
        # Agar invite_link bo'lsa, o'shani ishlatamiz.
        # Agar yo'q bo'lsa username orqali public link yasaymiz.
        url = invite_link if invite_link else f"https://t.me/{username.lstrip('@')}" if username else ""
        
        if url:
            builder.row(
                InlineKeyboardButton(
                    text=f" {title}",
                    url=url,
                    icon_custom_emoji_id=ID_FORWARD,
                    style="primary"
                )
            )
    builder.row(
        InlineKeyboardButton(
            text=" Tekshirish",
            callback_data="check_subscription",
            icon_custom_emoji_id=ID_CHECK,
            style="success"
        )
    )
    return builder.as_markup()


def get_main_inline_kb() -> InlineKeyboardMarkup:
    """Asosiy inline menyu."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=" Kino qidirish",
            callback_data="search_movie",
            icon_custom_emoji_id=ID_SEARCH,
            style="primary"
        ),
        InlineKeyboardButton(
            text=" Mashhurlar",
            callback_data="popular_movies",
            icon_custom_emoji_id=ID_FIRE,
            style="primary"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=" Yangi kinolar",
            callback_data="recent_movies",
            icon_custom_emoji_id=ID_SPARKLE,
            style="primary"
        ),
    )
    return builder.as_markup()


def get_movie_kb(code: str) -> InlineKeyboardMarkup:
    """Kino ko'rish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=" Qidirish",
            callback_data="search_movie",
            icon_custom_emoji_id=ID_SEARCH,
            style="primary"
        ),
        InlineKeyboardButton(
            text=" Mashhurlar",
            callback_data="popular_movies",
            icon_custom_emoji_id=ID_FIRE,
            style="primary"
        ),
    )
    return builder.as_markup()


def get_search_results_kb(
    movies: list, page: int = 0, per_page: int = 5
) -> InlineKeyboardMarkup:
    """Qidiruv natijalari klaviaturasi sahifalash bilan."""
    builder = InlineKeyboardBuilder()
    start = page * per_page
    end = start + per_page
    page_movies = movies[start:end]

    for movie in page_movies:
        builder.row(
            InlineKeyboardButton(
                text=f" {movie['title']} | {movie['code']}",
                callback_data=f"get_movie:{movie['code']}",
                icon_custom_emoji_id=ID_CLAPPER,
                style="primary"
            )
        )

    nav_buttons: list[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text=" Oldingi",
                callback_data=f"search_page:{page - 1}",
                icon_custom_emoji_id=ID_BACK,
                style="primary"
            )
        )
    if end < len(movies):
        nav_buttons.append(
            InlineKeyboardButton(
                text=" Keyingi",
                callback_data=f"search_page:{page + 1}",
                icon_custom_emoji_id=ID_FORWARD,
                style="primary"
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(
            text=" Bosh menyu",
            callback_data="main_menu",
            icon_custom_emoji_id=ID_HOME,
            style="primary"
        )
    )
    return builder.as_markup()


def get_popular_movies_kb(movies: list) -> InlineKeyboardMarkup:
    """Mashhur kinolar ro'yxati."""
    builder = InlineKeyboardBuilder()
    for i, movie in enumerate(movies, 1):
        views = movie["views"]
        builder.row(
            InlineKeyboardButton(
                text=f" {i}. {movie['title']}  —  {views} ko'rish",
                callback_data=f"get_movie:{movie['code']}",
                icon_custom_emoji_id=ID_CLAPPER,
                style="primary"
            )
        )
    builder.row(
        InlineKeyboardButton(
            text=" Bosh menyu",
            callback_data="main_menu",
            icon_custom_emoji_id=ID_HOME,
            style="primary"
        )
    )
    return builder.as_markup()


def get_recent_movies_kb(movies: list) -> InlineKeyboardMarkup:
    """Yangi qo'shilgan kinolar."""
    builder = InlineKeyboardBuilder()
    for movie in movies:
        builder.row(
            InlineKeyboardButton(
                text=f" {movie['title']} | {movie['code']}",
                callback_data=f"get_movie:{movie['code']}",
                icon_custom_emoji_id=ID_CLAPPER,
                style="primary"
            )
        )
    builder.row(
        InlineKeyboardButton(
            text=" Bosh menyu",
            callback_data="main_menu",
            icon_custom_emoji_id=ID_HOME,
            style="primary"
        )
    )
    return builder.as_markup()


def get_back_kb() -> InlineKeyboardMarkup:
    """Orqaga tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" Orqaga",
                    callback_data="main_menu",
                    icon_custom_emoji_id=ID_BACK,
                    style="danger"
                )
            ]
        ]
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN KLAVIATURALARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def get_admin_panel_kb() -> InlineKeyboardMarkup:
    """Admin boshqaruv paneli."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=" Kino qo'shish",
            callback_data="admin:add_movie",
            icon_custom_emoji_id=ID_ADD,
            style="success"
        ),
        InlineKeyboardButton(
            text=" Kino o'chirish",
            callback_data="admin:delete_movie",
            icon_custom_emoji_id=ID_DELETE,
            style="danger"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=" Kinolar ro'yxati",
            callback_data="admin:movie_list",
            icon_custom_emoji_id=ID_FOLDER,
            style="primary"
        ),
        InlineKeyboardButton(
            text=" Statistika",
            callback_data="admin:statistics",
            icon_custom_emoji_id=ID_CHART,
            style="primary"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=" Xabar yuborish",
            callback_data="admin:broadcast",
            icon_custom_emoji_id=ID_MEGAPHONE,
            style="primary"
        ),
        InlineKeyboardButton(
            text=" Kanallar",
            callback_data="admin:channels",
            icon_custom_emoji_id=ID_CHANNEL,
            style="primary"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=" Backup",
            callback_data="admin:backup",
            icon_custom_emoji_id=ID_FOLDER,
            style="primary"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" Bosh menyu",
            callback_data="main_menu",
            icon_custom_emoji_id=ID_HOME,
            style="primary"
        )
    )
    return builder.as_markup()


def get_admin_confirm_kb(action: str) -> InlineKeyboardMarkup:
    """Tasdiqlash / Bekor qilish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" Tasdiqlash",
                    callback_data=f"confirm:{action}",
                    icon_custom_emoji_id=ID_CHECK,
                    style="success"
                ),
                InlineKeyboardButton(
                    text=" Bekor qilish",
                    callback_data="admin:cancel",
                    icon_custom_emoji_id=ID_CROSS,
                    style="danger"
                ),
            ]
        ]
    )


def get_skip_caption_kb() -> InlineKeyboardMarkup:
    """Caption o'tkazib yuborish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" O'tkazib yuborish",
                    callback_data="skip_caption",
                    icon_custom_emoji_id=ID_FORWARD,
                    style="primary"
                )
            ],
            [
                InlineKeyboardButton(
                    text=" Bekor qilish",
                    callback_data="admin:cancel",
                    icon_custom_emoji_id=ID_CROSS,
                    style="danger"
                )
            ],
        ]
    )


def get_admin_back_kb() -> InlineKeyboardMarkup:
    """Admin panelga qaytish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" Admin panel",
                    callback_data="admin:panel",
                    icon_custom_emoji_id=ID_BACK,
                    style="primary"
                ),
                InlineKeyboardButton(
                    text=" Bekor qilish",
                    callback_data="admin:cancel",
                    icon_custom_emoji_id=ID_CROSS,
                    style="danger"
                ),
            ]
        ]
    )


def get_channel_management_kb(channels: list) -> InlineKeyboardMarkup:
    """Kanallarni boshqarish."""
    builder = InlineKeyboardBuilder()
    for ch in channels:
        username = ch["channel_username"] or str(ch["channel_id"])
        title = ch["channel_title"] or username
        builder.row(
            InlineKeyboardButton(
                text=f" {title}",
                callback_data=f"remove_channel:{ch['channel_id']}",
                icon_custom_emoji_id=ID_DELETE,
                style="danger"
            )
        )
    builder.row(
        InlineKeyboardButton(
            text=" Kanal qo'shish",
            callback_data="admin:add_channel",
            icon_custom_emoji_id=ID_ADD,
            style="success"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=" Admin panel",
            callback_data="admin:panel",
            icon_custom_emoji_id=ID_BACK,
            style="primary"
        )
    )
    return builder.as_markup()


def get_movie_list_kb(
    movies: list, page: int = 0, per_page: int = 8
) -> InlineKeyboardMarkup:
    """Admin kinolar ro'yxati sahifalash bilan."""
    builder = InlineKeyboardBuilder()
    start = page * per_page
    end = start + per_page
    page_movies = movies[start:end]

    for movie in page_movies:
        views = movie["views"]
        builder.row(
            InlineKeyboardButton(
                text=f"[{movie['code']}] {movie['title']}  ({views})",
                callback_data=f"admin:view_movie:{movie['code']}",
                icon_custom_emoji_id=ID_CLAPPER,
                style="primary"
            )
        )

    nav_buttons: list[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text=" Oldingi",
                callback_data=f"admin:movie_page:{page - 1}",
                icon_custom_emoji_id=ID_BACK,
                style="primary"
            )
        )
    if end < len(movies):
        nav_buttons.append(
            InlineKeyboardButton(
                text=" Keyingi",
                callback_data=f"admin:movie_page:{page + 1}",
                icon_custom_emoji_id=ID_FORWARD,
                style="primary"
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        InlineKeyboardButton(
            text=" Admin panel",
            callback_data="admin:panel",
            icon_custom_emoji_id=ID_BACK,
            style="primary"
        )
    )
    return builder.as_markup()


def get_admin_movie_detail_kb(code: str) -> InlineKeyboardMarkup:
    """Admin kino tafsilotlari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" O'chirish",
                    callback_data=f"admin:confirm_delete:{code}",
                    icon_custom_emoji_id=ID_DELETE,
                    style="danger"
                )
            ],
            [
                InlineKeyboardButton(
                    text=" Ro'yxatga qaytish",
                    callback_data="admin:movie_list",
                    icon_custom_emoji_id=ID_BACK,
                    style="primary"
                )
            ],
        ]
    )





def get_confirm_delete_kb(code: str) -> InlineKeyboardMarkup:
    """O'chirishni tasdiqlash."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=" Ha, o'chirish",
                    callback_data=f"admin:do_delete:{code}",
                    icon_custom_emoji_id=ID_CHECK,
                    style="danger"
                ),
                InlineKeyboardButton(
                    text=" Yo'q, bekor qilish",
                    callback_data="admin:movie_list",
                    icon_custom_emoji_id=ID_CROSS,
                    style="primary"
                ),
            ]
        ]
    )
