#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
دمج جميع المراحل والتحسينات في تقرير نهائي احترافي
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
print(f"   ✓ المرحلة 1: {len(phase1.get('sections', []))} أقسام")

with open(PHASE2, 'r', encoding='utf-8') as f:
    phase2 = json.load(f)
print(f"   ✓ المرحلة 2: {len(phase2.get('sections', []))} أقسام")

with open(PHASE3, 'r', encoding='utf-8') as f:
    phase3 = json.load(f)
print(f"   ✓ المرحلة 3: {len(phase3.get('sections', []))} أقسام")

# بناء التقرير المدمج
report = {
    "metadata": {
        "title": "تقرير السمعة الإعلامية - وزارة الرياضة والشباب القطرية",
        "subtitle": "تحليل شامل للفعاليات الرياضية الكبرى",
        "period": "نوفمبر 2025 - يناير 2026",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "2.0 - Professional Enhanced",
        "quality_level": "Professional - Saudi Electricity Standard"
    },
    "sections": []
}

# دمج الأقسام من المراحل الثلاث
report["sections"].extend(phase1.get("sections", []))
report["sections"].extend(phase2.get("sections", []))
report["sections"].extend(phase3.get("sections", []))

with open(ENHANCED_DATA, 'r', encoding='utf-8') as f:
    enhancements = json.load(f)

print(f"\n📊 التقرير الأصلي: {len(report.get('sections', []))} أقسام")
print(f"📈 التحسينات: {len(enhancements.keys())} عناصر")

# إضافة التحسينات للتقرير
report["enhancements"] = enhancements
report["metadata"]["version"] = "2.0 - Professional Enhanced"
report["metadata"]["enhanced_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report["metadata"]["quality_level"] = "Professional - Saudi Electricity Standard"

# تحديث الأقسام بالمخططات المحددة
charts_spec = enhancements.get("charts_specification", {})

# ربط المخططات بالأقسام
for section in report.get("sections", []):
    section_id = section.get("id", "")
    
    # البحث عن المخططات المناسبة لهذا القسم
    matched_charts = []
    for chart_id, chart_info in charts_spec.items():
        if section_id.startswith(chart_id[:2]) or chart_id.split("-")[0] == section_id[:2]:
            matched_charts.append(chart_info)
    
    if matched_charts:
        section["charts"] = matched_charts

# إضافة بيانات المؤثرين للأقسام المناسبة
for section in report.get("sections", []):
    if "التواصل الاجتماعي" in section.get("title", "") or "social" in section.get("id", "").lower():
        section["influencers_data"] = enhancements.get("influencers_detailed", {})

# إضافة تحليل الفعاليات الثلاث
for section in report.get("sections", []):
    if "الفعاليات" in section.get("title", "") or "الأحداث" in section.get("title", ""):
        section["top_events_analysis"] = enhancements.get("top_3_events_deep_analysis", {})

# إضافة Word Cloud للمواضيع
for section in report.get("sections", []):
    if "المواضيع" in section.get("title", "") or "topics" in section.get("id", "").lower():
        section["word_cloud"] = enhancements.get("word_cloud_data", {})

# حساب إجمالي الصفحات الجديد (تقديري)
total_pages = sum(section.get("pages", 1) for section in report.get("sections", []))
# إضافة صفحات للمحتوى الجديد
additional_pages = 15  # للمخططات والمؤثرين والتحليل المفصل
report["metadata"]["estimated_pages"] = total_pages + additional_pages

# حفظ التقرير المدمج
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize(OUTPUT_FILE) / 1024

print("\n" + "=" * 70)
print("✅ تم دمج التقرير بنجاح!")
print("=" * 70)
print(f"\n📁 الملف: {OUTPUT_FILE}")
print(f"📦 الحجم: {file_size:.1f} KB")
print(f"📄 الصفحات المقدرة: {total_pages + additional_pages}")

print("\n" + "=" * 70)
print("📋 محتويات التقرير النهائي المحسّن:")
print("=" * 70)

for i, section in enumerate(report.get("sections", []), 1):
    charts_count = len(section.get("charts", []))
    has_influencers = "✅" if section.get("influencers_data") else ""
    has_events = "✅" if section.get("top_events_analysis") else ""
    has_wordcloud = "✅" if section.get("word_cloud") else ""
    
    extras = []
    if charts_count > 0:
        extras.append(f"{charts_count} مخطط")
    if has_influencers:
        extras.append("مؤثرون")
    if has_events:
        extras.append("تحليل فعاليات")
    if has_wordcloud:
        extras.append("Word Cloud")
    
    extras_str = f" [{', '.join(extras)}]" if extras else ""
    print(f"{i:2d}. {section.get('title', 'غير محدد')}{extras_str}")

print("\n" + "=" * 70)
print("🎯 التقرير جاهز للتحويل إلى شرائح احترافية!")
print("=" * 70)
