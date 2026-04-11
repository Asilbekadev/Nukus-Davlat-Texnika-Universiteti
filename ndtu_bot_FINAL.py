"""
🎓 NDTU Test Bot - To'liq versiya
✅ Fanlar: Web, DB, Dasturlash, Kompyuter Tarmoqlari (2 bo'lim), O'rnatilgan Tizimlar
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import json
import random
import sqlite3

# 🔧 Konfiguratsiya
BOT_TOKEN = "8544526802:AAECKF6ox7x9rjfP-Nd69gU0oPa5vN8u_ZA"

# 📊 Database
class Database:
    def __init__(self):
        self.init_database()

    def get_connection(self):
        return sqlite3.connect('users.db')

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                phone_number TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                subject TEXT,
                correct_answers INTEGER,
                total_questions INTEGER,
                score REAL,
                passed BOOLEAN,
                test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
            )
        ''')

        conn.commit()
        conn.close()

    def get_user(self, telegram_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def save_user(self, user_id, first_name, last_name, username, phone=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (telegram_id, first_name, last_name, username, phone_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, first_name, last_name, username, phone))
        conn.commit()
        conn.close()

    def save_test_result(self, telegram_id, subject, correct, total, score, passed):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO test_results (telegram_id, subject, correct_answers, total_questions, score, passed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (telegram_id, subject, correct, total, score, passed))
        conn.commit()
        conn.close()

# 🎯 Test sessiya
class TestSession:
    def __init__(self, subject):
        self.subject = subject
        self.current_question = 0
        self.correct_answers = 0
        self.total_answered = 0
        self.used_questions = []

    def get_progress(self):
        return (self.correct_answers / self.total_answered * 100) if self.total_answered > 0 else 0

# 🌐 Global
db = Database()
user_sessions = {}

# 📱 Telefon so'rash
def get_phone_keyboard():
    button = KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)
    return ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)

# 📚 Fanlar menyusi
def get_subjects_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Web dasturlash", callback_data="subject_web")],
        [InlineKeyboardButton("💾 Ma'lumotlar bazasi", callback_data="subject_db")],
        [InlineKeyboardButton("💻 Dasturlash asoslari", callback_data="subject_programming")],
        [InlineKeyboardButton("🌐 Kompyuter tarmoqlari", callback_data="subject_network")],
        [InlineKeyboardButton("🔧 O'rnatilgan tizimlar", callback_data="subject_embedded")],
    ])

# 🏠 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data = db.get_user(user.id)

    db.save_user(user.id, user.first_name, user.last_name or '', user.username or '')

    if not user_data or not user_data[4]:
        text = (
            "👋 *Xush kelibsiz!*\n\n"
            "🎓 *NDTU Test Botiga kirish uchun*\n"
            "📱 Telefon raqamingizni yuboring\n\n"
            "⬇️ Pastdagi tugmani bosing"
        )
        await update.message.reply_text(text, reply_markup=get_phone_keyboard(), parse_mode='Markdown')
    else:
        text = (
            f"👋 *Xush kelibsiz, {user.first_name}!*\n\n"
            "🎓 *NDTU Test Tizimi*\n\n"
            "📚 *Fanlardan birini tanlang:*"
        )
        await update.message.reply_text(text, reply_markup=get_subjects_keyboard(), parse_mode='Markdown')

# 📞 Kontakt qabul qilish
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.effective_user

    if not contact or contact.user_id != user.id:
        await update.message.reply_text("❌ Iltimos, o'z telefon raqamingizni yuboring!")
        return

    db.save_user(user.id, user.first_name, user.last_name or '', user.username or '', contact.phone_number)

    text = (
        "✅ *Telefon raqamingiz saqlandi!*\n\n"
        "🎉 *Endi botdan to'liq foydalanishingiz mumkin*\n\n"
        "📚 *Fanlardan birini tanlang:*"
    )

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    await update.message.reply_text("⬇️", reply_markup=get_subjects_keyboard())

# 📚 Fan tanlash
async def subject_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subjects = {
        "subject_web": "🌐 Web dasturlash",
        "subject_db": "💾 Ma'lumotlar bazasi",
        "subject_programming": "💻 Dasturlash asoslari",
        "subject_network": "🌐 Kompyuter tarmoqlari",
        "subject_embedded": "🔧 O'rnatilgan tizimlar",
    }

    subject_name = subjects.get(query.data, "Fan")

    # ⭐ Kompyuter tarmoqlari uchun 2 bo'lim
    if query.data == "subject_network":
        keyboard = [
            [InlineKeyboardButton("📘 1-bo'lim (200 ta savol)", callback_data="network_part1")],
            [InlineKeyboardButton("📗 2-bo'lim (tez orada)", callback_data="network_part2")],
            [InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_subjects")]
        ]

        text = (
            "🌐 *Kompyuter tarmoqlari*\n\n"
            "📚 *Bo'limlarni tanlang:*\n\n"
            "📘 *1-bo'lim*\n"
            "   • 200 ta savol\n"
            "   • Barcha mavzular\n"
            "   • Random tartib\n\n"
            "📗 *2-bo'lim*\n"
            "   • Tez orada qo'shiladi\n\n"
            "🎯 *Qaysi bo'limdan boshlaysiz?*"
        )

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    # ⭐ O'rnatilgan tizimlar uchun to'g'ridan test
    if query.data == "subject_embedded":
        keyboard = [
            [InlineKeyboardButton("📝 Testni boshlash (100 ta savol)", callback_data="start_test_embedded")],
            [InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_subjects")]
        ]

        text = (
            "🔧 *O'rnatilgan tizimlar*\n\n"
            "📊 *Test ma'lumotlari:*\n"
            "• 100 ta savol\n"
            "• Random tartibda savollar\n"
            "• Har savoldan keyin natija\n"
            "• Minimum 56% o'tish balli\n"
            "• Istalgan vaqt yakunlash\n\n"
            "🎯 *Tayyor bo'lsangiz, boshlang!*"
        )

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    # Boshqa fanlar uchun oddiy test
    keyboard = [
        [InlineKeyboardButton("📝 Testni boshlash", callback_data=f"start_test_{query.data.split('_')[1]}")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_subjects")]
    ]

    text = (
        f"{subject_name}\n\n"
        "📊 *Test ma'lumotlari:*\n"
        "• Random tartibda savollar\n"
        "• Har savoldan keyin natija\n"
        "• Minimum 56% o'tish balli\n"
        "• Istalgan vaqt yakunlash\n\n"
        "🎯 *Tayyor bo'lsangiz, boshlang!*"
    )

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# 🚀 Test boshlash
async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    callback_data = query.data

    # Subject aniqlash
    if callback_data in ['network_part1', 'network_part2']:
        subject = callback_data
    elif callback_data.startswith("start_test_"):
        subject = callback_data[len("start_test_"):]
    else:
        subject = callback_data

    print(f"🎯 Test boshlandi: User={user_id}, Subject={subject}")

    session = TestSession(subject)
    user_sessions[user_id] = session

    await send_question(query, user_id)

# 📂 Savollarni yuklash (markazlashtirilgan)
def load_questions(subject):
    if subject == 'network_part1':
        with open('network_part1.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    elif subject == 'network_part2':
        with open('network_part2.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    elif subject == 'embedded':
        with open('embedded_systems.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        with open('questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(subject, [])

# ❓ Savol yuborish
async def send_question(query, user_id):
    session = user_sessions.get(user_id)
    if not session:
        return

    try:
        all_questions = load_questions(session.subject)
        print(f"✅ {len(all_questions)} ta savol yuklandi ({session.subject})")
    except FileNotFoundError as e:
        error_msg = "❌ Fayl topilmadi!\n\n"
        if session.subject == 'network_part1':
            error_msg += "📂 `network_part1.json` fayli yo'q!\nIltimos, botning yonida faylni yarating."
        elif session.subject == 'network_part2':
            error_msg += "📂 `network_part2.json` hali yaratilmagan.\nTez orada qo'shiladi!"
        elif session.subject == 'embedded':
            error_msg += "📂 `embedded_systems.json` fayli yo'q!\nIltimos, faylni yuklab qo'ying."
        else:
            error_msg += "📂 `questions.json` fayli topilmadi!"
        await query.edit_message_text(error_msg, parse_mode='Markdown')
        return
    except Exception as e:
        await query.edit_message_text(f"❌ Xatolik yuz berdi: {str(e)}")
        return

    if not all_questions:
        await query.edit_message_text("❌ Savollar bo'sh!")
        return

    available = [q for i, q in enumerate(all_questions) if i not in session.used_questions]

    if not available:
        await finish_test(query, user_id)
        return

    question = random.choice(available)
    session.used_questions.append(all_questions.index(question))
    session.current_question = all_questions.index(question)

    keyboard = [[InlineKeyboardButton(f"{chr(65+i)}. {a['text']}", callback_data=f"answer_{i}")]
                for i, a in enumerate(question['answers'])]
    keyboard.append([InlineKeyboardButton("❌ Testni yakunlash", callback_data="finish_test")])

    progress = session.get_progress()
    text = (
        f"📊 *Savol {session.total_answered + 1}*\n\n"
        f"📈 Joriy natija: {progress:.1f}%\n"
        f"✅ To'g'ri: {session.correct_answers} | "
        f"❌ Noto'g'ri: {session.total_answered - session.correct_answers}\n\n"
        f"❓ *{question['question']}*"
    )

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# ✅ Javob tekshirish
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    session = user_sessions.get(user_id)
    if not session:
        return

    answer_index = int(query.data.split('_')[1])

    try:
        all_questions = load_questions(session.subject)
        question = all_questions[session.current_question]
    except Exception as e:
        await query.edit_message_text(f"❌ Xatolik: {str(e)}")
        return

    is_correct = question['answers'][answer_index]['correct']
    session.total_answered += 1

    if is_correct:
        session.correct_answers += 1
        result_text = "✅ *To'g'ri javob!*"
        emoji = "🎉"
    else:
        correct_answer = next(a['text'] for a in question['answers'] if a['correct'])
        result_text = f"❌ *Noto'g'ri javob!*\n\n✔️ *To'g'ri javob:* {correct_answer}"
        emoji = "😞"

    progress = session.get_progress()
    text = (
        f"{emoji} {result_text}\n\n"
        f"📊 *Natija:*\n"
        f"✅ To'g'ri: {session.correct_answers}\n"
        f"❌ Noto'g'ri: {session.total_answered - session.correct_answers}\n"
        f"📈 Ball: {progress:.1f}%\n"
        f"📝 Jami: {session.total_answered} ta savol"
    )

    keyboard = [[InlineKeyboardButton("➡️ Keyingi savol", callback_data="next_question")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# 🏁 Test yakunlash
async def finish_test(query, user_id):
    session = user_sessions.get(user_id)
    if not session:
        return

    progress = session.get_progress()
    passed = progress >= 56

    db.save_test_result(user_id, session.subject, session.correct_answers,
                        session.total_answered, progress, passed)

    status = "✅ *Tabriklaymiz! Imtihondan o'tdingiz!*" if passed else "❌ *Afsuski, imtihondan o'ta olmadingiz*"
    emoji = "🎉🎊🏆" if passed else "😞📚"

    # Qayta urinish callback
    if session.subject in ['network_part1', 'network_part2']:
        retry_callback = session.subject
    else:
        retry_callback = f"start_test_{session.subject}"

    keyboard = [
        [InlineKeyboardButton("🔄 Qayta urinish", callback_data=retry_callback)],
        [InlineKeyboardButton("◀️ Bosh menyu", callback_data="back_to_subjects")]
    ]

    # Fan nomi
    subject_names = {
        "web": "Web dasturlash",
        "db": "Ma'lumotlar bazasi",
        "programming": "Dasturlash asoslari",
        "network_part1": "Kompyuter tarmoqlari - 1-bo'lim",
        "network_part2": "Kompyuter tarmoqlari - 2-bo'lim",
        "embedded": "O'rnatilgan tizimlar",
    }
    subject_display = subject_names.get(session.subject, session.subject)

    text = (
        f"{emoji}\n\n"
        f"{status}\n\n"
        f"📚 *Fan:* {subject_display}\n\n"
        f"📊 *Yakuniy natija:*\n"
        f"✅ To'g'ri javoblar: {session.correct_answers}\n"
        f"❌ Noto'g'ri javoblar: {session.total_answered - session.correct_answers}\n"
        f"📝 Jami savollar: {session.total_answered}\n"
        f"📈 Ball: {progress:.1f}%\n\n"
        f"⚠️ O'tish balli: 56%"
    )

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    del user_sessions[user_id]

# 🎛️ Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data.startswith("subject_"):
        await subject_selected(update, context)
    elif query.data in ['network_part1', 'network_part2']:
        await start_test(update, context)
    elif query.data.startswith("start_test_"):
        await start_test(update, context)
    elif query.data.startswith("answer_"):
        await check_answer(update, context)
    elif query.data == "next_question":
        await send_question(query, query.from_user.id)
    elif query.data == "finish_test":
        await query.answer()
        await finish_test(query, query.from_user.id)
    elif query.data == "back_to_subjects":
        await query.answer()
        text = (
            "🎓 *NDTU Test Tizimi*\n\n"
            "📚 *Fanlardan birini tanlang:*"
        )
        await query.edit_message_text(text, reply_markup=get_subjects_keyboard(), parse_mode='Markdown')

# 🚀 Ishga tushirish
def main():
    print("=" * 60)
    print("🎓 NDTU Test Bot - To'liq versiya")
    print("=" * 60)
    print("🔧 Database sozlanmoqda...")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot tayyor!")
    print("=" * 60)
    print("📚 Fanlar:")
    print("   • Web dasturlash          → questions.json")
    print("   • Ma'lumotlar bazasi      → questions.json")
    print("   • Dasturlash asoslari     → questions.json")
    print("   • Kompyuter tarmoqlari:")
    print("     - 📘 1-bo'lim           → network_part1.json")
    print("     - 📗 2-bo'lim           → network_part2.json")
    print("   • O'rnatilgan tizimlar    → embedded_systems.json")
    print("=" * 60)
    print("📊 Statistika: python admin.py")
    print("🎓 Bot ishga tushdi...")
    print("=" * 60)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
