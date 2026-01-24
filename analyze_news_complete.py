# -*- coding: utf-8 -*-
"""
تحليل شامل لبيانات الإعلام التقليدي
وزارة الرياضة والشباب القطرية
"""

import pandas as pd
import os
import json
import warnings
warnings.filterwarnings('ignore')

BASE_PATH = "static/data/meltwater/Qatr"

# المسارات مع مجلدات البحث المتعددة
TRACKS = {
    'track1': {
        'name': 'وزارة الرياضة والشباب القطرية',
        'path': 'وزارة الرياضة والشباب القطرية ',
        'search_folders': ['x', 'analytics', 'overview']
    },
    'track2': {
        'name': 'الفعاليات الكبرى',
        'path': 'الفعاليات الكبرى',
        'search_folders': ['Analytic', 'X', 'Overview']
    },
    'track3': {
        'name': 'الفعاليات الرياضية والصحية المحلية',
        'path': 'الفعاليات الرياضية والصحية المحلية',
        'search_folders': ['analytics', 'x', 'overview']
    },
    'track4': {
        'name': 'الفعاليات التراثية والوطنية',
        'path': 'الفعاليات التراثية والوطنية',
        'search_folders': ['Analytics', 'x', 'Overview']
    }
}

def safe_read_csv(filepath):
    """قراءة ملف CSV"""
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'cp1256']
    for enc in encodings:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except:
            continue
    return None

def find_file(base_path, track_path, folders, filename_pattern):
    """البحث عن ملف في مجلدات متعددة"""
    for folder in folders:
        folder_path = os.path.join(base_path, track_path, folder)
        if os.path.exists(folder_path):
            for f in os.listdir(folder_path):
                if filename_pattern in f and f.endswith('.csv'):
                    return os.path.join(folder_path, f)
    return None

def classify_source(source_name):
    """تصنيف المصدر"""
    source_lower = str(source_name).lower()
    qatar_kw = ['qatar', 'qna', 'الراية', 'الشرق', 'العرب', 'الوطن', 'قطر', 'peninsula', 'gulf times', 'tribune', 'الكأس', 'مشيرب']
    arabic_kw = ['russia today', 'msn', 'klyoum', 'مصرس', 'العربي', 'الزهراء', 'نبض']
    
    if any(kw in source_lower for kw in qatar_kw):
        return 'قطري'
    elif any(kw in source_lower for kw in arabic_kw):
        return 'عربي'
    return 'دولي'

def main():
    print("="*100)
    print("🏟️ تحليل شامل للإعلام التقليدي - وزارة الرياضة والشباب القطرية")
    print("="*100)
    
    all_results = {
        'summary': {
            'total_publications': 0,
            'total_unique_sources': 0,
            'qatar_sources_count': 0,
            'arabic_sources_count': 0,
            'international_sources_count': 0
        },
        'tracks': {}
    }
    
    all_sources = {}
    
    for track_id, track_info in TRACKS.items():
        print(f"\n{'='*80}")
        print(f"📊 {track_info['name']}")
        print("="*80)
        
        # البحث عن ملف المصادر الإعلامية
        editorial_file = find_file(BASE_PATH, track_info['path'], 
                                   track_info['search_folders'], 'Top_Editorial_Sources')
        
        track_data = {
            'name': track_info['name'],
            'total_publications': 0,
            'sources': [],
            'classification': {'قطري': 0, 'عربي': 0, 'دولي': 0}
        }
        
        if editorial_file:
            df = safe_read_csv(editorial_file)
            if df is not None and not df.empty:
                # استخراج البيانات
                total_pubs = int(df['Publications'].sum())
                track_data['total_publications'] = total_pubs
                all_results['summary']['total_publications'] += total_pubs
                
                print(f"\n📰 إجمالي المنشورات: {total_pubs:,}")
                print(f"📋 عدد المصادر: {len(df)}")
                
                print(f"\n🏆 أهم 10 مصادر:")
                print("-"*60)
                
                for i, (source, row) in enumerate(df.head(10).iterrows()):
                    pubs = int(row['Publications'])
                    cat = classify_source(source)
                    print(f"   {i+1}. {source}")
                    print(f"      [{cat}] - {pubs:,} منشور")
                    
                    track_data['sources'].append({
                        'name': source,
                        'publications': pubs,
                        'category': cat
                    })
                    
                    # جمع في المصادر الكلية
                    if source not in all_sources:
                        all_sources[source] = {'total': 0, 'category': cat}
                    all_sources[source]['total'] += pubs
                
                # تصنيف جميع المصادر
                for source in df.index:
                    cat = classify_source(source)
                    track_data['classification'][cat] += 1
                
                print(f"\n📊 توزيع المصادر:")
                print(f"   • مصادر قطرية: {track_data['classification']['قطري']}")
                print(f"   • مصادر عربية: {track_data['classification']['عربي']}")
                print(f"   • مصادر دولية: {track_data['classification']['دولي']}")
        else:
            print("⚠️ لم يتم العثور على بيانات")
        
        all_results['tracks'][track_id] = track_data
    
    # الملخص الشامل
    print("\n" + "="*100)
    print("📊 الملخص التنفيذي الشامل")
    print("="*100)
    
    all_results['summary']['total_unique_sources'] = len(all_sources)
    
    # حساب التصنيفات الكلية
    for src, data in all_sources.items():
        if data['category'] == 'قطري':
            all_results['summary']['qatar_sources_count'] += 1
        elif data['category'] == 'عربي':
            all_results['summary']['arabic_sources_count'] += 1
        else:
            all_results['summary']['international_sources_count'] += 1
    
    print(f"\n📌 إجمالي حجم الحديث في الإعلام التقليدي: {all_results['summary']['total_publications']:,} منشور")
    print(f"📌 عدد المصادر الفريدة: {all_results['summary']['total_unique_sources']}")
    print(f"\n📊 توزيع المصادر الكلي:")
    print(f"   • قطرية: {all_results['summary']['qatar_sources_count']}")
    print(f"   • عربية: {all_results['summary']['arabic_sources_count']}")
    print(f"   • دولية: {all_results['summary']['international_sources_count']}")
    
    print(f"\n📈 توزيع المنشورات حسب المسار:")
    print("-"*60)
    for track_id, data in all_results['tracks'].items():
        pct = (data['total_publications'] / all_results['summary']['total_publications'] * 100) if all_results['summary']['total_publications'] > 0 else 0
        print(f"   • {data['name']}: {data['total_publications']:,} ({pct:.1f}%)")
    
    # أهم 15 مصدر عام
    print(f"\n🏆 أهم 15 مصدر إعلامي (إجمالي):")
    print("-"*60)
    sorted_sources = sorted(all_sources.items(), key=lambda x: x[1]['total'], reverse=True)[:15]
    for i, (src, data) in enumerate(sorted_sources, 1):
        print(f"   {i}. {src}: {data['total']:,} [{data['category']}]")
    
    # حفظ النتائج
    with open('news_analysis_complete.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ تم حفظ النتائج في: news_analysis_complete.json")
    
    return all_results

if __name__ == "__main__":
    main()
