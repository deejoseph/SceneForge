@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

REM ===== 配置路径 =====
set "COMFY_ROOT=D:\PixelSmile\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable"
set "PROJECT_ROOT=D:\PixelSmile\SceneForge"
set "ENV_NAME=ai_backend"

REM ===== 显存优化参数 =====
set CUDA_MODULE_LOADING=LAZY
set PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

REM ===== 1️⃣ 启动 ComfyUI =====
echo [1/4] 正在启动 ComfyUI (后端绘图引擎)...
# 建议保持 --lowvram。如果运行 1344 分辨率依然报 Out of Memory，可以考虑换成 --normalvram 配合下面的分配优化
start "ComfyUI" /min "%COMFY_ROOT%\python_embeded\python.exe" ^
  -s "%COMFY_ROOT%\ComfyUI\main.py" ^
  --windows-standalone-build ^
  --lowvram ^
  --preview-method auto ^
  --fp16-vae

# 将等待时间从 8 秒延长到 15 秒，给 6.5G 模型充足的“起床时间”
timeout /t 15 /nobreak > nul

REM ===== 2️⃣ 激活 conda 环境 =====
echo [2/4] 正在激活 AI 后端环境: %ENV_NAME%...
where conda >nul 2>nul
if %ERRORLEVEL%==0 (
    call conda activate %ENV_NAME%
) else (
    if exist "%USERPROFILE%\anaconda3\condabin\conda.bat" set "CONDA_BAT=%USERPROFILE%\anaconda3\condabin\conda.bat"
    if exist "%USERPROFILE%\miniconda3\condabin\conda.bat" set "CONDA_BAT=%USERPROFILE%\miniconda3\condabin\conda.bat"
    if defined CONDA_BAT (call "%CONDA_BAT%" activate %ENV_NAME%)
)

REM ===== 3️⃣ 启动 FastAPI 后端 =====
echo [3/4] 正在启动定制系统业务逻辑 (Port 8000)...
cd /d "%PROJECT_ROOT%"
start "Backend" cmd /k uvicorn main:app --reload --port 8000

REM 等待后端启动完成
timeout /t 3 /nobreak > nul

REM ===== 4️⃣ 启动前端静态服务器并打开浏览器 =====
echo [4/4] 正在启动前端界面并自动打开浏览器 (Port 8080)...
REM 使用 start /min 隐藏静态服务器窗口
start "Frontend_Server" /min python -m http.server 8080

# 自动调用系统默认浏览器打开页面
start http://127.0.0.1:8080/index.html

echo ===============================================
echo      青瓷定制氛围确认系统 - 启动完成
echo ===============================================
echo  前端访问: http://127.0.0.1:8080/index.html
echo  后端接口: http://127.0.0.1:8000/docs
echo ===============================================
echo  提示：请保持所有窗口开启。关闭此窗口不会停止后台服务。
pause