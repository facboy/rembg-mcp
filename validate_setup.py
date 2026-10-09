#!/usr/bin/env python3
"""
Validation script for Rembg MCP Server setup
This script performs comprehensive checks to ensure everything is working correctly
"""

import os
import sys
import subprocess
from pathlib import Path

def check_mark(condition, message):
    """Print check mark or X based on condition"""
    symbol = "✅" if condition else "❌"
    print(f"{symbol} {message}")
    return condition

def main():
    print("🔍 Validating Rembg MCP Server Setup")
    print("=" * 40)

    all_checks_passed = True

    # Check Python version
    python_version = sys.version_info
    python_ok = python_version >= (3, 10)
    all_checks_passed &= check_mark(
        python_ok,
        f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}"
    )

    # Check virtual environment
    venv_exists = Path(".venv").exists()
    all_checks_passed &= check_mark(venv_exists, "uv virtual environment exists")

    # Check if we're in the virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    all_checks_passed &= check_mark(in_venv, "Running in virtual environment")

    # Check package imports
    try:
        import mcp
        mcp_ok = True
    except ImportError:
        mcp_ok = False
    all_checks_passed &= check_mark(mcp_ok, "MCP package available")

    try:
        import rembg
        rembg_ok = True
    except ImportError:
        rembg_ok = False
    all_checks_passed &= check_mark(rembg_ok, "Rembg package available")

    try:
        from rembg_mcp.server import RembgMCPServer
        server_ok = True
    except ImportError:
        server_ok = False
    all_checks_passed &= check_mark(server_ok, "Rembg MCP server module available")

    # Check scripts
    start_script_exists = Path("start_server.sh").exists()
    all_checks_passed &= check_mark(start_script_exists, "Start script exists")

    if start_script_exists:
        start_script_executable = os.access("start_server.sh", os.X_OK)
        all_checks_passed &= check_mark(start_script_executable, "Start script is executable")

    # Check configuration files
    config_exists = Path("claude_desktop_config.json").exists()
    all_checks_passed &= check_mark(config_exists, "Claude Desktop config exists")

    # Check model cache directory
    model_cache = Path.home() / ".u2net"
    cache_exists = model_cache.exists()
    all_checks_passed &= check_mark(cache_exists, "Model cache directory exists")

    # Test server instantiation
    if server_ok:
        try:
            server = RembgMCPServer()
            server_instantiation_ok = True
        except Exception as e:
            server_instantiation_ok = False
            print(f"   Error: {e}")
        all_checks_passed &= check_mark(server_instantiation_ok, "Server can be instantiated")

    print("\n" + "=" * 40)

    if all_checks_passed:
        print("🎉 All checks passed! Your Rembg MCP Server is ready to use.")
        print("\nNext steps:")
        print("1. Start the server: ./start_server.sh")
        print("2. Configure your MCP client (Claude Desktop, Claude Code, etc.)")
        print("3. Test with a simple image background removal")
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("\nTroubleshooting:")
        print("1. Run the setup script again: ./setup.sh")
        print("2. Sync the environment: uv sync")
        print("3. Reinstall dependencies if needed")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())