import pandas as pd
import os
import json

BASE_PATH = "static/data/meltwater/Qatr"

def deep_semantic_understanding():
    # تعريف "القواميس الاستراتيجية" لفهم المعنى وليس فقط الكلمة
    logic_map = {
        "Strategic_Excellence": ["ريادة", "تميز", "احترافية", "بنية تحتية", "نجاح باهر", "استضافة استثنائية"],
        "National_Pride": ["فخر", "اعتزاز", "هوية قطرية", "موروث", "أجيال", "الأصالة"],
        "Economic_Impact": ["سياحة", "زوار", "إشغال", "جذب", "عالمي", "وجهة"],
        "Youth_Engagement": ["تمكين", "إشراك", "تطوع", "طاقة شبابية", "فرصة"]
    }

    detailed_insights = {}

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # القراءة بترميز Meltwater الصحيح
                df = pd.read_csv(file_path, encoding='utf-16', sep='\t') if file.endswith('.csv') else pd.read_excel(file_path)
                
                # البحث عن العمود الذي يحتوي على "النص الكامل"
                text_col = next((c for c in df.columns if c in ['Hit Sentence', 'Content', 'Text']), None)
                if not text_col: continue

                # تحديد المسار
                current_track = "Other"
                if "Track1" in root or "وزارة" in file: current_track = "Track1_Ministry"
                elif "Track2" in root or "الكبرى" in file: current_track = "Track2_GlobalEvents"
                elif "Track3" in root or "التراثية" in file: current_track = "Track3_Heritage"
                elif "Track4" in root or "المحلية" in file: current_track = "Track4_Community"

                if current_track not in detailed_insights:
                    detailed_insights[current_track] = {"logic_analysis": {k: [] for k in logic_map}}

                # إجبار الكود على "فهم" الجمل
                # نأخذ عينة من أكثر الجمل تأثيراً (عالية الوصول) لتحليل منطقها
                if 'Reach' in df.columns:
                    df = df.sort_values(by='Reach', ascending=False)
                
                top_sentences = df[text_col].astype(str).head(100).tolist()
                
                for sentence in top_sentences:
                    for logic_key, keywords in logic_map.items():
                        if any(k in sentence for k in keywords):
                            # حفظ الجملة كدليل منطقي
                            if len(detailed_insights[current_track]["logic_analysis"][logic_key]) < 5:
                                detailed_insights[current_track]["logic_analysis"][logic_key].append(sentence[:200])

            except: continue

    return detailed_insights

# تشغيل الفهم العميق
insights_logic = deep_semantic_understanding()
print(json.dumps(insights_logic, indent=4, ensure_ascii=False))

# حفظ البيانات
output_path = "static/data/meltwater/Qatr/mys_qatar_semantic.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(insights_logic, f, indent=4, ensure_ascii=False)
print(f"\n✅ تم حفظ البيانات في: {output_path}")
