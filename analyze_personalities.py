#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحليل المؤثرين في الصورة الإعلامية - الفعاليات الكبرى
البحث عن الشخصيات المذكورة في الأخبار (رسمية، رياضية، إعلامية)
منهجية صارمة: البحث في Title و Hit Sentence
"""

import pandas as pd
import re
from collections import Counter

# قراءة البيانات
csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"

df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# فلترة الإعلام التقليدي (online news)
traditional_df = df[df['Source Type'] == 'online news'].copy()
print(f"إجمالي الأخبار (الإعلام التقليدي): {len(traditional_df)}")

# ===== تعريف الشخصيات المؤثرة =====

# 1. الشخصيات الرسمية القطرية
qatari_officials = {
    'الشيخ تميم بن حمد': r'تميم بن حمد|الأمير تميم|أمير قطر|Sheikh Tamim|Emir of Qatar|تميم',
    'الشيخ جوعان بن حمد': r'جوعان بن حمد|الشيخ جوعان|Sheikh Joaan|جوعان',
    'الشيخ حمد بن خليفة': r'حمد بن خليفة بن أحمد|Sheikh Hamad bin Khalifa bin Ahmad',
    'الشيخ محمد بن حمد': r'محمد بن حمد آل ثاني|الشيخ محمد بن حمد',
    'ياسر الجمال': r'ياسر.*الجمال|ياسر بن عبدالله|Yasser Al-Jamal',
    'فواز المسيفري': r'فواز.*المسيفري|Fawaz Al-Mseifri',
    'راشد النعيمي': r'راشد.*النعيمي|Rashid Al-Nuaimi',
}

# 2. شخصيات FIFA والاتحادات
fifa_officials = {
    'جياني إنفانتينو': r'إنفانتينو|انفانتينو|Infantino|رئيس الفيفا|FIFA President',
    'FIFA': r'FIFA|الفيفا|الاتحاد الدولي',
    'AFC': r'AFC|الاتحاد الآسيوي|Asian Football',
}

# 3. الشخصيات الرياضية (لاعبون ومدربون)
sports_personalities = {
    'أكرم عفيف': r'أكرم عفيف|Akram Afif',
    'المعز علي': r'المعز علي|Almoez Ali',
    'سعد الشيب': r'سعد الشيب|Saad Al-Sheeb',
    'حسن الهيدوس': r'حسن الهيدوس|Hassan Al-Haydos',
    'كارلوس كيروش': r'كيروش|Queiroz|كارلوس كيروش',
    'تيناتي': r'تيناتي|Tinatin|ماركيز لوبيز',
    'ماكس فيرستابن': r'فيرستابن|Verstappen|ماكس',
    'لويس هاميلتون': r'هاميلتون|Hamilton|لويس',
    'رافا نادال': r'نادال|Nadal|رافا',
}

# 4. وسائل الإعلام والقنوات
media_entities = {
    'beIN Sports': r'beIN|بي إن|بين سبورت|bein',
    'الكأس': r'الكأس|alkass|Al Kass',
    'الجزيرة': r'الجزيرة|Al Jazeera|Aljazeera',
    'العربية': r'العربية|Al Arabiya',
    'Sky Sports': r'Sky Sports|سكاي',
    'ESPN': r'ESPN',
}

# دالة للبحث عن شخصية في النص
def search_personality(df, name, pattern):
    matches = df[
        df['Title'].str.contains(pattern, case=False, na=False, regex=True) |
        df['Hit Sentence'].str.contains(pattern, case=False, na=False, regex=True)
    ]
    return len(matches)

# دالة لتحليل النبرة للشخصية
def analyze_sentiment_for_personality(df, pattern):
    matches = df[
        df['Title'].str.contains(pattern, case=False, na=False, regex=True) |
        df['Hit Sentence'].str.contains(pattern, case=False, na=False, regex=True)
    ]
    if len(matches) == 0:
        return {'total': 0, 'positive': 0, 'neutral': 0, 'negative': 0}
    
    sentiments = matches['Sentiment'].value_counts()
    return {
        'total': len(matches),
        'positive': sentiments.get('Positive', 0),
        'neutral': sentiments.get('Neutral', 0),
        'negative': sentiments.get('Negative', 0)
    }

print("\n" + "="*80)
print("🏛️ الشخصيات الرسمية القطرية")
print("="*80)

qatari_results = {}
for name, pattern in qatari_officials.items():
    result = analyze_sentiment_for_personality(traditional_df, pattern)
    if result['total'] > 0:
        qatari_results[name] = result
        pos_pct = (result['positive'] / result['total'] * 100) if result['total'] > 0 else 0
        neu_pct = (result['neutral'] / result['total'] * 100) if result['total'] > 0 else 0
        neg_pct = (result['negative'] / result['total'] * 100) if result['total'] > 0 else 0
        print(f"\n📌 {name}: {result['total']} ظهور")
        print(f"    إيجابي: {result['positive']} ({pos_pct:.1f}%)")
        print(f"    محايد: {result['neutral']} ({neu_pct:.1f}%)")
        print(f"    سلبي: {result['negative']} ({neg_pct:.1f}%)")

print("\n" + "="*80)
print("⚽ FIFA والاتحادات الدولية")
print("="*80)

fifa_results = {}
for name, pattern in fifa_officials.items():
    result = analyze_sentiment_for_personality(traditional_df, pattern)
    if result['total'] > 0:
        fifa_results[name] = result
        pos_pct = (result['positive'] / result['total'] * 100) if result['total'] > 0 else 0
        print(f"\n📌 {name}: {result['total']} ظهور (إيجابي: {pos_pct:.1f}%)")

print("\n" + "="*80)
print("🌟 الشخصيات الرياضية (لاعبون ومدربون)")
print("="*80)

sports_results = {}
for name, pattern in sports_personalities.items():
    result = analyze_sentiment_for_personality(traditional_df, pattern)
    if result['total'] > 0:
        sports_results[name] = result
        print(f"📌 {name}: {result['total']} ظهور")

print("\n" + "="*80)
print("📺 وسائل الإعلام والقنوات")
print("="*80)

media_results = {}
for name, pattern in media_entities.items():
    result = analyze_sentiment_for_personality(traditional_df, pattern)
    if result['total'] > 0:
        media_results[name] = result
        print(f"📌 {name}: {result['total']} ظهور")

# ===== تحليل Keyphrases للبحث عن أسماء إضافية =====
print("\n" + "="*80)
print("🔍 تحليل الأسماء الأكثر تكراراً في Keyphrases")
print("="*80)

if 'Keyphrases' in traditional_df.columns:
    all_phrases = []
    for phrases in traditional_df['Keyphrases'].dropna():
        if isinstance(phrases, str):
            for phrase in phrases.split(','):
                phrase = phrase.strip()
                # البحث عن عبارات تبدو كأسماء (تحتوي على كلمتين أو أكثر)
                if phrase and len(phrase) > 3:
                    all_phrases.append(phrase)
    
    phrase_counts = Counter(all_phrases)
    print("\nأكثر 30 عبارة تكراراً (قد تحتوي أسماء):")
    for phrase, count in phrase_counts.most_common(30):
        if count >= 5:
            print(f"  - {phrase}: {count}")

# ===== البحث في عمود Author Name =====
print("\n" + "="*80)
print("✍️ الكُتّاب الأكثر تأثيراً")
print("="*80)

author_counts = traditional_df['Author Name'].dropna().value_counts().head(15)
for author, count in author_counts.items():
    if author and str(author).strip() and count >= 10:
        print(f"📌 {author}: {count} مقال")

# ===== ملخص للشريحة 30 =====
print("\n" + "="*80)
print("📋 ملخص للشريحة 30 - المؤثرون في الصورة الإعلامية")
print("="*80)

# ترتيب الشخصيات حسب الظهور
all_personalities = {}
all_personalities.update(qatari_results)
all_personalities.update(fifa_results)
all_personalities.update(sports_results)
all_personalities.update(media_results)

sorted_personalities = sorted(all_personalities.items(), key=lambda x: x[1]['total'], reverse=True)

print(f"\nإجمالي التغطيات: {len(traditional_df):,}")
print(f"\nأبرز الشخصيات المؤثرة:")
for name, data in sorted_personalities[:10]:
    pos_pct = (data['positive'] / data['total'] * 100) if data['total'] > 0 else 0
    print(f"  - {name}: {data['total']} ظهور (إيجابي: {pos_pct:.0f}%)")

# حساب إجمالي الظهورات حسب الفئة
total_qatari = sum(r['total'] for r in qatari_results.values())
total_fifa = sum(r['total'] for r in fifa_results.values())
total_sports = sum(r['total'] for r in sports_results.values())
total_media = sum(r['total'] for r in media_results.values())

print(f"\nتوزيع حسب الفئة:")
print(f"  - شخصيات رسمية قطرية: {total_qatari}")
print(f"  - FIFA والاتحادات: {total_fifa}")
print(f"  - شخصيات رياضية: {total_sports}")
print(f"  - وسائل الإعلام: {total_media}")
