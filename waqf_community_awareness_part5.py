# -*- coding: utf-8 -*-
"""
محتوى تاب الوعي المجتمعي - الجزء الخامس
مستوى التفاعل ومؤشرات الثقة
الهيئة العامة للأوقاف - تقرير تحليل السمعة الرقمية
"""

# ═══════════════════════════════════════════════════════════════════════════
# القسم 09: مستوى التفاعل (Engagement Level)
# ═══════════════════════════════════════════════════════════════════════════

ENGAGEMENT_SECTION = {
    "section_number": "09",
    "title": "مستوى التفاعل",
    "subtitle_en": "Engagement Level",
    
    "intro": {
        "title": "تفاعل الجمهور مع محتوى الوقف",
        "text": "رصد مستوى تفاعل الجمهور مع المحتوى المتعلق بالأوقاف في وسائل الإعلام والمنصات الاجتماعية"
    },
    
    # إحصائيات التفاعل الرئيسية
    "main_stats": [
        {
            "icon": "📊",
            "value": "متوسط",
            "label": "مستوى التفاعل العام",
            "trend": "neutral",
            "description": "تفاعل معتدل يحتاج لتحفيز"
        },
        {
            "icon": "💬",
            "value": "2.3K",
            "label": "متوسط التعليقات الشهرية",
            "trend": "up",
            "description": "ارتفاع ملحوظ في المناقشات"
        },
        {
            "icon": "🔄",
            "value": "15K",
            "label": "متوسط إعادة التغريد",
            "trend": "up",
            "description": "انتشار جيد للمحتوى"
        },
        {
            "icon": "❤️",
            "value": "45K",
            "label": "متوسط الإعجابات الشهرية",
            "trend": "stable",
            "description": "تقدير إيجابي مستقر"
        }
    ],
    
    # تحليل التفاعل حسب نوع المحتوى
    "content_engagement": {
        "title": "التفاعل حسب نوع المحتوى",
        "types": [
            {
                "type": "success_stories",
                "icon": "🏆",
                "label": "قصص النجاح",
                "engagement_level": 85,
                "color": "green",
                "insight": "أعلى تفاعل - القصص الإنسانية تجذب الجمهور"
            },
            {
                "type": "donation_campaigns",
                "icon": "💰",
                "label": "حملات التبرع",
                "engagement_level": 78,
                "color": "blue",
                "insight": "تفاعل مرتفع خاصة في المناسبات الدينية"
            },
            {
                "type": "educational",
                "icon": "📚",
                "label": "المحتوى التعليمي",
                "engagement_level": 55,
                "color": "yellow",
                "insight": "تفاعل متوسط - يحتاج لتبسيط وإبداع"
            },
            {
                "type": "news",
                "icon": "📰",
                "label": "الأخبار الرسمية",
                "engagement_level": 40,
                "color": "orange",
                "insight": "تفاعل منخفض نسبياً - طابع رسمي جاف"
            },
            {
                "type": "statistics",
                "icon": "📈",
                "label": "الإحصائيات والأرقام",
                "engagement_level": 35,
                "color": "red",
                "insight": "أقل تفاعل - تحتاج لتقديم بصري جذاب"
            }
        ]
    },
    
    # بطاقات تحليل التفاعل
    "analysis_cards": [
        {
            "icon": "⏰",
            "card_type": "timing",
            "title": "أوقات الذروة",
            "stats": [
                {"label": "بعد صلاة الجمعة", "percentage": 40},
                {"label": "رمضان والمناسبات الدينية", "percentage": 65},
                {"label": "نهاية العام (ديسمبر)", "percentage": 35}
            ],
            "insight": "التفاعل يرتفع مع المناسبات الدينية والشعور بالمسؤولية الاجتماعية"
        },
        {
            "icon": "👥",
            "card_type": "demographics",
            "title": "الفئات الأكثر تفاعلاً",
            "segments": [
                {"segment": "كبار السن (55+)", "engagement": "عالي جداً", "icon": "👴"},
                {"segment": "الفئة المتوسطة (35-54)", "engagement": "متوسط-مرتفع", "icon": "👨"},
                {"segment": "الشباب (18-34)", "engagement": "منخفض", "icon": "👦"},
                {"segment": "المرأة", "engagement": "متوسط", "icon": "👩"}
            ],
            "gap_note": "فجوة واضحة في تفاعل الشباب تستدعي محتوى موجه"
        },
        {
            "icon": "📱",
            "card_type": "platforms",
            "title": "التفاعل حسب المنصة",
            "platforms": [
                {"name": "تويتر/إكس", "icon": "𝕏", "engagement": 75, "note": "المنصة الرئيسية للنقاش"},
                {"name": "إنستجرام", "icon": "📸", "engagement": 60, "note": "محتوى بصري جذاب"},
                {"name": "يوتيوب", "icon": "▶️", "engagement": 45, "note": "فيديوهات طويلة أقل تفاعلاً"},
                {"name": "سناب شات", "icon": "👻", "engagement": 30, "note": "ضعيف جداً مع الشباب"},
                {"name": "تيك توك", "icon": "🎵", "engagement": 20, "note": "شبه غائب"}
            ]
        },
        {
            "icon": "💡",
            "card_type": "triggers",
            "title": "محفزات التفاعل",
            "positive_triggers": [
                {"icon": "❤️", "text": "القصص الإنسانية المؤثرة"},
                {"icon": "🎯", "text": "الأرقام الواضحة للإنجازات"},
                {"icon": "🌟", "text": "شهادات المستفيدين"},
                {"icon": "📢", "text": "دعوات العمل المباشرة"}
            ],
            "negative_triggers": [
                {"icon": "📋", "text": "اللغة الرسمية الجافة"},
                {"icon": "📄", "text": "المحتوى النصي الطويل"},
                {"icon": "🔄", "text": "تكرار المعلومات ذاتها"},
                {"icon": "🔇", "text": "غياب التفاعل مع التعليقات"}
            ]
        }
    ],
    
    # توصيات تحسين التفاعل
    "recommendations": {
        "title": "توصيات لتحسين التفاعل",
        "items": [
            {
                "icon": "🎬",
                "title": "المحتوى المرئي القصير",
                "description": "فيديوهات 30-60 ثانية تروي قصص الأثر",
                "priority": "عالية"
            },
            {
                "icon": "🎯",
                "title": "استهداف الشباب",
                "description": "محتوى عصري على تيك توك وسناب شات",
                "priority": "عالية"
            },
            {
                "icon": "💬",
                "title": "التفاعل المباشر",
                "description": "الرد على التعليقات والأسئلة بانتظام",
                "priority": "متوسطة"
            },
            {
                "icon": "📊",
                "title": "إنفوجرافيك",
                "description": "تحويل الإحصائيات لمحتوى بصري سهل",
                "priority": "متوسطة"
            }
        ]
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# القسم 10: مؤشرات الثقة (Trust Indicators)
# ═══════════════════════════════════════════════════════════════════════════

TRUST_INDICATORS_SECTION = {
    "section_number": "10",
    "title": "مؤشرات الثقة",
    "subtitle_en": "Trust Indicators",
    
    "intro": {
        "title": "قياس مستوى الثقة المجتمعية في الوقف",
        "text": "تحليل مؤشرات الثقة العامة تجاه قطاع الوقف ومؤسساته من خلال رصد المحتوى الإعلامي والتفاعلات الاجتماعية"
    },
    
    # مقياس الثقة العام
    "trust_meter": {
        "title": "مستوى الثقة العام",
        "overall_score": 65,
        "max_score": 100,
        "rating": "متوسط-مرتفع",
        "trend": "تصاعدي",
        "description": "ثقة إيجابية تتعزز تدريجياً مع الإصلاحات",
        "meter_segments": [
            {"range": "0-25", "label": "ثقة منخفضة", "color": "red"},
            {"range": "26-50", "label": "ثقة متوسطة", "color": "orange"},
            {"range": "51-75", "label": "ثقة جيدة", "color": "yellow"},
            {"range": "76-100", "label": "ثقة عالية", "color": "green"}
        ],
        "current_position": "ثقة جيدة (65/100)"
    },
    
    # مؤشرات الثقة التفصيلية
    "trust_stats": [
        {
            "icon": "🏛️",
            "indicator": "الثقة في الهيئة العامة للأوقاف",
            "score": 75,
            "trend": "up",
            "insight": "ثقة مرتفعة بفضل الإشراف الحكومي الرسمي"
        },
        {
            "icon": "📱",
            "indicator": "الثقة في منصة إحسان",
            "score": 85,
            "trend": "up",
            "insight": "أعلى مستوى ثقة بين المنصات الوقفية"
        },
        {
            "icon": "🏢",
            "indicator": "الثقة في الأوقاف الخاصة",
            "score": 45,
            "trend": "neutral",
            "insight": "ثقة متحفظة تحتاج لشفافية أكبر"
        },
        {
            "icon": "👨‍💼",
            "indicator": "الثقة في نُظّار الأوقاف",
            "score": 50,
            "trend": "up",
            "insight": "تحسن تدريجي مع أنظمة الحوكمة الجديدة"
        },
        {
            "icon": "💰",
            "indicator": "الثقة في إدارة أموال الوقف",
            "score": 55,
            "trend": "up",
            "insight": "تحسن ملحوظ مع الإفصاح عن الاستثمارات"
        },
        {
            "icon": "📊",
            "indicator": "الثقة في التقارير والبيانات",
            "score": 60,
            "trend": "up",
            "insight": "إيجابية مع كل تقرير سنوي جديد"
        }
    ],
    
    # عوامل بناء الثقة
    "trust_builders": {
        "title": "عوامل تعزز الثقة",
        "factors": [
            {
                "icon": "👁️",
                "factor": "الشفافية",
                "weight": 30,
                "elements": ["تقارير مالية منشورة", "إفصاح عن المشاريع", "بيانات الأداء"]
            },
            {
                "icon": "✅",
                "factor": "الإنجاز الملموس",
                "weight": 25,
                "elements": ["مشاريع مكتملة", "مستفيدون فعليون", "أثر واضح"]
            },
            {
                "icon": "🏛️",
                "factor": "الإشراف الحكومي",
                "weight": 20,
                "elements": ["رقابة رسمية", "أنظمة واضحة", "محاسبة"]
            },
            {
                "icon": "🌟",
                "factor": "السمعة المؤسسية",
                "weight": 15,
                "elements": ["تاريخ نظيف", "قيادات موثوقة", "شراكات قوية"]
            },
            {
                "icon": "💬",
                "factor": "التواصل الفعّال",
                "weight": 10,
                "elements": ["الرد على الاستفسارات", "الشكاوى المعالجة", "القنوات المتاحة"]
            }
        ]
    },
    
    # عوامل تقويض الثقة
    "trust_barriers": {
        "title": "عوامل تُضعف الثقة",
        "barriers": [
            {
                "icon": "🔒",
                "barrier": "غياب الشفافية",
                "impact": "عالي",
                "description": "عدم نشر تقارير مالية أو بيانات أداء"
            },
            {
                "icon": "⚠️",
                "barrier": "حوادث سابقة",
                "impact": "متوسط-عالي",
                "description": "قضايا تلاعب أو إهمال في إدارة أوقاف"
            },
            {
                "icon": "📉",
                "barrier": "الأداء الضعيف",
                "impact": "متوسط",
                "description": "أوقاف معطلة أو عوائد متدنية"
            },
            {
                "icon": "🔇",
                "barrier": "ضعف التواصل",
                "impact": "متوسط",
                "description": "عدم الرد على التساؤلات والشكاوى"
            },
            {
                "icon": "❓",
                "barrier": "الغموض التشريعي",
                "impact": "منخفض-متوسط",
                "description": "عدم وضوح الأنظمة والإجراءات"
            }
        ]
    },
    
    # الثقة حسب الشرائح
    "trust_by_segment": {
        "title": "الثقة حسب شرائح الجمهور",
        "segments": [
            {
                "segment": "المتدينون التقليديون",
                "icon": "🕌",
                "trust_level": 80,
                "description": "ثقة عالية مبنية على القيم الدينية"
            },
            {
                "segment": "كبار السن",
                "icon": "👴",
                "trust_level": 75,
                "description": "ثقة مبنية على التجربة والتاريخ"
            },
            {
                "segment": "رجال الأعمال",
                "icon": "💼",
                "trust_level": 60,
                "description": "ثقة حذرة مرتبطة بالعوائد والشفافية"
            },
            {
                "segment": "المتعلمون/المثقفون",
                "icon": "🎓",
                "trust_level": 55,
                "description": "ثقة مشروطة بالحوكمة والشفافية"
            },
            {
                "segment": "الشباب",
                "icon": "👦",
                "trust_level": 45,
                "description": "ثقة منخفضة نسبياً مع استعداد للتحسن"
            },
            {
                "segment": "المتشككون",
                "icon": "🤔",
                "trust_level": 25,
                "description": "ثقة ضعيفة تحتاج جهوداً مكثفة"
            }
        ]
    },
    
    # توصيات بناء الثقة
    "trust_recommendations": {
        "title": "توصيات لتعزيز الثقة",
        "items": [
            {
                "priority": 1,
                "icon": "📊",
                "title": "الإفصاح الدوري",
                "description": "نشر تقارير مالية ربع سنوية وسنوية"
            },
            {
                "priority": 2,
                "icon": "🎯",
                "title": "قصص الأثر",
                "description": "توثيق ونشر قصص المستفيدين الحقيقية"
            },
            {
                "priority": 3,
                "icon": "💬",
                "title": "قنوات التواصل",
                "description": "إتاحة قنوات للاستفسار والشكاوى"
            },
            {
                "priority": 4,
                "icon": "⚡",
                "title": "سرعة الاستجابة",
                "description": "معالجة الملاحظات والشكاوى بسرعة"
            },
            {
                "priority": 5,
                "icon": "🤝",
                "title": "المشاركة المجتمعية",
                "description": "إشراك الجمهور في قرارات الأوقاف"
            }
        ]
    }
}


# ═══════════════════════════════════════════════════════════════════════════
# دوال مساعدة
# ═══════════════════════════════════════════════════════════════════════════

def get_engagement_stats():
    """الحصول على إحصائيات التفاعل الرئيسية"""
    return ENGAGEMENT_SECTION["main_stats"]


def get_content_engagement():
    """الحصول على تحليل التفاعل حسب نوع المحتوى"""
    return ENGAGEMENT_SECTION["content_engagement"]["types"]


def get_trust_score():
    """الحصول على مستوى الثقة العام"""
    return TRUST_INDICATORS_SECTION["trust_meter"]


def get_trust_indicators():
    """الحصول على مؤشرات الثقة التفصيلية"""
    return TRUST_INDICATORS_SECTION["trust_stats"]


def get_trust_by_segment():
    """الحصول على الثقة حسب شرائح الجمهور"""
    return TRUST_INDICATORS_SECTION["trust_by_segment"]["segments"]


def get_trust_builders():
    """الحصول على عوامل تعزيز الثقة"""
    return TRUST_INDICATORS_SECTION["trust_builders"]["factors"]


def print_part5_summary():
    """طباعة ملخص الجزء الخامس"""
    print("=" * 60)
    print("الوعي المجتمعي - الجزء الخامس")
    print("=" * 60)
    
    print("\n📊 الأقسام المتضمنة:")
    print("  9. مستوى التفاعل (Engagement Level)")
    print("  10. مؤشرات الثقة (Trust Indicators)")
    
    print(f"\n📈 إحصائيات التفاعل: {len(get_engagement_stats())}")
    for stat in get_engagement_stats():
        print(f"   {stat['icon']} {stat['label']}: {stat['value']}")
    
    print(f"\n🛡️ مؤشرات الثقة: {len(get_trust_indicators())}")
    for indicator in get_trust_indicators():
        print(f"   {indicator['icon']} {indicator['indicator']}: {indicator['score']}/100")
    
    trust_meter = get_trust_score()
    print(f"\n📊 مستوى الثقة العام: {trust_meter['overall_score']}/100 ({trust_meter['rating']})")


if __name__ == "__main__":
    print_part5_summary()
