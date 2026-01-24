#!/usr/bin/env python3
"""
تحليل بيانات Meltwater من مجلد qatr3
مع تصنيف البيانات حسب:
1. الوزارة (Ministry)
2. الفعاليات العالمية (Global Events)
مع استبعاد الأنشطة التراثية والمحلية
"""

import os
import pandas as pd
import json
from collections import defaultdict
from datetime import datetime

# المسارات
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr3"
OUTPUT_FILE = "/Users/taherirshaid/Desktop/Project/24-45-Platform/qatr3_final_analysis.json"

# كلمات مفتاحية للوزارة
MINISTRY_KEYWORDS = [
    "وزارة الرياضة والشباب",
    "وزارة الرياضة",
    "سعادة الوزير",
    "وكيل الوزارة",
    "قرار وزاري",
    "قرار",
    "اتفاقية",
    "MSY",
    "Ministry of Sports",
    "Minister of Sports",
    "صالح الحمد الملا",
    "الشيخ حمد بن خليفة"
]

# كلمات مفتاحية للفعاليات العالمية
GLOBAL_EVENTS_KEYWORDS = [
    "كأس العرب",
    "مونديال العرب",
    "كأس القارات",
    "فورمولا 1",
    "فورمولا واحد",
    "Formula 1",
    "F1",
    "بادل",
    "Padel",
    "UFC",
    "يو اف سي",
    "FIFA",
    "فيفا",
    "كأس العالم",
    "مونديال قطر",
    "الدوري العالمي",
    "جراند بري",
    "Grand Prix"
]

# كلمات للاستبعاد (الأنشطة التراثية والمحلية)
EXCLUSION_KEYWORDS = [
    "مرمي",
    "القلايل",
    "الرياضة للجميع",
    "رياضة للجميع",
    "مهرجان تراثي",
    "الألعاب الشعبية",
    "الصيد بالصقور"
]

def read_csv_file(filepath):
    """قراءة ملف CSV بترميز UTF-16 LE"""
    try:
        df = pd.read_csv(filepath, encoding='utf-16-le', sep='\t', on_bad_lines='skip')
        return df
    except Exception as e:
        print(f"خطأ في قراءة {filepath}: {e}")
        return pd.DataFrame()

def should_exclude(text):
    """التحقق إذا كان النص يجب استبعاده"""
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    for keyword in EXCLUSION_KEYWORDS:
        if keyword.lower() in text_lower:
            return True
    return False

def classify_record(row):
    """تصنيف السجل: ministry, global_events, أو excluded"""
    # دمج الحقول النصية للبحث
    text_fields = []
    for col in ['Title', 'Headline', 'Key Phrases', 'Opening Text', 'Hit Sentence']:
        if col in row.index and pd.notna(row[col]):
            text_fields.append(str(row[col]))
    combined_text = ' '.join(text_fields).lower()
    
    # التحقق من الاستبعاد أولاً
    if should_exclude(combined_text):
        return 'excluded'
    
    # تحديد نوع المحتوى
    is_ministry = any(kw.lower() in combined_text for kw in MINISTRY_KEYWORDS)
    is_global = any(kw.lower() in combined_text for kw in GLOBAL_EVENTS_KEYWORDS)
    
    if is_global:
        return 'global_events'
    elif is_ministry:
        return 'ministry'
    else:
        return 'other'

def analyze_data():
    """تحليل البيانات من المجلدين"""
    results = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_folder': 'qatr3',
        'tracks': {},
        'totals': {},
        'sentiment_distribution': {},
        'source_distribution': {},
        'top_influencers': [],
        'top_hashtags': [],
        'excluded_count': 0
    }
    
    all_records = []
    
    # قراءة بيانات الفعاليات العالمية - Analytics
    global_folder = os.path.join(BASE_PATH, "الأحاث العالمية ")
    if os.path.exists(global_folder):
        analytics_folder = os.path.join(global_folder, "Analytics")
        if os.path.exists(analytics_folder):
            for file in os.listdir(analytics_folder):
                if file.endswith('.csv'):
                    filepath = os.path.join(analytics_folder, file)
                    df = read_csv_file(filepath)
                    if not df.empty:
                        df['source_track'] = 'global_events'
                        df['media_category'] = 'traditional'
                        all_records.append(df)
                        print(f"✓ قراءة {len(df)} سجل من الفعاليات العالمية (Analytics)")
        
        # قراءة X insights للفعاليات العالمية
        x_folder = os.path.join(global_folder, "X insights")
        if os.path.exists(x_folder):
            for file in os.listdir(x_folder):
                if file.endswith('.csv') and 'Sentiment' not in file:
                    filepath = os.path.join(x_folder, file)
                    df = read_csv_file(filepath)
                    if not df.empty:
                        df['source_track'] = 'global_events'
                        df['media_category'] = 'social'
                        all_records.append(df)
                        print(f"✓ قراءة {len(df)} سجل من الفعاليات العالمية (X Platform)")
    
    # قراءة بيانات الوزارة - Analytics
    ministry_folder = os.path.join(BASE_PATH, "وزارة الرياضة والشباب القطرية")
    if os.path.exists(ministry_folder):
        analytics_folder = os.path.join(ministry_folder, "Analytics")
        if os.path.exists(analytics_folder):
            for file in os.listdir(analytics_folder):
                if file.endswith('.csv'):
                    filepath = os.path.join(analytics_folder, file)
                    df = read_csv_file(filepath)
                    if not df.empty:
                        df['source_track'] = 'ministry'
                        df['media_category'] = 'traditional'
                        all_records.append(df)
                        print(f"✓ قراءة {len(df)} سجل من الوزارة (Analytics)")
        
        # قراءة X insights للوزارة
        x_folder = os.path.join(ministry_folder, "X insights")
        if os.path.exists(x_folder):
            for file in os.listdir(x_folder):
                if file.endswith('.csv') and 'Sentiment' not in file:
                    filepath = os.path.join(x_folder, file)
                    df = read_csv_file(filepath)
                    if not df.empty:
                        df['source_track'] = 'ministry'
                        df['media_category'] = 'social'
                        all_records.append(df)
                        print(f"✓ قراءة {len(df)} سجل من الوزارة (X Platform)")
    
    if not all_records:
        print("❌ لم يتم العثور على بيانات")
        return results
    
    # دمج جميع السجلات
    combined_df = pd.concat(all_records, ignore_index=True)
    print(f"\n📊 إجمالي السجلات المقروءة: {len(combined_df)}")
    
    # إزالة التكرارات بناءً على Document ID
    if 'Document ID' in combined_df.columns:
        original_count = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['Document ID'], keep='first')
        print(f"✓ إزالة {original_count - len(combined_df)} سجل مكرر")
    
    # تطبيق الفلترة والاستبعاد
    filtered_records = []
    excluded_count = 0
    
    for _, row in combined_df.iterrows():
        classification = classify_record(row)
        if classification == 'excluded':
            excluded_count += 1
        elif classification in ['ministry', 'global_events']:
            row_dict = row.to_dict()
            row_dict['classification'] = classification
            filtered_records.append(row_dict)
    
    results['excluded_count'] = excluded_count
    print(f"✓ تم استبعاد {excluded_count} سجل (أنشطة تراثية/محلية)")
    
    # تحويل إلى DataFrame
    if filtered_records:
        df = pd.DataFrame(filtered_records)
    else:
        df = combined_df.copy()
        df['classification'] = df.apply(lambda x: classify_record(x), axis=1)
        df = df[df['classification'].isin(['ministry', 'global_events'])]
    
    print(f"📊 السجلات بعد الفلترة: {len(df)}")
    
    # تحليل حسب التصنيف
    tracks_analysis = {
        'ministry': {'count': 0, 'reach': 0, 'engagement': 0, 'sentiment': {}, 'sources': {}},
        'global_events': {'count': 0, 'reach': 0, 'engagement': 0, 'sentiment': {}, 'sources': {}}
    }
    
    # تحديد أعمدة المصادر
    source_col = None
    for col in ['Media Type', 'Source Type', 'Type']:
        if col in df.columns:
            source_col = col
            break
    
    sentiment_col = None
    for col in ['Sentiment', 'Sentiment Score']:
        if col in df.columns:
            sentiment_col = col
            break
    
    reach_col = None
    for col in ['Reach', 'Estimated Reach', 'Potential Reach']:
        if col in df.columns:
            reach_col = col
            break
    
    engagement_col = None
    for col in ['Engagement', 'Total Engagement', 'Interactions']:
        if col in df.columns:
            engagement_col = col
            break
    
    # حساب الإحصائيات لكل تصنيف
    for classification in ['ministry', 'global_events']:
        subset = df[df['classification'] == classification] if 'classification' in df.columns else df[df['source_track'] == classification]
        
        tracks_analysis[classification]['count'] = len(subset)
        
        # الوصول
        if reach_col and reach_col in subset.columns:
            tracks_analysis[classification]['reach'] = int(pd.to_numeric(subset[reach_col], errors='coerce').fillna(0).sum())
        
        # التفاعل
        if engagement_col and engagement_col in subset.columns:
            tracks_analysis[classification]['engagement'] = int(pd.to_numeric(subset[engagement_col], errors='coerce').fillna(0).sum())
        
        # المشاعر
        if sentiment_col and sentiment_col in subset.columns:
            sentiment_counts = subset[sentiment_col].value_counts().to_dict()
            tracks_analysis[classification]['sentiment'] = {str(k): int(v) for k, v in sentiment_counts.items()}
        
        # المصادر
        if source_col and source_col in subset.columns:
            source_counts = subset[source_col].value_counts().to_dict()
            tracks_analysis[classification]['sources'] = {str(k): int(v) for k, v in source_counts.items()}
    
    results['tracks'] = tracks_analysis
    
    # الإجماليات
    results['totals'] = {
        'total_records': len(df),
        'ministry_count': tracks_analysis['ministry']['count'],
        'global_events_count': tracks_analysis['global_events']['count'],
        'total_reach': tracks_analysis['ministry']['reach'] + tracks_analysis['global_events']['reach'],
        'total_engagement': tracks_analysis['ministry']['engagement'] + tracks_analysis['global_events']['engagement']
    }
    
    # توزيع المشاعر الإجمالي
    if sentiment_col and sentiment_col in df.columns:
        results['sentiment_distribution'] = {str(k): int(v) for k, v in df[sentiment_col].value_counts().to_dict().items()}
    
    # توزيع المصادر (Social vs Traditional) - استخدام العمود media_category
    if 'media_category' in df.columns:
        social_count = len(df[df['media_category'] == 'social'])
        traditional_count = len(df[df['media_category'] == 'traditional'])
        
        results['source_distribution'] = {
            'social': social_count,
            'traditional': traditional_count,
            'detailed': {}
        }
        
        if source_col and source_col in df.columns:
            source_dist = df[source_col].value_counts().to_dict()
            results['source_distribution']['detailed'] = {str(k): int(v) for k, v in source_dist.items()}
    elif source_col and source_col in df.columns:
        source_dist = df[source_col].value_counts().to_dict()
        social_count = 0
        traditional_count = 0
        
        for source, count in source_dist.items():
            source_lower = str(source).lower()
            if any(x in source_lower for x in ['twitter', 'x', 'social', 'facebook', 'instagram', 'tiktok']):
                social_count += count
            else:
                traditional_count += count
        
        results['source_distribution'] = {
            'social': social_count,
            'traditional': traditional_count,
            'detailed': {str(k): int(v) for k, v in source_dist.items()}
        }
    
    # أهم المؤثرين
    influencer_col = None
    for col in ['Author Name', 'Author', 'Source']:
        if col in df.columns:
            influencer_col = col
            break
    
    if influencer_col:
        # استبعاد القيم الفارغة والمصادر الإخبارية
        influencers = df[influencer_col].dropna()
        influencer_counts = influencers.value_counts()
        
        top_influencers = []
        for name, count in influencer_counts.head(10).items():
            if name and str(name).strip() and len(str(name)) > 2:
                # حساب الوصول والتفاعل لكل مؤثر
                influencer_data = df[df[influencer_col] == name]
                reach = 0
                engagement = 0
                
                if reach_col and reach_col in influencer_data.columns:
                    reach = int(pd.to_numeric(influencer_data[reach_col], errors='coerce').fillna(0).sum())
                
                if engagement_col and engagement_col in influencer_data.columns:
                    engagement = int(pd.to_numeric(influencer_data[engagement_col], errors='coerce').fillna(0).sum())
                
                top_influencers.append({
                    'name': str(name),
                    'mentions': int(count),
                    'reach': reach,
                    'engagement': engagement
                })
                
                if len(top_influencers) >= 5:
                    break
        
        results['top_influencers'] = top_influencers
    
    # أهم الهاشتاقات
    hashtag_col = None
    for col in ['Hashtags', 'Key Phrases', 'Keywords']:
        if col in df.columns:
            hashtag_col = col
            break
    
    if hashtag_col:
        all_hashtags = []
        for tags in df[hashtag_col].dropna():
            if isinstance(tags, str):
                for tag in tags.split(','):
                    tag = tag.strip()
                    if tag.startswith('#') or (tag and len(tag) > 2):
                        all_hashtags.append(tag)
        
        from collections import Counter
        hashtag_counts = Counter(all_hashtags)
        results['top_hashtags'] = [{'tag': tag, 'count': count} for tag, count in hashtag_counts.most_common(5)]
    
    return results

def main():
    print("=" * 60)
    print("تحليل بيانات Meltwater - مجلد qatr3")
    print("=" * 60)
    print()
    
    results = analyze_data()
    
    # حفظ النتائج
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print("ملخص النتائج")
    print("=" * 60)
    print()
    
    totals = results.get('totals', {})
    print(f"📊 إجمالي السجلات: {totals.get('total_records', 0):,}")
    print(f"   ├─ الوزارة: {totals.get('ministry_count', 0):,}")
    print(f"   └─ الفعاليات العالمية: {totals.get('global_events_count', 0):,}")
    print()
    print(f"❌ السجلات المستبعدة: {results.get('excluded_count', 0):,}")
    print()
    print(f"🌍 إجمالي الوصول: {totals.get('total_reach', 0):,}")
    print(f"💬 إجمالي التفاعل: {totals.get('total_engagement', 0):,}")
    print()
    
    # توزيع المصادر
    source_dist = results.get('source_distribution', {})
    if source_dist:
        print("📱 توزيع المصادر:")
        print(f"   ├─ منصات التواصل: {source_dist.get('social', 0):,}")
        print(f"   └─ الإعلام التقليدي: {source_dist.get('traditional', 0):,}")
        print()
    
    # المشاعر
    sentiment = results.get('sentiment_distribution', {})
    if sentiment:
        print("😊 توزيع المشاعر:")
        for sent, count in sentiment.items():
            print(f"   ├─ {sent}: {count:,}")
        print()
    
    # المؤثرين
    influencers = results.get('top_influencers', [])
    if influencers:
        print("👥 أبرز المؤثرين:")
        for i, inf in enumerate(influencers, 1):
            print(f"   {i}. {inf['name']} ({inf['mentions']} ذكر)")
        print()
    
    print(f"✅ تم حفظ النتائج في: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
