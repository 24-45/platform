#!/usr/bin/env python3
"""
استخراج تغريدات الجمهور الحقيقية من ملفات Meltwater
البحث في جميع ملفات X insights و overview
"""

import pandas as pd
import os
import json
import re
from pathlib import Path

# مسار المجلد الرئيسي
BASE_PATH = "/Users/taherirshaid/Desktop/Project/24-45-Platform/static/data/meltwater/qatr 4"

# الكلمات التي تستبعد الحسابات الرسمية والإعلامية
EXCLUDE_WORDS = [
    # وسائل إعلام عربية
    'jazeera', 'alarabiya', 'ajarabic', 'ajplus', 'skynews', 'bbc', 'cnn',
    'reuters', 'afp', 'france24', 'dw', 'rt_arabic', 'mbc', 'alaraby',
    'alhurra', 'masr', 'youm7', 'shorouk', 'masrawy', 'alanba', 'annahar',
    'الجزيرة', 'العربية', 'سكاي', 'بي_بي_سي', 'رويترز', 'فرانس',
    # وسائل إعلام رياضية
    'bein', 'beinsports', 'ssc', 'alkass', 'stadium', 'kooora', 'yallakora',
    'filgoal', 'goal', 'espn', 'sport', 'btolat', 'koora', 'stadium',
    'الكاس', 'بي_ان', 'كووورة', 'يلا_كورة', 'فيلجول', 'بطولات',
    # حسابات رسمية
    'gov', 'ministry', 'official', 'olympic', 'fifa', 'afc', 'fiba',
    'qatar', 'qatarairways', 'qfa', 'qoc', 'aspire', 'katara',
    'الرياضة', 'الشباب', 'وزارة', 'رسمي', 'الأولمبية', 'الاتحاد',
    'qatarstc', 'qatargas', 'ooredoo', 'vodafone',
    # صحفيين ومحللين
    'journalist', 'reporter', 'editor', 'analyst', 'correspondent',
    'صحفي', 'مراسل', 'محلل', 'إعلامي', 'كاتب', 'محرر',
    # أندية ومنتخبات
    'club', 'fc', 'team', 'national', 'منتخب', 'نادي', 'الأهلي', 'الزمالك',
    'الهلال', 'النصر', 'الاتحاد', 'الأهلى', 'برشلونة', 'ريال',
    # حسابات موثقة كبيرة
    'verified', 'blue_check', 'celebrity',
]

# قائمة سوداء لحسابات محددة
BLACKLIST_ACCOUNTS = [
    'aaborashed', 'gaborashed', 'saborashed', 'tamaborashed',
    'ajaborashed', 'aaborashid', 'aborashid',
    'khlooodf', 'khlodf', 'kh_jassim', 'alaborashid',
    'tamaborashid', 'alaborasid', 'aborasid',
    '@TamimBinHamad', '@khalaborashid',
    # حسابات إعلامية
    'baborashed', 'alborashid', 'ajarabic', 'aaborashid',
]

# كلمات تدل على جمهور حقيقي
AUDIENCE_INDICATORS = [
    'والله', 'الحمدلله', 'ماشاء الله', 'صراحة', 'بصراحة',
    'رحت', 'روحت', 'حضرت', 'شفت', 'رايح', 'بروح',
    'يا ناس', 'يا جماعة', 'الله يعطيك', 'تستاهل', 'يستاهل',
    'انا', 'أنا', 'احنا', 'نحنا', 'عندنا', 'بلدنا',
    'حبيت', 'عجبني', 'استمتعت', 'استانست', 'فرحت',
    'زعلت', 'تضايقت', 'غلطوا', 'يا حرام', 'مو معقول',
    'ليش', 'ليه', 'كيف', 'شلون', 'وش', 'ايش',
    'اجل', 'ايه', 'اه', 'لا', 'صح', 'غلط',
    'تذاكر', 'تذكرة', 'التذاكر', 'الاسعار', 'السعر', 'غالي', 'رخيص',
    'الملعب', 'الجو', 'الحضور', 'التنظيم', 'المواصلات',
]

# كلمات المشاعر الإيجابية
POSITIVE_KEYWORDS = [
    'شكرا', 'شكراً', 'ممتاز', 'رائع', 'جميل', 'مبدع', 'عظيم', 'تستاهل',
    'يستاهلون', 'ابداع', 'احترافي', 'احترافية', 'مبهر', 'مذهل', 'فخر',
    'افتخر', 'نفتخر', 'يسعدني', 'سعيد', 'فرحان', 'الله يعطيهم',
    'ما شاء الله', 'ماشاء الله', 'تبارك', 'حلو', 'عاش', 'براڤو',
    'برافو', 'يعطيكم العافية', 'العافية', 'موفقين', 'مبروك',
    'تحية', 'تحيه', 'الأفضل', 'افضل', 'أفضل', 'نجاح', 'ناجح',
    'استمتعت', 'استمتعنا', 'لذيذ', 'حماس', 'حماسي', 'روعة', 'روعه',
    'ممتازة', 'رائعة', 'جميلة', 'مبدعة', 'عظيمة', 'مبهرة', 'مذهلة',
    'سعيدة', 'فرحانة', 'حلوة', 'عاشت', 'ناجحة', 'لذيذة',
    'أحسنت', 'أحسنتم', 'تسلم', 'يسلمو', 'الله يوفقكم', 'الله يعطيكم',
    'الله يبارك', 'مو طبيعي', 'شي ثاني', 'عالمي', 'مستوى',
]

# كلمات المشاعر السلبية
NEGATIVE_KEYWORDS = [
    'زحمة', 'زحمه', 'غالي', 'غاليه', 'سعر', 'اسعار', 'أسعار', 'التذاكر',
    'تذكرة', 'مشكلة', 'مشكله', 'مشاكل', 'سيء', 'سيئ', 'سيئة', 'ضعيف',
    'ضعيفة', 'فاشل', 'فاشلة', 'فشل', 'خايس', 'خايسة', 'زفت',
    'للأسف', 'مؤسف', 'محزن', 'حزين', 'خسارة', 'خسرنا', 'ظلم',
    'حرام', 'عيب', 'قرف', 'مقرف', 'تعب', 'متعب', 'صعب', 'صعبة',
    'مستحيل', 'نصب', 'نصابين', 'حرامية', 'استغلال', 'مستغلين',
    'ليش كذا', 'ليه كده', 'وش السالفة', 'شو هالحكي', 'مو صاحي',
    'طفش', 'ملل', 'ممل', 'بطيء', 'تأخير', 'ما فيه', 'مافي',
    'نقص', 'ناقص', 'ناقصة', 'ردي', 'رديء', 'رديئة', 'وسخ',
    'مهزلة', 'كارثة', 'فضيحة', 'عار', 'معقول', 'غير معقول',
    'مو معقول', 'مش معقول', 'ما يصير', 'لا يصير', 'غلط', 'خطأ',
    'انتقاد', 'نقد', 'اعتراض', 'رفض', 'مرفوض', 'غير مقبول',
    'احتكار', 'محتكر', 'تلاعب', 'غش', 'فوضى', 'فوضوي',
]

def is_genuine_audience(author_handle, author_name, reach):
    """التحقق من أن الحساب هو جمهور حقيقي"""
    if not author_handle or pd.isna(author_handle):
        return False
    
    handle_lower = str(author_handle).lower()
    name_lower = str(author_name).lower() if author_name and not pd.isna(author_name) else ''
    
    # استبعاد الحسابات في القائمة السوداء
    for blocked in BLACKLIST_ACCOUNTS:
        if blocked.lower() in handle_lower:
            return False
    
    # استبعاد الحسابات التي تحتوي على كلمات مستبعدة
    for word in EXCLUDE_WORDS:
        if word.lower() in handle_lower or word.lower() in name_lower:
            return False
    
    # استبعاد الحسابات ذات الوصول الكبير جداً (مشاهير/إعلام)
    try:
        reach_val = float(reach) if reach and not pd.isna(reach) else 0
        if reach_val > 500000:  # أكثر من 500 ألف
            return False
        if reach_val < 100:  # أقل من 100 (بوتات)
            return False
    except:
        pass
    
    return True

def analyze_sentiment(text, meltwater_sentiment):
    """تحليل المشاعر مع الاعتماد على Meltwater + تحليل إضافي"""
    if not text or pd.isna(text):
        return 'neutral', 0
    
    text = str(text).lower()
    
    positive_score = sum(1 for word in POSITIVE_KEYWORDS if word in text)
    negative_score = sum(1 for word in NEGATIVE_KEYWORDS if word in text)
    
    # إعطاء وزن لتحليل Meltwater
    mw_sentiment = str(meltwater_sentiment).lower() if meltwater_sentiment and not pd.isna(meltwater_sentiment) else ''
    
    if mw_sentiment == 'positive':
        positive_score += 2
    elif mw_sentiment == 'negative':
        negative_score += 2
    
    if positive_score > negative_score and positive_score >= 2:
        return 'positive', positive_score
    elif negative_score > positive_score and negative_score >= 2:
        return 'negative', negative_score
    elif positive_score > 0:
        return 'positive', positive_score
    elif negative_score > 0:
        return 'negative', negative_score
    else:
        return 'neutral', 0

def has_audience_indicators(text):
    """التحقق من وجود مؤشرات الجمهور الحقيقي"""
    if not text or pd.isna(text):
        return False, 0
    
    text = str(text)
    count = sum(1 for ind in AUDIENCE_INDICATORS if ind in text)
    return count > 0, count

def clean_text(text):
    """تنظيف النص"""
    if not text or pd.isna(text):
        return ''
    text = str(text)
    # إزالة الروابط
    text = re.sub(r'https?://\S+', '', text)
    # إزالة mentions مكررة
    text = re.sub(r'@\w+', '', text)
    text = text.strip()
    return text[:500] if len(text) > 500 else text

def process_csv_file(file_path):
    """معالجة ملف CSV واحد"""
    tweets = []
    
    try:
        # قراءة الملف بترميز مختلف
        for encoding in ['utf-16', 'utf-8', 'utf-8-sig', 'latin-1']:
            try:
                df = pd.read_csv(file_path, encoding=encoding, sep='\t', on_bad_lines='skip', low_memory=False)
                break
            except:
                continue
        else:
            return []
        
        # التأكد من وجود الأعمدة المطلوبة
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
            
            # التحقق من أنه جمهور حقيقي
            if not is_genuine_audience(author_handle, author_name, reach):
                continue
            
            # تنظيف النص
            clean = clean_text(text)
            if len(clean) < 20:  # نص قصير جداً
                continue
            
            # تحليل المشاعر
            sentiment, score = analyze_sentiment(text, mw_sentiment)
            
            # التحقق من مؤشرات الجمهور
            has_indicators, indicator_count = has_audience_indicators(text)
            
            tweets.append({
                'author_handle': str(author_handle),
                'author_name': str(author_name) if author_name and not pd.isna(author_name) else '',
                'text': clean,
                'full_text': str(text)[:1000] if text else '',
                'url': str(url) if url and not pd.isna(url) else '',
                'reach': float(reach) if reach and not pd.isna(reach) else 0,
                'engagement': float(engagement) if engagement and not pd.isna(engagement) else 0,
                'likes': float(likes) if likes and not pd.isna(likes) else 0,
                'sentiment': sentiment,
                'sentiment_score': score,
                'meltwater_sentiment': str(mw_sentiment) if mw_sentiment else '',
                'has_audience_indicators': has_indicators,
                'indicator_count': indicator_count,
                'source_file': os.path.basename(file_path)
            })
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return tweets

def find_all_csv_files():
    """البحث عن جميع ملفات CSV في المجلد"""
    csv_files = []
    
    for root, dirs, files in os.walk(BASE_PATH):
        # التركيز على مجلدات X insights و overview
        if 'X insights' in root or 'overview' in root:
            for file in files:
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(root, file))
    
    return csv_files

def main():
    print("=" * 60)
    print("استخراج تغريدات الجمهور الحقيقية من Meltwater")
    print("=" * 60)
    
    # العثور على جميع الملفات
    csv_files = find_all_csv_files()
    print(f"\nتم العثور على {len(csv_files)} ملف CSV")
    
    all_tweets = []
    
    for file_path in csv_files:
        print(f"\nمعالجة: {os.path.basename(file_path)[:50]}...")
        tweets = process_csv_file(file_path)
        print(f"   -> {len(tweets)} تغريدة")
        all_tweets.extend(tweets)
    
    print(f"\n{'=' * 60}")
    print(f"إجمالي التغريدات المستخرجة: {len(all_tweets)}")
    
    # إزالة التكرارات
    seen_texts = set()
    unique_tweets = []
    for tweet in all_tweets:
        text_key = tweet['text'][:100]
        if text_key not in seen_texts:
            seen_texts.add(text_key)
            unique_tweets.append(tweet)
    
    print(f"بعد إزالة التكرارات: {len(unique_tweets)}")
    
    # فصل الإيجابية والسلبية
    positive_tweets = [t for t in unique_tweets if t['sentiment'] == 'positive']
    negative_tweets = [t for t in unique_tweets if t['sentiment'] == 'negative']
    
    # ترتيب حسب الجودة (مؤشرات الجمهور + المشاعر + التفاعل)
    def quality_score(t):
        return (
            t['indicator_count'] * 3 +
            t['sentiment_score'] * 2 +
            min(t['engagement'], 1000) / 100 +
            (1 if t['meltwater_sentiment'] == t['sentiment'] else 0)
        )
    
    positive_tweets.sort(key=quality_score, reverse=True)
    negative_tweets.sort(key=quality_score, reverse=True)
    
    print(f"\nالتغريدات الإيجابية: {len(positive_tweets)}")
    print(f"التغريدات السلبية: {len(negative_tweets)}")
    
    # أخذ أفضل 20 من كل نوع
    best_positive = positive_tweets[:20]
    best_negative = negative_tweets[:20]
    
    print(f"\n{'=' * 60}")
    print("🟢 أفضل 15 تغريدة إيجابية من الجمهور:")
    print("=" * 60)
    for i, tweet in enumerate(best_positive[:15], 1):
        print(f"\n{i}. @{tweet['author_handle']}")
        print(f"   {tweet['text'][:150]}...")
        print(f"   🔗 {tweet['url'][:60]}...")
        print(f"   📊 Reach: {tweet['reach']:,.0f} | Score: {tweet['sentiment_score']}")
    
    print(f"\n{'=' * 60}")
    print("🔴 أفضل 15 تغريدة سلبية من الجمهور:")
    print("=" * 60)
    for i, tweet in enumerate(best_negative[:15], 1):
        print(f"\n{i}. @{tweet['author_handle']}")
        print(f"   {tweet['text'][:150]}...")
        print(f"   🔗 {tweet['url'][:60]}...")
        print(f"   📊 Reach: {tweet['reach']:,.0f} | Score: {tweet['sentiment_score']}")
    
    # حفظ النتائج
    output = {
        'total_processed': len(all_tweets),
        'unique_tweets': len(unique_tweets),
        'positive_count': len(positive_tweets),
        'negative_count': len(negative_tweets),
        'best_positive': best_positive,
        'best_negative': best_negative
    }
    
    output_path = "/Users/taherirshaid/Desktop/Project/24-45-Platform/data/meltwater/deep_audience_tweets.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم حفظ النتائج في: {output_path}")

if __name__ == "__main__":
    main()
