#!/usr/bin/env python3
"""
تحليل بيانات Meltwater - Qatr01
Data Engineer Analysis Script
"""

import pandas as pd
import glob
import os
import json
from collections import Counter
import re

# المسار الرئيسي للبيانات
BASE_PATH = "static/data/meltwater/Qatr01"

def find_all_csv_files(base_path):
    """البحث عن جميع ملفات CSV في المجلد وكل المجلدات الفرعية"""
    csv_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def load_and_merge_data(csv_files):
    """قراءة ودمج جميع ملفات CSV"""
    all_dfs = []
    file_info = []
    
    for file_path in csv_files:
        try:
            # تحديد نوع المصدر من المسار
            path_lower = file_path.lower()
            if '/x/' in path_lower:
                source_type = 'X Platform'
            elif '/الإعلام التقليدي/' in file_path:
                source_type = 'Traditional Media'
            else:
                # إذا لم يكن x فهو تقليدي
                source_type = 'Traditional Media'
            
            # تحديد الفئة
            if 'الفعاليات الكبرى' in file_path:
                category = 'Global Events'
            elif 'الفعاليات التراثية' in file_path:
                category = 'Heritage Events'
            elif 'الفعاليات الرياضية' in file_path:
                category = 'Sports Events'
            elif 'وزارة الرياضة' in file_path:
                category = 'Ministry'
            else:
                category = 'Other'
            
            # ملفات Meltwater تكون UTF-16 LE مع TAB كفاصل
            df = pd.read_csv(file_path, encoding='utf-16-le', sep='\t')
            
            if df is None or len(df) == 0:
                print(f"⚠️ Empty file: {os.path.basename(file_path)}")
                continue
                
            df['Source_Type'] = source_type
            df['Category'] = category
            df['Source_File'] = os.path.basename(file_path)
            
            all_dfs.append(df)
            file_info.append({
                'file': os.path.basename(file_path)[:50],
                'source_type': source_type,
                'category': category,
                'rows': len(df)
            })
            print(f"   ✅ {category} ({source_type}): {len(df)} records")
            
        except Exception as e:
            print(f"❌ Error: {os.path.basename(file_path)[:40]} - {e}")
    
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True)
        return merged_df, file_info
    return pd.DataFrame(), file_info

def clean_data(df):
    """تنظيف البيانات"""
    original_count = len(df)
    
    # البحث عن عمود Document ID
    id_cols = [col for col in df.columns if 'document' in col.lower() or 'id' in col.lower()]
    if id_cols:
        df = df.drop_duplicates(subset=[id_cols[0]])
    
    # تنظيف التواريخ
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except:
            pass
    
    cleaned_count = len(df)
    
    return df, original_count, cleaned_count

def analyze_sentiment(df):
    """تحليل المشاعر"""
    sentiment_col = None
    for col in df.columns:
        if 'sentiment' in col.lower():
            sentiment_col = col
            break
    
    if sentiment_col:
        sentiment_counts = df[sentiment_col].value_counts().to_dict()
        return sentiment_counts
    return {"No Sentiment Column": "Not Found"}

def get_top_influencers(df, top_n=5):
    """استخراج أبرز المؤثرين"""
    # استخدام الأعمدة الصحيحة من Meltwater
    author_col = 'Author Name' if 'Author Name' in df.columns else None
    handle_col = 'Author Handle' if 'Author Handle' in df.columns else None
    reach_col = 'Reach' if 'Reach' in df.columns else None
    engagement_col = 'Engagement' if 'Engagement' in df.columns else None
    
    if not author_col:
        return []
    
    # تنظيف البيانات - إزالة القيم الفارغة
    df_clean = df[df[author_col].notna() & (df[author_col] != '')].copy()
    
    # تجميع حسب المؤلف
    agg_dict = {author_col: 'count'}
    if reach_col:
        agg_dict[reach_col] = 'sum'
    if engagement_col:
        agg_dict[engagement_col] = 'sum'
    
    influencers = df_clean.groupby(author_col).agg(agg_dict)
    influencers = influencers.rename(columns={author_col: 'posts'})
    
    # ترتيب حسب الوصول أو التفاعل أو عدد المنشورات
    if reach_col and reach_col in influencers.columns:
        influencers = influencers.sort_values(reach_col, ascending=False)
    elif engagement_col and engagement_col in influencers.columns:
        influencers = influencers.sort_values(engagement_col, ascending=False)
    else:
        influencers = influencers.sort_values('posts', ascending=False)
    
    result = []
    for idx, row in influencers.head(top_n).iterrows():
        item = {
            "name": str(idx),
            "posts": int(row['posts'])
        }
        if reach_col and reach_col in row.index:
            item["reach"] = int(row[reach_col]) if pd.notna(row[reach_col]) else 0
        if engagement_col and engagement_col in row.index:
            item["engagement"] = int(row[engagement_col]) if pd.notna(row[engagement_col]) else 0
        result.append(item)
    
    return result

def get_top_engaged_posts(df, top_n=3):
    """استخراج أعلى المنشورات تفاعلاً"""
    # استخدام الأعمدة الصحيحة من Meltwater
    engagement_col = 'Engagement' if 'Engagement' in df.columns else None
    title_col = 'Title' if 'Title' in df.columns else None
    content_col = 'Opening Text' if 'Opening Text' in df.columns else None
    author_col = 'Author Name' if 'Author Name' in df.columns else None
    url_col = 'URL' if 'URL' in df.columns else None
    
    result = []
    
    if engagement_col:
        # تحويل Engagement لأرقام
        df_sorted = df.copy()
        df_sorted[engagement_col] = pd.to_numeric(df_sorted[engagement_col], errors='coerce')
        df_sorted = df_sorted.dropna(subset=[engagement_col])
        df_sorted = df_sorted.nlargest(top_n, engagement_col)
        
        for idx, row in df_sorted.iterrows():
            # استخدام العنوان أو المحتوى
            title = str(row[title_col])[:150] if title_col and pd.notna(row[title_col]) else ""
            content = str(row[content_col])[:200] if content_col and pd.notna(row[content_col]) else ""
            
            # اختيار النص الأفضل
            text = title if title and title != "News Article" else content
            if not text or text == "nan":
                text = "منشور بدون عنوان"
            
            item = {
                "title": text,
                "engagement": int(row[engagement_col]),
                "source_type": row.get('Source_Type', 'Unknown'),
                "category": row.get('Category', 'Unknown')
            }
            if author_col and pd.notna(row.get(author_col)):
                item["author"] = str(row[author_col])
            if url_col and pd.notna(row.get(url_col)):
                item["url"] = str(row[url_col])[:100]
            
            result.append(item)
    
    return result

def extract_hashtags(df, top_n=5):
    """استخراج أكثر الهاشتاقات استخداماً"""
    hashtags = []
    
    # البحث في جميع الأعمدة النصية
    for col in df.columns:
        if df[col].dtype == 'object':
            for text in df[col].dropna().astype(str):
                found = re.findall(r'#(\w+)', text)
                hashtags.extend(found)
    
    if hashtags:
        hashtag_counts = Counter(hashtags).most_common(top_n)
        return [{"hashtag": f"#{tag}", "count": count} for tag, count in hashtag_counts]
    
    return []

def get_volume_by_source(df):
    """حجم المحتوى حسب المصدر"""
    if 'Source_Type' in df.columns:
        return df['Source_Type'].value_counts().to_dict()
    return {}

def get_volume_by_category(df):
    """حجم المحتوى حسب الفئة"""
    if 'Category' in df.columns:
        return df['Category'].value_counts().to_dict()
    return {}

def get_weekly_trends(df):
    """اتجاهات أسبوعية"""
    date_col = None
    for col in df.columns:
        if 'date' in col.lower():
            date_col = col
            break
    
    if date_col:
        try:
            df['Week'] = pd.to_datetime(df[date_col], errors='coerce').dt.isocalendar().week
            weekly = df.groupby(['Week', 'Source_Type']).size().unstack(fill_value=0)
            return weekly.to_dict()
        except:
            pass
    return {}

def main():
    print("=" * 60)
    print("🔍 تحليل بيانات Meltwater - Qatr01")
    print("=" * 60)
    
    # 1. البحث عن الملفات
    print("\n📂 البحث عن ملفات CSV...")
    csv_files = find_all_csv_files(BASE_PATH)
    print(f"   تم العثور على {len(csv_files)} ملفات")
    
    # 2. قراءة ودمج البيانات
    print("\n📊 قراءة ودمج البيانات...")
    df, file_info = load_and_merge_data(csv_files)
    
    if df.empty:
        print("❌ لم يتم العثور على بيانات!")
        return
    
    print(f"   إجمالي السجلات: {len(df)}")
    print(f"   الأعمدة: {list(df.columns)}")
    
    # 3. تنظيف البيانات
    print("\n🧹 تنظيف البيانات...")
    df, original, cleaned = clean_data(df)
    print(f"   قبل التنظيف: {original}")
    print(f"   بعد التنظيف: {cleaned}")
    print(f"   تم إزالة: {original - cleaned} مكررات")
    
    # 4. استخراج المؤشرات
    print("\n📈 استخراج المؤشرات الرئيسية...")
    
    results = {
        "summary": {
            "total_records": cleaned,
            "files_processed": len(csv_files),
            "duplicates_removed": original - cleaned
        },
        "volume_by_source": get_volume_by_source(df),
        "volume_by_category": get_volume_by_category(df),
        "sentiment_analysis": analyze_sentiment(df),
        "top_influencers_traditional": get_top_influencers(df[df['Source_Type'] == 'Traditional Media'], 5),
        "top_influencers_x": get_top_influencers(df[df['Source_Type'] == 'X Platform'], 5),
        "top_engaged_posts": get_top_engaged_posts(df, 5),
        "top_hashtags": extract_hashtags(df, 10),
        "files_info": file_info
    }
    
    # 5. طباعة النتائج
    print("\n" + "=" * 60)
    print("📋 النتائج النهائية (JSON)")
    print("=" * 60)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    # حفظ النتائج
    output_file = "qatr01_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ تم حفظ النتائج في: {output_file}")
    
    return results

if __name__ == "__main__":
    main()
