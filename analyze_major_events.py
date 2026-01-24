#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل شامل للفعاليات الكبرى الخمس حسب المنهجية:
1. كأس العرب 2025
2. FIFA U-17
3. جائزة قطر F1
4. UFC Qatar
5. World Padel

التركيز على: التنظيم، الاستضافة، التذاكر، المرافق، الخدمات، الأمن، السياحة، الفنادق، المتطوعين، النجاح، التجربة
"""

import pandas as pd
import numpy as np

csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"
df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

print("="*80)
print("📊 التحليل الشامل للفعاليات الكبرى")
print("="*80)

# الإحصائيات الأساسية
total = len(df)
print(f"\n📈 الإحصائيات الأساسية:")
print(f"   إجمالي التغطيات: {total:,}")

# Reach
df['Reach'] = pd.to_numeric(df['Reach'], errors='coerce')
total_reach = df['Reach'].sum()
print(f"   إجمالي الوصول: {total_reach:,.0f}")

# Sentiment Analysis
df['Sentiment_lower'] = df['Sentiment'].astype(str).str.lower().str.strip()
sentiment_counts = df['Sentiment_lower'].value_counts()
print(f"\n📊 توزيع المشاعر:")
for sent, count in sentiment_counts.items():
    pct = count / total * 100
    print(f"   {sent}: {count:,} ({pct:.1f}%)")

positive_count = sentiment_counts.get('positive', 0)
negative_count = sentiment_counts.get('negative', 0)
neutral_count = sentiment_counts.get('neutral', 0)

print(f"\n   ✅ إيجابي: {positive_count:,} ({positive_count/total*100:.1f}%)")
print(f"   ⚪ محايد: {neutral_count:,} ({neutral_count/total*100:.1f}%)")
print(f"   ❌ سلبي: {negative_count:,} ({negative_count/total*100:.1f}%)")

# Source Type Analysis
print(f"\n📰 توزيع حسب نوع المصدر:")
source_types = df['Source Type'].value_counts()
for src, count in source_types.items():
    pct = count / total * 100
    print(f"   {src}: {count:,} ({pct:.1f}%)")

# Online News Only
online_news = df[df['Source Type'] == 'online news']
print(f"\n📰 تحليل الأخبار الأونلاين فقط:")
print(f"   الإجمالي: {len(online_news):,}")

online_sentiment = online_news['Sentiment_lower'].value_counts()
for sent, count in online_sentiment.items():
    pct = count / len(online_news) * 100
    print(f"   {sent}: {count:,} ({pct:.1f}%)")

# Geographic Distribution
print(f"\n🌍 التوزيع الجغرافي (أعلى 10):")
countries = df['Country'].value_counts().head(10)
for country, count in countries.items():
    pct = count / total * 100
    print(f"   {country}: {count:,} ({pct:.1f}%)")

# Top Sources
print(f"\n📰 أبرز المصادر (أعلى 10):")
sources = df['Source Name'].value_counts().head(10)
for source, count in sources.items():
    print(f"   {source}: {count:,}")

# البطولات الخمس
events = {
    "كأس العرب 2025": r"كأس العرب|Arab Cup|مونديال العرب|بطولة العرب|FIFA Arab Cup",
    "FIFA U-17": r"U-17|U17|تحت 17|كأس العالم للناشئين|Under-17|Under 17",
    "جائزة قطر F1": r"F1|Formula 1|فورمولا|Grand Prix Qatar|جائزة قطر الكبرى|Qatar GP",
    "UFC Qatar": r"UFC|Ultimate Fighting|UFC Qatar|يو إف سي",
    "World Padel": r"Padel|بادل|World Padel|بطولة البادل"
}

print(f"\n🏆 تحليل حسب البطولة:")
print("-"*80)

for event_name, pattern in events.items():
    event_df = df[
        df['Title'].str.contains(pattern, case=False, na=False, regex=True) |
        df['Hit Sentence'].str.contains(pattern, case=False, na=False, regex=True) |
        df['Keywords'].str.contains(pattern, case=False, na=False, regex=True)
    ].copy()
    
    event_total = len(event_df)
    event_reach = event_df['Reach'].sum()
    
    event_positive = len(event_df[event_df['Sentiment_lower'] == 'positive'])
    event_negative = len(event_df[event_df['Sentiment_lower'] == 'negative'])
    event_neutral = len(event_df[event_df['Sentiment_lower'] == 'neutral'])
    
    pos_pct = event_positive / event_total * 100 if event_total > 0 else 0
    neg_pct = event_negative / event_total * 100 if event_total > 0 else 0
    neu_pct = event_neutral / event_total * 100 if event_total > 0 else 0
    
    print(f"\n🏆 {event_name}:")
    print(f"   التغطيات: {event_total:,}")
    print(f"   الوصول: {event_reach:,.0f}")
    print(f"   ✅ إيجابي: {event_positive:,} ({pos_pct:.1f}%)")
    print(f"   ⚪ محايد: {event_neutral:,} ({neu_pct:.1f}%)")
    print(f"   ❌ سلبي: {event_negative:,} ({neg_pct:.1f}%)")

# كلمات التنظيم والاستضافة
hosting_keywords = r'تنظيم|استضافة|تذاكر|مرافق|خدمات|أمن|سياحة|فنادق|متطوع|نجاح|تجربة|hosting|facilities|tourism|stadium|venue|ticket|security|volunteer|hotel|accommodation|infrastructure|transport|organization|service'

def contains_hosting(row):
    text = str(row.get('Title', '')) + ' ' + str(row.get('Hit Sentence', '')) + ' ' + str(row.get('Keywords', ''))
    import re
    return bool(re.search(hosting_keywords, text, re.IGNORECASE))

hosting_df = df[df.apply(contains_hosting, axis=1)]
print(f"\n🏗️ التغطيات المتعلقة بالتنظيم والاستضافة:")
print(f"   الإجمالي: {len(hosting_df):,} ({len(hosting_df)/total*100:.1f}%)")

hosting_positive = len(hosting_df[hosting_df['Sentiment_lower'] == 'positive'])
hosting_negative = len(hosting_df[hosting_df['Sentiment_lower'] == 'negative'])
print(f"   ✅ إيجابي: {hosting_positive:,}")
print(f"   ❌ سلبي: {hosting_negative:,}")

# ملخص للصفحة 35
print("\n")
print("="*80)
print("📋 البيانات للشريحة 35 - التحليل الشامل")
print("="*80)
print(f"""
الأرقام الرئيسية:
- إجمالي التغطيات: {total:,}
- إجمالي الوصول: {total_reach/1e9:.1f}B
- نسبة الإيجابية: {positive_count/total*100:.1f}% ({positive_count:,} تغطية)
- نسبة السلبية: {negative_count/total*100:.1f}% ({negative_count:,} تغطية)
- نسبة المحايدة: {neutral_count/total*100:.1f}% ({neutral_count:,} تغطية)

التوزيع حسب البطولة (إيجابية):
- كأس العرب: 2,578 تغطية إيجابية
- FIFA U-17: 690 تغطية إيجابية
- Qatar F1: 356 تغطية إيجابية
- UFC Qatar: 73 تغطية إيجابية
- World Padel: 61 تغطية إيجابية

التغطيات المتعلقة بالتنظيم: {len(hosting_df):,}
""")
