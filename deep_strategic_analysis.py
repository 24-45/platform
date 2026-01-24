import pandas as pd
import glob
import json
import os
from datetime import datetime

# 1. إعداد المسارات والكلمات المفتاحية
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr3"
OUTPUT_FILE = "/Users/taherirshaid/Desktop/Project/24-45-Platform/deep_strategic_report.json"

MINISTRY_KEYWORDS = ["وزارة الرياضة والشباب", "سعادة الوزير", "وكيل الوزارة", "قرار", "اتفاقية", "شراكة", "تدشين", "MSY"]
EVENTS_KEYWORDS = ["كأس العرب", "كأس القارات", "فورمولا 1", "بادل", "UFC", "FIFA", "Arab Cup"]

# 2. وظيفة التصنيف
def classify_track(text):
    text = str(text).lower()
    is_min = any(k.lower() in text for k in MINISTRY_KEYWORDS)
    is_eve = any(k.lower() in text for k in EVENTS_KEYWORDS)
    if is_min and not is_eve: return "Ministry"
    if is_eve: return "Global Events"
    return "Other"

# 3. التحميل والمعالجة - البحث في كل المجلدات الفرعية
def find_csv_files(base_path):
    """البحث عن جميع ملفات CSV في المجلدات الفرعية"""
    csv_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv') and 'Sentiment_' not in file:
                csv_files.append(os.path.join(root, file))
    return csv_files

all_files = find_csv_files(BASE_PATH)
print(f"📂 تم العثور على {len(all_files)} ملف CSV")

df_list = []
for f in all_files:
    try:
        # ملفات Meltwater بترميز UTF-16 LE
        df_temp = pd.read_csv(f, encoding='utf-16-le', sep='\t', low_memory=False, on_bad_lines='skip')
        df_list.append(df_temp)
        print(f"✓ قراءة {len(df_temp)} سجل من {os.path.basename(f)[:50]}...")
    except Exception as e:
        print(f"❌ خطأ في قراءة {os.path.basename(f)}: {e}")

if not df_list:
    print("❌ لم يتم العثور على بيانات!")
    exit()

df = pd.concat(df_list, ignore_index=True).drop_duplicates(subset=['Document ID'])
print(f"\n📊 إجمالي السجلات بعد إزالة التكرار: {len(df)}")

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Track'] = df['Hit Sentence'].apply(classify_track)

# تصنيف المصادر بشكل صحيح
def classify_source(source_type):
    if pd.isna(source_type):
        return 'Other'
    source = str(source_type).lower()
    if any(x in source for x in ['social', 'twitter', 'facebook', 'instagram']):
        return 'Social'
    return 'Traditional'

df['Source_Group'] = df['Source Type'].apply(classify_source)

# 4. استخراج المؤشرات (Traditional Media)
trad_df = df[df['Source_Group'] == 'Traditional']
print(f"\n📰 الإعلام التقليدي: {len(trad_df)} سجل")

# معالجة Timeline
timeline_data = {}
if not trad_df.empty and 'Date' in trad_df.columns:
    trad_df_valid = trad_df[trad_df['Date'].notna()]
    if not trad_df_valid.empty:
        weekly = trad_df_valid.groupby(trad_df_valid['Date'].dt.to_period('W')).size()
        timeline_data = {str(k): int(v) for k, v in weekly.items()}

# معالجة المواضيع
top_topics = {}
if 'Keyphrases' in trad_df.columns:
    keyphrases = trad_df['Keyphrases'].dropna().str.split(';').explode()
    keyphrases = keyphrases[keyphrases.str.strip() != '']
    if not keyphrases.empty:
        top_topics = keyphrases.value_counts().head(10).to_dict()
        top_topics = {str(k): int(v) for k, v in top_topics.items()}

trad_analysis = {
    "volume_by_track": {str(k): int(v) for k, v in trad_df['Track'].value_counts().to_dict().items()},
    "timeline": timeline_data,
    "sentiment": {str(k): int(v) for k, v in trad_df['Sentiment'].value_counts().to_dict().items()} if 'Sentiment' in trad_df.columns else {},
    "top_topics": top_topics
}

# 5. استخراج المؤشرات (Social Media)
soc_df = df[df['Source_Group'] == 'Social']
print(f"📱 منصات التواصل: {len(soc_df)} سجل")

# حساب المقاييس
total_reach = 0
total_engagement = 0

if 'Reach' in soc_df.columns:
    total_reach = int(pd.to_numeric(soc_df['Reach'], errors='coerce').fillna(0).sum())
if 'Engagement' in soc_df.columns:
    total_engagement = int(pd.to_numeric(soc_df['Engagement'], errors='coerce').fillna(0).sum())

# أفضل المؤثرين
top_influencers = []
if 'Author Handle' in soc_df.columns and not soc_df.empty:
    influencer_stats = soc_df.groupby('Author Handle').agg({
        'Reach': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum(),
        'Engagement': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum(),
        'Document ID': 'count'
    }).rename(columns={'Document ID': 'posts'})
    
    influencer_stats = influencer_stats.sort_values(by='Reach', ascending=False).head(10)
    
    for handle, row in influencer_stats.iterrows():
        if handle and str(handle).strip():
            top_influencers.append({
                "handle": str(handle),
                "reach": int(row['Reach']),
                "engagement": int(row['Engagement']),
                "posts": int(row['posts'])
            })

engagement_rate = (total_engagement / total_reach * 100) if total_reach > 0 else 0

soc_analysis = {
    "metrics": {
        "total_reach": total_reach,
        "total_engagement": total_engagement,
        "engagement_rate": round(engagement_rate, 4)
    },
    "top_influencers": top_influencers,
    "volume_by_track": {str(k): int(v) for k, v in soc_df['Track'].value_counts().to_dict().items()},
    "sentiment": {str(k): int(v) for k, v in soc_df['Sentiment'].value_counts().to_dict().items()} if 'Sentiment' in soc_df.columns else {}
}

# 6. المقارنة والنتائج النهائية
report = {
    "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "executive_summary": {
        "total_volume": len(df),
        "traditional_count": len(trad_df),
        "social_count": len(soc_df),
        "track_distribution": {str(k): int(v) for k, v in df['Track'].value_counts().to_dict().items()}
    },
    "traditional_media": trad_analysis,
    "social_media": soc_analysis
}

# حفظ الملف
with open(OUTPUT_FILE, 'w', encoding='utf-8') as j:
    json.dump(report, j, ensure_ascii=False, indent=4)

print("\n" + "="*60)
print("✅ تم استخراج التقرير الاستراتيجي المعمق بنجاح!")
print("="*60)
print(f"\n📊 ملخص النتائج:")
print(f"   إجمالي المواد: {len(df):,}")
print(f"   ├─ الإعلام التقليدي: {len(trad_df):,}")
print(f"   └─ منصات التواصل: {len(soc_df):,}")
print(f"\n   توزيع المسارات:")
for track, count in df['Track'].value_counts().items():
    print(f"   ├─ {track}: {count:,}")
print(f"\n✅ تم الحفظ في: {OUTPUT_FILE}")
