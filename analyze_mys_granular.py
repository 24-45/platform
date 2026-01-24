import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def granular_strategic_analysis():
    # تعريف المكونات التفصيلية لكل مسار
    sub_tracks = {
        "Track1_Ministry": ["قرارات", "تصريحات", "مبادرات", "تمكين", "وزير", "الشباب"],
        "Track2_GlobalEvents": ["كأس العرب", "FIFA", "F1", "UFC", "Padel", "جائزة قطر", "بادل", "فورمولا"],
        "Track3_Heritage": ["مرمي", "سيلين", "هذاب", "مواتر", "نومس", "تراث", "القناص"],
        "Track4_Community": ["الوكرة", "دروب قطر", "ذيب", "Criterium", "الرياضة للجميع", "تحدي"]
    }
    
    # الكلمات المفتاحية لتصنيف المسارات
    mapping = {
        "Track1_Ministry": ["وزارة", "ministry"],
        "Track2_GlobalEvents": ["الكبرى", "global", "كأس"],
        "Track3_Heritage": ["التراثية", "heritage", "algannas", "mawat"],
        "Track4_Community": ["الصحية", "المحلية", "community", "تحدي", "wakra"]
    }

    results = {track: {sub: {"volume": 0} for sub in subs} for track, subs in sub_tracks.items()}

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # قراءة الملفات
                if file.endswith('.csv'):
                    df = pd.read_csv(file_path, encoding='utf-16', sep='\t')
                elif file.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file_path)
                else:
                    continue

                # تحديد المسار الأب بناءً على الكلمات المفتاحية
                parent_track = None
                for track, keywords in mapping.items():
                    if any(k in root.lower() or k in file.lower() for k in keywords):
                        parent_track = track
                        break
                
                if parent_track is None:
                    continue

                # تحليل المضمون الداخلي
                text_col = next((c for c in df.columns if c in ['Hit Sentence', 'Content']), None)
                if text_col:
                    content_chunk = " ".join(df[text_col].astype(str).tolist())
                    
                    for sub_item in sub_tracks[parent_track]:
                        # عد المرات التي ذكر فيها اسم الفعالية أو المبادرة
                        mention_count = content_chunk.lower().count(sub_item.lower())
                        results[parent_track][sub_item]["volume"] += mention_count
                        
            except: continue

    return results

# تنفيذ التحليل
detailed_insights = granular_strategic_analysis()
print("\n" + "="*50)
print("تحليل المكونات التفصيلية (Inside Each Track):")
print(json.dumps(detailed_insights, indent=4, ensure_ascii=False))
