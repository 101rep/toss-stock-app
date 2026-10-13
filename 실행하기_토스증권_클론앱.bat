@echo off
chcp 65001 > nul
echo ========================================================
echo   토스 증권 스타일 실시간 시세 & TOP 100 탐색기 실행
echo   (한국투자증권 KIS Open API 연동 지원 / 광고 없음)
echo ========================================================
echo.

set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

start "" "%APP_DIR%index.html"

echo 브라우저에서 토스 증권 스타일 뷰어가 정상 실행되었습니다.
timeout /t 3 > nul
exit
