@echo off
cd /d "%~dp0"

echo Building BarenPDF.py ...
pyinstaller --onefile --console --clean --strip --upx-dir="C:\Users\AKIRRA\Documents\upx" --icon=BarenPDF.ico BarenPDF.py

echo Building BarenExtractor.py ...
pyinstaller --onefile --console --clean --strip --upx-dir="C:\Users\AKIRRA\Documents\upx" --icon=BarenExtractor.ico BarenExtractor.py

echo Build process completed!
pause