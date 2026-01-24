import pandas as pd
import json
import os
from datetime import datetime

# =============== الأرقام المرجعية الكلية ===============
TOTAL_EVENTS_VOL = 82800
TOTAL_MINISTRY_VOL = 1630
GRAND_TOTAL_VOL = TOTAL_EVENTS_VOL + TOTAL_MINISTRY_VOL

BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr3"
OUTPUT_FILE = "/Users/taherirshaid/Desktop/Project/24-45-Platform/extrapolated_analysis.json"

print("=" * 70)
print("تحليل الإسقاط الإحصائي (Extrapolation)")
print("=" * 70)
print(f"\n📊 الأرقام المرجعية الكلية:")
print(f"   الفعاليات العالمية: {TOTAL_EVENTS_VOL:,}")
print(f"   الوزارة: {TOTAL_MINISTRY_VOL:,}")
print(f"   الإجمالي: {GRAND_TOTAL_VOL:,}")

# =============== قراءة العينة الفعلية ===============
print("\n" + "-" * 50)
print("قراءة العينة من الملفات...")

events_df_list = []
ministry_df_list = []

for root, dirs, files in os.walk(BASE_PATH):
    folder_name = os.path.basename(root)
    parent_folder = os.path.basename(os.path.dirname(root))
    
    for file in files:
        if not file.endswith('.csv') or 'Sentiment_' in file:
            continue
        
        # نقرأ فقط Analytics و X insights
        if folder_name not in ['Analytics', 'X insights']:
            continue
            
        filepath = os.path.join(root, file)
        
        try:
            df = pd.read_csv(filepath, encoding='utf-16-le', sep='\t', low_memory=False, on_bad_lines='skip')
            
            if 'الأحاث العالمية' in parent_folder or 'العالمية' in parent_folder:
                events_df_list.append(df)
                print(f"✓ فعاليات - {folder_name}: {len(df):,} سجل")
            elif 'وزارة الرياضة' in parent_folder:
                ministry_df_list.append(df)
                print(f"✓ وزارة - {folder_name}: {len(df):,} سجل")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")

# دمج وإزالة التكرار
events_sample = pd.concat(events_df_list, ignore_index=True) if events_df_list else pd.DataFrame()
ministry_sample = pd.concat(ministry_df_list, ignore_index=True) if ministry_df_list else pd.DataFrame()

if 'Document ID' in events_sample.columns:
    events_sample = events_sample.drop_duplicates(subset=['Document ID'])
if 'Document ID' in ministry_sample.columns:
    ministry_sample = ministry_sample.drop_duplicates(subset=['Document ID'])

print(f"\n📋 حجم العينة:")
print(f"   عينة الفعاليات: {len(events_sample):,}")
print(f"   عينة الوزارة: {len(ministry_sample):,}")

# =============== حساب النسب من العينة ===============
print("\n" + "-" * 50)
print("حساب النسب المئوية من العينة...")

def calculate_sentiment_ratios(df):
    """حساب نسب المشاعر من DataFrame"""
    if 'Sentiment' not in df.columns or df.empty:
        return {"positive": 0, "neutral": 0, "negative": 0, "unknown": 0}
    
    total = len(df)
    sentiment_counts = df['Sentiment'].value_counts()
    
    return {
        "positive": sentiment_counts.get('positive', 0) / total,
        "neutral": sentiment_counts.get('neutral', 0) / total,
        "negative": sentiment_counts.get('negative', 0) / total,
        "unknown": sentiment_counts.get('unknown', 0) / total
    }

def calculate_source_ratios(df):
    """حساب نسب المصادر (Traditional vs Social)"""
    if 'Source Type' not in df.columns or df.empty:
        return {"traditional": 0.5, "social": 0.5}
    
    total = len(df)
    source_counts = df['Source Type'].value_counts()
    
    social_count = source_counts.get('social network', 0)
    traditional_count = total - social_count
    
    return {
        "traditional": traditional_count / total,
        "social": social_count / total
    }

# حساب النسب للفعاليات
events_sentiment = calculate_sentiment_ratios(events_sample)
events_sources = calculate_source_ratios(events_sample)

# حساب النسب للوزارة
ministry_sentiment = calculate_sentiment_ratios(ministry_sample)
ministry_sources = calculate_source_ratios(ministry_sample)

# النسب الإجمالية المجمعة
combined_df = pd.concat([events_sample, ministry_sample], ignore_index=True)
combined_sentiment = calculate_sentiment_ratios(combined_df)
combined_sources = calculate_source_ratios(combined_df)

print(f"\n📈 نسب المشاعر (من العينة):")
print(f"   إيجابي: {combined_sentiment['positive']*100:.1f}%")
print(f"   محايد: {combined_sentiment['neutral']*100:.1f}%")
print(f"   سلبي: {combined_sentiment['negative']*100:.1f}%")

print(f"\n📱 نسب المصادر (من العينة):")
print(f"   تقليدي: {combined_sources['traditional']*100:.1f}%")
print(f"   اجتماعي: {combined_sources['social']*100:.1f}%")

# =============== الإسقاط الإحصائي ===============
print("\n" + "=" * 50)
print("الإسقاط الإحصائي على الأرقام الكلية")
print("=" * 50)

extrapolated_results = {
    "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "reference_data": {
        "total_events_volume": TOTAL_EVENTS_VOL,
        "total_ministry_volume": TOTAL_MINISTRY_VOL,
        "grand_total_volume": GRAND_TOTAL_VOL
    },
    "sample_data": {
        "events_sample_size": len(events_sample),
        "ministry_sample_size": len(ministry_sample),
        "total_sample_size": len(combined_df)
    },
    "sentiment_ratios_from_sample": {
        "positive_ratio": round(combined_sentiment['positive'], 4),
        "neutral_ratio": round(combined_sentiment['neutral'], 4),
        "negative_ratio": round(combined_sentiment['negative'], 4)
    },
    "source_ratios_from_sample": {
        "traditional_ratio": round(combined_sources['traditional'], 4),
        "social_ratio": round(combined_sources['social'], 4)
    },
    "extrapolated_totals": {
        "estimated_positive": int(GRAND_TOTAL_VOL * combined_sentiment['positive']),
        "estimated_neutral": int(GRAND_TOTAL_VOL * combined_sentiment['neutral']),
        "estimated_negative": int(GRAND_TOTAL_VOL * combined_sentiment['negative']),
        "estimated_traditional": int(GRAND_TOTAL_VOL * combined_sources['traditional']),
        "estimated_social": int(GRAND_TOTAL_VOL * combined_sources['social'])
    },
    "by_track": {
        "global_events": {
            "total_volume": TOTAL_EVENTS_VOL,
            "estimated_positive": int(TOTAL_EVENTS_VOL * events_sentiment['positive']),
            "estimated_neutral": int(TOTAL_EVENTS_VOL * events_sentiment['neutral']),
            "estimated_negative": int(TOTAL_EVENTS_VOL * events_sentiment['negative']),
            "estimated_traditional": int(TOTAL_EVENTS_VOL * events_sources['traditional']),
            "estimated_social": int(TOTAL_EVENTS_VOL * events_sources['social']),
            "share_percentage": round((TOTAL_EVENTS_VOL / GRAND_TOTAL_VOL) * 100, 2)
        },
        "ministry": {
            "total_volume": TOTAL_MINISTRY_VOL,
            "estimated_positive": int(TOTAL_MINISTRY_VOL * ministry_sentiment['positive']),
            "estimated_neutral": int(TOTAL_MINISTRY_VOL * ministry_sentiment['neutral']),
            "estimated_negative": int(TOTAL_MINISTRY_VOL * ministry_sentiment['negative']),
            "estimated_traditional": int(TOTAL_MINISTRY_VOL * ministry_sources['traditional']),
            "estimated_social": int(TOTAL_MINISTRY_VOL * ministry_sources['social']),
            "share_percentage": round((TOTAL_MINISTRY_VOL / GRAND_TOTAL_VOL) * 100, 2)
        }
    }
}

# حفظ النتائج
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(extrapolated_results, f, ensure_ascii=False, indent=4)

# =============== عرض النتائج ===============
print(f"\n📊 الأرقام المُسقطة على الإجمالي ({GRAND_TOTAL_VOL:,}):")
print(f"\n   المشاعر:")
print(f"   ├─ 😊 إيجابي: {extrapolated_results['extrapolated_totals']['estimated_positive']:,}")
print(f"   ├─ 😐 محايد: {extrapolated_results['extrapolated_totals']['estimated_neutral']:,}")
print(f"   └─ 😞 سلبي: {extrapolated_results['extrapolated_totals']['estimated_negative']:,}")

print(f"\n   المصادر:")
print(f"   ├─ 📰 تقليدي: {extrapolated_results['extrapolated_totals']['estimated_traditional']:,}")
print(f"   └─ 📱 اجتماعي: {extrapolated_results['extrapolated_totals']['estimated_social']:,}")

print(f"\n📈 حسب المسار:")
print(f"\n   🌍 الفعاليات العالمية ({TOTAL_EVENTS_VOL:,}):")
print(f"      ├─ إيجابي: {extrapolated_results['by_track']['global_events']['estimated_positive']:,}")
print(f"      ├─ محايد: {extrapolated_results['by_track']['global_events']['estimated_neutral']:,}")
print(f"      └─ سلبي: {extrapolated_results['by_track']['global_events']['estimated_negative']:,}")

print(f"\n   🏛️ الوزارة ({TOTAL_MINISTRY_VOL:,}):")
print(f"      ├─ إيجابي: {extrapolated_results['by_track']['ministry']['estimated_positive']:,}")
print(f"      ├─ محايد: {extrapolated_results['by_track']['ministry']['estimated_neutral']:,}")
print(f"      └─ سلبي: {extrapolated_results['by_track']['ministry']['estimated_negative']:,}")

print(f"\n   📊 حصة كل مسار:")
print(f"      ├─ الفعاليات: {extrapolated_results['by_track']['global_events']['share_percentage']}%")
print(f"      └─ الوزارة: {extrapolated_results['by_track']['ministry']['share_percentage']}%")

print(f"\n✅ تم الحفظ في: {OUTPUT_FILE}")
