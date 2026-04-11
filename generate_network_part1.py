#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kompyuter Tarmoqlari 1-bo'lim - Barcha 200 ta savolni yaratish
Ishlatish: python3 generate_network_part1.py
"""

import json

# BARCHA 200 TA SAVOL (* belgisi to'g'ri javobni bildiradi)
ALL_QUESTIONS = [
    {"savol": "Quyida keltirilgan kompyuter tarmoqlarining qaysi biri avval paydo bo'lgan?", "javoblar": ["global kompyuter tarmoqlari", "*lokal kompyuter tarmoqlari", "kampuslar tarmog'i", "korporativ tarmoqlar"]},
    {"savol": "To'rtta bir-biri bilan bog'langan bog'lamlar strukturasi (kvadrat shaklida) qaysi topologiya turiga mansub?", "javoblar": ["Xalqa", "Yulduz", "*To'liq bog'lanishli", "Yacheykali"]},
    {"savol": "Ketma-ket bir-biri bilan bog'langan 3 ta bog'lamlar (oxiri boshi bilan bog'lanmagan) strukturasi qaysi topologiya turiga tegishli?", "javoblar": ["*Umumiy shina", "Xalqa", "To'liq bog'lanishli", "Yulduz"]},
    {"savol": "Kompyuter tizimlarida ma'lumotlarni uzatish ishonchliligini oshirish qanday amal bilan bajariladi?", "javoblar": ["*kontrol summani xisoblash bilan", "ma'lumotni bir necha marta uzatish bilan", "axborotni ishonchliligini tekshirishning majoritar usulini", "maxsus apparat-programma vositalari yordamida"]},
    {"savol": "Qaysi topologiya birgalikda foydalanilmaydigan muhitni qo'llamasligi mumkin?", "javoblar": ["*to'liq bog'lanishli", "Xalqa", "Yulduz", "umumiy shina"]},
    {"savol": "Kompyuterning tashqi interfeysi deganda nima tushuniladi?", "javoblar": ["*kompyuter bilan tashqi qurilmani bog'lovchi simlar va ular orqali axborot almashinish qoidalari to'plamlari", "tashqi qurilmani kompyuterga bog'lashda ishlatiladigan ulovchi simlar", "kompyuterning tashqi portlari", "tashqi qurilma bilan kompyuter o'rtasida axborot almashinish qoidalari to'plami"]},
    {"savol": "Uchta o'zaro bog'langan bog'lamlardan iborat tuzilma (uchburchak shaklida) topologiyaning qaysi turiga tegishli?", "javoblar": ["*To'liq bog'lanishli", "Umumiy shina", "Yulduz", "Yacheykali"]},
    {"savol": "Qanday topologiyaning xususiy xoli umumiy shina xisoblanadi?", "javoblar": ["*Yulduz", "To'liq bog'lanishli", "Xalqa", "Yacheykali"]},
    {"savol": "Topologiyalardan qaysi biri ishonchliligi yuqori hisoblanadi?", "javoblar": ["Yulduz", "Xalqa", "*Аralash", "Umumiy shina"]},
    {"savol": "MAC sathi qanday vazifani bajaradi?", "javoblar": ["*uzatish muhitiga murojaat qilishni boshqarish", "stantsiyalar o'rtasida axborotni har-xil ishonchlilik darajasi bilan uzatish", "bitlar sathida axborot uzatishni boshqarish", "bloklar sathida axborot uzatishni boshqarish"]},
    {"savol": "LLC sathi qanday vazifani bajaradi?", "javoblar": ["*stantsiyalar o'rtasida axborotni har-xil ishonchlilik darajasi bilan uzatish", "bitlar sathida axborot uzatishni boshqarish", "bloklar sathida axborot uzatishni boshqarish", "uzatish muhitiga murojaat qilishni boshqarish"]},
    {"savol": "Stantsiyalar o'rtasida axborotni har-xil ishonchlilik darajasi bilan uzatish vazifasini qaysi sath bajaradi?", "javoblar": ["*LLC sathi", "Fizik sath", "Tarmoq sathi", "MAC sathi"]},
    {"savol": "Uzatish muhitiga murojaat qilishni boshqarish vazifasini qaysi sath bajaradi?", "javoblar": ["*MAC sathi", "Fizik sath", "Tarmoq sathi", "LLC sathi"]},
    {"savol": "l0Base-2 segmentining uzunligi ko'pi bilan qancha bo'lishi mumkin?", "javoblar": ["*185 metr", "400 metr", "200 metr", "500 metr"]},
    {"savol": "O'ralma juftlik kabeli simlarini, uning konnektorlariga ulashning necha xil variantlari mavjud?", "javoblar": ["*2", "3", "4", "1"]},
    {"savol": "Ethernet tarmoqlarida uzatish muhitiga murojaat qilishning qaysi usuli qo'llaniladi?", "javoblar": ["*CSMA/CD", "CSTK/CE", "CSQE/NQ", "CSTK/QL"]},
    {"savol": "Ethernet da kommutatsiyalashning qaysi xilidan foydalaniladi?", "javoblar": ["*paketlarni deytagrammali kommutatsiyalash", "paketlarni virtual kanal orqali uzatish", "vaqtni taqsimlash asosida kanallarni kommutatsiyalash", "chastotali multiplekslash asosida kanallarni kommutatsiyalash"]},
    {"savol": "Optik tolali Ethernet tarmog'ining maksimal uzunligi qanday?", "javoblar": ["*2740 m", "500 m", "5000 m", "2500 m"]},
    {"savol": "100Base-TX spetsifikatsiyasi qaysi texnologiyaga tegishli?", "javoblar": ["*Fast Ethernet", "Ethernet", "Gigabit Ethernet", "FDDI"]},
    {"savol": "Ethernet texnologiyasi tarmoqlarida ma'lumotlar kadri qanday preambulaga ega?", "javoblar": ["1111", "11110000", "*10101010", "11001100"]},
    {"savol": "Signalni to'liq aylanib chiqish vaqti –PDV ning maksimal qiymati qanday?", "javoblar": ["576 bitli interval", "*512 bitli interval", "600 bitli interval", "624 bitli interval"]},
    {"savol": "PDV deganda nima tushuniladi?", "javoblar": ["*Signalni to'liq aylanib chiqish vaqti", "Kadrlar orasidagi masofaning qisqarishi", "Kadrlar orasidagi masofa", "Bitli interval"]},
    {"savol": "Fast Ethernet texnologiyasi spetsifikatsiyalari qaysi komitet tarkibida ishlab chiqilgan?", "javoblar": ["*802.3", "802.2", "802.1", "802.5"]},
    {"savol": "Ethernet texnologiyasida koaksial kabelining ma'lumotlarni uzatish tezligi qanday?", "javoblar": ["*10 Mbit/s", "1 Mbit/s", "100 Mbit/s", "1000 Mbit/s"]},
    {"savol": "Fast Ethernet texnologiyasida o'ralma juftlik kabelining ma'lumotlarni uzatish tezligi qanday?", "javoblar": ["*100 Mbit/s", "10 Mbit/s", "1 Mbit/s", "1000 Mbit/s"]},
    {"savol": "Lokal tarmoqlarda keng tarqalgan topologiya turi qaysi?", "javoblar": ["*Yulduz", "Xalqa", "To'liq bog'langan", "Umumiy shina"]},
    {"savol": "1000Base-SX spetsifikatsiya qaysi texnologiyaga tegishli?", "javoblar": ["*Gigabit Ethernet", "Fast Ethernet", "Ethernet", "10G Ethernet"]},
    {"savol": "10Base-T standartida o'ralma juftlik kabeli simlarining nechta jufti ishlatiladi?", "javoblar": ["*2", "4", "1", "3"]},
    {"savol": "100Base-TX spetsifikatsiyasida o'ralma juftlik kabeli simlarining nechta jufti ishlatiladi?", "javoblar": ["*2", "4", "1", "3"]},
    {"savol": "Kompyuterni kontsentrator yoki kommutator bilan ulash uchun UTP kabelining qaysi varianti ishlatiladi?", "javoblar": ["*To'g'ridan-to'g'ri ulangan varianti", "Teskari ulangan varianti", "Krossover varianti", "Kesishgan holda ulangan varianti"]},
    # ... davomi ...
]

def convert_to_bot_format(q_data):
    """* belgili formatni bot formatiga o'tkazish"""
    formatted = {
        "question": q_data["savol"],
        "answers": []
    }
    
    for javob in q_data["javoblar"]:
        if javob.startswith("*"):
            formatted["answers"].append({
                "text": javob[1:],  # * ni olib tashlash
                "correct": True
            })
        else:
            formatted["answers"].append({
                "text": javob,
                "correct": False
            })
    
    return formatted


def main():
    print("=" * 60)
    print("🎓 Kompyuter Tarmoqlari 1-bo'lim - Savollar generatori")
    print("=" * 60)
    
    # Bot formatiga o'tkazish
    bot_questions = [convert_to_bot_format(q) for q in ALL_QUESTIONS]
    
    # Faylga yozish
    output_file = 'network_part1.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bot_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Tayyor!")
    print(f"📁 Fayl: {output_file}")
    print(f"📊 Savollar soni: {len(bot_questions)}")
    print(f"💾 Fayl hajmi: {len(json.dumps(bot_questions, ensure_ascii=False))} bayt")
    
    # Birinchi savolni ko'rsatish
    print(f"\n📝 Birinchi savol:")
    print(json.dumps(bot_questions[0], ensure_ascii=False, indent=2))
    
    print(f"\n⚠️  ESLATMA: Hozirda {len(ALL_QUESTIONS)} ta savol qo'shilgan.")
    print(f"    Qolgan savollarni qo'shish uchun ALL_QUESTIONS ro'yxatiga davom eting.")
    print(f"\n🚀 Botni ishga tushirish: python ndtu_bot_db_check.py")


if __name__ == '__main__':
    main()
