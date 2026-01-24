import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def deep_track_analysis():
    # المحاور التي سنقيس بها عمق كل مسار
    themes = {
        "Organization": ["تنظيم", "نجاح", "استضافة", "مرافق"],
        "Identity": ["تراث", "هوية", "وطني", "إرث"],
        "Youth": ["شباب", "تمكين", "مبادرة"],
        "Tourism": ["سياحة", "فنادق", "جماهير"]
    }
    
    mapping = {
        "Track1_Ministry": ["وزارة", "ministry"],
        "Track2_GlobalEvents": ["الكبرى", "global"],
        "Track3_Heritage": ["التراثية", "heritage"],
        "Track4_Community": ["الصحية", "المحلية"]
    }

    detailed_results = {}

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(('.csv', '.xlsx')):
                try:
                    df = pd.read_csv(os.path.join(root, file), encoding='utf-16', sep='\t') if file.endswith('.csv') else pd.read_excel(os.path.join(root, file))
                    
                    # تحديد المسار
                    current_track = "Other"
                    for track, keywords in mapping.items():
                        if any(k in root.lower() or k in file.lower() for k in keywords):
                            current_track = track
                            break
                    
                    if current_track not in detailed_results:
                        detailed_results[current_track] = {"volume": 0, "top_theme": "", "themes_count": {t: 0 for t in themes}}

                    text_col = next((c for c in df.columns if c in ['Hit Sentence', 'Content']), None)
                    if text_col:
                        full_text = " ".join(df[text_col].astype(str).tolist())
                        detailed_results[current_track]["volume"] += len(df)
                        for theme, keywords in themes.items():
                            count = sum(full_text.count(k) for k in keywords)
                            detailed_results[current_track]["themes_count"][theme] += count
                except: continue

    return detailed_results

# تشغيل التحليل العميق
final_deep_analysis = deep_track_analysis()
print(json.dumps(final_deep_analysis, indent=4, ensure_ascii=False))
