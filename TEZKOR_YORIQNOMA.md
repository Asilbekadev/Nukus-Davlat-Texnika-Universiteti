# 🚀 TEZKOR O'RNATISH YO'RIQNOMASI

## ✅ TAYYOR FAYLLAR

1. **ndtu_bot_FINAL.py** - To'liq ishlaydigan bot
2. **network_part1_SAMPLE.json** - 30 ta savol bilan namuna
3. **Bu yo'riqnoma** - Qadamma-qadam ko'rsatma

---

## 📦 1-QADAM: Fayllarni joylashtirish

### A) Bot faylini almashtirish

```bash
# Eski faylni zaxiralash
cp ndtu_bot_db_check.py ndtu_bot_db_check_OLD.py

# Yangi faylni nusxa olish
cp ndtu_bot_FINAL.py ndtu_bot_db_check.py
```

**Yoki qo'lda:**
1. `ndtu_bot_FINAL.py` ni oching
2. Barcha kodni nusxa oling (Ctrl+A, Ctrl+C)
3. `ndtu_bot_db_check.py` ni oching
4. Barcha kodni o'chirib, yangisini joylashtiring (Ctrl+A, Ctrl+V)
5. Saqlang (Ctrl+S)

---

### B) network_part1.json yaratish

**Option 1: Namunadan nusxa olish**

```bash
# Namunani network_part1.json ga nusxa olish
cp network_part1_SAMPLE.json network_part1.json
```

**Option 2: Qo'lda yaratish**

1. Botning yonida yangi fayl yarating: `network_part1.json`
2. `network_part1_SAMPLE.json` dan barcha kodni nusxa oling
3. `network_part1.json` ga joylashtiring
4. 200 ta savolingizni qo'shing (format pastda)

---

## 📝 2-QADAM: Savollar formatini to'ldirish

### Format (har bir savol uchun):

```json
{
  "question": "Savol matni?",
  "answers": [
    {"text": "Javob 1", "correct": false},
    {"text": "Javob 2", "correct": true},
    {"text": "Javob 3", "correct": false},
    {"text": "Javob 4", "correct": false}
  ]
}
```

### ⚠️ MUHIM qoidalar:

- ✅ Har bir savolda FAQAT 1 ta `"correct": true` bo'lishi kerak
- ✅ Qolgan javoblarda `"correct": false`
- ✅ Vergullarni unutmang (oxirgi elementdan tashqari)
- ✅ Qo'shtirnoqlarni to'g'ri yoping

---

## 📊 3-QADAM: JSON formatni tekshirish

Faylni saqlagandan keyin:

```bash
# JSON formatni tekshirish
python3 -m json.tool network_part1.json > /dev/null && echo "✅ Format to'g'ri" || echo "❌ Format xato"
```

**Yoki online:**
- jsonlint.com saytiga boring
- Faylni yuklang yoki kodni joylashtiring

---

## 🚀 4-QADAM: Ishga tushirish

```bash
# Botni ishga tushirish
python3 ndtu_bot_db_check.py
```

### Ko'rinishi:

```
============================================================
🎓 NDTU Test Bot - Kompyuter Tarmoqlari 2 bo'limli
============================================================
🔧 Database sozlanmoqda...
✅ Bot tayyor!
============================================================
📚 Fanlar:
   • Web dasturlash (questions.json)
   • Ma'lumotlar bazasi (questions.json)
   • Dasturlash asoslari (questions.json)
   • Kompyuter tarmoqlari:
     - 📘 1-bo'lim (network_part1.json)
     - 📗 2-bo'lim (network_part2.json)
============================================================
📊 Statistika: python admin.py
🎓 Bot ishga tushdi...
============================================================
```

---

## ✅ 5-QADAM: Telegram'da test qilish

1. Telegram'da botni oching
2. `/start` bosing
3. Telefon raqamni yuboring (agar avval yuborilmagan bo'lsa)
4. "🌐 Kompyuter tarmoqlari" tugmasini bosing
5. **Yangi interfeys ko'rinadi:**

```
🌐 Kompyuter tarmoqlari

📚 Bo'limlarni tanlang:

📘 1-bo'lim
   • 200 ta savol
   • Barcha mavzular
   • Random tartib

📗 2-bo'lim
   • Tez orada qo'shiladi

🎯 Qaysi bo'limdan boshlaysiz?

[📘 1-bo'lim (200 ta savol)]
[📗 2-bo'lim (tez orada)]
[◀️ Orqaga]
```

6. "📘 1-bo'lim" ni bosing
7. Test boshlanadi! ✅

---

## 🔍 Xatoliklarni tuzatish

### ❌ Xato 1: "network_part1.json topilmadi"

**Sabab:** Fayl yo'q yoki noto'g'ri joyda

**Yechim:**
```bash
# Botning yonida ekanligini tekshiring
ls -la network_part1.json

# Agar yo'q bo'lsa, namunadan nusxa oling
cp network_part1_SAMPLE.json network_part1.json
```

---

### ❌ Xato 2: JSON format xatosi

**Sabab:** Sintaksis xatosi (vergul, qo'shtirnoq, va h.k.)

**Yechim:**
```bash
# Formatni tekshirish
python3 -m json.tool network_part1.json
```

Tez-tez xatolar:
- Vergul unutilgan: `}]` → `},]`
- Qo'shtirnoq ochiq: `"text: "Javob"` → `"text": "Javob"`
- Oxirida ortiqcha vergul: `[{"id": 1},]` → `[{"id": 1}]`

---

### ❌ Xato 3: Bo'limlar ko'rinmayapti

**Sabab:** Bot to'g'ri yangilanmagan

**Yechim:**
1. Botni to'xtatish: `Ctrl+C`
2. Faylni tekshirish:
```python
# 192-qator atrofida:
if query.data == "subject_network":
    # Bu kod bor ekanligini tekshiring
```
3. Qayta ishga tushirish:
```bash
python3 ndtu_bot_db_check.py
```

---

### ❌ Xato 4: Savollar boshlanmayapti

**Sabab:** callback_data noto'g'ri

**Terminal'da ko'ring:**
```
🎯 Test boshlandi: User=123456789, Subject=network_part1
📂 network_part1.json dan yuklanyapti...
✅ 30 ta savol yuklandi
```

Agar bu ko'rinmasa - botni qayta ishga tushiring.

---

## 📁 Fayl tuzilishi

```
ndtu_bot/
├── ndtu_bot_db_check.py       ← Yangilangan (FINAL versiya)
├── questions.json              ← O'zgarmagan (web, db, programming)
├── network_part1.json          ← YANGI (200 ta savol)
├── network_part1_SAMPLE.json   ← Namuna (30 ta savol)
├── users.db                    ← Database (avtomatik)
└── admin.py                    ← O'zgarmagan
```

---

## 🎯 Qisqacha

1. ✅ `ndtu_bot_FINAL.py` → `ndtu_bot_db_check.py` ga nusxa oling
2. ✅ `network_part1_SAMPLE.json` → `network_part1.json` yarating
3. ✅ 200 ta savolingizni qo'shing
4. ✅ JSON formatni tekshiring
5. ✅ Botni ishga tushiring
6. ✅ Telegram'da sinab ko'ring

---

## 🆘 Yordam kerakmi?

**Terminal'dagi xatolarni diqqat bilan o'qing:**

```bash
# Qizil matnlar - xatolar
# Yashil matnlar - muvaffaqiyat
```

**Xatolik haqida ma'lumot:**
1. Xato matnini to'liq nusxa oling
2. Qaysi qatorda xato bo'lganini toping
3. JSON validator da tekshiring (jsonlint.com)

---

## ✨ TAYYOR!

**3 ta oddiy qadam:**
1. Fayllarni nusxa oling
2. Savollarni qo'shing  
3. Ishga tushiring

**Muvaffaqiyatlar!** 🎉🚀