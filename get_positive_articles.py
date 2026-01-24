#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

file_path = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/Qatr/الفعاليات التراثية والوطنية/Overview/_____authoralgannas_qa_OR_authormawaterqatar_OR_au - Jan 19, 2026 - 10 27 26 AM.csv"

df = pd.read_csv(file_path, sep='\t', encoding='utf-16')
news_df = df[df['Source Type'] == 'online news'].copy()

# Get positive articles with highest reach
positive_df = news_df[news_df['Sentiment'] == 'positive'].copy()
positive_df['Reach'] = pd.to_numeric(positive_df['Reach'], errors='coerce')
top_positive = positive_df.nlargest(10, 'Reach')[['Date', 'Source Name', 'Title', 'URL', 'Reach']]

print("=== TOP 10 POSITIVE ARTICLES ===")
for idx, (i, row) in enumerate(top_positive.iterrows()):
    print(f"\n--- Article {idx+1} ---")
    print(f"Date: {row['Date']}")
    print(f"Source: {row['Source Name']}")
    title = str(row['Title'])[:150] if pd.notna(row['Title']) else 'N/A'
    print(f"Title: {title}")
    print(f"URL: {row['URL']}")
    print(f"Reach: {row['Reach']}")
