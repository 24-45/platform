import pandas as pd
import os
from collections import Counter

# مسار الملف الرئيسي
data_path = "static/data/meltwater/Qatr/الفعاليات التراثية والوطنية/Overview"
main_file = "_____authoralgannas_qa_OR_authormawaterqatar_OR_au - Jan 19, 2026 - 10 27 26 AM.csv"

file_path = os.path.join(data_path, main_file)

print("=" * 80)
print("تحليل بيانات الفعاليات التراثية والوطنية - Online News فقط")
print("=" * 80)

# قراءة الملف
try:
    df = pd.read_csv(file_path, sep='\t', encoding='utf-16-le', on_bad_lines='skip')
    print(f"\n✅ تم تحميل الملف بنجاح")
    print(f"📊 إجمالي السجلات في الملف: {len(df):,}")
    print(f"📋 الأعمدة: {list(df.columns)[:15]}...")
except Exception as e:
    print(f"❌ خطأ في قراءة الملف: {e}")
    exit()

# البحث عن عمود Source Type
source_type_col = None
for col in df.columns:
    if 'source' in col.lower() and 'type' in col.lower():
        source_type_col = col
        break
    elif 'type' in col.lower():
        source_type_col = col

print(f"\n📌 عمود نوع المصدر: {source_type_col}")

# عرض القيم الفريدة لنوع المصدر
if source_type_col:
    print(f"\n📊 أنواع المصادر المتاحة:")
    source_counts = df[source_type_col].value_counts()
    for source, count in source_counts.items():
        print(f"   - {source}: {count:,}")

# فلترة Online News فقط
print("\n" + "=" * 80)
print("🔍 فلترة: Online News فقط")
print("=" * 80)

# البحث عن online news
df_online = df[df[source_type_col].str.lower().str.contains('online news', na=False)]
print(f"\n✅ عدد سجلات Online News: {len(df_online):,}")

# البحث عن عمود Sentiment
sentiment_col = None
for col in df.columns:
    if 'sentiment' in col.lower():
        sentiment_col = col
        break

print(f"\n📌 عمود المشاعر: {sentiment_col}")

# تحليل المشاعر
print("\n" + "-" * 50)
print("📊 تحليل المشاعر (Sentiment Analysis)")
print("-" * 50)

if sentiment_col:
    sentiment_counts = df_online[sentiment_col].value_counts()
    total = len(df_online)
    for sentiment, count in sentiment_counts.items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"   {sentiment}: {count:,} ({percentage:.1f}%)")

# البحث عن عمود Source Name
source_name_col = None
for col in df.columns:
    if 'source' in col.lower() and 'name' in col.lower():
        source_name_col = col
        break

# تحليل المصادر
print("\n" + "-" * 50)
print("📰 أهم المصادر الإخبارية")
print("-" * 50)

if source_name_col:
    source_names = df_online[source_name_col].value_counts().head(15)
    for source, count in source_names.items():
        print(f"   {source}: {count}")

# البحث عن عمود Country
country_col = None
for col in df.columns:
    if 'country' in col.lower():
        country_col = col
        break

# تحليل الدول
print("\n" + "-" * 50)
print("🌍 التوزيع الجغرافي")
print("-" * 50)

if country_col:
    country_counts = df_online[country_col].value_counts().head(10)
    for country, count in country_counts.items():
        print(f"   {country}: {count}")

# البحث عن عمود Language
lang_col = None
for col in df.columns:
    if 'language' in col.lower():
        lang_col = col
        break

# تحليل اللغات
print("\n" + "-" * 50)
print("🗣️ اللغات")
print("-" * 50)

if lang_col:
    lang_counts = df_online[lang_col].value_counts()
    for lang, count in lang_counts.items():
        print(f"   {lang}: {count}")

# البحث عن عمود Reach
reach_col = None
for col in df.columns:
    if 'reach' in col.lower():
        reach_col = col
        break

# تحليل الوصول
print("\n" + "-" * 50)
print("📈 تحليل الوصول (Reach)")
print("-" * 50)

if reach_col:
    # تحويل إلى رقم
    df_online_copy = df_online.copy()
    df_online_copy[reach_col] = pd.to_numeric(df_online_copy[reach_col].astype(str).str.replace(',', ''), errors='coerce')
    total_reach = df_online_copy[reach_col].sum()
    avg_reach = df_online_copy[reach_col].mean()
    max_reach = df_online_copy[reach_col].max()
    print(f"   إجمالي الوصول: {total_reach:,.0f}")
    print(f"   متوسط الوصول: {avg_reach:,.0f}")
    print(f"   أعلى وصول: {max_reach:,.0f}")

# البحث عن عمود Date
date_col = None
for col in df.columns:
    if 'date' in col.lower():
        date_col = col
        break

# تحليل التاريخ
print("\n" + "-" * 50)
print("📅 الفترة الزمنية")
print("-" * 50)

# أول عمود عادة يكون التاريخ
first_col = df_online.columns[0]
print(f"   أول تاريخ: {df_online[first_col].min()}")
print(f"   آخر تاريخ: {df_online[first_col].max()}")

# تحليل الكلمات الرئيسية
print("\n" + "-" * 50)
print("🔑 الكلمات الرئيسية (من العناوين)")
print("-" * 50)

# البحث عن عمود العنوان
title_col = None
for col in df.columns:
    if 'title' in col.lower() or 'headline' in col.lower():
        title_col = col
        break

if title_col:
    # جمع الكلمات من العناوين
    keywords = ['مرمي', 'مهرجان', 'سيلين', 'Sealine', 'التراث', 'الصقور', 'هدد التحدي', 
                'الطلع', 'كتارا', 'Monster Jam', 'قطر', 'Qatar']
    for keyword in keywords:
        count = df_online[title_col].str.contains(keyword, na=False, case=False).sum()
        if count > 0:
            print(f"   {keyword}: {count}")

# ملخص نهائي
print("\n" + "=" * 80)
print("📋 ملخص التحليل النهائي")
print("=" * 80)
print(f"""
📊 إجمالي البيانات في الملف: {len(df):,} سجل
🔍 سجلات Online News: {len(df_online):,} سجل
📈 نسبة Online News: {(len(df_online)/len(df)*100):.1f}%

📝 تحليل المشاعر (Online News):
""")

if sentiment_col:
    for sentiment, count in df_online[sentiment_col].value_counts().items():
        percentage = (count / len(df_online)) * 100
        bar = "█" * int(percentage / 2)
        print(f"   {sentiment}: {count:,} ({percentage:.1f}%) {bar}")

print("\n✅ انتهى التحليل!")
