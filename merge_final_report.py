"""
دمج جميع المراحل في تقرير نهائي واحد
Merge all phases into one final report
"""

import json
import os
from datetime import datetime

# المسارات
PHASES_PATH = "static/data/qatar_sports_analysis/report_phases"
OUTPUT_PATH = "static/data/qatar_sports_analysis"

def load_phase(phase_num):
    """تحميل مرحلة"""
    files = {
        1: 'phase1_introduction_methodology_summary.json',
        2: 'phase2_media_topic_analysis.json',
        3: 'phase3_results_recommendations.json'
    }
    filepath = os.path.join(PHASES_PATH, files[phase_num])
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def merge_report():
    """دمج التقرير الكامل"""
    print("=" * 70)
    print("🇶🇦 تقرير الكفاءة الإعلامية والسمعة المؤسسية")
    print("   وزارة الرياضة والشباب القطرية")
    print("   نوفمبر 2025 - يناير 2026")
    print("=" * 70)
    
    print("\n📂 جاري تحميل المراحل الثلاث...")
    
    phase1 = load_phase(1)
    print("   ✅ المرحلة الأولى: المقدمة + المنهجية + الملخص التنفيذي")
    
    phase2 = load_phase(2)
    print("   ✅ المرحلة الثانية: الإعلام التقليدي + التواصل + المواضيع")
    
    phase3 = load_phase(3)
    print("   ✅ المرحلة الثالثة: النتائج + التوصيات + الملاحق")
    
    # بناء التقرير النهائي
    final_report = {
        "report_metadata": {
            "title": "تقرير الكفاءة الإعلامية والسمعة المؤسسية",
            "subtitle": "وزارة الرياضة والشباب القطرية",
            "period": "نوفمبر 2025 - يناير 2026",
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "version": "1.0",
            "total_pages": 44,
            "language": "العربية",
            "prepared_by": "فريق التحليل الإعلامي"
        },
        
        "table_of_contents": {
            "sections": [
                {"number": 1, "title": "المقدمة", "page": 3, "subsections": [
                    "تمهيد", "نبذة عن الوزارة", "أهداف التقرير", "أهمية التقرير", "نطاق التقرير"
                ]},
                {"number": 2, "title": "المنهجية", "page": 5, "subsections": [
                    "النطاق والعينة", "تجهيز البيانات", "التصنيف الموضوعي", "قياس الانطباعات"
                ]},
                {"number": 3, "title": "الملخص التنفيذي", "page": 9, "subsections": [
                    "نظرة عامة", "الأرقام الرئيسية", "محركات المشهد", "الأنماط الزمنية", "محركات الإيجابية والسلبية"
                ]},
                {"number": 4, "title": "تحليل الإعلام التقليدي", "page": 13, "subsections": [
                    "نظرة عامة", "تحليل المصادر", "المواضيع الرئيسية", "توزيع المشاعر", "التغطيات المميزة"
                ]},
                {"number": 5, "title": "تحليل منصات التواصل الاجتماعي", "page": 19, "subsections": [
                    "نظرة عامة", "توزيع المنصات", "تحليل التفاعل", "الهاشتاقات", "المؤثرون", "المحتوى الفيروسي"
                ]},
                {"number": 6, "title": "تحليل المواضيع والاتجاهات", "page": 25, "subsections": [
                    "التحليل التفصيلي للمواضيع", "مقارنة الفعاليات السبع", "المواضيع الناشئة", "مصفوفة المواضيع والمشاعر"
                ]},
                {"number": 7, "title": "النتائج والاستنتاجات", "page": 33, "subsections": [
                    "ملخص النتائج", "النتائج الرئيسية", "تحليل SWOT", "بطاقة الأداء"
                ]},
                {"number": 8, "title": "التوصيات الاستراتيجية", "page": 37, "subsections": [
                    "التوصيات الاستراتيجية", "التوصيات التكتيكية", "توصيات خاصة بالفعاليات", "خارطة طريق التنفيذ"
                ]},
                {"number": 9, "title": "الملاحق", "page": 41, "subsections": [
                    "تفاصيل البيانات", "تفاصيل الفعاليات", "المصادر الإعلامية", "تحليل اللغات", "المؤثرون", "المصطلحات"
                ]}
            ]
        },
        
        "key_highlights": {
            "total_materials": 150838,
            "total_reach": "134+ مليار",
            "positive_sentiment": "28%",
            "negative_sentiment": "5.8%",
            "events_covered": 7,
            "analysis_days": 90,
            "overall_rating": "A+"
        },
        
        # المحتوى الكامل للأقسام
        "sections": {
            "section_1": phase1.get("section_1_introduction", {}),
            "section_2": phase1.get("section_2_methodology", {}),
            "section_3": phase1.get("section_3_executive_summary", {}),
            "section_4": phase2.get("section_4_traditional_media", {}),
            "section_5": phase2.get("section_5_social_media", {}),
            "section_6": phase2.get("section_6_topic_analysis", {}),
            "section_7": phase3.get("section_7_results", {}),
            "section_8": phase3.get("section_8_recommendations", {}),
            "section_9": phase3.get("section_9_appendices", {})
        },
        
        "conclusion": phase3.get("report_conclusion", {})
    }
    
    # حفظ التقرير النهائي
    output_file = os.path.join(OUTPUT_PATH, 'FINAL_REPORT_COMPLETE.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n💾 تم حفظ التقرير النهائي في: {output_file}")
    
    # طباعة ملخص التقرير
    print("\n" + "=" * 70)
    print("📋 ملخص التقرير النهائي")
    print("=" * 70)
    
    print("\n📑 جدول المحتويات:")
    for section in final_report['table_of_contents']['sections']:
        print(f"   {section['number']}. {section['title']} (صفحة {section['page']})")
        for sub in section['subsections'][:3]:
            print(f"      • {sub}")
        if len(section['subsections']) > 3:
            print(f"      • ... (+{len(section['subsections'])-3} أقسام فرعية)")
    
    print("\n" + "=" * 70)
    print("📊 أبرز الأرقام:")
    print("=" * 70)
    highlights = final_report['key_highlights']
    print(f"   📰 إجمالي المواد الإعلامية: {highlights['total_materials']:,}")
    print(f"   📣 إجمالي الوصول: {highlights['total_reach']}")
    print(f"   ✅ نسبة الإيجابية: {highlights['positive_sentiment']}")
    print(f"   ❌ نسبة السلبية: {highlights['negative_sentiment']}")
    print(f"   🏆 عدد الفعاليات: {highlights['events_covered']}")
    print(f"   📅 فترة التحليل: {highlights['analysis_days']} يوم")
    print(f"   ⭐ التقييم العام: {highlights['overall_rating']}")
    
    print("\n" + "=" * 70)
    print("✅ التقرير النهائي جاهز!")
    print("=" * 70)
    
    # إحصائيات الملف
    file_size = os.path.getsize(output_file)
    print(f"\n📁 حجم الملف: {file_size/1024:.1f} KB")
    
    # قائمة الملفات المُنشأة
    print("\n📂 جميع الملفات المُنشأة:")
    print(f"   1. {PHASES_PATH}/phase1_introduction_methodology_summary.json")
    print(f"   2. {PHASES_PATH}/phase2_media_topic_analysis.json")
    print(f"   3. {PHASES_PATH}/phase3_results_recommendations.json")
    print(f"   4. {output_file} (التقرير النهائي الكامل)")
    
    return final_report

if __name__ == "__main__":
    report = merge_report()
