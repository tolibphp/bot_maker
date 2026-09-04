import os

with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the templates block
old_block = '''TEMPLATES = {
    "kino": {"name": "?? Kino Bot", "price": 30_000, "module": "kino_bot", "daily_price": 5000},
    "stars": {"name": "-?? Stars Referral Bot", "price": 10_000, "module": "stars_bot", "daily_price": 2000},
    "money": {"name": "?' Premium Pul Ishlash", "price": 10_000, "module": "money_bot", "daily_price": 2000},
    "downloader": {"name": "?"? Video Yuklovchi Bot", "price": 10_000, "module": "downloader_bot", "daily_price": 2000}
}'''

new_block = '''TEMPLATES = {
    "kino": {"name": "?? Oddiy Kino Bot", "price": 10_000, "module": "kino_bot", "daily_price": 2000},
    "pro_kino": {"name": "?? Professional Kino Bot", "price": 30_000, "module": "pro_kino_bot", "daily_price": 5000},
    "stars": {"name": "-?? Stars Referral Bot", "price": 10_000, "module": "stars_bot", "daily_price": 2000},
    "money": {"name": "?' Premium Pul Ishlash", "price": 10_000, "module": "money_bot", "daily_price": 2000},
    "downloader": {"name": "?"? Video Yuklovchi Bot", "price": 10_000, "module": "downloader_bot", "daily_price": 2000}
}'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated config.py")
else:
    print("Could not find the exact block in config.py")
