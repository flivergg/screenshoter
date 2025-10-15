@echo off
chcp 65001
echo Установка зависимостей...
pip install pyinstaller keyboard

echo Очистка предыдущих сборок...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Скриншотер.spec" del "Скриншотер.spec"

echo Компиляция приложения...
pyinstaller --onefile --noconsole --name "Скриншотер" --hidden-import=keyboard --hidden-import=threading --clean screenshot_app.py

echo.
echo ✅ Готово! 
echo 📁 Готовый файл: dist\Скриншотер.exe
echo.
echo 🎯 Функции:
echo - F2 - быстрый скриншот
echo - Ctrl+Q или Ctrl+W - выход
echo - Кнопка в приложении
echo.
pause
