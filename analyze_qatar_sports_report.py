"""
تحليل شامل لبيانات وزارة الرياضة والشباب القطرية
Qatar Ministry of Sports and Youth - Comprehensive Analysis Report
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from collections import Counter
import re
from pathlib import Path

# ============================================
# 1. إعدادات المسارات
# ============================================
BASE_PATH = "static/data/meltwater/qatr 4"
EVENTS_PATH = os.path.join(BASE_PATH, "الأحداث")
MINISTRY_PATH = os.path.join(BASE_PATH, "وزارة الرياضة والشباب")
OUTPUT_PATH = "static/data/qatar_sports_analysis"

# إنشاء مجلد المخرجات
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ============================================
# 2. قراءة البيانات
# ============================================
def read_csv_file(file_path):
    """قراءة ملف CSV مع معالجة الترميز"""
    encodings = ['utf-16', 'utf-8', 'utf-8-sig', 'latin-1', 'cp1256']
    separators = ['\t', ',', ';']
    
    for encoding in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep=sep, on_bad_lines='skip')
                if len(df.columns) > 5:
                    print(f"✅ تم قراءة: {os.path.basename(file_path)[:50]}... ({len(df)} صف)")
                    return df
            except:
                continue
    
    print(f"❌ فشل قراءة: {os.path.basename(file_path)[:50]}")
    return None

def load_all_data():
    """تحميل جميع البيانات من المجلدات"""
    all_data = {
        'ministry': {'analytics': None, 'x_insights': None},
        'events': {}
    }
    
    # تحميل بيانات الوزارة
    ministry_analytics = os.path.join(MINISTRY_PATH, "Analytics")
    ministry_x = os.path.join(MINISTRY_PATH, "X insights")
    
    if os.path.exists(ministry_analytics):
        for file in os.listdir(ministry_analytics):
            if file.endswith('.csv'):
                all_data['ministry']['analytics'] = read_csv_file(os.path.join(ministry_analytics, file))
                break
    
    if os.path.exists(ministry_x):
        for file in os.listdir(ministry_x):
            if file.endswith('.csv'):
                all_data['ministry']['x_insights'] = read_csv_file(os.path.join(ministry_x, file))
                break
    
    # تحميل بيانات الفعاليات
    if os.path.exists(EVENTS_PATH):
        for event_folder in os.listdir(EVENTS_PATH):
            if event_folder.startswith('.'):
                continue
            
            event_path = os.path.join(EVENTS_PATH, event_folder)
            if os.path.isdir(event_path):
                all_data['events'][event_folder] = {'analytics': None, 'x_insights': None}
                
                analytics_path = os.path.join(event_path, "Analytics")
                x_path = os.path.join(event_path, "X insights")
                
                if os.path.exists(analytics_path):
                    for file in os.listdir(analytics_path):
                        if file.endswith('.csv'):
                            all_data['events'][event_folder]['analytics'] = read_csv_file(os.path.join(analytics_path, file))
                            break
                
                if os.path.exists(x_path):
                    for file in os.listdir(x_path):
                        if file.endswith('.csv'):
                            all_data['events'][event_folder]['x_insights'] = read_csv_file(os.path.join(x_path, file))
                            break
    
    return all_data

# ============================================
# 3. تصنيف المحتوى
# ============================================
def classify_content(text):
    """تصنيف المحتوى حسب الموضوع"""
    if pd.isna(text):
        return "غير مصنف"
    
    text = str(text).lower()
    
    categories = {
        'استضافة وتنظيم': ['استضاف', 'تنظيم', 'hosting', 'organization', 'host', 'organize', 'يستضيف', 'تستضيف'],
        'بنية تحتية': ['ملعب', 'stadium', 'منشأة', 'facility', 'infrastructure', 'بنية', 'أسباير', 'aspire', 'لوسيل', 'lusail'],
        'مسؤولون': ['وزير', 'minister', 'شيخ', 'sheikh', 'رئيس', 'president', 'أمير', 'emir', 'الذوادي', 'thawadi', 'جوعان', 'joaan'],
        'فعاليات تراثية': ['هجن', 'camel', 'صقور', 'falcon', 'قناص', 'gannas', 'تراث', 'heritage', 'هذاب', 'hathab', 'سيلين', 'sealine'],
        'دوري وأندية': ['دوري', 'league', 'السد', 'sadd', 'الدحيل', 'duhail', 'الريان', 'rayyan', 'كأس الأمير', 'amir cup'],
        'منتخبات': ['منتخب', 'national team', 'المنتخب', 'العنابي'],
        'شباب ومبادرات': ['شباب', 'youth', 'مبادر', 'initiative', 'برنامج', 'program', 'تطوير', 'development'],
        'بطولات دولية': ['كأس العرب', 'arab cup', 'كأس العالم', 'world cup', 'فورمولا', 'formula', 'f1', 'ufc', 'ترايثلون', 'triathlon'],
        'إرث ورؤية': ['إرث', 'legacy', 'رؤية', 'vision', '2030', 'مستقبل', 'future'],
        'جماهير وتجربة': ['جماهير', 'fans', 'تجربة', 'experience', 'زوار', 'visitors', 'سياح', 'tourists']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category
    
    return "أخرى"

def classify_sentiment_arabic(sentiment):
    """تحويل المشاعر للعربية"""
    mapping = {
        'positive': 'إيجابي',
        'negative': 'سلبي',
        'neutral': 'محايد',
        'not rated': 'غير مصنف'
    }
    return mapping.get(str(sentiment).lower(), 'غير مصنف')

# ============================================
# 4. التحليل الرئيسي
# ============================================
def analyze_dataframe(df, name="البيانات"):
    """تحليل شامل لـ DataFrame"""
    if df is None or df.empty:
        return None
    
    analysis = {
        'name': name,
        'total_mentions': len(df),
        'date_range': {},
        'sentiment': {},
        'source_types': {},
        'languages': {},
        'countries': {},
        'top_sources': {},
        'categories': {},
        'reach': {},
        'engagement': {},
        'daily_trend': {},
        'weekly_trend': {},
        'top_authors': {},
        'top_hashtags': [],
        'sample_positive': [],
        'sample_negative': [],
        'sample_neutral': []
    }
    
    # نطاق التاريخ
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        valid_dates = df['Date'].dropna()
        if len(valid_dates) > 0:
            analysis['date_range'] = {
                'start': str(valid_dates.min().date()),
                'end': str(valid_dates.max().date()),
                'days': (valid_dates.max() - valid_dates.min()).days
            }
            
            # الاتجاه اليومي
            daily = df.groupby(df['Date'].dt.date).size()
            analysis['daily_trend'] = {str(k): int(v) for k, v in daily.items()}
            
            # الاتجاه الأسبوعي
            df['Week'] = df['Date'].dt.isocalendar().week
            weekly = df.groupby('Week').size()
            analysis['weekly_trend'] = {f"Week_{int(k)}": int(v) for k, v in weekly.items()}
    
    # تحليل المشاعر
    if 'Sentiment' in df.columns:
        sentiment_counts = df['Sentiment'].value_counts()
        total = len(df)
        analysis['sentiment'] = {
            'counts': {str(k): int(v) for k, v in sentiment_counts.items()},
            'percentages': {str(k): round(v/total*100, 2) for k, v in sentiment_counts.items()}
        }
    
    # أنواع المصادر
    if 'Source Type' in df.columns:
        source_types = df['Source Type'].value_counts()
        analysis['source_types'] = {str(k): int(v) for k, v in source_types.items()}
    
    # اللغات
    if 'Language' in df.columns:
        languages = df['Language'].value_counts().head(10)
        analysis['languages'] = {str(k): int(v) for k, v in languages.items()}
    
    # الدول
    if 'Country' in df.columns:
        countries = df['Country'].value_counts().head(15)
        analysis['countries'] = {str(k): int(v) for k, v in countries.items()}
    
    # أبرز المصادر
    if 'Source Name' in df.columns:
        sources = df['Source Name'].value_counts().head(20)
        analysis['top_sources'] = {str(k): int(v) for k, v in sources.items()}
    
    # الوصول
    if 'Reach' in df.columns:
        df['Reach'] = pd.to_numeric(df['Reach'], errors='coerce')
        reach_sum = df['Reach'].sum()
        reach_mean = df['Reach'].mean()
        reach_max = df['Reach'].max()
        analysis['reach'] = {
            'total': int(reach_sum) if pd.notna(reach_sum) else 0,
            'average': int(reach_mean) if pd.notna(reach_mean) else 0,
            'max': int(reach_max) if pd.notna(reach_max) else 0
        }
    
    # التفاعل
    if 'Engagement' in df.columns:
        df['Engagement'] = pd.to_numeric(df['Engagement'], errors='coerce')
        eng_sum = df['Engagement'].sum()
        eng_mean = df['Engagement'].mean()
        analysis['engagement'] = {
            'total': int(eng_sum) if pd.notna(eng_sum) else 0,
            'average': int(eng_mean) if pd.notna(eng_mean) else 0
        }
    
    # تصنيف المحتوى
    text_col = None
    if 'Opening Text' in df.columns:
        text_col = 'Opening Text'
    elif 'Hit Sentence' in df.columns:
        text_col = 'Hit Sentence'
    
    if text_col:
        df['Category'] = df[text_col].apply(classify_content)
        categories = df['Category'].value_counts()
        analysis['categories'] = {str(k): int(v) for k, v in categories.items()}
    
    # أبرز المؤلفين
    if 'Author Name' in df.columns:
        authors = df['Author Name'].value_counts().head(15)
        analysis['top_authors'] = {str(k): int(v) for k, v in authors.items()}
    
    # الهاشتاقات
    if 'Hashtags' in df.columns:
        all_hashtags = []
        for tags in df['Hashtags'].dropna():
            if isinstance(tags, str):
                all_hashtags.extend([t.strip() for t in tags.split(';') if t.strip()])
        hashtag_counts = Counter(all_hashtags).most_common(20)
        analysis['top_hashtags'] = [[str(h), int(c)] for h, c in hashtag_counts]
    
    # عينات من المحتوى حسب المشاعر
    if 'Sentiment' in df.columns and text_col:
        for sent_type, sent_key in [('positive', 'sample_positive'), ('negative', 'sample_negative'), ('neutral', 'sample_neutral')]:
            samples = df[df['Sentiment'].str.lower() == sent_type].head(5)
            if len(samples) > 0:
                for _, row in samples.iterrows():
                    sample = {
                        'date': str(row.get('Date', ''))[:10],
                        'source': str(row.get('Source Name', '')),
                        'text': str(row.get(text_col, ''))[:300],
                        'reach': int(row.get('Reach', 0)) if pd.notna(row.get('Reach')) else 0
                    }
                    analysis[sent_key].append(sample)
    
    return analysis

# ============================================
# 5. تحليل المقارنة بين الفعاليات
# ============================================
def compare_events(all_data):
    """مقارنة الفعاليات المختلفة"""
    comparison = []
    
    for event_name, event_data in all_data['events'].items():
        analytics = event_data.get('analytics')
        x_insights = event_data.get('x_insights')
        
        event_stats = {
            'event': event_name,
            'traditional_media': len(analytics) if analytics is not None else 0,
            'social_media': len(x_insights) if x_insights is not None else 0,
            'total': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'positive_rate': 0,
            'negative_rate': 0,
            'reach': 0
        }
        
        # دمج البيانات للتحليل
        dfs = []
        if analytics is not None:
            dfs.append(analytics)
        if x_insights is not None:
            dfs.append(x_insights)
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            event_stats['total'] = len(combined)
            
            if 'Sentiment' in combined.columns:
                sent_lower = combined['Sentiment'].str.lower()
                event_stats['positive_count'] = int((sent_lower == 'positive').sum())
                event_stats['negative_count'] = int((sent_lower == 'negative').sum())
                event_stats['neutral_count'] = int((sent_lower == 'neutral').sum())
                
                if len(combined) > 0:
                    event_stats['positive_rate'] = round(event_stats['positive_count'] / len(combined) * 100, 2)
                    event_stats['negative_rate'] = round(event_stats['negative_count'] / len(combined) * 100, 2)
            
            if 'Reach' in combined.columns:
                combined['Reach'] = pd.to_numeric(combined['Reach'], errors='coerce')
                reach_sum = combined['Reach'].sum()
                event_stats['reach'] = int(reach_sum) if pd.notna(reach_sum) else 0
        
        comparison.append(event_stats)
    
    return pd.DataFrame(comparison)

# ============================================
# 6. تحليل المؤثرين
# ============================================
def analyze_influencers(df, name=""):
    """تحليل المؤثرين والحسابات البارزة"""
    if df is None or df.empty:
        return []
    
    influencers = []
    
    if 'Author Name' in df.columns and 'Reach' in df.columns:
        df = df.copy()
        df['Reach'] = pd.to_numeric(df['Reach'], errors='coerce')
        
        author_stats = df.groupby('Author Name').agg({
            'Reach': 'sum',
            'Document ID': 'count'
        }).reset_index()
        
        author_stats.columns = ['author', 'total_reach', 'posts_count']
        author_stats = author_stats.sort_values('total_reach', ascending=False).head(20)
        
        for idx, row in author_stats.iterrows():
            author_df = df[df['Author Name'] == row['author']]
            dominant_sentiment = 'neutral'
            if 'Sentiment' in author_df.columns and len(author_df) > 0:
                mode = author_df['Sentiment'].mode()
                if len(mode) > 0:
                    dominant_sentiment = str(mode.iloc[0])
            
            influencers.append({
                'author': str(row['author']),
                'total_reach': int(row['total_reach']) if pd.notna(row['total_reach']) else 0,
                'posts_count': int(row['posts_count']),
                'dominant_sentiment': dominant_sentiment
            })
    
    return influencers

# ============================================
# 7. إنشاء الملخص التنفيذي
# ============================================
def generate_executive_summary(all_data, all_analysis):
    """إنشاء الملخص التنفيذي"""
    summary = {
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'period': 'نوفمبر 2025 - يناير 2026 (90 يوم)',
        'total_mentions': 0,
        'traditional_media': 0,
        'social_media': 0,
        'events_covered': len(all_data['events']),
        'overall_sentiment': {},
        'sentiment_counts': {},
        'key_metrics': {},
        'top_events_by_volume': [],
        'top_events_by_reach': [],
        'reach_total': 0,
        'engagement_total': 0
    }
    
    all_sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    total_reach = 0
    total_engagement = 0
    
    # حساب الإجماليات من الفعاليات
    event_volumes = []
    event_reaches = []
    
    for event_name, event_data in all_data['events'].items():
        event_total = 0
        event_reach = 0
        
        if event_data.get('analytics') is not None:
            df = event_data['analytics']
            summary['traditional_media'] += len(df)
            event_total += len(df)
            
            if 'Sentiment' in df.columns:
                for sent in df['Sentiment'].str.lower():
                    if sent == 'positive':
                        all_sentiments['positive'] += 1
                    elif sent == 'negative':
                        all_sentiments['negative'] += 1
                    else:
                        all_sentiments['neutral'] += 1
            
            if 'Reach' in df.columns:
                df['Reach'] = pd.to_numeric(df['Reach'], errors='coerce')
                reach = df['Reach'].sum()
                if pd.notna(reach):
                    total_reach += reach
                    event_reach += reach
            
            if 'Engagement' in df.columns:
                df['Engagement'] = pd.to_numeric(df['Engagement'], errors='coerce')
                eng = df['Engagement'].sum()
                if pd.notna(eng):
                    total_engagement += eng
        
        if event_data.get('x_insights') is not None:
            df = event_data['x_insights']
            summary['social_media'] += len(df)
            event_total += len(df)
            
            if 'Sentiment' in df.columns:
                for sent in df['Sentiment'].str.lower():
                    if sent == 'positive':
                        all_sentiments['positive'] += 1
                    elif sent == 'negative':
                        all_sentiments['negative'] += 1
                    else:
                        all_sentiments['neutral'] += 1
            
            if 'Reach' in df.columns:
                df['Reach'] = pd.to_numeric(df['Reach'], errors='coerce')
                reach = df['Reach'].sum()
                if pd.notna(reach):
                    total_reach += reach
                    event_reach += reach
            
            if 'Engagement' in df.columns:
                df['Engagement'] = pd.to_numeric(df['Engagement'], errors='coerce')
                eng = df['Engagement'].sum()
                if pd.notna(eng):
                    total_engagement += eng
        
        event_volumes.append({'event': event_name, 'volume': event_total})
        event_reaches.append({'event': event_name, 'reach': int(event_reach)})
    
    # بيانات الوزارة
    if all_data['ministry']['analytics'] is not None:
        df = all_data['ministry']['analytics']
        summary['traditional_media'] += len(df)
        
        if 'Sentiment' in df.columns:
            for sent in df['Sentiment'].str.lower():
                if sent == 'positive':
                    all_sentiments['positive'] += 1
                elif sent == 'negative':
                    all_sentiments['negative'] += 1
                else:
                    all_sentiments['neutral'] += 1
    
    if all_data['ministry']['x_insights'] is not None:
        df = all_data['ministry']['x_insights']
        summary['social_media'] += len(df)
        
        if 'Sentiment' in df.columns:
            for sent in df['Sentiment'].str.lower():
                if sent == 'positive':
                    all_sentiments['positive'] += 1
                elif sent == 'negative':
                    all_sentiments['negative'] += 1
                else:
                    all_sentiments['neutral'] += 1
    
    summary['total_mentions'] = summary['traditional_media'] + summary['social_media']
    summary['reach_total'] = int(total_reach)
    summary['engagement_total'] = int(total_engagement)
    
    # حساب نسب المشاعر
    total_sent = sum(all_sentiments.values())
    if total_sent > 0:
        summary['sentiment_counts'] = all_sentiments
        summary['overall_sentiment'] = {
            'إيجابي': f"{round(all_sentiments['positive']/total_sent*100, 1)}%",
            'سلبي': f"{round(all_sentiments['negative']/total_sent*100, 1)}%",
            'محايد': f"{round(all_sentiments['neutral']/total_sent*100, 1)}%"
        }
    
    # ترتيب الفعاليات
    summary['top_events_by_volume'] = sorted(event_volumes, key=lambda x: x['volume'], reverse=True)[:5]
    summary['top_events_by_reach'] = sorted(event_reaches, key=lambda x: x['reach'], reverse=True)[:5]
    
    # مؤشرات رئيسية
    summary['key_metrics'] = {
        'total_materials': summary['total_mentions'],
        'traditional_percentage': round(summary['traditional_media'] / summary['total_mentions'] * 100, 1) if summary['total_mentions'] > 0 else 0,
        'social_percentage': round(summary['social_media'] / summary['total_mentions'] * 100, 1) if summary['total_mentions'] > 0 else 0,
        'positive_percentage': round(all_sentiments['positive'] / total_sent * 100, 1) if total_sent > 0 else 0,
        'negative_percentage': round(all_sentiments['negative'] / total_sent * 100, 1) if total_sent > 0 else 0,
        'reach_total': summary['reach_total'],
        'engagement_total': summary['engagement_total']
    }
    
    return summary

# ============================================
# 8. تحليل المواضيع التفصيلي
# ============================================
def analyze_topics(all_data):
    """تحليل المواضيع بالتفصيل"""
    topics = {
        'فعاليات_رياضية_كبرى': [],
        'بنية_تحتية': [],
        'مسؤولون': [],
        'استضافة_وتنظيم': [],
        'جماهير_وتجربة': [],
        'إرث_ورؤية': []
    }
    
    # تجميع كل البيانات
    all_texts = []
    
    for event_name, event_data in all_data['events'].items():
        for data_type in ['analytics', 'x_insights']:
            df = event_data.get(data_type)
            if df is not None and len(df) > 0:
                text_col = 'Opening Text' if 'Opening Text' in df.columns else 'Hit Sentence'
                if text_col in df.columns:
                    for _, row in df.iterrows():
                        text = str(row.get(text_col, ''))
                        sentiment = str(row.get('Sentiment', 'neutral'))
                        reach = row.get('Reach', 0)
                        all_texts.append({
                            'text': text,
                            'event': event_name,
                            'sentiment': sentiment,
                            'reach': reach,
                            'category': classify_content(text)
                        })
    
    # تصنيف حسب الموضوع
    for item in all_texts:
        cat = item['category']
        if 'بطولات' in cat or 'فعاليات' in cat:
            topics['فعاليات_رياضية_كبرى'].append(item)
        elif 'بنية' in cat:
            topics['بنية_تحتية'].append(item)
        elif 'مسؤول' in cat:
            topics['مسؤولون'].append(item)
        elif 'استضافة' in cat:
            topics['استضافة_وتنظيم'].append(item)
        elif 'جماهير' in cat:
            topics['جماهير_وتجربة'].append(item)
        elif 'إرث' in cat:
            topics['إرث_ورؤية'].append(item)
    
    # إحصائيات كل موضوع
    topic_stats = {}
    for topic_name, items in topics.items():
        if len(items) > 0:
            positive = sum(1 for i in items if 'positive' in str(i['sentiment']).lower())
            negative = sum(1 for i in items if 'negative' in str(i['sentiment']).lower())
            topic_stats[topic_name] = {
                'count': len(items),
                'positive': positive,
                'negative': negative,
                'neutral': len(items) - positive - negative,
                'positive_rate': round(positive / len(items) * 100, 1)
            }
    
    return topic_stats

# ============================================
# 9. إنشاء التقرير النهائي
# ============================================
def generate_full_report():
    """إنشاء التقرير الكامل"""
    print("=" * 60)
    print("🇶🇦 تحليل بيانات وزارة الرياضة والشباب القطرية")
    print("   Qatar Ministry of Sports & Youth Analysis")
    print("=" * 60)
    
    # تحميل البيانات
    print("\n📂 جاري تحميل البيانات...")
    all_data = load_all_data()
    
    # تحليل البيانات
    print("\n📊 جاري التحليل...")
    all_analysis = {}
    
    # تحليل الوزارة
    print("\n🏛️ تحليل بيانات الوزارة...")
    if all_data['ministry']['analytics'] is not None:
        all_analysis['ministry_analytics'] = analyze_dataframe(
            all_data['ministry']['analytics'], 
            "وزارة الرياضة والشباب - الإعلام التقليدي"
        )
    
    if all_data['ministry']['x_insights'] is not None:
        all_analysis['ministry_social'] = analyze_dataframe(
            all_data['ministry']['x_insights'],
            "وزارة الرياضة والشباب - منصات التواصل"
        )
    
    # تحليل الفعاليات
    print("\n🏆 تحليل بيانات الفعاليات...")
    for event_name, event_data in all_data['events'].items():
        print(f"   📌 {event_name}")
        if event_data.get('analytics') is not None:
            all_analysis[f"{event_name}_analytics"] = analyze_dataframe(
                event_data['analytics'],
                f"{event_name} - الإعلام التقليدي"
            )
        if event_data.get('x_insights') is not None:
            all_analysis[f"{event_name}_social"] = analyze_dataframe(
                event_data['x_insights'],
                f"{event_name} - منصات التواصل"
            )
    
    # مقارنة الفعاليات
    print("\n📈 جاري مقارنة الفعاليات...")
    events_comparison = compare_events(all_data)
    
    # تحليل المؤثرين
    print("\n👥 جاري تحليل المؤثرين...")
    all_influencers = {}
    
    # مؤثرين الوزارة
    if all_data['ministry']['x_insights'] is not None:
        all_influencers['ministry'] = analyze_influencers(all_data['ministry']['x_insights'], "الوزارة")
    
    # مؤثرين الفعاليات
    for key, data in all_data['events'].items():
        if data.get('x_insights') is not None:
            all_influencers[key] = analyze_influencers(data['x_insights'], key)
    
    # تحليل المواضيع
    print("\n📑 جاري تحليل المواضيع...")
    topic_analysis = analyze_topics(all_data)
    
    # الملخص التنفيذي
    print("\n📋 جاري إنشاء الملخص التنفيذي...")
    executive_summary = generate_executive_summary(all_data, all_analysis)
    
    # حفظ النتائج
    print("\n💾 جاري حفظ النتائج...")
    
    # حفظ التحليل الكامل
    with open(os.path.join(OUTPUT_PATH, 'full_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(all_analysis, f, ensure_ascii=False, indent=2, default=str)
    
    # حفظ الملخص التنفيذي
    with open(os.path.join(OUTPUT_PATH, 'executive_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(executive_summary, f, ensure_ascii=False, indent=2)
    
    # حفظ مقارنة الفعاليات
    events_comparison.to_csv(os.path.join(OUTPUT_PATH, 'events_comparison.csv'), index=False, encoding='utf-8-sig')
    events_comparison.to_json(os.path.join(OUTPUT_PATH, 'events_comparison.json'), orient='records', force_ascii=False, indent=2)
    
    # حفظ المؤثرين
    with open(os.path.join(OUTPUT_PATH, 'influencers.json'), 'w', encoding='utf-8') as f:
        json.dump(all_influencers, f, ensure_ascii=False, indent=2)
    
    # حفظ تحليل المواضيع
    with open(os.path.join(OUTPUT_PATH, 'topic_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(topic_analysis, f, ensure_ascii=False, indent=2)
    
    # طباعة الملخص
    print("\n" + "=" * 60)
    print("📊 الملخص التنفيذي")
    print("=" * 60)
    print(f"📅 الفترة: {executive_summary['period']}")
    print(f"📰 إجمالي المواد: {executive_summary['total_mentions']:,}")
    print(f"   ├── الإعلام التقليدي: {executive_summary['traditional_media']:,}")
    print(f"   └── منصات التواصل: {executive_summary['social_media']:,}")
    print(f"🏆 الفعاليات المغطاة: {executive_summary['events_covered']}")
    print(f"📣 إجمالي الوصول: {executive_summary['reach_total']:,}")
    
    print(f"\n💚 المشاعر الإجمالية:")
    for sent, pct in executive_summary['overall_sentiment'].items():
        emoji = "💚" if "إيجابي" in sent else ("❤️" if "سلبي" in sent else "💛")
        print(f"   {emoji} {sent}: {pct}")
    
    print("\n" + "-" * 60)
    print("📈 ترتيب الفعاليات حسب الحجم:")
    for i, evt in enumerate(executive_summary['top_events_by_volume'], 1):
        print(f"   {i}. {evt['event']}: {evt['volume']:,}")
    
    print("\n" + "-" * 60)
    print("📊 تحليل المواضيع:")
    for topic, stats in topic_analysis.items():
        print(f"   📌 {topic}: {stats['count']} مادة ({stats['positive_rate']}% إيجابي)")
    
    print("\n" + "=" * 60)
    print(f"✅ تم حفظ النتائج في: {OUTPUT_PATH}/")
    print("   ├── full_analysis.json")
    print("   ├── executive_summary.json")
    print("   ├── events_comparison.csv")
    print("   ├── events_comparison.json")
    print("   ├── influencers.json")
    print("   └── topic_analysis.json")
    print("=" * 60)
    
    return {
        'all_analysis': all_analysis,
        'executive_summary': executive_summary,
        'events_comparison': events_comparison,
        'influencers': all_influencers,
        'topic_analysis': topic_analysis
    }

# ============================================
# 10. تشغيل التحليل
# ============================================
if __name__ == "__main__":
    results = generate_full_report()
