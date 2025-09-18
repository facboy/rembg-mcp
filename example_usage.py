#!/usr/bin/env python3
"""Example usage of the Rembg MCP Server tools."""

import asyncio
import json
from pathlib import Path

# Example tool calls that would be made by an MCP client

def example_single_image():
    """Example of processing a single image."""
    tool_call = {
        "name": "rembg-i",
        "arguments": {
            "input_path": "/path/to/input/image.jpg",
            "output_path": "/path/to/output/image.png",
            "model": "u2net",
            "alpha_matting": False,
            "only_mask": False
        }
    }
    print("Single image processing tool call:")
    print(json.dumps(tool_call, indent=2))
    print()

def example_batch_processing():
    """Example of batch processing a folder."""
    tool_call = {
        "name": "rembg-p",
        "arguments": {
            "input_folder": "/path/to/input/folder",
            "output_folder": "/path/to/output/folder",
            "model": "birefnet-general",
            "alpha_matting": True,
            "only_mask": False,
            "file_extensions": [".jpg", ".jpeg", ".png"]
        }
    }
    print("Batch processing tool call:")
    print(json.dumps(tool_call, indent=2))
    print()

def example_mask_only():
    """Example of generating masks only."""
    tool_call = {
        "name": "rembg-i",
        "arguments": {
            "input_path": "/path/to/input/portrait.jpg",
            "output_path": "/path/to/output/mask.png",
            "model": "birefnet-portrait",
            "only_mask": True
        }
    }
    print("Mask-only processing tool call:")
    print(json.dumps(tool_call, indent=2))

if __name__ == "__main__":
    print("Rembg MCP Server - Example Tool Calls")
    print("=" * 50)
    example_single_image()
    example_batch_processing()
    example_mask_only()