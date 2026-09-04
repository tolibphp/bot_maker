"""
Telegram Premium Emoji konstantalar va yordamchi funksiyalar.

USE_PREMIUM_EMOJI = True  → <tg-emoji> teglar ishlatiladi (default).
USE_PREMIUM_EMOJI = False → oddiy Unicode fallback ishlatiladi.
"""

import os

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PREMIUM EMOJI REJIMI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USE_PREMIUM_EMOJI: bool = os.getenv("USE_PREMIUM_EMOJI", "true").lower() == "true"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PREMIUM EMOJI GENERATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _pe(emoji_id: str, fallback: str = "") -> str:
    """Premium emoji yoki fallback qaytarish."""
    if USE_PREMIUM_EMOJI:
        return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
    return fallback


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  RAW EMOJI IDs (FOR BUTTONS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID_MOVIE = "5375464961822695044"
ID_POPCORN = "5469903029144657419"
ID_FIRE = "5375464961822695044"
ID_TROPHY = "5438485047021705795"
ID_STAR = "5433653135799228968"
ID_SPARKLE = "5409008750893734809"
ID_CLAPPER = "5375464961822695044"
ID_SEARCH = "5435957248314579621"
ID_HOME = "5472164874886846699"
ID_BACK = "5256247952564825322"
ID_FORWARD = "5255835489675519149"
ID_ADD = "5465226866321268133"
ID_DELETE = "5888558080173545731"
ID_DOWNLOAD = "5433653135799228968"
ID_CHECK = "6323133642960799652"
ID_CROSS = "5888558080173545731"
ID_WARNING = "5438303606128285373"
ID_INFO = "5438303606128285373"
ID_LOCK = "5433811242135331842"
ID_GEAR = "5296369303661067030"
ID_CHART = "5438574962162043987"
ID_USER = "5440603840288165037"
ID_USERS = "5440603840288165037"
ID_SEND = "6323395189289256377"
ID_CHANNEL = "6323395189289256377"
ID_MEGAPHONE = "5438618057863893203"
ID_CROWN = "5296369303661067030"
ID_FOLDER = "5258096772776991776"
ID_NUMBER = "5438326064512275784"
ID_CLOCK = "5373012449597335010"
ID_KEY = "5373012449597335010"
ID_WAVE = "5372926953978341366"
ID_GLOBE = "5372926953978341366"
ID_PIN = "5433614747381538714"
ID_SHIELD = "5433614747381538714"
ID_DIAMOND = "5780405967527089720"
ID_ROBOT = "5780405967527089720"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HTML PE_* CONSTANTS (FOR MESSAGES)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PE_MOVIE = _pe(ID_MOVIE, "\U0001f3ac")
PE_POPCORN = _pe(ID_POPCORN, "\U0001f37f")
PE_FIRE = _pe(ID_FIRE, "\U0001f525")
PE_TROPHY = _pe(ID_TROPHY, "\U0001f3c6")
PE_STAR = _pe(ID_STAR, "\u2b50")
PE_SPARKLE = _pe(ID_SPARKLE, "\u2728")
PE_CLAPPER = _pe(ID_CLAPPER, "\U0001f3ac")
PE_SEARCH = _pe(ID_SEARCH, "\U0001f50d")
PE_HOME = _pe(ID_HOME, "\U0001f3e0")
PE_BACK = _pe(ID_BACK, "\u25c0\ufe0f")
PE_FORWARD = _pe(ID_FORWARD, "\u25b6\ufe0f")
PE_ADD = _pe(ID_ADD, "\u2795")
PE_DELETE = _pe(ID_DELETE, "\U0001f5d1\ufe0f")
PE_DOWNLOAD = _pe(ID_DOWNLOAD, "\U0001f4e5")
PE_CHECK = _pe(ID_CHECK, "\u2705")
PE_CROSS = _pe(ID_CROSS, "\u274c")
PE_WARNING = _pe(ID_WARNING, "\u26a0\ufe0f")
PE_INFO = _pe(ID_INFO, "\u2139\ufe0f")
PE_LOCK = _pe(ID_LOCK, "\U0001f512")
PE_GEAR = _pe(ID_GEAR, "\u2699\ufe0f")
PE_CHART = _pe(ID_CHART, "\U0001f4ca")
PE_USER = _pe(ID_USER, "\U0001f464")
PE_USERS = _pe(ID_USERS, "\U0001f465")
PE_SEND = _pe(ID_SEND, "\U0001f4e4")
PE_CHANNEL = _pe(ID_CHANNEL, "\U0001f4e2")
PE_MEGAPHONE = _pe(ID_MEGAPHONE, "\U0001f4e3")
PE_CROWN = _pe(ID_CROWN, "\U0001f451")
PE_FOLDER = _pe(ID_FOLDER, "\U0001f4c1")
PE_NUMBER = _pe(ID_NUMBER, "#\ufe0f\u20e3")
PE_CLOCK = _pe(ID_CLOCK, "\U0001f550")
PE_KEY = _pe(ID_KEY, "\U0001f511")
PE_WAVE = _pe(ID_WAVE, "\U0001f44b")
PE_GLOBE = _pe(ID_GLOBE, "\U0001f310")
PE_PIN = _pe(ID_PIN, "\U0001f4cc")
PE_SHIELD = _pe(ID_SHIELD, "\U0001f6e1\ufe0f")
PE_DIAMOND = _pe(ID_DIAMOND, "\U0001f48e")
PE_ROBOT = _pe(ID_ROBOT, "\U0001f916")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  YORDAMCHI FUNKSIYALAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def is_admin(user_id: int, admin_ids: list[int]) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish."""
    return user_id in admin_ids


def format_movie_caption(
    title: str, code: str, caption: str | None = None
) -> str:
    """Kino uchun chiroyli caption yaratish."""
    text = (
        f"{PE_CLAPPER} <b>{title}</b>\n"
        f"{'━' * 22}\n\n"
        f"{PE_NUMBER} <b>Kod:</b> <code>{code}</code>\n"
    )
    if caption:
        text += f"\n{PE_PIN} {caption}\n"

    text += (
        f"\n{'━' * 22}\n"
        f"{PE_POPCORN} <i>Yoqimli tomosha tilaymiz!</i>"
    )
    return text


def format_number(num: int) -> str:
    """Raqamni ming ajratgich bilan formatlash."""
    return f"{num:,}".replace(",", " ")
