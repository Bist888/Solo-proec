import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean_build():
    """Очистка предыдущей сборки"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('cms.spec'):
        os.remove('cms.spec')

def copy_project_files():
    """Копирование файлов проекта"""
    # Создаем временные директории
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('media', exist_ok=True)

    # Копируем шаблоны
    if os.path.exists('cms_content/templates'):
        shutil.copytree('cms_content/templates', 'templates/cms_content', dirs_exist_ok=True)

    # Копируем статические файлы
    if os.path.exists('cms_content/static'):
        shutil.copytree('cms_content/static', 'static/cms_content', dirs_exist_ok=True)

def build_standalone():
    """Сборка standalone версии"""
    # Находим PyInstaller
    pyinstaller_cmd = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Python', 'Python312', 'Scripts', 'pyinstaller.exe')
    
    if not os.path.exists(pyinstaller_cmd):
        print("PyInstaller не найден. Устанавливаем...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)

    # Создаем spec файл
    current_dir = str(Path.cwd()).replace('\\', '/')
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['manage.py'],
    pathex=['{current_dir}'],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('media', 'media'),
        ('cms', 'cms'),
        ('cms_content', 'cms_content'),
        ('db.sqlite3', '.'),
    ],
    hiddenimports=[
        'django',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'cms_content',
        'cms_content.models',
        'cms_content.views',
        'cms_content.urls',
        'cms_content.forms',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='cms',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    with open('cms.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    # Запускаем PyInstaller
    subprocess.run([pyinstaller_cmd, 'cms.spec', '--clean'], check=True)

def main():
    """Основная функция сборки"""
    print("Начинаем сборку проекта...")
    
    # Очистка предыдущей сборки
    print("Очистка предыдущей сборки...")
    clean_build()
    
    # Копирование файлов проекта
    print("Копирование файлов проекта...")
    copy_project_files()
    
    # Сборка standalone версии
    print("Сборка standalone версии...")
    build_standalone()
    
    print("Сборка завершена успешно!")
    print("Исполняемый файл находится в папке dist/cms")

if __name__ == '__main__':
    main() 