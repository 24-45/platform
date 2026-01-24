import pandas as pd
import os
import json

# تحديد المسار الذي ذكرته
BASE_PATH = "static/data/meltwater/Qatr"

# تعريف المسارات الأربعة بناءً على طلبك
tracks_config = {
    "Track1_Ministry": "وزارة الرياضة والشباب القطرية",
    "Track2_GlobalEvents": "الفعاليات الكبرى",
    "Track3_Heritage": "الفعاليات التراثية والوطنية",
    "Track4_Community": "الفعاليات الرياضية الصحية المحلية"
}

# كلمات الفلترة لاستبعاد المحتوى الرياضي الفني في المسار الثاني
exclude_words = ['أهداف', 'تسجيل', 'نتيجة المباراة', 'فوز الفريق', 'خسارة', 'تشكيلة', 'المدرب', 'ركلة جزاء']

def analyze_folder(folder_path, is_global=False):
    all_data = []
    
    # التأكد من وجود المجلد
    if not os.path.exists(folder_path):
        return {"error": f"المسار غير موجود: {folder_path}"}

    # قراءة كل ملفات الاكسل داخل المجلد
    for file in os.listdir(folder_path):
        if file.endswith(('.xlsx', '.xls')):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_excel(file_path)
                # تحديد المصدر (منصة اكس أو إعلام)
                if 'x' in file.lower() or 'twitter' in file.lower():
                    df['source_group'] = 'X'
                else:
                    df['source_group'] = 'News'
                all_data.append(df)
            except Exception as e:
                print(f"خطأ في قراءة الملف {file}: {e}")

    if not all_data:
        return {"status": "لا توجد بيانات"}

    combined_df = pd.concat(all_data, ignore_index=True)

    # تطبيق فلتر الاستبعاد للمسار الثاني (الفعاليات الكبرى)
    if is_global:
        # البحث عن عمود النص (Meltwater عادة يستخدم 'Hit Sentence' أو 'Content')
        text_col = next((c for c in combined_df.columns if c in ['Hit Sentence', 'Content', 'Text']), None)
        if text_col:
            combined_df = combined_df[~combined_df[text_col].astype(str).str.contains('|'.join(exclude_words), na=False)]

    # حساب الأرقام النهائية
    summary = {
        "total_volume": len(combined_df),
        "news_volume": len(combined_df[combined_df['source_group'] == 'News']),
        "x_volume": len(combined_df[combined_df['source_group'] == 'X']),
        "sentiment": combined_df['Sentiment'].value_counts().to_dict() if 'Sentiment' in combined_df.columns else "N/A"
    }
    return summary

# التنفيذ
final_results = {}
for track_id, folder_name in tracks_config.items():
    full_path = os.path.join(BASE_PATH, folder_name)
    print(f"جاري تحليل: {folder_name}...")
    is_global = (track_id == "Track2_GlobalEvents")
    final_results[folder_name] = analyze_folder(full_path, is_global)

# طباعة النتيجة النهائية بشكل جميل لنسخها
print("\n" + "="*30)
print("النتيجة الجاهزة للتحليل:")
print("="*30)
print(json.dumps(final_results, indent=4, ensure_ascii=False))
