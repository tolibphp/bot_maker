import os
import glob
import re

base_dir = r"C:\Users\user\Desktop\bot_maker\templates\pro_kino_bot"

prefixes = ['database', 'handlers', 'keyboards', 'middlewares', 'states', 'utils']

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix absolute imports
            for prefix in prefixes:
                content = re.sub(rf"^import {prefix}\.", f"import templates.pro_kino_bot.{prefix}.", content, flags=re.MULTILINE)
                content = re.sub(rf"^from {prefix}", f"from templates.pro_kino_bot.{prefix}", content, flags=re.MULTILINE)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
print("Imports fixed")
