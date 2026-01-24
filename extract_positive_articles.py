#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استخراج أبرز التغطيات الإيجابية للتحقق من المنهجية
"""

import pandas as pd

csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"
df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# فلترة الإيجابية من online news
positive_df = df[(df['Sentiment'].str.lower() == 'positive') & (df['Source Type'] == 'online news')].copy()

print(f"إجمالي التغطيات الإيجابية: {len(positive_df)}")
print()

# ترتيب حسب الوصول
if 'Reach' in positive_df.columns:
    positive_df['Reach'] = pd.to_numeric(positive_df['Reach'], errors='coerce')
    top_15 = positive_df.nlargest(15, 'Reach')[['Title', 'Source Name', 'Date', 'Reach', 'URL']]
    
    print("="*80)
    print("أبرز 15 تغطية إيجابية (حسب الوصول):")
    print("="*80)
    
    for idx, (i, row) in enumerate(top_15.iterrows(), 1):
        title = str(row['Title'])[:70] if pd.notna(row['Title']) else 'N/A'
        source = str(row['Source Name']) if pd.notna(row['Source Name']) else 'N/A'
        date = str(row['Date']) if pd.notna(row['Date']) else 'N/A'
        reach = row['Reach'] if pd.notna(row['Reach']) else 0
        url = str(row['URL'])[:100] if pd.notna(row['URL']) else 'N/A'
        
        print(f"\n{idx}. {title}")
        print(f"   📰 {source} | 📅 {date} | 👁️ {reach:,.0f}")
        print(f"   🔗 {url}")

print("\n" + "="*80)
print("تحليل المصادر:")
print("="*80)

source_counts = positive_df['Source Name'].value_counts().head(10)
for source, count in source_counts.items():
    print(f"  {source}: {count} مقال")
