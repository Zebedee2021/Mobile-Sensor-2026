@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动 Sensor Logger 托盘程序...
echo.
python scripts\tray.py
if errorlevel 1 (
    echo.
    echo 启动失败，请检查是否安装了 pystray 和 pillow
    echo 运行: pip install pystray pillow
    pause
)
