#!/bin/bash

# Model Download Script for Rembg MCP Server
# This script activates the virtual environment and runs the Python model downloader

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

# Check if virtual environment exists
if [ ! -d "rembg" ]; then
    print_error "Virtual environment 'rembg' not found!"
    print_error "Please run setup.sh first to create the environment."
    exit 1
fi

# Check if virtual environment has rembg installed
print_status "Activating virtual environment..."
source rembg/bin/activate

# Verify rembg is available
if ! python -c "import rembg" 2>/dev/null; then
    print_error "Rembg is not installed in the virtual environment!"
    print_error "Please run setup.sh to install dependencies."
    exit 1
fi

print_success "Virtual environment activated and rembg is available"

# Set environment variables
export REMBG_HOME="$HOME/.u2net"
export OMP_NUM_THREADS=4

# Run the Python download script with any arguments passed to this script
print_status "Starting model download script..."
python download_models.py "$@"

# Check exit status
if [ $? -eq 0 ]; then
    print_success "Model download completed successfully!"
else
    print_error "Model download failed or was cancelled."
    exit 1
fi