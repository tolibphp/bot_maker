import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from templates.kino_bot.database import KinoDB
from templates.kino_bot.keyboards import (
    admin_main_kb, channels_manage_kb, cancel_admin_kb,
    movie_list_kb, confirm_delete_kb, channel_post_kb
)
from templates.kino_bot.states import (
    AddMovieStates, AddChannelStates,
    BroadcastStates, BanUserStates
)

logger = logging.getLogger(__name__)


def create_admin_router(kino_db: KinoDB, admin_id: int) -> Router:
    router = Router()

    def is_admin(message: Message) -> bool:
        return message.from_user.id == admin_id

    # ==========================================
    #  ➕ KINO QO'SHISH (Nom → Video → Tayyor!)
    # ==========================================

    @router.message(F.text == "➕ Kino qo'shish")
    async def add_movie_start(message: Message, state: FSMContext):
        if not is_admin(message):
            return
        await message.answer(
            "➕ <b>Kino qo'shish</b>\n\n"
            "Kino nomini kiriting:",
            reply_markup=cancel_admin_kb(),
            parse_mode="HTML"
        )
        await state.set_state(AddMovieStates.waiting_name)

    @router.message(AddMovieStates.waiting_name)
    async def add_movie_name(message: Message, state: FSMContext):
        if not is_admin(message):
            return
        await state.update_data(movie_name=message.text.strip())
        await message.answer(
            "📤 Kino faylini yuboring (video yoki dokument):",
            parse_mode="HTML"
        )
        await state.set_state(AddMovieStates.waiting_file)

    @router.message(AddMovieStates.waiting_file, F.video | F.document)
    async def add_movie_file(message: Message, state: FSMContext):
        if not is_admin(message):
            return

        if message.video:
            file_id = message.video.file_id
        elif message.document:
            file_id = message.document.file_id
        else:
            await message.answer("❌ Video yoki dokument yuboring.")
            return

        data = await state.get_data()
        caption = message.caption

        code = await kino_db.add_movie(
            name=data["movie_name"],
            category_id=None,
            file_id=file_id,
            caption=caption
        )

        await message.answer(
            f"✅ <b>Kino qo'shildi!</b>\n\n"
            f"🎬 Nomi: <b>{data['movie_name']}</b>\n"
            f"📌 Kodi: <code>#{code}</code>",
            reply_markup=admin_main_kb(),
            parse_mode="HTML"
        )

        # --- Kanalga avto-post ---
        channels = await kino_db.get_channels()
        if channels:
            bot_me = await message.bot.get_me()
            post_caption = (
                f"🎬 <b>{data['movie_name']}</b>\n\n"
                f"📌 Kod: <code>#{code}</code>\n\n"
                f"▶️ Botda ko'rish uchun tugmani bosing 👇"
            )
            post_kb = channel_post_kb(bot_me.username)

            for ch in channels:
                try:
                    if message.video:
                        await message.bot.send_video(
                            chat_id=ch["channel_id"],
                            video=file_id,
                            caption=post_caption,
                            reply_markup=post_kb,
                            parse_mode="HTML"
                        )
                    else:
                        await message.bot.send_document(
                            chat_id=ch["channel_id"],
                            document=file_id,
                            caption=post_caption,
                            reply_markup=post_kb,
                            parse_mode="HTML"
                        )
                except Exception as e:
                    await message.answer(
                        f"⚠️ Kanalga post qilib bo'lmadi: {e}",
                        parse_mode="HTML"
                    )

        await state.clear()

    @router.message(AddMovieStates.waiting_file)
    async def add_movie_file_invalid(message: Message):
        await message.answer("❌ Iltimos, video yoki dokument faylini yuboring.")

    # ==========================================
    #  📋 KINOLAR RO'YXATI (sahifali + o'chirish)
    # ==========================================

    @router.message(F.text == "📋 Kinolar ro'yxati")
    async def movies_list(message: Message):
        if not is_admin(message):
            return

        total = await kino_db.get_movies_count()
        if total == 0:
            await message.answer("📋 Hali kino qo'shilmagan.")
            return

        per_page = 8
        total_pages = (total + per_page - 1) // per_page
        movies = await kino_db.get_all_movies(page=0, per_page=per_page)

        text = f"📋 <b>Kinolar ro'yxati</b> ({total} ta)\n\n"
        text += "O'chirish uchun 🗑 bosing:\n"

        await message.answer(
            text,
            reply_markup=movie_list_kb(movies, 0, total_pages),
            parse_mode="HTML"
        )

    @router.callback_query(F.data.startswith("mpage:"))
    async def movies_page(callback: CallbackQuery):
        page = int(callback.data.split(":")[1])
        per_page = 8
        total = await kino_db.get_movies_count()
        total_pages = (total + per_page - 1) // per_page
        movies = await kino_db.get_all_movies(page=page, per_page=per_page)

        text = f"📋 <b>Kinolar ro'yxati</b> ({total} ta)\n\n"
        text += "O'chirish uchun 🗑 bosing:\n"

        await callback.message.edit_text(
            text,
            reply_markup=movie_list_kb(movies, page, total_pages),
            parse_mode="HTML"
        )

    @router.callback_query(F.data.startswith("delmovie:"))
    async def delete_movie_inline(callback: CallbackQuery):
        code = callback.data.split(":")[1]
        movie = await kino_db.get_movie_by_code(code)
        if not movie:
            await callback.answer("Kino topilmadi!", show_alert=True)
            return

        await callback.message.edit_text(
            f"🗑 <b>{movie['name']}</b> (#{movie['code']}) ni o'chirmoqchimisiz?",
            reply_markup=confirm_delete_kb(code),
            parse_mode="HTML"
        )

    @router.callback_query(F.data.startswith("confirm_del:"))
    async def confirm_delete_movie(callback: CallbackQuery):
        code = callback.data.split(":")[1]
        movie = await kino_db.get_movie_by_code(code)
        if movie:
            await kino_db.delete_movie(code)
            await callback.message.edit_text(
                f"✅ <b>{movie['name']}</b> (#{movie['code']}) o'chirildi.",
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text("❌ Kino topilmadi.")

    @router.callback_query(F.data == "cancel_del")
    async def cancel_delete(callback: CallbackQuery):
        await callback.message.delete()

    # ==========================================
    #  📢 KANAL SOZLASH
    #  (Majburiy obuna + Kanalimiz tugmasi + Avto-post)
    # ==========================================

    @router.message(F.text == "📢 Kanal sozlash")
    async def manage_channels(message: Message):
        if not is_admin(message):
            return
        channels = await kino_db.get_channels()

        text = (
            "📢 <b>Kanal sozlash</b>\n\n"
            "Shu yerda qo'shgan kanalingiz:\n"
            "✅ Majburiy obuna tekshiriladi\n"
            "📢 «Kanalimiz» tugmasida ko'rsatiladi\n"
            "📤 Yangi kino avtomatik post qilinadi\n\n"
        )
        if channels:
            text += "<b>Qo'shilgan kanallar:</b>\n"
            for ch in channels:
                text += f"📢 {ch['channel_name'] or ch['channel_id']}\n"
            text += "\nO'chirish uchun bosing 👇"
        else:
            text += "⚠️ Hali kanal qo'shilmagan.\nQo'shish uchun tugmani bosing 👇"

        await message.answer(
            text,
            reply_markup=channels_manage_kb(channels),
            parse_mode="HTML"
        )

    @router.callback_query(F.data == "add_channel")
    async def add_channel_start(callback: CallbackQuery, state: FSMContext):
        await callback.message.edit_text(
            "📢 Kanal username ni kiriting\n"
            "Misol: <code>@mychannel</code>\n\n"
            "⚠️ <b>Muhim:</b> Bot kanalda admin bo'lishi kerak!\n"
            "(Kanalga botni admin qilib qo'shing)",
            parse_mode="HTML"
        )
        await state.set_state(AddChannelStates.waiting_channel)

    @router.message(AddChannelStates.waiting_channel)
    async def add_channel_name(message: Message, state: FSMContext):
        if not is_admin(message):
            return
        channel_id = message.text.strip()

        # Try to get channel info
        try:
            chat = await message.bot.get_chat(channel_id)
            channel_name = chat.title
        except Exception:
            channel_name = channel_id

        await kino_db.add_channel(channel_id, channel_name)
        await message.answer(
            f"✅ Kanal <b>{channel_name}</b> qo'shildi!\n\n"
            f"Endi bu kanal:\n"
            f"✅ Majburiy obuna uchun tekshiriladi\n"
            f"📢 «Kanalimiz» tugmasida ko'rsatiladi\n"
            f"📤 Yangi kinolar avtomatik post qilinadi",
            reply_markup=admin_main_kb(),
            parse_mode="HTML"
        )
        await state.clear()

    @router.callback_query(F.data.startswith("delch:"))
    async def delete_channel(callback: CallbackQuery):
        ch_id = int(callback.data.split(":")[1])
        await kino_db.delete_channel(ch_id)

        # Refresh list
        channels = await kino_db.get_channels()
        if channels:
            text = "✅ Kanal o'chirildi.\n\n<b>Qolgan kanallar:</b>\n"
            for ch in channels:
                text += f"📢 {ch['channel_name'] or ch['channel_id']}\n"
        else:
            text = "✅ Kanal o'chirildi.\n\n⚠️ Kanallar yo'q."

        await callback.message.edit_text(
            text,
            reply_markup=channels_manage_kb(channels),
            parse_mode="HTML"
        )

    # ==========================================
    #  📢 BROADCAST
    # ==========================================

    @router.message(F.text == "📢 Broadcast")
    async def broadcast_start(message: Message, state: FSMContext):
        if not is_admin(message):
            return
        users_count = await kino_db.get_users_count()
        await message.answer(
            f"📢 <b>Broadcast</b>\n\n"
            f"Jami foydalanuvchilar: {users_count}\n"
            f"Xabarni yuboring (matn, rasm, video...):",
            reply_markup=cancel_admin_kb(),
            parse_mode="HTML"
        )
        await state.set_state(BroadcastStates.waiting_message)

    @router.message(BroadcastStates.waiting_message)
    async def broadcast_send(message: Message, state: FSMContext):
        if not is_admin(message):
            return

        users = await kino_db.get_all_users()
        sent = 0
        failed = 0

        for user in users:
            try:
                await message.copy_to(user["telegram_id"])
                sent += 1
            except Exception:
                failed += 1

        await message.answer(
            f"📢 <b>Broadcast yakunlandi!</b>\n\n"
            f"✅ Yuborildi: {sent}\n"
            f"❌ Xatolik: {failed}",
            reply_markup=admin_main_kb(),
            parse_mode="HTML"
        )
        await state.clear()

    # ==========================================
    #  📊 STATISTIKA
    # ==========================================

    @router.message(F.text == "📊 Statistika")
    async def show_stats(message: Message):
        if not is_admin(message):
            return

        users_count = await kino_db.get_users_count()
        today_users = await kino_db.get_today_users_count()
        movies_count = await kino_db.get_movies_count()
        channels = await kino_db.get_channels()

        await message.answer(
            f"📊 <b>Bot Statistikasi</b>\n\n"
            f"👥 Jami foydalanuvchilar: <b>{users_count}</b>\n"
            f"🆕 Bugungi yangi: <b>{today_users}</b>\n"
            f"🎬 Jami kinolar: <b>{movies_count}</b>\n"
            f"📢 Kanallar: <b>{len(channels)}</b>",
            reply_markup=admin_main_kb(),
            parse_mode="HTML"
        )

    # ==========================================
    #  🚫 BAN / UNBAN
    # ==========================================

    @router.message(F.text == "🚫 Ban / Unban")
    async def ban_start(message: Message, state: FSMContext):
        if not is_admin(message):
            return
        await message.answer(
            "🚫 <b>Ban / Unban</b>\n\n"
            "Foydalanuvchi Telegram ID sini kiriting:\n"
            "(Ban qilish yoki bandan chiqarish)",
            reply_markup=cancel_admin_kb(),
            parse_mode="HTML"
        )
        await state.set_state(BanUserStates.waiting_user_id)

    @router.message(BanUserStates.waiting_user_id)
    async def ban_user_id(message: Message, state: FSMContext):
        if not is_admin(message):
            return

        try:
            user_id = int(message.text.strip())
        except ValueError:
            await message.answer("❌ Noto'g'ri ID.")
            return

        user = await kino_db.get_user(user_id)
        if not user:
            await message.answer(
                "❌ Bu foydalanuvchi botdan foydalanmagan.",
                reply_markup=admin_main_kb()
            )
            await state.clear()
            return

        if user["is_banned"]:
            await kino_db.unban_user(user_id)
            await message.answer(
                f"✅ <b>{user['full_name']}</b> bandan chiqarildi.",
                reply_markup=admin_main_kb(),
                parse_mode="HTML"
            )
        else:
            await kino_db.ban_user(user_id)
            await message.answer(
                f"🚫 <b>{user['full_name']}</b> bloklandi.",
                reply_markup=admin_main_kb(),
                parse_mode="HTML"
            )
        await state.clear()

    # ==========================================
    #  ❌ BEKOR QILISH
    # ==========================================

    @router.callback_query(F.data == "cancel_admin")
    async def cancel_admin(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Bekor qilindi.")
        await callback.message.answer(
            "👑 Admin Panel",
            reply_markup=admin_main_kb(),
            parse_mode="HTML"
        )

    @router.callback_query(F.data == "noop")
    async def noop(callback: CallbackQuery):
        await callback.answer()

    return router
