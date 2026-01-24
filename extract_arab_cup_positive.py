#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استخراج التغطيات الإيجابية المتعلقة بكأس العرب
"""

import pandas as pd
import re

csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"
df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# فلترة الإيجابية من online news
positive_df = df[(df['Sentiment'].str.lower() == 'positive') & (df['Source Type'] == 'online news')].copy()

# البحث عن كأس العرب
arab_cup_pattern = r'كأس العرب|Arab Cup|مونديال العرب|بطولة العرب'
arab_cup_df = positive_df[
    positive_df['Title'].str.contains(arab_cup_pattern, case=False, na=False, regex=True) |
    positive_df['Hit Sentence'].str.contains(arab_cup_pattern, case=False, na=False, regex=True)
].copy()

arab_cup_df['Reach'] = pd.to_numeric(arab_cup_df['Reach'], errors='coerce')

print(f"إجمالي التغطيات الإيجابية عن كأس العرب: {len(arab_cup_df)}")
print()

top_20 = arab_cup_df.nlargest(20, 'Reach')[['Title', 'Source Name', 'Date', 'Reach', 'URL']]

print("="*80)
print("أبرز 20 تغطية إيجابية عن كأس العرب:")
print("="*80)

for idx, (i, row) in enumerate(top_20.iterrows(), 1):
    title = str(row['Title'])[:80] if pd.notna(row['Title']) else 'N/A'
    source = str(row['Source Name']) if pd.notna(row['Source Name']) else 'N/A'
    date = str(row['Date']) if pd.notna(row['Date']) else 'N/A'
    reach = row['Reach'] if pd.notna(row['Reach']) else 0
    url = str(row['URL']) if pd.notna(row['URL']) else 'N/A'
    
    print(f"\n{idx}. {title}")
    print(f"   📰 {source}")
    print(f"   📅 {date} | 👁️ {reach:,.0f}")
    print(f"   🔗 {url}")

# التغطيات الدولية
print("\n" + "="*80)
print("التغطيات الدولية الكبرى:")
print("="*80)

intl_sources = ['Al Jazeera', 'Reuters', 'Goal.com', 'Yahoo', 'BBC', 'ESPN', 'Sky Sports', 'Goal']
intl_df = arab_cup_df[arab_cup_df['Source Name'].str.contains('|'.join(intl_sources), case=False, na=False)]

for idx, (i, row) in enumerate(intl_df.nlargest(10, 'Reach').iterrows(), 1):
    title = str(row['Title'])[:70] if pd.notna(row['Title']) else 'N/A'
    source = str(row['Source Name']) if pd.notna(row['Source Name']) else 'N/A'
    reach = row['Reach'] if pd.notna(row['Reach']) else 0
    url = str(row['URL']) if pd.notna(row['URL']) else 'N/A'
    
    print(f"\n{idx}. {source}: {title}")
    print(f"   👁️ {reach:,.0f}")
    print(f"   🔗 {url}")
