#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استخراج أعلى 6 محتويات تفاعلاً من ملفات Meltwater
"""

import os
import csv
import json
from pathlib import Path

def get_event_name(file_path):
    """استخراج اسم الحدث من مسار الملف"""
    path_parts = file_path.split(os.sep)
    full_path = file_path.lower()
    
    # البحث عن اسم الحدث في المسار الكامل
    if 'فورمولا' in file_path or 'grand prix' in full_path or 'formula' in full_path or 'f1' in full_path.split('/'):
        return 'Formula 1 - جائزة قطر الكبرى'
    elif 'كأس العرب' in file_path or 'arab cup' in full_path or 'arab_cup' in full_path:
        return 'FIFA Arab Cup - كأس العرب'
    elif 'ufc' in full_path:
        return 'UFC Qatar'
    elif 'wtt' in full_path or 'تنس الطاولة' in file_path:
        return 'WTT - تنس الطاولة'
    elif 'كأس القارات' in file_path or 'intercontinental' in full_path:
        return 'FIFA Intercontinental Cup - كأس القارات'
    elif 'u-17' in full_path or 'u17' in full_path or 'تحت 17' in file_path:
        return 'FIFA U-17 World Cup'
    elif 't100' in full_path or 'ترايثلون' in file_path or 'triathlon' in full_path:
        return 'T100 Triathlon - ترايثلون'
    elif 'وزارة الرياضة' in file_path:
        return 'وزارة الرياضة والشباب'
    
    return 'غير محدد'

def parse_number(value):
    """تحويل النص إلى رقم"""
    if not value or value.strip() == '':
        return 0
    try:
        # إزالة الفواصل والمسافات
        clean_value = value.strip().replace(',', '').replace(' ', '')
        return int(float(clean_value))
    except:
        return 0

def read_meltwater_csv(file_path):
    """قراءة ملف Meltwater CSV بتشفير UTF-16"""
    records = []
    event_name = get_event_name(file_path)
    
    try:
        # محاولة قراءة الملف بتشفير UTF-16
        with open(file_path, 'r', encoding='utf-16') as f:
            content = f.read()
    except:
        try:
            with open(file_path, 'r', encoding='utf-16-le') as f:
                content = f.read()
        except:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"خطأ في قراءة الملف: {file_path}: {e}")
                return []
    
    lines = content.strip().split('\n')
    if len(lines) < 2:
        return []
    
    # تحليل الهيدر
    header = lines[0].split('\t')
    header = [h.strip() for h in header]
    
    # إنشاء قاموس للأعمدة
    col_index = {name: i for i, name in enumerate(header)}
    
    # الأعمدة المطلوبة
    url_col = col_index.get('URL', -1)
    author_name_col = col_index.get('Author Name', -1)
    author_handle_col = col_index.get('Author Handle', -1)
    hit_sentence_col = col_index.get('Hit Sentence', -1)
    opening_text_col = col_index.get('Opening Text', -1)
    engagement_col = col_index.get('Engagement', -1)
    reach_col = col_index.get('Reach', -1)
    likes_col = col_index.get('Likes', -1)
    shares_col = col_index.get('Shares', -1)
    reposts_col = col_index.get('Reposts', -1)
    views_col = col_index.get('Views', -1)
    estimated_views_col = col_index.get('Estimated Views', -1)
    date_col = col_index.get('Date', -1)
    
    for line in lines[1:]:
        if not line.strip():
            continue
        
        fields = line.split('\t')
        
        try:
            # استخراج القيم
            url = fields[url_col] if url_col >= 0 and url_col < len(fields) else ''
            author_name = fields[author_name_col] if author_name_col >= 0 and author_name_col < len(fields) else ''
            author_handle = fields[author_handle_col] if author_handle_col >= 0 and author_handle_col < len(fields) else ''
            
            # النص - محاولة Hit Sentence أولاً ثم Opening Text
            text = ''
            if hit_sentence_col >= 0 and hit_sentence_col < len(fields):
                text = fields[hit_sentence_col]
            if not text and opening_text_col >= 0 and opening_text_col < len(fields):
                text = fields[opening_text_col]
            
            engagement = parse_number(fields[engagement_col]) if engagement_col >= 0 and engagement_col < len(fields) else 0
            reach = parse_number(fields[reach_col]) if reach_col >= 0 and reach_col < len(fields) else 0
            likes = parse_number(fields[likes_col]) if likes_col >= 0 and likes_col < len(fields) else 0
            
            # المشاركات - Shares أو Reposts
            shares = 0
            if shares_col >= 0 and shares_col < len(fields):
                shares = parse_number(fields[shares_col])
            if shares == 0 and reposts_col >= 0 and reposts_col < len(fields):
                shares = parse_number(fields[reposts_col])
            
            # المشاهدات - Views أو Estimated Views
            views = 0
            if views_col >= 0 and views_col < len(fields):
                views = parse_number(fields[views_col])
            if views == 0 and estimated_views_col >= 0 and estimated_views_col < len(fields):
                views = parse_number(fields[estimated_views_col])
            
            date = fields[date_col] if date_col >= 0 and date_col < len(fields) else ''
            
            # تخطي السجلات بدون تفاعل
            if engagement == 0:
                continue
            
            # تنظيف URL
            url = url.strip().strip('"').replace('""', '"')
            
            record = {
                'url': url,
                'author_name': author_name.strip(),
                'author_handle': author_handle.strip(),
                'text': text.strip()[:500],  # أول 500 حرف
                'engagement': engagement,
                'reach': reach,
                'likes': likes,
                'shares': shares,
                'views': views,
                'date': date.strip(),
                'event': event_name
            }
            
            records.append(record)
            
        except Exception as e:
            continue
    
    return records

def main():
    base_path = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr 4"
    
    all_records = []
    
    # البحث عن جميع ملفات X insights
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv') and 'X insights' in root:
                file_path = os.path.join(root, file)
                print(f"معالجة: {file[:50]}...")
                records = read_meltwater_csv(file_path)
                all_records.extend(records)
                print(f"  تم استخراج {len(records)} سجل")
    
    print(f"\n{'='*80}")
    print(f"إجمالي السجلات: {len(all_records)}")
    
    # ترتيب حسب Engagement
    all_records.sort(key=lambda x: x['engagement'], reverse=True)
    
    # أعلى 6
    top_6 = all_records[:6]
    
    print(f"\n{'='*80}")
    print("🏆 أعلى 6 محتويات تفاعلاً:")
    print(f"{'='*80}\n")
    
    for i, record in enumerate(top_6, 1):
        print(f"📊 المحتوى رقم {i}:")
        print(f"{'─'*60}")
        print(f"🎯 الحدث: {record['event']}")
        print(f"📅 التاريخ: {record['date']}")
        print(f"👤 اسم الناشر: {record['author_name']}")
        print(f"🔗 الهاندل: {record['author_handle']}")
        print(f"🌐 URL: {record['url']}")
        print(f"📝 النص: {record['text'][:200]}...")
        print(f"💬 التفاعل (Engagement): {record['engagement']:,}")
        print(f"📢 الوصول (Reach): {record['reach']:,}")
        print(f"❤️ الإعجابات (Likes): {record['likes']:,}")
        print(f"🔄 المشاركات (Shares/Reposts): {record['shares']:,}")
        print(f"👁️ المشاهدات (Views): {record['views']:,}")
        print(f"\n")
    
    # حفظ النتائج في JSON
    output_file = "/Users/taherirshaid/Desktop/Project/24-45-Platform/top_6_engagement.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(top_6, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم حفظ النتائج في: {output_file}")
    
    return top_6

if __name__ == "__main__":
    main()
