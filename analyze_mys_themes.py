import pandas as pd
import os

BASE_PATH = "static/data/meltwater/Qatr"

def strategic_content_analysis():
    # المحاور الاستراتيجية التي تهم صاحب القرار في قطر
    themes = {
        "كفاءة التنظيم والاستضافة": ["تنظيم", "نجاح", "استضافة", "مرافق", "ملاعب", "سلاسة", "Hosting", "Organization"],
        "تعزيز الهوية والإرث": ["تراث", "هوية", "وطني", "إرث", "مرمي", "سيلين", "Heritage", "Identity"],
        "تمكين الشباب والمشاركة": ["شباب", "مبادرة", "تمكين", "مشاركة", "Youth", "Empowerment"],
        "الوجهة السياحية والرياضية": ["سياحة", "فنادق", "جمهور", "مشجعين", "Tourism", "Fans"]
    }

    results_summary = {}

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(('.csv', '.xlsx')):
                try:
                    df = pd.read_csv(os.path.join(root, file), encoding='utf-16', sep='\t') if file.endswith('.csv') else pd.read_excel(os.path.join(root, file))
                    text_col = next((c for c in df.columns if c in ['Hit Sentence', 'Content']), None)
                    
                    if text_col:
                        full_text = " ".join(df[text_col].astype(str).tolist())
                        for theme, keywords in themes.items():
                            count = sum(full_text.count(k) for k in keywords)
                            results_summary[theme] = results_summary.get(theme, 0) + count
                except: continue

    print("\n" + "="*40)
    print("نتائج تحليل المضمون (Thematic Analysis):")
    for theme, val in results_summary.items():
        print(f"📌 {theme}: تم رصد {val} دلالة إعلامية")
    print("="*40)

strategic_content_analysis()
