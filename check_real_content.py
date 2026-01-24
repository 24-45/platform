#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import json

BASE_PATH = Path("static/data/meltwater/qatr 4")

def read_csv(fp):
    for enc in ['utf-16', 'utf-8', 'utf-8-sig']:
        try:
            df = pd.read_csv(fp, encoding=enc, sep='\t')
            if len(df.columns) > 5:
                return df
        except:
            pass
    return None

def get_event(fp):
    s = str(fp)
    if 'العرب' in s: return 'كأس العرب'
    if 'UFC' in s: return 'UFC قطر'
    if 'فورمولا' in s or 'Grand Prix' in s: return 'F1 قطر'
    if 'U-17' in s or 'تحت 17' in s: return 'U-17 WC'
    if 'WTT' in s: return 'WTT'
    if 'T100' in s: return 'T100'
    if 'Intercontinental' in s: return 'Intercontinental'
    if 'وزارة' in s: return 'وزارة'
    return 'other'

results = []
print("="*60)
print("تحليل ملفات Meltwater للتحقق من المحتوى الأكثر تفاعلاً")
print("="*60)

for f in BASE_PATH.rglob("*.csv"):
    df = read_csv(f)
    if df is None:
        continue
    
    event = get_event(f)
    folder_type = 'X insights' if 'X insights' in str(f) else 'overview' if 'overview' in str(f) else 'other'
    
    print(f"\n📁 {f.name[:50]}")
    print(f"   الحدث: {event} | النوع: {folder_type}")
    print(f"   الأعمدة ({len(df.columns)}): {list(df.columns)[:6]}")
    print(f"   الصفوف: {len(df)}")
    
    # أعمدة التفاعل
    eng = [c for c in df.columns if 'engagement' in c.lower() or 'reach' in c.lower() or 'view' in c.lower() or 'like' in c.lower()]
    if eng:
        print(f"   📊 أعمدة التفاعل: {eng}")
        
        for col in eng:
            try:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
                top = df.nlargest(3, col)
                for i, row in top.iterrows():
                    text_cols = [c for c in df.columns if 'hit' in c.lower() or 'title' in c.lower() or 'headline' in c.lower()]
                    text = ""
                    for tc in text_cols:
                        if pd.notna(row.get(tc)):
                            text = str(row[tc])[:100]
                            break
                    if not text:
                        for c in df.columns:
                            v = row.get(c)
                            if pd.notna(v) and isinstance(v, str) and len(v) > 30 and 'http' not in v[:10]:
                                text = v[:100]
                                break
                    
                    reach = 0
                    for c in df.columns:
                        if 'reach' in c.lower() and pd.notna(row.get(c)):
                            try:
                                reach = float(str(row[c]).replace(',', ''))
                            except:
                                pass
                    
                    results.append({
                        'event': event,
                        'engagement': float(row[col]) if pd.notna(row[col]) else 0,
                        'reach': reach,
                        'text': text,
                        'column': col
                    })
            except Exception as e:
                print(f"   ❌ خطأ: {e}")

# الترتيب والطباعة
results = sorted(results, key=lambda x: x['engagement'], reverse=True)
unique = []
seen = set()
for r in results:
    key = r['text'][:30] if r['text'] else str(r['engagement'])
    if key not in seen:
        seen.add(key)
        unique.append(r)

print("\n" + "="*80)
print("🏆 المحتوى الأكثر تفاعلاً الحقيقي:")
print("="*80)

for i, r in enumerate(unique[:15], 1):
    print(f"\n{i}. الحدث: {r['event']}")
    print(f"   التفاعل: {r['engagement']:,.0f}")
    print(f"   الوصول: {r['reach']:,.0f}")
    print(f"   المحتوى: {r['text'][:80]}...")

# حفظ النتائج
with open('real_top_content.json', 'w', encoding='utf-8') as f:
    json.dump(unique[:20], f, ensure_ascii=False, indent=2)
print("\n✅ تم حفظ النتائج في real_top_content.json")
