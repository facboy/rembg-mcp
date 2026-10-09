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
from PIL import Image
from rembg import new_session, remove
from rembg.sessions import sessions_names


class RembgMCPServer:
    """MCP Server for rembg background removal operations."""

    def __init__(self) -> None:
        self.server = Server("rembg-mcp", version="0.1.0")
        self._sessions: Dict[str, Any] = {}
        self._model_descriptions = self._get_model_descriptions()
        self._setup_handlers()

    def _get_model_descriptions(self) -> Dict[str, str]:
        """Get descriptions for each model based on their use cases."""
        return {
            "u2net": "General purpose model with good balance of speed and accuracy. Best for most common use cases.",
            "u2netp": "Lightweight version of U2Net with faster inference but slightly lower accuracy.",
            "u2net_human_seg": "Optimized for human portrait segmentation. Best for photos of people.",
            "u2net_cloth_seg": "Specialized for clothing and fashion items segmentation.",
            "silueta": "Very lightweight model for quick processing when speed is priority over accuracy.",
            "isnet-general-use": "ISNet model for general use cases with good edge preservation.",
            "isnet-anime": "Specialized for anime and cartoon-style images with clean line art.",
            "birefnet-general": "High accuracy BiRefNet model for general use cases. Slower but very precise.",
            "birefnet-general-lite": "Lighter version of BiRefNet-general with faster processing.",
            "birefnet-portrait": "Optimized for portrait photography with excellent hair and edge detail.",
            "birefnet-dis": "BiRefNet model trained on Distinguishable Image Segmentation dataset.",
            "birefnet-hrsod": "High-resolution salient object detection model for detailed segmentation.",
            "birefnet-cod": "Camouflaged object detection model for complex backgrounds.",
            "birefnet-massive": "Largest BiRefNet model with highest accuracy but slowest processing.",
            "sam": "Segment Anything Model supporting interactive prompts (points, boxes). Most versatile.",
            "dis-anime": "DIS model specialized for anime and cartoon images.",
            "dis-custom": "Custom DIS model variant.",
            "dis-general-use": "DIS model for general purpose background removal.",
            "bria-rmbg": "BRIA background removal model with commercial-friendly license.",
            "ben-custom": "Custom Ben model variant."
        }

    def _get_available_models(self) -> List[str]:
        """Get list of models that are actually available (downloaded) on the system."""
        from rembg.sessions.base import BaseSession

        u2net_home = BaseSession.u2net_home()
        available_models = []

        # Map model names to their actual ONNX filenames
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
            "birefnet-massive": "birefnet-massive.onnx",
            "dis-anime": "dis-anime.onnx",
            "dis-custom": "dis-custom.onnx",
            "dis-general-use": "dis-general-use.onnx",
            "bria-rmbg": "bria-rmbg.onnx",
            "ben-custom": "ben-custom.onnx"
        }

        for model_name in sessions_names:
            model_files_exist = False

            if model_name == "sam":
                encoder_path = os.path.join(u2net_home, "sam_vit_b_01ec64.encoder.onnx")
                decoder_path = os.path.join(u2net_home, "sam_vit_b_01ec64.decoder.onnx")
                model_files_exist = os.path.exists(encoder_path) and os.path.exists(decoder_path)
            else:
                # Use the mapped filename if available, otherwise fall back to default pattern
                filename = filename_map.get(model_name, f"{model_name}.onnx")
                model_path = os.path.join(u2net_home, filename)
                model_files_exist = os.path.exists(model_path)

            if model_files_exist:
                available_models.append(model_name)

        return available_models if available_models else sessions_names

    def _setup_handlers(self) -> None:
        """Register the MCP request handlers."""

        async def handle_list_tools(
            ctx: Any, params: types.PaginatedRequestParams | None
        ) -> types.ListToolsResult:
            """List available tools."""
            available_models = self._get_available_models()
            model_enum_with_descriptions = []

            for model in available_models:
                description = self._model_descriptions.get(model, f"Model: {model}")
                model_enum_with_descriptions.append({"const": model, "description": description})

            tools = [
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
                                "description": "Model to use for background removal. Each model is optimized for different use cases.",
                                "default": "u2net",
                                "oneOf": model_enum_with_descriptions
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
                                "description": "Model to use for background removal. Each model is optimized for different use cases.",
                                "default": "u2net",
                                "oneOf": model_enum_with_descriptions
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
            return types.ListToolsResult(tools=tools)

        async def handle_call_tool(
            ctx: Any, params: types.CallToolRequestParams
        ) -> types.CallToolResult:
            """Handle tool calls."""
            name = params.name
            arguments = params.arguments or {}
            if name == "rembg-i":
                content = await self._handle_rembg_i(arguments)
            elif name == "rembg-p":
                content = await self._handle_rembg_p(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
            return types.CallToolResult(content=content)

        self.server.add_request_handler(
            "tools/list", types.PaginatedRequestParams, handle_list_tools
        )
        self.server.add_request_handler(
            "tools/call", types.CallToolRequestParams, handle_call_tool
        )

    async def _handle_rembg_i(self, arguments: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
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

    async def _handle_rembg_p(self, arguments: Dict[str, Any]) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
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
                self.server.create_initialization_options(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            )


def main() -> None:
    """Main entry point for the MCP server."""
    server = RembgMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()