#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل موسع للمؤثرين في الصورة الإعلامية
البحث الشامل عن كل الشخصيات المذكورة
"""

import pandas as pd
import re
from collections import Counter

# قراءة البيانات
csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"

df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)
traditional_df = df[df['Source Type'] == 'online news'].copy()

print(f"إجمالي الأخبار: {len(traditional_df)}")

# ===== البحث الموسع =====

# شخصيات رياضية من كأس العرب
arab_cup_players = {
    # قطر
    'أكرم عفيف': r'أكرم\s*عفيف|Akram\s*Afif',
    'المعز علي': r'المعز\s*علي|Almoez\s*Ali',
    'سعد الشيب': r'سعد\s*الشيب|Saad\s*Sheeb',
    'حسن الهيدوس': r'الهيدوس|Haydos',
    'محمد منتري': r'منتري|Muntari',
    'كريم بوضياف': r'بوضياف|Boudiaf',
    'عبدالكريم حسن': r'عبدالكريم\s*حسن|Abdelkarim\s*Hassan',
    # مصر
    'محمد صلاح': r'محمد\s*صلاح|Mohamed\s*Salah|Mo\s*Salah|صلاح',
    'عمر مرموش': r'مرموش|Marmoush',
    'محمود تريزيجيه': r'تريزيجيه|Trezeguet',
    # السعودية
    'فراس البريكان': r'البريكان|Buraikan',
    'سالم الدوسري': r'الدوسري|Dosari',
    # العراق
    'أيمن حسين': r'أيمن\s*حسين|Ayman\s*Hussein',
    # المغرب
    'إبراهيم دياز': r'دياز|Diaz|براهيم',
    'أشرف حكيمي': r'حكيمي|Hakimi',
    # تونس
    'يوسف المساكني': r'المساكني|Msakni',
    # الجزائر
    'إسماعيل بن ناصر': r'بن\s*ناصر|Bennacer',
    'رياض محرز': r'محرز|Mahrez',
}

# مدربون
coaches = {
    'ماركيز لوبيز': r'ماركيز|لوبيز|Lopez|Marquez',
    'كارلوس كيروش': r'كيروش|Queiroz',
    'حسام حسن': r'حسام\s*حسن|Hossam\s*Hassan',
    'هيرفي رينار': r'رينار|Renard|هيرفي',
    'ألكسندر': r'ألكسندر|Alexander',
    'نبيل معلول': r'معلول|Maâloul',
    'جمال بلماضي': r'بلماضي|Belmadi',
}

# شخصيات رسمية قطرية (موسعة)
qatari_officials = {
    'الشيخ تميم بن حمد': r'تميم\s*بن\s*حمد|الأمير\s*تميم|أمير\s*قطر|Sheikh\s*Tamim|Emir',
    'الشيخ جوعان بن حمد': r'جوعان\s*بن\s*حمد|الشيخ\s*جوعان|Sheikh\s*Joaan',
    'الشيخ حمد بن خليفة بن أحمد': r'حمد\s*بن\s*خليفة\s*بن\s*أحمد',
    'الشيخ محمد بن حمد': r'محمد\s*بن\s*حمد\s*آل\s*ثاني',
    'ناصر الخاطر': r'ناصر\s*الخاطر|Nasser\s*Al-Khater',
    'حسن الذوادي': r'الذوادي|Al-Thawadi',
    'ياسر الجمال': r'ياسر.*الجمال',
    'فواز المسيفري': r'فواز.*المسيفري',
    'راشد النعيمي': r'راشد.*النعيمي',
}

# FIFA والاتحادات
fifa_entities = {
    'جياني إنفانتينو': r'إنفانتينو|انفانتينو|Infantino',
    'FIFA': r'\bFIFA\b|الفيفا',
    'AFC': r'\bAFC\b|الاتحاد\s*الآسيوي',
    'CAF': r'\bCAF\b|كاف|الاتحاد\s*الأفريقي',
    'UEFA': r'\bUEFA\b|الاتحاد\s*الأوروبي',
}

# وسائل الإعلام
media_channels = {
    'beIN Sports': r'beIN|بي\s*إن|بين\s*سبورت',
    'الكأس': r'\bالكأس\b|alkass|Al\s*Kass',
    'الجزيرة': r'\bالجزيرة\b|Al\s*Jazeera|Aljazeera',
    'العربية': r'\bالعربية\b|Al\s*Arabiya',
    'الرياضية السعودية': r'الرياضية\s*السعودية|SSC',
    'MBC': r'\bMBC\b',
    'ON Time': r'أون\s*تايم|ON\s*Time',
}

# F1 - شخصيات
f1_personalities = {
    'ماكس فيرستابن': r'فيرستابن|Verstappen',
    'لويس هاميلتون': r'هاميلتون|Hamilton',
    'تشارلز لوكلير': r'لوكلير|Leclerc',
    'لاندو نوريس': r'نوريس|Norris',
    'كارلوس ساينز': r'ساينز|Sainz',
}

# UFC - شخصيات
ufc_personalities = {
    'دانا وايت': r'دانا\s*وايت|Dana\s*White',
    'حبيب نورماغوميدوف': r'حبيب|Khabib|نورماغوميدوف',
    'إسلام ماخاتشيف': r'ماخاتشيف|Makhachev|إسلام',
}

# Padel - شخصيات
padel_personalities = {
    'رافا نادال': r'نادال|Nadal|رافا',
    'نوفاك ديوكوفيتش': r'ديوكوفيتش|Djokovic',
}

def search_and_analyze(df, name, pattern):
    matches = df[
        df['Title'].str.contains(pattern, case=False, na=False, regex=True) |
        df['Hit Sentence'].str.contains(pattern, case=False, na=False, regex=True)
    ]
    return len(matches)

print("\n" + "="*80)
print("🏛️ الشخصيات الرسمية القطرية")
print("="*80)
results = []
for name, pattern in qatari_officials.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'رسمية'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("⚽ اللاعبون (كأس العرب)")
print("="*80)
for name, pattern in arab_cup_players.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'لاعب'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("🎯 المدربون")
print("="*80)
for name, pattern in coaches.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'مدرب'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("🏆 FIFA والاتحادات")
print("="*80)
for name, pattern in fifa_entities.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'اتحاد'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("📺 القنوات الإعلامية")
print("="*80)
for name, pattern in media_channels.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'إعلام'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("🏎️ F1 شخصيات")
print("="*80)
for name, pattern in f1_personalities.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'F1'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("🥊 UFC شخصيات")
print("="*80)
for name, pattern in ufc_personalities.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'UFC'))
        print(f"  {name}: {count}")

print("\n" + "="*80)
print("🎾 Padel شخصيات")
print("="*80)
for name, pattern in padel_personalities.items():
    count = search_and_analyze(traditional_df, name, pattern)
    if count > 0:
        results.append((name, count, 'Padel'))
        print(f"  {name}: {count}")

# ترتيب النتائج
print("\n" + "="*80)
print("📋 ملخص المؤثرين (مرتب حسب الظهور)")
print("="*80)

sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
for name, count, category in sorted_results[:20]:
    print(f"  {name} ({category}): {count}")

# حساب التوزيع
categories = {}
for name, count, category in results:
    if category not in categories:
        categories[category] = 0
    categories[category] += count

print("\n📊 توزيع حسب الفئة:")
for cat, total in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {total}")
