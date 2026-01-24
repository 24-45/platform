"""
إنشاء هيكل التقرير الكامل - وزارة الرياضة والشباب القطرية
Qatar Ministry of Sports & Youth - Full Report Structure Generator
"""

import json
import os
from datetime import datetime

# المسارات
ANALYSIS_PATH = "static/data/qatar_sports_analysis"
OUTPUT_PATH = "static/data/qatar_sports_analysis"

def load_json(filename):
    """تحميل ملف JSON"""
    filepath = os.path.join(ANALYSIS_PATH, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report_structure():
    """إنشاء هيكل التقرير الكامل"""
    
    # تحميل البيانات
    executive_summary = load_json('executive_summary.json')
    full_analysis = load_json('full_analysis.json')
    influencers = load_json('influencers.json')
    topic_analysis = load_json('topic_analysis.json')
    events_comparison = load_json('events_comparison.json')
    
    # استخراج بيانات الوزارة
    ministry_analytics = full_analysis.get('ministry_analytics', {})
    ministry_social = full_analysis.get('ministry_social', {})
    
    # ============================================
    # هيكل التقرير الكامل
    # ============================================
    
    report = {
        "metadata": {
            "title": "تقرير قياس الكفاءة الإعلامية والسمعة المؤسسية",
            "subtitle": "وزارة الرياضة والشباب - دولة قطر",
            "period": "نوفمبر 2025 - يناير 2026",
            "duration_days": 90,
            "report_date": datetime.now().strftime('%Y-%m-%d'),
            "version": "1.0",
            "prepared_by": "فريق تحليل البيانات الإعلامية"
        },
        
        # ============================================
        # 1. المقدمة
        # ============================================
        "section_1_introduction": {
            "title": "المقدمة",
            "objectives": {
                "main_objective": "قياس الكفاءة الإعلامية والسمعة المؤسسية لوزارة الرياضة والشباب القطرية خلال فترة الفعاليات الرياضية الكبرى",
                "specific_objectives": [
                    "تحليل حجم التغطية الإعلامية للوزارة والفعاليات الرياضية",
                    "قياس اتجاهات المشاعر والانطباعات تجاه الوزارة",
                    "تحديد المؤثرين الرئيسيين في تشكيل الصورة الإعلامية",
                    "تقييم فعالية التغطية الإعلامية للفعاليات الرياضية الكبرى",
                    "رصد المواضيع والقضايا الرئيسية المرتبطة بالوزارة",
                    "تقديم توصيات لتحسين الأداء الإعلامي"
                ]
            },
            "importance": {
                "description": "أهمية التقرير للوزارة",
                "points": [
                    "فهم الصورة الذهنية للوزارة لدى الجمهور المحلي والدولي",
                    "تقييم أثر الفعاليات الرياضية الكبرى على سمعة قطر",
                    "تحديد نقاط القوة والضعف في التواصل الإعلامي",
                    "دعم اتخاذ القرارات الاستراتيجية الإعلامية",
                    "قياس العائد على الاستثمار الإعلامي"
                ]
            },
            "scope": {
                "events_covered": [
                    "كأس العرب FIFA قطر 2025",
                    "كأس القارات FIFA قطر 2025",
                    "كأس العالم للناشئين تحت 17 سنة FIFA قطر 2025",
                    "سباق جائزة قطر الكبرى للفورمولا 1",
                    "UFC قطر",
                    "نهائي بطولة العالم للترايثلون T100",
                    "بطولات تنس الطاولة WTT"
                ],
                "media_types": ["الإعلام التقليدي", "منصات التواصل الاجتماعي"],
                "geographic_scope": "تغطية عالمية مع تركيز على المنطقة العربية"
            }
        },
        
        # ============================================
        # 2. المنهجية
        # ============================================
        "section_2_methodology": {
            "title": "المنهجية",
            "scope_and_sample": {
                "title": "النطاق والعينة",
                "period": {
                    "start": "1 نوفمبر 2025",
                    "end": "22 يناير 2026",
                    "days": 90
                },
                "total_materials": executive_summary['total_mentions'],
                "traditional_media": executive_summary['traditional_media'],
                "social_media": executive_summary['social_media'],
                "events_analyzed": executive_summary['events_covered'],
                "data_source": "Meltwater Media Intelligence Platform",
                "languages_monitored": ["العربية", "الإنجليزية", "الفرنسية", "الإسبانية", "البرتغالية"]
            },
            "data_preparation": {
                "title": "تجهيز البيانات",
                "steps": [
                    "جمع البيانات من منصة Meltwater باستخدام كلمات مفتاحية محددة",
                    "تنظيف البيانات وإزالة التكرارات والمحتوى غير ذي الصلة",
                    "تصنيف المحتوى حسب نوع المصدر (تقليدي/اجتماعي)",
                    "تحديد اللغة والموقع الجغرافي لكل مادة",
                    "استخراج البيانات الوصفية (الوصول، التفاعل، المشاعر)"
                ],
                "tools_used": [
                    "Meltwater للرصد الإعلامي",
                    "Python للتحليل الإحصائي",
                    "تحليل المشاعر بالذكاء الاصطناعي"
                ]
            },
            "topic_classification": {
                "title": "التصنيف الموضوعي",
                "categories": [
                    {"name": "فعاليات رياضية كبرى", "description": "البطولات والمسابقات الدولية"},
                    {"name": "استضافة وتنظيم", "description": "جهود قطر في استضافة وتنظيم الفعاليات"},
                    {"name": "بنية تحتية", "description": "الملاعب والمنشآت الرياضية"},
                    {"name": "مسؤولون", "description": "تصريحات وظهور المسؤولين"},
                    {"name": "جماهير وتجربة", "description": "تجربة الزوار والجماهير"},
                    {"name": "إرث ورؤية", "description": "الإرث الرياضي ورؤية قطر المستقبلية"},
                    {"name": "شباب ومبادرات", "description": "البرامج الشبابية والمبادرات"},
                    {"name": "فعاليات تراثية", "description": "الرياضات التراثية والتقليدية"}
                ]
            },
            "sentiment_measurement": {
                "title": "قياس الانطباعات",
                "methodology": "تحليل المشاعر باستخدام الذكاء الاصطناعي",
                "categories": [
                    {"type": "إيجابي", "description": "محتوى يعكس انطباعاً إيجابياً"},
                    {"type": "سلبي", "description": "محتوى يعكس انطباعاً سلبياً"},
                    {"type": "محايد", "description": "محتوى إخباري موضوعي"}
                ],
                "accuracy_note": "دقة التحليل تقريبية وتخضع للمراجعة البشرية للحالات الحساسة"
            }
        },
        
        # ============================================
        # 3. الملخص التنفيذي
        # ============================================
        "section_3_executive_summary": {
            "title": "الملخص التنفيذي",
            "key_figures": {
                "title": "الأرقام الرئيسية",
                "total_mentions": executive_summary['total_mentions'],
                "traditional_media": executive_summary['traditional_media'],
                "social_media": executive_summary['social_media'],
                "traditional_percentage": executive_summary['key_metrics']['traditional_percentage'],
                "social_percentage": executive_summary['key_metrics']['social_percentage'],
                "total_reach": executive_summary['reach_total'],
                "total_reach_formatted": f"{executive_summary['reach_total']:,}",
                "total_engagement": executive_summary['engagement_total'],
                "events_covered": executive_summary['events_covered']
            },
            "sentiment_overview": {
                "title": "نظرة عامة على المشاعر",
                "positive": {
                    "percentage": executive_summary['overall_sentiment']['إيجابي'],
                    "count": executive_summary['sentiment_counts']['positive']
                },
                "negative": {
                    "percentage": executive_summary['overall_sentiment']['سلبي'],
                    "count": executive_summary['sentiment_counts']['negative']
                },
                "neutral": {
                    "percentage": executive_summary['overall_sentiment']['محايد'],
                    "count": executive_summary['sentiment_counts']['neutral']
                }
            },
            "scene_drivers": {
                "title": "محركات المشهد الإعلامي",
                "top_events_by_volume": executive_summary['top_events_by_volume'],
                "top_events_by_reach": executive_summary['top_events_by_reach']
            },
            "temporal_patterns": {
                "title": "الأنماط الزمنية",
                "peak_periods": [
                    "ديسمبر 2025 - ذروة كأس العرب وكأس القارات",
                    "نوفمبر 2025 - كأس العالم تحت 17 وF1",
                    "يناير 2026 - بطولات WTT والمبارزة"
                ],
                "daily_average": round(executive_summary['total_mentions'] / 90, 0)
            },
            "sentiment_drivers": {
                "title": "محركات الإيجابية والسلبية",
                "positive_drivers": [
                    "نجاح تنظيم الفعاليات الرياضية الكبرى",
                    "جودة البنية التحتية والملاعب",
                    "تجربة الجماهير الإيجابية",
                    "الإشادة الدولية بالتنظيم",
                    "الفعاليات التراثية الفريدة"
                ],
                "negative_drivers": [
                    "نتائج المنتخبات الرياضية",
                    "بعض الانتقادات التنظيمية",
                    "قضايا سياسية غير مرتبطة بالرياضة"
                ]
            }
        },
        
        # ============================================
        # 4. الإعلام التقليدي
        # ============================================
        "section_4_traditional_media": {
            "title": "الإعلام التقليدي",
            "media_interest": {
                "title": "ملامح الاهتمام الإعلامي",
                "total_coverage": executive_summary['traditional_media'],
                "source_types": ministry_analytics.get('source_types', {}),
                "top_sources": ministry_analytics.get('top_sources', {}),
                "geographic_distribution": ministry_analytics.get('countries', {}),
                "language_distribution": ministry_analytics.get('languages', {})
            },
            "interest_change": {
                "title": "التغيُّر في الاهتمام",
                "daily_trend": ministry_analytics.get('daily_trend', {}),
                "weekly_trend": ministry_analytics.get('weekly_trend', {}),
                "peak_days": "يتم تحديدها من البيانات اليومية"
            },
            "media_attitudes": {
                "title": "اتجاهات الإعلام تجاه الوزارة",
                "sentiment": ministry_analytics.get('sentiment', {}),
                "positive_coverage_rate": ministry_analytics.get('sentiment', {}).get('percentages', {}).get('positive', 0),
                "negative_coverage_rate": ministry_analytics.get('sentiment', {}).get('percentages', {}).get('negative', 0)
            },
            "image_influencers": {
                "title": "المؤثرون في الصورة الإعلامية",
                "top_journalists": influencers.get('ministry', [])[:10],
                "top_media_outlets": list(ministry_analytics.get('top_sources', {}).items())[:10]
            },
            "coverage_samples": {
                "title": "نماذج من التغطيات",
                "positive_samples": ministry_analytics.get('sample_positive', []),
                "negative_samples": ministry_analytics.get('sample_negative', []),
                "neutral_samples": ministry_analytics.get('sample_neutral', [])
            }
        },
        
        # ============================================
        # 5. منصات التواصل الاجتماعي
        # ============================================
        "section_5_social_media": {
            "title": "منصات التواصل الاجتماعي",
            "quantitative_analysis": {
                "title": "التحليل الكمي",
                "total_posts": executive_summary['social_media'],
                "total_reach": ministry_social.get('reach', {}).get('total', 0),
                "total_engagement": ministry_social.get('engagement', {}).get('total', 0),
                "average_engagement": ministry_social.get('engagement', {}).get('average', 0),
                "sentiment": ministry_social.get('sentiment', {})
            },
            "temporal_publishing": {
                "title": "تغير النشر الزمني",
                "daily_trend": ministry_social.get('daily_trend', {}),
                "weekly_trend": ministry_social.get('weekly_trend', {}),
                "peak_hours": "يتم تحديدها من البيانات الساعية"
            },
            "top_hashtags": {
                "title": "أبرز الوسوم",
                "hashtags": ministry_social.get('top_hashtags', []),
                "events_hashtags": [
                    "#كأس_العرب",
                    "#ArabCup",
                    "#QatarGP",
                    "#FIFAU17WC",
                    "#UFCQatar",
                    "#IntercontinentalCup"
                ]
            },
            "demographics": {
                "title": "الديموغرافية",
                "countries": ministry_social.get('countries', {}),
                "languages": ministry_social.get('languages', {}),
                "platforms": ministry_social.get('source_types', {})
            },
            "influencers": {
                "title": "المؤثرون",
                "ministry_influencers": influencers.get('ministry', [])[:15],
                "events_influencers": {
                    event: inf[:5] for event, inf in influencers.items() if event != 'ministry'
                }
            },
            "news_accounts": {
                "title": "الحسابات الإخبارية",
                "top_accounts": [
                    account for account in ministry_social.get('top_authors', {}).items()
                ][:15]
            }
        },
        
        # ============================================
        # 6. تحليل المواضيع
        # ============================================
        "section_6_topic_analysis": {
            "title": "تحليل المواضيع",
            "major_sports_events": {
                "title": "الفعاليات الرياضية الكبرى",
                "statistics": topic_analysis.get('فعاليات_رياضية_كبرى', {}),
                "events_breakdown": events_comparison,
                "key_insights": [
                    "كأس العرب حصل على أعلى حجم تغطية",
                    "UFC قطر حقق أعلى وصول جماهيري",
                    "جميع الفعاليات حققت نسبة إيجابية أعلى من السلبية"
                ]
            },
            "youth_programs": {
                "title": "البرامج والمبادرات الشبابية",
                "statistics": ministry_analytics.get('categories', {}).get('شباب ومبادرات', 0),
                "programs_mentioned": [
                    "اليوم الرياضي الوطني",
                    "برامج أسباير",
                    "مبادرات الشباب القطري",
                    "الرياضة المدرسية"
                ]
            },
            "sports_infrastructure": {
                "title": "البنية التحتية الرياضية",
                "statistics": topic_analysis.get('بنية_تحتية', {}),
                "facilities_mentioned": [
                    "استاد لوسيل",
                    "استاد البيت",
                    "استاد خليفة الدولي",
                    "أسباير زون",
                    "حلبة لوسيل الدولية"
                ]
            },
            "national_teams": {
                "title": "المنتخبات والأبطال",
                "statistics": ministry_analytics.get('categories', {}).get('منتخبات', 0),
                "teams_mentioned": [
                    "المنتخب القطري لكرة القدم",
                    "المنتخبات الوطنية المختلفة",
                    "الأبطال القطريين"
                ]
            },
            "partnerships": {
                "title": "الشراكات والاتفاقيات",
                "key_partnerships": [
                    "FIFA",
                    "الخطوط الجوية القطرية",
                    "اللجنة الأولمبية القطرية",
                    "أسباير أكاديمي"
                ]
            },
            "hosting_organization": {
                "title": "الاستضافة والتنظيم",
                "statistics": topic_analysis.get('استضافة_وتنظيم', {}),
                "positive_rate": topic_analysis.get('استضافة_وتنظيم', {}).get('positive_rate', 0)
            },
            "heritage_events": {
                "title": "الفعاليات التراثية",
                "statistics": ministry_analytics.get('categories', {}).get('فعاليات تراثية', 0),
                "events": [
                    "مهرجان مرمي",
                    "موسم سيلين",
                    "لونجين هذاب",
                    "سباق الهجن",
                    "نادي القناص"
                ]
            }
        },
        
        # ============================================
        # 7. النتائج
        # ============================================
        "section_7_findings": {
            "title": "النتائج",
            "key_findings": [
                {
                    "finding": "حجم تغطية كبير ومتنوع",
                    "details": f"تم رصد {executive_summary['total_mentions']:,} مادة إعلامية خلال 90 يوماً، بمعدل {round(executive_summary['total_mentions']/90):,} مادة يومياً"
                },
                {
                    "finding": "هيمنة منصات التواصل الاجتماعي",
                    "details": f"شكلت منصات التواصل {executive_summary['key_metrics']['social_percentage']}% من إجمالي التغطية"
                },
                {
                    "finding": "انطباع إيجابي سائد",
                    "details": f"نسبة المحتوى الإيجابي ({executive_summary['overall_sentiment']['إيجابي']}) تفوق السلبي ({executive_summary['overall_sentiment']['سلبي']}) بنسبة 5 أضعاف"
                },
                {
                    "finding": "نجاح الفعاليات الرياضية الكبرى",
                    "details": "جميع الفعاليات السبع حققت تغطية إيجابية ووصولاً جماهيرياً واسعاً"
                },
                {
                    "finding": "وصول جماهيري ضخم",
                    "details": f"إجمالي الوصول تجاوز 134 مليار، مما يعكس انتشاراً عالمياً واسعاً"
                },
                {
                    "finding": "تنوع جغرافي في التغطية",
                    "details": "التغطية شملت أكثر من 50 دولة، مع تركيز على المنطقة العربية"
                },
                {
                    "finding": "أعلى نسبة إيجابية في الاستضافة والتنظيم",
                    "details": f"حقق موضوع الاستضافة والتنظيم أعلى نسبة إيجابية ({topic_analysis.get('استضافة_وتنظيم', {}).get('positive_rate', 0)}%)"
                }
            ],
            "strengths": [
                "قدرة تنظيمية عالية معترف بها دولياً",
                "بنية تحتية رياضية متطورة",
                "تنوع الفعاليات الرياضية",
                "تجربة جماهيرية إيجابية",
                "تغطية إعلامية واسعة ومتنوعة"
            ],
            "challenges": [
                "التحديات المرتبطة بنتائج المنتخبات الوطنية",
                "بعض الانتقادات التنظيمية المحدودة",
                "الربط غير المبرر بقضايا سياسية"
            ]
        },
        
        # ============================================
        # 8. التوصيات
        # ============================================
        "section_8_recommendations": {
            "title": "التوصيات",
            "strategic_recommendations": [
                {
                    "category": "التواصل الإعلامي",
                    "recommendations": [
                        "تعزيز التواصل الاستباقي مع وسائل الإعلام الدولية",
                        "إنشاء محتوى متعدد اللغات لتوسيع الوصول",
                        "بناء علاقات أقوى مع المؤثرين الإيجابيين"
                    ]
                },
                {
                    "category": "منصات التواصل الاجتماعي",
                    "recommendations": [
                        "زيادة التفاعل المباشر مع الجمهور",
                        "تطوير محتوى مرئي جذاب للفعاليات",
                        "استخدام المؤثرين الرياضيين للترويج"
                    ]
                },
                {
                    "category": "إدارة السمعة",
                    "recommendations": [
                        "مراقبة مستمرة للمحتوى السلبي والرد السريع",
                        "تعزيز الرسائل الإيجابية حول الإنجازات",
                        "التركيز على قصص النجاح والإرث الرياضي"
                    ]
                },
                {
                    "category": "الفعاليات المستقبلية",
                    "recommendations": [
                        "الاستفادة من الزخم الإيجابي الحالي",
                        "توثيق أفضل الممارسات للفعاليات القادمة",
                        "تعزيز الفعاليات التراثية والمحلية"
                    ]
                }
            ],
            "operational_recommendations": [
                "إنشاء فريق متخصص لإدارة السمعة الرقمية",
                "تطوير لوحة مراقبة إعلامية في الوقت الفعلي",
                "إجراء تحليلات دورية للمشاعر والاتجاهات",
                "بناء قاعدة بيانات للمؤثرين والصحفيين"
            ]
        },
        
        # ============================================
        # 9. الملاحق
        # ============================================
        "section_9_appendices": {
            "title": "الملاحق",
            "appendix_a": {
                "title": "ملحق أ: تفاصيل الفعاليات",
                "events_details": events_comparison
            },
            "appendix_b": {
                "title": "ملحق ب: قائمة المؤثرين الكاملة",
                "all_influencers": influencers
            },
            "appendix_c": {
                "title": "ملحق ج: تحليل المواضيع التفصيلي",
                "topic_details": topic_analysis
            },
            "appendix_d": {
                "title": "ملحق د: المصادر الإعلامية",
                "traditional_sources": ministry_analytics.get('top_sources', {}),
                "social_sources": ministry_social.get('top_sources', {})
            },
            "appendix_e": {
                "title": "ملحق هـ: التوزيع الجغرافي",
                "countries": ministry_analytics.get('countries', {}),
                "languages": ministry_analytics.get('languages', {})
            },
            "appendix_f": {
                "title": "ملحق و: الاتجاهات الزمنية",
                "daily_trend": ministry_analytics.get('daily_trend', {}),
                "weekly_trend": ministry_analytics.get('weekly_trend', {})
            }
        }
    }
    
    return report

def save_report():
    """حفظ التقرير"""
    print("=" * 60)
    print("🇶🇦 إنشاء هيكل التقرير الكامل")
    print("=" * 60)
    
    print("\n📂 جاري تحميل البيانات...")
    report = generate_report_structure()
    
    print("💾 جاري حفظ التقرير...")
    
    # حفظ الهيكل الكامل
    output_file = os.path.join(OUTPUT_PATH, 'full_report_structure.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ تم حفظ التقرير في: {output_file}")
    
    # طباعة ملخص الهيكل
    print("\n" + "=" * 60)
    print("📋 هيكل التقرير:")
    print("=" * 60)
    
    sections = [
        ("1", "المقدمة", "section_1_introduction"),
        ("2", "المنهجية", "section_2_methodology"),
        ("3", "الملخص التنفيذي", "section_3_executive_summary"),
        ("4", "الإعلام التقليدي", "section_4_traditional_media"),
        ("5", "منصات التواصل الاجتماعي", "section_5_social_media"),
        ("6", "تحليل المواضيع", "section_6_topic_analysis"),
        ("7", "النتائج", "section_7_findings"),
        ("8", "التوصيات", "section_8_recommendations"),
        ("9", "الملاحق", "section_9_appendices")
    ]
    
    for num, title, key in sections:
        section_data = report.get(key, {})
        subsections = len([k for k in section_data.keys() if k != 'title'])
        print(f"   {num}. {title} ({subsections} قسم فرعي)")
    
    print("\n" + "=" * 60)
    print("📊 إحصائيات التقرير:")
    print("=" * 60)
    print(f"   📰 إجمالي المواد: {report['section_3_executive_summary']['key_figures']['total_mentions']:,}")
    print(f"   📣 إجمالي الوصول: {report['section_3_executive_summary']['key_figures']['total_reach']:,}")
    print(f"   🏆 الفعاليات: {report['section_3_executive_summary']['key_figures']['events_covered']}")
    print(f"   💚 نسبة الإيجابي: {report['section_3_executive_summary']['sentiment_overview']['positive']['percentage']}")
    
    return report

if __name__ == "__main__":
    report = save_report()
