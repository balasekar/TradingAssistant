@echo off
REM ============================================================
REM   MORNING TRADING ROUTINE  (~25 min total)
REM   Chains: Tool 1 (regime briefing) -> Tool 2 (charts) -> Tool 3 (research)
REM ============================================================

setlocal
set ROOT=%~dp0
set PYEXE=%ROOT%openbb-env\Scripts\python.exe
set SKILLS=%ROOT%claude-trading-skills
set TODAY=%date:~10,4%-%date:~4,2%-%date:~7,2%
set REPORTS=%SKILLS%\reports\daily-%TODAY%
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo.
echo ============================================================
echo  MORNING TRADING ROUTINE  -  %TODAY%
echo ============================================================
echo.

REM -- Pre-flight check --
if not exist "%PYEXE%" (
    echo [ERROR] Python venv not found at %PYEXE%
    echo Re-run the OpenBB install steps from README.md
    pause & exit /b 1
)
if not exist "%SKILLS%\skills\market-breadth-analyzer" (
    echo [ERROR] claude-trading-skills repo not found
    echo Run: git clone https://github.com/tradermonty/claude-trading-skills "%SKILLS%"
    pause & exit /b 1
)
if not exist "%REPORTS%" mkdir "%REPORTS%"

REM ============================================================
REM  STEP 1/4  Market Breadth (Tool 1)
REM ============================================================
echo [1/4] Running Market Breadth Analyzer...
"%PYEXE%" "%SKILLS%\skills\market-breadth-analyzer\scripts\market_breadth_analyzer.py" ^
    --detail-url  "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" ^
    --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv" ^
    --output-dir  "%REPORTS%"
if errorlevel 1 ( echo [WARN] Breadth step had errors - continuing anyway )

REM ============================================================
REM  STEP 2/4  Uptrend Analysis (Tool 1)
REM ============================================================
echo.
echo [2/4] Running Uptrend Analyzer...
"%PYEXE%" "%SKILLS%\skills\uptrend-analyzer\scripts\uptrend_analyzer.py" --output-dir "%REPORTS%"
if errorlevel 1 ( echo [WARN] Uptrend step had errors - continuing anyway )

REM ============================================================
REM  STEP 3/4  Exposure Coach synthesis (Tool 1)
REM ============================================================
echo.
echo [3/4] Synthesizing into exposure recommendation...
for /f "delims=" %%i in ('dir /b /od "%REPORTS%\market_breadth_*.json" 2^>nul') do set BREADTH=%REPORTS%\%%i
for /f "delims=" %%i in ('dir /b /od "%REPORTS%\uptrend_analysis_*.json" 2^>nul') do set UPTREND=%REPORTS%\%%i
if "%BREADTH%"=="" goto :step4
if "%UPTREND%"=="" goto :step4
"%PYEXE%" "%SKILLS%\skills\exposure-coach\scripts\calculate_exposure.py" ^
    --breadth "%BREADTH%" --uptrend "%UPTREND%" --output-dir "%REPORTS%"

REM ============================================================
REM  STEP 4/4  Portfolio fundamentals check (Tool 3)
REM ============================================================
:step4
echo.
echo [4/4] Pulling fundamentals for your portfolio (MSFT + HUBS)...
"%PYEXE%" "%ROOT%my_scripts\portfolio_health_check.py"

REM ============================================================
REM  Open the briefing + TradingView (Tool 2)
REM ============================================================
echo.
echo ============================================================
echo  ROUTINE COMPLETE  -  opening briefing + TradingView...
echo ============================================================
if exist "%REPORTS%\BRIEFING.md" (
    start "" "%REPORTS%\BRIEFING.md"
) else (
    REM Open the latest exposure markdown if no human briefing exists
    for /f "delims=" %%i in ('dir /b /od "%REPORTS%\exposure_posture_*.md" 2^>nul') do start "" "%REPORTS%\%%i"
)
start "" "https://www.tradingview.com/chart/?symbol=NASDAQ%%3AMSFT"
echo.
echo  Reports saved to: %REPORTS%
echo.
pause
endlocal
