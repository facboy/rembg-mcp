#!/bin/bash

# Model Download Script for Rembg MCP Server
# This script runs the Python model downloader through the uv-managed environment

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_status "🤖 Rembg Model Download Utility"
echo "=" * 40

# Check if uv is available
if ! command -v uv >/dev/null 2>&1; then
    print_error "uv is not installed. See https://docs.astral.sh/uv/ for installation instructions."
    exit 1
fi

# Ensure the environment is synced
print_status "Syncing environment with uv..."
uv sync

# Verify rembg is available
if ! uv run python -c "import rembg" 2>/dev/null; then
    print_error "Rembg is not installed in the uv environment!"
    print_error "Please run setup.sh to install dependencies."
    exit 1
fi

print_success "uv environment ready and rembg is available"

# Set environment variables
export OMP_NUM_THREADS=4

# Run the Python download script with any arguments passed to this script
print_status "Starting model download script..."
uv run python download_models.py "$@"

# Check exit status
if [ $? -eq 0 ]; then
    print_success "Model download completed successfully!"
else
    print_error "Model download failed or was cancelled."
    exit 1
fi