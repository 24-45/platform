#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكربت استخراج تغريدات الجمهور الحقيقية من بيانات Meltwater
يبحث عن تغريدات إيجابية وسلبية حقيقية من الجمهور (وليس المسؤولين)
"""

import pandas as pd
import os
import json
from datetime import datetime

# المسار الأساسي للبيانات
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/data/meltwater"

# قائمة الحسابات الرسمية والمسؤولين (لاستبعادها)
OFFICIAL_ACCOUNTS = [
    'tamimbinhamad', 'joaanbinhamad', 'khk', 'mohamedbinzayed', 'hhtbzayed',
    'hamdanbinzayed', 'spagov', 'abdulaziztf', 'nawafbinfaisal', 'marzouqalghanim',
    'alkasstvsports', 'saudinews50', 'okaz_online', 'ajenglish', 'fifaworldcup',
    'qatarairways', 'derradjihafid', 'khalidjassem74', 'mohammedawaad',
    'shasha_sports', 'eplworld', 'bt3', '_90tm', 'sba_sport', 'shabiba',
    'hrhmbnsalmaan', 'actionma3waleed', 'surenewsksa'
]

# كلمات مفتاحية للتغريدات الإيجابية
POSITIVE_KEYWORDS = [
    'رائع', 'مبهر', 'تنظيم محكم', 'نجاح', 'فخر', 'فخور', 'أبدع', 'متميز',
    'عالمي', 'استثنائي', 'مذهل', 'ممتاز', 'تجربة رائعة', 'أسطوري', 'مميز',
    'شكرا قطر', 'أجمل', 'أفضل', 'تحية', 'مبروك', 'الله يوفقهم', 'ما شاء الله',
    'amazing', 'incredible', 'fantastic', 'great', 'wonderful', 'best',
    'proud', 'success', 'excellent', 'outstanding', 'bravo', 'congratulations'
]

# كلمات مفتاحية للتغريدات السلبية
NEGATIVE_KEYWORDS = [
    'فشل', 'سيء', 'مخيب', 'ضعيف', 'فضيحة', 'عار', 'تخلف', 'كارثة',
    'مهزلة', 'خيبة', 'أسوأ', 'مؤسف', 'محزن', 'غضب', 'انتقاد', 'سخرية',
    'تذمر', 'شكوى', 'غلاء', 'مشكلة', 'صعوبة', 'تأخير', 'زحام', 'ازدحام',
    'تنظيم سيء', 'إحباط', 'خطأ', 'disaster', 'fail', 'terrible', 'bad',
    'shame', 'disappointed', 'worst', 'angry', 'problem', 'expensive'
]


def load_csv_files():
    """تحميل جميع ملفات CSV من مجلدات Meltwater"""
    all_data = []
    
    # البحث في كل المجلدات
    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                    if len(df) > 0:
                        all_data.append(df)
                        print(f"✓ تم تحميل: {file} ({len(df)} صف)")
                except Exception as e:
                    try:
                        df = pd.read_csv(file_path, encoding='latin-1')
                        if len(df) > 0:
                            all_data.append(df)
                            print(f"✓ تم تحميل: {file} ({len(df)} صف)")
                    except:
                        print(f"✗ خطأ في تحميل: {file}")
    
    return all_data


def is_official_account(handle):
    """التحقق مما إذا كان الحساب رسمياً"""
    if pd.isna(handle):
        return False
    handle_clean = str(handle).lower().replace('@', '').strip()
    return handle_clean in OFFICIAL_ACCOUNTS


def is_real_audience_tweet(row):
    """التحقق من أن التغريدة من جمهور حقيقي"""
    handle = str(row.get('Handle', '')).lower() if pd.notna(row.get('Handle')) else ''
    author = str(row.get('Author', '')).lower() if pd.notna(row.get('Author')) else ''
    reach = row.get('Reach', 0)
    
    # استبعاد الحسابات الرسمية
    if is_official_account(handle):
        return False
    
    # استبعاد الحسابات ذات الوصول العالي جداً (عادة إعلامية)
    if reach and reach > 1000000:
        return False
    
    # استبعاد الحسابات الإعلامية والصحفية
    media_keywords = ['news', 'أخبار', 'صحيفة', 'جريدة', 'قناة', 'sport', 'media', 'tv', 'إعلام']
    for keyword in media_keywords:
        if keyword in handle or keyword in author:
            return False
    
    return True


def calculate_engagement_score(row):
    """حساب نقاط التفاعل للتغريدة"""
    retweets = row.get('Retweets', 0) or 0
    reach = row.get('Reach', 0) or 0
    
    # نقاط التفاعل = إعادات التغريد × 10 + الوصول / 1000
    score = (retweets * 10) + (reach / 1000)
    return score


def contains_keywords(text, keywords):
    """التحقق من وجود كلمات مفتاحية في النص"""
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False


def extract_audience_tweets(dataframes):
    """استخراج تغريدات الجمهور الإيجابية والسلبية"""
    
    positive_tweets = []
    negative_tweets = []
    
    for df in dataframes:
        # تحديد أسماء الأعمدة
        url_col = None
        text_col = None
        sentiment_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if 'url' in col_lower:
                url_col = col
            if 'sentence' in col_lower or 'text' in col_lower or 'match' in col_lower:
                text_col = col
            if 'sentiment' in col_lower:
                sentiment_col = col
        
        if not url_col or not text_col:
            continue
        
        for _, row in df.iterrows():
            # التحقق من أنها تغريدة X/Twitter
            url = str(row.get(url_col, ''))
            if 'twitter.com' not in url and 'x.com' not in url:
                continue
            
            # التحقق من أنها من جمهور حقيقي
            if not is_real_audience_tweet(row):
                continue
            
            text = row.get(text_col, '')
            if pd.isna(text) or len(str(text)) < 30:
                continue
            
            tweet_data = {
                'url': url,
                'text': str(text)[:300],  # تحديد طول النص
                'author': row.get('Author', 'مستخدم'),
                'handle': row.get('Handle', ''),
                'date': row.get('Date', ''),
                'reach': row.get('Reach', 0),
                'retweets': row.get('Retweets', 0),
                'sentiment': row.get(sentiment_col, '') if sentiment_col else '',
                'engagement_score': calculate_engagement_score(row)
            }
            
            # تصنيف التغريدة
            sentiment = str(row.get(sentiment_col, '')).lower() if sentiment_col else ''
            
            if sentiment == 'positive' or contains_keywords(text, POSITIVE_KEYWORDS):
                positive_tweets.append(tweet_data)
            elif sentiment == 'negative' or contains_keywords(text, NEGATIVE_KEYWORDS):
                negative_tweets.append(tweet_data)
    
    return positive_tweets, negative_tweets


def filter_best_tweets(tweets, count=15):
    """اختيار أفضل التغريدات بناءً على معايير محددة"""
    
    # إزالة التكرارات بناءً على النص
    seen_texts = set()
    unique_tweets = []
    for tweet in tweets:
        text_key = tweet['text'][:100]  # أول 100 حرف للمقارنة
        if text_key not in seen_texts:
            seen_texts.add(text_key)
            unique_tweets.append(tweet)
    
    # ترتيب حسب نقاط التفاعل
    sorted_tweets = sorted(unique_tweets, key=lambda x: x['engagement_score'], reverse=True)
    
    # اختيار الأفضل
    return sorted_tweets[:count]


def format_tweet_for_display(tweet, index):
    """تنسيق التغريدة للعرض"""
    return f"""
═══════════════════════════════════════════════════════════
التغريدة #{index + 1}
═══════════════════════════════════════════════════════════
👤 الكاتب: {tweet['author']} ({tweet['handle']})
📅 التاريخ: {tweet['date']}
📊 الوصول: {tweet['reach']:,} | إعادات التغريد: {tweet['retweets']}
🔗 الرابط: {tweet['url']}

📝 النص:
{tweet['text']}
"""


def save_results(positive_tweets, negative_tweets):
    """حفظ النتائج في ملف JSON"""
    results = {
        'extraction_date': datetime.now().isoformat(),
        'positive_tweets': positive_tweets,
        'negative_tweets': negative_tweets,
        'summary': {
            'total_positive': len(positive_tweets),
            'total_negative': len(negative_tweets)
        }
    }
    
    output_path = os.path.join(BASE_PATH, 'audience_tweets_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ تم حفظ النتائج في: {output_path}")
    return output_path


def main():
    print("=" * 60)
    print("🔍 بدء استخراج تغريدات الجمهور من بيانات Meltwater")
    print("=" * 60)
    
    # تحميل البيانات
    print("\n📂 تحميل ملفات CSV...")
    dataframes = load_csv_files()
    
    if not dataframes:
        print("❌ لم يتم العثور على ملفات بيانات!")
        return
    
    print(f"\n✓ تم تحميل {len(dataframes)} ملف بيانات")
    
    # استخراج التغريدات
    print("\n🔎 استخراج تغريدات الجمهور...")
    positive_tweets, negative_tweets = extract_audience_tweets(dataframes)
    
    print(f"\n📊 النتائج الأولية:")
    print(f"   - تغريدات إيجابية: {len(positive_tweets)}")
    print(f"   - تغريدات سلبية: {len(negative_tweets)}")
    
    # اختيار أفضل التغريدات
    best_positive = filter_best_tweets(positive_tweets, 15)
    best_negative = filter_best_tweets(negative_tweets, 15)
    
    print(f"\n✅ تم اختيار أفضل التغريدات:")
    print(f"   - أفضل {len(best_positive)} تغريدة إيجابية")
    print(f"   - أفضل {len(best_negative)} تغريدة سلبية")
    
    # عرض التغريدات الإيجابية
    print("\n" + "=" * 60)
    print("📗 التغريدات الإيجابية (صوت الجمهور)")
    print("=" * 60)
    for i, tweet in enumerate(best_positive):
        print(format_tweet_for_display(tweet, i))
    
    # عرض التغريدات السلبية
    print("\n" + "=" * 60)
    print("📕 التغريدات السلبية (صوت الجمهور)")
    print("=" * 60)
    for i, tweet in enumerate(best_negative):
        print(format_tweet_for_display(tweet, i))
    
    # حفظ النتائج
    save_results(best_positive, best_negative)
    
    print("\n" + "=" * 60)
    print("✅ اكتمل استخراج تغريدات الجمهور!")
    print("=" * 60)


if __name__ == "__main__":
    main()
