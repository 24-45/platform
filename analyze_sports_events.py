# -*- coding: utf-8 -*-
import pandas as pd
import os
from collections import Counter

# مسارات البيانات
base_path = "static/data/meltwater/Qatr/الفعاليات الرياضية والصحية المحلية"
overview_path = os.path.join(base_path, "overview")
analytics_path = os.path.join(base_path, "analytics")

print("=" * 80)
print("تحليل بيانات الفعاليات الرياضية والصحية المحلية")
print("=" * 80)

# قراءة الملف الرئيسي
main_csv = None
for f in os.listdir(overview_path):
    if f.endswith('.csv') and 'تحدي_الوكرة' in f:
        main_csv = os.path.join(overview_path, f)
        break

if not main_csv:
    for f in os.listdir(overview_path):
        if f.endswith('.csv') and not any(x in f for x in ['Sentiment', 'Top_', 'Mentions']):
            main_csv = os.path.join(overview_path, f)
            break

print(f"\n📁 الملف الرئيسي: {os.path.basename(main_csv)}")

# قراءة البيانات
df = None
for encoding in ['utf-8', 'utf-16', 'cp1256', 'latin-1']:
    for delimiter in ['\t', ',', ';']:
        try:
            df = pd.read_csv(main_csv, encoding=encoding, delimiter=delimiter, on_bad_lines='skip')
            if len(df.columns) > 5:
                print(f"✅ تم القراءة: encoding={encoding}, delimiter='{delimiter}'")
                break
        except:
            continue
    if df is not None and len(df.columns) > 5:
        break

print(f"\n📊 إجمالي السجلات: {len(df)}")

# عرض الأعمدة
print(f"\n📋 الأعمدة ({len(df.columns)}):")
for i, col in enumerate(df.columns[:20]):
    print(f"   {i}: {col}")

# ============================================
# 1. تصفية الأخبار فقط (Online News)
# ============================================
print("\n" + "=" * 80)
print("1️⃣ تصفية الأخبار الإلكترونية فقط")
print("=" * 80)

# البحث عن عمود Source Type (عادة العمود 7)
source_type_col = df.columns[7] if len(df.columns) > 7 else None
print(f"📌 عمود Source Type: {source_type_col}")

if source_type_col:
    print(f"\n📊 توزيع أنواع المصادر:")
    print(df[source_type_col].value_counts())
    
    # تصفية الأخبار
    news_df = df[df[source_type_col].str.contains('news|online', case=False, na=False)]
    social_df = df[df[source_type_col].str.contains('social', case=False, na=False)]
    
    print(f"\n✅ الأخبار الإلكترونية: {len(news_df)} تغطية")
    print(f"❌ وسائل التواصل: {len(social_df)} منشور")
else:
    news_df = df
    print("⚠️ استخدام كل البيانات")

# ============================================
# 2. تحليل المشاعر
# ============================================
print("\n" + "=" * 80)
print("2️⃣ تحليل المشاعر (Sentiment)")
print("=" * 80)

sentiment_col = None
for col in df.columns:
    if 'sentiment' in col.lower():
        sentiment_col = col
        break

if sentiment_col:
    print(f"\n📊 المشاعر (كل البيانات):")
    print(df[sentiment_col].value_counts())
    
    print(f"\n📊 المشاعر (الأخبار فقط):")
    news_sentiment = news_df[sentiment_col].value_counts()
    print(news_sentiment)
    
    # النسب المئوية
    total_news = len(news_df)
    print(f"\n📊 النسب المئوية (الأخبار):")
    for sent, count in news_sentiment.items():
        pct = (count / total_news) * 100
        print(f"   {sent}: {count} ({pct:.1f}%)")

# ============================================
# 3. تحليل الدول
# ============================================
print("\n" + "=" * 80)
print("3️⃣ توزيع الدول")
print("=" * 80)

country_col = None
for col in df.columns:
    if 'country' in col.lower():
        country_col = col
        break

if country_col:
    print(f"\n📊 الدول (الأخبار فقط - أعلى 15):")
    news_countries = news_df[country_col].value_counts().head(15)
    for country, count in news_countries.items():
        pct = (count / len(news_df)) * 100
        print(f"   {country}: {count} ({pct:.1f}%)")

# ============================================
# 4. تحليل اللغات
# ============================================
print("\n" + "=" * 80)
print("4️⃣ توزيع اللغات")
print("=" * 80)

language_col = None
for col in df.columns:
    if 'language' in col.lower():
        language_col = col
        break

if language_col:
    print(f"\n📊 اللغات (الأخبار فقط):")
    news_languages = news_df[language_col].value_counts().head(10)
    for lang, count in news_languages.items():
        pct = (count / len(news_df)) * 100
        print(f"   {lang}: {count} ({pct:.1f}%)")

# ============================================
# 5. تحليل المصادر
# ============================================
print("\n" + "=" * 80)
print("5️⃣ أهم المصادر الإخبارية")
print("=" * 80)

source_name_col = None
for col in df.columns:
    if 'source' in col.lower() and 'name' in col.lower():
        source_name_col = col
        break

if source_name_col:
    print(f"\n📊 المصادر (الأخبار - أعلى 15):")
    news_sources = news_df[source_name_col].value_counts().head(15)
    for source, count in news_sources.items():
        print(f"   {source}: {count}")

# ============================================
# 6. تحليل الفعاليات
# ============================================
print("\n" + "=" * 80)
print("6️⃣ الفعاليات (Input Name)")
print("=" * 80)

input_name_col = None
for col in df.columns:
    if 'input' in col.lower() and 'name' in col.lower():
        input_name_col = col
        break

if input_name_col:
    print(f"\n📊 الفعاليات (كل البيانات):")
    all_events = df[input_name_col].value_counts()
    for event, count in all_events.items():
        pct = (count / len(df)) * 100
        print(f"   {event}: {count} ({pct:.1f}%)")
    
    print(f"\n📊 الفعاليات (الأخبار فقط):")
    news_events = news_df[input_name_col].value_counts()
    for event, count in news_events.items():
        pct = (count / len(news_df)) * 100
        print(f"   {event}: {count} ({pct:.1f}%)")

# ============================================
# 7. تحليل الوصول
# ============================================
print("\n" + "=" * 80)
print("7️⃣ تحليل الوصول (Reach)")
print("=" * 80)

reach_col = None
for col in df.columns:
    if 'reach' in col.lower():
        reach_col = col
        break

if reach_col:
    news_df_copy = news_df.copy()
    news_df_copy[reach_col] = pd.to_numeric(news_df_copy[reach_col], errors='coerce')
    total_reach = news_df_copy[reach_col].sum()
    avg_reach = news_df_copy[reach_col].mean()
    max_reach = news_df_copy[reach_col].max()
    
    print(f"\n📊 إحصائيات الوصول (الأخبار):")
    print(f"   إجمالي الوصول: {total_reach:,.0f}")
    print(f"   متوسط الوصول: {avg_reach:,.0f}")
    print(f"   أعلى وصول: {max_reach:,.0f}")

# ============================================
# 8. التوزيع الأسبوعي
# ============================================
print("\n" + "=" * 80)
print("8️⃣ التوزيع الأسبوعي")
print("=" * 80)

date_col = df.columns[0]  # عادة أول عمود
print(f"📌 عمود التاريخ: {date_col}")

news_df_copy = news_df.copy()
news_df_copy[date_col] = pd.to_datetime(news_df_copy[date_col], errors='coerce')
news_df_copy['week'] = news_df_copy[date_col].dt.strftime('%Y-W%V')

weekly = news_df_copy.groupby('week').size().sort_index()
print(f"\n📊 التوزيع الأسبوعي (الأخبار):")
for week, count in weekly.items():
    print(f"   {week}: {count}")

# ============================================
# 9. أفضل 10 تغطيات إيجابية
# ============================================
print("\n" + "=" * 80)
print("9️⃣ أفضل 10 تغطيات إيجابية")
print("=" * 80)

if sentiment_col and reach_col:
    positive_news = news_df[news_df[sentiment_col].str.lower() == 'positive'].copy()
    positive_news[reach_col] = pd.to_numeric(positive_news[reach_col], errors='coerce')
    top_positive = positive_news.nlargest(10, reach_col)
    
    # البحث عن أعمدة العنوان والرابط
    title_col = None
    url_col = None
    
    for col in df.columns:
        if 'title' in col.lower() or 'headline' in col.lower():
            title_col = col
        if col.lower() == 'url':
            url_col = col
    
    print(f"\n📊 أفضل 10 تغطيات إيجابية:")
    for idx, (_, row) in enumerate(top_positive.iterrows(), 1):
        title = str(row.get(title_col, 'N/A'))[:80] if title_col else 'N/A'
        url = str(row.get(url_col, 'N/A'))[:100] if url_col else 'N/A'
        source = str(row.get(source_name_col, 'N/A')) if source_name_col else 'N/A'
        reach = row.get(reach_col, 0)
        date = row.get(date_col, 'N/A')
        
        print(f"\n   {idx}. {title}")
        print(f"      المصدر: {source}")
        print(f"      التاريخ: {date}")
        print(f"      الوصول: {reach:,.0f}")
        print(f"      الرابط: {url}")

# ============================================
# 10. قراءة ملفات Analytics
# ============================================
print("\n" + "=" * 80)
print("🔟 ملفات Analytics")
print("=" * 80)

if os.path.exists(analytics_path):
    analytics_files = os.listdir(analytics_path)
    print(f"\n📁 ملفات Analytics ({len(analytics_files)}):")
    for f in analytics_files:
        print(f"   - {f}")
    
    for f in analytics_files:
        if f.endswith('.csv'):
            filepath = os.path.join(analytics_path, f)
            try:
                adf = pd.read_csv(filepath)
                print(f"\n📊 {f}:")
                print(adf.head(15).to_string())
            except Exception as e:
                print(f"   ❌ خطأ: {e}")
else:
    print("⚠️ مجلد Analytics غير موجود")

# ============================================
# 11. قراءة ملفات Overview الإضافية
# ============================================
print("\n" + "=" * 80)
print("1️⃣1️⃣ ملفات Overview الإضافية")
print("=" * 80)

overview_files = os.listdir(overview_path)
for f in overview_files:
    if f.endswith('.csv') and any(x in f for x in ['Sentiment', 'Top_', 'Mentions']):
        filepath = os.path.join(overview_path, f)
        try:
            odf = pd.read_csv(filepath)
            print(f"\n📊 {f}:")
            print(odf.head(30).to_string())
        except Exception as e:
            print(f"   ❌ خطأ: {e}")

# ============================================
# ملخص نهائي
# ============================================
print("\n" + "=" * 80)
print("📋 الملخص النهائي")
print("=" * 80)

print(f"""
📊 الإحصائيات الرئيسية:
   - إجمالي السجلات: {len(df)}
   - الأخبار الإلكترونية: {len(news_df)}
   - وسائل التواصل: {len(df) - len(news_df)}

📈 المشاعر (الأخبار):
""")

if sentiment_col:
    for sent, count in news_df[sentiment_col].value_counts().items():
        pct = (count / len(news_df)) * 100
        print(f"   - {sent}: {count} ({pct:.1f}%)")

print("\n✅ اكتمل التحليل!")
