@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM ===== 配置路径（按你当前路径写）=====
set "COMFY_ROOT=D:\PixelSmile\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable"
set "PROJECT_ROOT=D:\PixelSmile\SceneForge"
set "ENV_NAME=ai_backend"

REM ===== 1️⃣ 启动 ComfyUI =====
echo [1/3] Starting ComfyUI...
start "ComfyUI" /min "%COMFY_ROOT%\python_embeded\python.exe" ^
  -s "%COMFY_ROOT%\ComfyUI\main.py" ^
  --windows-standalone-build ^
  --lowvram

REM 等待 ComfyUI 启动
timeout /t 8 /nobreak > nul

REM ===== 2️⃣ 激活 conda 环境 =====
echo [2/3] Activating conda env...

where conda >nul 2>nul
if %ERRORLEVEL%==0 (
    call conda activate %ENV_NAME%
) else (
    if exist "%USERPROFILE%\anaconda3\condabin\conda.bat" set "CONDA_BAT=%USERPROFILE%\anaconda3\condabin\conda.bat"
    if exist "%USERPROFILE%\miniconda3\condabin\conda.bat" set "CONDA_BAT=%USERPROFILE%\miniconda3\condabin\conda.bat"
    if defined CONDA_BAT (call "%CONDA_BAT%" activate %ENV_NAME%)
)

REM ===== 3️⃣ 启动 FastAPI =====
echo [3/3] Starting FastAPI backend...
cd /d "%PROJECT_ROOT%"

start "Backend" cmd /k uvicorn main:app --reload --port 8000

REM ===== 可选：启动前端 =====
REM 如果你用 vite/react，可以取消下面注释

REM start "Frontend" cmd /k npm run dev

echo =====================================
echo   AI Ceramic System is Running
echo =====================================
echo ComfyUI:  http://127.0.0.1:8188
echo Backend:  http://127.0.0.1:8000/docs
echo =====================================

pause