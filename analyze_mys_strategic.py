import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def strategic_questions_analyzer():
    report_structure = {}
    
    mapping = {
        "Track1_Ministry": ["وزارة", "ministry"],
        "Track2_GlobalEvents": ["الكبرى", "global"],
        "Track3_Heritage": ["التراثية", "heritage"],
        "Track4_Community": ["الصحية", "المحلية"]
    }

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # 1. القراءة مع دعم التوقيت والمشاعر
                df = pd.read_csv(file_path, encoding='utf-16', sep='\t') if file.endswith('.csv') else pd.read_excel(file_path)
                
                # توحيد التواريخ
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])

                # تحديد المسار
                track_name = "Other"
                for t, keywords in mapping.items():
                    if any(k in file_path.lower() or k in file.lower() for k in keywords):
                        track_name = t
                        break
                
                if track_name not in report_structure:
                    report_structure[track_name] = {
                        "volume": 0,
                        "timeline": {},
                        "sentiment": {"Positive": 0, "Neutral": 0, "Negative": 0},
                        "top_influencers": [],
                        "media_type": {"Traditional": 0, "Social": 0}
                    }

                # أ. ملامح الاهتمام (حجم التغطية)
                count = len(df)
                report_structure[track_name]["volume"] += count

                # ب. التغير الزمني (تحليل السلاسل الزمنية)
                if 'Date' in df.columns:
                    daily_counts = df.set_index('Date').resample('W').size().to_dict()
                    for date, val in daily_counts.items():
                        date_str = date.strftime('%Y-%m-%d')
                        report_structure[track_name]["timeline"][date_str] = report_structure[track_name]["timeline"].get(date_str, 0) + val

                # ج. اتجاهات الإعلام (إيجابي/سلبي/محايد)
                if 'Sentiment' in df.columns:
                    s_counts = df['Sentiment'].value_counts().to_dict()
                    for s_type, s_val in s_counts.items():
                        if s_type in report_structure[track_name]["sentiment"]:
                            report_structure[track_name]["sentiment"][s_type] += s_val

                # د. ملامح الاهتمام في التواصل والمؤثرين
                if 'Source Name' in df.columns and 'Reach' in df.columns:
                    influencers = df.nlargest(5, 'Reach')[['Source Name', 'Reach']].to_dict('records')
                    report_structure[track_name]["top_influencers"].extend(influencers)

                # هـ. تصنيف (تقليدي vs تواصل)
                is_social = any(k in file.lower() for k in ['x', 'twitter', 'social'])
                type_key = "Social" if is_social else "Traditional"
                report_structure[track_name]["media_type"][type_key] += count

            except: continue

    return report_structure

# تنفيذ التحليل الاستراتيجي
strategic_data = strategic_questions_analyzer()
print(json.dumps(strategic_data, indent=4, ensure_ascii=False))

# حفظ البيانات
output_path = "static/data/meltwater/Qatr/mys_qatar_strategic.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(strategic_data, f, indent=4, ensure_ascii=False)
print(f"\n✅ تم حفظ البيانات في: {output_path}")
