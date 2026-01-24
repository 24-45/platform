"""
المرحلة الأولى: المقدمة + المنهجية + الملخص التنفيذي
Phase 1: Introduction + Methodology + Executive Summary
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

def build_phase1():
    """بناء المرحلة الأولى من التقرير"""
    
    # تحميل البيانات
    executive_summary = load_json('executive_summary.json')
    full_analysis = load_json('full_analysis.json')
    topic_analysis = load_json('topic_analysis.json')
    events_comparison = load_json('events_comparison.json')
    
    ministry_analytics = full_analysis.get('ministry_analytics', {})
    
    phase1 = {
        "phase": 1,
        "title": "المرحلة الأولى: الإطار العام والملخص التنفيذي",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        # ============================================
        # القسم الأول: المقدمة
        # ============================================
        "section_1_introduction": {
            "section_number": 1,
            "title": "المقدمة",
            "page_count": 2,
            
            "opening_statement": {
                "title": "تمهيد",
                "content": """في إطار حرص وزارة الرياضة والشباب القطرية على تطوير أدائها المؤسسي وتعزيز حضورها الإعلامي، يأتي هذا التقرير ليقدم تحليلاً شاملاً ومعمقاً للكفاءة الإعلامية والسمعة المؤسسية للوزارة خلال فترة استثنائية شهدت استضافة قطر لسبع فعاليات رياضية كبرى.

يغطي هذا التقرير الفترة الممتدة من الأول من نوفمبر 2025 حتى الثاني والعشرين من يناير 2026، وهي فترة تميزت بكثافة الأحداث الرياضية الدولية التي عززت مكانة قطر كوجهة رياضية عالمية رائدة."""
            },
            
            "ministry_overview": {
                "title": "نبذة عن الوزارة",
                "content": """تعد وزارة الرياضة والشباب القطرية الجهة الحكومية المسؤولة عن تطوير القطاع الرياضي والشبابي في دولة قطر. تعمل الوزارة على تحقيق رؤية قطر الوطنية 2030 من خلال:

• تطوير البنية التحتية الرياضية وفق أعلى المعايير الدولية
• دعم المنتخبات الوطنية والرياضيين القطريين
• استضافة الفعاليات الرياضية الدولية الكبرى
• تعزيز ثقافة الرياضة والنشاط البدني في المجتمع
• رعاية البرامج الشبابية والمبادرات المجتمعية
• الحفاظ على الرياضات التراثية والتقليدية"""
            },
            
            "report_objectives": {
                "title": "أهداف التقرير",
                "main_objective": "قياس الكفاءة الإعلامية والسمعة المؤسسية لوزارة الرياضة والشباب القطرية خلال فترة الفعاليات الرياضية الكبرى (نوفمبر 2025 - يناير 2026)",
                "specific_objectives": [
                    {
                        "number": 1,
                        "objective": "تحليل حجم التغطية الإعلامية",
                        "description": "رصد وتحليل حجم التغطية الإعلامية للوزارة والفعاليات الرياضية في الإعلام التقليدي ومنصات التواصل الاجتماعي"
                    },
                    {
                        "number": 2,
                        "objective": "قياس اتجاهات المشاعر",
                        "description": "تحليل الانطباعات والمشاعر السائدة تجاه الوزارة وتصنيفها إلى إيجابية وسلبية ومحايدة"
                    },
                    {
                        "number": 3,
                        "objective": "تحديد المؤثرين الرئيسيين",
                        "description": "رصد الصحفيين والمؤثرين الأكثر تأثيراً في تشكيل الصورة الإعلامية للوزارة"
                    },
                    {
                        "number": 4,
                        "objective": "تقييم فعالية التغطية",
                        "description": "قياس مدى نجاح التغطية الإعلامية للفعاليات الرياضية السبع الكبرى"
                    },
                    {
                        "number": 5,
                        "objective": "رصد المواضيع الرئيسية",
                        "description": "تحديد وتحليل المواضيع والقضايا الأكثر ارتباطاً بالوزارة في الفضاء الإعلامي"
                    },
                    {
                        "number": 6,
                        "objective": "تقديم توصيات استراتيجية",
                        "description": "صياغة توصيات عملية لتحسين الأداء الإعلامي وتعزيز السمعة المؤسسية"
                    }
                ]
            },
            
            "report_importance": {
                "title": "أهمية التقرير للوزارة",
                "points": [
                    {
                        "point": "فهم الصورة الذهنية",
                        "description": "يوفر التقرير رؤية واضحة عن الصورة الذهنية للوزارة لدى الجمهور المحلي والدولي، مما يساعد في تحديد نقاط القوة التي يجب تعزيزها والتحديات التي تحتاج معالجة."
                    },
                    {
                        "point": "تقييم أثر الفعاليات",
                        "description": "يقيس التقرير الأثر الإعلامي للفعاليات الرياضية الكبرى على سمعة قطر الرياضية، ويحدد العوامل التي ساهمت في النجاح."
                    },
                    {
                        "point": "دعم اتخاذ القرار",
                        "description": "يوفر التقرير بيانات وتحليلات موثوقة تدعم اتخاذ القرارات الاستراتيجية المتعلقة بالتواصل الإعلامي والعلاقات العامة."
                    },
                    {
                        "point": "قياس العائد على الاستثمار",
                        "description": "يساعد في تقييم العائد الإعلامي على الاستثمار في استضافة الفعاليات الرياضية الدولية."
                    },
                    {
                        "point": "التخطيط المستقبلي",
                        "description": "يوفر أساساً للتخطيط الإعلامي للفعاليات المستقبلية بناءً على الدروس المستفادة."
                    }
                ]
            },
            
            "report_scope": {
                "title": "نطاق التقرير",
                "temporal_scope": {
                    "title": "النطاق الزمني",
                    "period": "1 نوفمبر 2025 - 22 يناير 2026",
                    "duration_days": 90,
                    "description": "تغطي هذه الفترة موسماً رياضياً استثنائياً شهدت فيه قطر استضافة سبع فعاليات رياضية دولية كبرى."
                },
                "geographic_scope": {
                    "title": "النطاق الجغرافي",
                    "description": "تغطية عالمية شاملة مع تركيز خاص على:",
                    "regions": [
                        "دولة قطر (التغطية المحلية)",
                        "دول مجلس التعاون الخليجي",
                        "المنطقة العربية",
                        "أوروبا وأمريكا الشمالية",
                        "آسيا وأفريقيا"
                    ]
                },
                "events_covered": {
                    "title": "الفعاليات المشمولة",
                    "events": [
                        {
                            "name": "كأس العرب FIFA قطر 2025",
                            "name_en": "FIFA Arab Cup Qatar 2025",
                            "date": "1-18 ديسمبر 2025",
                            "type": "كرة قدم"
                        },
                        {
                            "name": "كأس القارات FIFA قطر 2025",
                            "name_en": "FIFA Intercontinental Cup Qatar 2025",
                            "date": "ديسمبر 2025",
                            "type": "كرة قدم"
                        },
                        {
                            "name": "كأس العالم للناشئين تحت 17 سنة",
                            "name_en": "FIFA U-17 World Cup Qatar 2025",
                            "date": "3-27 نوفمبر 2025",
                            "type": "كرة قدم"
                        },
                        {
                            "name": "سباق جائزة قطر الكبرى للفورمولا 1",
                            "name_en": "Qatar Airways Qatar Grand Prix 2025",
                            "date": "28-30 نوفمبر 2025",
                            "type": "سباق سيارات"
                        },
                        {
                            "name": "UFC قطر",
                            "name_en": "UFC Qatar",
                            "date": "2025",
                            "type": "فنون قتالية"
                        },
                        {
                            "name": "نهائي بطولة العالم للترايثلون T100",
                            "name_en": "T100 Triathlon World Tour Final",
                            "date": "11-13 ديسمبر 2025",
                            "type": "ترايثلون"
                        },
                        {
                            "name": "بطولات تنس الطاولة WTT",
                            "name_en": "WTT Doha 2026",
                            "date": "يناير 2026",
                            "type": "تنس طاولة"
                        }
                    ]
                }
            }
        },
        
        # ============================================
        # القسم الثاني: المنهجية
        # ============================================
        "section_2_methodology": {
            "section_number": 2,
            "title": "المنهجية",
            "page_count": 4,
            
            "introduction": {
                "content": """اعتمد هذا التقرير على منهجية علمية صارمة في جمع البيانات وتحليلها، مستخدماً أحدث أدوات الرصد الإعلامي وتقنيات الذكاء الاصطناعي لتحليل المشاعر. تضمن هذه المنهجية الشفافية والموثوقية في النتائج المقدمة."""
            },
            
            "scope_and_sample": {
                "title": "2.1 النطاق والعينة",
                "data_source": {
                    "title": "مصدر البيانات",
                    "platform": "Meltwater Media Intelligence Platform",
                    "description": "منصة رصد إعلامي عالمية رائدة توفر تغطية شاملة للإعلام التقليدي ومنصات التواصل الاجتماعي في أكثر من 190 دولة."
                },
                "sample_size": {
                    "title": "حجم العينة",
                    "total": executive_summary['total_mentions'],
                    "total_formatted": f"{executive_summary['total_mentions']:,}",
                    "breakdown": {
                        "traditional_media": {
                            "count": executive_summary['traditional_media'],
                            "count_formatted": f"{executive_summary['traditional_media']:,}",
                            "percentage": executive_summary['key_metrics']['traditional_percentage'],
                            "types": ["صحف إلكترونية", "وكالات أنباء", "مواقع إخبارية", "مدونات", "منتديات"]
                        },
                        "social_media": {
                            "count": executive_summary['social_media'],
                            "count_formatted": f"{executive_summary['social_media']:,}",
                            "percentage": executive_summary['key_metrics']['social_percentage'],
                            "platforms": ["X (Twitter)", "Facebook", "Instagram", "YouTube", "TikTok", "Snapchat"]
                        }
                    }
                },
                "time_period": {
                    "title": "الفترة الزمنية",
                    "start_date": "1 نوفمبر 2025",
                    "end_date": "22 يناير 2026",
                    "duration_days": 90,
                    "daily_average": round(executive_summary['total_mentions'] / 90)
                },
                "languages_monitored": {
                    "title": "اللغات المرصودة",
                    "primary": ["العربية", "الإنجليزية"],
                    "secondary": ["الفرنسية", "الإسبانية", "البرتغالية", "الألمانية"],
                    "distribution": ministry_analytics.get('languages', {})
                },
                "geographic_coverage": {
                    "title": "التغطية الجغرافية",
                    "countries_count": len(ministry_analytics.get('countries', {})),
                    "top_countries": list(ministry_analytics.get('countries', {}).items())[:10]
                }
            },
            
            "data_preparation": {
                "title": "2.2 تجهيز البيانات",
                "steps": [
                    {
                        "step": 1,
                        "title": "جمع البيانات",
                        "description": "استخدام كلمات مفتاحية محددة بدقة لجمع المحتوى ذي الصلة بوزارة الرياضة والشباب والفعاليات الرياضية السبع.",
                        "keywords_used": [
                            "وزارة الرياضة والشباب القطرية",
                            "Ministry of Sports and Youth Qatar",
                            "أسماء الفعاليات الرياضية السبع",
                            "أسماء المسؤولين والشخصيات الرياضية",
                            "الملاعب والمنشآت الرياضية"
                        ]
                    },
                    {
                        "step": 2,
                        "title": "التنظيف والفلترة",
                        "description": "إزالة المحتوى المكرر وغير ذي الصلة، وتصفية النتائج للتركيز على المحتوى المرتبط فعلياً بالوزارة والفعاليات.",
                        "filters_applied": [
                            "استبعاد نتائج المباريات البحتة",
                            "استبعاد المحتوى السياسي غير المرتبط",
                            "استبعاد الإعلانات التجارية",
                            "التركيز على الاستضافة والتنظيم"
                        ]
                    },
                    {
                        "step": 3,
                        "title": "التصنيف الأولي",
                        "description": "تصنيف المحتوى حسب نوع المصدر (تقليدي/اجتماعي)، واللغة، والموقع الجغرافي.",
                        "classifications": ["نوع المصدر", "اللغة", "الدولة", "المنصة", "التاريخ"]
                    },
                    {
                        "step": 4,
                        "title": "استخراج البيانات الوصفية",
                        "description": "استخراج مؤشرات الأداء الرئيسية لكل مادة إعلامية.",
                        "metrics_extracted": ["الوصول (Reach)", "التفاعل (Engagement)", "المشاعر (Sentiment)", "الكلمات المفتاحية", "الهاشتاقات"]
                    }
                ],
                "tools_used": {
                    "title": "الأدوات المستخدمة",
                    "tools": [
                        {"name": "Meltwater", "purpose": "الرصد الإعلامي وجمع البيانات"},
                        {"name": "Python", "purpose": "التحليل الإحصائي ومعالجة البيانات"},
                        {"name": "AI Sentiment Analysis", "purpose": "تحليل المشاعر"},
                        {"name": "Data Visualization Tools", "purpose": "إنشاء الرسوم البيانية"}
                    ]
                }
            },
            
            "topic_classification": {
                "title": "2.3 التصنيف الموضوعي",
                "methodology": "تم تصنيف المحتوى إلى فئات موضوعية محددة بناءً على تحليل الكلمات المفتاحية والسياق.",
                "categories": [
                    {
                        "name": "فعاليات رياضية كبرى",
                        "description": "المحتوى المتعلق بالبطولات والمسابقات الدولية السبع",
                        "keywords": ["كأس العرب", "كأس القارات", "فورمولا 1", "UFC", "ترايثلون"],
                        "count": topic_analysis.get('فعاليات_رياضية_كبرى', {}).get('count', 0)
                    },
                    {
                        "name": "استضافة وتنظيم",
                        "description": "المحتوى المتعلق بجهود قطر في استضافة وتنظيم الفعاليات",
                        "keywords": ["استضافة", "تنظيم", "hosting", "organization"],
                        "count": topic_analysis.get('استضافة_وتنظيم', {}).get('count', 0)
                    },
                    {
                        "name": "بنية تحتية",
                        "description": "المحتوى المتعلق بالملاعب والمنشآت الرياضية",
                        "keywords": ["ملعب", "استاد", "stadium", "أسباير", "لوسيل"],
                        "count": topic_analysis.get('بنية_تحتية', {}).get('count', 0)
                    },
                    {
                        "name": "مسؤولون",
                        "description": "تصريحات وظهور المسؤولين القطريين",
                        "keywords": ["وزير", "الشيخ", "رئيس", "minister"],
                        "count": topic_analysis.get('مسؤولون', {}).get('count', 0)
                    },
                    {
                        "name": "جماهير وتجربة",
                        "description": "تجربة الزوار والجماهير",
                        "keywords": ["جماهير", "fans", "تجربة", "experience"],
                        "count": topic_analysis.get('جماهير_وتجربة', {}).get('count', 0)
                    },
                    {
                        "name": "إرث ورؤية",
                        "description": "الإرث الرياضي ورؤية قطر المستقبلية",
                        "keywords": ["إرث", "legacy", "رؤية", "2030"],
                        "count": topic_analysis.get('إرث_ورؤية', {}).get('count', 0)
                    }
                ]
            },
            
            "sentiment_measurement": {
                "title": "2.4 قياس الانطباعات",
                "methodology": {
                    "title": "منهجية تحليل المشاعر",
                    "description": "تم استخدام تقنيات الذكاء الاصطناعي المتقدمة لتحليل المشاعر في المحتوى الإعلامي، مع مراعاة السياق اللغوي والثقافي للمحتوى العربي والإنجليزي."
                },
                "categories": [
                    {
                        "type": "إيجابي",
                        "type_en": "Positive",
                        "color": "#27AE60",
                        "description": "محتوى يعكس انطباعاً إيجابياً تجاه الوزارة أو الفعاليات، يتضمن الإشادة أو الثناء أو التقدير.",
                        "examples": ["الإشادة بالتنظيم", "الثناء على البنية التحتية", "تجارب إيجابية للجماهير"]
                    },
                    {
                        "type": "سلبي",
                        "type_en": "Negative",
                        "color": "#E74C3C",
                        "description": "محتوى يعكس انطباعاً سلبياً أو انتقادياً، يتضمن شكاوى أو انتقادات أو استياء.",
                        "examples": ["انتقادات تنظيمية", "شكاوى من الخدمات", "استياء من النتائج"]
                    },
                    {
                        "type": "محايد",
                        "type_en": "Neutral",
                        "color": "#F39C12",
                        "description": "محتوى إخباري موضوعي لا يحمل انطباعاً إيجابياً أو سلبياً واضحاً.",
                        "examples": ["تغطية إخبارية", "إعلان عن فعاليات", "معلومات عامة"]
                    }
                ],
                "accuracy_notes": {
                    "title": "ملاحظات حول الدقة",
                    "notes": [
                        "دقة تحليل المشاعر تتراوح بين 85-90% للمحتوى الواضح",
                        "قد تنخفض الدقة في المحتوى الساخر أو متعدد المعاني",
                        "تم مراجعة عينة من الحالات الحساسة يدوياً",
                        "الأرقام المقدمة تمثل تقديرات موثوقة وليست مطلقة"
                    ]
                }
            }
        },
        
        # ============================================
        # القسم الثالث: الملخص التنفيذي
        # ============================================
        "section_3_executive_summary": {
            "section_number": 3,
            "title": "الملخص التنفيذي",
            "page_count": 4,
            
            "overview": {
                "title": "نظرة عامة",
                "content": f"""شهدت الفترة من نوفمبر 2025 إلى يناير 2026 نشاطاً إعلامياً استثنائياً حول وزارة الرياضة والشباب القطرية والفعاليات الرياضية الكبرى التي استضافتها الدولة. تم رصد {executive_summary['total_mentions']:,} مادة إعلامية عبر الإعلام التقليدي ومنصات التواصل الاجتماعي، بوصول إجمالي تجاوز 134 مليار.

الأرقام تعكس نجاحاً لافتاً في التغطية الإعلامية، حيث سجلت نسبة المحتوى الإيجابي (28%) أكثر من أربعة أضعاف المحتوى السلبي (5.8%)، مما يشير إلى انطباع عام إيجابي تجاه الوزارة والفعاليات الرياضية."""
            },
            
            "key_figures": {
                "title": "3.1 الأرقام الرئيسية",
                "metrics": [
                    {
                        "metric": "إجمالي المواد الإعلامية",
                        "value": executive_summary['total_mentions'],
                        "value_formatted": f"{executive_summary['total_mentions']:,}",
                        "icon": "📰",
                        "context": "مادة إعلامية تم رصدها خلال 90 يوماً"
                    },
                    {
                        "metric": "الإعلام التقليدي",
                        "value": executive_summary['traditional_media'],
                        "value_formatted": f"{executive_summary['traditional_media']:,}",
                        "percentage": executive_summary['key_metrics']['traditional_percentage'],
                        "icon": "📺",
                        "context": "من إجمالي التغطية"
                    },
                    {
                        "metric": "منصات التواصل",
                        "value": executive_summary['social_media'],
                        "value_formatted": f"{executive_summary['social_media']:,}",
                        "percentage": executive_summary['key_metrics']['social_percentage'],
                        "icon": "📱",
                        "context": "من إجمالي التغطية"
                    },
                    {
                        "metric": "إجمالي الوصول",
                        "value": executive_summary['reach_total'],
                        "value_formatted": f"{executive_summary['reach_total']:,}",
                        "value_simplified": "134+ مليار",
                        "icon": "📣",
                        "context": "إجمالي الأشخاص الذين وصلهم المحتوى"
                    },
                    {
                        "metric": "إجمالي التفاعل",
                        "value": executive_summary['engagement_total'],
                        "value_formatted": f"{executive_summary['engagement_total']:,}",
                        "icon": "💬",
                        "context": "إعجابات ومشاركات وتعليقات"
                    },
                    {
                        "metric": "الفعاليات المغطاة",
                        "value": executive_summary['events_covered'],
                        "icon": "🏆",
                        "context": "فعالية رياضية دولية كبرى"
                    },
                    {
                        "metric": "المعدل اليومي",
                        "value": round(executive_summary['total_mentions'] / 90),
                        "value_formatted": f"{round(executive_summary['total_mentions'] / 90):,}",
                        "icon": "📊",
                        "context": "مادة إعلامية يومياً في المتوسط"
                    }
                ],
                "insight": "تعكس هذه الأرقام حجم الاهتمام الإعلامي الكبير بالفعاليات الرياضية القطرية، مع هيمنة واضحة لمنصات التواصل الاجتماعي التي شكلت نحو 70% من إجمالي التغطية."
            },
            
            "scene_drivers": {
                "title": "3.2 محركات المشهد الإعلامي",
                "top_events_by_volume": {
                    "title": "الفعاليات الأكثر تغطية (حسب الحجم)",
                    "events": executive_summary['top_events_by_volume'],
                    "insight": "تصدرت كأس العرب قائمة الفعاليات الأكثر تغطية، ويعود ذلك إلى أهميتها الإقليمية وتزامنها مع ذكرى اليوم الوطني القطري."
                },
                "top_events_by_reach": {
                    "title": "الفعاليات الأعلى وصولاً (حسب الجمهور)",
                    "events": executive_summary['top_events_by_reach'],
                    "insight": "حققت UFC قطر أعلى وصول جماهيري رغم كونها ليست الأكثر تغطية، مما يعكس الجمهور العالمي الكبير لهذه الرياضة."
                },
                "key_drivers": [
                    {
                        "driver": "كأس العرب FIFA",
                        "impact": "محرك رئيسي للتغطية العربية",
                        "reason": "البطولة العربية الأبرز، فوز المغرب باللقب"
                    },
                    {
                        "driver": "فورمولا 1 قطر",
                        "impact": "جذب اهتمام عالمي واسع",
                        "reason": "سباق مثير على حلبة لوسيل الدولية"
                    },
                    {
                        "driver": "UFC قطر",
                        "impact": "أعلى وصول جماهيري",
                        "reason": "جمهور عالمي كبير، تغطية دولية مكثفة"
                    },
                    {
                        "driver": "كأس العالم تحت 17",
                        "impact": "اكتشاف المواهب الشابة",
                        "reason": "أول نسخة موسعة بـ 48 فريقاً"
                    }
                ]
            },
            
            "temporal_patterns": {
                "title": "3.3 الأنماط الزمنية",
                "peak_periods": [
                    {
                        "period": "أواخر نوفمبر 2025",
                        "events": ["سباق F1 قطر", "كأس العالم تحت 17"],
                        "description": "ذروة أولى مع تزامن سباق الفورمولا 1 ونهائيات كأس العالم للناشئين"
                    },
                    {
                        "period": "أوائل ديسمبر 2025",
                        "events": ["انطلاق كأس العرب"],
                        "description": "ذروة ثانية مع انطلاق كأس العرب والاهتمام العربي الكبير"
                    },
                    {
                        "period": "منتصف ديسمبر 2025",
                        "events": ["نهائي كأس العرب", "كأس القارات"],
                        "description": "الذروة الأعلى مع نهائي كأس العرب وتتويج المغرب"
                    },
                    {
                        "period": "يناير 2026",
                        "events": ["WTT Doha", "ماراثون الدوحة"],
                        "description": "استمرار النشاط مع بطولات تنس الطاولة والفعاليات المحلية"
                    }
                ],
                "daily_average": round(executive_summary['total_mentions'] / 90),
                "weekly_pattern": "ارتفاع ملحوظ في أيام المباريات والسباقات، وانخفاض نسبي في الفترات البينية"
            },
            
            "sentiment_drivers": {
                "title": "3.4 محركات الإيجابية والسلبية",
                "sentiment_overview": {
                    "positive": {
                        "percentage": executive_summary['overall_sentiment']['إيجابي'],
                        "count": executive_summary['sentiment_counts']['positive'],
                        "count_formatted": f"{executive_summary['sentiment_counts']['positive']:,}"
                    },
                    "negative": {
                        "percentage": executive_summary['overall_sentiment']['سلبي'],
                        "count": executive_summary['sentiment_counts']['negative'],
                        "count_formatted": f"{executive_summary['sentiment_counts']['negative']:,}"
                    },
                    "neutral": {
                        "percentage": executive_summary['overall_sentiment']['محايد'],
                        "count": executive_summary['sentiment_counts']['neutral'],
                        "count_formatted": f"{executive_summary['sentiment_counts']['neutral']:,}"
                    }
                },
                "positive_drivers": {
                    "title": "محركات الإيجابية",
                    "drivers": [
                        {
                            "driver": "نجاح التنظيم",
                            "description": "إشادة واسعة بالتنظيم المتقن للفعاليات الرياضية السبع",
                            "sentiment_rate": f"{topic_analysis.get('استضافة_وتنظيم', {}).get('positive_rate', 0)}%"
                        },
                        {
                            "driver": "جودة البنية التحتية",
                            "description": "الثناء على الملاعب والمنشآت الرياضية ذات المستوى العالمي",
                            "examples": ["استاد لوسيل", "حلبة لوسيل الدولية", "أسباير زون"]
                        },
                        {
                            "driver": "تجربة الجماهير",
                            "description": "ردود فعل إيجابية من الزوار والجماهير حول تجربتهم في قطر",
                            "sentiment_rate": f"{topic_analysis.get('جماهير_وتجربة', {}).get('positive_rate', 0)}%"
                        },
                        {
                            "driver": "الإشادة الدولية",
                            "description": "تصريحات إيجابية من المسؤولين الدوليين والرياضيين",
                            "examples": ["FIFA", "FIA", "UFC", "اللاعبين والمدربين"]
                        },
                        {
                            "driver": "الفعاليات التراثية",
                            "description": "اهتمام إيجابي بالفعاليات التراثية الفريدة",
                            "examples": ["مهرجان مرمي", "موسم سيلين", "لونجين هذاب"]
                        }
                    ]
                },
                "negative_drivers": {
                    "title": "محركات السلبية",
                    "drivers": [
                        {
                            "driver": "نتائج المنتخبات",
                            "description": "خيبة أمل من نتائج بعض المنتخبات الوطنية في البطولات",
                            "impact": "تأثير محدود على الصورة العامة"
                        },
                        {
                            "driver": "انتقادات تنظيمية محدودة",
                            "description": "بعض الملاحظات على جوانب تنظيمية معينة",
                            "impact": "نسبة ضئيلة من إجمالي التغطية"
                        },
                        {
                            "driver": "ربط بقضايا سياسية",
                            "description": "محاولات ربط الفعاليات الرياضية بقضايا سياسية غير مرتبطة",
                            "impact": "مصدره غالباً وسائل إعلام معادية"
                        }
                    ],
                    "mitigation_note": "النسبة الضئيلة للمحتوى السلبي (5.8%) تؤكد نجاح الفعاليات وإيجابية الانطباع العام"
                },
                "sentiment_by_topic": {
                    "title": "المشاعر حسب الموضوع",
                    "topics": [
                        {
                            "topic": "الاستضافة والتنظيم",
                            "positive_rate": topic_analysis.get('استضافة_وتنظيم', {}).get('positive_rate', 0),
                            "rank": 1,
                            "note": "أعلى نسبة إيجابية"
                        },
                        {
                            "topic": "الجماهير والتجربة",
                            "positive_rate": topic_analysis.get('جماهير_وتجربة', {}).get('positive_rate', 0),
                            "rank": 2
                        },
                        {
                            "topic": "المسؤولون",
                            "positive_rate": topic_analysis.get('مسؤولون', {}).get('positive_rate', 0),
                            "rank": 3
                        },
                        {
                            "topic": "الإرث والرؤية",
                            "positive_rate": topic_analysis.get('إرث_ورؤية', {}).get('positive_rate', 0),
                            "rank": 4
                        },
                        {
                            "topic": "الفعاليات الرياضية الكبرى",
                            "positive_rate": topic_analysis.get('فعاليات_رياضية_كبرى', {}).get('positive_rate', 0),
                            "rank": 5
                        },
                        {
                            "topic": "البنية التحتية",
                            "positive_rate": topic_analysis.get('بنية_تحتية', {}).get('positive_rate', 0),
                            "rank": 6
                        }
                    ]
                }
            },
            
            "key_takeaways": {
                "title": "الخلاصات الرئيسية",
                "takeaways": [
                    "تغطية إعلامية ضخمة بأكثر من 150 ألف مادة ووصول يتجاوز 134 مليار",
                    "نسبة الإيجابية (28%) تفوق السلبية (5.8%) بأكثر من 4 أضعاف",
                    "هيمنة منصات التواصل الاجتماعي بنسبة 70% من التغطية",
                    "موضوع الاستضافة والتنظيم يحقق أعلى نسبة إيجابية (42%)",
                    "تنوع جغرافي واسع في التغطية يعكس الاهتمام الدولي بقطر"
                ]
            }
        }
    }
    
    return phase1

def save_phase1():
    """حفظ المرحلة الأولى"""
    print("=" * 60)
    print("🇶🇦 المرحلة الأولى: المقدمة + المنهجية + الملخص التنفيذي")
    print("=" * 60)
    
    print("\n📂 جاري تحميل البيانات...")
    phase1 = build_phase1()
    
    print("💾 جاري حفظ المرحلة الأولى...")
    
    output_file = os.path.join(OUTPUT_PATH, 'phase1_introduction_methodology_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(phase1, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ تم حفظ المرحلة الأولى في: {output_file}")
    
    # طباعة ملخص
    print("\n" + "=" * 60)
    print("📋 محتويات المرحلة الأولى:")
    print("=" * 60)
    
    sections = [
        ("القسم 1", "المقدمة", "section_1_introduction", 2),
        ("القسم 2", "المنهجية", "section_2_methodology", 4),
        ("القسم 3", "الملخص التنفيذي", "section_3_executive_summary", 4)
    ]
    
    total_pages = 0
    for section_num, title, key, pages in sections:
        section_data = phase1.get(key, {})
        subsections = len([k for k in section_data.keys() if k not in ['section_number', 'title', 'page_count']])
        print(f"   {section_num}: {title}")
        print(f"      └── {subsections} قسم فرعي | {pages} صفحات")
        total_pages += pages
    
    print(f"\n   📄 إجمالي الصفحات: {total_pages} صفحة")
    
    print("\n" + "=" * 60)
    print("📊 أبرز الأرقام:")
    print("=" * 60)
    summary = phase1['section_3_executive_summary']['key_figures']
    for metric in summary['metrics'][:5]:
        print(f"   {metric['icon']} {metric['metric']}: {metric['value_formatted']}")
    
    print("\n" + "=" * 60)
    print("✅ المرحلة الأولى جاهزة!")
    print("=" * 60)
    
    return phase1

if __name__ == "__main__":
    phase1 = save_phase1()
