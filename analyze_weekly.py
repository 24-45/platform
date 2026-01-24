import pandas as pd

file_path = 'static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv'

df = pd.read_csv(file_path, sep='\t', encoding='utf-16-le', low_memory=False)

# Filter for online news only
trad = df[df['Source Type'] == 'online news'].copy()

# Parse dates
trad['Date'] = pd.to_datetime(trad['Date'], format='%Y-%m-%d', errors='coerce')

# Add week number (ISO week)
trad['Week'] = trad['Date'].dt.isocalendar().week
trad['Year'] = trad['Date'].dt.year

# Group by week
weekly = trad.groupby(['Year', 'Week']).size().reset_index(name='Count')
weekly = weekly.sort_values(['Year', 'Week'])

print('=== التوزيع الأسبوعي (الإعلام التقليدي فقط) ===')
for _, row in weekly.iterrows():
    print(f'W{int(row["Week"]):02d} ({int(row["Year"])}): {row["Count"]} تغطية')

print(f'\nإجمالي: {trad.shape[0]}')
