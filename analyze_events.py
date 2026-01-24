import pandas as pd
import re

file_path = 'static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv'

df = pd.read_csv(file_path, sep='\t', encoding='utf-16-le', low_memory=False)

# Filter for online news only (Traditional Media)
trad = df[df['Source Type'] == 'online news'].copy()

print(f"إجمالي الإعلام التقليدي: {len(trad)}")
print("="*60)

# Create a combined text column for searching
trad['combined_text'] = trad['Title'].fillna('') + ' ' + trad['Opening Text'].fillna('') + ' ' + trad['Hit Sentence'].fillna('')

# Define event patterns
events = {
    'كأس العرب 2025': r'كأس العرب|Arab Cup|مونديال العرب|بطولة العرب',
    'FIFA U-17': r'U-17|U17|تحت 17|كأس العالم للناشئين|FIFA U17|Under.17|under 17',
    'F1 قطر': r'F1|Formula|فورمولا|Formula 1|Grand Prix|جائزة قطر الكبرى',
    'UFC Qatar': r'UFC|يو إف سي|فنون القتال|MMA|Mixed Martial Arts',
    'World Padel': r'Padel|بادل|Premier Padel|World Padel'
}

# Analyze each event
results = {}
total_categorized = 0

for event_name, pattern in events.items():
    mask = trad['combined_text'].str.contains(pattern, case=False, na=False, regex=True)
    count = mask.sum()
    results[event_name] = count
    total_categorized += count
    percentage = (count / len(trad)) * 100
    print(f"{event_name}: {count} تغطية ({percentage:.1f}%)")

print("="*60)
print(f"المجموع المصنف: {total_categorized}")
print(f"غير مصنف/متداخل: قد يكون هناك تداخل بين الفئات")

# Check for overlap
print("\n" + "="*60)
print("فحص التداخل بين الفئات:")

# Create masks for each event
masks = {}
for event_name, pattern in events.items():
    masks[event_name] = trad['combined_text'].str.contains(pattern, case=False, na=False, regex=True)

# Calculate unique counts (non-overlapping)
arab_cup_only = masks['كأس العرب 2025'] & ~masks['FIFA U-17'] & ~masks['F1 قطر'] & ~masks['UFC Qatar'] & ~masks['World Padel']
u17_only = masks['FIFA U-17'] & ~masks['كأس العرب 2025'] & ~masks['F1 قطر'] & ~masks['UFC Qatar'] & ~masks['World Padel']
f1_only = masks['F1 قطر'] & ~masks['كأس العرب 2025'] & ~masks['FIFA U-17'] & ~masks['UFC Qatar'] & ~masks['World Padel']
ufc_only = masks['UFC Qatar'] & ~masks['كأس العرب 2025'] & ~masks['FIFA U-17'] & ~masks['F1 قطر'] & ~masks['World Padel']
padel_only = masks['World Padel'] & ~masks['كأس العرب 2025'] & ~masks['FIFA U-17'] & ~masks['F1 قطر'] & ~masks['UFC Qatar']

print(f"\nالتغطيات الحصرية (بدون تداخل):")
print(f"كأس العرب 2025 (حصري): {arab_cup_only.sum()}")
print(f"FIFA U-17 (حصري): {u17_only.sum()}")
print(f"F1 قطر (حصري): {f1_only.sum()}")
print(f"UFC Qatar (حصري): {ufc_only.sum()}")
print(f"World Padel (حصري): {padel_only.sum()}")

# Total unique
total_unique = arab_cup_only.sum() + u17_only.sum() + f1_only.sum() + ufc_only.sum() + padel_only.sum()
print(f"\nإجمالي الحصري: {total_unique}")

# Any event coverage
any_event = masks['كأس العرب 2025'] | masks['FIFA U-17'] | masks['F1 قطر'] | masks['UFC Qatar'] | masks['World Padel']
print(f"أي فعالية (مع التداخل): {any_event.sum()}")

# Not categorized
not_categorized = ~any_event
print(f"غير مصنف في أي فعالية: {not_categorized.sum()}")

# Calculate percentages for slide
print("\n" + "="*60)
print("النسب المئوية للشريحة (من الإعلام التقليدي 12,070):")
total = len(trad)
for event_name in results:
    pct = (results[event_name] / total) * 100
    print(f"{event_name}: {pct:.1f}%")
