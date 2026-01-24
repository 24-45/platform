#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكربت محسّن لاستخراج تغريدات الجمهور الحقيقية من بيانات Meltwater
يركز على التغريدات من أفراد الجمهور وليس المسؤولين أو الإعلام
"""

import pandas as pd
import os
import json
from datetime import datetime
import re

# المسار الأساسي للبيانات
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/data/meltwater"

# قائمة موسعة للحسابات الرسمية والإعلامية (لاستبعادها)
EXCLUDED_PATTERNS = [
    # حسابات رسمية
    'tamimbinhamad', 'joaanbinhamad', 'khk', 'mohamedbinzayed', 'hhtbzayed',
    'hamdanbinzayed', 'spagov', 'abdulaziztf', 'nawafbinfaisal', 'marzouqalghanim',
    'hrhmbnsalmaan', 'abdulaziztf',
    
    # قنوات رياضية
    'alkasstvsports', 'shasha_sports', 'beinsports', 'ssc', 'sba_sport',
    
    # وكالات أنباء
    'saudinews50', 'okaz_online', 'ajenglish', 'aljazeera', 'alarabiya',
    'reuters', 'afp', 'annahar', 'almadinanews', 'alarab_qatar',
    'assabahnews', 'shabiba', 'surenewsksa', 'onsiear', 'saudi_news77',
    
    # حسابات رياضية رسمية
    'fifaworldcup', 'qatarairways', 'eplworld', '_90tm', 'roadtoqatar',
    'marsalqatar', 'kataraqatar', 'actionma3waleed',
    
    # صحفيين معروفين
    'derradjihafid', 'khalidjassem74', 'mohammedawaad', 'bt3', 'halgawi',
    'edycohen', 'fahadalhurifi',
    
    # منتخبات وأندية
    'saudint', 'qfa', 'morocco', 'jordan',
]

# كلمات في الاسم تدل على حساب غير جمهوري
MEDIA_NAME_KEYWORDS = [
    'news', 'أخبار', 'صحيفة', 'جريدة', 'قناة', 'sport', 'media', 'tv', 'إعلام',
    'رسمي', 'official', 'gazette', 'times', 'daily', 'press', 'agency',
    'وكالة', 'تلفزيون', 'راديو', 'radio', 'channel', 'network', 'شبكة',
    'herald', 'post', 'tribune', 'journal', 'express', 'insider',
    'interactive', 'digital', 'portal'
]


def is_excluded_account(handle, author):
    """التحقق مما إذا كان الحساب يجب استبعاده"""
    if pd.isna(handle) and pd.isna(author):
        return True
    
    handle_clean = str(handle).lower().replace('@', '').strip() if pd.notna(handle) else ''
    author_clean = str(author).lower() if pd.notna(author) else ''
    
    # التحقق من القائمة السوداء
    for pattern in EXCLUDED_PATTERNS:
        if pattern in handle_clean:
            return True
    
    # التحقق من الكلمات الإعلامية
    for keyword in MEDIA_NAME_KEYWORDS:
        if keyword.lower() in handle_clean or keyword.lower() in author_clean:
            return True
    
    return False


def is_genuine_audience_tweet(row):
    """التحقق من أن التغريدة من جمهور حقيقي"""
    handle = row.get('Handle', '')
    author = row.get('Author', '')
    reach = row.get('Reach', 0) or 0
    url = str(row.get('URL', ''))
    
    # يجب أن تكون من تويتر/X فقط
    if 'twitter.com' not in url and 'x.com' not in url:
        return False
    
    # استبعاد الحسابات الرسمية والإعلامية
    if is_excluded_account(handle, author):
        return False
    
    # استبعاد الحسابات ذات الوصول العالي جداً (عادة إعلامية)
    if reach > 500000:
        return False
    
    # يفضل حسابات بوصول متوسط (جمهور حقيقي)
    if reach < 100:
        return False
    
    return True


def calculate_engagement_score(row):
    """حساب نقاط التفاعل"""
    retweets = row.get('Retweets', 0) or 0
    reach = row.get('Reach', 0) or 0
    return (retweets * 10) + (reach / 100)


def contains_positive_sentiment(text, sentiment):
    """التحقق من المشاعر الإيجابية"""
    positive_keywords = [
        'رائع', 'مبهر', 'تنظيم ممتاز', 'نجاح', 'فخر', 'فخور', 'أبدع', 'متميز',
        'عالمي', 'استثنائي', 'مذهل', 'ممتاز', 'تجربة رائعة', 'أسطوري', 'مميز',
        'شكرا قطر', 'أجمل بطولة', 'أفضل تنظيم', 'مبروك', 'ما شاء الله',
        'أحسنتم', 'تجربة لا تنسى', 'روعة', 'جميل', 'رهيب', 'خيالي',
        'amazing', 'incredible', 'fantastic', 'great', 'wonderful', 'best',
        'proud', 'excellent', 'outstanding', 'bravo', 'beautiful', 'awesome'
    ]
    
    if str(sentiment).lower() == 'positive':
        return True
    
    if pd.isna(text):
        return False
    
    text_lower = str(text).lower()
    for keyword in positive_keywords:
        if keyword.lower() in text_lower:
            return True
    return False


def contains_negative_sentiment(text, sentiment):
    """التحقق من المشاعر السلبية"""
    negative_keywords = [
        'فشل', 'سيء', 'مخيب', 'ضعيف', 'فضيحة', 'عار', 'كارثة',
        'مهزلة', 'خيبة', 'أسوأ', 'مؤسف', 'محزن', 'غضب', 'سخرية',
        'شكوى', 'غالي', 'غلاء', 'مشكلة', 'صعوبة', 'تأخير', 'زحام',
        'تنظيم سيء', 'إحباط', 'خسارة', 'هزيمة', 'انتقاد', 'ظلم', 'تحكيم',
        'حكم', 'خطأ تحكيمي', 'سرقة', 'مباراة سيئة', 'أداء ضعيف',
        'terrible', 'bad', 'disappointing', 'worst', 'angry', 'shame',
        'disaster', 'fail', 'problem', 'expensive', 'robbery', 'unfair'
    ]
    
    if str(sentiment).lower() == 'negative':
        return True
    
    if pd.isna(text):
        return False
    
    text_lower = str(text).lower()
    for keyword in negative_keywords:
        if keyword.lower() in text_lower:
            return True
    return False


def is_meaningful_tweet(text):
    """التحقق من أن التغريدة ذات معنى ومحتوى مفيد"""
    if pd.isna(text):
        return False
    
    text = str(text)
    
    # يجب أن تكون بطول معقول
    if len(text) < 40 or len(text) > 400:
        return False
    
    # استبعاد التغريدات التي هي مجرد روابط
    if text.startswith('http') or text.startswith('RT @'):
        return False
    
    # استبعاد التغريدات غير المرتبطة
    relevant_keywords = ['قطر', 'كأس', 'العرب', 'البطولة', 'الملعب', 'المباراة', 
                        'التنظيم', 'الجمهور', 'المشجعين', 'qatar', 'arab', 'cup',
                        'match', 'stadium', 'fans', 'organization']
    
    text_lower = text.lower()
    has_relevant = any(kw in text_lower for kw in relevant_keywords)
    
    return has_relevant


def load_main_data():
    """تحميل الملف الرئيسي للبيانات"""
    main_file = os.path.join(BASE_PATH, "cleaned", "events_cleaned.csv")
    
    try:
        df = pd.read_csv(main_file, encoding='utf-8', low_memory=False)
        print(f"✓ تم تحميل: events_cleaned.csv ({len(df)} صف)")
        return df
    except Exception as e:
        print(f"❌ خطأ في تحميل الملف: {e}")
        return None


def extract_audience_tweets(df):
    """استخراج تغريدات الجمهور"""
    
    positive_tweets = []
    negative_tweets = []
    
    # تحديد أسماء الأعمدة
    columns = df.columns.tolist()
    print(f"📋 الأعمدة المتاحة: {columns[:10]}...")
    
    url_col = None
    text_col = None
    sentiment_col = None
    
    for col in columns:
        col_lower = col.lower()
        if 'url' in col_lower and url_col is None:
            url_col = col
        if ('hit' in col_lower or 'sentence' in col_lower or 'text' in col_lower or 'snippet' in col_lower) and text_col is None:
            text_col = col
        if 'sentiment' in col_lower and sentiment_col is None:
            sentiment_col = col
    
    print(f"🔍 أعمدة مستخدمة: URL={url_col}, Text={text_col}, Sentiment={sentiment_col}")
    
    if not url_col:
        print("❌ لم يتم العثور على عمود URL")
        return [], []
    
    for idx, row in df.iterrows():
        url = str(row.get(url_col, '')) if url_col else ''
        
        # التحقق من أنها تغريدة من X/Twitter
        if 'twitter.com' not in url:
            continue
        
        # التحقق من أنها من جمهور حقيقي
        if not is_genuine_audience_tweet(row):
            continue
        
        text = row.get(text_col, '') if text_col else row.get('Hit Sentence', '')
        if not is_meaningful_tweet(text):
            continue
        
        sentiment = row.get(sentiment_col, '') if sentiment_col else ''
        
        tweet_data = {
            'url': url,
            'text': str(text)[:350],
            'author': row.get('Author', 'مستخدم'),
            'handle': row.get('Handle', row.get('Source', '')),
            'date': str(row.get('Date', ''))[:10],
            'reach': int(row.get('Reach', 0) or 0),
            'retweets': int(row.get('Retweets', 0) or 0),
            'sentiment': str(sentiment),
            'engagement_score': calculate_engagement_score(row)
        }
        
        # تصنيف التغريدة
        if contains_positive_sentiment(text, sentiment):
            positive_tweets.append(tweet_data)
        elif contains_negative_sentiment(text, sentiment):
            negative_tweets.append(tweet_data)
    
    return positive_tweets, negative_tweets


def filter_and_deduplicate(tweets, count=20):
    """تصفية وإزالة التكرارات"""
    
    # إزالة التكرارات
    seen = set()
    unique = []
    for t in tweets:
        key = t['text'][:80]
        if key not in seen:
            seen.add(key)
            unique.append(t)
    
    # ترتيب حسب التفاعل
    sorted_tweets = sorted(unique, key=lambda x: x['engagement_score'], reverse=True)
    
    return sorted_tweets[:count]


def format_tweet(tweet, index):
    """تنسيق التغريدة للعرض"""
    return f"""
{'='*70}
📌 التغريدة #{index + 1}
{'='*70}
👤 الكاتب: {tweet['author']} ({tweet['handle']})
📅 التاريخ: {tweet['date']}
📊 الوصول: {tweet['reach']:,} | 🔄 إعادات: {tweet['retweets']}
🔗 الرابط: {tweet['url']}

💬 النص:
"{tweet['text']}"
"""


def save_to_json(positive, negative):
    """حفظ النتائج"""
    output = {
        'extraction_date': datetime.now().isoformat(),
        'statistics': {
            'positive_count': len(positive),
            'negative_count': len(negative)
        },
        'positive_tweets': positive,
        'negative_tweets': negative
    }
    
    output_path = os.path.join(BASE_PATH, 'audience_voice_tweets.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم حفظ النتائج في: {output_path}")
    return output_path


def main():
    print("=" * 70)
    print("🔍 استخراج تغريدات الجمهور الحقيقية - صوت الجمهور")
    print("=" * 70)
    
    # تحميل البيانات
    df = load_main_data()
    if df is None:
        return
    
    # استخراج التغريدات
    print("\n🔎 جاري تحليل التغريدات...")
    positive, negative = extract_audience_tweets(df)
    
    print(f"\n📊 النتائج الأولية:")
    print(f"   ✅ إيجابية: {len(positive)}")
    print(f"   ❌ سلبية: {len(negative)}")
    
    # تصفية الأفضل
    best_positive = filter_and_deduplicate(positive, 20)
    best_negative = filter_and_deduplicate(negative, 20)
    
    print(f"\n✨ أفضل التغريدات المختارة:")
    print(f"   ✅ إيجابية: {len(best_positive)}")
    print(f"   ❌ سلبية: {len(best_negative)}")
    
    # عرض التغريدات الإيجابية
    print("\n" + "=" * 70)
    print("📗 التغريدات الإيجابية - صوت الجمهور")
    print("=" * 70)
    for i, t in enumerate(best_positive[:15]):
        print(format_tweet(t, i))
    
    # عرض التغريدات السلبية
    print("\n" + "=" * 70)
    print("📕 التغريدات السلبية - صوت الجمهور")
    print("=" * 70)
    for i, t in enumerate(best_negative[:15]):
        print(format_tweet(t, i))
    
    # حفظ النتائج
    save_to_json(best_positive, best_negative)
    
    print("\n" + "=" * 70)
    print("✅ اكتمل الاستخراج!")
    print("=" * 70)


if __name__ == "__main__":
    main()
