@echo off
REM ============================================================
REM  TradingView Desktop - Installer Launcher
REM  Double-click this file to install TradingView Desktop
REM ============================================================
echo.
echo Installing TradingView Desktop...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-AppPackage -Path '%~dp0TradingView_Installer\TradingView_3.1.0.7818_X64_msix_en-US.msix' -ForceApplicationShutdown"

if %errorlevel%==0 (
    echo.
    echo SUCCESS: TradingView Desktop is installed.
    echo Look for "TradingView" in your Start Menu.
    echo.
) else (
    echo.
    echo Install may have failed. Try running this script as Administrator.
    echo Or install manually from: https://www.tradingview.com/desktop/
    echo.
)

pause
