import pandas as pd
import os
import json

BASE_PATH = 'static/data/meltwater/Qatr01'

def find_csv(path):
    files = []
    for root, dirs, f in os.walk(path):
        for file in f:
            if file.endswith('.csv'):
                files.append(os.path.join(root, file))
    return files

csv_files = find_csv(BASE_PATH)
all_dfs = []

for fp in csv_files:
    if '/x/' in fp.lower():
        src = 'X Platform'
    else:
        src = 'Traditional Media'
    
    if 'الفعاليات الكبرى' in fp:
        cat = 'Global Events'
    elif 'الفعاليات التراثية' in fp:
        cat = 'Heritage Events'
    elif 'الفعاليات الرياضية' in fp:
        cat = 'Sports Events'
    elif 'وزارة الرياضة' in fp:
        cat = 'Ministry'
    else:
        cat = 'Other'
    
    df = pd.read_csv(fp, encoding='utf-16-le', sep='\t')
    df['Source_Type'] = src
    df['Category'] = cat
    all_dfs.append(df)

merged = pd.concat(all_dfs, ignore_index=True)
merged = merged.drop_duplicates(subset=['Document ID'])

# تفاصيل كل فئة حسب المصدر
result = {}
for cat in merged['Category'].unique():
    cat_df = merged[merged['Category'] == cat]
    trad = len(cat_df[cat_df['Source_Type'] == 'Traditional Media'])
    x = len(cat_df[cat_df['Source_Type'] == 'X Platform'])
    result[cat] = {'total': len(cat_df), 'traditional': trad, 'x': x}

print(json.dumps(result, ensure_ascii=False, indent=2))
print()
print('Total:', len(merged))
print('Traditional:', len(merged[merged['Source_Type'] == 'Traditional Media']))
print('X Platform:', len(merged[merged['Source_Type'] == 'X Platform']))
