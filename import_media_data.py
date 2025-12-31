#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت استيراد بيانات الأدوات الإعلامية من CSV
"""

import csv
import json
import re
from pathlib import Path

csv_file = "/Users/taherirshaid/Library/CloudStorage/GoogleDrive-taher.irshaid@gmail.com/ملفاتي/work/Resources/نوشن/ExportBlock-932a3536-c5b6-4f13-9a1b-b3b4072e01d6-Part-1/TREND PP#2 HQ/08e3e7d6824c412bbf910709fb520b79/TREND AD 44299ca6957041a4842de733f1195932_all.csv"

def parse_followers(value):
    """تحويل عدد المتابعين من نص إلى رقم"""
    if not value or str(value).strip() == '':
        return 0
    try:
        clean = str(value).replace(',', '').replace(' ', '').strip()
        return int(clean) if clean else 0
    except:
        return 0

def create_id(name):
    """إنشاء ID من الاسم"""
    if not name:
        return f"item_{abs(hash(str(name)))}"
    clean = re.sub(r'[^\w\s\u0600-\u06FF]', '', name.lower())
    clean = clean.replace(' ', '_')
    return clean[:50] if clean else f"item_{abs(hash(str(name)))}"

# قراءة CSV
data = {
    "database_info": {
        "name": "قاعدة البيانات الإعلامية - TREND AD",
        "version": "2.0",
        "last_updated": "2025-12-29",
        "source": "Notion Export - Complete Data"
    },
    "influencers": [],
    "newspapers": [],
    "news_accounts": [],
    "tv_channels": [],
    "radio_channels": [],
    "statistics": {}
}

print(f"📂 قراءة الملف: {csv_file}")

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"📊 عدد الصفوف: {len(rows)}")
    
    for i, row in enumerate(rows):
        name = row.get('Name', '').strip()
        if not name:
            continue
        
        # تحديد نوع الحساب
        account_type = row.get('نوع الحساب ', '').strip()
        category = row.get('التصنيفات', '').strip()
        
        # بناء الكائن الأساسي
        item = {
            "id": create_id(name),
            "name": name,
            "gender": row.get('الجنس', '').strip(),
            "country": row.get('الدولة', '').strip(),
            "city": row.get('المدينة', '').strip(),
            "continent": row.get('القارة', '').strip(),
            "sector": row.get('القطاع', '').strip(),
            "specializations": [s.strip() for s in row.get('المجال', '').split(',') if s.strip()],
            "description": row.get('الوصف', '').strip(),
            "website": row.get('الموقع الالكتروني', '').strip(),
            "contact": row.get('رقم التواصل', '').strip(),
            "category_tier": row.get('فئة الحساب', '').strip(),
            "relationship_level": row.get('مستوي العلاقة', '').strip(),
            "interaction_types": [t.strip() for t in row.get('نوع التفاعل', '').split(',') if t.strip()],
            "account_type": account_type,
            "categories": category,
            "image": row.get('Image', '').strip(),
            "regional_accounts": row.get('حسابات المناطق', '').strip(),
        }
        
        # إضافة المنصات
        platforms = {}
        total_followers = 0
        
        # Facebook
        fb_url = row.get('Facebook', '').strip()
        if fb_url:
            fb_followers = parse_followers(row.get('Facebook - Followers', ''))
            platforms['facebook'] = {"url": fb_url, "followers": fb_followers}
            total_followers += fb_followers
        
        # Instagram
        ig_url = row.get('Instagram', '').strip()
        if ig_url:
            ig_followers = parse_followers(row.get('Instagram - Followers', ''))
            platforms['instagram'] = {"url": ig_url, "followers": ig_followers}
            total_followers += ig_followers
        
        # Twitter/X
        x_url = row.get('X', '').strip()
        if x_url:
            x_followers = parse_followers(row.get('X - Followers', ''))
            platforms['twitter'] = {"url": x_url, "followers": x_followers}
            total_followers += x_followers
        
        # TikTok
        tt_url = row.get('Tik Tok', '').strip()
        if tt_url:
            tt_followers = parse_followers(row.get('Tik Tok - Followers', ''))
            platforms['tiktok'] = {"url": tt_url, "followers": tt_followers}
            total_followers += tt_followers
        
        # Snapchat
        snap_url = row.get('Snapchat', '').strip()
        if snap_url:
            snap_followers = parse_followers(row.get('Snapchat - Followers', ''))
            platforms['snapchat'] = {"url": snap_url, "followers": snap_followers}
            total_followers += snap_followers
        
        # YouTube
        yt_url = row.get('YouTube', '').strip()
        if yt_url:
            yt_followers = parse_followers(row.get('YouTube - Followers', ''))
            platforms['youtube'] = {"url": yt_url, "followers": yt_followers}
            total_followers += yt_followers
        
        # LinkedIn
        li_url = row.get('LinkedIn', '').strip()
        if li_url:
            li_followers = parse_followers(row.get('LinkedIn - Followers', ''))
            platforms['linkedin'] = {"url": li_url, "followers": li_followers}
            total_followers += li_followers
        
        item['platforms'] = platforms
        item['total_followers'] = total_followers
        
        # تصنيف حسب النوع
        category_lower = category.lower() if category else ''
        
        # تحديد التصنيف الرئيسي
        if 'صحف' in category or 'صحيفة' in category or 'جريدة' in category:
            if 'أفراد' not in category:  # صحف فقط بدون أفراد
                data['newspapers'].append(item)
            else:
                data['influencers'].append(item)
        elif 'حسابات اخبارية' in category or 'إخباري' in category or 'أخبار' in category:
            if 'أفراد' not in category:
                data['news_accounts'].append(item)
            else:
                data['influencers'].append(item)
        elif 'التلفزيون' in category or 'تلفزيون' in category or 'قناة تلفزيونية' in category or 'فضائية' in category:
            if 'أفراد' not in category:
                data['tv_channels'].append(item)
            else:
                data['influencers'].append(item)
        elif 'إذاعة' in category or 'راديو' in category:
            data['radio_channels'].append(item)
        else:
            data['influencers'].append(item)

# الإحصائيات
data['statistics'] = {
    "total": len(data['influencers']) + len(data['newspapers']) + len(data['news_accounts']) + len(data['tv_channels']) + len(data['radio_channels']),
    "influencers_count": len(data['influencers']),
    "newspapers_count": len(data['newspapers']),
    "news_accounts_count": len(data['news_accounts']),
    "tv_channels_count": len(data['tv_channels']),
    "radio_channels_count": len(data['radio_channels']),
}

# حفظ JSON
output_file = Path(__file__).parent / 'data' / 'media_database' / 'media_tools.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ تم التحويل بنجاح!")
print(f"📊 الإحصائيات:")
print(f"   - المؤثرين: {data['statistics']['influencers_count']}")
print(f"   - الصحف: {data['statistics']['newspapers_count']}")
print(f"   - حسابات إخبارية: {data['statistics']['news_accounts_count']}")
print(f"   - قنوات تلفزيونية: {data['statistics']['tv_channels_count']}")
print(f"   - قنوات إذاعية: {data['statistics']['radio_channels_count']}")
print(f"   - الإجمالي: {data['statistics']['total']}")
print(f"\n💾 تم الحفظ في: {output_file}")
