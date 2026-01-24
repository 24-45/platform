#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل القضايا الإعلامية المرتبطة بكل فعالية
"""

import pandas as pd
import re
from collections import Counter

# قراءة البيانات
csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"

df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# فلترة الإعلام التقليدي (online news)
traditional_df = df[df['Source Type'] == 'online news'].copy()
print(f"إجمالي الأخبار: {len(traditional_df)}")

# تعريف الفعاليات
events = {
    'كأس العرب 2025': r'كأس العرب|كاس العرب|arab cup|arabian gulf cup|خليجي 26|gulf cup|كأس الخليج',
    'FIFA U-17': r'تحت 17|U-17|U17|كأس العالم للناشئين|under.?17|ناشئين|U17|كأس العالم.*17',
    'F1 قطر': r'فورمولا|formula|F1|سباق|جائزة قطر الكبرى|grand prix|لوسيل|losail',
    'UFC Qatar': r'UFC|يو إف سي|فنون قتالية|مختلطة|MMA',
    'World Padel': r'بادل|padel|مضرب'
}

# القضايا الإعلامية المحتملة
topics = {
    'التنظيم والاستضافة': r'تنظيم|استضاف|organize|host|استقبال|ترتيب|إعداد|جاهز|نجاح التنظيم',
    'البنية التحتية': r'ملعب|استاد|منشأ|بنية تحتية|مرافق|stadium|infrastructure|منشآت|حلبة|مضمار',
    'الإنجازات الرياضية': r'فوز|فاز|بطل|لقب|إنجاز|تتويج|champion|victory|win|ذهب|فضة|برونز|medal|ميدالية|تأهل|أهداف',
    'الحضور الجماهيري': r'جماهير|جمهور|حضور|مشجع|تذاكر|crowd|fans|attendance|حشود|مدرجات',
    'الإشادة الدولية': r'إشادة|أشاد|ثناء|praise|commend|إعجاب|تقدير|امتياز|عالمي|دولي',
    'المنتخب القطري': r'منتخب قطر|العنابي|قطري|المنتخب الوطني|qatar national|qatar team|منتخبنا',
    'النجوم والمشاهير': r'نجم|نجوم|star|celebrity|مشاهير|لاعب|أسطورة|legend',
    'الإرث الرياضي': r'إرث|legacy|رؤية 2030|مستقبل|تطوير|development|استدامة',
    'البث والتغطية': r'بث|تغطية|broadcast|live|مباشر|قناة|شاشة|تلفزيون|إعلام',
    'الجوائز والتكريم': r'جائزة|تكريم|award|prize|أفضل|best|التميز|excellence'
}

print("\n" + "="*80)
print("تحليل القضايا الإعلامية لكل فعالية")
print("="*80)

# تحليل لكل فعالية
results = {}

for event_name, event_pattern in events.items():
    event_df = traditional_df[
        traditional_df['Title'].str.contains(event_pattern, case=False, na=False) | 
        traditional_df['Hit Sentence'].str.contains(event_pattern, case=False, na=False)
    ]
    
    print(f"\n{'='*60}")
    print(f"📌 {event_name} ({len(event_df)} خبر)")
    print(f"{'='*60}")
    
    topic_counts = {}
    for topic_name, topic_pattern in topics.items():
        # البحث في العنوان والمحتوى
        matches = event_df[
            event_df['Title'].str.contains(topic_pattern, case=False, na=False) |
            event_df['Hit Sentence'].str.contains(topic_pattern, case=False, na=False)
        ]
        count = len(matches)
        if count > 0:
            topic_counts[topic_name] = count
    
    # ترتيب حسب الأعلى
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nأبرز القضايا الإعلامية:")
    for i, (topic, count) in enumerate(sorted_topics[:5], 1):
        pct = (count / len(event_df) * 100) if len(event_df) > 0 else 0
        print(f"  {i}. {topic}: {count} ({pct:.1f}%)")
    
    results[event_name] = sorted_topics

# تحليل إجمالي للقضايا
print("\n" + "="*80)
print("📊 التحليل الإجمالي للقضايا الإعلامية (جميع الفعاليات)")
print("="*80)

total_topic_counts = {}
for topic_name, topic_pattern in topics.items():
    matches = traditional_df[
        traditional_df['Title'].str.contains(topic_pattern, case=False, na=False) |
        traditional_df['Hit Sentence'].str.contains(topic_pattern, case=False, na=False)
    ]
    total_topic_counts[topic_name] = len(matches)

sorted_total = sorted(total_topic_counts.items(), key=lambda x: x[1], reverse=True)
print(f"\nإجمالي الأخبار: {len(traditional_df)}")
print(f"\nالقضايا الإعلامية مرتبة:")
for i, (topic, count) in enumerate(sorted_total, 1):
    pct = (count / len(traditional_df) * 100)
    print(f"  {i}. {topic}: {count:,} ({pct:.1f}%)")

# تحليل Keyphrases الموجودة
print("\n" + "="*80)
print("📊 تحليل Keyphrases من البيانات")
print("="*80)

if 'Keyphrases' in traditional_df.columns:
    all_phrases = []
    for phrases in traditional_df['Keyphrases'].dropna():
        if isinstance(phrases, str):
            for phrase in phrases.split(','):
                phrase = phrase.strip()
                if phrase and len(phrase) > 2:
                    all_phrases.append(phrase)
    
    phrase_counts = Counter(all_phrases)
    print(f"\nأكثر 30 عبارة تكراراً:")
    for phrase, count in phrase_counts.most_common(30):
        print(f"  - {phrase}: {count}")
else:
    print("لا يوجد عمود Keyphrases")

# تحليل Keyphrases لكل فعالية
print("\n" + "="*80)
print("📊 أبرز Keyphrases لكل فعالية")
print("="*80)

for event_name, event_pattern in events.items():
    event_df = traditional_df[
        traditional_df['Title'].str.contains(event_pattern, case=False, na=False) | 
        traditional_df['Hit Sentence'].str.contains(event_pattern, case=False, na=False)
    ]
    
    if len(event_df) == 0:
        continue
        
    print(f"\n📌 {event_name}:")
    event_phrases = []
    for phrases in event_df['Keyphrases'].dropna():
        if isinstance(phrases, str):
            for phrase in phrases.split(','):
                phrase = phrase.strip()
                if phrase and len(phrase) > 2:
                    event_phrases.append(phrase)
    
    if event_phrases:
        phrase_counts = Counter(event_phrases)
        for phrase, count in phrase_counts.most_common(5):
            print(f"  - {phrase}: {count}")

# ملخص للشريحة
print("\n" + "="*80)
print("📋 ملخص للشريحة (Slide 29)")
print("="*80)
print("""
القضايا الإعلامية الأبرز:
""")
for i, (topic, count) in enumerate(sorted_total[:6], 1):
    pct = (count / len(traditional_df) * 100)
    print(f"{i}. {topic}: {count:,} خبر ({pct:.1f}%)")
