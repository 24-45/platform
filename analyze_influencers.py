#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل المؤثرين في الصورة الإعلامية - الفعاليات الكبرى
تحليل المصادر والكُتّاب الأكثر تأثيراً
"""

import pandas as pd
from collections import Counter

# قراءة البيانات
csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"

df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# فلترة الإعلام التقليدي (online news)
traditional_df = df[df['Source Type'] == 'online news'].copy()
print(f"إجمالي الأخبار (الإعلام التقليدي): {len(traditional_df)}")

# تحليل المصادر الإخبارية (Source Name)
print("\n" + "="*80)
print("📰 أكثر المصادر الإخبارية تغطية")
print("="*80)

source_counts = traditional_df['Source Name'].value_counts().head(20)
print("\nأكثر 20 مصدر:")
for source, count in source_counts.items():
    pct = (count / len(traditional_df)) * 100
    print(f"  - {source}: {count} ({pct:.1f}%)")

# تحليل الكُتّاب (Author Name)
print("\n" + "="*80)
print("✍️ أكثر الكُتّاب/المحررين نشراً")
print("="*80)

author_counts = traditional_df['Author Name'].dropna().value_counts().head(20)
print("\nأكثر 20 كاتب:")
for author, count in author_counts.items():
    if author and str(author).strip():
        print(f"  - {author}: {count}")

# تحليل نوع المصادر
print("\n" + "="*80)
print("📊 توزيع أنواع المصادر")
print("="*80)

# تصنيف المصادر حسب الدولة
qatar_sources = ['الراية', 'الشرق', 'العرب', 'Qatar Tribune', 'Gulf Times', 'The Peninsula', 'qatar', 'الوطن القطرية']
saudi_sources = ['العربية', 'الرياضية', 'عكاظ', 'الوطن', 'سبق', 'أرقام', 'argaam', 'saudi']
egypt_sources = ['اليوم السابع', 'المصري اليوم', 'الأهرام', 'الوطن', 'صدى البلد', 'بوابة الأهرام', 'مصراوي']
uae_sources = ['الإمارات اليوم', 'البيان', 'الاتحاد', 'الخليج', 'dubai', 'emirates']
international_sources = ['bbc', 'reuters', 'associated press', 'afp', 'cnn', 'sky', 'espn', 'goal', 'marca']

def classify_source(source_name):
    if pd.isna(source_name):
        return 'أخرى'
    source_lower = str(source_name).lower()
    
    for s in qatar_sources:
        if s.lower() in source_lower:
            return 'قطرية'
    for s in saudi_sources:
        if s.lower() in source_lower:
            return 'سعودية'
    for s in egypt_sources:
        if s.lower() in source_lower:
            return 'مصرية'
    for s in uae_sources:
        if s.lower() in source_lower:
            return 'إماراتية'
    for s in international_sources:
        if s.lower() in source_lower:
            return 'دولية'
    return 'أخرى'

traditional_df['Source Category'] = traditional_df['Source Name'].apply(classify_source)
source_cat_counts = traditional_df['Source Category'].value_counts()
print("\nتوزيع المصادر حسب الفئة:")
for cat, count in source_cat_counts.items():
    pct = (count / len(traditional_df)) * 100
    print(f"  - {cat}: {count} ({pct:.1f}%)")

# تحليل Sentiment حسب المصدر
print("\n" + "="*80)
print("😊 تحليل النبرة حسب المصادر الرئيسية")
print("="*80)

top_sources = source_counts.head(10).index.tolist()
for source in top_sources:
    source_df = traditional_df[traditional_df['Source Name'] == source]
    sentiments = source_df['Sentiment'].value_counts()
    total = len(source_df)
    
    positive = sentiments.get('Positive', 0)
    neutral = sentiments.get('Neutral', 0)
    negative = sentiments.get('Negative', 0)
    
    print(f"\n📌 {source} ({total} خبر):")
    print(f"    إيجابي: {positive} ({(positive/total*100):.1f}%)")
    print(f"    محايد: {neutral} ({(neutral/total*100):.1f}%)")
    print(f"    سلبي: {negative} ({(negative/total*100):.1f}%)")

# تحليل حسب الفعاليات
print("\n" + "="*80)
print("🏆 المصادر الأكثر تغطية لكل فعالية")
print("="*80)

events = {
    'كأس العرب 2025': r'كأس العرب|كاس العرب|arab cup|خليجي 26|gulf cup|كأس الخليج',
    'FIFA U-17': r'تحت 17|U-17|U17|كأس العالم للناشئين|under.?17|ناشئين',
    'F1 قطر': r'فورمولا|formula|F1|سباق|جائزة قطر الكبرى|grand prix|لوسيل|losail',
    'UFC Qatar': r'UFC|يو إف سي|فنون قتالية|مختلطة|MMA',
    'World Padel': r'بادل|padel|مضرب'
}

for event_name, event_pattern in events.items():
    event_df = traditional_df[
        traditional_df['Title'].str.contains(event_pattern, case=False, na=False) | 
        traditional_df['Hit Sentence'].str.contains(event_pattern, case=False, na=False)
    ]
    
    if len(event_df) > 0:
        print(f"\n📌 {event_name} ({len(event_df)} خبر):")
        top_event_sources = event_df['Source Name'].value_counts().head(5)
        for source, count in top_event_sources.items():
            print(f"    - {source}: {count}")

# ملخص للشريحة 30
print("\n" + "="*80)
print("📋 ملخص للشريحة 30 - المؤثرون في الصورة الإعلامية")
print("="*80)
print(f"""
إجمالي التغطيات: {len(traditional_df):,}

أبرز المصادر الإخبارية:
""")
for i, (source, count) in enumerate(source_counts.head(6).items(), 1):
    pct = (count / len(traditional_df)) * 100
    print(f"{i}. {source}: {count:,} ({pct:.1f}%)")

# تحليل Reach للمصادر
print("\n" + "="*80)
print("📈 المصادر الأعلى وصولاً (Reach)")
print("="*80)

source_reach = traditional_df.groupby('Source Name')['Reach'].sum().sort_values(ascending=False).head(10)
total_reach = traditional_df['Reach'].sum()
print(f"\nإجمالي الوصول: {total_reach:,.0f}")
print("\nأعلى 10 مصادر وصولاً:")
for source, reach in source_reach.items():
    pct = (reach / total_reach) * 100
    print(f"  - {source}: {reach:,.0f} ({pct:.1f}%)")
