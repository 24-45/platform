import pandas as pd
import os

BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr3"

print("=" * 70)
print("تحليل مصادر البيانات في كل ملف")
print("=" * 70)

total_files = 0
total_records = 0
all_sources = {}

for root, dirs, files in os.walk(BASE_PATH):
    for file in files:
        if file.endswith('.csv') and 'Sentiment_' not in file:
            filepath = os.path.join(root, file)
            try:
                df = pd.read_csv(filepath, encoding='utf-16-le', sep='\t', low_memory=False, on_bad_lines='skip')
                folder = os.path.basename(os.path.dirname(filepath))
                parent_folder = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
                
                total_files += 1
                total_records += len(df)
                
                print(f"\n📁 [{parent_folder[:20]}] / {folder}")
                print(f"   ملف: {file[:50]}...")
                print(f"   السجلات: {len(df):,}")
                
                if 'Source Type' in df.columns:
                    source_types = df['Source Type'].value_counts()
                    print(f"   أنواع المصادر:")
                    for st, count in source_types.items():
                        print(f"      - {st}: {count:,}")
                        if st not in all_sources:
                            all_sources[st] = 0
                        all_sources[st] += count
                else:
                    print(f"   ⚠️ لا يوجد عمود Source Type")
                    
            except Exception as e:
                print(f"❌ خطأ في {file}: {e}")

print("\n" + "=" * 70)
print("ملخص إجمالي المصادر (قبل إزالة التكرار)")
print("=" * 70)
print(f"\nعدد الملفات: {total_files}")
print(f"إجمالي السجلات: {total_records:,}")
print(f"\nتوزيع المصادر:")

social_total = 0
traditional_total = 0

for source, count in sorted(all_sources.items(), key=lambda x: x[1], reverse=True):
    print(f"   {source}: {count:,}")
    if 'social' in str(source).lower():
        social_total += count
    else:
        traditional_total += count

print(f"\n📱 منصات التواصل (social network): {social_total:,}")
print(f"📰 الإعلام التقليدي (online news + print): {traditional_total:,}")
