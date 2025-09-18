#!/usr/bin/env python3
"""Rembg MCP Server implementation."""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from PIL import Image
from rembg import new_session, remove


class RembgMCPServer:
    """MCP Server for rembg background removal operations."""

    def __init__(self) -> None:
        self.server = Server("rembg-mcp")
        self._sessions: Dict[str, Any] = {}
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools."""
            return [
                types.Tool(
                    name="rembg-i",
                    description="Remove background from a single image file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "input_path": {
                                "type": "string",
                                "description": "Path to the input image file"
                            },
                            "output_path": {
                                "type": "string",
                                "description": "Path for the output image file"
                            },
                            "model": {
                                "type": "string",
                                "description": "Model to use for background removal",
                                "default": "u2net",
                                "enum": [
                                    "u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg",
                                    "silueta", "isnet-general-use", "isnet-anime",
                                    "birefnet-general", "birefnet-general-lite",
                                    "birefnet-portrait", "birefnet-dis", "birefnet-hrsod",
                                    "birefnet-cod", "birefnet-massive", "sam"
                                ]
                            },
                            "alpha_matting": {
                                "type": "boolean",
                                "description": "Apply alpha matting for better edge quality",
                                "default": False
                            },
                            "only_mask": {
                                "type": "boolean",
                                "description": "Return only the mask instead of the cutout",
                                "default": False
                            }
                        },
                        "required": ["input_path", "output_path"]
                    }
                ),
                types.Tool(
                    name="rembg-p",
                    description="Remove backgrounds from all images in a folder",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "input_folder": {
                                "type": "string",
                                "description": "Path to the input folder containing images"
                            },
                            "output_folder": {
                                "type": "string",
                                "description": "Path to the output folder for processed images"
                            },
                            "model": {
                                "type": "string",
                                "description": "Model to use for background removal",
                                "default": "u2net",
                                "enum": [
                                    "u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg",
                                    "silueta", "isnet-general-use", "isnet-anime",
                                    "birefnet-general", "birefnet-general-lite",
                                    "birefnet-portrait", "birefnet-dis", "birefnet-hrsod",
                                    "birefnet-cod", "birefnet-massive", "sam"
                                ]
                            },
                            "alpha_matting": {
                                "type": "boolean",
                                "description": "Apply alpha matting for better edge quality",
                                "default": False
                            },
                            "only_mask": {
                                "type": "boolean",
                                "description": "Return only masks instead of cutouts",
                                "default": False
                            },
                            "file_extensions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "File extensions to process",
                                "default": [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
                            }
                        },
                        "required": ["input_folder", "output_folder"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool calls."""
            if name == "rembg-i":
                return await self._handle_rembg_i(arguments)
            elif name == "rembg-p":
                return await self._handle_rembg_p(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _handle_rembg_i(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle single image background removal."""
        try:
            input_path = Path(arguments["input_path"])
            output_path = Path(arguments["output_path"])
            model_name = arguments.get("model", "u2net")
            alpha_matting = arguments.get("alpha_matting", False)
            only_mask = arguments.get("only_mask", False)

            # Validate input file exists
            if not input_path.exists():
                return [types.TextContent(
                    type="text",
                    text=f"Error: Input file does not exist: {input_path}"
                )]

            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Get or create session for the model
            session = self._get_session(model_name)

            # Process the image
            with open(input_path, "rb") as input_file:
                input_data = input_file.read()

            output_data = remove(
                input_data,
                session=session,
                alpha_matting=alpha_matting,
                only_mask=only_mask
            )

            # Save the output
            with open(output_path, "wb") as output_file:
                output_file.write(output_data)

            return [types.TextContent(
                type="text",
                text=f"Successfully processed {input_path} -> {output_path} using model {model_name}"
            )]

        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error processing image: {str(e)}"
            )]

    async def _handle_rembg_p(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle batch folder processing."""
        try:
            input_folder = Path(arguments["input_folder"])
            output_folder = Path(arguments["output_folder"])
            model_name = arguments.get("model", "u2net")
            alpha_matting = arguments.get("alpha_matting", False)
            only_mask = arguments.get("only_mask", False)
            file_extensions = arguments.get("file_extensions", [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"])

            # Validate input folder exists
            if not input_folder.exists() or not input_folder.is_dir():
                return [types.TextContent(
                    type="text",
                    text=f"Error: Input folder does not exist or is not a directory: {input_folder}"
                )]

            # Create output directory
            output_folder.mkdir(parents=True, exist_ok=True)

            # Get or create session for the model
            session = self._get_session(model_name)

            # Find all image files
            image_files = []
            for ext in file_extensions:
                image_files.extend(input_folder.glob(f"*{ext}"))
                image_files.extend(input_folder.glob(f"*{ext.upper()}"))

            if not image_files:
                return [types.TextContent(
                    type="text",
                    text=f"No image files found in {input_folder} with extensions {file_extensions}"
                )]

            # Process each image
            processed_count = 0
            errors = []

            for image_file in image_files:
                try:
                    # Determine output path
                    output_file = output_folder / f"{image_file.stem}.out.png"

                    # Process the image
                    with open(image_file, "rb") as input_file:
                        input_data = input_file.read()

                    output_data = remove(
                        input_data,
                        session=session,
                        alpha_matting=alpha_matting,
                        only_mask=only_mask
                    )

                    # Save the output
                    with open(output_file, "wb") as output_file_handle:
                        output_file_handle.write(output_data)

                    processed_count += 1

                except Exception as e:
                    errors.append(f"Error processing {image_file.name}: {str(e)}")

            # Prepare result message
            result_parts = [
                f"Processed {processed_count} out of {len(image_files)} images",
                f"Model used: {model_name}",
                f"Output folder: {output_folder}"
            ]

            if errors:
                result_parts.append(f"Errors encountered:")
                result_parts.extend(errors)

            return [types.TextContent(
                type="text",
                text="\n".join(result_parts)
            )]

        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error processing folder: {str(e)}"
            )]

    def _get_session(self, model_name: str) -> Any:
        """Get or create a rembg session for the specified model."""
        if model_name not in self._sessions:
            self._sessions[model_name] = new_session(model_name)
        return self._sessions[model_name]

    async def run(self) -> None:
        """Run the MCP server."""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="rembg-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


def main() -> None:
    """Main entry point for the MCP server."""
    server = RembgMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()