#!/bin/bash

# Start the Rembg MCP Server
# This script runs the server through the uv-managed environment

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Set environment variables for rembg
export REMBG_HOME="$HOME/.u2net"
export OMP_NUM_THREADS=4

# Start the MCP server
echo "Starting Rembg MCP Server..."
exec uv run --no-sync python -m rembg_mcp.server