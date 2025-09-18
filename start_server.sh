#!/bin/bash

# Start the Rembg MCP Server
# This script activates the virtual environment and starts the server

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source rembg/bin/activate

# Set environment variables for rembg
export REMBG_HOME="$HOME/.u2net"
export OMP_NUM_THREADS=4

# Start the MCP server
echo "Starting Rembg MCP Server..."
python -m rembg_mcp.server