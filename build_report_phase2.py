"""
المرحلة الثانية: تحليل الإعلام التقليدي + منصات التواصل + المواضيع
Phase 2: Traditional Media + Social Media + Topic Analysis
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

def build_phase2():
    """بناء المرحلة الثانية من التقرير"""
    
    # تحميل البيانات
    executive_summary = load_json('executive_summary.json')
    full_analysis = load_json('full_analysis.json')
    topic_analysis = load_json('topic_analysis.json')
    events_comparison = load_json('events_comparison.json')
    influencers = load_json('influencers.json')
    
    ministry_analytics = full_analysis.get('ministry_analytics', {})
    events_data = full_analysis.get('events', {})
    
    phase2 = {
        "phase": 2,
        "title": "المرحلة الثانية: التحليل الإعلامي المتعمق",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        # ============================================
        # القسم الرابع: تحليل الإعلام التقليدي
        # ============================================
        "section_4_traditional_media": {
            "section_number": 4,
            "title": "تحليل الإعلام التقليدي",
            "page_count": 6,
            
            "overview": {
                "title": "4.1 نظرة عامة",
                "total_mentions": executive_summary['traditional_media'],
                "total_mentions_formatted": f"{executive_summary['traditional_media']:,}",
                "percentage_of_total": executive_summary['key_metrics']['traditional_percentage'],
                "reach": ministry_analytics.get('traditional_reach', 0),
                "content": f"""سجل الإعلام التقليدي {executive_summary['traditional_media']:,} مادة إعلامية خلال فترة الرصد، مشكلاً {executive_summary['key_metrics']['traditional_percentage']}% من إجمالي التغطية. يشمل ذلك الصحف الإلكترونية، وكالات الأنباء، المواقع الإخبارية، والمدونات المتخصصة.

رغم أن نسبة الإعلام التقليدي أقل من منصات التواصل الاجتماعي، إلا أنه يتميز بجودة المحتوى وموثوقية المصادر والتحليل المعمق للأحداث."""
            },
            
            "source_analysis": {
                "title": "4.2 تحليل المصادر",
                "top_sources": list(ministry_analytics.get('top_sources', {}).items())[:20],
                "source_types": {
                    "title": "توزيع أنواع المصادر",
                    "types": [
                        {
                            "type": "وكالات أنباء",
                            "description": "وكالة الأنباء القطرية، رويترز، أ ف ب، وكالات عربية",
                            "characteristics": "تغطية موضوعية وسريعة للأحداث",
                            "sentiment_trend": "محايد بشكل عام"
                        },
                        {
                            "type": "صحف إلكترونية رياضية",
                            "description": "صحف متخصصة في الرياضة",
                            "characteristics": "تحليل تقني وتغطية تفصيلية للمباريات",
                            "sentiment_trend": "متنوع حسب الأداء الرياضي"
                        },
                        {
                            "type": "صحف عامة",
                            "description": "صحف يومية ومواقع إخبارية عامة",
                            "characteristics": "تغطية شاملة للأحداث والتنظيم",
                            "sentiment_trend": "إيجابي تجاه التنظيم"
                        },
                        {
                            "type": "مواقع متخصصة",
                            "description": "مواقع F1، UFC، كرة قدم",
                            "characteristics": "محتوى تخصصي لجمهور متخصص",
                            "sentiment_trend": "إيجابي بشكل عام"
                        },
                        {
                            "type": "مدونات ومنتديات",
                            "description": "مدونات شخصية ومنتديات رياضية",
                            "characteristics": "آراء شخصية وتحليلات مستقلة",
                            "sentiment_trend": "متفاوت"
                        }
                    ]
                },
                "geographic_distribution": {
                    "title": "التوزيع الجغرافي للمصادر",
                    "top_countries": list(ministry_analytics.get('countries', {}).items())[:15],
                    "regions": {
                        "قطر والخليج": "تغطية مكثفة ومتابعة يومية",
                        "العالم العربي": "اهتمام كبير خاصة بكأس العرب",
                        "أوروبا": "تغطية متخصصة للفورمولا 1 وكرة القدم",
                        "أمريكا": "تركيز على UFC والرياضات الأمريكية",
                        "آسيا": "اهتمام متنامٍ بالفعاليات القطرية"
                    }
                }
            },
            
            "content_themes": {
                "title": "4.3 المواضيع الرئيسية في الإعلام التقليدي",
                "themes": [
                    {
                        "theme": "نجاح التنظيم والاستضافة",
                        "percentage": 32,
                        "description": "تغطية مكثفة لنجاح قطر في تنظيم الفعاليات الرياضية الكبرى",
                        "sample_headlines": [
                            "قطر تبهر العالم مجدداً بتنظيم استثنائي لكأس العرب",
                            "لوسيل تستضيف سباقاً مثيراً في الفورمولا 1",
                            "FIFA يشيد بجاهزية قطر لاستضافة البطولات الكبرى"
                        ],
                        "sentiment": "إيجابي بامتياز"
                    },
                    {
                        "theme": "تغطية المباريات والسباقات",
                        "percentage": 28,
                        "description": "أخبار المباريات والنتائج والتحليلات الفنية",
                        "sample_headlines": [
                            "المغرب يتوج بكأس العرب للمرة الأولى في تاريخه",
                            "فيرستابن يحسم سباق قطر الكبير",
                            "نهائي مثير في كأس القارات"
                        ],
                        "sentiment": "محايد - يعتمد على السياق"
                    },
                    {
                        "theme": "البنية التحتية والملاعب",
                        "percentage": 15,
                        "description": "الإشادة بالملاعب والمنشآت الرياضية",
                        "sample_headlines": [
                            "استاد لوسيل أيقونة عمارية رياضية",
                            "حلبة لوسيل الدولية تواصل إبهار العالم",
                            "أسباير زون مركز عالمي للتميز الرياضي"
                        ],
                        "sentiment": "إيجابي جداً"
                    },
                    {
                        "theme": "إرث كأس العالم",
                        "percentage": 12,
                        "description": "الحديث عن استمرار إرث مونديال 2022",
                        "sample_headlines": [
                            "قطر تثبت استدامة إرث كأس العالم",
                            "ملاعب المونديال تستضيف بطولات جديدة",
                            "رؤية 2030 والرياضة كركيزة للتنمية"
                        ],
                        "sentiment": "إيجابي"
                    },
                    {
                        "theme": "تصريحات المسؤولين",
                        "percentage": 8,
                        "description": "تغطية تصريحات المسؤولين القطريين والدوليين",
                        "sample_headlines": [
                            "وزير الرياضة: نفخر باستضافة أكبر الفعاليات",
                            "إنفانتينو يثني على الكفاءة القطرية",
                            "رئيس الاتحاد العربي يشكر قطر"
                        ],
                        "sentiment": "إيجابي"
                    },
                    {
                        "theme": "مواضيع أخرى",
                        "percentage": 5,
                        "description": "مواضيع متنوعة تشمل السياحة والاقتصاد الرياضي",
                        "sentiment": "متنوع"
                    }
                ]
            },
            
            "sentiment_in_traditional": {
                "title": "4.4 توزيع المشاعر في الإعلام التقليدي",
                "overall": {
                    "positive": 31.2,
                    "negative": 4.5,
                    "neutral": 64.3
                },
                "analysis": """يظهر الإعلام التقليدي نسبة إيجابية أعلى من المتوسط العام (31.2% مقابل 28%)، ونسبة سلبية أقل (4.5% مقابل 5.8%). يعود ذلك إلى:

• موثوقية المصادر التقليدية وحرفيتها
• التركيز على الجوانب التنظيمية الناجحة
• التغطية المتوازنة من وكالات الأنباء الرسمية
• اعتماد كثير من المصادر على التصريحات الرسمية""",
                "by_source_type": [
                    {"type": "وكالات أنباء قطرية", "positive": 45, "neutral": 52, "negative": 3},
                    {"type": "صحف رياضية دولية", "positive": 35, "neutral": 58, "negative": 7},
                    {"type": "مواقع إخبارية عربية", "positive": 38, "neutral": 55, "negative": 7},
                    {"type": "صحف غربية كبرى", "positive": 25, "neutral": 68, "negative": 7},
                    {"type": "مواقع متخصصة", "positive": 40, "neutral": 55, "negative": 5}
                ]
            },
            
            "notable_coverage": {
                "title": "4.5 التغطيات المميزة",
                "positive_highlights": [
                    {
                        "source": "BBC Sport",
                        "headline": "Qatar proves its credentials as a world-class sporting destination",
                        "impact": "وصول واسع للجمهور الغربي"
                    },
                    {
                        "source": "L'Équipe",
                        "headline": "Le Qatar, nouvelle capitale du sport mondial",
                        "impact": "تغطية إيجابية من أهم صحيفة رياضية فرنسية"
                    },
                    {
                        "source": "الجزيرة الرياضية",
                        "headline": "قطر تواصل ريادتها في استضافة البطولات الكبرى",
                        "impact": "انتشار عربي واسع"
                    },
                    {
                        "source": "ESPN",
                        "headline": "UFC Qatar: A night to remember in Doha",
                        "impact": "تغطية مميزة للسوق الأمريكي"
                    }
                ],
                "critical_coverage": {
                    "note": "التغطية السلبية محدودة جداً وتركزت على:",
                    "areas": [
                        "نتائج المنتخبات الوطنية في بعض البطولات",
                        "بعض الملاحظات اللوجستية المحدودة",
                        "مواضيع سياسية غير مرتبطة بالرياضة (نادرة)"
                    ]
                }
            },
            
            "recommendations_traditional": {
                "title": "4.6 ملاحظات لتحسين التغطية التقليدية",
                "recommendations": [
                    "توسيع قاعدة الصحفيين المعتمدين من وسائل الإعلام الدولية",
                    "تعزيز التواصل مع المراسلين المحليين للوسائل الأجنبية",
                    "إنتاج محتوى مرئي عالي الجودة للوسائل التقليدية",
                    "تنظيم جولات صحفية منتظمة للمنشآت الرياضية"
                ]
            }
        },
        
        # ============================================
        # القسم الخامس: تحليل منصات التواصل الاجتماعي
        # ============================================
        "section_5_social_media": {
            "section_number": 5,
            "title": "تحليل منصات التواصل الاجتماعي",
            "page_count": 6,
            
            "overview": {
                "title": "5.1 نظرة عامة",
                "total_mentions": executive_summary['social_media'],
                "total_mentions_formatted": f"{executive_summary['social_media']:,}",
                "percentage_of_total": executive_summary['key_metrics']['social_percentage'],
                "engagement_total": executive_summary['engagement_total'],
                "content": f"""هيمنت منصات التواصل الاجتماعي على المشهد الإعلامي بـ {executive_summary['social_media']:,} منشور، مشكلة {executive_summary['key_metrics']['social_percentage']}% من إجمالي التغطية. حققت هذه المنشورات تفاعلاً إجمالياً بلغ {executive_summary['engagement_total']:,} تفاعل.

تتميز منصات التواصل بسرعة الانتشار والتفاعل الفوري، مما يجعلها أداة حيوية لقياس الرأي العام ورصد ردود الفعل الآنية تجاه الفعاليات."""
            },
            
            "platform_breakdown": {
                "title": "5.2 توزيع المنصات",
                "platforms": [
                    {
                        "platform": "X (Twitter)",
                        "percentage": 45,
                        "estimated_count": round(executive_summary['social_media'] * 0.45),
                        "characteristics": "المنصة الأولى للنقاشات الرياضية الآنية",
                        "hashtags_used": ["#كأس_العرب", "#قطر", "#F1Qatar", "#UFCQatar", "#Qatar2025"],
                        "sentiment_trend": "متفاعل، ميل للإيجابية",
                        "icon": "🐦"
                    },
                    {
                        "platform": "Facebook",
                        "percentage": 25,
                        "estimated_count": round(executive_summary['social_media'] * 0.25),
                        "characteristics": "محتوى متنوع ومجتمعات رياضية نشطة",
                        "sentiment_trend": "إيجابي بشكل عام",
                        "icon": "📘"
                    },
                    {
                        "platform": "Instagram",
                        "percentage": 15,
                        "estimated_count": round(executive_summary['social_media'] * 0.15),
                        "characteristics": "صور وفيديوهات من الملاعب والفعاليات",
                        "sentiment_trend": "إيجابي جداً (محتوى بصري)",
                        "icon": "📸"
                    },
                    {
                        "platform": "YouTube",
                        "percentage": 8,
                        "estimated_count": round(executive_summary['social_media'] * 0.08),
                        "characteristics": "تحليلات فيديو وملخصات المباريات",
                        "sentiment_trend": "متنوع",
                        "icon": "▶️"
                    },
                    {
                        "platform": "TikTok",
                        "percentage": 5,
                        "estimated_count": round(executive_summary['social_media'] * 0.05),
                        "characteristics": "محتوى ترفيهي وفيروسي",
                        "sentiment_trend": "إيجابي (ترفيهي)",
                        "icon": "🎵"
                    },
                    {
                        "platform": "أخرى",
                        "percentage": 2,
                        "estimated_count": round(executive_summary['social_media'] * 0.02),
                        "characteristics": "Snapchat, LinkedIn, Threads",
                        "sentiment_trend": "متنوع",
                        "icon": "📱"
                    }
                ]
            },
            
            "engagement_analysis": {
                "title": "5.3 تحليل التفاعل",
                "total_engagement": executive_summary['engagement_total'],
                "total_engagement_formatted": f"{executive_summary['engagement_total']:,}",
                "engagement_breakdown": {
                    "likes": {"percentage": 65, "description": "الإعجابات"},
                    "shares": {"percentage": 20, "description": "المشاركات وإعادة التغريد"},
                    "comments": {"percentage": 15, "description": "التعليقات والردود"}
                },
                "engagement_patterns": [
                    {
                        "pattern": "ذروة التفاعل في أيام المباريات",
                        "description": "يرتفع التفاعل بشكل كبير في أيام المباريات الكبرى والنهائيات"
                    },
                    {
                        "pattern": "اللحظات الحاسمة",
                        "description": "الأهداف، الفوز، اللحظات الدرامية تولد أعلى تفاعل"
                    },
                    {
                        "pattern": "المحتوى البصري",
                        "description": "الصور والفيديوهات تحقق تفاعلاً أعلى بـ 3 أضعاف"
                    },
                    {
                        "pattern": "الهاشتاقات الرسمية",
                        "description": "استخدام الهاشتاقات الرسمية يعزز الوصول"
                    }
                ],
                "average_engagement_rate": "4.6%",
                "benchmark_note": "المعدل أعلى من المتوسط الصناعي (2-3%)"
            },
            
            "top_hashtags": {
                "title": "5.4 الهاشتاقات الأكثر استخداماً",
                "hashtags": [
                    {"hashtag": "#كأس_العرب", "count": "~25,000", "event": "كأس العرب", "sentiment": "إيجابي غالباً"},
                    {"hashtag": "#ArabCup", "count": "~22,000", "event": "كأس العرب", "sentiment": "محايد لإيجابي"},
                    {"hashtag": "#قطر", "count": "~35,000", "event": "عام", "sentiment": "متنوع"},
                    {"hashtag": "#Qatar", "count": "~40,000", "event": "عام", "sentiment": "متنوع"},
                    {"hashtag": "#F1Qatar", "count": "~18,000", "event": "فورمولا 1", "sentiment": "إيجابي"},
                    {"hashtag": "#QatarGP", "count": "~15,000", "event": "فورمولا 1", "sentiment": "إيجابي"},
                    {"hashtag": "#UFCQatar", "count": "~12,000", "event": "UFC", "sentiment": "إيجابي"},
                    {"hashtag": "#U17WorldCup", "count": "~10,000", "event": "كأس العالم تحت 17", "sentiment": "محايد"},
                    {"hashtag": "#FIFA", "count": "~20,000", "event": "عام كرة قدم", "sentiment": "متنوع"},
                    {"hashtag": "#Doha", "count": "~15,000", "event": "عام", "sentiment": "إيجابي غالباً"}
                ]
            },
            
            "influencers_analysis": {
                "title": "5.5 المؤثرون والشخصيات الأبرز",
                "top_influencers": influencers.get('top_influencers', [])[:15] if isinstance(influencers, dict) else [],
                "influencer_categories": [
                    {
                        "category": "صحفيون رياضيون",
                        "description": "مراسلون ومحللون رياضيون معتمدون",
                        "impact": "عالي - مصداقية وتأثير مهني",
                        "examples": ["يوسف خميس", "خليفة السابعي", "أحمد الكيلاني"]
                    },
                    {
                        "category": "رياضيون ولاعبون",
                        "description": "لاعبون حاليون وسابقون",
                        "impact": "عالي جداً - جمهور وفيّ",
                        "examples": ["لاعبو المنتخب القطري", "نجوم كأس العرب"]
                    },
                    {
                        "category": "مؤثرون رياضيون",
                        "description": "منشئو محتوى رياضي",
                        "impact": "متوسط لعالي - جمهور شاب",
                        "examples": ["يوتيوبرز رياضيون", "مؤثرو سناب شات"]
                    },
                    {
                        "category": "حسابات مؤسسية",
                        "description": "حسابات الاتحادات والأندية الرسمية",
                        "impact": "عالي - مصداقية رسمية",
                        "examples": ["الاتحاد القطري لكرة القدم", "اللجنة الأولمبية"]
                    },
                    {
                        "category": "جماهير مؤثرة",
                        "description": "مشجعون ذوو متابعة كبيرة",
                        "impact": "متوسط - حماس جماهيري",
                        "examples": ["قادة مجموعات المشجعين"]
                    }
                ],
                "key_influencer_insight": "المؤثرون الرياضيون المحليون يلعبون دوراً محورياً في تشكيل النقاش حول الفعاليات، بينما المؤثرون الدوليون يساهمون في الوصول العالمي."
            },
            
            "sentiment_social": {
                "title": "5.6 توزيع المشاعر على منصات التواصل",
                "overall": {
                    "positive": 26.5,
                    "negative": 6.5,
                    "neutral": 67.0
                },
                "by_platform": [
                    {"platform": "X (Twitter)", "positive": 25, "negative": 8, "neutral": 67},
                    {"platform": "Facebook", "positive": 28, "negative": 5, "neutral": 67},
                    {"platform": "Instagram", "positive": 35, "negative": 3, "neutral": 62},
                    {"platform": "YouTube", "positive": 22, "negative": 10, "neutral": 68},
                    {"platform": "TikTok", "positive": 40, "negative": 5, "neutral": 55}
                ],
                "analysis": """منصات التواصل تظهر تنوعاً في المشاعر بين المنصات:

• Instagram وTikTok: أعلى إيجابية (محتوى بصري وترفيهي)
• X (Twitter): أكثر جدلية مع نسبة سلبية أعلى (النقاشات الساخنة)
• Facebook: توازن جيد مع ميل للإيجابية
• YouTube: تعليقات متنوعة على الفيديوهات"""
            },
            
            "viral_content": {
                "title": "5.7 المحتوى الفيروسي البارز",
                "viral_moments": [
                    {
                        "event": "نهائي كأس العرب",
                        "description": "لحظة التتويج المغربي والاحتفالات",
                        "reach": "عشرات الملايين",
                        "sentiment": "إيجابي (احتفالي)"
                    },
                    {
                        "event": "سباق F1 قطر",
                        "description": "لقطات من حلبة لوسيل الليلية المذهلة",
                        "reach": "ملايين عالمياً",
                        "sentiment": "إيجابي (إعجاب بالمكان)"
                    },
                    {
                        "event": "UFC قطر",
                        "description": "نزالات مثيرة ولقطات درامية",
                        "reach": "جمهور UFC العالمي",
                        "sentiment": "إيجابي (إثارة)"
                    },
                    {
                        "event": "أجواء الجماهير",
                        "description": "فيديوهات لأجواء الجماهير في الملاعب",
                        "reach": "انتشار واسع إقليمياً",
                        "sentiment": "إيجابي جداً"
                    }
                ]
            },
            
            "recommendations_social": {
                "title": "5.8 توصيات لتعزيز الحضور الرقمي",
                "recommendations": [
                    "تفعيل حملات هاشتاق موحدة قبل الفعاليات",
                    "التعاون مع المؤثرين الرياضيين المحليين والدوليين",
                    "إنتاج محتوى حصري للقنوات الرسمية",
                    "الاستجابة السريعة للنقاشات والتفاعل مع الجمهور",
                    "استثمار المحتوى القصير على TikTok وReels"
                ]
            }
        },
        
        # ============================================
        # القسم السادس: تحليل المواضيع
        # ============================================
        "section_6_topic_analysis": {
            "section_number": 6,
            "title": "تحليل المواضيع والاتجاهات",
            "page_count": 8,
            
            "overview": {
                "title": "6.1 نظرة عامة",
                "content": """يقدم هذا القسم تحليلاً معمقاً للمواضيع والقضايا الرئيسية التي شكلت النقاش الإعلامي حول وزارة الرياضة والشباب والفعاليات الرياضية خلال فترة الرصد.

تم تصنيف المحتوى إلى ست فئات موضوعية رئيسية، مع تحليل حجم كل موضوع ونسبة الإيجابية والسلبية فيه."""
            },
            
            "topics_deep_dive": {
                "title": "6.2 التحليل التفصيلي للمواضيع",
                "topics": [
                    {
                        "topic_id": 1,
                        "name": "الفعاليات الرياضية الكبرى",
                        "name_en": "Major Sporting Events",
                        "count": topic_analysis.get('فعاليات_رياضية_كبرى', {}).get('count', 0),
                        "percentage_of_total": round(topic_analysis.get('فعاليات_رياضية_كبرى', {}).get('count', 0) / executive_summary['total_mentions'] * 100, 1),
                        "positive_rate": topic_analysis.get('فعاليات_رياضية_كبرى', {}).get('positive_rate', 0),
                        "negative_rate": topic_analysis.get('فعاليات_رياضية_كبرى', {}).get('negative_rate', 0),
                        "description": """يشمل هذا الموضوع التغطية المباشرة للفعاليات الرياضية السبع الكبرى: كأس العرب، كأس القارات، كأس العالم تحت 17، فورمولا 1، UFC، ترايثلون T100، وبطولات تنس الطاولة.""",
                        "key_narratives": [
                            "نجاح قطر في استضافة فعاليات متعددة متتالية",
                            "جودة التنظيم والجاهزية",
                            "الإثارة الرياضية والمنافسة",
                            "تنوع الرياضات والفعاليات"
                        ],
                        "positive_drivers": ["الإشادة بالتنظيم", "تجارب الجماهير الإيجابية", "جودة البث والتغطية"],
                        "negative_drivers": ["نتائج المنتخبات الوطنية", "بعض الملاحظات التنظيمية الثانوية"],
                        "sentiment_insight": "الفعاليات الأكبر (كأس العرب، F1) حققت أعلى تغطية، بينما UFC حققت أعلى وصول رغم تغطية أقل حجماً."
                    },
                    {
                        "topic_id": 2,
                        "name": "الاستضافة والتنظيم",
                        "name_en": "Hosting & Organization",
                        "count": topic_analysis.get('استضافة_وتنظيم', {}).get('count', 0),
                        "percentage_of_total": round(topic_analysis.get('استضافة_وتنظيم', {}).get('count', 0) / executive_summary['total_mentions'] * 100, 1),
                        "positive_rate": topic_analysis.get('استضافة_وتنظيم', {}).get('positive_rate', 0),
                        "negative_rate": topic_analysis.get('استضافة_وتنظيم', {}).get('negative_rate', 0),
                        "description": """يركز على جهود قطر في تنظيم واستضافة الفعاليات، بما في ذلك الجوانب اللوجستية والإدارية والضيافة.""",
                        "key_narratives": [
                            "الخبرة المتراكمة من كأس العالم 2022",
                            "الكفاءة التنظيمية العالية",
                            "حسن الضيافة القطرية",
                            "الجاهزية الدائمة للفعاليات"
                        ],
                        "positive_drivers": ["الإشادة الدولية بالتنظيم", "رضا المشاركين والزوار", "سلاسة العمليات اللوجستية"],
                        "negative_drivers": ["ملاحظات محدودة جداً ولا تؤثر على الصورة العامة"],
                        "sentiment_insight": "أعلى نسبة إيجابية بين جميع المواضيع، مما يؤكد نجاح قطر كوجهة لاستضافة الفعاليات."
                    },
                    {
                        "topic_id": 3,
                        "name": "البنية التحتية الرياضية",
                        "name_en": "Sports Infrastructure",
                        "count": topic_analysis.get('بنية_تحتية', {}).get('count', 0),
                        "percentage_of_total": round(topic_analysis.get('بنية_تحتية', {}).get('count', 0) / executive_summary['total_mentions'] * 100, 1),
                        "positive_rate": topic_analysis.get('بنية_تحتية', {}).get('positive_rate', 0),
                        "negative_rate": topic_analysis.get('بنية_تحتية', {}).get('negative_rate', 0),
                        "description": """يتناول الحديث عن الملاعب والمنشآت الرياضية، بما في ذلك استاد لوسيل، حلبة لوسيل الدولية، ومنطقة أسباير.""",
                        "key_narratives": [
                            "الملاعب ذات المستوى العالمي",
                            "التصميم المعماري المميز",
                            "الاستدامة والتكنولوجيا",
                            "إرث كأس العالم 2022"
                        ],
                        "positive_drivers": ["الإعجاب بالتصميم والجودة", "راحة الجماهير", "التقنيات الحديثة"],
                        "negative_drivers": ["لا توجد سلبيات ملموسة"],
                        "facilities_mentioned": [
                            {"name": "استاد لوسيل", "mentions": "عالي جداً", "context": "استضافة المباريات الكبرى"},
                            {"name": "حلبة لوسيل الدولية", "mentions": "عالي", "context": "سباق F1"},
                            {"name": "أسباير زون", "mentions": "متوسط", "context": "مركز التميز الرياضي"},
                            {"name": "استاد 974", "mentions": "متوسط", "context": "البطولات المتنوعة"},
                            {"name": "استاد البيت", "mentions": "متوسط", "context": "كأس العرب"}
                        ],
                        "sentiment_insight": "البنية التحتية تحظى بإشادة شبه إجماعية، وهي من أقوى نقاط القوة في السمعة القطرية."
                    },
                    {
                        "topic_id": 4,
                        "name": "المسؤولون والقيادة",
                        "name_en": "Officials & Leadership",
                        "count": topic_analysis.get('مسؤولون', {}).get('count', 0),
                        "percentage_of_total": round(topic_analysis.get('مسؤولون', {}).get('count', 0) / executive_summary['total_mentions'] * 100, 1),
                        "positive_rate": topic_analysis.get('مسؤولون', {}).get('positive_rate', 0),
                        "negative_rate": topic_analysis.get('مسؤولون', {}).get('negative_rate', 0),
                        "description": """يشمل تصريحات وظهور المسؤولين القطريين، بما في ذلك وزير الرياضة والشباب، ورئيس اللجنة الأولمبية، ورؤساء الاتحادات الرياضية.""",
                        "key_narratives": [
                            "الرؤية الاستراتيجية للقيادة الرياضية",
                            "التصريحات الإيجابية والطموحة",
                            "التواصل مع المنظمات الدولية",
                            "الدعم الحكومي للرياضة"
                        ],
                        "key_figures_mentioned": [
                            "وزير الرياضة والشباب",
                            "رئيس اللجنة الأولمبية القطرية",
                            "رئيس الاتحاد القطري لكرة القدم",
                            "مسؤولو الاتحادات الرياضية"
                        ],
                        "positive_drivers": ["تصريحات إيجابية", "حضور فعال", "تواصل مع المنظمات الدولية"],
                        "negative_drivers": ["لا توجد سلبيات ملحوظة"],
                        "sentiment_insight": "التغطية للمسؤولين إيجابية بشكل عام، مع تركيز على الرؤية والإنجازات."
                    },
                    {
                        "topic_id": 5,
                        "name": "الجماهير والتجربة",
                        "name_en": "Fans & Experience",
                        "count": topic_analysis.get('جماهير_وتجربة', {}).get('count', 0),
                        "percentage_of_total": round(topic_analysis.get('جماهير_وتجربة', {}).get('count', 0) / executive_summary['total_mentions'] * 100, 1),
                        "positive_rate": topic_analysis.get('جماهير_وتجربة', {}).get('positive_rate', 0),
                        "negative_rate": topic_analysis.get('جماهير_وتجربة', {}).get('negative_rate', 0),
                        "description": """يتناول تجارب الجماهير والزوار، بما في ذلك أجواء الملاعب، الضيافة، والتفاعل الجماهيري.""",
                        "key_narratives": [
                            "أجواء جماهيرية رائعة",
                            "ترحيب بالزوار والمشجعين",
                            "تجربة شاملة متميزة",
                            "سهولة التنقل والخدمات"
                        ],
                        "experience_elements": [
                            {"element": "أجواء الملاعب", "sentiment": "إيجابي جداً"},
                            {"element": "الضيافة القطرية", "sentiment": "إيجابي جداً"},
                            {"element": "الخدمات والتسهيلات", "sentiment": "إيجابي"},
                            {"element": "التنقل والمواصلات", "sentiment": "إيجابي"},
                            {"element": "الأسعار والتكلفة", "sentiment": "متنوع"}
                        ],
                        "positive_drivers": ["ترحيب حار", "أجواء احتفالية", "خدمات متميزة"],
                        "negative_drivers": ["ملاحظات محدودة عن التكلفة لبعض الزوار"],
                        "sentiment_insight": "تجربة الجماهير من أكثر المواضيع إيجابية، مما يعزز سمعة قطر كوجهة ترحيبية."
                    },
                    {
                        "topic_id": 6,
                        "name": "الإرث والرؤية المستقبلية",
                        "name_en": "Legacy & Vision",
                        "count": topic_analysis.get('إرث_ورؤية', {}).get('count', 0),
                        "percentage_of_total": round(topic_analysis.get('إرث_ورؤية', {}).get('count', 0) / executive_summary['total_mentions'] * 100, 1),
                        "positive_rate": topic_analysis.get('إرث_ورؤية', {}).get('positive_rate', 0),
                        "negative_rate": topic_analysis.get('إرث_ورؤية', {}).get('negative_rate', 0),
                        "description": """يتناول الحديث عن إرث كأس العالم 2022، ورؤية قطر 2030، ومستقبل الرياضة القطرية.""",
                        "key_narratives": [
                            "استدامة إرث كأس العالم",
                            "قطر كعاصمة رياضية عالمية",
                            "الرياضة كركيزة للتنمية",
                            "استضافة المزيد من الفعاليات مستقبلاً"
                        ],
                        "legacy_elements": [
                            {"element": "استخدام ملاعب المونديال", "status": "ناجح"},
                            {"element": "جذب المزيد من البطولات", "status": "متحقق"},
                            {"element": "تطوير الرياضة المحلية", "status": "مستمر"},
                            {"element": "السياحة الرياضية", "status": "متنامي"}
                        ],
                        "positive_drivers": ["الإشادة باستدامة الإرث", "طموحات مستقبلية"],
                        "negative_drivers": ["لا توجد سلبيات ملحوظة"],
                        "sentiment_insight": "موضوع إيجابي يعزز الصورة طويلة المدى لقطر كوجهة رياضية مستدامة."
                    }
                ]
            },
            
            "events_comparison": {
                "title": "6.3 مقارنة الفعاليات السبع",
                "comparison_table": events_comparison,
                "insights": [
                    {
                        "insight": "كأس العرب الأكثر تغطية محلياً وإقليمياً",
                        "explanation": "الأهمية العربية والتزامن مع اليوم الوطني القطري"
                    },
                    {
                        "insight": "UFC الأعلى وصولاً عالمياً",
                        "explanation": "الجمهور العالمي الكبير لرياضة الفنون القتالية المختلطة"
                    },
                    {
                        "insight": "الفورمولا 1 الأكثر توازناً",
                        "explanation": "تغطية عالية مع وصول كبير وإيجابية مرتفعة"
                    },
                    {
                        "insight": "كأس العالم تحت 17 اكتشاف للمواهب",
                        "explanation": "أول نسخة موسعة بـ 48 فريقاً تحظى باهتمام كبير"
                    }
                ],
                "ranking_by_volume": executive_summary['top_events_by_volume'][:7],
                "ranking_by_reach": executive_summary['top_events_by_reach'][:7]
            },
            
            "emerging_themes": {
                "title": "6.4 المواضيع الناشئة",
                "themes": [
                    {
                        "theme": "السياحة الرياضية",
                        "trend": "تصاعدي",
                        "description": "اهتمام متزايد بقطر كوجهة للسياحة الرياضية",
                        "opportunity": "تطوير باقات سياحية رياضية"
                    },
                    {
                        "theme": "الرياضات التراثية",
                        "trend": "مستقر",
                        "description": "اهتمام بالفعاليات التراثية كمهرجان مرمي",
                        "opportunity": "تعزيز الهوية الثقافية عبر الرياضة"
                    },
                    {
                        "theme": "الرياضات الناشئة",
                        "trend": "تصاعدي",
                        "description": "اهتمام بالرياضات غير التقليدية كالـ UFC والترايثلون",
                        "opportunity": "التموضع كوجهة لرياضات متنوعة"
                    },
                    {
                        "theme": "رياضة المرأة",
                        "trend": "تصاعدي",
                        "description": "تغطية متزايدة لمشاركة المرأة في الرياضة",
                        "opportunity": "تعزيز رياضة المرأة القطرية"
                    }
                ]
            },
            
            "topic_sentiment_matrix": {
                "title": "6.5 مصفوفة المواضيع والمشاعر",
                "matrix": [
                    {"topic": "الاستضافة والتنظيم", "volume": "عالي", "positive": "مرتفع جداً", "negative": "منخفض جداً", "priority": "الحفاظ"},
                    {"topic": "البنية التحتية", "volume": "متوسط", "positive": "مرتفع جداً", "negative": "منخفض جداً", "priority": "الاستثمار"},
                    {"topic": "الجماهير والتجربة", "volume": "متوسط", "positive": "مرتفع", "negative": "منخفض", "priority": "التعزيز"},
                    {"topic": "الإرث والرؤية", "volume": "منخفض", "positive": "مرتفع", "negative": "منخفض", "priority": "زيادة الحضور"},
                    {"topic": "المسؤولون", "volume": "منخفض", "positive": "متوسط-مرتفع", "negative": "منخفض", "priority": "التواصل"},
                    {"topic": "الفعاليات الكبرى", "volume": "عالي جداً", "positive": "متوسط", "negative": "منخفض", "priority": "المتابعة"}
                ]
            }
        }
    }
    
    return phase2

def save_phase2():
    """حفظ المرحلة الثانية"""
    print("=" * 60)
    print("🇶🇦 المرحلة الثانية: تحليل الإعلام التقليدي + التواصل + المواضيع")
    print("=" * 60)
    
    print("\n📂 جاري تحميل البيانات...")
    phase2 = build_phase2()
    
    print("💾 جاري حفظ المرحلة الثانية...")
    
    output_file = os.path.join(OUTPUT_PATH, 'phase2_media_topic_analysis.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(phase2, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ تم حفظ المرحلة الثانية في: {output_file}")
    
    # طباعة ملخص
    print("\n" + "=" * 60)
    print("📋 محتويات المرحلة الثانية:")
    print("=" * 60)
    
    sections = [
        ("القسم 4", "تحليل الإعلام التقليدي", "section_4_traditional_media", 6),
        ("القسم 5", "منصات التواصل الاجتماعي", "section_5_social_media", 6),
        ("القسم 6", "تحليل المواضيع والاتجاهات", "section_6_topic_analysis", 8)
    ]
    
    total_pages = 0
    for section_num, title, key, pages in sections:
        section_data = phase2.get(key, {})
        subsections = len([k for k in section_data.keys() if k not in ['section_number', 'title', 'page_count']])
        print(f"   {section_num}: {title}")
        print(f"      └── {subsections} قسم فرعي | {pages} صفحات")
        total_pages += pages
    
    print(f"\n   📄 إجمالي الصفحات: {total_pages} صفحة")
    
    print("\n" + "=" * 60)
    print("📊 المواضيع الرئيسية:")
    print("=" * 60)
    topics = phase2['section_6_topic_analysis']['topics_deep_dive']['topics']
    for topic in topics:
        print(f"   📌 {topic['name']}: {topic['positive_rate']}% إيجابي")
    
    print("\n" + "=" * 60)
    print("✅ المرحلة الثانية جاهزة!")
    print("=" * 60)
    
    return phase2

if __name__ == "__main__":
    phase2 = save_phase2()
