@echo off
@chcp 65001 >nul
setlocal enabledelayedexpansion

REM Пути
set PROJECT_DIR=D:\nginx-1.28.0\sheepcount
set VENV_DIR=%PROJECT_DIR%\venv
set NGINX_DIR=D:\nginx-1.28.0
set NGINX_EXE=%NGINX_DIR%\nginx.exe
set FLASK_APP=%PROJECT_DIR%\server\route.py

:MENU
cls
echo ============================
echo   Запуск SheepCounter
echo ============================
echo 1. Запустить nginx
echo 2. Остановить nginx
echo 3. Запустить Flask
echo 4. Остановить Flask
echo 5. Запустить php-cgi
echo 6. Остановить php-cgi
echo 7. Запустить всё
echo 8. Перезапустить всё (nginx + Flask + php-cgi)
echo 0. Выйти
echo ============================
set /p choice=Выберите действие:

if "%choice%"=="1" goto start_nginx
if "%choice%"=="2" goto stop_nginx
if "%choice%"=="3" goto start_flask
if "%choice%"=="4" goto stop_flask
if "%choice%"=="5" goto start_phpcgi
if "%choice%"=="6" goto stop_phpcgi
if "%choice%"=="7" goto start_all
if "%choice%"=="8" goto restart_all
if "%choice%"=="0" goto end

echo Неверный выбор
pause
goto MENU

:start_nginx
echo Запуск nginx...
cd /d %NGINX_DIR%
start "" "%NGINX_EXE%"
echo nginx запущен
pause
goto MENU

:stop_nginx
echo Остановка nginx...
taskkill /IM nginx.exe /F
echo nginx остановлен
pause
goto MENU

:start_flask
echo Запуск Flask...
cd /d %PROJECT_DIR%
call %VENV_DIR%\Scripts\activate.bat
start "Flask" cmd /k "python %FLASK_APP%"
goto MENU

:stop_flask
echo Остановка Flask...
for /f "tokens=5" %%a in ('tasklist /fi "imagename eq python.exe" /v ^| findstr "app.py"') do (
    echo Убиваем процесс PID %%a
    taskkill /PID %%a /F
)
pause
goto MENU

:start_phpcgi
echo Запуск php-cgi...
REM ВАЖНО: Укажи путь к php-cgi.exe ниже
set PHP_CGI_EXE=php-cgi.exe
start "php-cgi" cmd /k "%PHP_CGI_EXE% -b 127.0.0.1:9000"
echo php-cgi запущен
pause
goto MENU

:stop_phpcgi
echo Остановка php-cgi...
taskkill /IM php-cgi.exe /F
echo php-cgi остановлен
pause
goto MENU

:start_all
call :start_nginx
call :start_phpcgi
call :start_flask
goto MENU

:restart_all
call :stop_nginx
call :stop_phpcgi
call :stop_flask
call :start_all
goto MENU

:end
echo Выход...
exit /b
