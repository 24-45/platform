#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to extract tweets praising Qatar's organization and hosting
from Meltwater CSV files in qatr 4 folder
"""

import pandas as pd
import os
import re
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Base path for CSV files
base_path = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr 4"

# Keywords to search for organization/hosting praise
keywords = [
    # English keywords
    'organiz',
    'host',
    'amazing',
    'incredible',
    'outstanding',
    'excellent',
    'best ever',
    'world class',
    'world-class',
    'qatar did',
    'qatar is',
    'well done qatar',
    'congratulations qatar',
    'congrats qatar',
    'bravo qatar',
    'kudos qatar',
    'thank you qatar',
    'thanks qatar',
    'spectacular',
    'wonderful',
    'fantastic',
    'brilliant',
    'impressive',
    'stunning',
    'beautiful',
    'great event',
    'great job',
    'superb',
    'magnificent',
    'phenomenal',
    # Arabic keywords
    'استضافة',
    'تنظيم',
    'إشادة',
    'نجاح',
    'تميز',
    'رائع',
    'مبهر',
    'ممتاز',
    'عظيم',
    'مذهل',
    'احسنت قطر',
    'أحسنت قطر',
    'تبارك',
    'مبروك',
    'شكرا قطر',
    'شكراً قطر',
    'الف مبروك',
    'ألف مبروك',
    'احترافية',
    'منظم',
    'المنظمة',
    'قطر نموذج',
    'فخر',
]

def find_all_csv_files(base_path):
    """Find all CSV files in the directory tree"""
    csv_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def is_organization_praise(text):
    """Check if text contains organization/hosting praise"""
    if not isinstance(text, str):
        return False
    
    text_lower = text.lower()
    
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    
    return False

def extract_event_name(filepath):
    """Extract event name from file path"""
    if 'فورمولا' in filepath or 'Grand Prix' in filepath or 'F1' in filepath:
        return 'Formula 1 Qatar GP'
    elif 'UFC' in filepath:
        return 'UFC Qatar'
    elif 'العرب' in filepath or 'Arab Cup' in filepath:
        return 'FIFA Arab Cup 2025'
    elif 'U-17' in filepath or 'تحت 17' in filepath:
        return 'FIFA U-17 World Cup'
    elif 'القارات' in filepath or 'Intercontinental' in filepath:
        return 'FIFA Intercontinental Cup'
    elif 'T100' in filepath or 'الترايثلون' in filepath:
        return 'T100 Triathlon Finals'
    elif 'WTT' in filepath or 'تنس الطاولة' in filepath:
        return 'WTT Table Tennis'
    elif 'وزارة الرياضة' in filepath:
        return 'Ministry of Sports'
    elif 'بادل' in filepath or 'Padel' in filepath:
        return 'Padel World Cup'
    return 'Other Event'

def process_csv_file(filepath):
    """Process a single CSV file and extract relevant tweets"""
    try:
        # Try different encodings - UTF-16 first for Meltwater files
        df = None
        for encoding in ['utf-16', 'utf-16-le', 'utf-8', 'utf-8-sig', 'latin-1']:
            try:
                df = pd.read_csv(filepath, encoding=encoding, sep='\t', on_bad_lines='skip', low_memory=False)
                if len(df.columns) > 5:  # Valid parse
                    break
            except Exception as e:
                continue
        
        if df is None or len(df.columns) < 5:
            return []
        
        results = []
        event_name = extract_event_name(filepath)
        
        for idx, row in df.iterrows():
            text = row.get('Hit Sentence', '')
            if not isinstance(text, str):
                continue
            
            # Check if it's organization praise
            if is_organization_praise(text):
                engagement = 0
                views = 0
                
                if 'Engagement' in df.columns and pd.notna(row.get('Engagement')):
                    try:
                        engagement = int(float(str(row.get('Engagement', 0)).replace(',', '')))
                    except:
                        engagement = 0
                
                if 'Views' in df.columns and pd.notna(row.get('Views')):
                    try:
                        views = int(float(str(row.get('Views', 0)).replace(',', '')))
                    except:
                        views = 0
                
                author_name = row.get('Author Name', 'N/A')
                author_handle = row.get('Author Handle', 'N/A')
                url = row.get('URL', 'N/A')
                date = row.get('Date', 'N/A')
                source_type = row.get('Source Type', 'N/A')
                
                results.append({
                    'Event': event_name,
                    'Hit Sentence': text[:800],  # Truncate long texts
                    'Engagement': engagement,
                    'Views': views,
                    'Author Name': author_name if pd.notna(author_name) else 'N/A',
                    'Author Handle': author_handle if pd.notna(author_handle) else 'N/A',
                    'URL': url if pd.notna(url) else 'N/A',
                    'Date': date if pd.notna(date) else 'N/A',
                    'Source Type': source_type if pd.notna(source_type) else 'N/A',
                })
        
        return results
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def main():
    print("=" * 80)
    print("البحث عن التغريدات التي تشيد بالتنظيم القطري")
    print("Searching for tweets praising Qatar's organization")
    print("=" * 80)
    
    # Find all CSV files
    csv_files = find_all_csv_files(base_path)
    print(f"\nFound {len(csv_files)} CSV files to analyze\n")
    
    all_results = []
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)[:50]
        results = process_csv_file(filepath)
        all_results.extend(results)
        if results:
            print(f"✓ {filename}... → {len(results)} matches")
    
    print(f"\n{'=' * 80}")
    print(f"Total tweets found: {len(all_results)}")
    print(f"{'=' * 80}")
    
    if not all_results:
        print("\nNo matching tweets found.")
        return
    
    # Convert to DataFrame and sort by engagement
    df_results = pd.DataFrame(all_results)
    
    # Remove duplicates based on URL
    df_results = df_results.drop_duplicates(subset=['URL'])
    
    # Sort by engagement
    df_results = df_results.sort_values('Engagement', ascending=False)
    
    # Get top 10
    top_10 = df_results.head(10)
    
    print("\n" + "=" * 80)
    print("أعلى 10 تغريدات تفاعلاً تشيد بالتنظيم القطري")
    print("Top 10 Most Engaged Tweets Praising Qatar's Organization")
    print("=" * 80)
    
    for i, row in top_10.iterrows():
        print(f"\n{'─' * 80}")
        print(f"#{top_10.index.get_loc(i) + 1} - {row['Event']}")
        print(f"{'─' * 80}")
        print(f"📊 Engagement: {int(row['Engagement']):,} | 👁 Views: {int(row['Views']):,}")
        print(f"👤 Author: {row['Author Name']} (@{row['Author Handle']})")
        print(f"📅 Date: {row['Date']}")
        print(f"📌 Source: {row['Source Type']}")
        print(f"🔗 URL: {row['URL']}")
        print(f"\n📝 Content:")
        print(f"   {row['Hit Sentence']}")
    
    # Also save to CSV
    output_path = "/Users/taherirshaid/Desktop/Project/24-45-Platform/organization_praise_tweets.csv"
    df_results.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n\n✅ Full results saved to: {output_path}")
    
    # Print summary by event
    print("\n" + "=" * 80)
    print("ملخص حسب الحدث - Summary by Event")
    print("=" * 80)
    event_summary = df_results.groupby('Event').agg({
        'Engagement': ['count', 'sum', 'max']
    }).round(0)
    event_summary.columns = ['Count', 'Total Engagement', 'Max Engagement']
    print(event_summary.to_string())
    
    # Print top 10 again in a cleaner format for easy copying
    print("\n" + "=" * 80)
    print("النتائج بتنسيق مبسط للنسخ")
    print("=" * 80)
    for idx, (i, row) in enumerate(top_10.iterrows(), 1):
        print(f"\n{idx}. [{row['Event']}] Engagement: {int(row['Engagement']):,}")
        print(f"   Author: {row['Author Name']} (@{row['Author Handle']})")
        print(f"   Date: {row['Date']}")
        print(f"   URL: {row['URL']}")
        print(f"   Text: {str(row['Hit Sentence'])[:200]}...")

if __name__ == "__main__":
    main()
