# Rembg MCP Server

An MCP (Model Context Protocol) server for the rembg background removal library. Remove image backgrounds using AI models through Claude Code, Claude Desktop, Cursor, and other MCP-compatible tools.

## 🎯 Features

- **🖼️ Image Processing**: Remove backgrounds from single images or batch process folders
- **🤖 Multiple AI Models**: u2net, birefnet, isnet, sam, and more specialized models
- **⚡ Performance Optimized**: Model session reuse for efficient batch processing
- **🎨 Advanced Options**: Alpha matting, mask-only output, custom backgrounds
- **🌍 Cross-Platform**: Support for Windows, macOS, and Linux
- **🔧 Easy Integration**: Works with Claude Desktop, Claude Code CLI, Cursor IDE

## 📦 Quick Start

### 🚀 One-Click Installation

**Linux/macOS**
```bash
git clone <repository-url>
cd rembg-mcp
./setup.sh
```

**Windows**
```cmd
git clone <repository-url>
cd rembg-mcp
setup.bat
```

The setup scripts will automatically:
- Check Python 3.10+ requirement
- Create virtual environment
- Install all dependencies
- Configure MCP server
- Test the installation

### 🔧 Manual Installation

If you prefer manual installation or need custom configuration:

1. **Create virtual environment:**
```bash
python3 -m venv rembg
source rembg/bin/activate  # Linux/macOS
# or
rembg\Scripts\activate.bat  # Windows
```

2. **Install dependencies:**
```bash
pip install --upgrade pip
pip install mcp "rembg[cpu,cli]" pillow
pip install -e .
```

3. **Test installation:**
```bash
python test_server.py
python validate_setup.py
```

4. **For GPU support:**
```bash
pip install -e ".[gpu]"
```

## 🔧 MCP Configuration

### Claude Desktop Setup

1. **Find your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the rembg server configuration:**
```json
{
  "mcpServers": {
    "rembg": {
      "command": "/path/to/rembg-mcp/start_server.sh",
      "cwd": "/path/to/rembg-mcp",
      "env": {
        "REMBG_HOME": "~/.u2net",
        "OMP_NUM_THREADS": "4"
      }
    }
  }
}
```

3. **Replace `/path/to/rembg-mcp`** with your actual project path

4. **Restart Claude Desktop**

### Testing Your Setup

After configuration, test your MCP server:

1. **Start the server manually:**
```bash
./start_server.sh  # Linux/macOS
# or
start_server.bat   # Windows
```

2. **Verify MCP connection in Claude Desktop:**
   - Look for the rembg tools in your Claude conversation
   - Try a simple command: "List available MCP tools"

3. **Test with a sample image:**
   - Ask Claude: "Use rembg-i to remove the background from test.jpg"
   - The server will process your request and return results

### Claude Code CLI Setup

Add to your Claude Code settings:

```json
{
  "mcpServers": {
    "rembg": {
      "command": "/path/to/rembg-mcp/start_server.sh",
      "cwd": "/path/to/rembg-mcp",
      "env": {
        "REMBG_HOME": "~/.u2net",
        "OMP_NUM_THREADS": "4"
      }
    }
  }
}
```

### Cursor IDE Setup

Add to your Cursor settings or workspace `.cursor/settings.json`:

```json
{
  "mcp.servers": {
    "rembg": {
      "command": "/path/to/rembg-mcp/start_server.sh",
      "args": [],
      "cwd": "/path/to/rembg-mcp"
    }
  }
}
```

### Windows Configuration

For Windows users, use `start_server.bat` instead:

```json
{
  "mcpServers": {
    "rembg": {
      "command": "C:\\path\\to\\rembg-mcp\\start_server.bat",
      "cwd": "C:\\path\\to\\rembg-mcp"
    }
  }
}
```

## 🚀 How to Use

Once configured, you can use the rembg tools directly in your MCP-compatible application:

### Basic Usage Examples

**Single Image Processing:**
```
Remove the background from my photo.jpg and save it as photo_nobg.png
```

**Batch Processing:**
```
Process all images in my Photos folder and remove their backgrounds
```

**Advanced Processing:**
```
Use the birefnet-portrait model to remove backgrounds from all portrait photos in my folder, apply alpha matting for better edges, and save them to a new folder
```

## 🛠️ Available MCP Tools

### rembg-i - Single Image Background Removal

Removes background from a single image file with high precision.

**Required Parameters:**
- `input_path`: Path to the source image file
- `output_path`: Where to save the processed image

**Optional Parameters:**
- `model`: AI model to use (default: "u2net")
- `alpha_matting`: Improve edge quality (default: false)
- `only_mask`: Output black/white mask only (default: false)

**Supported formats:** JPG, PNG, BMP, TIFF, WebP

### rembg-p - Batch Folder Processing

Processes all images in a folder automatically.

**Required Parameters:**
- `input_folder`: Source folder containing images
- `output_folder`: Destination folder for processed images

**Optional Parameters:**
- `model`: AI model to use (default: "u2net")
- `alpha_matting`: Improve edge quality (default: false)
- `only_mask`: Output masks only (default: false)
- `file_extensions`: File types to process (default: common image formats)

**Features:**
- Automatically finds all supported images
- Preserves original filenames with `.out.png` suffix
- Detailed progress reporting
- Error handling for individual files

## 🤖 Supported AI Models

| Model | Use Case | Size | Quality |
|-------|----------|------|---------|
| `u2net` | General purpose (default) | Medium | Good |
| `u2netp` | Lightweight version | Small | Good |
| `u2net_human_seg` | Human subjects | Medium | Good |
| `u2net_cloth_seg` | Clothing segmentation | Medium | Good |
| `silueta` | Lightweight general | Small | Good |
| `isnet-general-use` | High quality general | Large | Excellent |
| `isnet-anime` | Anime characters | Large | Excellent |
| `birefnet-general` | High accuracy general | Large | Excellent |
| `birefnet-portrait` | Portrait photos | Large | Excellent |
| `birefnet-massive` | Massive dataset trained | X-Large | Best |
| `sam` | Segment Anything (prompt-based) | Large | Variable |

## 🔧 Configuration

### Environment Variables

- `REMBG_HOME`: Model storage directory (default: `~/.u2net`)
- `OMP_NUM_THREADS`: Number of CPU threads for processing (default: 4)
- `MODEL_CHECKSUM_DISABLED`: Skip model checksum verification

### Advanced Options

- **Alpha Matting**: Improves edge quality but increases processing time
- **Mask Only**: Returns black/white mask instead of transparent cutout
- **Custom Background Colors**: Replace transparent areas with solid colors
- **Batch Processing**: Automatically reuses model sessions for efficiency

## 📁 Project Structure

```
rembg-mcp/
├── rembg_mcp/
│   ├── __init__.py
│   └── server.py                      # Main MCP server implementation
├── rembg/                             # Virtual environment (git-ignored)
├── setup.sh                           # Linux/macOS setup script
├── setup.bat                          # Windows setup script
├── start_server.sh                    # Linux/macOS server startup
├── start_server.bat                   # Windows server startup (generated)
├── pyproject.toml                     # Python package configuration
├── claude_desktop_config.json         # Claude Desktop config (Linux/macOS)
├── claude_desktop_config_windows.json # Claude Desktop config (Windows)
├── test_server.py                     # Installation test
├── validate_setup.py                  # Comprehensive setup validation
├── example_usage.py                   # Usage examples
├── README.md                          # This file
├── USAGE_CN.md                       # Chinese documentation
└── CLAUDE.md                         # Claude Code context file
```

## 🚨 Troubleshooting

### Common Issues

**MCP Server Not Found**
- Verify the `command` path in your MCP configuration
- Ensure the script is executable: `chmod +x start_server.sh`
- Check that the virtual environment exists: `ls rembg/`

**Python Version Issues**
```bash
python --version  # Must be 3.10+
# If wrong version, install Python 3.10+ and recreate venv
```

**Model Download Problems**
```bash
# Clear model cache and re-download
rm -rf ~/.u2net
# Models will automatically re-download on next use
```

**Memory or Performance Issues**
```bash
# Reduce CPU threads
export OMP_NUM_THREADS=2

# Use lighter models (u2netp, silueta) instead of large ones
```

**Installation Problems**
```bash
# Clean reinstall
rm -rf rembg/
./setup.sh  # Or setup.bat on Windows
```

### Getting Help

- Run `python validate_setup.py` for detailed diagnostics
- Check server logs when starting manually
- Ensure your MCP client supports the latest protocol version

## 📚 Additional Resources

- [Rembg Library Documentation](https://github.com/danielgatis/rembg)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://claude.ai/code)
- [Chinese Usage Guide](./USAGE_CN.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [danielgatis/rembg](https://github.com/danielgatis/rembg) - The excellent background removal library
- [Anthropic](https://anthropic.com) - For the MCP protocol and Claude
- The open source community for the various AI models