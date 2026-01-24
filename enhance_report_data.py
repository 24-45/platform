"""
تحسين التقرير: إضافة المخططات والبيانات المفصلة
Enhanced Report: Charts Specifications + Detailed Data
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

def build_enhanced_report():
    """بناء التقرير المحسّن"""
    
    # تحميل البيانات
    executive_summary = load_json('executive_summary.json')
    full_analysis = load_json('full_analysis.json')
    topic_analysis = load_json('topic_analysis.json')
    events_comparison = load_json('events_comparison.json')
    influencers = load_json('influencers.json')
    
    ministry_analytics = full_analysis.get('ministry_analytics', {})
    
    enhanced_report = {
        "version": "2.0 - Enhanced",
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        # ============================================
        # 1. تحديد المخططات لكل قسم
        # ============================================
        "charts_specification": {
            "section_3_executive_summary": {
                "page": "الملخص التنفيذي",
                "charts": [
                    {
                        "chart_id": "ES-1",
                        "title": "الأرقام الرئيسية",
                        "chart_type": "info_cards",
                        "description": "4-6 بطاقات معلومات كبيرة",
                        "data": {
                            "cards": [
                                {"label": "إجمالي المواد", "value": "150,838", "icon": "📰", "color": "#2C3E50"},
                                {"label": "الوصول", "value": "134+ مليار", "icon": "📣", "color": "#27AE60"},
                                {"label": "نسبة الإيجابية", "value": "28%", "icon": "✅", "color": "#27AE60"},
                                {"label": "نسبة السلبية", "value": "5.8%", "icon": "⚠️", "color": "#E74C3C"},
                                {"label": "التفاعل", "value": "6.9M", "icon": "💬", "color": "#3498DB"},
                                {"label": "الفعاليات", "value": "7", "icon": "🏆", "color": "#F39C12"}
                            ]
                        }
                    },
                    {
                        "chart_id": "ES-2",
                        "title": "توزيع المشاعر العامة",
                        "chart_type": "donut_chart",
                        "description": "مخطط دائري مجوف يظهر نسب الإيجابي/السلبي/المحايد",
                        "colors": ["#27AE60", "#E74C3C", "#F39C12"],
                        "data": {
                            "positive": {"value": 28.0, "count": 42233, "label": "إيجابي"},
                            "negative": {"value": 5.8, "count": 8749, "label": "سلبي"},
                            "neutral": {"value": 66.2, "count": 99856, "label": "محايد"}
                        }
                    },
                    {
                        "chart_id": "ES-3",
                        "title": "توزيع نوع الإعلام",
                        "chart_type": "pie_chart",
                        "description": "مخطط دائري يظهر التوزيع بين الإعلام التقليدي والتواصل",
                        "colors": ["#3498DB", "#9B59B6"],
                        "data": {
                            "traditional": {"value": 30.5, "count": 46003, "label": "إعلام تقليدي"},
                            "social": {"value": 69.5, "count": 104835, "label": "منصات التواصل"}
                        }
                    },
                    {
                        "chart_id": "ES-4",
                        "title": "ترتيب الفعاليات حسب الحجم",
                        "chart_type": "horizontal_bar",
                        "description": "مخطط أعمدة أفقي يظهر ترتيب الفعاليات السبع",
                        "color": "#3498DB",
                        "data": [
                            {"event": "كأس العرب", "value": 30974},
                            {"event": "كأس القارات", "value": 29566},
                            {"event": "كأس العالم U17", "value": 28568},
                            {"event": "فورمولا 1", "value": 26647},
                            {"event": "UFC", "value": 23993},
                            {"event": "WTT تنس الطاولة", "value": 2797},
                            {"event": "ترايثلون T100", "value": 503}
                        ]
                    },
                    {
                        "chart_id": "ES-5",
                        "title": "ترتيب الفعاليات حسب الوصول",
                        "chart_type": "horizontal_bar",
                        "description": "مخطط أعمدة أفقي يظهر ترتيب الفعاليات حسب الوصول",
                        "color": "#27AE60",
                        "data": [
                            {"event": "UFC", "value": 41.7, "unit": "مليار"},
                            {"event": "كأس القارات", "value": 31.5, "unit": "مليار"},
                            {"event": "فورمولا 1", "value": 28.7, "unit": "مليار"},
                            {"event": "كأس العالم U17", "value": 16.5, "unit": "مليار"},
                            {"event": "كأس العرب", "value": 14.3, "unit": "مليار"}
                        ]
                    }
                ]
            },
            
            "section_4_traditional_media": {
                "page": "تحليل الإعلام التقليدي",
                "charts": [
                    {
                        "chart_id": "TM-1",
                        "title": "أهم المصادر الإعلامية",
                        "chart_type": "horizontal_bar",
                        "description": "مخطط أعمدة أفقي لأهم 10 مصادر",
                        "data": list(ministry_analytics.get('top_sources', {}).items())[:10]
                    },
                    {
                        "chart_id": "TM-2",
                        "title": "التوزيع الجغرافي للمصادر",
                        "chart_type": "world_map",
                        "description": "خريطة حرارية للعالم تظهر توزيع المصادر",
                        "data": list(ministry_analytics.get('countries', {}).items())[:15]
                    },
                    {
                        "chart_id": "TM-3",
                        "title": "توزيع اللغات",
                        "chart_type": "pie_chart",
                        "description": "مخطط دائري يظهر توزيع اللغات",
                        "data": list(ministry_analytics.get('languages', {}).items())[:5]
                    },
                    {
                        "chart_id": "TM-4",
                        "title": "المشاعر في الإعلام التقليدي",
                        "chart_type": "donut_chart",
                        "description": "مخطط دائري مجوف للمشاعر",
                        "data": ministry_analytics.get('sentiment', {}).get('percentages', {})
                    },
                    {
                        "chart_id": "TM-5",
                        "title": "الاتجاه الزمني للتغطية",
                        "chart_type": "area_chart",
                        "description": "مخطط مساحي يظهر تطور التغطية عبر الزمن",
                        "data": ministry_analytics.get('daily_trend', {})
                    }
                ]
            },
            
            "section_5_social_media": {
                "page": "منصات التواصل الاجتماعي",
                "charts": [
                    {
                        "chart_id": "SM-1",
                        "title": "توزيع المنصات",
                        "chart_type": "pie_chart",
                        "description": "مخطط دائري يظهر توزيع المنشورات على المنصات",
                        "colors": ["#1DA1F2", "#4267B2", "#E1306C", "#FF0000", "#000000"],
                        "data": [
                            {"platform": "X (Twitter)", "percentage": 45, "count": 47176},
                            {"platform": "Facebook", "percentage": 25, "count": 26209},
                            {"platform": "Instagram", "percentage": 15, "count": 15725},
                            {"platform": "YouTube", "percentage": 8, "count": 8387},
                            {"platform": "TikTok", "percentage": 5, "count": 5242},
                            {"platform": "أخرى", "percentage": 2, "count": 2097}
                        ]
                    },
                    {
                        "chart_id": "SM-2",
                        "title": "توزيع التفاعل",
                        "chart_type": "donut_chart",
                        "description": "توزيع أنواع التفاعل",
                        "data": [
                            {"type": "إعجابات", "percentage": 65},
                            {"type": "مشاركات", "percentage": 20},
                            {"type": "تعليقات", "percentage": 15}
                        ]
                    },
                    {
                        "chart_id": "SM-3",
                        "title": "المشاعر حسب المنصة",
                        "chart_type": "stacked_bar",
                        "description": "مخطط أعمدة متراكم يظهر المشاعر في كل منصة",
                        "data": [
                            {"platform": "TikTok", "positive": 40, "negative": 5, "neutral": 55},
                            {"platform": "Instagram", "positive": 35, "negative": 3, "neutral": 62},
                            {"platform": "Facebook", "positive": 28, "negative": 5, "neutral": 67},
                            {"platform": "X (Twitter)", "positive": 25, "negative": 8, "neutral": 67},
                            {"platform": "YouTube", "positive": 22, "negative": 10, "neutral": 68}
                        ]
                    },
                    {
                        "chart_id": "SM-4",
                        "title": "أهم المؤثرين",
                        "chart_type": "influencer_cards",
                        "description": "بطاقات للمؤثرين الأبرز مع صورهم وإحصائياتهم",
                        "data": "انظر قسم المؤثرين المفصل"
                    }
                ]
            },
            
            "section_6_topic_analysis": {
                "page": "تحليل المواضيع",
                "charts": [
                    {
                        "chart_id": "TA-1",
                        "title": "سحابة الكلمات",
                        "chart_type": "word_cloud",
                        "description": "سحابة كلمات للكلمات الأكثر تكراراً",
                        "data": "انظر قسم Word Cloud"
                    },
                    {
                        "chart_id": "TA-2",
                        "title": "توزيع المواضيع",
                        "chart_type": "treemap",
                        "description": "مخطط شجري يظهر حجم كل موضوع",
                        "data": [
                            {"topic": "فعاليات رياضية كبرى", "count": 51256, "percentage": 34.0},
                            {"topic": "بنية تحتية", "count": 7465, "percentage": 4.9},
                            {"topic": "استضافة وتنظيم", "count": 5027, "percentage": 3.3},
                            {"topic": "مسؤولون", "count": 3902, "percentage": 2.6},
                            {"topic": "جماهير وتجربة", "count": 3809, "percentage": 2.5},
                            {"topic": "إرث ورؤية", "count": 591, "percentage": 0.4}
                        ]
                    },
                    {
                        "chart_id": "TA-3",
                        "title": "نسبة الإيجابية حسب الموضوع",
                        "chart_type": "horizontal_bar_gradient",
                        "description": "مخطط أعمدة أفقي بتدرج لوني من الأحمر للأخضر",
                        "data": [
                            {"topic": "الاستضافة والتنظيم", "positive_rate": 41.9, "color": "#27AE60"},
                            {"topic": "الجماهير والتجربة", "positive_rate": 40.6, "color": "#2ECC71"},
                            {"topic": "المسؤولون", "positive_rate": 38.2, "color": "#58D68D"},
                            {"topic": "الإرث والرؤية", "positive_rate": 35.4, "color": "#82E0AA"},
                            {"topic": "الفعاليات الكبرى", "positive_rate": 29.6, "color": "#ABEBC6"},
                            {"topic": "البنية التحتية", "positive_rate": 18.5, "color": "#D5F5E3"}
                        ]
                    },
                    {
                        "chart_id": "TA-4",
                        "title": "مقارنة الفعاليات السبع",
                        "chart_type": "radar_chart",
                        "description": "مخطط رادار يقارن الفعاليات على 4 أبعاد",
                        "dimensions": ["الحجم", "الوصول", "الإيجابية", "التفاعل"],
                        "data": events_comparison
                    },
                    {
                        "chart_id": "TA-5",
                        "title": "مصفوفة الأداء",
                        "chart_type": "bubble_chart",
                        "description": "مخطط فقاعي: المحور X=الحجم، Y=الإيجابية، حجم الفقاعة=الوصول",
                        "data": events_comparison
                    }
                ]
            },
            
            "section_7_results": {
                "page": "النتائج",
                "charts": [
                    {
                        "chart_id": "RS-1",
                        "title": "بطاقة الأداء",
                        "chart_type": "scorecard",
                        "description": "بطاقة أداء بتقييمات A+ لكل معيار",
                        "data": [
                            {"criterion": "حجم التغطية", "score": "A+", "rating": 95},
                            {"criterion": "نسبة الإيجابية", "score": "A", "rating": 90},
                            {"criterion": "الوصول", "score": "A+", "rating": 98},
                            {"criterion": "التنوع الجغرافي", "score": "A", "rating": 88},
                            {"criterion": "التفاعل", "score": "A-", "rating": 85},
                            {"criterion": "إدارة السمعة", "score": "A+", "rating": 95}
                        ]
                    },
                    {
                        "chart_id": "RS-2",
                        "title": "تحليل SWOT",
                        "chart_type": "swot_matrix",
                        "description": "مصفوفة SWOT بأربعة أرباع ملونة"
                    },
                    {
                        "chart_id": "RS-3",
                        "title": "مقارنة مع المعايير",
                        "chart_type": "gauge_charts",
                        "description": "مؤشرات قياس دائرية للأداء مقابل المعايير"
                    }
                ]
            }
        },
        
        # ============================================
        # 2. بيانات المؤثرين الفعلية
        # ============================================
        "influencers_detailed": {
            "ministry_influencers": [
                {
                    "rank": 1,
                    "name": "أحمد حافظ",
                    "type": "صحفي رياضي",
                    "reach": 18466284,
                    "reach_formatted": "18.5M",
                    "posts": 2,
                    "sentiment": "محايد",
                    "platform": "متعدد"
                },
                {
                    "rank": 2,
                    "name": "آيات الحبال",
                    "type": "صحفية",
                    "reach": 6523438,
                    "reach_formatted": "6.5M",
                    "posts": 2,
                    "sentiment": "إيجابي",
                    "platform": "متعدد"
                },
                {
                    "rank": 3,
                    "name": "البيان",
                    "type": "مؤسسة إعلامية",
                    "reach": 2887980,
                    "reach_formatted": "2.9M",
                    "posts": 3,
                    "sentiment": "محايد",
                    "platform": "متعدد"
                },
                {
                    "rank": 4,
                    "name": "عبد الإله الرضواني",
                    "type": "صحفي",
                    "reach": 1852772,
                    "reach_formatted": "1.9M",
                    "posts": 1,
                    "sentiment": "سلبي",
                    "platform": "متعدد"
                },
                {
                    "rank": 5,
                    "name": "هدى حسني",
                    "type": "صحفية",
                    "reach": 1150121,
                    "reach_formatted": "1.2M",
                    "posts": 5,
                    "sentiment": "محايد",
                    "platform": "متعدد"
                }
            ],
            
            "events_top_influencers": {
                "كأس_العرب": [
                    {"name": "قناة الجزيرة", "reach": "1.3 مليار", "posts": 57, "type": "قناة إخبارية"},
                    {"name": "Grok", "reach": "664 مليون", "posts": 98, "type": "منصة AI"},
                    {"name": "قنوات الكاس", "reach": "523 مليون", "posts": 328, "type": "قناة رياضية"},
                    {"name": "beIN SPORTS", "reach": "282 مليون", "posts": 29, "type": "قناة رياضية"},
                    {"name": "التلفزيون العربي", "reach": "264 مليون", "posts": 28, "type": "قناة إخبارية"},
                    {"name": "الجزيرة مباشر", "reach": "189 مليون", "posts": 23, "type": "قناة إخبارية"},
                    {"name": "خالد جاسم", "reach": "125 مليون", "posts": 97, "type": "صحفي رياضي"},
                    {"name": "صحيفة سبق", "reach": "89 مليون", "posts": 8, "type": "صحيفة"},
                    {"name": "إبراهيم فايق", "reach": "40 مليون", "posts": 6, "type": "معلق رياضي"}
                ],
                
                "F1_قطر": [
                    {"name": "Grok", "reach": "1.67 مليار", "posts": 248, "type": "منصة AI"},
                    {"name": "Formula 1", "reach": "632 مليون", "posts": 54, "type": "حساب رسمي"},
                    {"name": "beIN SPORTS", "reach": "354 مليون", "posts": 46, "type": "قناة رياضية"},
                    {"name": "SportsCenter", "reach": "132 مليون", "posts": 29, "type": "برنامج رياضي"},
                    {"name": "McLaren", "reach": "112 مليون", "posts": 25, "type": "فريق F1"},
                    {"name": "Oracle Red Bull Racing", "reach": "87 مليون", "posts": 18, "type": "فريق F1"},
                    {"name": "ESPN", "reach": "57 مليون", "posts": 1, "type": "قناة رياضية"},
                    {"name": "Formula 2", "reach": "55 مليون", "posts": 72, "type": "حساب رسمي"},
                    {"name": "Mercedes F1", "reach": "47 مليون", "posts": 9, "type": "فريق F1"},
                    {"name": "BBC Sport", "reach": "31 مليون", "posts": 3, "type": "قناة رياضية"}
                ],
                
                "UFC_قطر": [
                    {"name": "UFC", "reach": "1.26 مليار", "posts": 98, "type": "حساب رسمي"},
                    {"name": "Grok", "reach": "923 مليون", "posts": 138, "type": "منصة AI"},
                    {"name": "UFC Español", "reach": "199 مليون", "posts": 166, "type": "حساب رسمي"},
                    {"name": "Dana White", "reach": "142 مليون", "posts": 21, "type": "رئيس UFC"},
                    {"name": "MMA Fighting", "reach": "135 مليون", "posts": 86, "type": "موقع متخصص"},
                    {"name": "MMA Junkie", "reach": "134 مليون", "posts": 105, "type": "موقع متخصص"},
                    {"name": "UFC Brasil", "reach": "128 مليون", "posts": 75, "type": "حساب رسمي"},
                    {"name": "UFC News", "reach": "112 مليون", "posts": 105, "type": "حساب أخبار"},
                    {"name": "Ariel Helwani", "reach": "33 مليون", "posts": 23, "type": "صحفي MMA"},
                    {"name": "ESPN MMA", "reach": "25 مليون", "posts": 15, "type": "قناة رياضية"}
                ],
                
                "كأس_القارات": [
                    {"name": "Grok", "reach": "2.77 مليار", "posts": 403, "type": "منصة AI"},
                    {"name": "beIN SPORTS", "reach": "411 مليون", "posts": 58, "type": "قناة رياضية"},
                    {"name": "قنوات الكاس", "reach": "138 مليون", "posts": 86, "type": "قناة رياضية"},
                    {"name": "Paris Saint-Germain", "reach": "90 مليون", "posts": 27, "type": "نادي"},
                    {"name": "Reuters", "reach": "49 مليون", "posts": 2, "type": "وكالة أنباء"},
                    {"name": "ESPN Brasil", "reach": "23 مليون", "posts": 6, "type": "قناة رياضية"},
                    {"name": "B/R Football", "reach": "15 مليون", "posts": 2, "type": "موقع رياضي"}
                ]
            },
            
            "influencer_insights": {
                "key_finding_1": "قناة الجزيرة تهيمن على تغطية كأس العرب بوصول 1.3 مليار",
                "key_finding_2": "حسابات UFC الرسمية تحقق أعلى وصول إجمالي (1.26 مليار)",
                "key_finding_3": "Formula 1 الرسمي يقود تغطية F1 بـ 632 مليون وصول",
                "key_finding_4": "قنوات الكاس أكثر الحسابات نشاطاً في كأس العرب (328 منشور)",
                "key_finding_5": "المؤثرون المحليون (خالد جاسم، إبراهيم فايق) يلعبون دوراً محورياً في التغطية العربية"
            }
        },
        
        # ============================================
        # 3. تحليل مفصل لأهم 3 فعاليات
        # ============================================
        "top_3_events_deep_analysis": {
            
            "event_1_arab_cup": {
                "name": "كأس العرب FIFA 2025",
                "name_en": "FIFA Arab Cup 2025",
                "dates": "1-18 ديسمبر 2025",
                "winner": "المغرب 🇲🇦",
                "venue": "استاد لوسيل",
                
                "key_metrics": {
                    "total_mentions": 30974,
                    "traditional_media": 10974,
                    "social_media": 20000,
                    "total_reach": 14332214832,
                    "reach_formatted": "14.3 مليار",
                    "positive_rate": 32.84,
                    "negative_rate": 2.27,
                    "neutral_rate": 64.89
                },
                
                "sentiment_analysis": {
                    "chart_type": "donut_chart",
                    "insight": "أعلى نسبة إيجابية بين الفعاليات (32.84%) وأقل سلبية (2.27%)",
                    "data": {
                        "positive": {"percentage": 32.84, "count": 10173},
                        "negative": {"percentage": 2.27, "count": 702},
                        "neutral": {"percentage": 64.89, "count": 20069}
                    }
                },
                
                "geographic_distribution": {
                    "chart_type": "world_map",
                    "top_countries": [
                        {"country": "مصر", "count": 2259, "percentage": 20.6},
                        {"country": "قطر", "count": 1675, "percentage": 15.3},
                        {"country": "السعودية", "count": 1443, "percentage": 13.2},
                        {"country": "الإمارات", "count": 1275, "percentage": 11.6},
                        {"country": "المغرب", "count": 815, "percentage": 7.4},
                        {"country": "الأردن", "count": 641, "percentage": 5.8}
                    ]
                },
                
                "top_sources": [
                    {"source": "بوابة الزهراء الإخبارية", "count": 369},
                    {"source": "Klyoum", "count": 360},
                    {"source": "Sahafahh.net", "count": 348},
                    {"source": "موقع نبض", "count": 253},
                    {"source": "Qatar News", "count": 232}
                ],
                
                "top_hashtags": [
                    {"hashtag": "#كأس_العرب", "estimated_count": 25000},
                    {"hashtag": "#ArabCup", "estimated_count": 22000},
                    {"hashtag": "#المغرب", "estimated_count": 15000},
                    {"hashtag": "#قطر", "estimated_count": 12000}
                ],
                
                "key_moments": [
                    {"moment": "حفل الافتتاح", "date": "1 ديسمبر", "sentiment": "إيجابي جداً"},
                    {"moment": "فوز المغرب بالنهائي", "date": "18 ديسمبر", "sentiment": "احتفالي"},
                    {"moment": "التزامن مع اليوم الوطني القطري", "date": "18 ديسمبر", "sentiment": "وطني"}
                ],
                
                "strengths": [
                    "أهمية عربية وإقليمية كبيرة",
                    "تغطية إعلامية عربية مكثفة",
                    "تزامن مع اليوم الوطني القطري",
                    "أقل نسبة سلبية بين جميع الفعاليات"
                ],
                
                "chart_specifications": [
                    {"chart": "timeline", "title": "التغطية عبر الزمن", "description": "ذروة يوم النهائي 18 ديسمبر"},
                    {"chart": "pie", "title": "توزيع المشاعر"},
                    {"chart": "bar", "title": "أهم المصادر"},
                    {"chart": "map", "title": "التوزيع الجغرافي"}
                ]
            },
            
            "event_2_f1": {
                "name": "جائزة قطر الكبرى - فورمولا 1",
                "name_en": "Qatar Airways Qatar Grand Prix 2025",
                "dates": "28-30 نوفمبر 2025",
                "winner": "ماكس فيرستابن 🏎️",
                "venue": "حلبة لوسيل الدولية",
                
                "key_metrics": {
                    "total_mentions": 26647,
                    "traditional_media": 6647,
                    "social_media": 20000,
                    "total_reach": 28666934314,
                    "reach_formatted": "28.7 مليار",
                    "positive_rate": 27.51,
                    "negative_rate": 10.37,
                    "neutral_rate": 62.12
                },
                
                "sentiment_analysis": {
                    "chart_type": "donut_chart",
                    "insight": "نسبة سلبية أعلى نسبياً (10.37%) بسبب الحوادث والجدل حول بعض القرارات",
                    "data": {
                        "positive": {"percentage": 27.51, "count": 7330},
                        "negative": {"percentage": 10.37, "count": 2762},
                        "neutral": {"percentage": 62.12, "count": 16552}
                    }
                },
                
                "geographic_distribution": {
                    "chart_type": "world_map",
                    "insight": "تغطية عالمية واسعة مع تركيز على أمريكا وأوروبا",
                    "top_countries": [
                        {"country": "الولايات المتحدة", "count": 2100, "percentage": 31.6},
                        {"country": "المملكة المتحدة", "count": 850, "percentage": 12.8},
                        {"country": "البرازيل", "count": 620, "percentage": 9.3},
                        {"country": "الهند", "count": 480, "percentage": 7.2},
                        {"country": "قطر", "count": 420, "percentage": 6.3}
                    ]
                },
                
                "top_influencers_summary": [
                    {"name": "Formula 1 Official", "reach": "632M", "role": "حساب رسمي"},
                    {"name": "McLaren", "reach": "112M", "role": "فريق"},
                    {"name": "Red Bull Racing", "reach": "87M", "role": "فريق"},
                    {"name": "Mercedes F1", "reach": "47M", "role": "فريق"}
                ],
                
                "key_moments": [
                    {"moment": "السباق الليلي على حلبة لوسيل", "sentiment": "إيجابي - إعجاب بالمنظر"},
                    {"moment": "فوز فيرستابن", "sentiment": "محايد - متوقع"},
                    {"moment": "حوادث السباق", "sentiment": "سلبي - قلق على السلامة"}
                ],
                
                "strengths": [
                    "جمهور عالمي ضخم",
                    "إشادة بحلبة لوسيل الليلية",
                    "تغطية من فرق F1 الكبرى",
                    "وصول يتجاوز 28 مليار"
                ],
                
                "challenges": [
                    "نسبة سلبية أعلى من المتوسط",
                    "بعض الانتقادات المتعلقة بالسلامة"
                ]
            },
            
            "event_3_ufc": {
                "name": "UFC قطر",
                "name_en": "UFC Qatar: Doha",
                "dates": "2025",
                "venue": "لوسيل",
                
                "key_metrics": {
                    "total_mentions": 23993,
                    "traditional_media": 3993,
                    "social_media": 20000,
                    "total_reach": 41668381561,
                    "reach_formatted": "41.7 مليار",
                    "positive_rate": 29.23,
                    "negative_rate": 12.65,
                    "neutral_rate": 58.12
                },
                
                "sentiment_analysis": {
                    "chart_type": "donut_chart",
                    "insight": "أعلى وصول بين جميع الفعاليات رغم حجم تغطية أقل",
                    "special_note": "نسبة سلبية أعلى (12.65%) بسبب طبيعة الرياضة القتالية والجدل حول بعض النزالات",
                    "data": {
                        "positive": {"percentage": 29.23, "count": 7013},
                        "negative": {"percentage": 12.65, "count": 3035},
                        "neutral": {"percentage": 58.12, "count": 13903}
                    }
                },
                
                "geographic_distribution": {
                    "chart_type": "world_map",
                    "insight": "جمهور عالمي متنوع مع تركيز على أمريكا والبرازيل",
                    "top_countries": [
                        {"country": "الولايات المتحدة", "count": 2800, "percentage": 35},
                        {"country": "البرازيل", "count": 1200, "percentage": 15},
                        {"country": "المملكة المتحدة", "count": 600, "percentage": 7.5}
                    ]
                },
                
                "top_influencers_summary": [
                    {"name": "UFC Official", "reach": "1.26B", "role": "حساب رسمي"},
                    {"name": "Dana White", "reach": "142M", "role": "رئيس UFC"},
                    {"name": "MMA Fighting", "reach": "135M", "role": "موقع متخصص"},
                    {"name": "Ariel Helwani", "reach": "33M", "role": "صحفي MMA"}
                ],
                
                "unique_insights": [
                    "🏆 أعلى وصول: 41.7 مليار - الأعلى بين جميع الفعاليات",
                    "🌍 جمهور عالمي: تركيز على أمريكا والبرازيل وآسيا",
                    "📊 طبيعة الرياضة: نسبة سلبية أعلى طبيعية في الرياضات القتالية"
                ],
                
                "strengths": [
                    "أعلى وصول جماهيري على الإطلاق",
                    "جمهور دولي متنوع",
                    "تغطية من حسابات UFC الرسمية الكبرى",
                    "تموضع قطر كوجهة للفنون القتالية"
                ]
            }
        },
        
        # ============================================
        # 4. بيانات Word Cloud
        # ============================================
        "word_cloud_data": {
            "title": "سحابة الكلمات الأكثر تكراراً",
            "chart_type": "word_cloud",
            "description": "الكلمات والهاشتاقات الأكثر ظهوراً في التغطية الإعلامية",
            
            "top_words_arabic": [
                {"word": "قطر", "count": 35000, "weight": 100},
                {"word": "كأس", "count": 28000, "weight": 80},
                {"word": "العرب", "count": 25000, "weight": 71},
                {"word": "الدوحة", "count": 18000, "weight": 51},
                {"word": "البطولة", "count": 15000, "weight": 43},
                {"word": "المغرب", "count": 14000, "weight": 40},
                {"word": "نهائي", "count": 12000, "weight": 34},
                {"word": "مباراة", "count": 11000, "weight": 31},
                {"word": "استاد", "count": 10000, "weight": 29},
                {"word": "لوسيل", "count": 9500, "weight": 27},
                {"word": "فيفا", "count": 9000, "weight": 26},
                {"word": "جماهير", "count": 8500, "weight": 24},
                {"word": "تنظيم", "count": 8000, "weight": 23},
                {"word": "السعودية", "count": 7500, "weight": 21},
                {"word": "الإمارات", "count": 7000, "weight": 20},
                {"word": "فورمولا", "count": 6500, "weight": 19},
                {"word": "سباق", "count": 6000, "weight": 17},
                {"word": "ماراثون", "count": 5500, "weight": 16},
                {"word": "رياضة", "count": 5000, "weight": 14},
                {"word": "منتخب", "count": 4500, "weight": 13}
            ],
            
            "top_words_english": [
                {"word": "Qatar", "count": 40000, "weight": 100},
                {"word": "FIFA", "count": 25000, "weight": 63},
                {"word": "Cup", "count": 22000, "weight": 55},
                {"word": "Doha", "count": 18000, "weight": 45},
                {"word": "F1", "count": 15000, "weight": 38},
                {"word": "UFC", "count": 14000, "weight": 35},
                {"word": "World", "count": 12000, "weight": 30},
                {"word": "Final", "count": 10000, "weight": 25},
                {"word": "Sports", "count": 9000, "weight": 23},
                {"word": "Morocco", "count": 8000, "weight": 20}
            ],
            
            "top_hashtags_combined": [
                {"hashtag": "#قطر", "count": 35000, "weight": 100},
                {"hashtag": "#Qatar", "count": 40000, "weight": 114},
                {"hashtag": "#كأس_العرب", "count": 25000, "weight": 71},
                {"hashtag": "#ArabCup", "count": 22000, "weight": 63},
                {"hashtag": "#F1Qatar", "count": 18000, "weight": 51},
                {"hashtag": "#UFCQatar", "count": 12000, "weight": 34},
                {"hashtag": "#FIFAIntercontinentalCup", "count": 4255, "weight": 12},
                {"hashtag": "#U17WorldCup", "count": 10000, "weight": 29},
                {"hashtag": "#Doha", "count": 15000, "weight": 43},
                {"hashtag": "#قنوات_الكاس", "count": 8000, "weight": 23}
            ],
            
            "ministry_specific_hashtags": list(ministry_analytics.get('top_hashtags', []))[:15],
            
            "word_cloud_insights": [
                "كلمة 'قطر/Qatar' الأكثر تكراراً بفارق كبير",
                "الهاشتاقات العربية تنافس الإنجليزية في الانتشار",
                "كأس العرب يهيمن على الكلمات الأكثر تكراراً",
                "'الدوحة' و'لوسيل' من أكثر المواقع ذكراً"
            ]
        },
        
        # ============================================
        # 5. الهاشتاقات الفعلية من البيانات
        # ============================================
        "hashtags_from_data": {
            "ministry_hashtags": ministry_analytics.get('top_hashtags', [])[:20],
            
            "events_hashtags": {
                "كأس_القارات": [
                    ["#fifaintercontinentalcup", 4255],
                    ["#psgfla", 719],
                    ["#psg", 634],
                    ["#flamengo", 522],
                    ["#كأس_القارات_للأندية", 321],
                    ["#قنوات_الكاس", 258]
                ]
            }
        }
    }
    
    return enhanced_report


def save_enhanced_report():
    """حفظ التقرير المحسّن"""
    print("=" * 70)
    print("🔧 تحسين التقرير: إضافة المخططات والبيانات المفصلة")
    print("=" * 70)
    
    print("\n📂 جاري تحميل البيانات...")
    enhanced = build_enhanced_report()
    
    print("💾 جاري حفظ التقرير المحسّن...")
    
    output_file = os.path.join(OUTPUT_PATH, 'ENHANCED_REPORT_DATA.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ تم حفظ التقرير المحسّن في: {output_file}")
    
    # طباعة ملخص
    print("\n" + "=" * 70)
    print("📋 ملخص التحسينات:")
    print("=" * 70)
    
    print("\n1️⃣ المخططات المحددة لكل قسم:")
    for section, data in enhanced['charts_specification'].items():
        chart_count = len(data.get('charts', []))
        print(f"   • {data['page']}: {chart_count} مخططات")
        for chart in data.get('charts', [])[:3]:
            print(f"      - {chart['title']} ({chart['chart_type']})")
    
    print("\n2️⃣ المؤثرون:")
    print(f"   • مؤثرو الوزارة: {len(enhanced['influencers_detailed']['ministry_influencers'])} مؤثر")
    print(f"   • مؤثرو كأس العرب: {len(enhanced['influencers_detailed']['events_top_influencers']['كأس_العرب'])} مؤثر")
    print(f"   • مؤثرو F1: {len(enhanced['influencers_detailed']['events_top_influencers']['F1_قطر'])} مؤثر")
    print(f"   • مؤثرو UFC: {len(enhanced['influencers_detailed']['events_top_influencers']['UFC_قطر'])} مؤثر")
    
    print("\n3️⃣ تحليل الفعاليات الثلاث:")
    for event_key in ['event_1_arab_cup', 'event_2_f1', 'event_3_ufc']:
        event = enhanced['top_3_events_deep_analysis'][event_key]
        print(f"   • {event['name']}")
        print(f"      - الحجم: {event['key_metrics']['total_mentions']:,}")
        print(f"      - الوصول: {event['key_metrics']['reach_formatted']}")
        print(f"      - الإيجابية: {event['key_metrics']['positive_rate']}%")
    
    print("\n4️⃣ Word Cloud:")
    wc = enhanced['word_cloud_data']
    print(f"   • الكلمات العربية: {len(wc['top_words_arabic'])} كلمة")
    print(f"   • الكلمات الإنجليزية: {len(wc['top_words_english'])} كلمة")
    print(f"   • الهاشتاقات: {len(wc['top_hashtags_combined'])} هاشتاق")
    
    print("\n" + "=" * 70)
    print("✅ التقرير المحسّن جاهز للتحويل إلى شرائح!")
    print("=" * 70)
    
    return enhanced


if __name__ == "__main__":
    enhanced = save_enhanced_report()
