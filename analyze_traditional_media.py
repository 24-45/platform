import pandas as pd
from collections import Counter
import json

# قراءة الملف
file_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"

# قراءة الملف بترميز UTF-16LE
df = pd.read_csv(file_path, sep='\t', encoding='utf-16-le')

print(f"إجمالي السجلات: {len(df)}")

# عرض أنواع المصادر
print(f"\n=== أنواع المصادر (Source Type) ===")
print(df['Source Type'].value_counts())

# فلترة للإعلام التقليدي فقط (online news)
traditional_media = df[df['Source Type'] == 'online news'].copy()
print(f"\n=== إحصائيات الإعلام التقليدي (online news) فقط ===")
print(f"عدد السجلات: {len(traditional_media)}")

# 1. توزيع المشاعر (Sentiment)
print(f"\n=== توزيع المشاعر (Sentiment) ===")
sentiment_counts = traditional_media['Sentiment'].value_counts()
print(sentiment_counts)
total_sentiment = sentiment_counts.sum()
print(f"\nالنسب المئوية:")
for sent, count in sentiment_counts.items():
    print(f"  {sent}: {count} ({count/total_sentiment*100:.1f}%)")

# 2. التوزيع الجغرافي (Country)
print(f"\n=== أعلى 15 دولة ===")
country_counts = traditional_media['Country'].value_counts().head(15)
print(country_counts)

# 3. التوزيع اللغوي (Language)
print(f"\n=== توزيع اللغات ===")
language_counts = traditional_media['Language'].value_counts().head(10)
print(language_counts)

# 4. التوزيع الشهري
print(f"\n=== التوزيع الشهري ===")
traditional_media['Date'] = pd.to_datetime(traditional_media['Date'])
traditional_media['Month'] = traditional_media['Date'].dt.strftime('%Y-%m')
monthly_counts = traditional_media['Month'].value_counts().sort_index()
print(monthly_counts)

# 5. أعلى 10 مصادر
print(f"\n=== أعلى 10 مصادر إعلامية ===")
source_counts = traditional_media['Source Name'].value_counts().head(10)
print(source_counts)

# 6. توزيع جغرافي مفصل (قطر، عربي، دولي)
print(f"\n=== التوزيع الجغرافي (قطر / عربي / دولي) ===")
arab_countries = ['Qatar', 'Saudi Arabia', 'United Arab Emirates', 'Egypt', 'Jordan', 
                  'Morocco', 'Algeria', 'Kuwait', 'Bahrain', 'Oman', 'Iraq', 'Lebanon',
                  'Tunisia', 'Libya', 'Syria', 'Palestine', 'Yemen', 'Sudan']

qatar_count = len(traditional_media[traditional_media['Country'] == 'Qatar'])
arab_count = len(traditional_media[traditional_media['Country'].isin([c for c in arab_countries if c != 'Qatar'])])
international_count = len(traditional_media[~traditional_media['Country'].isin(arab_countries)])

print(f"قطر: {qatar_count}")
print(f"الدول العربية (بدون قطر): {arab_count}")
print(f"دولي: {international_count}")

# حفظ النتائج
results = {
    "total_records": len(df),
    "traditional_media_records": len(traditional_media),
    "sentiment": {str(k): int(v) for k, v in sentiment_counts.items()},
    "top_countries": {str(k): int(v) for k, v in country_counts.items()},
    "languages": {str(k): int(v) for k, v in language_counts.items()},
    "monthly_distribution": {str(k): int(v) for k, v in monthly_counts.items()},
    "top_sources": {str(k): int(v) for k, v in source_counts.items()},
    "geographic_distribution": {
        "qatar": qatar_count,
        "arab_without_qatar": arab_count,
        "international": international_count
    }
}

with open('traditional_media_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== تم حفظ النتائج في traditional_media_analysis.json ===")
