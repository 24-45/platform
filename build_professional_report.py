#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
دمج جميع المراحل والتحسينات في تقرير نهائي احترافي
إصدار 2.0 - مطابق لمعايير تقرير الكهرباء السعودية
"""

import json
import os
from datetime import datetime

# المسارات
BASE_PATH = "static/data/qatar_sports_analysis/report_phases"
PHASE1 = os.path.join(BASE_PATH, "phase1_introduction_methodology_summary.json")
PHASE2 = os.path.join(BASE_PATH, "phase2_media_topic_analysis.json")
PHASE3 = os.path.join(BASE_PATH, "phase3_results_recommendations.json")
ENHANCED_DATA = os.path.join(BASE_PATH, "ENHANCED_REPORT_DATA.json")
OUTPUT_FILE = os.path.join(BASE_PATH, "PROFESSIONAL_REPORT_FINAL.json")

print("=" * 70)
print("🔗 دمج جميع المراحل والتحسينات في تقرير نهائي احترافي")
print("=" * 70)

# تحميل المراحل الثلاث
print("\n📂 جاري تحميل الملفات...")

with open(PHASE1, 'r', encoding='utf-8') as f:
    phase1 = json.load(f)

with open(PHASE2, 'r', encoding='utf-8') as f:
    phase2 = json.load(f)

with open(PHASE3, 'r', encoding='utf-8') as f:
    phase3 = json.load(f)

with open(ENHANCED_DATA, 'r', encoding='utf-8') as f:
    enhancements = json.load(f)

# استخراج الأقسام من كل مرحلة
def extract_sections(phase_data):
    sections = []
    for key, value in phase_data.items():
        if key.startswith("section_") and isinstance(value, dict):
            sections.append({
                "key": key,
                "data": value
            })
    return sections

phase1_sections = extract_sections(phase1)
phase2_sections = extract_sections(phase2)
phase3_sections = extract_sections(phase3)

print(f"   ✓ المرحلة 1: {len(phase1_sections)} أقسام")
print(f"   ✓ المرحلة 2: {len(phase2_sections)} أقسام")
print(f"   ✓ المرحلة 3: {len(phase3_sections)} أقسام")

# المخططات المحددة
charts_spec = enhancements.get("charts_specification", {})

# بناء التقرير المدمج الاحترافي
report = {
    "metadata": {
        "title": "تقرير السمعة الإعلامية",
        "subtitle": "وزارة الرياضة والشباب - دولة قطر",
        "period": "نوفمبر 2025 - يناير 2026",
        "analysis_period_days": 90,
        "total_materials_analyzed": 150838,
        "traditional_media": 46003,
        "social_media": 104835,
        "events_covered": 7,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "2.0 - Professional Enhanced",
        "quality_level": "Professional - Saudi Electricity Standard",
        "prepared_by": "منصة 24-45 للذكاء الإعلامي"
    },
    "structure": {
        "total_sections": 10,
        "total_subsections": 25,
        "estimated_pages": 55,
        "charts_count": 25,
        "tables_count": 15,
        "infographics_count": 10
    },
    "sections": []
}

# معالجة وتحويل كل قسم
section_order = 1

# === المرحلة 1: المقدمة والمنهجية والملخص ===
for section in phase1_sections:
    section_data = section["data"]
    section_key = section["key"]
    
    # تحديد المخططات المناسبة
    assigned_charts = []
    if "executive_summary" in section_key:
        assigned_charts = [
            charts_spec.get("ES-1"),
            charts_spec.get("ES-2"),
            charts_spec.get("ES-3")
        ]
    
    report["sections"].append({
        "order": section_order,
        "id": section_key,
        "title": section_data.get("title", ""),
        "pages": section_data.get("pages", 2),
        "content": section_data,
        "charts": [c for c in assigned_charts if c],
        "phase": 1
    })
    section_order += 1

# === المرحلة 2: التحليل الإعلامي ===
for section in phase2_sections:
    section_data = section["data"]
    section_key = section["key"]
    
    assigned_charts = []
    if "traditional" in section_key:
        assigned_charts = [
            charts_spec.get("TM-1"),
            charts_spec.get("TM-2"),
            charts_spec.get("TM-3")
        ]
    elif "social" in section_key:
        assigned_charts = [
            charts_spec.get("SM-1"),
            charts_spec.get("SM-2"),
            charts_spec.get("SM-3")
        ]
        # إضافة بيانات المؤثرين
        section_data["influencers_detailed"] = enhancements.get("influencers_detailed", {})
    elif "topic" in section_key:
        assigned_charts = [
            charts_spec.get("TA-1"),
            charts_spec.get("TA-2"),
            charts_spec.get("TA-3")
        ]
        # إضافة Word Cloud
        section_data["word_cloud_data"] = enhancements.get("word_cloud_data", {})
    
    report["sections"].append({
        "order": section_order,
        "id": section_key,
        "title": section_data.get("title", ""),
        "pages": section_data.get("pages", 3),
        "content": section_data,
        "charts": [c for c in assigned_charts if c],
        "phase": 2
    })
    section_order += 1

# === المرحلة 3: النتائج والتوصيات ===
for section in phase3_sections:
    section_data = section["data"]
    section_key = section["key"]
    
    assigned_charts = []
    if "results" in section_key or "findings" in section_key:
        assigned_charts = [
            charts_spec.get("RS-1"),
            charts_spec.get("RS-2"),
            charts_spec.get("RS-3")
        ]
    
    report["sections"].append({
        "order": section_order,
        "id": section_key,
        "title": section_data.get("title", ""),
        "pages": section_data.get("pages", 2),
        "content": section_data,
        "charts": [c for c in assigned_charts if c],
        "phase": 3
    })
    section_order += 1

# === إضافة قسم خاص للفعاليات الثلاث ===
top_3_events = enhancements.get("top_3_events_deep_analysis", {})
report["sections"].append({
    "order": section_order,
    "id": "section_special_top_events",
    "title": "تحليل معمق: أهم ثلاث فعاليات رياضية",
    "pages": 6,
    "content": {
        "title": "تحليل معمق: أهم ثلاث فعاليات رياضية",
        "description": "تحليل تفصيلي لأداء أهم ثلاث فعاليات من حيث الوصول والتفاعل",
        "events": top_3_events
    },
    "charts": [
        {
            "id": "TOP3-1",
            "title": "مقارنة الوصول للفعاليات الثلاث",
            "type": "horizontal_bar",
            "description": "مقارنة إجمالي الوصول"
        },
        {
            "id": "TOP3-2",
            "title": "توزيع المشاعر حسب الفعالية",
            "type": "grouped_bar",
            "description": "نسب الإيجابية والحيادية والسلبية"
        },
        {
            "id": "TOP3-3",
            "title": "خريطة المؤثرين",
            "type": "bubble_chart",
            "description": "أهم المؤثرين لكل فعالية"
        }
    ],
    "phase": 3
})
section_order += 1

# === إضافة قسم Word Cloud ===
word_cloud_data = enhancements.get("word_cloud_data", {})
report["sections"].append({
    "order": section_order,
    "id": "section_word_cloud",
    "title": "سحابة الكلمات والهاشتاقات الأكثر تداولاً",
    "pages": 2,
    "content": {
        "title": "سحابة الكلمات والهاشتاقات",
        "description": "الكلمات والمواضيع الأكثر ارتباطاً بالفعاليات الرياضية القطرية",
        "word_cloud": word_cloud_data
    },
    "charts": [
        {
            "id": "WC-1",
            "title": "سحابة الكلمات العربية",
            "type": "word_cloud",
            "language": "ar"
        },
        {
            "id": "WC-2",
            "title": "سحابة الكلمات الإنجليزية",
            "type": "word_cloud",
            "language": "en"
        },
        {
            "id": "WC-3",
            "title": "الهاشتاقات الأكثر تداولاً",
            "type": "horizontal_bar",
            "color_scheme": "gradient"
        }
    ],
    "phase": 3
})

# تحديث إحصائيات الهيكل
report["structure"]["total_sections"] = len(report["sections"])
total_pages = sum(s.get("pages", 2) for s in report["sections"])
report["structure"]["estimated_pages"] = total_pages
total_charts = sum(len(s.get("charts", [])) for s in report["sections"])
report["structure"]["charts_count"] = total_charts

# إضافة التحسينات كمرجع
report["enhancements_reference"] = {
    "charts_specification": charts_spec,
    "influencers_summary": {
        "ministry": len(enhancements.get("influencers_detailed", {}).get("ministry_influencers", [])),
        "arab_cup": len(enhancements.get("influencers_detailed", {}).get("arab_cup_influencers", [])),
        "f1": len(enhancements.get("influencers_detailed", {}).get("f1_influencers", [])),
        "ufc": len(enhancements.get("influencers_detailed", {}).get("ufc_influencers", []))
    },
    "top_3_events": list(top_3_events.keys()),
    "word_cloud_stats": {
        "arabic_words": len(word_cloud_data.get("arabic_words", [])),
        "english_words": len(word_cloud_data.get("english_words", [])),
        "hashtags": len(word_cloud_data.get("top_hashtags", []))
    }
}

# حفظ التقرير
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize(OUTPUT_FILE) / 1024

print("\n" + "=" * 70)
print("✅ تم إنشاء التقرير النهائي الاحترافي!")
print("=" * 70)
print(f"\n📁 الملف: {OUTPUT_FILE}")
print(f"📦 الحجم: {file_size:.1f} KB")

print("\n" + "=" * 70)
print("📊 إحصائيات التقرير:")
print("=" * 70)
print(f"   📄 إجمالي الأقسام: {report['structure']['total_sections']}")
print(f"   📑 إجمالي الصفحات: {report['structure']['estimated_pages']}")
print(f"   📈 إجمالي المخططات: {report['structure']['charts_count']}")

print("\n" + "=" * 70)
print("📋 محتويات التقرير:")
print("=" * 70)

for section in report["sections"]:
    charts_count = len(section.get("charts", []))
    charts_info = f" [{charts_count} مخططات]" if charts_count > 0 else ""
    phase_info = f"(المرحلة {section['phase']})"
    print(f"   {section['order']:2d}. {section['title'][:40]:<40} {charts_info} {phase_info}")

print("\n" + "=" * 70)
print("🎯 التقرير جاهز للتحويل إلى شرائح احترافية!")
print("=" * 70)
