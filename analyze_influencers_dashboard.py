#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_influencers_dashboard.py
تحليل المؤثرين في الصورة الإعلامية - حسب المنهجية الصارمة
"""

import pandas as pd
import re
from collections import Counter

# قراءة البيانات
csv_path = "static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv"

df = pd.read_csv(csv_path, encoding='utf-16-le', sep='\t', low_memory=False)

# فلترة الإعلام التقليدي (online news) فقط
traditional_df = df[df['Source Type'] == 'online news'].copy()
total_articles = len(traditional_df)

print("="*80)
print(f"📊 تحليل المؤثرين في الصورة الإعلامية")
print(f"📰 إجمالي التغطيات (الإعلام التقليدي): {total_articles:,}")
print("="*80)

def search_in_text(df, pattern, columns=['Title', 'Hit Sentence']):
    mask = pd.Series(False, index=df.index)
    for col in columns:
        if col in df.columns:
            mask |= df[col].str.contains(pattern, case=False, na=False, regex=True)
    return df[mask]

def analyze_sentiment_for_pattern(df, pattern):
    matches = search_in_text(df, pattern)
    if len(matches) == 0:
        return {'total': 0, 'positive': 0, 'neutral': 0, 'negative': 0,
                'pos_pct': 0, 'neu_pct': 0, 'neg_pct': 0}
    
    sentiments = matches['Sentiment'].str.lower().value_counts()
    total = len(matches)
    pos = sentiments.get('positive', 0)
    neu = sentiments.get('neutral', 0)
    neg = sentiments.get('negative', 0)
    
    return {
        'total': total, 'positive': pos, 'neutral': neu, 'negative': neg,
        'pos_pct': round(pos / total * 100) if total > 0 else 0,
        'neu_pct': round(neu / total * 100) if total > 0 else 0,
        'neg_pct': round(neg / total * 100) if total > 0 else 0
    }

# 1. مسؤولون رياضيون
print("\n" + "="*80)
print("👔 1. مسؤولون رياضيون")
print("="*80)
fifa_results = analyze_sentiment_for_pattern(traditional_df, r'FIFA|الفيفا|إنفانتينو|انفانتينو|Infantino')
organizing_results = analyze_sentiment_for_pattern(traditional_df, r'اللجنة العليا|Supreme Committee|اللجنة المنظمة|التنظيم المحكم|منظمي البطولة')
federation_results = analyze_sentiment_for_pattern(traditional_df, r'AFC|CAF|UEFA|الاتحاد الآسيوي|الاتحاد الأفريقي|الاتحاد الأوروبي')

officials_pos = fifa_results['positive'] + organizing_results['positive'] + federation_results['positive']
officials_neu = fifa_results['neutral'] + organizing_results['neutral'] + federation_results['neutral']
officials_neg = fifa_results['negative'] + organizing_results['negative'] + federation_results['negative']
officials_total = fifa_results['total'] + organizing_results['total'] + federation_results['total']

print(f"\n📌 FIFA وإنفانتينو: {fifa_results['total']:,}")
print(f"   إيجابي: {fifa_results['positive']} | محايد: {fifa_results['neutral']} | سلبي: {fifa_results['negative']}")
print(f"\n📌 اللجنة المنظمة: {organizing_results['total']:,}")
print(f"   إيجابي: {organizing_results['positive']} | محايد: {organizing_results['neutral']} | سلبي: {organizing_results['negative']}")
print(f"\n📌 رؤساء الاتحادات: {federation_results['total']:,}")
print(f"   إيجابي: {federation_results['positive']} | محايد: {federation_results['neutral']} | سلبي: {federation_results['negative']}")
print(f"\n🔢 الإجمالي: {officials_total:,}")
if officials_total > 0:
    print(f"   إيجابي: {round(officials_pos/officials_total*100)}% | محايد: {round(officials_neu/officials_total*100)}% | سلبي: {round(officials_neg/officials_total*100)}%")

# 2. خبراء ومحللون
print("\n" + "="*80)
print("🎓 2. خبراء ومحللون")
print("="*80)
analysts_results = analyze_sentiment_for_pattern(traditional_df, r'محلل|تحليل رياضي|خبير كرة|analyst|analysis|tactical')
academic_results = analyze_sentiment_for_pattern(traditional_df, r'دراسة|بحث|أكاديمي|جامعة|study|research|university|academic')
expert_opinions_results = analyze_sentiment_for_pattern(traditional_df, r'قال الخبير|رأي|صرح|يرى المحلل|في رأيه|وفق الخبير')

experts_pos = analysts_results['positive'] + academic_results['positive'] + expert_opinions_results['positive']
experts_neu = analysts_results['neutral'] + academic_results['neutral'] + expert_opinions_results['neutral']
experts_neg = analysts_results['negative'] + academic_results['negative'] + expert_opinions_results['negative']
experts_total = analysts_results['total'] + academic_results['total'] + expert_opinions_results['total']

print(f"\n📌 تحليلات رياضية: {analysts_results['total']:,}")
print(f"📌 دراسات أكاديمية: {academic_results['total']:,}")
print(f"📌 آراء متخصصة: {expert_opinions_results['total']:,}")
print(f"\n🔢 الإجمالي: {experts_total:,}")
if experts_total > 0:
    print(f"   إيجابي: {round(experts_pos/experts_total*100)}% | محايد: {round(experts_neu/experts_total*100)}% | سلبي: {round(experts_neg/experts_total*100)}%")

# 3. إعلاميون ومحررون
print("\n" + "="*80)
print("🎙️ 3. إعلاميون ومحررون")
print("="*80)
correspondents_results = analyze_sentiment_for_pattern(traditional_df, r'مراسل|correspondent|reporter|مبعوث|من الملعب|من الدوحة')
commentators_results = analyze_sentiment_for_pattern(traditional_df, r'معلق|commentator|commentary|التعليق الرياضي')
journalists_results = analyze_sentiment_for_pattern(traditional_df, r'صحفي|صحافي|كاتب رياضي|journalist|sports writer|محرر رياضي')

media_people_pos = correspondents_results['positive'] + commentators_results['positive'] + journalists_results['positive']
media_people_neu = correspondents_results['neutral'] + commentators_results['neutral'] + journalists_results['neutral']
media_people_neg = correspondents_results['negative'] + commentators_results['negative'] + journalists_results['negative']
media_people_total = correspondents_results['total'] + commentators_results['total'] + journalists_results['total']

print(f"\n📌 مراسلون ميدانيون: {correspondents_results['total']:,}")
print(f"📌 معلقون رياضيون: {commentators_results['total']:,}")
print(f"📌 صحفيون متخصصون: {journalists_results['total']:,}")
print(f"\n🔢 الإجمالي: {media_people_total:,}")
if media_people_total > 0:
    print(f"   إيجابي: {round(media_people_pos/media_people_total*100)}% | محايد: {round(media_people_neu/media_people_total*100)}% | سلبي: {round(media_people_neg/media_people_total*100)}%")

# 4. وسائل الإعلام
print("\n" + "="*80)
print("📺 4. وسائل الإعلام")
print("="*80)
source_counts = traditional_df['Source Name'].value_counts()

news_agencies = ['Reuters', 'AFP', 'AP', 'QNA', 'WAM', 'SPA', 'KUNA', 'وكالة', 'Agence', 'Agency']
arabic_papers = ['الراية', 'الشرق', 'الأهرام', 'اليوم السابع', 'الوطن', 'الجزيرة', 'الرياض', 'عكاظ', 'الاتحاد', 'البيان']
sports_sites = ['Goal', 'ESPN', 'beIN', 'Kooora', 'كورة', 'الكأس', 'FilGoal', 'YallaKora', 'يلا', 'في الجول', 'Sport360']

news_agency_count = sum(source_counts[s] for s in source_counts.index if any(a.lower() in str(s).lower() for a in news_agencies))
arabic_papers_count = sum(source_counts[s] for s in source_counts.index if any(p in str(s) for p in arabic_papers))
sports_sites_count = sum(source_counts[s] for s in source_counts.index if any(site.lower() in str(s).lower() for site in sports_sites))

print(f"\n📌 وكالات الأنباء الدولية: {news_agency_count:,}")
print(f"📌 الصحف العربية: {arabic_papers_count:,}")
print(f"📌 المواقع الرياضية: {sports_sites_count:,}")
print(f"\n🔢 الإجمالي (كل المصادر): {total_articles:,}")

# تحليل المشاعر الكلي
sentiment_counts = traditional_df['Sentiment'].str.lower().value_counts()
media_pos = sentiment_counts.get('positive', 0)
media_neu = sentiment_counts.get('neutral', 0)
media_neg = sentiment_counts.get('negative', 0)

print(f"\n📊 المشاعر الكلية للتغطيات:")
print(f"   إيجابي: {media_pos:,} ({round(media_pos/total_articles*100)}%)")
print(f"   محايد: {media_neu:,} ({round(media_neu/total_articles*100)}%)")
print(f"   سلبي: {media_neg:,} ({round(media_neg/total_articles*100)}%)")

# الملخص النهائي
print("\n" + "="*80)
print("📋 ملخص Dashboard الشريحة 30")
print("="*80)

print(f"""
الفئة 1: مسؤولون رياضيون
  العدد: {officials_total:,}
  - FIFA وإنفانتينو: {fifa_results['total']:,} ({round(fifa_results['total']/officials_total*100) if officials_total > 0 else 0}%)
  - اللجنة المنظمة: {organizing_results['total']:,} ({round(organizing_results['total']/officials_total*100) if officials_total > 0 else 0}%)
  - رؤساء الاتحادات: {federation_results['total']:,} ({round(federation_results['total']/officials_total*100) if officials_total > 0 else 0}%)

الفئة 2: خبراء ومحللون
  العدد: {experts_total:,}
  - تحليلات رياضية: {analysts_results['total']:,} ({round(analysts_results['total']/experts_total*100) if experts_total > 0 else 0}%)
  - دراسات أكاديمية: {academic_results['total']:,} ({round(academic_results['total']/experts_total*100) if experts_total > 0 else 0}%)
  - آراء متخصصة: {expert_opinions_results['total']:,} ({round(expert_opinions_results['total']/experts_total*100) if experts_total > 0 else 0}%)

الفئة 3: إعلاميون ومحررون
  العدد: {media_people_total:,}
  - مراسلون ميدانيون: {correspondents_results['total']:,} ({round(correspondents_results['total']/media_people_total*100) if media_people_total > 0 else 0}%)
  - معلقون رياضيون: {commentators_results['total']:,} ({round(commentators_results['total']/media_people_total*100) if media_people_total > 0 else 0}%)
  - صحفيون متخصصون: {journalists_results['total']:,} ({round(journalists_results['total']/media_people_total*100) if media_people_total > 0 else 0}%)

الفئة 4: وسائل الإعلام
  العدد: {total_articles:,}
  - وكالات الأنباء: {news_agency_count:,} ({round(news_agency_count/total_articles*100)}%)
  - الصحف العربية: {arabic_papers_count:,} ({round(arabic_papers_count/total_articles*100)}%)
  - المواقع الرياضية: {sports_sites_count:,} ({round(sports_sites_count/total_articles*100)}%)
""")
