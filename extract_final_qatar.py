#!/usr/bin/env python3
"""
استخراج تغريدات الجمهور الحقيقية - النسخة النهائية
التركيز على التغريدات المتعلقة بالتنظيم والتذاكر
"""

import pandas as pd
import os
import json
import re
from pathlib import Path

# مسار المجلد الرئيسي
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr 4"

# الكلمات التي تستبعد الحسابات الرسمية والإعلامية
EXCLUDE_ACCOUNTS = [
    'jazeera', 'alarabiya', 'ajarabic', 'ajplus', 'skynews', 'bbc', 'cnn',
    'reuters', 'afp', 'france24', 'dw', 'rt_arabic', 'mbc', 'alaraby',
    'bein', 'beinsports', 'ssc', 'alkass', 'kooora', 'yallakora',
    'filgoal', 'goal', 'espn', 'btolat', 'koora',
    'gov', 'ministry', 'official', 'olympic', 'fifa', 'afc',
    'qatarairways', 'qfa', 'qoc', 'aspire', 'katara',
    '964arabic', '964', 'news',
    # حسابات UFC
    'ufc', 'mma', 'happypunch', 'spinninbackfist', 'champrds', 'cejudo',
    'acdmma', 'espnmma', 'lasueur', 'dovysim', 'tekkersfoot', 'cbssports',
]

# كلمات التنظيم والملاعب
ORGANIZATION_KEYWORDS = [
    'قطر', 'Qatar', 'الدوحة', 'Doha', 'التنظيم', 'تنظيم',
    'الملعب', 'الملاعب', 'استاد', 'البيت', 'لوسيل', '974',
    'الفنادق', 'فندق', 'التذاكر', 'تذكرة', 'تذاكر',
    'الحضور', 'الجماهير', 'الجمهور', 'الاستضافة', 'استضافة',
    'كأس العرب', 'كاس العرب', 'ArabCup',
    'مترو', 'المترو', 'المواصلات', 'النقل',
    'الأمن', 'التأمين', 'آمنة', 'آمن',
]

# كلمات إيجابية قوية
STRONG_POSITIVE = [
    'شكرا قطر', 'شكراً قطر', 'شكراً لقطر', 'شكرا لقطر',
    'تستاهل قطر', 'يستاهلون', 'تستاهلون',
    'تنظيم رائع', 'تنظيم مبهر', 'تنظيم احترافي', 'تنظيم ممتاز',
    'ملاعب اسطورية', 'ملاعب رائعة', 'ملاعب مبهرة',
    'نجاح كأس العرب', 'نجاح البطولة',
    'ما شاء الله', 'ماشاء الله',
    'الله يعطيهم العافية', 'الله يوفقهم',
    'افتخر', 'نفتخر', 'فخر',
    'احترافي', 'احترافية', 'عالمي', 'عالمية',
    'ابداع', 'إبداع', 'مبدع', 'مبدعين',
    'مبروك', 'مباركين', 'الف مبروك',
    'ممتاز', 'رائع', 'مبهر', 'مذهل', 'عظيم', 'جميل',
]

# كلمات إيجابية عادية
NORMAL_POSITIVE = [
    'شكرا', 'شكراً', 'ممتاز', 'رائع', 'جميل', 'عظيم',
    'نجاح', 'ناجح', 'ناجحة', 'موفق', 'موفقين',
    'حماس', 'حماسي', 'استمتعت', 'استمتعنا',
    'أحسنت', 'تسلم', 'يسلمو', 'العافية',
    'حلو', 'حلوة', 'جميلة', 'رائعة',
]

# كلمات سلبية متعلقة بالتنظيم
ORGANIZATION_NEGATIVE = [
    # التذاكر
    'التذاكر غالية', 'الأسعار غالية', 'سعر غالي', 'اسعار نار',
    'ما حصلت تذاكر', 'ما لقيت تذاكر', 'نفذت التذاكر',
    'تذاكر غالية', 'تذكرة غالية',
    # التنظيم
    'تنظيم سيء', 'تنظيم ضعيف', 'تنظيم فاشل',
    'زحمة', 'زحمه', 'ازدحام', 'طوابير',
    # الخدمات
    'مشكلة', 'مشكله', 'مشاكل',
    'فوضى', 'فوضوي',
    'تأخير', 'متأخر', 'تأخر',
]

# كلمات سلبية عادية
NORMAL_NEGATIVE = [
    'غالي', 'غاليه', 'غالية', 'مكلف', 'مكلفة',
    'سعر', 'أسعار', 'اسعار',
    'سيء', 'سيئ', 'سيئة', 'ضعيف', 'ضعيفة',
    'فاشل', 'فاشلة', 'فشل',
    'للأسف', 'مؤسف', 'محزن',
    'صعب', 'صعبة', 'صعوبة',
    'نقص', 'ناقص', 'ناقصة',
    'مو معقول', 'مش معقول', 'غير معقول',
]

def is_genuine_audience(author_handle, author_name):
    """التحقق من أن الحساب هو جمهور حقيقي"""
    if not author_handle or pd.isna(author_handle):
        return False
    
    handle_lower = str(author_handle).lower()
    name_lower = str(author_name).lower() if author_name and not pd.isna(author_name) else ''
    
    for word in EXCLUDE_ACCOUNTS:
        if word.lower() in handle_lower or word.lower() in name_lower:
            return False
    
    return True

def is_about_organization(text):
    """التحقق من أن التغريدة متعلقة بالتنظيم"""
    if not text or pd.isna(text):
        return False
    
    text = str(text)
    count = sum(1 for keyword in ORGANIZATION_KEYWORDS if keyword in text)
    return count >= 1

def analyze_sentiment_detailed(text, meltwater_sentiment):
    """تحليل المشاعر بشكل مفصل"""
    if not text or pd.isna(text):
        return 'neutral', 0, []
    
    text_lower = str(text).lower()
    text_original = str(text)
    
    # البحث عن الكلمات الإيجابية القوية
    strong_positive_found = []
    for word in STRONG_POSITIVE:
        if word in text_original or word.lower() in text_lower:
            strong_positive_found.append(word)
    
    # البحث عن الكلمات الإيجابية العادية
    normal_positive_found = []
    for word in NORMAL_POSITIVE:
        if word in text_original or word.lower() in text_lower:
            normal_positive_found.append(word)
    
    # البحث عن الكلمات السلبية المتعلقة بالتنظيم
    org_negative_found = []
    for word in ORGANIZATION_NEGATIVE:
        if word in text_original or word.lower() in text_lower:
            org_negative_found.append(word)
    
    # البحث عن الكلمات السلبية العادية
    normal_negative_found = []
    for word in NORMAL_NEGATIVE:
        if word in text_original or word.lower() in text_lower:
            normal_negative_found.append(word)
    
    # حساب النتيجة
    positive_score = len(strong_positive_found) * 3 + len(normal_positive_found)
    negative_score = len(org_negative_found) * 3 + len(normal_negative_found)
    
    # إعطاء وزن لتحليل Meltwater
    mw_sentiment = str(meltwater_sentiment).lower() if meltwater_sentiment and not pd.isna(meltwater_sentiment) else ''
    if mw_sentiment == 'positive':
        positive_score += 2
    elif mw_sentiment == 'negative':
        negative_score += 2
    
    keywords_found = strong_positive_found + normal_positive_found + org_negative_found + normal_negative_found
    
    if positive_score > negative_score and positive_score >= 3:
        return 'positive', positive_score, keywords_found
    elif negative_score > positive_score and negative_score >= 2:
        return 'negative', negative_score, keywords_found
    elif positive_score > 0 and positive_score > negative_score:
        return 'positive', positive_score, keywords_found
    elif negative_score > 0:
        return 'negative', negative_score, keywords_found
    else:
        return 'neutral', 0, keywords_found

def clean_text(text):
    """تنظيف النص"""
    if not text or pd.isna(text):
        return ''
    text = str(text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'^(QT|RT)\s*@?\w*:?\s*', '', text)
    text = text.strip()
    return text[:600] if len(text) > 600 else text

def process_csv_file(file_path):
    """معالجة ملف CSV واحد"""
    tweets = []
    
    try:
        for encoding in ['utf-16', 'utf-8', 'utf-8-sig', 'latin-1']:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep='\t', on_bad_lines='skip', low_memory=False)
                break
            except:
                continue
        else:
            return []
        
        required_cols = ['Author Handle', 'Opening Text', 'Reach', 'URL']
        if not all(col in df.columns for col in required_cols):
            return []
        
        for _, row in df.iterrows():
            author_handle = row.get('Author Handle', '')
            author_name = row.get('Author Name', '')
            text = row.get('Opening Text', '') or row.get('Hit Sentence', '')
            reach = row.get('Reach', 0)
            url = row.get('URL', '')
            mw_sentiment = row.get('Sentiment', '')
            engagement = row.get('Engagement', 0)
            likes = row.get('Likes', 0)
            
            if not is_genuine_audience(author_handle, author_name):
                continue
            
            if not is_about_organization(text):
                continue
            
            clean = clean_text(text)
            if len(clean) < 40:
                continue
            
            try:
                reach_val = float(reach) if reach and not pd.isna(reach) else 0
                if reach_val > 600000 or reach_val < 50:
                    continue
            except:
                continue
            
            sentiment, score, keywords = analyze_sentiment_detailed(text, mw_sentiment)
            
            if sentiment == 'neutral':
                continue
            
            tweets.append({
                'author_handle': str(author_handle).replace('@', ''),
                'author_name': str(author_name) if author_name and not pd.isna(author_name) else '',
                'text': clean,
                'url': str(url) if url and not pd.isna(url) else '',
                'reach': reach_val,
                'engagement': float(engagement) if engagement and not pd.isna(engagement) else 0,
                'likes': float(likes) if likes and not pd.isna(likes) else 0,
                'sentiment': sentiment,
                'sentiment_score': score,
                'keywords_found': keywords[:5],
                'meltwater_sentiment': str(mw_sentiment) if mw_sentiment else '',
            })
    
    except Exception as e:
        print(f"Error: {e}")
    
    return tweets

def find_all_csv_files():
    csv_files = []
    for root, dirs, files in os.walk(BASE_PATH):
        if 'X insights' in root or 'overview' in root:
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
    return csv_files

def main():
    print("=" * 70)
    print("استخراج تغريدات الجمهور - النسخة النهائية")
    print("=" * 70)
    
    csv_files = find_all_csv_files()
    print(f"\nتم العثور على {len(csv_files)} ملف CSV")
    
    all_tweets = []
    for file_path in csv_files:
        tweets = process_csv_file(file_path)
        all_tweets.extend(tweets)
    
    print(f"إجمالي التغريدات المستخرجة: {len(all_tweets)}")
    
    # إزالة التكرارات
    seen_texts = set()
    unique_tweets = []
    for tweet in all_tweets:
        text_key = tweet['text'][:60]
        if text_key not in seen_texts:
            seen_texts.add(text_key)
            unique_tweets.append(tweet)
    
    print(f"بعد إزالة التكرارات: {len(unique_tweets)}")
    
    positive_tweets = [t for t in unique_tweets if t['sentiment'] == 'positive']
    negative_tweets = [t for t in unique_tweets if t['sentiment'] == 'negative']
    
    def quality_score(t):
        return t['sentiment_score'] * 5 + min(t['likes'], 1000) / 100
    
    positive_tweets.sort(key=quality_score, reverse=True)
    negative_tweets.sort(key=quality_score, reverse=True)
    
    print(f"\n✅ التغريدات الإيجابية: {len(positive_tweets)}")
    print(f"❌ التغريدات السلبية: {len(negative_tweets)}")
    
    # أفضل 15
    best_positive = positive_tweets[:15]
    best_negative = negative_tweets[:15]
    
    print(f"\n{'=' * 70}")
    print("🟢 أفضل 15 تغريدة إيجابية:")
    print("=" * 70)
    for i, t in enumerate(best_positive, 1):
        print(f"\n{i}. @{t['author_handle']}")
        print(f"   \"{t['text'][:180]}\"")
        print(f"   🔗 {t['url']}")
        print(f"   ❤️ {t['likes']:,.0f} likes | Keywords: {t['keywords_found']}")
    
    print(f"\n{'=' * 70}")
    print("🔴 أفضل 15 تغريدة سلبية:")
    print("=" * 70)
    for i, t in enumerate(best_negative, 1):
        print(f"\n{i}. @{t['author_handle']}")
        print(f"   \"{t['text'][:180]}\"")
        print(f"   🔗 {t['url']}")
        print(f"   ❤️ {t['likes']:,.0f} likes | Keywords: {t['keywords_found']}")
    
    # حفظ النتائج
    output = {
        'summary': {
            'positive_count': len(positive_tweets),
            'negative_count': len(negative_tweets),
        },
        'positive_tweets': best_positive,
        'negative_tweets': best_negative
    }
    
    output_path = "/Users/taherirshaid/Desktop/Project/24-45-Platform/data/meltwater/final_qatar_audience.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم الحفظ في: {output_path}")

if __name__ == "__main__":
    main()
