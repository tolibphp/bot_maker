"""Foydalanuvchi handlerlari."""

from __future__ import annotations

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ChatJoinRequest

from templates.pro_kino_bot.utils.context import current_admin_id
from templates.pro_kino_bot.database.db import Database
from templates.pro_kino_bot.keyboards.inline_kb import (
    get_back_kb,
    get_main_inline_kb,
    get_movie_kb,
    get_popular_movies_kb,
    get_recent_movies_kb,
    get_search_results_kb,
    get_subscription_kb,
)
from templates.pro_kino_bot.keyboards.reply_kb import get_admin_menu_kb, get_cancel_kb, get_main_menu_kb
from templates.pro_kino_bot.states.states import SearchStates
from templates.pro_kino_bot.utils.premium_emoji import (
    PE_CHECK,
    PE_CLAPPER,
    PE_CROSS,
    PE_DIAMOND,
    PE_FIRE,
    PE_GLOBE,
    PE_HOME,
    PE_INFO,
    PE_MOVIE,
    PE_POPCORN,
    PE_ROBOT,
    PE_SEARCH,
    PE_SHIELD,
    PE_SPARKLE,
    PE_STAR,
    PE_TROPHY,
    PE_USER,
    PE_WAVE,
    format_movie_caption,
    format_number,
)

router = Router(name="user")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  /start BUYRUG'I
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database, state: FSMContext) -> None:
    await state.clear()
    user = message.from_user
    await db.add_user(user.id, user.full_name, user.username)

    # Deep-link orqali kino kodi bilan kelsa
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        code = args[1].strip()
        movie = await db.get_movie_by_code(code)
        if movie:
            await _send_movie(message, movie, db)
            return

    text = (
        f"{PE_WAVE} <b>Assalomu alaykum, {user.first_name}!</b>\n"
        f"{'━' * 26}\n\n"
        f"{PE_ROBOT} <b>Kino Bot</b>ga xush kelibsiz!\n\n"
        f"{PE_CLAPPER} Bu bot orqali siz minglab kinolarni\n"
        f"topishingiz va ko'rishingiz mumkin.\n\n"
        f"{PE_SPARKLE} <b>Qanday foydalanish:</b>\n\n"
        f"  {PE_SEARCH} Kino kodini yuboring\n"
        f"  {PE_STAR} Nomi bo'yicha qidiring\n"
        f"  {PE_FIRE} Mashhur kinolarni ko'ring\n\n"
        f"{'━' * 26}\n"
        f"{PE_POPCORN} <i>Yoqimli tomosha!</i>"
    )

    kb = get_admin_menu_kb() if user.id in ADMIN_IDS else get_main_menu_kb()
    await message.answer(text, reply_markup=kb, parse_mode="HTML")
    await message.answer(
        f"{PE_HOME} <b>Bosh menyu</b>",
        reply_markup=get_main_inline_kb(),
        parse_mode="HTML",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  KINO KODI BO'YICHA QIDIRISH (raqam xabar)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


from aiogram.filters import StateFilter

@router.message(F.text.regexp(r"^\d+$"), StateFilter(None))
async def handle_movie_code(message: Message, db: Database) -> None:

    code = message.text.strip()
    movie = await db.get_movie_by_code(code)

    if movie:
        await _send_movie(message, movie, db)
    else:
        text = (
            f"{PE_CROSS} <b>Kino topilmadi</b>\n\n"
            f"{PE_INFO} <code>{code}</code> kodli kino bazada mavjud emas.\n"
            f"{PE_SEARCH} Boshqa kod bilan urinib ko'ring."
        )
        await message.answer(
            text, reply_markup=get_back_kb(), parse_mode="HTML"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  REPLY TUGMALAR HANDLERI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.message(F.text.endswith("Kino qidirish"))
async def reply_search(message: Message, state: FSMContext) -> None:
    await state.set_state(SearchStates.waiting_for_query)
    text = (
        f"{PE_SEARCH} <b>Kino qidirish</b>\n"
        f"{'━' * 24}\n\n"
        f"{PE_INFO} Kino nomini yoki kodini yuboring.\n"
        f"{PE_SPARKLE} Masalan: <code>Matrix</code>"
    )
    await message.answer(
        text, reply_markup=get_cancel_kb(), parse_mode="HTML"
    )


@router.message(F.text.endswith("Mashhur kinolar"))
async def reply_popular(
    message: Message, db: Database, state: FSMContext
) -> None:
    await state.clear()
    movies = await db.get_popular_movies(10)
    if not movies:
        text = (
            f"{PE_INFO} <b>Hozircha kinolar mavjud emas</b>\n\n"
            f"{PE_MOVIE} Tez orada yangi kinolar qo'shiladi!"
        )
        await message.answer(
            text, reply_markup=get_back_kb(), parse_mode="HTML"
        )
        return

    text = (
        f"{PE_TROPHY} <b>Eng mashhur kinolar</b>\n"
        f"{'━' * 26}\n\n"
        f"{PE_FIRE} Eng ko'p ko'rilgan TOP-{len(movies)} kinolar:"
    )
    await message.answer(
        text,
        reply_markup=get_popular_movies_kb(movies),
        parse_mode="HTML",
    )


@router.message(F.text.endswith("Yangi kinolar"))
async def reply_recent(
    message: Message, db: Database, state: FSMContext
) -> None:
    await state.clear()
    movies = await db.get_recent_movies(10)
    if not movies:
        text = (
            f"{PE_INFO} <b>Hozircha kinolar mavjud emas</b>\n\n"
            f"{PE_MOVIE} Tez orada yangi kinolar qo'shiladi!"
        )
        await message.answer(
            text, reply_markup=get_back_kb(), parse_mode="HTML"
        )
        return

    text = (
        f"{PE_STAR} <b>Yangi qo'shilgan kinolar</b>\n"
        f"{'━' * 26}\n\n"
        f"{PE_SPARKLE} So'nggi {len(movies)} ta kino:"
    )
    await message.answer(
        text,
        reply_markup=get_recent_movies_kb(movies),
        parse_mode="HTML",
    )


@router.message(F.text.endswith("Biz haqimizda"))
async def reply_about(message: Message, state: FSMContext) -> None:
    await state.clear()
    text = (
        f"{PE_DIAMOND} <b>Kino Bot haqida</b>\n"
        f"{'➖' * 26}\n\n"
        f"{PE_ROBOT} Bu bot orqali siz turli janrdagi\n"
        f"kinolarni topishingiz mumkin.\n\n"
        f"{PE_CLAPPER} <b>Imkoniyatlar:</b>\n\n"
        f"  {PE_SEARCH} Kod bo'yicha tez qidirish\n"
        f"  {PE_STAR} Nom bo'yicha qidirish\n"
        f"  {PE_FIRE} Mashhur kinolar ro'yxati\n"
        f"  {PE_SPARKLE} Yangi kinolar\n\n"
        f"{'➖' * 26}\n"
        f"{PE_SHIELD} <b>Barcha huquqlar himoyalangan.</b>"
    )
    await message.answer(
        text, reply_markup=get_back_kb(), parse_mode="HTML"
    )

@router.chat_join_request()
async def handle_join_request(join_request: ChatJoinRequest, bot: Bot, db: Database) -> None:
    """Maxfiy kanalga zayavka tashlaganlarni bazaga saqlaydi va qabul qilmay turib ruxsat beradi."""
    try:
        await db.add_join_request(join_request.from_user.id, join_request.chat.id)
        await bot.send_message(
            chat_id=join_request.from_user.id,
            text=f"✅ <b>{join_request.chat.title}</b> kanaliga so'rovingiz yuborildi!\nEndi botdan bemalol foydalanishingiz mumkin.",
            parse_mode="HTML"
        )
    except Exception as e:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  QIDIRISH FSM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@router.message(F.text.contains("Bekor qilish"))
async def cancel_search(message: Message, state: FSMContext) -> None:
    await state.clear()
    kb = (
        get_admin_menu_kb()
        if message.from_user.id in ADMIN_IDS
        else get_main_menu_kb()
    )
    text = f"{PE_CHECK} <b>Bekor qilindi</b>"
    await message.answer(text, reply_markup=kb, parse_mode="HTML")
    await message.answer(
        f"{PE_HOME} <b>Bosh menyu</b>",
        reply_markup=get_main_inline_kb(),
        parse_mode="HTML",
    )


@router.message(SearchStates.waiting_for_query)
async def process_search_query(
    message: Message, db: Database, state: FSMContext
) -> None:
    query = message.text.strip()
    if len(query) < 2:
        text = (
            f"{PE_CROSS} <b>Juda qisqa so'rov</b>\n\n"
            f"{PE_INFO} Kamida 2 ta belgi yuboring."
        )
        await message.answer(text, parse_mode="HTML")
        return

    movies = await db.search_movies(query)
    await state.clear()

    kb = (
        get_admin_menu_kb()
        if message.from_user.id in ADMIN_IDS
        else get_main_menu_kb()
    )
    await message.answer(
        f"{PE_SEARCH} Qidirish natijalari...", reply_markup=kb, parse_mode="HTML"
    )

    if not movies:
        text = (
            f"{PE_CROSS} <b>Natija topilmadi</b>\n\n"
            f"{PE_INFO} \"<code>{query}</code>\" bo'yicha "
            f"hech qanday kino topilmadi.\n\n"
            f"{PE_SPARKLE} Boshqa so'z bilan qidirib ko'ring."
        )
        await message.answer(
            text, reply_markup=get_back_kb(), parse_mode="HTML"
        )
        return

    # Qidiruv natijalarini state'ga saqlash (sahifalash uchun)
    await state.update_data(
        search_results=[
            {"code": m["code"], "title": m["title"], "views": m["views"]}
            for m in movies
        ]
    )

    text = (
        f"{PE_CHECK} <b>{format_number(len(movies))} ta natija topildi</b>\n"
        f"{'━' * 24}\n\n"
        f"{PE_SEARCH} \"<code>{query}</code>\" bo'yicha:"
    )
    await message.answer(
        text,
        reply_markup=get_search_results_kb(movies),
        parse_mode="HTML",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CALLBACK QUERY HANDLERLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


async def _safe_edit(callback: CallbackQuery, text: str, reply_markup) -> None:
    if callback.message.text:
        await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    else:
        await callback.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = f"{PE_HOME} <b>Bosh menyu</b>"
    await _safe_edit(callback, text, get_main_inline_kb())
    await callback.answer()


@router.callback_query(F.data == "search_movie")
async def cb_search(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SearchStates.waiting_for_query)
    text = (
        f"{PE_SEARCH} <b>Kino qidirish</b>\n"
        f"{'━' * 24}\n\n"
        f"{PE_INFO} Kino nomini yoki kodini yuboring."
    )
    await _safe_edit(callback, text, get_back_kb())
    await callback.answer()


@router.callback_query(F.data == "popular_movies")
async def cb_popular(
    callback: CallbackQuery, db: Database, state: FSMContext
) -> None:
    await state.clear()
    movies = await db.get_popular_movies(10)
    if not movies:
        text = (
            f"{PE_INFO} <b>Hozircha kinolar mavjud emas</b>\n\n"
            f"{PE_MOVIE} Tez orada yangi kinolar qo'shiladi!"
        )
        await _safe_edit(callback, text, get_back_kb())
        await callback.answer()
        return

    text = (
        f"{PE_TROPHY} <b>Eng mashhur kinolar</b>\n"
        f"{'━' * 26}\n\n"
        f"{PE_FIRE} TOP-{len(movies)} kinolar:"
    )
    await _safe_edit(callback, text, get_popular_movies_kb(movies))
    await callback.answer()


@router.callback_query(F.data == "recent_movies")
async def cb_recent(
    callback: CallbackQuery, db: Database, state: FSMContext
) -> None:
    await state.clear()
    movies = await db.get_recent_movies(10)
    if not movies:
        text = (
            f"{PE_INFO} <b>Hozircha kinolar mavjud emas</b>\n\n"
            f"{PE_MOVIE} Tez orada yangi kinolar qo'shiladi!"
        )
        await _safe_edit(callback, text, get_back_kb())
        await callback.answer()
        return

    text = (
        f"{PE_STAR} <b>Yangi qo'shilgan kinolar</b>\n"
        f"{'━' * 26}\n\n"
        f"{PE_SPARKLE} So'nggi {len(movies)} ta kino:"
    )
    await _safe_edit(callback, text, get_recent_movies_kb(movies))
    await callback.answer()


@router.callback_query(F.data.startswith("get_movie:"))
async def cb_get_movie(
    callback: CallbackQuery, db: Database
) -> None:
    code = callback.data.split(":", 1)[1]
    movie = await db.get_movie_by_code(code)
    if not movie:
        text = f"{PE_CROSS} <b>Kino topilmadi</b>"
        await _safe_edit(callback, text, get_back_kb())
        await callback.answer()
        return

    await callback.answer()
    await _send_movie_from_callback(callback, movie, db)


@router.callback_query(F.data.startswith("search_page:"))
async def cb_search_page(
    callback: CallbackQuery, state: FSMContext
) -> None:
    page = int(callback.data.split(":", 1)[1])
    data = await state.get_data()
    movies = data.get("search_results", [])

    if not movies:
        await callback.answer("Natijalar topilmadi")
        return

    text = (
        f"{PE_SEARCH} <b>Qidiruv natijalari</b>\n"
        f"{'━' * 24}\n\n"
        f"{PE_INFO} Sahifa: {page + 1}"
    )
    await _safe_edit(callback, text, get_search_results_kb(movies, page))
    await callback.answer()


@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(
    callback: CallbackQuery, db: Database, bot: Bot, state: FSMContext
) -> None:
    user = callback.from_user
    channels = await db.get_channels()

    not_subscribed: list[dict] = []
    for row in channels:
        ch = dict(row) if hasattr(row, "keys") else row
        try:
            member = await bot.get_chat_member(
                chat_id=ch["channel_id"], user_id=user.id
            )
            if member.status in ("left", "kicked"):
                has_req = await db.has_join_request(user.id, ch["channel_id"])
                if not has_req:
                    not_subscribed.append(ch)
        except Exception:
            has_req = await db.has_join_request(user.id, ch["channel_id"])
            if not has_req:
                not_subscribed.append(ch)

    if not_subscribed:
        await callback.answer(
            "Hali barcha kanallarga obuna bo'lmagansiz yoki zayavka tashlamagansiz!", show_alert=True
        )
        return

    await callback.answer("Tekshirish muvaffaqiyatli!", show_alert=False)
    
    # Delete the subscription message
    try:
        await callback.message.delete()
    except Exception:
        pass
        
    # Welcome the user
    text = (
        f"✅ <b>Barcha kanallarga a'zo bo'ldingiz (yoki zayavka qabul qilindi)!</b>\n\n"
        f"Endi botdan bemalol foydalanishingiz mumkin.\n"
        f"Kino kodini yuboring yoki quyidagi tugmalardan foydalaning."
    )
    from keyboards.reply_kb import get_main_kb
    await callback.message.answer(text, parse_mode="HTML", reply_markup=get_main_kb())

    text = (
        f"{PE_CHECK} <b>Obuna tasdiqlandi!</b>\n\n"
        f"{PE_WAVE} Xush kelibsiz, {user.first_name}!\n"
        f"{PE_POPCORN} Endi kino kodini yuboring."
    )
    kb = get_admin_menu_kb() if user.id in ADMIN_IDS else get_main_menu_kb()
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await callback.message.answer(
        f"{PE_HOME} <b>Bosh menyu</b>",
        reply_markup=get_main_inline_kb(),
        parse_mode="HTML",
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  YORDAMCHI FUNKSIYALAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


async def _send_movie(
    message: Message, movie, db: Database
) -> None:
    """Kinoni foydalanuvchiga yuborish."""
    await db.increment_views(movie["code"])
    caption = format_movie_caption(
        movie["title"], movie["code"], movie["caption"]
    )

    file_type = movie["file_type"]
    file_id = movie["file_id"]

    try:
        if file_type == "video":
            await message.answer_video(
                video=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
        elif file_type == "document":
            await message.answer_document(
                document=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
        elif file_type == "animation":
            await message.answer_animation(
                animation=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
        else:
            await message.answer_document(
                document=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
    except Exception:
        text = (
            f"{PE_CROSS} <b>Xatolik yuz berdi</b>\n\n"
            f"{PE_INFO} Kino faylini yuborishda muammo chiqdi.\n"
            f"Iltimos, keyinroq urinib ko'ring."
        )
        await message.answer(text, parse_mode="HTML")


async def _send_movie_from_callback(
    callback: CallbackQuery, movie, db: Database
) -> None:
    """Callback orqali kinoni yuborish."""
    await db.increment_views(movie["code"])
    caption = format_movie_caption(
        movie["title"], movie["code"], movie["caption"]
    )

    file_type = movie["file_type"]
    file_id = movie["file_id"]

    try:
        if file_type == "video":
            await callback.message.answer_video(
                video=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
        elif file_type == "document":
            await callback.message.answer_document(
                document=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
        elif file_type == "animation":
            await callback.message.answer_animation(
                animation=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
        else:
            await callback.message.answer_document(
                document=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_movie_kb(movie["code"]),
            )
    except Exception:
        text = (
            f"{PE_CROSS} <b>Xatolik yuz berdi</b>\n\n"
            f"{PE_INFO} Kino faylini yuborishda muammo chiqdi."
        )
        await callback.message.answer(text, parse_mode="HTML")
