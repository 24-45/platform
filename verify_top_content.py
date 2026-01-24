#!/usr/bin/env python3
"""
استخراج المحتوى الأكثر تفاعلاً الحقيقي من ملفات Meltwater
"""

import os
import pandas as pd
from pathlib import Path

BASE_PATH = Path("static/data/meltwater/qatr 4")

def read_meltwater_csv(file_path):
    """قراءة ملف CSV من Meltwater"""
    encodings = ['utf-16', 'utf-8', 'utf-8-sig', 'latin-1']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, sep='\t')
            if len(df.columns) > 5:
                return df
        except:
            pass
        
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            if len(df.columns) > 5:
                return df
        except:
            pass
    
    return None

def get_event_name(file_path):
    """استخراج اسم الحدث من مسار الملف"""
    path_str = str(file_path)
    
    if "كأس العرب" in path_str:
        return "كأس العرب 2025"
    elif "UFC" in path_str:
        return "UFC قطر"
    elif "فورمولا" in path_str or "Grand Prix" in path_str:
        return "F1 قطر"
    elif "U-17" in path_str or "تحت 17" in path_str:
        return "كأس العالم U-17"
    elif "WTT" in path_str:
        return "WTT تنس الطاولة"
    elif "T100" in path_str or "الترايثلون" in path_str:
        return "نهائي الترايثلون"
    elif "Intercontinental" in path_str or "القارات" in path_str:
        return "كأس القارات FIFA"
    elif "وزارة" in path_str:
        return "وزارة الرياضة"
    else:
        return "غير معروف"

def extract_top_content():
    """استخراج أعلى المحتويات تفاعلاً"""
    
    all_content = []
    
    # البحث في جميع ملفات CSV
    for csv_file in BASE_PATH.rglob("*.csv"):
        event_name = get_event_name(csv_file)
        folder_type = "overview" if "overview" in str(csv_file) else "X insights" if "X insights" in str(csv_file) else "other"
        
        df = read_meltwater_csv(csv_file)
        if df is None:
            continue
        
        print(f"\n{'='*60}")
        print(f"📁 {csv_file.name[:50]}...")
        print(f"📌 الحدث: {event_name}")
        print(f"📂 النوع: {folder_type}")
        print(f"📊 الأعمدة: {list(df.columns)[:10]}")
        print(f"📈 عدد الصفوف: {len(df)}")
        
        # البحث عن أعمدة التفاعل
        engagement_cols = [col for col in df.columns if any(x in col.lower() for x in ['engagement', 'reach', 'impression', 'like', 'retweet', 'share', 'view'])]
        if engagement_cols:
            print(f"📊 أعمدة التفاعل: {engagement_cols}")
        
        # البحث عن أعمدة النص/المحتوى
        text_cols = [col for col in df.columns if any(x in col.lower() for x in ['hit sentence', 'title', 'text', 'content', 'headline'])]
        if text_cols:
            print(f"📝 أعمدة النص: {text_cols}")
        
        # محاولة العثور على أعلى محتوى
        for eng_col in engagement_cols:
            try:
                df[eng_col] = pd.to_numeric(df[eng_col].astype(str).str.replace(',', ''), errors='coerce')
                top_rows = df.nlargest(3, eng_col)
                
                for _, row in top_rows.iterrows():
                    content_text = ""
                    for text_col in text_cols:
                        if text_col in row and pd.notna(row[text_col]):
                            content_text = str(row[text_col])[:200]
                            break
                    
                    if not content_text:
                        for col in df.columns:
                            if pd.notna(row[col]) and isinstance(row[col], str) and len(str(row[col])) > 50:
                                content_text = str(row[col])[:200]
                                break
                    
                    engagement_value = row[eng_col] if pd.notna(row[eng_col]) else 0
                    
                    # البحث عن Reach
                    reach_value = 0
                    for col in df.columns:
                        if 'reach' in col.lower():
                            if pd.notna(row[col]):
                                try:
                                    reach_value = float(str(row[col]).replace(',', ''))
                                except:
                                    pass
                    
                    all_content.append({
                        'event': event_name,
                        'folder': folder_type,
                        'engagement': engagement_value,
                        'reach': reach_value,
                        'text': content_text,
                        'eng_col': eng_col,
                        'source': csv_file.name[:30]
                    })
            except Exception as e:
                pass
    
    # ترتيب حسب التفاعل
    all_content.sort(key=lambda x: x['engagement'], reverse=True)
    
    print("\n" + "="*80)
    print("🏆 أعلى 20 محتوى تفاعلاً:")
    print("="*80)
    
    seen_texts = set()
    rank = 1
    for item in all_content[:50]:
        # تجنب التكرار
        text_key = item['text'][:50] if item['text'] else ""
        if text_key in seen_texts:
            continue
        seen_texts.add(text_key)
        
        if rank > 20:
            break
            
        print(f"\n🥇 المركز {rank}:")
        print(f"   الحدث: {item['event']}")
        print(f"   التفاعل: {item['engagement']:,.0f}")
        print(f"   الوصول: {item['reach']:,.0f}")
        print(f"   العمود: {item['eng_col']}")
        print(f"   المحتوى: {item['text'][:100]}...")
        
        rank += 1
    
    return all_content

if __name__ == "__main__":
    extract_top_content()
