import os

with open('bot_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
old_import = "from templates.kino_bot import KinoBot"
new_import = "from templates.kino_bot import KinoBot\nfrom templates.pro_kino_bot.bot import KinoBot as ProKinoBot"

if old_import in content:
    content = content.replace(old_import, new_import)

# Add elif branch
old_branch = """            elif bot_data["template_type"] == "kino":
                bot_instance = KinoBot(
                    bot_token=bot_data["bot_token"],
                    admin_id=bot_data["owner_telegram_id"],
                    db_path=bot_data["db_path"],
                    bot_id=bot_id
                )"""

new_branch = """            elif bot_data["template_type"] == "kino":
                bot_instance = KinoBot(
                    bot_token=bot_data["bot_token"],
                    admin_id=bot_data["owner_telegram_id"],
                    db_path=bot_data["db_path"],
                    bot_id=bot_id
                )
            elif bot_data["template_type"] == "pro_kino":
                bot_instance = ProKinoBot(
                    bot_token=bot_data["bot_token"],
                    admin_id=bot_data["owner_telegram_id"],
                    db_path=bot_data["db_path"],
                    bot_id=bot_id
                )"""

if old_branch in content:
    content = content.replace(old_branch, new_branch)

with open('bot_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated bot_manager.py")
