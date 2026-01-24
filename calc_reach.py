import pandas as pd
import os

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
    df = pd.read_csv(fp, encoding='utf-16-le', sep='\t', low_memory=False)
    all_dfs.append(df)

merged = pd.concat(all_dfs, ignore_index=True)
merged = merged.drop_duplicates(subset=['Document ID'])

# حساب الوصول
reach = pd.to_numeric(merged['Reach'], errors='coerce').sum()
engagement = pd.to_numeric(merged['Engagement'], errors='coerce').sum()

print(f'Total Records: {len(merged):,}')
print(f'Total Reach: {reach:,.0f}')
print(f'Total Engagement: {engagement:,.0f}')
if reach > 1e9:
    print(f'Reach Formatted: {reach/1e9:.2f}B')
else:
    print(f'Reach Formatted: {reach/1e6:.0f}M')
