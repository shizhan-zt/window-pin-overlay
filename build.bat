@echo off
chcp 65001 >nul
echo 正在打包钉子插件...
python -m PyInstaller --onefile --noconsole --name "钉子插件" --distpath . --clean "钉子插件.pyw"
echo 打包完成
del 钉子插件.spec 2>nul
rmdir /s /q build 2>nul
pause
