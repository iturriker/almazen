import os

def tree(name, file, ignore_dirs=None, ignore_files=None):
    with open(file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk('.'):
            # Ignorar carpetas en ignore_dirs
            for dir_name in ignore_dirs:
                if dir_name in dirs:
                    dirs.remove(dir_name)

            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * level
            folder_name = name if root == '.' else os.path.basename(root)
            f.write(f'{indent}{folder_name}/\n')
            subindent = ' ' * 4 * (level + 1)

            # Ignorar archivos en ignore_files
            for file_name in files:
                if file_name not in ignore_files:
                    f.write(f'{subindent}{file_name}\n')

project_name = 'almazen'
output_file = 'structure.txt'
ignore_dirs = ['.git', '__pycache__']
ignore_files = ['structure.py', 'structure.txt', 'LICENSE', 'README.md']

tree(project_name, output_file, ignore_dirs=ignore_dirs, ignore_files=ignore_files)