"""FSM holatlar - Admin va Foydalanuvchi uchun."""

from aiogram.fsm.state import State, StatesGroup


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ADMIN HOLATLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class AddMovieStates(StatesGroup):
    """Kino qo'shish bosqichlari."""

    waiting_for_code = State()
    waiting_for_title = State()
    waiting_for_file = State()
    waiting_for_caption = State()


class DeleteMovieStates(StatesGroup):
    """Kino o'chirish bosqichlari."""

    waiting_for_code = State()


class BroadcastStates(StatesGroup):
    """Xabar yuborish bosqichlari."""

    waiting_for_message = State()
    confirm = State()


class AddChannelStates(StatesGroup):
    """Kanal qo'shish bosqichlari."""

    waiting_for_channel = State()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FOYDALANUVCHI HOLATLARI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchStates(StatesGroup):
    """Kino qidirish holati."""

    waiting_for_query = State()
