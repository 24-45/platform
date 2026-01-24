import pandas as pd
import os
import json
from datetime import datetime

BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr3"
OUTPUT_FILE = "/Users/taherirshaid/Desktop/Project/24-45-Platform/deep_strategic_report.json"

MINISTRY_KEYWORDS = ["وزارة الرياضة والشباب", "سعادة الوزير", "وكيل الوزارة", "قرار", "اتفاقية", "شراكة", "تدشين", "MSY"]
EVENTS_KEYWORDS = ["كأس العرب", "كأس القارات", "فورمولا 1", "بادل", "UFC", "FIFA", "Arab Cup"]

def classify_track(text):
    text = str(text).lower()
    is_min = any(k.lower() in text for k in MINISTRY_KEYWORDS)
    is_eve = any(k.lower() in text for k in EVENTS_KEYWORDS)
    if is_min and not is_eve: return "Ministry"
    if is_eve: return "Global Events"
    return "Other"

print("=" * 70)
print("تحليل صحيح - قراءة Analytics + X insights فقط")
print("=" * 70)

# قراءة الملفات الصحيحة فقط
traditional_records = []
social_records = []

for root, dirs, files in os.walk(BASE_PATH):
    folder_name = os.path.basename(root)
    
    for file in files:
        if not file.endswith('.csv') or 'Sentiment_' in file:
            continue
            
        filepath = os.path.join(root, file)
        
        try:
            df = pd.read_csv(filepath, encoding='utf-16-le', sep='\t', low_memory=False, on_bad_lines='skip')
            
            # قراءة Analytics للإعلام التقليدي
            if folder_name == 'Analytics':
                df['media_type'] = 'traditional'
                traditional_records.append(df)
                print(f"📰 Analytics: {len(df):,} سجل تقليدي")
            
            # قراءة X insights لمنصات التواصل
            elif folder_name == 'X insights':
                df['media_type'] = 'social'
                social_records.append(df)
                print(f"📱 X insights: {len(df):,} سجل اجتماعي")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")

# دمج البيانات
print("\n" + "-" * 50)

trad_df = pd.concat(traditional_records, ignore_index=True) if traditional_records else pd.DataFrame()
soc_df = pd.concat(social_records, ignore_index=True) if social_records else pd.DataFrame()

print(f"الإعلام التقليدي (قبل إزالة التكرار): {len(trad_df):,}")
print(f"منصات التواصل (قبل إزالة التكرار): {len(soc_df):,}")

# إزالة التكرار
if 'Document ID' in trad_df.columns:
    trad_df = trad_df.drop_duplicates(subset=['Document ID'])
if 'Document ID' in soc_df.columns:
    soc_df = soc_df.drop_duplicates(subset=['Document ID'])

print(f"\nالإعلام التقليدي (بعد إزالة التكرار): {len(trad_df):,}")
print(f"منصات التواصل (بعد إزالة التكرار): {len(soc_df):,}")

# تصنيف المسارات
trad_df['Track'] = trad_df['Hit Sentence'].apply(classify_track) if 'Hit Sentence' in trad_df.columns else 'Unknown'
soc_df['Track'] = soc_df['Hit Sentence'].apply(classify_track) if 'Hit Sentence' in soc_df.columns else 'Unknown'

# دمج الكل
df = pd.concat([trad_df, soc_df], ignore_index=True)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

print(f"\n📊 الإجمالي النهائي: {len(df):,}")

# =============== تحليل الإعلام التقليدي ===============
print("\n" + "=" * 50)
print("تحليل الإعلام التقليدي")
print("=" * 50)

# Timeline
timeline_data = {}
if not trad_df.empty and 'Date' in trad_df.columns:
    trad_df['Date'] = pd.to_datetime(trad_df['Date'], errors='coerce')
    trad_valid = trad_df[trad_df['Date'].notna()]
    if not trad_valid.empty:
        weekly = trad_valid.groupby(trad_valid['Date'].dt.to_period('W')).size()
        timeline_data = {str(k): int(v) for k, v in weekly.items()}

# المواضيع
top_topics = {}
if 'Keyphrases' in trad_df.columns:
    keyphrases = trad_df['Keyphrases'].dropna().str.split(';').explode()
    keyphrases = keyphrases[keyphrases.str.strip() != '']
    if not keyphrases.empty:
        top_topics = {str(k): int(v) for k, v in keyphrases.value_counts().head(10).items()}

trad_analysis = {
    "total_volume": len(trad_df),
    "volume_by_track": {str(k): int(v) for k, v in trad_df['Track'].value_counts().items()},
    "timeline": timeline_data,
    "sentiment": {str(k): int(v) for k, v in trad_df['Sentiment'].value_counts().items()} if 'Sentiment' in trad_df.columns else {},
    "top_topics": top_topics
}

# =============== تحليل منصات التواصل ===============
print("=" * 50)
print("تحليل منصات التواصل")
print("=" * 50)

total_reach = int(pd.to_numeric(soc_df['Reach'], errors='coerce').fillna(0).sum()) if 'Reach' in soc_df.columns else 0
total_engagement = int(pd.to_numeric(soc_df['Engagement'], errors='coerce').fillna(0).sum()) if 'Engagement' in soc_df.columns else 0

# أفضل المؤثرين
top_influencers = []
if 'Author Handle' in soc_df.columns:
    inf_stats = soc_df.groupby('Author Handle').agg({
        'Reach': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum(),
        'Engagement': lambda x: pd.to_numeric(x, errors='coerce').fillna(0).sum(),
        'Document ID': 'count'
    }).rename(columns={'Document ID': 'posts'})
    
    inf_stats = inf_stats.sort_values(by='Reach', ascending=False).head(10)
    
    for handle, row in inf_stats.iterrows():
        if handle and str(handle).strip():
            top_influencers.append({
                "handle": str(handle),
                "reach": int(row['Reach']),
                "engagement": int(row['Engagement']),
                "posts": int(row['posts'])
            })

soc_analysis = {
    "total_volume": len(soc_df),
    "metrics": {
        "total_reach": total_reach,
        "total_engagement": total_engagement,
        "engagement_rate": round((total_engagement / total_reach * 100), 4) if total_reach > 0 else 0
    },
    "volume_by_track": {str(k): int(v) for k, v in soc_df['Track'].value_counts().items()},
    "sentiment": {str(k): int(v) for k, v in soc_df['Sentiment'].value_counts().items()} if 'Sentiment' in soc_df.columns else {},
    "top_influencers": top_influencers
}

# =============== التقرير النهائي ===============
report = {
    "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "data_source": "Analytics + X insights only (no duplicates)",
    "executive_summary": {
        "total_volume": len(df),
        "traditional_count": len(trad_df),
        "social_count": len(soc_df),
        "track_distribution": {str(k): int(v) for k, v in df['Track'].value_counts().items()}
    },
    "traditional_media": trad_analysis,
    "social_media": soc_analysis
}

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=4)

# =============== عرض النتائج ===============
print("\n" + "=" * 70)
print("✅ النتائج الصحيحة")
print("=" * 70)

print(f"\n📊 إجمالي المواد: {len(df):,}")
print(f"   ├─ 📰 الإعلام التقليدي: {len(trad_df):,} ({len(trad_df)/len(df)*100:.1f}%)")
print(f"   └─ 📱 منصات التواصل: {len(soc_df):,} ({len(soc_df)/len(df)*100:.1f}%)")

print(f"\n🎯 توزيع المسارات:")
for track, count in df['Track'].value_counts().items():
    print(f"   ├─ {track}: {count:,}")

print(f"\n🌍 الوصول: {total_reach:,}")
print(f"💬 التفاعل: {total_engagement:,}")

print(f"\n✅ تم الحفظ في: {OUTPUT_FILE}")
