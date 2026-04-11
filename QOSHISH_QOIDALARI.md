# 📚 Kompyuter Tarmoqlari 1-bo'limni qo'shish - TO'LIQ YO'RIQNOMA

## 🎯 Maqsad
Kompyuter Tarmoqlari faniga 2 ta bo'lim qo'shish:
- 📘 **1-bo'lim** - 200 ta savol (sizning savollaringiz)
- 📗 **2-bo'lim** - keyinroq qo'shiladi

## 📁 Kerakli fayllar

```
ndtu_bot/
├── ndtu_bot_db_check.py     ← YANGILASH KERAK
├── questions.json            ← O'ZGARMAYDI (web, db, programming)
├── network_part1.json        ← YANGI FAYL YARATISH KERAK
└── users.db                  ← O'zgarmaydi
```

---

## 📝 1-QADAM: `network_part1.json` yaratish

###Option 1: Qo'lda yaratish

Botning yonida `network_part1.json` faylini yarating:

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

**⚠️ MUHIM Format qoidalari:**
- `question` - savol matni
- `answers` - javoblar massivi
- `text` - javob matni  
- `correct` - to'g'ri javob uchun `true`, noto'g'ri uchun `false`
- Faqat BITTA javob `"correct": true` bo'lishi kerak

### Option 2: Python skript bilan

Men sizga `generate_network_part1.py` faylini tayyorladim.

**Ishlatish:**
1. Fayldagi `ALL_QUESTIONS` ro'yxatiga barcha savollaringizni qo'shing:
```python
ALL_QUESTIONS = [
    {"savol": "...", "javoblar": ["noto'g'ri", "*to'g'ri", "noto'g'ri", "noto'g'ri"]},
    # ... 200 ta savol
]
```

2. Skriptni ishga tushiring:
```bash
python3 generate_network_part1.py
```

3. `network_part1.json` avtomatik yaratiladi! ✅

---

## 🤖 2-QADAM: Botni yangilash

`ndtu_bot_db_check.py` faylida **3 TA JOY**ni yangilash kerak:

### ✏️ A) Kompyuter Tarmoqlari tugmasiga bo'limlar qo'shish

**📍 Joylashuv:** ~140-qator, `subject_selected()` funksiyasi

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

    # ⭐⭐⭐ YANGI KOD - Kompyuter tarmoqlari uchun bo'limlar ⭐⭐⭐
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
    # ⭐⭐⭐ YANGI KOD TUGADI ⭐⭐⭐

    # Qolgan fanlar uchun eski kod davom etadi
    keyboard = [
        [InlineKeyboardButton("📝 Testni boshlash", callback_data=f"start_test_{query.data.split('_')[1]}")],
        [InlineKeyboardButton("◀️ Orqaga", callback_data="back_to_subjects")]
    ]
    # ... qolgan kod
```

---

### ✏️ B) Savollarni yuklashda alohida fayl ishlatish

**📍 Joylashuv:** ~205-qator, `send_question()` funksiyasi

**O'ZGARTIRISH KERAK:**

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
    elif session.subject == 'network_part2':
        with open('network_part2.json', 'r', encoding='utf-8') as f:
            all_questions = json.load(f)
    else:
        # Web, DB, Programming uchun questions.json
        with open('questions.json', 'r', encoding='utf-8') as f:
            all_questions = json.load(f).get(session.subject, [])
except Exception as e:
    await query.edit_message_text(f"❌ Savollar topilmadi! Xato: {str(e)}")
    return
```

---

### ✏️ C) Database'da saqlash (ixtiyoriy yangilash)

**Database o'zgarmaydi!** Chunki:
- `subject` ustuni `TEXT` tipida
- `"network_part1"` deb saqlaydi
- Hech qanday struktura o'zgarmaydi

Agar ixtiyoriy ravishda ko'rsatish uchun nom qo'shmoqchi bo'lsangiz:

```python
# Admin.py yoki finish_test() da
subject_names = {
    "web": "Web dasturlash",
    "db": "Ma'lumotlar bazasi",
    "programming": "Dasturlash asoslari",
    "network_part1": "Kompyuter tarmoqlari - 1-bo'lim",
    "network_part2": "Kompyuter tarmoqlari - 2-bo'lim"
}
```

---

## 🚀 3-QADAM: Ishga tushirish

1. **Fayllarni tekshiring:**
```bash
ls -la
# Ko'rinishi kerak:
# ndtu_bot_db_check.py
# questions.json
# network_part1.json  ← Yangi!
# users.db
```

2. **network_part1.json formatini tekshiring:**
```bash
python3 -m json.tool network_part1.json > /dev/null && echo "✅ JSON formati to'g'ri" || echo "❌ JSON xatosi"
```

3. **Botni ishga tushiring:**
```bash
python3 ndtu_bot_db_check.py
```

4. **Konsolda ko'ring:**
```
🔧 Database sozlanmoqda...
✅ NDTU Test Bot tayyor!
🎓 Bot ishga tushdi...
```

---

## ✅ 4-QADAM: Sinov

### Telegram'da test qiling:

1. `/start` bosing
2. Telefon raqam yuboring
3. "🌐 Kompyuter tarmoqlari" tanlang
4. **Yangi interfeys ko'rinishi kerak:**

```
🌐 Kompyuter tarmoqlari

📚 Bo'limlarni tanlang:
• 📘 1-bo'lim - 200 ta savol
• 📗 2-bo'lim - (tez orada)

🎯 Qaysi bo'limdan boshlaysiz?

[📘 1-bo'lim]
[📗 2-bo'lim]
[◀️ Orqaga]
```

5. "📘 1-bo'lim" bosing
6. Testni boshlang va tekshiring

---

## 📊 Natijalarni ko'rish

Database'da saqlangan:

```bash
python3 admin.py
# 2 ni tanlang (Test natijalarini ko'rish)
```

Ko'rinishi:
```
ID     User ID    Fan                          To'g'ri  Jami  Ball    Status
1      123456789  network_part1                15       20    75.0%   ✅ O'tdi
```

---

## ⚠️ Tez-tez uchraydigan xatolar

### ❌ Xato 1: `network_part1.json` topilmadi
**Sabab:** Fayl yo'q yoki noto'g'ri joyda

**Yechim:**
```bash
# Botning yonida ekanligini tekshiring
ls -la network_part1.json

# Agar yo'q bo'lsa, yarating
touch network_part1.json
```

---

### ❌ Xato 2: JSON format xatosi
**Sabab:** JSON sintaksisi noto'g'ri

**Yechim:**
```bash
# Formatni tekshiring
python3 -m json.tool network_part1.json

# Yoki online: jsonlint.com
```

Tez-tez uchraydigan xatolar:
- Vergul unutish: `{"text": "Javob"} <- vergul kerak ,`
- Qo'shtirnoq ochiq: `"text: "Javob"` ← yopish kerak
- Oxirgi elementda ortiqcha vergul: `{"id": 1},]` ← vergulni olib tashlash

---

### ❌ Xato 3: Bot ishlayapti, lekin bo'limlar ko'rinmayapti
**Sabab:** `subject_selected()` to'g'ri yangilanmagan

**Yechim:**
```python
# Tekshiring: if query.data == "subject_network":
# Qayta ishga tushiring
```

---

### ❌ Xato 4: Savollar random emas
**Sabab:** `random.choice()` ishlamayapti

**Yechim:** Bot'ni to'xtatib, qayta ishga tushiring
```bash
Ctrl+C  # To'xtatish
python3 ndtu_bot_db_check.py  # Qayta ishga tushirish
```

---

## 🎨 Qo'shimcha: 2-bo'limni qo'shish

Kelajakda 2-bo'lim qo'shish uchun:

1. `network_part2.json` yarating (xuddi network_part1 kabi)
2. Bot kodida allaqachon tayyor:
   - `"start_test_network_part2"` callback
   - `elif session.subject == 'network_part2'` shartlash

Faqat faylni yaratish va savollarni qo'shish kifoya!

---

## 📞 Yordam

**Muammo yuzaga kelsa:**

1. **Terminal'dagi xatolarni o'qing**
   ```bash
   python3 ndtu_bot_db_check.py
   # Qizil matnlardagi xatolarni diqqat bilan o'qing
   ```

2. **JSON formatini tekshiring**
   ```bash
   python3 -c "import json; print(json.load(open('network_part1.json'))[:1])"
   ```

3. **Database'ni tekshiring**
   ```bash
   python3 admin.py
   ```

---

## ✨ Xulosa

**3 ta qadam:**
1. ✅ `network_part1.json` yarating (200 ta savol)
2. ✅ Bot'da 3 joyni yangilang (A, B, C)
3. ✅ Ishga tushiring va test qiling

**Tayyor!** 🎉

Muvaffaqiyatlar! 🚀