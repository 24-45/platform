import pandas as pd
import json
import os
import re
from collections import Counter
from datetime import datetime

BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr3"
OUTPUT_FILE = "/Users/taherirshaid/Desktop/Project/24-45-Platform/deep_qualitative_analysis.json"

# =============== الكلمات المفتاحية للتصنيف ===============

# كلمات جودة التنظيم
ORGANIZATION_QUALITY = [
    "تنظيم", "منظم", "إبهار", "رائع", "متميز", "احترافي", "عالمي",
    "متطوعين", "خدمات", "بنية تحتية", "ملاعب", "استضافة", "ضيافة",
    "تجربة", "سلس", "ناجح", "نجاح", "إنجاز", "تفوق", "excellence",
    "organization", "world-class", "infrastructure", "hospitality"
]

# كلمات كفاءة الإدارة
MANAGEMENT_EFFICIENCY = [
    "إدارة", "قيادة", "استراتيجية", "قرار", "خطة", "تطوير", "تمكين",
    "رؤية", "إنجاز", "مبادرة", "شراكة", "اتفاقية", "تعاون",
    "leadership", "management", "strategy", "vision", "initiative"
]

# كلمات الإشادة بالدولة
STATE_PRAISE = [
    "قطر", "الدولة", "دولة قطر", "Qatar", "قطري", "الدوحة",
    "سمعة", "مكانة", "ريادة", "صورة", "إنجاز قطر", "نموذج"
]

# كلمات الإشادة بالوزارة
MINISTRY_PRAISE = [
    "وزارة الرياضة", "الوزارة", "سعادة الوزير", "وزير الرياضة",
    "صالح الحمد", "Ministry of Sports", "MSY"
]

# كلمات المحتوى الرياضي البحت
SPORTS_CONTENT = [
    "مباراة", "هدف", "فوز", "خسارة", "لاعب", "منتخب", "بطولة",
    "نتيجة", "تأهل", "إقصاء", "ركلة", "تسديدة", "حارس",
    "match", "goal", "win", "player", "team", "score"
]

# كلمات تصريحات الوزير
MINISTER_STATEMENTS = [
    "صرح", "أكد", "أعلن", "قال الوزير", "تصريح", "كلمة",
    "خلال حديثه", "في تصريحات", "أشار", "نوه"
]

# كلمات الثقة والإيجابية
CONFIDENCE_KEYWORDS = [
    "ثقة", "تفاؤل", "نجاح", "إنجاز", "فخر", "اعتزاز", "تميز",
    "قدرة", "كفاءة", "استعداد", "جاهزية", "تألق"
]

# =============== وظائف التحليل ===============

def extract_ngrams(text, n=2):
    """استخراج N-grams من النص"""
    if pd.isna(text):
        return []
    words = str(text).split()
    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        # تنظيف من الرموز
        ngram = re.sub(r'[^\w\s]', '', ngram)
        if len(ngram) > 3:
            ngrams.append(ngram)
    return ngrams

def classify_content(text):
    """تصنيف المحتوى إلى فئات"""
    if pd.isna(text):
        return "other"
    
    text_lower = str(text).lower()
    
    scores = {
        "state_praise": sum(1 for k in STATE_PRAISE if k.lower() in text_lower),
        "ministry_praise": sum(1 for k in MINISTRY_PRAISE if k.lower() in text_lower),
        "sports_content": sum(1 for k in SPORTS_CONTENT if k.lower() in text_lower),
        "organization_quality": sum(1 for k in ORGANIZATION_QUALITY if k.lower() in text_lower)
    }
    
    max_category = max(scores, key=scores.get)
    if scores[max_category] > 0:
        return max_category
    return "other"

def has_minister_statement(text):
    """التحقق من وجود تصريح للوزير"""
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    return any(k.lower() in text_lower for k in MINISTER_STATEMENTS)

def calculate_confidence_score(text):
    """حساب درجة الثقة في النص"""
    if pd.isna(text):
        return 0
    text_lower = str(text).lower()
    return sum(1 for k in CONFIDENCE_KEYWORDS if k.lower() in text_lower)

def analyze_deep_content():
    """التحليل المعمق للمحتوى"""
    
    print("=" * 70)
    print("تحليل المحتوى النوعي المعمق (Qualitative Content Analysis)")
    print("=" * 70)
    
    # قراءة البيانات
    all_records = []
    
    for root, dirs, files in os.walk(BASE_PATH):
        folder_name = os.path.basename(root)
        
        if folder_name not in ['Analytics', 'X insights']:
            continue
            
        for file in files:
            if not file.endswith('.csv') or 'Sentiment_' in file:
                continue
            
            filepath = os.path.join(root, file)
            try:
                df = pd.read_csv(filepath, encoding='utf-16-le', sep='\t', low_memory=False, on_bad_lines='skip')
                df['media_type'] = 'social' if folder_name == 'X insights' else 'traditional'
                all_records.append(df)
                print(f"✓ قراءة {len(df):,} سجل من {folder_name}")
            except Exception as e:
                print(f"❌ خطأ: {e}")
    
    if not all_records:
        print("لم يتم العثور على بيانات")
        return
    
    df = pd.concat(all_records, ignore_index=True)
    if 'Document ID' in df.columns:
        df = df.drop_duplicates(subset=['Document ID'])
    
    print(f"\n📊 إجمالي السجلات: {len(df):,}")
    
    # تصنيف المسارات
    def classify_track(text):
        text = str(text).lower()
        ministry_kw = ["وزارة الرياضة", "سعادة الوزير", "وكيل الوزارة", "msy"]
        events_kw = ["كأس العرب", "كأس القارات", "فورمولا", "ufc", "fifa", "arab cup"]
        
        if any(k in text for k in events_kw):
            return "Global Events"
        if any(k in text for k in ministry_kw):
            return "Ministry"
        return "Other"
    
    df['Track'] = df['Hit Sentence'].apply(classify_track)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # =============== 1. تحليل سياق النجاح ===============
    print("\n" + "-" * 50)
    print("1️⃣ تحليل سياق النجاح في الفعاليات الكبرى")
    print("-" * 50)
    
    events_df = df[df['Track'] == 'Global Events']
    
    # استخراج N-grams لجودة التنظيم
    all_bigrams = []
    all_trigrams = []
    
    for text in events_df['Hit Sentence'].dropna():
        all_bigrams.extend(extract_ngrams(text, 2))
        all_trigrams.extend(extract_ngrams(text, 3))
    
    top_bigrams = Counter(all_bigrams).most_common(20)
    top_trigrams = Counter(all_trigrams).most_common(15)
    
    # تصفية N-grams المتعلقة بالتنظيم
    organization_ngrams = []
    for ngram, count in top_bigrams + top_trigrams:
        if any(k.lower() in ngram.lower() for k in ORGANIZATION_QUALITY + MANAGEMENT_EFFICIENCY):
            organization_ngrams.append({"phrase": ngram, "count": count})
    
    print(f"   عبارات التنظيم والجودة: {len(organization_ngrams)}")
    
    # =============== 2. تحليل محاور القيادة ===============
    print("\n" + "-" * 50)
    print("2️⃣ تحليل محاور القيادة في مسار الوزارة")
    print("-" * 50)
    
    ministry_df = df[df['Track'] == 'Ministry']
    
    leadership_ngrams = []
    for text in ministry_df['Hit Sentence'].dropna():
        bigrams = extract_ngrams(text, 2)
        for bg in bigrams:
            if any(k.lower() in bg.lower() for k in MANAGEMENT_EFFICIENCY):
                leadership_ngrams.append(bg)
    
    leadership_counts = Counter(leadership_ngrams).most_common(15)
    print(f"   عبارات القيادة والإدارة: {len(leadership_counts)}")
    
    # =============== 3. تصنيف الردود والتفاعلات ===============
    print("\n" + "-" * 50)
    print("3️⃣ تصنيف الردود والتفاعلات")
    print("-" * 50)
    
    df['content_category'] = df['Hit Sentence'].apply(classify_content)
    category_counts = df['content_category'].value_counts()
    
    print(f"   إشادة بالدولة: {category_counts.get('state_praise', 0):,}")
    print(f"   إشادة بالوزارة: {category_counts.get('ministry_praise', 0):,}")
    print(f"   محتوى رياضي بحت: {category_counts.get('sports_content', 0):,}")
    print(f"   جودة التنظيم: {category_counts.get('organization_quality', 0):,}")
    print(f"   أخرى: {category_counts.get('other', 0):,}")
    
    # =============== 4. الربط الزمني ===============
    print("\n" + "-" * 50)
    print("4️⃣ الربط الزمني (تصريحات الوزير ↔ نبرة الثقة)")
    print("-" * 50)
    
    df['has_minister_statement'] = df['Hit Sentence'].apply(has_minister_statement)
    df['confidence_score'] = df['Hit Sentence'].apply(calculate_confidence_score)
    
    # تجميع حسب الأسبوع
    df_valid = df[df['Date'].notna()].copy()
    df_valid['week'] = df_valid['Date'].dt.to_period('W')
    
    weekly_analysis = df_valid.groupby('week').agg({
        'has_minister_statement': 'sum',
        'confidence_score': 'mean',
        'Document ID': 'count'
    }).rename(columns={'Document ID': 'volume'})
    
    # حساب الارتباط
    correlation_data = []
    for week, row in weekly_analysis.iterrows():
        correlation_data.append({
            "week": str(week),
            "minister_statements": int(row['has_minister_statement']),
            "avg_confidence": round(row['confidence_score'], 3),
            "volume": int(row['volume'])
        })
    
    print(f"   أسابيع التحليل: {len(correlation_data)}")
    
    # =============== 5. تحليل خصائص الوسائط ===============
    print("\n" + "-" * 50)
    print("5️⃣ تحليل خصائص الوسائط الإعلامية")
    print("-" * 50)
    
    trad_df = df[df['media_type'] == 'traditional']
    soc_df = df[df['media_type'] == 'social']
    
    # تركيز الإعلام التقليدي
    trad_categories = trad_df['content_category'].value_counts()
    soc_categories = soc_df['content_category'].value_counts()
    
    print(f"\n   📰 الإعلام التقليدي:")
    for cat, count in trad_categories.items():
        pct = count / len(trad_df) * 100 if len(trad_df) > 0 else 0
        print(f"      {cat}: {count:,} ({pct:.1f}%)")
    
    print(f"\n   📱 منصات التواصل:")
    for cat, count in soc_categories.items():
        pct = count / len(soc_df) * 100 if len(soc_df) > 0 else 0
        print(f"      {cat}: {count:,} ({pct:.1f}%)")
    
    # =============== بناء التقرير النهائي ===============
    
    report = {
        "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sample_size": len(df),
        
        "1_success_context_analysis": {
            "description": "تحليل سياق النجاح في الفعاليات الكبرى",
            "events_volume": len(events_df),
            "top_organization_phrases": organization_ngrams[:15],
            "top_bigrams": [{"phrase": p, "count": c} for p, c in top_bigrams[:10]],
            "top_trigrams": [{"phrase": p, "count": c} for p, c in top_trigrams[:10]]
        },
        
        "2_leadership_analysis": {
            "description": "تحليل محاور القيادة في مسار الوزارة",
            "ministry_volume": len(ministry_df),
            "leadership_phrases": [{"phrase": p, "count": c} for p, c in leadership_counts]
        },
        
        "3_content_classification": {
            "description": "تصنيف الردود والتفاعلات",
            "categories": {
                "state_praise": int(category_counts.get('state_praise', 0)),
                "ministry_praise": int(category_counts.get('ministry_praise', 0)),
                "sports_content": int(category_counts.get('sports_content', 0)),
                "organization_quality": int(category_counts.get('organization_quality', 0)),
                "other": int(category_counts.get('other', 0))
            },
            "percentages": {
                cat: round(count / len(df) * 100, 2) 
                for cat, count in category_counts.items()
            }
        },
        
        "4_temporal_correlation": {
            "description": "الربط الزمني بين تصريحات الوزير ونبرة الثقة",
            "weekly_data": correlation_data,
            "total_minister_statements": int(df['has_minister_statement'].sum()),
            "avg_confidence_overall": round(df['confidence_score'].mean(), 3)
        },
        
        "5_media_features": {
            "traditional_media": {
                "total": len(trad_df),
                "focus_analysis": {
                    cat: {
                        "count": int(count),
                        "percentage": round(count / len(trad_df) * 100, 2) if len(trad_df) > 0 else 0
                    }
                    for cat, count in trad_categories.items()
                },
                "insight": "الإعلام التقليدي يركز أكثر على التغطية الرسمية والأحداث"
            },
            "social_media": {
                "total": len(soc_df),
                "focus_analysis": {
                    cat: {
                        "count": int(count),
                        "percentage": round(count / len(soc_df) * 100, 2) if len(soc_df) > 0 else 0
                    }
                    for cat, count in soc_categories.items()
                },
                "insight": "منصات التواصل تعكس التفاعل العفوي والآراء الشخصية"
            }
        },
        
        "6_strategic_narrative": {
            "ministry_image": {
                "visibility": len(ministry_df),
                "positive_mentions": int(category_counts.get('ministry_praise', 0)),
                "assessment": "صورة الوزارة كجهة راعية ومنظمة"
            },
            "state_reputation": {
                "global_events_coverage": len(events_df),
                "state_praise_mentions": int(category_counts.get('state_praise', 0)),
                "assessment": "تأثير الفعاليات على سمعة الدولة"
            }
        }
    }
    
    # حفظ التقرير
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    
    print("\n" + "=" * 70)
    print("✅ اكتمل التحليل النوعي المعمق")
    print("=" * 70)
    print(f"\n📊 ملخص النتائج:")
    print(f"   حجم العينة: {len(df):,}")
    print(f"   تصريحات الوزير المكتشفة: {int(df['has_minister_statement'].sum()):,}")
    print(f"   متوسط درجة الثقة: {df['confidence_score'].mean():.3f}")
    print(f"\n✅ تم الحفظ في: {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_deep_content()
