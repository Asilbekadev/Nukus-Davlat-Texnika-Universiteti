"""
🎓 NDTU Test Bot — To'liq versiya
python-telegram-bot 22.x bilan yozilgan

Fanlar:
  • Web dasturlash         → questions.json
  • Ma'lumotlar bazasi    → questions.json
  • Dasturlash asoslari   → questions.json
  • Kompyuter tarmoqlari  → network_part1.json / network_part2.json
  • O'rnatilgan tizimlar  → embedded_systems.json
"""

import json
import logging
import random
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ──────────────────────────────────────────────
# ⚙️  Sozlamalar
# ──────────────────────────────────────────────
BOT_TOKEN = "8544526802:AAECKF6ox7x9rjfP-Nd69gU0oPa5vN8u_ZA"       # ← bu yerga o'z tokeningizni kiriting
PASSING_SCORE = 56                       # % da o'tish balli
DB_PATH = Path("users.db")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# 📁  Fayl xaritasi
# ──────────────────────────────────────────────
SUBJECT_FILES: dict[str, str | None] = {
    "web":           "questions.json",
    "db":            "questions.json",
    "programming":   "questions.json",
    "network_part1": "network_part1.json",
    "network_part2": "network_part2.json",
    "embedded":      "embedded_systems.json",
    "os":            "operatsion_tizim.json",
}

SUBJECT_NAMES: dict[str, str] = {
    "web":           "🌐 Web dasturlash",
    "db":            "💾 Ma'lumotlar bazasi",
    "programming":   "💻 Dasturlash asoslari",
    "network_part1": "🌐 Kompyuter tarmoqlari — 1-bo'lim",
    "network_part2": "🌐 Kompyuter tarmoqlari — 2-bo'lim",
    "embedded":      "🔧 O'rnatilgan tizimlar",
    "os":            "🖥️ Operatsion tizimlar",
}


# ──────────────────────────────────────────────
# 🗄️  Database
# ──────────────────────────────────────────────
class Database:
    def __init__(self, path: Path = DB_PATH) -> None:
        self.path = str(path)
        self._init()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init(self) -> None:
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id       INTEGER PRIMARY KEY,
                    first_name        TEXT,
                    last_name         TEXT,
                    username          TEXT,
                    phone_number      TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS test_results (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id     INTEGER,
                    subject         TEXT,
                    correct_answers INTEGER,
                    total_questions INTEGER,
                    score           REAL,
                    passed          BOOLEAN,
                    test_date       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
                );
            """)

    def get_user(self, telegram_id: int):
        with self._conn() as conn:
            return conn.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()

    def save_user(
        self,
        telegram_id: int,
        first_name: str,
        last_name: str,
        username: str,
        phone: str | None = None,
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO users
                   (telegram_id, first_name, last_name, username, phone_number)
                   VALUES (?, ?, ?, ?, ?)""",
                (telegram_id, first_name, last_name, username, phone),
            )

    def save_result(
        self,
        telegram_id: int,
        subject: str,
        correct: int,
        total: int,
        score: float,
        passed: bool,
    ) -> None:
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO test_results
                   (telegram_id, subject, correct_answers, total_questions, score, passed)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (telegram_id, subject, correct, total, score, passed),
            )


# ──────────────────────────────────────────────
# 🎯  Test sessiyasi
# ──────────────────────────────────────────────
@dataclass
class TestSession:
    subject: str
    current_index: int = 0
    correct: int = 0
    answered: int = 0
    used: list[int] = field(default_factory=list)

    @property
    def wrong(self) -> int:
        return self.answered - self.correct

    @property
    def progress(self) -> float:
        return (self.correct / self.answered * 100) if self.answered else 0.0


# ──────────────────────────────────────────────
# 🌐  Globallar
# ──────────────────────────────────────────────
db = Database()
sessions: dict[int, TestSession] = {}


# ──────────────────────────────────────────────
# 📋  Klaviatura yordamchilari
# ──────────────────────────────────────────────
def kb_phone() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def kb_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Web dasturlash",        callback_data="sub_web")],
        [InlineKeyboardButton("💾 Ma'lumotlar bazasi",   callback_data="sub_db")],
        [InlineKeyboardButton("💻 Dasturlash asoslari",  callback_data="sub_programming")],
        [InlineKeyboardButton("🌐 Kompyuter tarmoqlari", callback_data="sub_network")],
        [InlineKeyboardButton("🔧 O'rnatilgan tizimlar", callback_data="sub_embedded")],
        [InlineKeyboardButton("🖥️ Operatsion tizimlar",  callback_data="sub_os")],
    ])


def kb_back() -> list[list[InlineKeyboardButton]]:
    return [[InlineKeyboardButton("◀️ Orqaga", callback_data="back")]]


# ──────────────────────────────────────────────
# 📂  Savollarni yuklash
# ──────────────────────────────────────────────
def load_questions(subject: str) -> list[dict]:
    filepath = SUBJECT_FILES.get(subject)
    if not filepath:
        return []

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(filepath)

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # questions.json ichida sub-key bo'ladi (web, db, programming)
    if isinstance(data, dict):
        return data.get(subject, [])
    return data   # network_part1.json, embedded_systems.json — to'g'ridan-to'g'ri ro'yxat


# ──────────────────────────────────────────────
# 🏠  /start
# ──────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Avval databasedan qidirish — mavjud bo'lsa, yangilamasdan ishlatamiz
    record = db.get_user(user.id)

    if not record:
        # Yangi foydalanuvchi — faqat asosiy ma'lumotlarni saqlaymiz, telefon yo'q
        db.save_user(user.id, user.first_name, user.last_name or "", user.username or "")
        await update.message.reply_text(
            "👋 *Xush kelibsiz!*\n\n"
            "🎓 *NDTU Test Botiga kirish uchun*\n"
            "📱 Telefon raqamingizni yuboring\n\n"
            "⬇️ Pastdagi tugmani bosing",
            reply_markup=kb_phone(),
            parse_mode="Markdown",
        )
        return

    phone_saved = record[4]  # phone_number ustuni

    if not phone_saved:
        # Bazada bor, lekin telefon raqami yo'q — qayta so'raymiz
        await update.message.reply_text(
            "📱 *Telefon raqamingiz hali saqlanmagan*\n\n"
            "Botdan to'liq foydalanish uchun\n"
            "telefon raqamingizni yuboring:\n\n"
            "⬇️ Pastdagi tugmani bosing",
            reply_markup=kb_phone(),
            parse_mode="Markdown",
        )
    else:
        # Ro'yxatdan o'tgan foydalanuvchi — to'g'ridan-to'g'ri menyuga
        await update.message.reply_text(
            f"👋 *Xush kelibsiz, {user.first_name}!*\n\n"
            "🎓 *NDTU Test Tizimi*\n\n"
            "📚 *Fanlardan birini tanlang:*",
            reply_markup=kb_main(),
            parse_mode="Markdown",
        )


# ──────────────────────────────────────────────
# 📞  Kontakt qabul qilish
# ──────────────────────────────────────────────
async def on_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contact = update.message.contact
    user = update.effective_user

    if not contact or contact.user_id != user.id:
        await update.message.reply_text("❌ Iltimos, o'z telefon raqamingizni yuboring!")
        return

    db.save_user(user.id, user.first_name, user.last_name or "", user.username or "", contact.phone_number)

    await update.message.reply_text(
        "✅ *Telefon raqamingiz saqlandi!*\n\n"
        "🎉 *Endi botdan to'liq foydalanishingiz mumkin*",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        "📚 *Fanlardan birini tanlang:*",
        reply_markup=kb_main(),
        parse_mode="Markdown",
    )


# ──────────────────────────────────────────────
# 📚  Fan tanlash
# ──────────────────────────────────────────────
async def on_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    key = query.data[4:]  # "sub_web" → "web"

    if key == "network":
        await query.edit_message_text(
            "🌐 *Kompyuter tarmoqlari*\n\n"
            "📚 *Bo'limni tanlang:*\n\n"
            "📘 *1-bo'lim* — 200 ta savol\n"
            "📗 *2-bo'lim* — tez orada\n\n"
            "🎯 *Qaysi bo'limdan boshlaysiz?*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📘 1-bo'lim (200 ta savol)", callback_data="test_network_part1")],
                [InlineKeyboardButton("📗 2-bo'lim (tez orada)",   callback_data="test_network_part2")],
                *kb_back(),
            ]),
            parse_mode="Markdown",
        )
        return

    subject_key = key  # web / db / programming / embedded / os
    name = SUBJECT_NAMES.get(subject_key, key)

    extra = ""
    if key == "embedded":
        extra = "• 100 ta savol\n"
    elif key == "os":
        extra = "• 154 ta savol\n"

    await query.edit_message_text(
        f"{name}\n\n"
        "📊 *Test ma'lumotlari:*\n"
        f"{extra}"
        "• Random tartibda savollar\n"
        "• Har savoldan keyin natija\n"
        f"• Minimum {PASSING_SCORE}% o'tish balli\n"
        "• Istalgan vaqt yakunlash mumkin\n\n"
        "🎯 *Tayyor bo'lsangiz, boshlang!*",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Testni boshlash", callback_data=f"test_{subject_key}")],
            *kb_back(),
        ]),
        parse_mode="Markdown",
    )


# ──────────────────────────────────────────────
# 🚀  Test boshlash
# ──────────────────────────────────────────────
async def on_start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    subject = query.data[5:]   # "test_web" → "web"
    user_id = query.from_user.id

    sessions[user_id] = TestSession(subject=subject)
    logger.info("Test boshlandi: user=%s, subject=%s", user_id, subject)
    await _send_question(query, user_id)


# ──────────────────────────────────────────────
# ❓  Savol yuborish
# ──────────────────────────────────────────────
async def _send_question(query, user_id: int) -> None:
    session = sessions.get(user_id)
    if not session:
        return

    try:
        all_q = load_questions(session.subject)
    except FileNotFoundError as fname:
        messages = {
            "network_part2.json": "📗 *2-bo'lim* hali tayyorlanmagan. Tez orada qo'shiladi!",
        }
        msg = messages.get(
            str(fname),
            f"❌ `{fname}` fayli topilmadi!\nIltimos, faylni bot papkasiga joylashtiring.",
        )
        await query.edit_message_text(msg, parse_mode="Markdown")
        return
    except Exception as exc:
        await query.edit_message_text(f"❌ Xatolik: {exc}")
        return

    available = [(i, q) for i, q in enumerate(all_q) if i not in session.used]

    if not available:
        await _finish_test(query, user_id)
        return

    idx, question = random.choice(available)
    session.used.append(idx)
    session.current_index = idx

    buttons = [
        [InlineKeyboardButton(f"{chr(65 + i)}. {ans['text']}", callback_data=f"ans_{i}")]
        for i, ans in enumerate(question["answers"])
    ]
    buttons.append([InlineKeyboardButton("⛔ Testni yakunlash", callback_data="finish")])

    await query.edit_message_text(
        f"📊 *Savol {session.answered + 1}*\n\n"
        f"📈 Joriy natija: {session.progress:.1f}%\n"
        f"✅ To'g'ri: {session.correct}  |  ❌ Noto'g'ri: {session.wrong}\n\n"
        f"❓ *{question['question']}*",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )


# ──────────────────────────────────────────────
# ✅  Javob tekshirish
# ──────────────────────────────────────────────
async def on_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = sessions.get(user_id)
    if not session:
        await query.edit_message_text("⚠️ Sessiya topilmadi. /start bosing.")
        return

    ans_idx = int(query.data[4:])   # "ans_2" → 2

    try:
        question = load_questions(session.subject)[session.current_index]
    except Exception as exc:
        await query.edit_message_text(f"❌ Xatolik: {exc}")
        return

    is_correct = question["answers"][ans_idx]["correct"]
    session.answered += 1

    if is_correct:
        session.correct += 1
        verdict = "✅ *To'g'ri javob!*"
        emoji = "🎉"
    else:
        right = next(a["text"] for a in question["answers"] if a["correct"])
        verdict = f"❌ *Noto'g'ri javob!*\n\n✔️ *To'g'ri javob:* {right}"
        emoji = "😞"

    await query.edit_message_text(
        f"{emoji} {verdict}\n\n"
        "📊 *Natija:*\n"
        f"✅ To'g'ri:   {session.correct}\n"
        f"❌ Noto'g'ri: {session.wrong}\n"
        f"📈 Ball:       {session.progress:.1f}%\n"
        f"📝 Jami:       {session.answered} ta savol",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➡️ Keyingi savol", callback_data="next")],
        ]),
        parse_mode="Markdown",
    )


# ──────────────────────────────────────────────
# 🏁  Test yakunlash
# ──────────────────────────────────────────────
async def _finish_test(query, user_id: int) -> None:
    session = sessions.pop(user_id, None)
    if not session:
        return

    passed = session.progress >= PASSING_SCORE
    db.save_result(
        user_id, session.subject,
        session.correct, session.answered,
        session.progress, passed,
    )

    header = "✅ *Tabriklaymiz! Imtihondan o'tdingiz!*" if passed else "❌ *Afsuski, imtihondan o'ta olmadingiz*"
    emoji  = "🎉🎊🏆" if passed else "😞📚"
    name   = SUBJECT_NAMES.get(session.subject, session.subject)

    retry_cb = f"test_{session.subject}"

    await query.edit_message_text(
        f"{emoji}\n\n"
        f"{header}\n\n"
        f"📚 *Fan:* {name}\n\n"
        "📊 *Yakuniy natija:*\n"
        f"✅ To'g'ri javoblar:    {session.correct}\n"
        f"❌ Noto'g'ri javoblar: {session.wrong}\n"
        f"📝 Jami savollar:       {session.answered}\n"
        f"📈 Ball:                {session.progress:.1f}%\n\n"
        f"⚠️ O'tish balli: {PASSING_SCORE}%",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Qayta urinish", callback_data=retry_cb)],
            [InlineKeyboardButton("◀️ Bosh menyu",    callback_data="back")],
        ]),
        parse_mode="Markdown",
    )


# ──────────────────────────────────────────────
# 🎛️  Markaziy callback handler
# ──────────────────────────────────────────────
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data  = query.data

    if data.startswith("sub_"):
        await on_subject(update, context)

    elif data.startswith("test_"):
        await on_start_test(update, context)

    elif data.startswith("ans_"):
        await on_answer(update, context)

    elif data == "next":
        await query.answer()
        await _send_question(query, query.from_user.id)

    elif data == "finish":
        await query.answer()
        await _finish_test(query, query.from_user.id)

    elif data == "back":
        await query.answer()
        await query.edit_message_text(
            "🎓 *NDTU Test Tizimi*\n\n📚 *Fanlardan birini tanlang:*",
            reply_markup=kb_main(),
            parse_mode="Markdown",
        )

    else:
        await query.answer("❓ Noma'lum buyruq", show_alert=True)


# ──────────────────────────────────────────────
# 🚀  Ishga tushirish
# ──────────────────────────────────────────────
def main() -> None:
    banner = [
        "=" * 58,
        "  🎓 NDTU Test Bot — python-telegram-bot 22.x",
        "=" * 58,
        "  📚 Fanlar:",
        "     • Web dasturlash         → questions.json",
        "     • Ma'lumotlar bazasi    → questions.json",
        "     • Dasturlash asoslari   → questions.json",
        "     • Tarmoqlar 1-bo'lim    → network_part1.json",
        "     • Tarmoqlar 2-bo'lim    → network_part2.json",
        "     • O'rnatilgan tizimlar  → embedded_systems.json",
        "     • Operatsion tizimlar   → operatsion_tizim.json",
        f"  ✅ O'tish balli: {PASSING_SCORE}%",
        "=" * 58,
    ]
    print("\n".join(banner))

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.CONTACT, on_contact))
    app.add_handler(CallbackQueryHandler(on_callback))

    logger.info("Bot polling rejimida ishga tushdi ✅")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()