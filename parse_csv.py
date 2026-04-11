import csv
import urllib.parse
import sys
import json

# Read the CSV with proper encoding
rows = []
with open('/Users/francogu/Desktop/kol_video_analysis/leona_report/data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    for row in reader:
        rows.append(row)

print(f"Total rows: {len(rows)}")
print(f"Headers ({len(headers)}):")
for i, h in enumerate(headers[:20]):
    print(f"  [{i}] {h}")

# Parse key fields
total_spend = 0
total_gmv = 0
themes = {}
kol_tiers = {}
content_types = {}
girl_boss_rows = []

for row in rows:
    # Get key fields
    spend = float(row.get('花费', 0) or 0)
    roi = float(row.get('roi', 0) or 0)
    gmv = float(row.get('GMV', 0) or 0)
    impressions = int(float(row.get('展示', 0) or 0))
    clicks = int(float(row.get('点击', 0) or 0))
    ctr = float(row.get('CTR', 0) or 0)
    cvr = float(row.get('CVR', 0) or 0)
    orders = int(float(row.get('订单数', 0) or 0))
    username = row.get('username', '')
    follower_tier = row.get('达人级别', '')
    theme = row.get('主题', '')
    content_type = row.get('内容类型', '')
    grade = row.get('评级', '')
    total_spend_col = float(row.get('总花费', 0) or 0)
    total_gmv_col = float(row.get('总GMV', 0) or 0)
    total_roi = float(row.get('总ROI', 0) or 0)
    
    total_spend += total_spend_col
    total_gmv += total_gmv_col
    
    # Count themes
    if theme:
        themes[theme] = themes.get(theme, 0) + 1
    
    # Count tiers
    if follower_tier:
        kol_tiers[follower_tier] = kol_tiers.get(follower_tier, 0) + 1
    
    # Girl boss detection
    theme_lower = (theme or '').lower()
    if 'girl' in theme_lower or 'girlboss' in theme_lower or 'boss' in theme_lower:
        girl_boss_rows.append({
            'username': username,
            'theme': theme,
            'spend': total_spend_col,
            'gmv': total_gmv_col,
            'roi': total_roi,
            'impressions': impressions,
            'ctr': ctr,
            'orders': orders,
            'tier': follower_tier,
            'grade': grade
        })

print(f"\nTotal spend: {total_spend:.2f}")
print(f"Total GMV: {total_gmv:.2f}")
print(f"\nThemes ({len(themes)}):")
for t, c in sorted(themes.items(), key=lambda x: -x[1])[:30]:
    print(f"  {t}: {c}")

print(f"\nKOL Tiers:")
for t, c in sorted(kol_tiers.items(), key=lambda x: -x[1]):
    print(f"  {t}: {c}")

print(f"\nGirl Boss related content: {len(girl_boss_rows)}")
for r in girl_boss_rows:
    print(f"  @{r['username']} | {r['theme']} | spend={r['spend']} | gmv={r['gmv']} | roi={r['roi']} | tier={r['tier']}")
