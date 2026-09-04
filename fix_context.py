import os

context_code = '''import contextvars

current_admin_id = contextvars.ContextVar("current_admin_id", default=0)
'''

with open(r'C:\Users\user\Desktop\bot_maker\templates\pro_kino_bot\utils\context.py', 'w', encoding='utf-8') as f:
    f.write(context_code)

def replace_in_file(filepath, old, new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# admin.py
admin_path = r'C:\Users\user\Desktop\bot_maker\templates\pro_kino_bot\handlers\admin.py'
with open(admin_path, 'r', encoding='utf-8') as f:
    admin_code = f.read()
admin_code = admin_code.replace('from config import ADMIN_IDS', 'from templates.pro_kino_bot.utils.context import current_admin_id')
admin_code = admin_code.replace('def _is_admin(user_id: int) -> bool:\n    return user_id in ADMIN_IDS', 'def _is_admin(user_id: int) -> bool:\n    return user_id == current_admin_id.get()')
with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(admin_code)

# user.py
user_path = r'C:\Users\user\Desktop\bot_maker\templates\pro_kino_bot\handlers\user.py'
replace_in_file(user_path, 'from config import ADMIN_IDS', 'from templates.pro_kino_bot.utils.context import current_admin_id')
replace_in_file(user_path, 'if callback.from_user.id in ADMIN_IDS:', 'if callback.from_user.id == current_admin_id.get():')

# subscription.py
sub_path = r'C:\Users\user\Desktop\bot_maker\templates\pro_kino_bot\middlewares\subscription.py'
replace_in_file(sub_path, 'from config import ADMIN_IDS', 'from templates.pro_kino_bot.utils.context import current_admin_id')
replace_in_file(sub_path, 'if user_id in ADMIN_IDS:', 'if user_id == current_admin_id.get():')

# scheduler.py
sched_path = r'C:\Users\user\Desktop\bot_maker\templates\pro_kino_bot\utils\scheduler.py'
replace_in_file(sched_path, 'from config import ADMIN_IDS, DB_PATH', 'from templates.pro_kino_bot.utils.context import current_admin_id')
replace_in_file(sched_path, 'for admin_id in ADMIN_IDS:', 'for admin_id in [current_admin_id.get()]:')

print("Context variables injected")
