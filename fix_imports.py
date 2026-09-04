import os

def replace_in_folder(folder_path, old_text, new_text):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_text in content:
                    content = content.replace(old_text, new_text)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {file_path}")

replace_in_folder('templates/pro_kino_bot', 'templates.kino_bot', 'templates.pro_kino_bot')
