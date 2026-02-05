# -*- coding: utf-8 -*-
"""
ملف التجميع الرئيسي لمحتوى تاب الأداء الإعلامي
الهيئة العامة للأوقاف - تقرير تحليل السمعة الرقمية

هذا الملف يجمع جميع الأجزاء الستة في مكان واحد للوصول السهل
"""

# استيراد جميع الأجزاء
from waqf_media_performance_part1 import (
    POST_TYPES_ANALYSIS,
    DIGITAL_FOOTPRINT,
    TOP_HASHTAGS,
    TOP_ACCOUNTS,
    SENTIMENT_ANALYSIS,
    REACH_ANALYSIS,
    VISIBILITY_PEAKS,
    COMMUNICATION_GAPS_X,
    get_all_hashtags,
    get_top_accounts_list,
    get_sentiment_triggers,
    get_visibility_peaks,
    get_communication_gaps
)

from waqf_media_performance_part2 import (
    NEWS_ANALYSIS_OVERVIEW,
    STRATEGIC_READING,
    NEWS_PEAKS,
    MONTHLY_LEADERS,
    TOP_NEWS_TOPICS,
    PRESS_LEADERS,
    PRESS_COMMUNICATION_GAPS,
    get_press_gaps,
    get_critical_gaps,
    get_positive_gaps,
    get_all_recommendations as get_news_recommendations
)

from waqf_media_performance_part3 import (
    STUDY_OVERVIEW,
    SENTIMENT_SECTION,
    STEREOTYPES_SECTION,
    KNOWLEDGE_GAPS_SECTION,
    get_all_stereotypes,
    get_knowledge_gaps,
    get_sentiment_data
)

from waqf_media_performance_part4 import (
    SENSITIVE_ISSUES_SECTION,
    KEY_MESSAGES_SECTION,
    AUDIENCE_SEGMENTS_SECTION,
    get_sensitive_issues,
    get_key_messages,
    get_audience_segments
)

from waqf_media_performance_part5 import (
    CONCEPTUAL_FRAMES_SECTION,
    BRAND_PERSONALITY_SECTION,
    ENGAGEMENT_LEVEL_SECTION,
    get_conceptual_frames,
    get_personality_traits,
    get_engagement_metrics,
    get_engagement_gaps
)

from waqf_media_performance_part6 import (
    TRUST_INDICATORS_SECTION,
    SCENARIOS_SECTION,
    STRATEGIC_RECOMMENDATIONS_SECTION,
    get_trust_score,
    get_trust_challenges,
    get_current_scenario,
    get_target_scenario,
    get_strategic_recommendations,
    get_implementation_roadmap
)


# ═══════════════════════════════════════════════════════════════════════════
# هيكل تاب الأداء الإعلامي الكامل
# ═══════════════════════════════════════════════════════════════════════════

MEDIA_PERFORMANCE_TAB_STRUCTURE = {
    "tab_name": "الأداء الإعلامي",
    "tab_id": "media-performance",
    
    "sections": [
        {
            "id": "x-analysis",
            "title": "التحليل على منصة X",
            "subtitle_en": "X Platform Analysis",
            "parts": ["part1"],
            "subsections": [
                "أنواع المنشورات",
                "البصمة الرقمية",
                "أبرز الوسوم",
                "أبرز الحسابات",
                "تحليل المشاعر",
                "تحليل الوصول",
                "ذروات الظهور",
                "فجوات التواصل على X"
            ]
        },
        {
            "id": "news-analysis",
            "title": "التحليل الصحفي والإخباري",
            "subtitle_en": "News & Press Analysis",
            "parts": ["part2"],
            "subsections": [
                "نظرة عامة على التغطية الإخبارية",
                "القراءة الاستراتيجية",
                "ذروات الأخبار",
                "المتصدرون شهرياً",
                "أبرز المواضيع",
                "المتصدرون صحفياً",
                "فجوات التواصل الصحفي"
            ]
        },
        {
            "id": "media-image-study",
            "title": "دراسة الصورة الإعلامية",
            "subtitle_en": "Media Image Study",
            "parts": ["part3", "part4", "part5", "part6"],
            "subsections": [
                "01. نظرة عامة على الدراسة",
                "02. تحليل المشاعر",
                "03. الصور النمطية",
                "04. فجوات المعرفة",
                "05. القضايا الحرجة",
                "06. الرسائل المتداولة",
                "07. شرائح الجمهور",
                "08. الأطر المفهومية",
                "09. هوية الوقف",
                "10. مستوى التفاعل",
                "11. مؤشرات الثقة",
                "12. السيناريو الحالي مقابل المستهدف",
                "13. التوصيات الاستراتيجية"
            ]
        }
    ],
    
    "files": {
        "part1": "waqf_media_performance_part1.py",
        "part2": "waqf_media_performance_part2.py",
        "part3": "waqf_media_performance_part3.py",
        "part4": "waqf_media_performance_part4.py",
        "part5": "waqf_media_performance_part5.py",
        "part6": "waqf_media_performance_part6.py"
    }
}


# ═══════════════════════════════════════════════════════════════════════════
# دوال الوصول الموحدة
# ═══════════════════════════════════════════════════════════════════════════

def get_full_media_performance_data():
    """الحصول على جميع بيانات الأداء الإعلامي"""
    return {
        # Part 1: X Analysis
        "x_analysis": {
            "post_types": POST_TYPES_ANALYSIS,
            "digital_footprint": DIGITAL_FOOTPRINT,
            "hashtags": TOP_HASHTAGS,
            "accounts": TOP_ACCOUNTS,
            "sentiment": SENTIMENT_ANALYSIS,
            "reach": REACH_ANALYSIS,
            "peaks": VISIBILITY_PEAKS,
            "gaps": COMMUNICATION_GAPS_X
        },
        
        # Part 2: News Analysis
        "news_analysis": {
            "overview": NEWS_ANALYSIS_OVERVIEW,
            "strategic_reading": STRATEGIC_READING,
            "peaks": NEWS_PEAKS,
            "monthly_leaders": MONTHLY_LEADERS,
            "topics": TOP_NEWS_TOPICS,
            "press_leaders": PRESS_LEADERS,
            "gaps": PRESS_COMMUNICATION_GAPS
        },
        
        # Part 3-6: Media Image Study
        "media_image_study": {
            "overview": STUDY_OVERVIEW,
            "sentiment": SENTIMENT_SECTION,
            "stereotypes": STEREOTYPES_SECTION,
            "knowledge_gaps": KNOWLEDGE_GAPS_SECTION,
            "sensitive_issues": SENSITIVE_ISSUES_SECTION,
            "key_messages": KEY_MESSAGES_SECTION,
            "audience_segments": AUDIENCE_SEGMENTS_SECTION,
            "frames": CONCEPTUAL_FRAMES_SECTION,
            "brand_personality": BRAND_PERSONALITY_SECTION,
            "engagement": ENGAGEMENT_LEVEL_SECTION,
            "trust": TRUST_INDICATORS_SECTION,
            "scenarios": SCENARIOS_SECTION,
            "recommendations": STRATEGIC_RECOMMENDATIONS_SECTION
        }
    }


def print_full_summary():
    """طباعة ملخص شامل لتاب الأداء الإعلامي"""
    print("=" * 70)
    print("📊 تقرير الأداء الإعلامي - الهيئة العامة للأوقاف")
    print("=" * 70)
    
    print("\n" + "─" * 70)
    print("📱 الجزء الأول: التحليل على منصة X")
    print("─" * 70)
    print(f"  • أنواع المنشورات: {len(POST_TYPES_ANALYSIS['types'])} أنواع")
    print(f"  • الوسوم الرئيسية: {len(get_all_hashtags())} وسم")
    print(f"  • الحسابات المؤثرة: {len(get_top_accounts_list())} حساب")
    print(f"  • ذروات الظهور: {len(get_visibility_peaks())} ذروات")
    print(f"  • فجوات التواصل: {len(get_communication_gaps())} فجوات")
    
    print("\n" + "─" * 70)
    print("📰 الجزء الثاني: التحليل الصحفي")
    print("─" * 70)
    print(f"  • المواضيع الرئيسية: {len(TOP_NEWS_TOPICS['topics'])} مواضيع")
    print(f"  • ذروات الأخبار: {len(NEWS_PEAKS['peaks'])} ذروات")
    print(f"  • فجوات صحفية: {len(get_press_gaps())} فجوات")
    
    print("\n" + "─" * 70)
    print("🔍 الجزء الثالث: دراسة الصورة الإعلامية")
    print("─" * 70)
    print(f"  • الصور النمطية: {len(get_all_stereotypes())} صور")
    print(f"  • فجوات المعرفة: {len(get_knowledge_gaps())} فجوات")
    print(f"  • القضايا الحرجة: {len(get_sensitive_issues())} قضايا")
    print(f"  • الرسائل المتداولة: {len(get_key_messages())} رسائل")
    print(f"  • شرائح الجمهور: {len(get_audience_segments())} شرائح")
    print(f"  • الأطر المفهومية: {len(get_conceptual_frames())} إطارات")
    print(f"  • سمات الهوية: {len(get_personality_traits())} سمات")
    
    print("\n" + "─" * 70)
    print("📈 مؤشرات الأداء الرئيسية")
    print("─" * 70)
    trust = get_trust_score()
    print(f"  • درجة الثقة: {trust['overall']}/100")
    print(f"  • التوصيات الاستراتيجية: {len(get_strategic_recommendations())} توصيات")
    
    print("\n" + "═" * 70)
    print("✅ تم تحميل جميع البيانات بنجاح")
    print("═" * 70)


# ═══════════════════════════════════════════════════════════════════════════
# نقطة الدخول
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print_full_summary()
