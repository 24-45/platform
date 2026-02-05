# -*- coding: utf-8 -*-
"""
الملف الرئيسي لتاب الوعي المجتمعي
يجمع كل الأجزاء ويوفر واجهة موحدة للوصول للبيانات
الهيئة العامة للأوقاف - تقرير تحليل السمعة الرقمية
"""

# ═══════════════════════════════════════════════════════════════════════════
# استيراد الأجزاء
# ═══════════════════════════════════════════════════════════════════════════

from waqf_community_awareness_part1 import (
    TAB_INFO,
    STUDY_INTRO,
    SENTIMENT_SECTION,
    STEREOTYPES_SECTION,
    get_sentiment_data,
    get_main_stereotypes,
    get_sentiment_gap
)

from waqf_community_awareness_part2 import (
    KNOWLEDGE_GAPS_SECTION,
    SENSITIVE_ISSUES_SECTION,
    get_knowledge_gaps,
    get_sensitive_issues,
    get_gap_initiatives,
    get_survey_results
)

from waqf_community_awareness_part3 import (
    KEY_MESSAGES_SECTION,
    AUDIENCE_SEGMENTS_SECTION,
    get_key_messages,
    get_audience_segments,
    get_message_corrections,
    get_communication_strategies
)

from waqf_community_awareness_part4 import (
    CONCEPTUAL_FRAMES_SECTION,
    BRAND_PERSONALITY_SECTION,
    get_conceptual_frames,
    get_brand_traits,
    get_positive_traits,
    get_negative_traits
)

from waqf_community_awareness_part5 import (
    ENGAGEMENT_SECTION,
    TRUST_INDICATORS_SECTION,
    get_engagement_stats,
    get_content_engagement,
    get_trust_score,
    get_trust_indicators,
    get_trust_by_segment,
    get_trust_builders
)

from waqf_community_awareness_part6 import (
    SCENARIOS_SECTION,
    STRATEGIC_RECOMMENDATIONS_SECTION,
    CONCLUSION_SECTION,
    get_current_scenario,
    get_target_scenario,
    get_gap_analysis,
    get_recommendations,
    get_high_priority_recommendations,
    get_conclusion
)


# ═══════════════════════════════════════════════════════════════════════════
# البيانات الموحدة
# ═══════════════════════════════════════════════════════════════════════════

# معلومات التاب
COMMUNITY_AWARENESS_TAB = {
    "id": "view-media-image",
    "title": "الوعي المجتمعي",
    "title_en": "Community Awareness",
    "icon": "👥",
    "order": 4,
    "sections_count": 12
}

# قائمة الأقسام
SECTIONS = [
    {"number": "01", "title": "تحليل المشاعر", "title_en": "Sentiment Analysis", "part": 1},
    {"number": "02", "title": "تحليل الصور النمطية", "title_en": "Stereotypes Analysis", "part": 1},
    {"number": "03", "title": "الفجوات المعرفية", "title_en": "Knowledge Gaps", "part": 2},
    {"number": "04", "title": "القضايا الحساسة", "title_en": "Sensitive Issues", "part": 2},
    {"number": "05", "title": "الرسائل الرئيسية", "title_en": "Key Messages", "part": 3},
    {"number": "06", "title": "شرائح الجمهور", "title_en": "Audience Segments", "part": 3},
    {"number": "07", "title": "الأطر المفهومية", "title_en": "Conceptual Frames", "part": 4},
    {"number": "08", "title": "هوية الوقف", "title_en": "Brand Personality", "part": 4},
    {"number": "09", "title": "مستوى التفاعل", "title_en": "Engagement Level", "part": 5},
    {"number": "10", "title": "مؤشرات الثقة", "title_en": "Trust Indicators", "part": 5},
    {"number": "11", "title": "السيناريو الحالي والمستهدف", "title_en": "Current vs Target", "part": 6},
    {"number": "12", "title": "التوصيات الاستراتيجية", "title_en": "Recommendations", "part": 6}
]

# جميع البيانات مجمعة
ALL_SECTIONS_DATA = {
    "tab_info": COMMUNITY_AWARENESS_TAB,
    "intro": STUDY_INTRO,
    "sections": {
        "sentiment": SENTIMENT_SECTION,
        "stereotypes": STEREOTYPES_SECTION,
        "knowledge_gaps": KNOWLEDGE_GAPS_SECTION,
        "sensitive_issues": SENSITIVE_ISSUES_SECTION,
        "key_messages": KEY_MESSAGES_SECTION,
        "audience_segments": AUDIENCE_SEGMENTS_SECTION,
        "conceptual_frames": CONCEPTUAL_FRAMES_SECTION,
        "brand_personality": BRAND_PERSONALITY_SECTION,
        "engagement": ENGAGEMENT_SECTION,
        "trust_indicators": TRUST_INDICATORS_SECTION,
        "scenarios": SCENARIOS_SECTION,
        "recommendations": STRATEGIC_RECOMMENDATIONS_SECTION
    },
    "conclusion": CONCLUSION_SECTION
}


# ═══════════════════════════════════════════════════════════════════════════
# دوال الواجهة الموحدة
# ═══════════════════════════════════════════════════════════════════════════

def get_tab_info():
    """الحصول على معلومات التاب"""
    return COMMUNITY_AWARENESS_TAB


def get_all_sections():
    """الحصول على قائمة جميع الأقسام"""
    return SECTIONS


def get_section_by_number(section_number):
    """الحصول على قسم محدد برقمه"""
    section_map = {
        "01": SENTIMENT_SECTION,
        "02": STEREOTYPES_SECTION,
        "03": KNOWLEDGE_GAPS_SECTION,
        "04": SENSITIVE_ISSUES_SECTION,
        "05": KEY_MESSAGES_SECTION,
        "06": AUDIENCE_SEGMENTS_SECTION,
        "07": CONCEPTUAL_FRAMES_SECTION,
        "08": BRAND_PERSONALITY_SECTION,
        "09": ENGAGEMENT_SECTION,
        "10": TRUST_INDICATORS_SECTION,
        "11": SCENARIOS_SECTION,
        "12": STRATEGIC_RECOMMENDATIONS_SECTION
    }
    return section_map.get(section_number)


def get_all_data():
    """الحصول على جميع البيانات"""
    return ALL_SECTIONS_DATA


def get_executive_summary():
    """الحصول على ملخص تنفيذي للتاب"""
    return {
        "tab": COMMUNITY_AWARENESS_TAB["title"],
        "sections_count": len(SECTIONS),
        "key_insights": [
            {
                "area": "المشاعر العامة",
                "finding": get_sentiment_data()["overall"]["percentage"],
                "status": "إيجابي"
            },
            {
                "area": "الثقة المجتمعية", 
                "finding": f"{get_trust_score()['overall_score']}/100",
                "status": get_trust_score()["rating"]
            },
            {
                "area": "فجوة الوعي",
                "finding": f"{get_gap_analysis()['overall_gap']} نقطة",
                "status": "يحتاج تحسين"
            }
        ],
        "recommendations_count": len(get_recommendations()),
        "high_priority_count": len(get_high_priority_recommendations())
    }


def get_data_for_charts():
    """الحصول على البيانات الجاهزة للرسوم البيانية"""
    return {
        "sentiment_comparison": get_sentiment_data()["comparison"],
        "stereotypes": [
            {"name": s["title"], "category": s.get("category", "neutral")} 
            for s in get_main_stereotypes()
        ],
        "knowledge_gaps": [
            {"gap": g["title"], "awareness": g.get("awareness_percentage", 0)} 
            for g in get_knowledge_gaps()
        ],
        "trust_indicators": [
            {"indicator": t["indicator"], "score": t["score"]} 
            for t in get_trust_indicators()
        ],
        "engagement_by_content": get_content_engagement(),
        "scenario_comparison": {
            "current": get_current_scenario()["score"],
            "target": get_target_scenario()["score"],
            "gap": get_gap_analysis()["overall_gap"]
        }
    }


# ═══════════════════════════════════════════════════════════════════════════
# دوال التصدير للقالب
# ═══════════════════════════════════════════════════════════════════════════

def render_section_html(section_number):
    """تصدير HTML لقسم محدد (placeholder للتطوير)"""
    section = get_section_by_number(section_number)
    if section:
        return f"<div class='section' id='section-{section_number}'>{section['title']}</div>"
    return ""


def export_to_json():
    """تصدير جميع البيانات كـ JSON"""
    import json
    return json.dumps(ALL_SECTIONS_DATA, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════
# طباعة الملخص
# ═══════════════════════════════════════════════════════════════════════════

def print_full_summary():
    """طباعة ملخص كامل للتاب"""
    print("═" * 70)
    print("📊 تاب الوعي المجتمعي - ملخص شامل")
    print("═" * 70)
    
    print(f"\n{'─' * 70}")
    print("📋 الأقسام:")
    print(f"{'─' * 70}")
    for section in SECTIONS:
        print(f"   {section['number']}. {section['title']} ({section['title_en']}) - Part {section['part']}")
    
    print(f"\n{'─' * 70}")
    print("📈 الإحصائيات الرئيسية:")
    print(f"{'─' * 70}")
    
    # المشاعر
    sentiment = get_sentiment_data()
    print(f"\n   🎭 تحليل المشاعر:")
    print(f"      • إيجابي: {sentiment['overall']['positive']}%")
    print(f"      • سلبي: {sentiment['overall']['negative']}%")
    print(f"      • محايد: {sentiment['overall']['neutral']}%")
    
    # الثقة
    trust = get_trust_score()
    print(f"\n   🛡️ مستوى الثقة: {trust['overall_score']}/100 ({trust['rating']})")
    
    # التوصيات
    recs = get_recommendations()
    high_recs = get_high_priority_recommendations()
    print(f"\n   📋 التوصيات:")
    print(f"      • إجمالي: {len(recs)}")
    print(f"      • عالية الأولوية: {len(high_recs)}")
    
    # الفجوة
    gap = get_gap_analysis()
    print(f"\n   📊 تحليل الفجوة:")
    print(f"      • الحالي: {get_current_scenario()['score']}/100")
    print(f"      • المستهدف: {get_target_scenario()['score']}/100")
    print(f"      • الفجوة: {gap['overall_gap']} نقطة")
    
    print(f"\n{'═' * 70}")
    print("✅ تم تحميل جميع بيانات تاب الوعي المجتمعي بنجاح")
    print(f"{'═' * 70}")


if __name__ == "__main__":
    print_full_summary()
