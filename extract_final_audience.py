#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكربت نهائي لاستخراج تغريدات الجمهور الحقيقية
يركز على أفراد الجمهور فقط ويستبعد كل الحسابات الرسمية والإعلامية
"""

import pandas as pd
import os
import json
from datetime import datetime

BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/data/meltwater"

# استبعاد أي حساب يحتوي على هذه الكلمات
EXCLUDE_WORDS = [
    # إعلام
    'news', 'أخبار', 'صحيفة', 'جريدة', 'قناة', 'media', 'tv', 'television',
    'radio', 'channel', 'network', 'شبكة', 'وكالة', 'agency', 'press',
    'times', 'daily', 'gazette', 'herald', 'post', 'tribune', 'journal',
    'تلفزيون', 'إذاعة', 'breaking', 'عاجل', 'alert', 'official', 'رسمي',
    # رياضة
    'sports', 'sport', 'soccer', 'football', 'fifa', 'fc', 'club',
    'team', 'league', 'cup', 'match', 'stadium', 'arena',
    # حكومي
    'gov', 'ministry', 'وزارة', 'هيئة', 'مجلس', 'council', 'authority',
    # تجاري
    'brand', 'company', 'inc', 'corp', 'store', 'shop', 'market',
    # شخصيات عامة
    'sheik', 'شيخ', 'أمير', 'emir', 'prince', 'king', 'ملك', 'royal',
    'minister', 'وزير', 'president', 'رئيس', 'ceo', 'founder',
    # حسابات كبيرة
    'studio', 'interactive', 'digital', 'portal', 'online', 'stuff',
    'world', 'global', 'international', 'arab', 'qatar', 'saudi',
    'uae', 'kuwait', 'oman', 'bahrain', 'jordan', 'morocco', 'egypt',
]

# قائمة سوداء للحسابات المحددة
BLACKLIST = [
    'tamimbinhamad', 'joaanbinhamad', 'khk', 'mohamedbinzayed', 'bt3',
    'shasha_sports', 'alkasstvsports', 'derradjihafid', 'khalidjassem74',
    '_90tm', 'fifaworldcup', 'saudinews50', 'okaz_online', 'alarab_qatar',
    'qatartelevision', 'ittistudio', 'kataraqatar', 'assabahnews', 'shabiba',
    'alraya_n', 'misbarfc', 'saudistuff', 'alekhbariyabrk', 'leomessimedia',
    'imiasanmia', 'amrfahmy2007', 'a_albander', 'khalafmelfi',
]


def is_genuine_audience(handle, author, reach):
    """فحص صارم للتأكد من أن الحساب جمهور حقيقي"""
    
    handle_lower = str(handle).lower().replace('@', '') if pd.notna(handle) else ''
    author_lower = str(author).lower() if pd.notna(author) else ''
    
    # استبعاد من القائمة السوداء
    for bl in BLACKLIST:
        if bl in handle_lower:
            return False
    
    # استبعاد بناءً على الكلمات
    combined = handle_lower + ' ' + author_lower
    for word in EXCLUDE_WORDS:
        if word.lower() in combined:
            return False
    
    # استبعاد الحسابات الكبيرة جداً
    reach_val = reach if pd.notna(reach) else 0
    if reach_val > 200000:
        return False
    
    # استبعاد الحسابات الصغيرة جداً
    if reach_val < 500:
        return False
    
    return True


def analyze_sentiment(text):
    """تحليل مشاعر النص"""
    text = str(text).lower() if pd.notna(text) else ''
    
    positive_words = [
        'رائع', 'ممتاز', 'مبهر', 'جميل', 'روعة', 'فخر', 'فخور', 'شكرا', 'مبروك',
        'نجاح', 'تنظيم رائع', 'أبدع', 'ما شاء الله', 'استثنائي', 'عالمي', 'مذهل',
        'تجربة رائعة', 'أجمل', 'أفضل', 'احترافي', 'متميز', 'تهانينا',
        'amazing', 'great', 'wonderful', 'fantastic', 'excellent', 'beautiful',
        'proud', 'incredible', 'awesome', 'best', 'congratulations', 'bravo'
    ]
    
    negative_words = [
        'سيء', 'فاشل', 'مخيب', 'ضعيف', 'كارثة', 'فضيحة', 'عار', 'أسوأ',
        'خيبة', 'غضب', 'انتقاد', 'مشكلة', 'صعوبة', 'غلاء', 'غالي',
        'زحام', 'تأخير', 'إحباط', 'حزين', 'سرقة', 'ظلم', 'تحكيم سيء',
        'خسارة', 'هزيمة', 'خطأ', 'اعتراض',
        'bad', 'terrible', 'worst', 'disappointing', 'disaster', 'fail',
        'shame', 'angry', 'problem', 'expensive', 'robbery', 'unfair'
    ]
    
    pos_score = sum(1 for w in positive_words if w in text)
    neg_score = sum(1 for w in negative_words if w in text)
    
    if pos_score > neg_score:
        return 'positive', pos_score
    elif neg_score > pos_score:
        return 'negative', neg_score
    return 'neutral', 0


def is_relevant_tweet(text):
    """التأكد من أن التغريدة متعلقة بالبطولة"""
    text = str(text).lower() if pd.notna(text) else ''
    
    # كلمات تدل على أنها متعلقة بالبطولة
    relevant = [
        'قطر', 'كأس', 'العرب', 'البطولة', 'الملعب', 'المباراة', 'المنتخب',
        'الجمهور', 'المشجعين', 'التنظيم', 'الدوحة', 'لوسيل', 'البيت',
        'qatar', 'arab cup', 'doha', 'stadium', 'match', 'team', 'fans'
    ]
    
    return any(r in text for r in relevant)


def extract_tweets():
    """استخراج التغريدات"""
    
    # تحميل البيانات
    df = pd.read_csv(f"{BASE_PATH}/cleaned/events_cleaned.csv", low_memory=False)
    print(f"📂 تم تحميل {len(df)} صف من البيانات")
    
    positive_tweets = []
    negative_tweets = []
    
    for _, row in df.iterrows():
        url = str(row.get('URL', ''))
        if 'twitter.com' not in url:
            continue
        
        handle = row.get('Handle', row.get('Source', ''))
        author = row.get('Author', '')
        reach = row.get('Reach', 0)
        
        if not is_genuine_audience(handle, author, reach):
            continue
        
        text = row.get('Opening Text', row.get('Hit Sentence', ''))
        if not is_relevant_tweet(text) or len(str(text)) < 50:
            continue
        
        sentiment, score = analyze_sentiment(text)
        if sentiment == 'neutral' or score < 1:
            continue
        
        tweet = {
            'url': url,
            'text': str(text)[:300],
            'author': author if pd.notna(author) else 'مستخدم',
            'handle': str(handle).replace('@', '') if pd.notna(handle) else '',
            'date': str(row.get('Date', ''))[:10],
            'reach': int(reach) if pd.notna(reach) else 0,
            'retweets': int(row.get('Retweets', 0) or 0),
            'sentiment_score': score
        }
        
        if sentiment == 'positive':
            positive_tweets.append(tweet)
        else:
            negative_tweets.append(tweet)
    
    return positive_tweets, negative_tweets


def deduplicate_and_sort(tweets, count=20):
    """إزالة التكرار والترتيب"""
    seen = set()
    unique = []
    for t in tweets:
        key = t['text'][:60]
        if key not in seen:
            seen.add(key)
            unique.append(t)
    
    # ترتيب بناءً على التفاعل ودرجة المشاعر
    sorted_tweets = sorted(unique, 
                          key=lambda x: (x['sentiment_score'] * 100) + x['retweets'] + (x['reach'] / 1000), 
                          reverse=True)
    return sorted_tweets[:count]


def display_tweet(t, i):
    """عرض التغريدة"""
    print(f"""
{'─'*60}
📌 #{i+1} | @{t['handle']}
{'─'*60}
📅 {t['date']} | 👁️ {t['reach']:,} | 🔄 {t['retweets']}
🔗 {t['url']}

💬 {t['text']}
""")


def main():
    print("="*60)
    print("🎯 استخراج تغريدات الجمهور الحقيقية")
    print("="*60)
    
    positive, negative = extract_tweets()
    
    print(f"\n📊 النتائج الأولية:")
    print(f"   ✅ إيجابية: {len(positive)}")
    print(f"   ❌ سلبية: {len(negative)}")
    
    best_pos = deduplicate_and_sort(positive, 20)
    best_neg = deduplicate_and_sort(negative, 20)
    
    print(f"\n✨ تم اختيار:")
    print(f"   ✅ أفضل {len(best_pos)} تغريدة إيجابية")
    print(f"   ❌ أفضل {len(best_neg)} تغريدة سلبية")
    
    # عرض الإيجابية
    print("\n" + "="*60)
    print("📗 تغريدات الجمهور الإيجابية")
    print("="*60)
    for i, t in enumerate(best_pos[:15]):
        display_tweet(t, i)
    
    # عرض السلبية
    print("\n" + "="*60)
    print("📕 تغريدات الجمهور السلبية")
    print("="*60)
    for i, t in enumerate(best_neg[:15]):
        display_tweet(t, i)
    
    # حفظ النتائج
    output = {
        'date': datetime.now().isoformat(),
        'positive': best_pos,
        'negative': best_neg
    }
    
    with open(f"{BASE_PATH}/final_audience_tweets.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم حفظ النتائج في: {BASE_PATH}/final_audience_tweets.json")


if __name__ == "__main__":
    main()
