#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
from pathlib import Path

# Read one file to test
filepath = '/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr 4/الأحداث/كأس القارات FIFA/overview/FIFA_Intercontinental_Cup_OR_Intercontinental_Cup_ - Jan 22, 2026 - 6 03 30 PM.csv'

df = pd.read_csv(filepath, encoding='utf-16', sep='\t', on_bad_lines='skip', low_memory=False)

# Search for organization keywords
keywords = ['organiz', 'host', 'amazing', 'incredible', 'outstanding', 'excellent', 'best ever', 'world class', 'qatar did', 'qatar is', 'تنظيم', 'استضافة', 'رائع', 'مبهر']

count = 0
for idx, row in df.iterrows():
    text = str(row.get('Hit Sentence', '')).lower()
    for kw in keywords:
        if kw.lower() in text:
            print(f'Found: {kw}')
            print(f'Text: {text[:300]}...')
            print(f'Engagement: {row.get("Engagement", 0)}')
            print('-' * 50)
            count += 1
            if count >= 5:
                break
    if count >= 5:
        break

print(f'\nTotal matches shown: {count}')
