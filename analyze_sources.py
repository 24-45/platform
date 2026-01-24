#!/usr/bin/env python3
"""
تحليل مصادر الأخبار من ملفات Meltwater Analytics
"""

import os
import pandas as pd
from collections import defaultdict
import json
import glob

# المسار الأساسي
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr 4"

# قائمة لتخزين جميع ملفات CSV
csv_files = []

# البحث عن جميع ملفات CSV في مجلدات Analytics
for root, dirs, files in os.walk(BASE_PATH):
    if 'Analytics' in root:
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))

print(f"=== تم العثور على {len(csv_files)} ملف CSV ===\n")

# طباعة الملفات الموجودة
for i, f in enumerate(csv_files, 1):
    print(f"{i}. {os.path.basename(os.path.dirname(os.path.dirname(f)))}")
    print(f"   الملف: {os.path.basename(f)[:50]}...")

print("\n" + "="*80 + "\n")

# قاموس لتخزين المصادر
all_sources = defaultdict(lambda: {"count": 0, "category": "", "events": []})

# تصنيف المصادر
QATAR_SOURCES = [
    "al raya", "الراية", "al sharq", "الشرق", "qatar news", "qna", 
    "وكالة الأنباء القطرية", "gulf times", "the peninsula", "qatar tribune",
    "al watan", "الوطن", "العرب", "al arab", "lusail news", "لوسيل",
    "i love qatar", "marhaba", "qatar living", "الدوحة", "doha news"
]

ARAB_SOURCES = [
    "الزهراء", "klyoum", "كل يوم", "نبض", "nabd", "عرب خبر", "arabkhabar",
    "العربية", "الجزيرة", "al jazeera", "al arabiya", "سكاي نيوز عربية",
    "bein", "بي ان", "الشرق الأوسط", "asharq", "cnn عربي", "فرانس 24",
    "rt arabic", "dw عربي", "المصري اليوم", "اليوم السابع", "الأهرام"
]

def classify_source(source_name):
    """تصنيف المصدر"""
    source_lower = source_name.lower()
    
    for q in QATAR_SOURCES:
        if q in source_lower:
            return "قطري"
    
    for a in ARAB_SOURCES:
        if a in source_lower:
            return "عربي"
    
    return "دولي"

# قراءة كل ملف CSV
for csv_file in csv_files:
    try:
        # تحديد اسم الحدث
        event_name = os.path.basename(os.path.dirname(os.path.dirname(csv_file)))
        
        # قراءة الملف بترميز UTF-16-LE (Meltwater format)
        df = pd.read_csv(csv_file, encoding='utf-16-le', sep='\t', on_bad_lines='skip')
        print(f"   ✓ ترميز: utf-16-le, فاصل: tab")
        
        print(f"\n📊 تحليل: {event_name}")
        print(f"   الأعمدة: {list(df.columns)[:5]}...")
        print(f"   عدد الصفوف: {len(df)}")
        
        # البحث عن عمود المصدر (Source Name هو الصحيح)
        source_col = None
        for col in df.columns:
            if col == 'Source Name':
                source_col = col
                break
        
        # إذا لم يوجد، نبحث عن بدائل
        if not source_col:
            for col in df.columns:
                col_lower = col.lower()
                if 'source name' in col_lower or 'outlet' in col_lower:
                    source_col = col
                    break
        
        if source_col:
            print(f"   عمود المصدر: {source_col}")
            
            # حساب عدد المنشورات لكل مصدر
            source_counts = df[source_col].value_counts()
            
            for source, count in source_counts.items():
                if pd.notna(source) and str(source).strip():
                    source_name = str(source).strip()
                    all_sources[source_name]["count"] += count
                    all_sources[source_name]["category"] = classify_source(source_name)
                    if event_name not in all_sources[source_name]["events"]:
                        all_sources[source_name]["events"].append(event_name)
        else:
            print(f"   ⚠️ لم يتم العثور على عمود المصدر")
            print(f"   الأعمدة المتاحة: {list(df.columns)}")
            
    except Exception as e:
        print(f"   ❌ خطأ في قراءة الملف: {e}")

print("\n" + "="*80)
print("=== نتائج التحليل ===")
print("="*80)

# تحويل إلى قائمة وترتيب
sources_list = [(name, data["count"], data["category"], data["events"]) 
                for name, data in all_sources.items()]
sources_list.sort(key=lambda x: x[1], reverse=True)

# تصنيف حسب الفئة
qatar_sources = [(n, c, e) for n, c, cat, e in sources_list if cat == "قطري"]
arab_sources = [(n, c, e) for n, c, cat, e in sources_list if cat == "عربي"]
intl_sources = [(n, c, e) for n, c, cat, e in sources_list if cat == "دولي"]

print(f"\n🇶🇦 المصادر القطرية ({len(qatar_sources)} مصدر):")
print("-" * 60)
total_qatar = 0
for i, (name, count, events) in enumerate(qatar_sources[:10], 1):
    print(f"{i:2}. {name[:40]:<40} | {count:>6} خبر")
    total_qatar += count
print(f"\n   الإجمالي: {total_qatar:,} خبر")

print(f"\n🌍 المصادر العربية ({len(arab_sources)} مصدر):")
print("-" * 60)
total_arab = 0
for i, (name, count, events) in enumerate(arab_sources[:10], 1):
    print(f"{i:2}. {name[:40]:<40} | {count:>6} خبر")
    total_arab += count
print(f"\n   الإجمالي: {total_arab:,} خبر")

print(f"\n🌐 المصادر الدولية ({len(intl_sources)} مصدر):")
print("-" * 60)
total_intl = 0
for i, (name, count, events) in enumerate(intl_sources[:10], 1):
    print(f"{i:2}. {name[:40]:<40} | {count:>6} خبر")
    total_intl += count
print(f"\n   الإجمالي: {total_intl:,} خبر")

print("\n" + "="*80)
print(f"📊 الإجمالي الكلي: {sum(c for _, c, _, _ in sources_list):,} خبر من {len(sources_list)} مصدر")
print("="*80)

# حفظ النتائج في ملف JSON
output_data = {
    "summary": {
        "total_sources": len(sources_list),
        "total_articles": sum(c for _, c, _, _ in sources_list),
        "qatar_sources": len(qatar_sources),
        "arab_sources": len(arab_sources),
        "intl_sources": len(intl_sources)
    },
    "qatar": [{"name": n, "count": c, "events": e} for n, c, e in qatar_sources[:10]],
    "arab": [{"name": n, "count": c, "events": e} for n, c, e in arab_sources[:10]],
    "international": [{"name": n, "count": c, "events": e} for n, c, e in intl_sources[:10]],
    "all_sources": [{"name": n, "count": c, "category": cat, "events": e} 
                    for n, c, cat, e in sources_list]
}

with open("/Users/taherirshaid/Desktop/Project/24-45-Platform/sources_analysis.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\n✅ تم حفظ النتائج في sources_analysis.json")
