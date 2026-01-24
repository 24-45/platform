import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def master_granular_analysis():
    # 1. تعريف الهيكل التفصيلي (المسارات + المحاور الفرعية)
    structure = {
        "Track1_Ministry": {
            "keywords": ["وزارة", "ministry"],
            "sub_themes": {
                "قرارات وتصريحات": ["قرار", "تصريح", "مرسوم", "اعتماد", "توجيه", "وزير"],
                "مبادرات شبابية": ["مبادرة", "جيل مبادر", "تمكين", "رواد", "مركز الشباب", "سياسة الشباب"]
            },
            "context_filter": [] # لا يوجد فلتر استبعاد لهذا المسار
        },
        "Track2_GlobalEvents": {
            "keywords": ["الكبرى", "global", "events"],
            "sub_themes": {
                "كأس العرب 2025": ["كأس العرب", "arab cup"],
                "FIFA U-17": ["U-17", "ناشئين", "فيفا", "fifa"],
                "جائزة قطر F1": ["f1", "فورمولا", "formula", "لوسيل", "lusail"],
                "UFC Qatar": ["ufc", "فنون قتالية"],
                "World Padel": ["بادل", "padel"]
            },
            # الفلتر الصارم: يجب وجود كلمات تنظيمية واستبعاد الكلمات الفنية
            "context_filter": {
                "include": ["تنظيم", "استضافة", "تذاكر", "مرافق", "خدمات", "أمن", "سياحة", "فنادق", "hosting", "organization"],
                "exclude": ["أهداف", "تسجيل", "فوز", "خسارة", "score", "goal", "result", "تشكيلة"]
            }
        },
        "Track3_Heritage": {
            "keywords": ["التراثية", "heritage"],
            "sub_themes": {
                "مهرجان مرمي": ["مرمي", "marmi"],
                "موسم سيلين": ["سيلين", "sealine"],
                "لونجين هذاب": ["هذاب", "hathab"],
                "مركز مواتر": ["مواتر", "mawater"]
            },
            "context_filter": {
                "include": ["تراث", "هوية", "تنظيم", "نجاح", "جمهور"],
                "exclude": [] 
            }
        },
        "Track4_SportsForAll": {
            "keywords": ["الصحية", "المحلية", "community"],
            "sub_themes": {
                "تحدي الوكرة": ["الوكرة", "wakra challenge"],
                "دروب قطر": ["دروب", "duroob"],
                "ذيب ألترا": ["ذيب", "theeb"],
                "Night Criterium": ["criterium", "كريتيريوم"]
            },
            "context_filter": {
                "include": ["مشاركة", "مجتمع", "صحة", "تسجيل", "تنظيم"],
                "exclude": []
            }
        }
    }

    final_report = {}

    print("--- بدء التحليل التفصيلي الدقيق (Granular Analysis) ---")

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # قراءة الملف
                if file.endswith('.csv'):
                    try:
                        df = pd.read_csv(file_path, encoding='utf-16', sep='\t')
                    except:
                        df = pd.read_csv(file_path, encoding='utf-8-sig')
                elif file.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                else:
                    continue

                text_col = next((c for c in df.columns if c in ['Hit Sentence', 'Content', 'Text', 'Full Text']), None)
                if not text_col: continue

                # تحديد المسار الرئيسي
                current_track_key = None
                for t_key, t_data in structure.items():
                    if any(k in file_path.lower() or k in file.lower() for k in t_data["keywords"]):
                        current_track_key = t_key
                        break
                
                if not current_track_key: continue

                if current_track_key not in final_report:
                    final_report[current_track_key] = {sub: {"volume": 0, "sentiment": {"Positive": 0, "Negative": 0, "Neutral": 0}, "top_phrases": []} for sub in structure[current_track_key]["sub_themes"]}

                # --- الفلترة والتحليل ---
                config = structure[current_track_key]
                
                # 1. تطبيق فلتر الاستبعاد العام للمسار (مثلاً استبعاد الأهداف في المسار 2)
                if config["context_filter"] and "exclude" in config["context_filter"]:
                    exclude_pattern = '|'.join(config["context_filter"]["exclude"])
                    if exclude_pattern:
                        df = df[~df[text_col].astype(str).str.contains(exclude_pattern, case=False, na=False)]

                # 2. تطبيق فلتر الشمول (التنظيم والاستضافة)
                if config["context_filter"] and "include" in config["context_filter"]:
                    include_pattern = '|'.join(config["context_filter"]["include"])
                    if include_pattern:
                        # نحتفظ فقط بالصفوف التي تحتوي على كلمات التنظيم
                        # (ملاحظة: هذا قد يقلل العدد ولكنه يضمن الجودة)
                        pass # يمكن تفعيل هذا السطر لفلترة صارمة جداً: df = df[df[text_col].astype(str).str.contains(include_pattern, case=False, na=False)]

                # 3. توزيع البيانات على المحاور الفرعية
                for sub_name, sub_keywords in config["sub_themes"].items():
                    pattern = '|'.join(sub_keywords)
                    # البحث عن الكلمات الفرعية داخل النص
                    sub_df = df[df[text_col].astype(str).str.contains(pattern, case=False, na=False)]
                    
                    if not sub_df.empty:
                        # تسجيل الحجم
                        final_report[current_track_key][sub_name]["volume"] += len(sub_df)
                        
                        # تسجيل المشاعر
                        if 'Sentiment' in sub_df.columns:
                            s_counts = sub_df['Sentiment'].value_counts().to_dict()
                            for k, v in s_counts.items():
                                if k in final_report[current_track_key][sub_name]["sentiment"]:
                                    final_report[current_track_key][sub_name]["sentiment"][k] += v

                        # تسجيل عينة من النصوص (لتحليل المضمون لاحقاً)
                        sample_texts = sub_df[text_col].astype(str).head(3).tolist()
                        final_report[current_track_key][sub_name]["top_phrases"].extend(sample_texts)

            except Exception as e:
                continue

    return final_report

# تشغيل
granular_data = master_granular_analysis()
print(json.dumps(granular_data, indent=4, ensure_ascii=False))

# حفظ البيانات
output_path = "static/data/meltwater/Qatr/mys_qatar_granular_master.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(granular_data, f, indent=4, ensure_ascii=False)
print(f"\n✅ تم حفظ البيانات في: {output_path}")
