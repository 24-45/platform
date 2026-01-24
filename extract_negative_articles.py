#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استخراج التغطيات السلبية للبطولات الخمس:
1. كأس العرب 2025
2. FIFA U-17
3. جائزة قطر F1
4. UFC Qatar
5. World Padel
"""

import pandas as pd

csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"
df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# البطولات الخمس وكلماتها المفتاحية
events = {
    "كأس العرب 2025": r"كأس العرب|Arab Cup|مونديال العرب|بطولة العرب|FIFA Arab Cup",
    "FIFA U-17": r"U-17|U17|تحت 17|كأس العالم للناشئين|Under-17|Under 17",
    "جائزة قطر F1": r"F1|Formula 1|فورمولا|Grand Prix Qatar|جائزة قطر الكبرى|Qatar GP",
    "UFC Qatar": r"UFC|Ultimate Fighting|UFC Qatar|يو إف سي",
    "World Padel": r"Padel|بادل|World Padel|بطولة البادل"
}

# فلترة السلبية + online news
df['Sentiment_lower'] = df['Sentiment'].astype(str).str.lower().str.strip()
negative_online = df[(df['Sentiment_lower'] == 'negative') & (df['Source Type'] == 'online news')].copy()
negative_online['Reach'] = pd.to_numeric(negative_online['Reach'], errors='coerce')

print("="*80)
print("📊 استخراج التغطيات السلبية للبطولات الخمس")
print("="*80)

all_results = {}

for event_name, pattern in events.items():
    # البحث في Title و Hit Sentence و Keywords
    event_df = negative_online[
        negative_online['Title'].str.contains(pattern, case=False, na=False, regex=True) |
        negative_online['Hit Sentence'].str.contains(pattern, case=False, na=False, regex=True) |
        negative_online['Keywords'].str.contains(pattern, case=False, na=False, regex=True)
    ].copy()
    
    print(f"\n{'='*80}")
    print(f"🔴 {event_name}")
    print(f"{'='*80}")
    print(f"عدد التغطيات السلبية: {len(event_df)}")
    
    if len(event_df) > 0:
        top_5 = event_df.nlargest(5, 'Reach')
        
        print(f"\n📰 أبرز 5 تغطيات سلبية:")
        print("-"*60)
        
        for idx, (i, row) in enumerate(top_5.iterrows(), 1):
            title = str(row['Title'])[:70] if pd.notna(row['Title']) else 'N/A'
            source = str(row['Source Name']) if pd.notna(row['Source Name']) else 'N/A'
            reach = row['Reach'] if pd.notna(row['Reach']) else 0
            url = str(row['URL']) if pd.notna(row['URL']) else 'N/A'
            date = str(row['Date']) if pd.notna(row['Date']) else 'N/A'
            
            print(f"\n{idx}. {title}")
            print(f"   📰 {source} | 📅 {date} | 👁️ {reach:,.0f}")
            print(f"   🔗 {url}")
        
        all_results[event_name] = {
            'count': len(event_df),
            'top_articles': top_5[['Title', 'Source Name', 'Date', 'Reach', 'URL']].to_dict('records')
        }
    else:
        all_results[event_name] = {'count': 0, 'top_articles': []}

# ملخص
print("\n")
print("="*80)
print("📋 ملخص التغطيات السلبية لكل بطولة")
print("="*80)
print(f"{'البطولة':<30} {'عدد التغطيات':>15}")
print("-"*50)
for event, data in all_results.items():
    print(f"{event:<30} {data['count']:>15,}")
