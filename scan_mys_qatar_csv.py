import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def fix_x_detection():
    final_stats = {}
    
    # الكلمات المفتاحية لتصنيف المسارات (حسب تنظيمك للمجلدات)
    mapping = {
        "Track1_Ministry": ["وزارة", "ministry"],
        "Track2_GlobalEvents": ["الكبرى", "global", "events"],
        "Track3_Heritage": ["التراثية", "heritage", "nomas", "algannas"],
        "Track4_Community": ["الصحية", "المحلية", "community"]
    }

    print("--- بدأنا عملية البحث المعمق عن ملفات X والأخبار ---")

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(('.csv', '.xlsx')):
                file_path = os.path.join(root, file)
                try:
                    # محاولة قراءة الملف بترميزات Meltwater المختلفة
                    if file.endswith('.csv'):
                        try:
                            df = pd.read_csv(file_path, encoding='utf-16', sep='\t')
                        except:
                            df = pd.read_csv(file_path, encoding='utf-8-sig')
                    else:
                        df = pd.read_excel(file_path)

                    if df is not None:
                        # 1. تحديد المسار بناءً على مكان الملف
                        category = "عام"
                        for key, keywords in mapping.items():
                            if any(k in file_path.lower() or k in file.lower() for k in keywords):
                                category = key
                                break
                        
                        if category not in final_stats:
                            final_stats[category] = {"news": 0, "x": 0, "total": 0, "reach": 0}

                        # 2. كشف هل هو ملف X؟ (بالنظر داخل عمود Source Type)
                        is_x = False
                        if 'Source Type' in df.columns:
                            if df['Source Type'].str.contains('Twitter|Social', case=False, na=False).any():
                                is_x = True
                        
                        # 3. تسجيل الأرقام وفهم المضمون
                        count = len(df)
                        if is_x:
                            final_stats[category]["x"] += count
                            if 'Reach' in df.columns:
                                final_stats[category]["reach"] += pd.to_numeric(df['Reach'], errors='coerce').sum()
                        else:
                            final_stats[category]["news"] += count
                        
                        final_stats[category]["total"] += count
                        print(f"✅ تم اكتشاف وقراءة: {file} | المسار: {category} | النوع: {'X' if is_x else 'News'}")

                except Exception as e:
                    continue

    return final_stats

# تشغيل
results = fix_x_detection()
print("\n" + "="*40)
print("النتائج النهائية (بما في ذلك X):")
print(json.dumps(results, indent=4, ensure_ascii=False))
