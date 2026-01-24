import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def ultra_detailed_analysis():
    # تعريف الفعاليات الدقيقة لكل مسار للبحث عنها داخل النصوص
    sub_events = {
        "Track1_Ministry": ["قرارات", "تصريحات", "مبادرات شبابية", "تمكين", "وزير الرياضة"],
        "Track2_GlobalEvents": ["كأس العرب", "FIFA U-17", "F1", "UFC", "Padel", "جائزة قطر"],
        "Track3_Heritage": ["مرمي", "سيلين", "هذاب", "مواتر", "نومس", "الشقب"],
        "Track4_Community": ["الوكرة", "دروب قطر", "ذيب ألترا", "Criterium", "الرياضة للجميع"]
    }

    # المحاور التحليلية التي سنقيس بها "نوعية" الكلام
    themes = {
        "Strategic_Value": ["تنظيم", "نجاح", "استضافة", "احترافية", "بنية تحتية"],
        "Cultural_Value": ["هوية", "تراث", "عادات", "فخر", "إرث"],
        "Impact_Value": ["مشاركة", "تفاعل", "حضور جماهيري", "سياحة", "وصول"]
    }
    
    # الكلمات المفتاحية لتصنيف المسارات
    mapping = {
        "Track1_Ministry": ["وزارة", "ministry"],
        "Track2_GlobalEvents": ["الكبرى", "global", "كأس"],
        "Track3_Heritage": ["التراثية", "heritage", "algannas", "mawat"],
        "Track4_Community": ["الصحية", "المحلية", "community", "تحدي", "wakra"]
    }

    final_report = {}

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # القراءة الذكية
                if file.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding='utf-16', sep='\t')
                elif file.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                else:
                    continue
                
                # ربط الملف بالمسار الصحيح
                parent_track = None
                for track, keywords in mapping.items():
                    if any(k in root.lower() or k in file.lower() for k in keywords):
                        parent_track = track
                        break
                
                if parent_track is None: continue
                if parent_track not in final_report: final_report[parent_track] = {}

                text_col = next((c for c in df.columns if c in ['Hit Sentence', 'Content']), None)
                if text_col:
                    for event in sub_events[parent_track]:
                        # البحث عن النصوص التي ذكرت الفعالية تحديداً
                        mask = df[text_col].astype(str).str.contains(event, case=False, na=False)
                        event_data = df[mask]
                        
                        if not event_data.empty:
                            if event not in final_report[parent_track]:
                                final_report[parent_track][event] = {"volume": 0, "themes": {t: 0 for t in themes}}
                            
                            final_report[parent_track][event]["volume"] += len(event_data)
                            
                            # تحليل المضمون داخل هذه الفعالية
                            event_text = " ".join(event_data[text_col].astype(str).tolist())
                            for t_name, keywords in themes.items():
                                count = sum(event_text.count(k) for k in keywords)
                                final_report[parent_track][event]["themes"][t_name] += count
            except: continue

    return final_report

# تشغيل التنقيب
detailed_data = ultra_detailed_analysis()
print(json.dumps(detailed_data, indent=4, ensure_ascii=False))

# حفظ البيانات في ملف JSON
output_path = "static/data/meltwater/Qatr/mys_qatar_analysis.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(detailed_data, f, indent=4, ensure_ascii=False)
print(f"\n✅ تم حفظ البيانات في: {output_path}")
