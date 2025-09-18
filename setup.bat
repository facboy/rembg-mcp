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

REM Check Python installation
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found

REM Remove existing virtual environment
if exist "rembg" (
    echo [WARNING] Removing existing virtual environment...
    rmdir /s /q rembg
)

REM Create virtual environment
echo [INFO] Creating virtual environment 'rembg'...
python -m venv rembg

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call rembg\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing MCP Python SDK...
pip install mcp

echo [INFO] Installing rembg with CPU support...
pip install "rembg[cpu,cli]"

echo [INFO] Installing additional dependencies...
pip install pillow

REM Install the MCP server
echo [INFO] Installing rembg-mcp in development mode...
pip install -e .

REM Test installation
echo [INFO] Testing installation...
python test_server.py
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
    pip install "rembg[gpu,cli]" --upgrade
    echo [SUCCESS] GPU support installed!
    echo [WARNING] Note: GPU support requires CUDA to be properly configured
)

REM Generate Windows start script
echo [INFO] Creating Windows start script...
echo @echo off > start_server.bat
echo REM Start the Rembg MCP Server on Windows >> start_server.bat
echo set "SCRIPT_DIR=%%~dp0" >> start_server.bat
echo cd /d "%%SCRIPT_DIR%%" >> start_server.bat
echo call rembg\Scripts\activate.bat >> start_server.bat
echo set REMBG_HOME=%%USERPROFILE%%\.u2net >> start_server.bat
echo set OMP_NUM_THREADS=4 >> start_server.bat
echo echo Starting Rembg MCP Server... >> start_server.bat
echo python -m rembg_mcp.server >> start_server.bat

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

echo.
echo 🎉 Rembg MCP Server setup completed successfully!
echo.
echo 📋 Setup Summary:
echo   ✓ Virtual environment created: %SCRIPT_DIR%rembg
echo   ✓ Dependencies installed
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