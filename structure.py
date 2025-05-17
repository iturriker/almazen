import os

def tree(path, name, file):
    with open(file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * level
            folder_name = name if root == path else os.path.basename(root)
            f.write(f'{indent}{folder_name}/\n')
            subindent = ' ' * 4 * (level + 1)
            for file_name in files:
                f.write(f'{subindent}{file_name}\n')

tree('.', 'almazen', 'structure.txt')