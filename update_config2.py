import os

with open('config.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '"kino":' in line:
        # We replace the old kino line, and insert the pro_kino line right after
        lines[i] = '    "kino": {"name": "🎬 Oddiy Kino Bot", "price": 10_000, "module": "kino_bot", "daily_price": 2000},\n'
        lines.insert(i + 1, '    "pro_kino": {"name": "🎬🔥 Professional Kino Bot", "price": 30_000, "module": "pro_kino_bot", "daily_price": 5000},\n')
        break

with open('config.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
