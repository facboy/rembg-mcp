#!/usr/bin/env python3
"""
Model Download Script for Rembg MCP Server
Downloads and caches AI models for background removal
"""

import sys
from pathlib import Path

def check_rembg_available():
    """Check if rembg is available in the current environment"""
    try:
        import rembg  # noqa: F401
        return True
    except ImportError:
        return False

def download_model(model_name):
    """Download a specific model using rembg"""
    try:
        from rembg import new_session
        print(f"📥 Downloading model: {model_name}")
        print("   This may take a few minutes depending on your internet connection...")

        # Create a session which automatically downloads the model
        _ = new_session(model_name)
        print(f"✅ Successfully downloaded and cached: {model_name}")
        return True

    except Exception as e:
        print(f"❌ Failed to download {model_name}: {e}")
        return False

def get_downloaded_models():
    """Get list of already downloaded models"""
    cache_dir = Path.home() / ".u2net"
    downloaded = set()

    if cache_dir.exists():
        # Map ONNX filenames to model names
        filename_map = {
            "u2net.onnx": "u2net",
            "u2netp.onnx": "u2netp",
            "u2net_human_seg.onnx": "u2net_human_seg",
            "u2net_cloth_seg.onnx": "u2net_cloth_seg",
            "silueta.onnx": "silueta",
            "isnet-general-use.onnx": "isnet-general-use",
            "isnet-anime.onnx": "isnet-anime",
            "birefnet-general.onnx": "birefnet-general",
            "birefnet-general-lite.onnx": "birefnet-general-lite",
            "birefnet-portrait.onnx": "birefnet-portrait",
            "birefnet-dis.onnx": "birefnet-dis",
            "birefnet-hrsod.onnx": "birefnet-hrsod",
            "birefnet-cod.onnx": "birefnet-cod",
            "birefnet-massive.onnx": "birefnet-massive"
        }

        for onnx_file in cache_dir.glob("*.onnx"):
            model_name = filename_map.get(onnx_file.name)
            if model_name:
                downloaded.add(model_name)

    return downloaded

def delete_model(model_name):
    """Delete a downloaded model"""
    cache_dir = Path.home() / ".u2net"

    # Map model names to ONNX filenames
    filename_map = {
        "u2net": "u2net.onnx",
        "u2netp": "u2netp.onnx",
        "u2net_human_seg": "u2net_human_seg.onnx",
        "u2net_cloth_seg": "u2net_cloth_seg.onnx",
        "silueta": "silueta.onnx",
        "isnet-general-use": "isnet-general-use.onnx",
        "isnet-anime": "isnet-anime.onnx",
        "birefnet-general": "birefnet-general.onnx",
        "birefnet-general-lite": "birefnet-general-lite.onnx",
        "birefnet-portrait": "birefnet-portrait.onnx",
        "birefnet-dis": "birefnet-dis.onnx",
        "birefnet-hrsod": "birefnet-hrsod.onnx",
        "birefnet-cod": "birefnet-cod.onnx",
        "birefnet-massive": "birefnet-massive.onnx"
    }

    filename = filename_map.get(model_name)
    if not filename:
        print(f"❌ Unknown model: {model_name}")
        return False

    model_path = cache_dir / filename
    if not model_path.exists():
        print(f"❌ Model not found: {model_name}")
        return False

    try:
        model_path.unlink()
        print(f"🗑️  Successfully deleted: {model_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete {model_name}: {e}")
        return False

def get_model_info():
    """Get information about available models with download URLs from rembg repository"""
    models = {
        "u2net": {
            "name": "U2Net General",
            "size": "~170MB",
            "speed": "Medium",
            "quality": "Good",
            "description": "General purpose model (recommended for beginners)",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
        },
        "u2netp": {
            "name": "U2Net Plus",
            "size": "~4MB",
            "speed": "Fast",
            "quality": "Good",
            "description": "Lightweight version, good for batch processing",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2netp.onnx"
        },
        "u2net_human_seg": {
            "name": "U2Net Human Segmentation",
            "size": "~170MB",
            "speed": "Medium",
            "quality": "Good",
            "description": "Pre-trained model for human segmentation",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_human_seg.onnx"
        },
        "u2net_cloth_seg": {
            "name": "U2Net Cloth Segmentation",
            "size": "~170MB",
            "speed": "Medium",
            "quality": "Good",
            "description": "Cloths parsing: Upper body, Lower body, Full body",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_cloth_seg.onnx"
        },
        "silueta": {
            "name": "Silueta",
            "size": "~43MB",
            "speed": "Fast",
            "quality": "Good",
            "description": "Compact model with good performance",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/silueta.onnx"
        },
        "isnet-general-use": {
            "name": "ISNet General",
            "size": "~180MB",
            "speed": "Medium",
            "quality": "Excellent",
            "description": "High quality general purpose model",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx"
        },
        "isnet-anime": {
            "name": "ISNet Anime",
            "size": "~180MB",
            "speed": "Medium",
            "quality": "Excellent",
            "description": "High-accuracy segmentation for anime characters",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-anime.onnx"
        },
        "birefnet-general": {
            "name": "BiRefNet General",
            "size": "~300MB",
            "speed": "Slow",
            "quality": "Excellent",
            "description": "High accuracy general purpose model",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-general-epoch_244.onnx"
        },
        "birefnet-general-lite": {
            "name": "BiRefNet General Lite",
            "size": "~150MB",
            "speed": "Medium",
            "quality": "Excellent",
            "description": "Light version of BiRefNet general model",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-general-bb_swin_v1_tiny-epoch_232.onnx"
        },
        "birefnet-portrait": {
            "name": "BiRefNet Portrait",
            "size": "~300MB",
            "speed": "Slow",
            "quality": "Excellent",
            "description": "Specialized for human portraits and selfies",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-portrait-epoch_150.onnx"
        },
        "birefnet-dis": {
            "name": "BiRefNet DIS",
            "size": "~300MB",
            "speed": "Slow",
            "quality": "Excellent",
            "description": "Dichotomous image segmentation model",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-DIS-epoch_590.onnx"
        },
        "birefnet-hrsod": {
            "name": "BiRefNet HRSOD",
            "size": "~300MB",
            "speed": "Slow",
            "quality": "Excellent",
            "description": "High-resolution salient object detection",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-HRSOD_DHU-epoch_115.onnx"
        },
        "birefnet-cod": {
            "name": "BiRefNet COD",
            "size": "~300MB",
            "speed": "Slow",
            "quality": "Excellent",
            "description": "Concealed object detection model",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-COD-epoch_125.onnx"
        },
        "birefnet-massive": {
            "name": "BiRefNet Massive",
            "size": "~300MB",
            "speed": "Slow",
            "quality": "Best",
            "description": "Trained with massive dataset for best results",
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-massive-TR_DIS5K_TR_TEs-epoch_420.onnx"
        }
    }
    return models

def interactive_model_selection():
    """Interactive model selection interface"""
    models = get_model_info()
    downloaded_models = get_downloaded_models()

    print("\n🤖 Available AI Models for Background Removal:")
    print("=" * 70)

    # Display model options
    model_list = list(models.keys())
    for i, (model_name, info) in enumerate(zip(model_list, models.values()), 1):
        status = "✅ Downloaded" if model_name in downloaded_models else "⬜ Not Downloaded"
        print(f"{i:2d}. {info['name']} [{status}]")
        print(f"    Size: {info['size']:>8} | Speed: {info['speed']:>6} | Quality: {info['quality']}")
        print(f"    {info['description']}")
        print()

    print("Recommended for new users:")
    print("  • Option 1 (u2net) - Good balance of speed and quality")
    print("  • Option 9 (birefnet-general) - Best quality for general use")
    print("  • Option 10 (birefnet-portrait) - Best for portrait photos")

    while True:
        try:
            print(f"\nOperations:")
            print(f"  📥 Download: Enter numbers (1-{len(model_list)}) separated by spaces")
            print(f"  🗑️  Delete: Type 'delete' followed by numbers (e.g., 'delete 1 5')")
            print(f"  📋 List: Type 'list' to show downloaded models")
            print(f"  ⚡ Quick: Press Enter for u2net (recommended), 'all' for all models")
            print(f"  🚪 Exit: Type 'skip' to exit")

            choice = input("\nYour choice: ").strip()

            if choice == "":
                return {"action": "download", "models": ["u2net"]}
            elif choice.lower() == "skip":
                return {"action": "skip", "models": []}
            elif choice.lower() == "all":
                return {"action": "download", "models": model_list}
            elif choice.lower() == "list":
                if downloaded_models:
                    print(f"\n📋 Downloaded models ({len(downloaded_models)}):")
                    for model in sorted(downloaded_models):
                        model_info = models.get(model, {})
                        print(f"  ✅ {model_info.get('name', model)} ({model_info.get('size', 'Unknown size')})")
                else:
                    print("\n📋 No models downloaded yet")
                continue
            elif choice.lower().startswith("delete "):
                # Parse delete command
                try:
                    delete_numbers = [int(x.strip()) for x in choice[7:].split()]
                    delete_models = []

                    for num in delete_numbers:
                        if 1 <= num <= len(model_list):
                            model_name = model_list[num - 1]
                            if model_name in downloaded_models:
                                delete_models.append(model_name)
                            else:
                                print(f"⚠️  Model {num} ({model_name}) is not downloaded")
                        else:
                            print(f"❌ Invalid choice: {num}. Please select 1-{len(model_list)}")

                    if delete_models:
                        return {"action": "delete", "models": delete_models}
                    else:
                        print("No valid models to delete")
                        continue

                except ValueError:
                    print("Invalid delete syntax. Use: delete 1 2 3")
                    continue
            else:
                # Parse space-separated numbers for download
                selected_numbers = [int(x.strip()) for x in choice.split()]
                selected_models = []

                for num in selected_numbers:
                    if 1 <= num <= len(model_list):
                        selected_models.append(model_list[num - 1])
                    else:
                        print(f"Invalid choice: {num}. Please select 1-{len(model_list)}")
                        break
                else:
                    return {"action": "download", "models": selected_models}

        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers separated by spaces.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return {"action": "skip", "models": []}

def main():
    """Main function for model download script"""
    print("🎯 Rembg Model Download Utility")
    print("=" * 40)

    # Check if rembg is available
    if not check_rembg_available():
        print("❌ Error: rembg is not installed or not available in current environment")
        print("Please run this script from the activated virtual environment:")
        print("  source rembg/bin/activate")
        print("  python download_models.py")
        sys.exit(1)

    # Check model cache directory
    cache_dir = Path.home() / ".u2net"
    print(f"📁 Model cache directory: {cache_dir}")

    if cache_dir.exists():
        existing_files = list(cache_dir.glob("*.onnx"))
        if existing_files:
            print(f"📋 Found {len(existing_files)} existing model(s):")
            for file in existing_files:
                print(f"   • {file.name}")
        else:
            print("📋 No models cached yet")
    else:
        print("📋 Model cache directory will be created")

    # Interactive model selection
    if len(sys.argv) > 1:
        # Command line arguments provided
        if sys.argv[1].lower() == "delete":
            # Delete mode from command line
            if len(sys.argv) < 3:
                print("❌ Delete mode requires model names. Usage: python download_models.py delete model1 model2")
                return
            result = {"action": "delete", "models": sys.argv[2:]}
        else:
            # Download mode from command line
            result = {"action": "download", "models": sys.argv[1:]}
        print(f"\n📋 Command line operation: {result['action']} {', '.join(result['models'])}")
    else:
        # Interactive selection
        result = interactive_model_selection()

    action = result["action"]
    selected_models = result["models"]

    if action == "skip" or not selected_models:
        print("\n⏭️  No operation performed.")
        print("You can manage models later by running: python download_models.py")
        return

    if action == "delete":
        # Delete selected models
        print(f"\n🗑️  Starting deletion of {len(selected_models)} model(s)...")
        success_count = 0
        failed_models = []

        for model in selected_models:
            print(f"\n{'='*50}")
            if delete_model(model):
                success_count += 1
            else:
                failed_models.append(model)

        # Summary
        print(f"\n{'='*50}")
        print("📊 Deletion Summary:")
        print(f"   🗑️  Successfully deleted: {success_count}/{len(selected_models)} models")

        if failed_models:
            print(f"   ❌ Failed deletions: {', '.join(failed_models)}")

        if success_count > 0:
            remaining = get_downloaded_models()
            if remaining:
                print(f"\n📋 Remaining downloaded models: {len(remaining)}")
                for model in sorted(remaining):
                    print(f"   ✅ {model}")
            else:
                print(f"\n🧹 Model cache cleared! Directory: {cache_dir}")

    elif action == "download":
        # Download selected models
        print(f"\n🚀 Starting download of {len(selected_models)} model(s)...")
        success_count = 0
        failed_models = []

        for model in selected_models:
            print(f"\n{'='*50}")
            if download_model(model):
                success_count += 1
            else:
                failed_models.append(model)

        # Summary
        print(f"\n{'='*50}")
        print("📊 Download Summary:")
        print(f"   ✅ Successfully downloaded: {success_count}/{len(selected_models)} models")

        if failed_models:
            print(f"   ❌ Failed downloads: {', '.join(failed_models)}")
            print("\nYou can retry failed downloads by running:")
            print(f"   python download_models.py {' '.join(failed_models)}")

        if success_count > 0:
            print(f"\n🎉 Ready to use! Your models are cached in: {cache_dir}")
            print("You can now start the MCP server: ./start_server.sh")

    print("\n💡 Model Usage Tips:")
    print("   • u2net: Good for general use")
    print("   • birefnet-portrait: Best for selfies and portraits")
    print("   • isnet-anime: Perfect for anime/cartoon images")
    print("   • silueta/u2netp: Fast processing for batch jobs")
    print("\n📖 Usage Examples:")
    print("   python download_models.py              # Interactive mode")
    print("   python download_models.py u2net        # Download specific model")
    print("   python download_models.py delete u2net # Delete specific model")

if __name__ == "__main__":
    main()