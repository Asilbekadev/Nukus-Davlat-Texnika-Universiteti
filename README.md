# 🎓 Kompyuter Tarmoqlari 1-bo'limni qo'shish yo'riqnomasi

## 📋 QADAMMA-QADAM YO'RIQNOMA

### 1️⃣ QADAM: `network_part1.json` faylini yaratish

Bot bilan bir katalogda yangi fayl yarating:

**Fayl nomi:** `network_part1.json`

**Struktura:**
```json
[
  {
    "question": "Savol matni?",
    "answers": [
      {"text": "Javob 1", "correct": false},
      {"text": "Javob 2", "correct": true},
      {"text": "Javob 3", "correct": false},
      {"text": "Javob 4", "correct": false}
    ]
  }
]
```

**⚠️ MUHIM:**
- `questions.json` ga tegmang!
- Yangi fayl yarating: `network_part1.json`
- Bot bilan bir xil papkada bo'lsin

---

### 2️⃣ QADAM: Botni yangilash (ndtu_bot_db_check.py)

#### A) Fanlar menyusini yangilash

**📍 66-qator atrofida:** `get_subjects_keyboard()` funksiyasini toping

**Eski kod:**
```python
def get_subjects_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Web dasturlash", callback_data="subject_web")],
        [InlineKeyboardButton("💾 Ma'lumotlar bazasi", callback_data="subject_db")],
        [InlineKeyboardButton("💻 Dasturlash asoslari", callback_data="subject_programming")],
        [InlineKeyboardButton("🌐 Kompyuter tarmoqlari", callback_data="subject_network")]
    ])
```

**Yangi kod:**
```python
def get_subjects_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Web dasturlash", callback_data="subject_web")],
        [InlineKeyboardButton("💾 Ma'lumotlar bazasi", callback_data="subject_db")],
        [InlineKeyboardButton("💻 Dasturlash asoslari", callback_data="subject_programming")],
        [InlineKeyboardButton("🌐 Kompyuter tarmoqlari", callback_data="subject_network")]
    ])
```

---

#### B) Kompyuter Tarmoqlari bo'limlarini ko'rsatish

**📍 145-150 qator atrofida:** `subject_selected()` funksiyasida

**Qo'shish kerak:**

```python
async def subject_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subjects = {
        "subject_web": "🌐 Web dasturlash",
        "subject_db": "💾 Ma'lumotlar bazasi",
        "subject_programming": "💻 Dasturlash asoslari",
        "subject_network": "🌐 Kompyuter tarmoqlari"
    }

    subject_name = subjects.get(query.data, "Fan")

    # ⭐ YANGI: Kompyuter tarmoqlari uchun 2 bo'lim
    if query.data == "subject_network":
        keyboard = [
            [InlineKeyboardButton("📘 1-bo'lim", callback_data="start_test_network_part1")],
            [InlineKeyboardButton("📗 2-bo'lim", callback_data="start_test_network_part2")],
            [InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_subjects")]
        ]
        
        text = (
            f"🌐 *Kompyuter tarmoqlari*\n\n"
            "📚 *Bo'limlarni tanlang:*\n"
            "• 📘 1-bo'lim - 200 ta savol\n"
            "• 📗 2-bo'lim - (tez orada)\n\n"
            "🎯 *Qaysi bo'limdan boshlaysiz?*"
        )
        
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    # Qolgan fanlar uchun eski kod
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
```

---

#### C) Savollarni yuklash (send_question funksiyasi)

**📍 205-215 qator atrofida:** `send_question()` funksiyasida

**Eski kod:**
```python
try:
    with open('questions.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f).get(session.subject, [])
except:
    await query.edit_message_text("❌ Savollar bazasi topilmadi!")
    return
```

**Yangi kod:**
```python
try:
    # ⭐ YANGI: network_part1 uchun alohida fayl
    if session.subject == 'network_part1':
        with open('network_part1.json', 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
    else:
        with open('questions.json', 'r', encoding='utf-8') as f:
            all_questions = json.load(f).get(session.subject, [])
except Exception as e:
    await query.edit_message_text(f"❌ Savollar bazasi topilmadi! Xato: {str(e)}")
    return
```

---

#### D) Button handler yangilash

**📍 300-310 qator atrofida:** `button_handler()` funksiyasida

```python
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data.startswith("subject_"):
        await subject_selected(update, context)
    elif query.data.startswith("start_test_"):
        await start_test(update, context)
    # ... qolgan kodlar
```

---

### 3️⃣ QADAM: Savollarni `network_part1.json` ga qo'shish

Men sizga 200 ta savolni tayyor formatda beraman.

**Faylda saqlanadigan format:**

```json
[
  {
    "question": "Quyida keltirilgan kompyuter tarmoqlarining qaysi biri avval paydo bo'lgan?",
    "answers": [
      {"text": "global kompyuter tarmoqlari", "correct": false},
      {"text": "lokal kompyuter tarmoqlari", "correct": true},
      {"text": "kampuslar tarmog'i", "correct": false},
      {"text": "korporativ tarmoqlar", "correct": false}
    ]
  },
  {
    "question": "To'rtta bir-biri bilan bog'langan bog'lamlar strukturasi (kvadrat shaklida) qaysi topologiya turiga mansub?",
    "answers": [
      {"text": "Xalqa", "correct": false},
      {"text": "Yulduz", "correct": false},
      {"text": "To'liq bog'lanishli", "correct": true},
      {"text": "Yacheykali", "correct": false}
    ]
  }
]
```

---

### 4️⃣ QADAM: Database o'zgarishlari (SHART EMAS!)

Database'ni o'zgartirish kerak emas! Chunki:
- `test_results` jadvalidagi `subject` ustuni TEXT tipida
- `network_part1` deb yoziladi
- Hech qanday struktura o'zgarmaydi

---

### 5️⃣ QADAM: Testlash

1. **Botni ishga tushiring:**
```bash
python ndtu_bot_db_check.py
```

2. **Telegram'da sinab ko'ring:**
   - /start bosing
   - "🌐 Kompyuter tarmoqlari" tanlang
   - "📘 1-bo'lim" ko'rinishi kerak
   - Testni boshlang

3. **Xatoliklarni tekshiring:**
```bash
# Terminal'da ko'ring:
# ✅ network_part1.json dan yuklandi
# ✅ 200 ta savol topildi
```

---

## 📊 NATIJA

**Foydalanuvchi ko'radi:**
```
🎓 NDTU Test Tizimi

📚 Fanlardan birini tanlang:
[🌐 Web dasturlash]
[💾 Ma'lumotlar bazasi]
[💻 Dasturlash asoslari]
[🌐 Kompyuter tarmoqlari]  ← Bu bosilsa

👇 Pastda bo'limlar paydo bo'ladi:
[📘 1-bo'lim]  ← 200 ta savol
[📗 2-bo'lim]  ← (tez orada)
[◀️ Orqaga]
```

---

## 🎯 FAYLLAR RO'YXATI

```
ndtu_bot/
├── ndtu_bot_db_check.py    ← Yangilangan bot
├── questions.json           ← O'zgarmagan (web, db, programming)
├── network_part1.json       ← YANGI fayl (200 ta savol)
├── users.db                 ← Database (o'zgarmaydi)
└── admin.py                 ← Admin panel (o'zgarmaydi)
```

---

## ⚠️ MUHIM ESLATMALAR

1. **`questions.json` ga tegmang** - bu web, db, programming uchun
2. **Yangi fayl yarating** - `network_part1.json`
3. **Database o'zgarmaydi** - subject TEXT tipida
4. **Testdan keyin** - admin.py orqali natijalarni ko'ring

---

## 🆘 TEZKOR YORDAM

**Xato 1:** `network_part1.json` topilmadi
→ Faylni bot bilan bir papkaga qo'ying

**Xato 2:** JSON format xatosi
→ JSON validator da tekshiring (jsonlint.com)

**Xato 3:** Savollar chiqmaydi
→ `print(len(all_questions))` qo'shib tekshiring

---

## ✅ QISQACHA

1. `network_part1.json` yarating
2. Botda 3 joyni yangilang (A, B, C)
3. 200 ta savolni qo'shing
4. Ishga tushiring va sinab ko'ring

**Tayyor!** 🎉
