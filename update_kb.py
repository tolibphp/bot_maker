import os

with open('master_bot/keyboards.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'callback_data="template:kino"' in line:
        lines[i] = '        [InlineKeyboardButton(text=" Oddiy Kino Bot - 10,000 so\'m", callback_data="template:kino", icon_custom_emoji_id=MOVIE_ID, style="primary")],\n'
        lines.insert(i + 1, '        [InlineKeyboardButton(text=" Professional Kino Bot - 30,000 so\'m", callback_data="template:pro_kino", icon_custom_emoji_id=MOVIE_ID, style="primary")],\n')
        break

with open('master_bot/keyboards.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
