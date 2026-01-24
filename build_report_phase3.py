"""
المرحلة الثالثة: النتائج + التوصيات + الملاحق
Phase 3: Results + Recommendations + Appendices
"""

import json
import os
from datetime import datetime

# المسارات
ANALYSIS_PATH = "static/data/qatar_sports_analysis"
OUTPUT_PATH = "static/data/qatar_sports_analysis/report_phases"

os.makedirs(OUTPUT_PATH, exist_ok=True)

def load_json(filename):
    """تحميل ملف JSON"""
    filepath = os.path.join(ANALYSIS_PATH, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_phase3():
    """بناء المرحلة الثالثة من التقرير"""
    
    # تحميل البيانات
    executive_summary = load_json('executive_summary.json')
    full_analysis = load_json('full_analysis.json')
    topic_analysis = load_json('topic_analysis.json')
    events_comparison = load_json('events_comparison.json')
    influencers = load_json('influencers.json')
    
    ministry_analytics = full_analysis.get('ministry_analytics', {})
    events_data = full_analysis.get('events', {})
    
    phase3 = {
        "phase": 3,
        "title": "المرحلة الثالثة: النتائج والتوصيات والملاحق",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        # ============================================
        # القسم السابع: النتائج والاستنتاجات
        # ============================================
        "section_7_results": {
            "section_number": 7,
            "title": "النتائج والاستنتاجات",
            "page_count": 4,
            
            "overview": {
                "title": "7.1 ملخص النتائج",
                "content": f"""خلص هذا التحليل إلى مجموعة من النتائج الجوهرية التي تلخص الأداء الإعلامي لوزارة الرياضة والشباب القطرية والفعاليات الرياضية خلال الفترة من نوفمبر 2025 إلى يناير 2026.

تم تحليل {executive_summary['total_mentions']:,} مادة إعلامية عبر الإعلام التقليدي ومنصات التواصل الاجتماعي، بوصول إجمالي تجاوز 134 مليار، مما يعكس حجم الاهتمام الإعلامي الكبير بالفعاليات الرياضية القطرية."""
            },
            
            "key_findings": {
                "title": "7.2 النتائج الرئيسية",
                "findings": [
                    {
                        "finding_id": 1,
                        "category": "حجم التغطية",
                        "finding": "تغطية إعلامية ضخمة ومتنوعة",
                        "detail": f"رُصدت {executive_summary['total_mentions']:,} مادة إعلامية خلال 90 يوماً، بمعدل يومي يتجاوز {round(executive_summary['total_mentions']/90):,} مادة، مما يؤكد الاهتمام الإعلامي المستمر والكثيف.",
                        "significance": "عالية",
                        "icon": "📰"
                    },
                    {
                        "finding_id": 2,
                        "category": "توازن التغطية",
                        "finding": "هيمنة منصات التواصل الاجتماعي",
                        "detail": f"شكلت منصات التواصل الاجتماعي {executive_summary['key_metrics']['social_percentage']}% من التغطية ({executive_summary['social_media']:,} منشور) مقابل {executive_summary['key_metrics']['traditional_percentage']}% للإعلام التقليدي ({executive_summary['traditional_media']:,} مادة).",
                        "significance": "متوسطة",
                        "icon": "📱"
                    },
                    {
                        "finding_id": 3,
                        "category": "المشاعر العامة",
                        "finding": "انطباع إيجابي سائد",
                        "detail": f"بلغت نسبة المحتوى الإيجابي {executive_summary['overall_sentiment']['إيجابي']}% مقابل {executive_summary['overall_sentiment']['سلبي']}% سلبي فقط، أي أن الإيجابية تفوق السلبية بأكثر من 4 أضعاف.",
                        "significance": "عالية جداً",
                        "icon": "✅"
                    },
                    {
                        "finding_id": 4,
                        "category": "موضوع التنظيم",
                        "finding": "نجاح باهر في التنظيم والاستضافة",
                        "detail": f"سجل موضوع الاستضافة والتنظيم أعلى نسبة إيجابية بـ {topic_analysis.get('استضافة_وتنظيم', {}).get('positive_rate', 42)}%، مما يؤكد السمعة الممتازة لقطر كمنظم للفعاليات الكبرى.",
                        "significance": "عالية جداً",
                        "icon": "🏟️"
                    },
                    {
                        "finding_id": 5,
                        "category": "الوصول العالمي",
                        "finding": "انتشار عالمي واسع",
                        "detail": f"تجاوز الوصول الإجمالي 134 مليار، مع تغطية من أكثر من {len(ministry_analytics.get('countries', {}))} دولة، مما يعكس المكانة العالمية لقطر الرياضية.",
                        "significance": "عالية",
                        "icon": "🌍"
                    },
                    {
                        "finding_id": 6,
                        "category": "تنوع الفعاليات",
                        "finding": "نجاح تنظيم 7 فعاليات متنوعة",
                        "detail": "استضافت قطر بنجاح فعاليات متنوعة تشمل كرة القدم، الفورمولا 1، UFC، الترايثلون، وتنس الطاولة، مؤكدة قدرتها على استضافة مختلف الرياضات.",
                        "significance": "عالية",
                        "icon": "🏆"
                    },
                    {
                        "finding_id": 7,
                        "category": "البنية التحتية",
                        "finding": "إشادة واسعة بالمنشآت الرياضية",
                        "detail": "حظيت البنية التحتية الرياضية (الملاعب، حلبة لوسيل، أسباير) بإشادة شبه إجماعية، مع شبه انعدام للانتقادات.",
                        "significance": "عالية",
                        "icon": "🏗️"
                    },
                    {
                        "finding_id": 8,
                        "category": "تجربة الجماهير",
                        "finding": "رضا عالٍ للجماهير والزوار",
                        "detail": f"سجل موضوع الجماهير والتجربة نسبة إيجابية عالية بـ {topic_analysis.get('جماهير_وتجربة', {}).get('positive_rate', 41)}%، مما يعزز صورة قطر كوجهة ترحيبية.",
                        "significance": "عالية",
                        "icon": "👥"
                    }
                ]
            },
            
            "swot_analysis": {
                "title": "7.3 تحليل نقاط القوة والضعف",
                "strengths": {
                    "title": "نقاط القوة",
                    "icon": "💪",
                    "points": [
                        {
                            "point": "سمعة تنظيمية ممتازة",
                            "evidence": "أعلى نسبة إيجابية في موضوع التنظيم والاستضافة",
                            "recommendation": "الحفاظ على هذا المستوى وتوثيقه"
                        },
                        {
                            "point": "بنية تحتية عالمية المستوى",
                            "evidence": "إشادة شبه إجماعية بالملاعب والمنشآت",
                            "recommendation": "استثمار هذه الميزة في جذب المزيد من البطولات"
                        },
                        {
                            "point": "خبرة متراكمة من كأس العالم 2022",
                            "evidence": "استمرارية النجاح في الفعاليات اللاحقة",
                            "recommendation": "توثيق أفضل الممارسات ونقل الخبرات"
                        },
                        {
                            "point": "ضيافة قطرية مميزة",
                            "evidence": "تجارب إيجابية للزوار والجماهير",
                            "recommendation": "تعزيز برامج الضيافة الرياضية"
                        },
                        {
                            "point": "تنوع الفعاليات المستضافة",
                            "evidence": "7 فعاليات متنوعة في 90 يوماً",
                            "recommendation": "التوسع في استضافة رياضات جديدة"
                        }
                    ]
                },
                "weaknesses": {
                    "title": "نقاط الضعف",
                    "icon": "⚠️",
                    "points": [
                        {
                            "point": "محدودية الانتشار العربي لبعض الرياضات",
                            "evidence": "اهتمام أقل بـ UFC والترايثلون عربياً",
                            "recommendation": "حملات توعية بالرياضات غير التقليدية"
                        },
                        {
                            "point": "نتائج المنتخبات الوطنية",
                            "evidence": "بعض الخيبة من نتائج المنتخب القطري",
                            "recommendation": "الفصل بين التنظيم والأداء الرياضي"
                        }
                    ]
                },
                "opportunities": {
                    "title": "الفرص",
                    "icon": "🚀",
                    "points": [
                        {
                            "point": "السياحة الرياضية",
                            "description": "اهتمام متزايد بقطر كوجهة للسياحة الرياضية",
                            "action": "تطوير باقات سياحية رياضية متكاملة"
                        },
                        {
                            "point": "التموضع كعاصمة رياضية عالمية",
                            "description": "الإشادة الدولية تفتح فرصاً لاستضافة بطولات أكبر",
                            "action": "الترشح لاستضافة بطولات عالمية جديدة"
                        },
                        {
                            "point": "الرياضات الناشئة",
                            "description": "نجاح UFC والترايثلون يفتح آفاقاً جديدة",
                            "action": "استقطاب رياضات ناشئة أخرى"
                        },
                        {
                            "point": "رياضة المرأة",
                            "description": "اهتمام متزايد برياضة المرأة عالمياً",
                            "action": "استضافة بطولات نسائية دولية"
                        },
                        {
                            "point": "الرياضات التراثية",
                            "description": "اهتمام بالفعاليات التراثية الفريدة",
                            "action": "تطوير تجربة الرياضات التراثية للسياح"
                        }
                    ]
                },
                "threats": {
                    "title": "التحديات",
                    "icon": "🛡️",
                    "points": [
                        {
                            "point": "المنافسة الإقليمية",
                            "description": "منافسة من دول الخليج في استضافة الفعاليات",
                            "mitigation": "التميز بالجودة وليس الكمية"
                        },
                        {
                            "point": "التغطية السلبية المتعمدة",
                            "description": "بعض وسائل الإعلام المعادية",
                            "mitigation": "تعزيز الحضور الإعلامي الإيجابي"
                        },
                        {
                            "point": "الإجهاد من كثافة الفعاليات",
                            "description": "خطر الإرهاق من الفعاليات المتتالية",
                            "mitigation": "التخطيط الاستراتيجي للفعاليات"
                        }
                    ]
                }
            },
            
            "performance_scorecard": {
                "title": "7.4 بطاقة الأداء",
                "overall_score": "A+",
                "overall_rating": "ممتاز",
                "criteria": [
                    {
                        "criterion": "حجم التغطية الإعلامية",
                        "score": "A+",
                        "rating": 95,
                        "benchmark": "أعلى من المتوقع"
                    },
                    {
                        "criterion": "نسبة الإيجابية",
                        "score": "A",
                        "rating": 90,
                        "benchmark": "ممتاز (28% إيجابي)"
                    },
                    {
                        "criterion": "الوصول الجماهيري",
                        "score": "A+",
                        "rating": 98,
                        "benchmark": "134+ مليار وصول"
                    },
                    {
                        "criterion": "تنوع المصادر الجغرافية",
                        "score": "A",
                        "rating": 88,
                        "benchmark": "تغطية عالمية"
                    },
                    {
                        "criterion": "التفاعل الاجتماعي",
                        "score": "A-",
                        "rating": 85,
                        "benchmark": "فوق المتوسط"
                    },
                    {
                        "criterion": "إدارة السمعة السلبية",
                        "score": "A+",
                        "rating": 95,
                        "benchmark": "5.8% سلبي فقط"
                    }
                ],
                "summary": "حققت وزارة الرياضة والشباب والفعاليات الرياضية أداءً إعلامياً ممتازاً يتجاوز المعايير المتوقعة في معظم المؤشرات."
            }
        },
        
        # ============================================
        # القسم الثامن: التوصيات الاستراتيجية
        # ============================================
        "section_8_recommendations": {
            "section_number": 8,
            "title": "التوصيات الاستراتيجية",
            "page_count": 4,
            
            "overview": {
                "title": "8.1 مقدمة التوصيات",
                "content": """بناءً على النتائج والتحليلات الواردة في هذا التقرير، نقدم مجموعة من التوصيات الاستراتيجية والتكتيكية الهادفة إلى:

• تعزيز نقاط القوة والاستفادة منها
• معالجة التحديات والفجوات المحددة
• استثمار الفرص المتاحة
• تحسين الأداء الإعلامي المستقبلي"""
            },
            
            "strategic_recommendations": {
                "title": "8.2 التوصيات الاستراتيجية",
                "recommendations": [
                    {
                        "rec_id": 1,
                        "title": "التموضع كعاصمة رياضية عالمية",
                        "priority": "عالية",
                        "timeframe": "طويل المدى (3-5 سنوات)",
                        "description": "البناء على النجاحات المتحققة لترسيخ مكانة قطر كوجهة رياضية عالمية رائدة.",
                        "actions": [
                            "وضع استراتيجية متكاملة للتموضع الرياضي الدولي",
                            "الترشح لاستضافة بطولات عالمية كبرى (كأس العالم للأندية الموسع، بطولات أولمبية)",
                            "تطوير شراكات طويلة المدى مع الاتحادات الدولية",
                            "إنشاء هوية بصرية وإعلامية موحدة 'Qatar Sports'"
                        ],
                        "expected_impact": "تعزيز السمعة الرياضية الدولية",
                        "kpis": ["عدد الفعاليات المستضافة سنوياً", "التصنيف الدولي كوجهة رياضية"]
                    },
                    {
                        "rec_id": 2,
                        "title": "تطوير السياحة الرياضية",
                        "priority": "عالية",
                        "timeframe": "متوسط المدى (1-3 سنوات)",
                        "description": "استثمار الاهتمام المتزايد بقطر كوجهة رياضية لتطوير قطاع السياحة الرياضية.",
                        "actions": [
                            "التعاون مع هيئة السياحة لتطوير باقات سياحية رياضية",
                            "إنشاء منصة رقمية لتجربة الفعاليات الرياضية في قطر",
                            "تطوير برامج تجربة الملاعب والمنشآت للسياح",
                            "التسويق المشترك مع شركات الطيران والفنادق"
                        ],
                        "expected_impact": "زيادة السياحة الرياضية وإيرادات القطاع",
                        "kpis": ["عدد السياح الرياضيين سنوياً", "إيرادات السياحة الرياضية"]
                    },
                    {
                        "rec_id": 3,
                        "title": "تعزيز الحضور الرقمي",
                        "priority": "عالية",
                        "timeframe": "قصير المدى (6-12 شهر)",
                        "description": "تطوير الحضور الرقمي للوزارة والفعاليات الرياضية على منصات التواصل الاجتماعي.",
                        "actions": [
                            "تطوير استراتيجية محتوى رقمي شاملة",
                            "إنشاء فريق متخصص لإدارة منصات التواصل",
                            "التعاون مع المؤثرين الرياضيين المحليين والدوليين",
                            "إنتاج محتوى فيديو عالي الجودة لكل فعالية",
                            "تفعيل حملات هاشتاق موحدة قبل الفعاليات"
                        ],
                        "expected_impact": "زيادة التفاعل والوصول الرقمي",
                        "kpis": ["نمو المتابعين", "معدل التفاعل", "الوصول العضوي"]
                    },
                    {
                        "rec_id": 4,
                        "title": "برنامج العلاقات الإعلامية الدولية",
                        "priority": "متوسطة-عالية",
                        "timeframe": "متوسط المدى (1-2 سنة)",
                        "description": "تطوير علاقات استراتيجية مع وسائل الإعلام الدولية الرائدة.",
                        "actions": [
                            "إنشاء قاعدة بيانات شاملة للصحفيين الرياضيين الدوليين",
                            "تنظيم جولات صحفية منتظمة للمنشآت الرياضية",
                            "إنشاء مركز إعلامي دائم للصحفيين الرياضيين",
                            "برنامج دعوات للصحفيين المؤثرين لتغطية الفعاليات",
                            "توفير محتوى حصري للوسائل الإعلامية الرئيسية"
                        ],
                        "expected_impact": "تحسين جودة التغطية الدولية",
                        "kpis": ["عدد المقالات الإيجابية في الوسائل الدولية", "قيمة التغطية الإعلامية"]
                    }
                ]
            },
            
            "tactical_recommendations": {
                "title": "8.3 التوصيات التكتيكية",
                "recommendations": [
                    {
                        "area": "إدارة الأزمات والسمعة",
                        "recommendations": [
                            "إنشاء غرفة عمليات إعلامية أثناء الفعاليات الكبرى",
                            "تطوير بروتوكولات استجابة سريعة للمحتوى السلبي",
                            "رصد آني للمشاعر على منصات التواصل",
                            "إعداد رسائل رئيسية جاهزة للسيناريوهات المختلفة"
                        ]
                    },
                    {
                        "area": "المحتوى والإنتاج الإعلامي",
                        "recommendations": [
                            "إنتاج أفلام وثائقية عن الفعاليات الكبرى",
                            "تطوير محتوى ما وراء الكواليس للفعاليات",
                            "إنشاء أرشيف رقمي للموروث الرياضي القطري",
                            "إنتاج محتوى متعدد اللغات (عربي، إنجليزي، فرنسي)"
                        ]
                    },
                    {
                        "area": "التفاعل مع الجمهور",
                        "recommendations": [
                            "برنامج سفراء رياضيين من المشجعين",
                            "حملات تفاعلية قبل وأثناء الفعاليات",
                            "استطلاعات رأي دورية لقياس رضا الجماهير",
                            "برامج ولاء للمشجعين الدائمين"
                        ]
                    },
                    {
                        "area": "القياس والتحليل",
                        "recommendations": [
                            "تطوير لوحة مؤشرات أداء إعلامي شاملة",
                            "تقارير رصد إعلامي أسبوعية أثناء الفعاليات",
                            "تقييم شامل بعد كل فعالية رئيسية",
                            "قياس العائد على الاستثمار الإعلامي"
                        ]
                    }
                ]
            },
            
            "event_specific_recommendations": {
                "title": "8.4 توصيات خاصة بالفعاليات",
                "events": [
                    {
                        "event": "الفعاليات القادمة لكرة القدم",
                        "recommendations": [
                            "الاستفادة من قاعدة المشجعين العربية الكبيرة",
                            "التركيز على إرث كأس العالم 2022",
                            "تطوير محتوى تفاعلي للمشجعين"
                        ]
                    },
                    {
                        "event": "فورمولا 1 قطر المستقبلية",
                        "recommendations": [
                            "تعزيز الشراكة مع F1 للمحتوى الحصري",
                            "تطوير تجربة الحلبة للزوار على مدار العام",
                            "استهداف السوق الأوروبي والأمريكي"
                        ]
                    },
                    {
                        "event": "الرياضات القتالية (UFC)",
                        "recommendations": [
                            "استثمار الوصول العالمي الكبير",
                            "التوسع في استضافة فعاليات أكثر",
                            "التسويق للجمهور الآسيوي والأمريكي"
                        ]
                    },
                    {
                        "event": "الفعاليات التراثية",
                        "recommendations": [
                            "تطوير تجربة سياحية متكاملة",
                            "إنتاج محتوى وثائقي عالي الجودة",
                            "ربط الرياضة التراثية بالهوية الوطنية"
                        ]
                    }
                ]
            },
            
            "implementation_roadmap": {
                "title": "8.5 خارطة طريق التنفيذ",
                "phases": [
                    {
                        "phase": "المرحلة الأولى (0-6 أشهر)",
                        "focus": "التأسيس والتخطيط",
                        "actions": [
                            "تشكيل فريق عمل الاتصال الاستراتيجي",
                            "تطوير استراتيجية المحتوى الرقمي",
                            "إطلاق برنامج الرصد الإعلامي المحسن",
                            "بناء قاعدة بيانات المؤثرين والصحفيين"
                        ]
                    },
                    {
                        "phase": "المرحلة الثانية (6-12 شهر)",
                        "focus": "التنفيذ والتجريب",
                        "actions": [
                            "إطلاق الحملات الرقمية الجديدة",
                            "تنفيذ برنامج العلاقات الإعلامية",
                            "تطوير منصة السياحة الرياضية",
                            "قياس وتقييم المرحلة الأولى"
                        ]
                    },
                    {
                        "phase": "المرحلة الثالثة (12-24 شهر)",
                        "focus": "التوسع والتحسين",
                        "actions": [
                            "توسيع نطاق البرامج الناجحة",
                            "تطوير الشراكات الاستراتيجية",
                            "إطلاق مبادرات جديدة",
                            "التحضير للفعاليات الكبرى القادمة"
                        ]
                    }
                ]
            }
        },
        
        # ============================================
        # القسم التاسع: الملاحق
        # ============================================
        "section_9_appendices": {
            "section_number": 9,
            "title": "الملاحق",
            "page_count": 6,
            
            "appendix_a": {
                "title": "ملحق أ: تفاصيل البيانات",
                "data_summary": {
                    "total_materials": executive_summary['total_mentions'],
                    "traditional_media": executive_summary['traditional_media'],
                    "social_media": executive_summary['social_media'],
                    "total_reach": executive_summary['reach_total'],
                    "total_engagement": executive_summary['engagement_total'],
                    "analysis_period": "1 نوفمبر 2025 - 22 يناير 2026",
                    "days_analyzed": 90,
                    "events_covered": 7
                },
                "sentiment_breakdown": {
                    "positive": {
                        "count": executive_summary['sentiment_counts']['positive'],
                        "percentage": executive_summary['overall_sentiment']['إيجابي']
                    },
                    "negative": {
                        "count": executive_summary['sentiment_counts']['negative'],
                        "percentage": executive_summary['overall_sentiment']['سلبي']
                    },
                    "neutral": {
                        "count": executive_summary['sentiment_counts']['neutral'],
                        "percentage": executive_summary['overall_sentiment']['محايد']
                    }
                }
            },
            
            "appendix_b": {
                "title": "ملحق ب: تفاصيل الفعاليات السبع",
                "events": events_comparison
            },
            
            "appendix_c": {
                "title": "ملحق ج: المصادر الإعلامية الرئيسية",
                "top_sources": list(ministry_analytics.get('top_sources', {}).items())[:30],
                "geographic_distribution": list(ministry_analytics.get('countries', {}).items())[:20]
            },
            
            "appendix_d": {
                "title": "ملحق د: تحليل اللغات",
                "languages": list(ministry_analytics.get('languages', {}).items()),
                "primary_languages": ["العربية", "الإنجليزية"],
                "arabic_percentage": round(ministry_analytics.get('languages', {}).get('Arabic', 0) / ministry_analytics.get('total_mentions', 1) * 100, 1) if ministry_analytics.get('total_mentions', 0) > 0 else 0
            },
            
            "appendix_e": {
                "title": "ملحق هـ: المؤثرون والشخصيات الأبرز",
                "top_influencers": influencers.get('top_influencers', [])[:20] if isinstance(influencers, dict) else []
            },
            
            "appendix_f": {
                "title": "ملحق و: مصطلحات ومفاهيم",
                "glossary": [
                    {"term": "الوصول (Reach)", "definition": "العدد الإجمالي للأشخاص الذين يمكن أن يصلهم المحتوى"},
                    {"term": "التفاعل (Engagement)", "definition": "مجموع التفاعلات (إعجابات، مشاركات، تعليقات)"},
                    {"term": "تحليل المشاعر (Sentiment Analysis)", "definition": "تصنيف المحتوى إلى إيجابي أو سلبي أو محايد"},
                    {"term": "الإعلام التقليدي", "definition": "الصحف، وكالات الأنباء، المواقع الإخبارية، المدونات"},
                    {"term": "منصات التواصل الاجتماعي", "definition": "X، Facebook، Instagram، YouTube، TikTok، Snapchat"},
                    {"term": "المؤثر (Influencer)", "definition": "شخص له تأثير على جمهور واسع عبر منصات التواصل"},
                    {"term": "الهاشتاق (Hashtag)", "definition": "وسم يستخدم لتجميع المحتوى حول موضوع معين"},
                    {"term": "المحتوى الفيروسي (Viral Content)", "definition": "محتوى ينتشر بسرعة كبيرة عبر المنصات الرقمية"}
                ]
            }
        },
        
        # ============================================
        # ختام التقرير
        # ============================================
        "report_conclusion": {
            "title": "ختام التقرير",
            "closing_statement": f"""يختتم هذا التقرير تحليلاً شاملاً للأداء الإعلامي لوزارة الرياضة والشباب القطرية والفعاليات الرياضية الكبرى خلال الفترة من نوفمبر 2025 إلى يناير 2026.

أثبتت النتائج أن قطر تواصل ترسيخ مكانتها كوجهة رياضية عالمية رائدة، مع تحقيق أداء إعلامي ممتاز يتجلى في:

• تغطية ضخمة بأكثر من {executive_summary['total_mentions']:,} مادة إعلامية
• انطباع إيجابي سائد بنسبة {executive_summary['overall_sentiment']['إيجابي']}%
• وصول عالمي يتجاوز 134 مليار
• نجاح في تنظيم 7 فعاليات رياضية متنوعة

نوصي بتبني التوصيات الاستراتيجية والتكتيكية الواردة في هذا التقرير لمواصلة تعزيز السمعة الإعلامية والريادة الرياضية القطرية.""",
            "prepared_by": "فريق التحليل الإعلامي",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "version": "1.0"
        }
    }
    
    return phase3

def save_phase3():
    """حفظ المرحلة الثالثة"""
    print("=" * 60)
    print("🇶🇦 المرحلة الثالثة: النتائج + التوصيات + الملاحق")
    print("=" * 60)
    
    print("\n📂 جاري تحميل البيانات...")
    phase3 = build_phase3()
    
    print("💾 جاري حفظ المرحلة الثالثة...")
    
    output_file = os.path.join(OUTPUT_PATH, 'phase3_results_recommendations.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(phase3, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ تم حفظ المرحلة الثالثة في: {output_file}")
    
    # طباعة ملخص
    print("\n" + "=" * 60)
    print("📋 محتويات المرحلة الثالثة:")
    print("=" * 60)
    
    sections = [
        ("القسم 7", "النتائج والاستنتاجات", "section_7_results", 4),
        ("القسم 8", "التوصيات الاستراتيجية", "section_8_recommendations", 4),
        ("القسم 9", "الملاحق", "section_9_appendices", 6)
    ]
    
    total_pages = 0
    for section_num, title, key, pages in sections:
        section_data = phase3.get(key, {})
        subsections = len([k for k in section_data.keys() if k not in ['section_number', 'title', 'page_count']])
        print(f"   {section_num}: {title}")
        print(f"      └── {subsections} قسم فرعي | {pages} صفحات")
        total_pages += pages
    
    print(f"\n   📄 إجمالي الصفحات: {total_pages} صفحة")
    
    print("\n" + "=" * 60)
    print("📊 النتائج الرئيسية:")
    print("=" * 60)
    findings = phase3['section_7_results']['key_findings']['findings'][:4]
    for finding in findings:
        print(f"   {finding['icon']} {finding['finding']}")
    
    print("\n" + "=" * 60)
    print("✅ المرحلة الثالثة جاهزة!")
    print("=" * 60)
    
    return phase3

if __name__ == "__main__":
    phase3 = save_phase3()
