#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract data for Heritage Events slides 36-45
"""

import pandas as pd
from datetime import datetime

# Load the main data file
file_path = "static/data/meltwater/Qatr/الفعاليات التراثية والوطنية/Overview/_____authoralgannas_qa_OR_authormawaterqatar_OR_au - Jan 19, 2026 - 10 27 26 AM.csv"

df = pd.read_csv(file_path, sep='\t', encoding='utf-16')

# Filter for online news only
news_df = df[df['Source Type'] == 'online news'].copy()

print(f"Total records: {len(df)}")
print(f"Online news records: {len(news_df)}")

# Convert date
news_df['Date'] = pd.to_datetime(news_df['Date'])

# Weekly distribution
news_df['Week'] = news_df['Date'].dt.isocalendar().week
news_df['Year'] = news_df['Date'].dt.year

# Group by week
weekly = news_df.groupby(['Year', 'Week']).size().reset_index(name='Count')
print("\n=== WEEKLY DISTRIBUTION ===")
for _, row in weekly.iterrows():
    print(f"Year {row['Year']} Week {row['Week']}: {row['Count']}")

# Top 3 weeks
top_weeks = weekly.nlargest(3, 'Count')
print("\n=== TOP 3 WEEKS ===")
for _, row in top_weeks.iterrows():
    print(f"Week {row['Week']}: {row['Count']}")

# Sentiment distribution
print("\n=== SENTIMENT ===")
sentiment = news_df['Sentiment'].value_counts()
print(sentiment)

# Country distribution
print("\n=== COUNTRY ===")
country = news_df['Country'].value_counts().head(10)
print(country)

# Language distribution
print("\n=== LANGUAGE ===")
language = news_df['Language'].value_counts()
print(language)

# Source distribution
print("\n=== TOP SOURCES ===")
sources = news_df['Source Name'].value_counts().head(10)
print(sources)

# Get positive articles with highest reach
print("\n=== TOP POSITIVE ARTICLES ===")
positive_df = news_df[news_df['Sentiment'] == 'positive'].copy()
positive_df['Reach'] = pd.to_numeric(positive_df['Reach'], errors='coerce')
top_positive = positive_df.nlargest(10, 'Reach')[['Date', 'Source Name', 'Headline', 'URL', 'Reach']]
for i, row in top_positive.iterrows():
    print(f"\n--- Article {i} ---")
    print(f"Date: {row['Date']}")
    print(f"Source: {row['Source Name']}")
    headline = row['Headline'][:100] if pd.notna(row['Headline']) else 'N/A'
    print(f"Headline: {headline}")
    print(f"URL: {row['URL']}")
    print(f"Reach: {row['Reach']}")
