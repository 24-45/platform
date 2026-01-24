import pandas as pd
from collections import Counter

file_path = 'static/data/meltwater/Qatr/الفعاليات الكبرى/Overview/______________كأس_العرب_OR_مونديال_العرب_OR_بطولة_ - Jan 19, 2026 - 9 11 49 AM.csv'

df = pd.read_csv(file_path, sep='\t', encoding='utf-16-le', low_memory=False)
trad = df[df['Source Type'] == 'online news'].copy()

print(f'=== تحليل Keyphrases ===')
print(f'إجمالي: {len(trad)}')

# Get all keyphrases
all_keyphrases = []
for kp in trad['Keyphrases'].dropna():
    phrases = [p.strip() for p in str(kp).split(';')]
    all_keyphrases.extend(phrases)

# Count keyphrases
kp_counts = Counter(all_keyphrases)
print('\nأعلى 30 keyphrase:')
for phrase, count in kp_counts.most_common(30):
    if phrase and len(phrase) > 2:
        pct = (count / len(trad)) * 100
        print(f'  {phrase}: {count} ({pct:.1f}%)')
