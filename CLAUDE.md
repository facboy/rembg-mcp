# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) implementation for **rembg**, a popular Python library for removing image backgrounds using machine learning models. The main rembg codebase is located in a separate directory and this directory serves as the MCP wrapper implementation.

**Rembg** is a tool that removes image backgrounds using various pre-trained models including U2Net, BiRefNet, ISNet, and SAM. It supports both CLI usage and library integration with multiple input/output formats (PIL, OpenCV, bytes).

## Development Commands

### Python Environment
- **Python Version**: 3.10-3.13 (as specified in rembg's setup.py)
- **Package Manager**: pip with setuptools

### Testing
```bash
# Run tests (if rembg source is available)
python -m pytest
```

### Development Installation
```bash
# Install rembg in development mode
pip install -e ".[dev,cpu,cli]"  # or [gpu] for GPU support
```

### Code Quality
```bash
# Code quality tools
black .          # Code formatting
flake8 .         # Linting
isort .          # Import sorting
mypy .           # Type checking
bandit .         # Security analysis
```

## Architecture Overview

### Core Components (from github/rembg/)

1. **rembg/bg.py** - Main background removal logic with `remove()` function
2. **rembg/session_factory.py** - Factory for creating model sessions (`new_session()`)
3. **rembg/sessions/** - Model-specific implementations:
   - `base.py` - BaseSession abstract class
   - Individual model sessions (u2net, birefnet, isnet, sam, etc.)
4. **rembg/commands/** - CLI command implementations (i, p, s, b subcommands)
5. **rembg/cli.py** - Main CLI entry point using Click

### Session Pattern
The library uses a session pattern for model management:
- `new_session(model_name)` creates a session with ONNX runtime
- Sessions handle model downloading, normalization, and prediction
- Reusing sessions across multiple images improves performance

### Model Types
- **u2net**: General purpose (default)
- **birefnet**: High accuracy variants (general, portrait, massive)
- **isnet**: Anime and general use
- **sam**: Segment Anything Model with prompt support
- **silueta**: Lightweight version

### CLI Structure
- `rembg i` - Process individual files
- `rembg p` - Process folders (with watch mode)
- `rembg s` - HTTP server mode
- `rembg b` - RGB24 binary stream processing

## MCP Implementation Considerations

When implementing MCP tools for rembg:

1. **Model Management**: Handle model downloads (~100MB+ files) to `~/.u2net/`
2. **Session Reuse**: Create sessions once and reuse for multiple operations
3. **Input Formats**: Support PIL Images, file paths, bytes, and URLs
4. **Memory Management**: Large models require careful memory handling
5. **GPU Support**: Detect CUDA/ROCm availability for acceleration
6. **Output Formats**: PNG with transparency, configurable background colors

## Key Entry Points

- `rembg.remove(input, session=None, **kwargs)` - Main function
- `rembg.new_session(model_name="u2net")` - Session creation
- Alpha matting, mask-only output, and background replacement options available

## MCP Implementation

This directory contains the MCP server implementation with the following structure:

```
rembg-mcp/
├── rembg_mcp/
│   ├── __init__.py
│   └── server.py                # Main MCP server implementation
├── setup.sh                     # Linux/macOS setup script
├── setup.bat                    # Windows setup script
├── start_server.sh              # Server startup script
├── pyproject.toml               # Python package configuration
├── claude_desktop_config.json   # Example Claude Desktop configuration
├── test_server.py               # Installation test
├── validate_setup.py            # Setup validation
├── example_usage.py            # Example tool call demonstrations
└── README.md                   # Usage documentation
```

### Available MCP Tools

1. **rembg-i**: Process single image files
   - Supports all rembg models and options
   - Handles alpha matting and mask-only output

2. **rembg-p**: Batch process folders
   - Configurable file extensions
   - Reuses model sessions for efficiency
   - Detailed progress reporting

### Development Commands

```bash
# Setup environment (recommended)
./setup.sh

# Or manual installation
pip install -e .

# Install with GPU support
pip install -e ".[gpu]"

# Run the MCP server
./start_server.sh
# Or manually: python -m rembg_mcp.server

# Test installation
python test_server.py
python validate_setup.py
```

## Dependencies

Core: numpy, pillow, opencv-python-headless, onnxruntime, scipy, pymatting
CLI: click, fastapi, uvicorn, aiohttp (for server mode)
MCP: mcp (Python SDK)
Dev: pytest, black, flake8, mypy, isort