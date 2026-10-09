@echo off
REM Rembg MCP Server Setup Script for Windows
REM This script sets up the complete environment for the Rembg MCP server

setlocal EnableDelayedExpansion

echo 🚀 Rembg MCP Server Setup for Windows
echo ====================================

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo [INFO] Working directory: %SCRIPT_DIR%

REM Check uv installation
echo [INFO] Checking uv installation...
where uv >nul 2>&1
if errorlevel 1 (
    echo [ERROR] uv is not installed or not in PATH
    echo See https://docs.astral.sh/uv/ for installation instructions
    pause
    exit /b 1
)

echo [SUCCESS] uv found

REM Create the virtual environment and install all dependencies from pyproject.toml / uv.lock
echo [INFO] Syncing environment with uv...
uv sync
if errorlevel 1 (
    echo [ERROR] uv sync failed!
    pause
    exit /b 1
)

REM Test installation
echo [INFO] Testing installation...
uv run python test_server.py
if errorlevel 1 (
    echo [ERROR] Installation test failed!
    pause
    exit /b 1
)

echo [SUCCESS] Installation test passed!

REM Create model cache directory
echo [INFO] Creating model cache directory...
if not exist "%USERPROFILE%\.u2net" mkdir "%USERPROFILE%\.u2net"

REM Ask for GPU support
echo.
set /p GPU_CHOICE="Do you want to install GPU support? (y/N): "
if /i "!GPU_CHOICE!"=="y" (
    echo [INFO] Installing GPU support...
    uv sync --extra gpu
    echo [SUCCESS] GPU support installed!
    echo [WARNING] Note: GPU support requires CUDA to be properly configured
)

REM Generate Windows start script
echo [INFO] Creating Windows start script...
echo @echo off > start_server.bat
echo REM Start the Rembg MCP Server on Windows >> start_server.bat
echo set "SCRIPT_DIR=%%~dp0" >> start_server.bat
echo cd /d "%%SCRIPT_DIR%%" >> start_server.bat
echo set REMBG_HOME=%%USERPROFILE%%\.u2net >> start_server.bat
echo set OMP_NUM_THREADS=4 >> start_server.bat
echo echo Starting Rembg MCP Server... >> start_server.bat
echo uv run --no-sync python -m rembg_mcp.server >> start_server.bat

REM Generate configuration for Windows
echo [INFO] Generating configuration files...
(
echo {
echo   "mcpServers": {
echo     "rembg": {
echo       "command": "%SCRIPT_DIR%start_server.bat",
echo       "cwd": "%SCRIPT_DIR%",
echo       "env": {
echo         "REMBG_HOME": "~/.u2net",
echo         "OMP_NUM_THREADS": "4"
echo       }
echo     }
echo   }
echo }
) > claude_desktop_config_windows.json

echo [SUCCESS] Created claude_desktop_config_windows.json

REM Model download section
echo.
echo [INFO] 🤖 AI Model Setup
echo Rembg requires AI models to remove backgrounds. Models are cached locally (%%USERPROFILE%%\.u2net^)
echo and only need to be downloaded once.
echo.

REM Check if any models already exist
if exist "%USERPROFILE%\.u2net\*.onnx" (
    echo [SUCCESS] Found existing models in cache
    dir "%USERPROFILE%\.u2net\*.onnx" /b 2>nul
    echo.
)

set /p MODEL_CHOICE="Would you like to download AI models now? (Y/n): "
if /i "!MODEL_CHOICE!"=="n" (
    echo [WARNING] Skipping model download.
    echo [WARNING] Models will be downloaded automatically when first used, but this may cause delays.
    echo You can download models later by running: .\download_models.py
) else (
    echo [INFO] Starting model download...
    uv run python download_models.py
    echo.
)

echo.
echo 🎉 Rembg MCP Server setup completed successfully!
echo.
echo 📋 Setup Summary:
echo   ✓ uv environment synced: %SCRIPT_DIR%.venv
echo   ✓ Dependencies installed from uv.lock
echo   ✓ MCP server installed in development mode
echo   ✓ Windows scripts created
echo   ✓ Configuration files updated
echo.
echo 🚀 Next Steps:
echo.
echo 1. Start the server:
echo    start_server.bat
echo.
echo 2. For Claude Desktop, copy configuration from:
echo    claude_desktop_config_windows.json
echo    to: %%APPDATA%%\Claude\claude_desktop_config.json
echo.
echo 3. See README.md for complete usage guide
echo.
echo [SUCCESS] Setup complete! The Rembg MCP server is ready to use.

pause