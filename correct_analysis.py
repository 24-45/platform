#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
التحليل الصحيح للفعاليات الكبرى - الأخبار الأونلاين فقط
حسب المنهجية: Source Type = 'online news'
"""

import pandas as pd

csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"
df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# الأخبار الأونلاين فقط - حسب المنهجية
online_news = df[df['Source Type'] == 'online news'].copy()

print("="*80)
print("📊 التحليل الصحيح - الأخبار الأونلاين فقط")
print("="*80)

total = len(online_news)
print(f"\n📈 إجمالي التغطية الإعلامية (أخبار أونلاين): {total:,}")

online_news['Reach'] = pd.to_numeric(online_news['Reach'], errors='coerce')
total_reach = online_news['Reach'].sum()
print(f"   الوصول التراكمي: {total_reach:,.0f} ({total_reach/1e9:.1f}B)")

online_news['Sentiment_lower'] = online_news['Sentiment'].astype(str).str.lower().str.strip()
sentiment_counts = online_news['Sentiment_lower'].value_counts()

positive_count = sentiment_counts.get('positive', 0)
negative_count = sentiment_counts.get('negative', 0)
neutral_count = sentiment_counts.get('neutral', 0)

print(f"\n📊 توزيع المشاعر:")
print(f"   ✅ إيجابي: {positive_count:,} ({positive_count/total*100:.1f}%)")
print(f"   ⚪ محايد: {neutral_count:,} ({neutral_count/total*100:.1f}%)")
print(f"   ❌ سلبي: {negative_count:,} ({negative_count/total*100:.1f}%)")

# البطولات الخمس - أخبار أونلاين فقط
events = {
    "كأس العرب 2025": r"كأس العرب|Arab Cup|مونديال العرب|بطولة العرب|FIFA Arab Cup",
    "FIFA U-17": r"U-17|U17|تحت 17|كأس العالم للناشئين|Under-17|Under 17",
    "جائزة قطر F1": r"F1|Formula 1|فورمولا|Grand Prix Qatar|جائزة قطر الكبرى|Qatar GP",
    "UFC Qatar": r"UFC|Ultimate Fighting|UFC Qatar|يو إف سي",
    "World Padel": r"Padel|بادل|World Padel|بطولة البادل"
}

print(f"\n🏆 تحليل الفعاليات الخمس (أخبار أونلاين فقط):")
print("-"*80)

for event_name, pattern in events.items():
    event_df = online_news[
        online_news['Title'].str.contains(pattern, case=False, na=False, regex=True) |
        online_news['Hit Sentence'].str.contains(pattern, case=False, na=False, regex=True) |
        online_news['Keywords'].str.contains(pattern, case=False, na=False, regex=True)
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
    print(f"   الوصول: {event_reach:,.0f} ({event_reach/1e9:.2f}B)")
    print(f"   ✅ إيجابي: {event_positive:,} ({pos_pct:.1f}%)")
    print(f"   ⚪ محايد: {event_neutral:,} ({neu_pct:.1f}%)")
    print(f"   ❌ سلبي: {event_negative:,} ({neg_pct:.1f}%)")

# التوزيع الجغرافي
print(f"\n🌍 التوزيع الجغرافي (أعلى 10):")
countries = online_news['Country'].value_counts().head(10)
for country, count in countries.items():
    pct = count / total * 100
    print(f"   {country}: {count:,} ({pct:.1f}%)")

# ملخص للشريحة 35
print("\n")
print("="*80)
print("📋 الأرقام الصحيحة للشريحة 35")
print("="*80)
print(f"""
✅ الأرقام المعتمدة (أخبار أونلاين فقط):
- إجمالي التغطيات: {total:,}
- الوصول التراكمي: {total_reach/1e9:.1f}B
- الإيجابية: {positive_count/total*100:.1f}% ({positive_count:,})
- السلبية: {negative_count/total*100:.1f}% ({negative_count:,})
- المحايد: {neutral_count/total*100:.1f}% ({neutral_count:,})
""")
