# Fayl Tizimi Analizatori va Menedjer 🚀

Murakkab va foydali Python script - fayl tizimingizni tahlil qilish va boshqarish uchun.

## Xususiyatlar 🌟

1. **To'liq Katalog Tahlili** - Fayllar va kataloglar statistikasi
2. **Dublikat Fayllarni Topish** - SHA-256 hash orqali
3. **Fayl Turlari Statistikasi** - Kengaytma bo'yicha guruhlash
4. **Eng Katta Fayllar** - Disk joyini egallagan fayllarni topish
5. **Dublikatlarni Avtomatik O'chirish** - Disk joyini bo'shatish
6. **JSON Eksport** - Hisobotni saqlash

## O'rnatish 📦

```bash
# Scriptga ruxsat berish
chmod +x file_system_analyzer.py

# Ishga tushirish
python file_system_analyzer.py --help
```

## Foydalanish 💻

### 1. To'liq tahlil

```bash
python file_system_analyzer.py /path/to/directory --analyze
```

Natija:
```
🔍 Tahlil boshlanmoqda: /path/to/directory
============================================================

📊 UMUMIY STATISTIKA
============================================================
Jami fayllar: 1523
Jami kataloglar: 89
Umumiy hajm: 2.45 GB
Xatolar: 0

📁 FAYL TURLARI BO'YICHA STATISTIKA
============================================================
.jpg                 | Soni:    450 | Hajm:     1.20 GB | 49.0%
.py                  | Soni:    320 | Hajm:   450.50 MB | 18.0%
.txt                 | Soni:    280 | Hajm:    85.30 MB | 3.5%
```

### 2. Dublikatlarni topish

```bash
python file_system_analyzer.py /path/to/directory --duplicates
```

### 3. Eng katta fayllarni ko'rish

```bash
# Eng katta 20 ta faylni ko'rsatish
python file_system_analyzer.py /path/to/directory --large-files 20
```

### 4. Dublikatlarni o'chirish

```bash
python file_system_analyzer.py /path/to/directory --duplicates --clean-duplicates
```

⚠️ **Diqqat**: Bu buyruq dublikat fayllarni o'chiradi! Ehtiyot bo'ling.

### 5. Hisobotni saqlash

```bash
python file_system_analyzer.py /path/to/directory --analyze --export report.json
```

### 6. Barcha funksiyalarni birga ishlatish

```bash
python file_system_analyzer.py ~/Documents \
  --analyze \
  --duplicates \
  --large-files 15 \
  --export analysis_report.json
```

## Parametrlar 📋

| Parametr | Qisqa | Tavsif |
|----------|-------|--------|
| `--analyze` | `-a` | To'liq tahlil qilish |
| `--duplicates` | `-d` | Dublikatlarni topish |
| `--large-files N` | `-l N` | Eng katta N ta faylni ko'rsatish |
| `--clean-duplicates` | `-c` | Dublikatlarni o'chirish |
| `--export FILE` | `-e FILE` | JSON ga eksport |

## Misol Natijalar 📊

### Umumiy Statistika
- ✅ 1,523 ta fayl tahlil qilindi
- 📁 89 ta katalog topildi
- 💾 2.45 GB umumiy hajm
- 🔄 45 ta dublikat guruh (120 MB)
- 📦 Eng katta fayl: video.mp4 (850 MB)

### Fayl Turlari
- **Rasmlar (.jpg, .png)**: 1.2 GB (49%)
- **Python (.py)**: 450 MB (18%)
- **Dokumentlar (.pdf, .docx)**: 380 MB (15%)
- **Video (.mp4, .avi)**: 320 MB (13%)
- **Boshqalar**: 130 MB (5%)

## Texnik Ma'lumotlar ⚙️

- **Til**: Python 3.6+
- **Kutubxonalar**: Standart kutubxonalar (qo'shimcha o'rnatish kerak emas)
- **Hash Algoritmi**: SHA-256
- **Ishlash Tezligi**: ~1000 fayl/soniya (SSD da)

## Xavfsizlik 🔒

- Fayllarni o'qishdan oldin ruxsatlarni tekshiradi
- Dublikatlarni o'chirishdan oldin tasdiqlash so'raydi
- Barcha operatsiyalar loglarga yoziladi
- Asl fayllarni saqlab qolish (birinchi nusxani)

## Foydalanish Stsenariylari 💡

1. **Disk Joyini Bo'shatish**: Dublikatlarni topib o'chirish
2. **Loyiha Tahlili**: Qaysi fayl turlari ko'p joy egallashini bilish
3. **Backup Tekshirish**: Dublikatlarni topish
4. **Fayllarni Tartibga Solish**: Katta fayllarni topib boshqa joyga ko'chirish
5. **Audit**: Tizim holatini muntazam tekshirish

## Kelajakdagi Yangilanishlar 🔮

- [ ] GUI interfeys qo'shish
- [ ] Parallel fayllarni qayta ishlash
- [ ] Cloud storage integratsiyasi
- [ ] Avtomatik tartibga solish
- [ ] Fayllarni siqish taklifi

## Muammolar va Yechimlar 🔧

**Muammo**: "Permission denied" xatosi
**Yechim**: Script sudo bilan ishga tushiring yoki faqat o'qish mumkin bo'lgan kataloglarni tahlil qiling

**Muammo**: Juda sekin ishlaydi
**Yechim**: Dublikatlarni topishni o'chiring (`--duplicates` ni ishlatmang)


**Muallif**: Claude (Anthropic AI yordamida)
**Versiya**: 1.0.0
**Sana**: 2026
