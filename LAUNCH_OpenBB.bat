@echo off
REM ============================================================
REM  OpenBB Platform - Interactive Python Shell
REM  Double-click this file to start OpenBB
REM ============================================================
echo.
echo Starting OpenBB Platform...
echo.
echo Try these commands once Python starts:
echo.
echo   from openbb import obb
echo   obb.equity.price.quote("MSFT").to_dataframe()
echo   obb.equity.fundamental.overview("MSFT").to_dataframe()
echo   obb.news.company("HUBS", limit=10).to_dataframe()
echo.
echo Type exit() to quit.
echo ============================================================
echo.

cd /d "%~dp0"
call "openbb-env\Scripts\activate.bat"
python -i -c "from openbb import obb; print('OpenBB loaded as obb. Try: obb.equity.price.quote(\"MSFT\")')"
