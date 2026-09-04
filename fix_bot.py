import os

with open('templates/pro_kino_bot/bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove import
import_line = "from templates.pro_kino_bot.middlewares.subscription import SubscriptionMiddleware\n"
content = content.replace(import_line, "")

# Remove middleware registration
mw_line1 = "        self.dp.message.middleware(SubscriptionMiddleware(self.kino_db))\n"
mw_line2 = "        self.dp.callback_query.middleware(SubscriptionMiddleware(self.kino_db))\n"
content = content.replace(mw_line1, "")
content = content.replace(mw_line2, "")

with open('templates/pro_kino_bot/bot.py', 'w', encoding='utf-8') as f:
    f.write(content)
