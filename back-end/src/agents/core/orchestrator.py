"""Orchestrator Agent - Coordinates the Educational Multi-Agent System.

This orchestrator coordinates all three agents (Code Generator, Line Explainer,
Code Chunker) to provide a complete educational code generation experience.
"""

import time
import uuid
from datetime import datetime
from typing import Optional

from .code_generator import CodeGeneratorAgent
from .line_explainer import LineExplainerAgent
from .code_chunker import CodeChunkerAgent
from ..models.schemas import (
    CodeGenerationRequest,
    OrchestratorResponse,
    CodeGenerationOutput,
    LineExplanationOutput,
    CodeChunkOutput,
)


class OrchestratorAgent:
    """Coordinates the multi-agent educational code generation workflow.

    This orchestrator manages the complete workflow:
    1. Generate code (Agent 1: Code Generator)
    2. Explain line-by-line (Agent 2: Line Explainer)
    3. Chunk code sections (Agent 3: Code Chunker)

    It handles error recovery, tracks processing time, and generates unique
    request IDs for tracing.

    Attributes:
        code_generator: Code Generator Agent instance
        line_explainer: Line Explainer Agent instance
        code_chunker: Code Chunker Agent instance
        model_id: Claude model identifier used by all agents
    """

    def __init__(self, model_id: str = "claude-sonnet-4-20250514"):
        """Initialize the Orchestrator Agent.

        Args:
            model_id: Claude model identifier to use for all agents
        """
        self.model_id = model_id
        self.code_generator = CodeGeneratorAgent(model_id=model_id)
        self.line_explainer = LineExplainerAgent(model_id=model_id)
        self.code_chunker = CodeChunkerAgent(model_id=model_id)

    def process_request(self, request: CodeGenerationRequest) -> OrchestratorResponse:
        """Orchestrate the full workflow synchronously.

        This method coordinates all three agents to:
        1. Generate code based on user prompt
        2. Explain the code line-by-line
        3. Chunk the code into logical sections

        Args:
            request: CodeGenerationRequest with user prompt and preferences

        Returns:
            OrchestratorResponse containing all agent outputs and metadata

        Raises:
            Exception: If any agent fails or validation errors occur
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Step 1: Generate code (Agent 1)
            print(f"[{request_id}] Step 1/3: Generating code...")
            code_output: CodeGenerationOutput = self.code_generator.generate_code(request)
            print(f"[{request_id}] ✅ Code generated ({len(code_output.code)} chars)")

            # Step 2: Explain line-by-line (Agent 2)
            print(f"[{request_id}] Step 2/3: Explaining code line-by-line...")
            line_output: LineExplanationOutput = self.line_explainer.explain_code(code_output)
            print(f"[{request_id}] ✅ Explanations generated ({len(line_output.code)} lines)")

            # Step 3: Chunk code (Agent 3)
            print(f"[{request_id}] Step 3/3: Chunking code into sections...")
            chunk_output: CodeChunkOutput = self.code_chunker.chunk_code(line_output)
            print(f"[{request_id}] ✅ Code chunked ({len(chunk_output.code)} chunks)")

            # Calculate processing time
            processing_time = time.time() - start_time

            # Build final response
            response = OrchestratorResponse(
                request_id=request_id,
                generated_code=code_output,
                line_explanations=line_output,
                chunked_code=chunk_output,
                processing_time_seconds=round(processing_time, 2),
                status="success"
            )

            print(f"[{request_id}] 🎉 Complete! Processing time: {processing_time:.2f}s")
            return response

        except Exception as e:
            processing_time = time.time() - start_time
            error_message = f"Orchestration failed after {processing_time:.2f}s: {str(e)}"
            print(f"[{request_id}] ❌ {error_message}")
            raise Exception(error_message)

    async def aprocess_request(self, request: CodeGenerationRequest) -> OrchestratorResponse:
        """Orchestrate the full workflow asynchronously.

        This async method coordinates all three agents to:
        1. Generate code based on user prompt
        2. Explain the code line-by-line
        3. Chunk the code into logical sections

        Args:
            request: CodeGenerationRequest with user prompt and preferences

        Returns:
            OrchestratorResponse containing all agent outputs and metadata

        Raises:
            Exception: If any agent fails or validation errors occur
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Step 1: Generate code (Agent 1)
            print(f"[{request_id}] Step 1/3: Generating code...")
            code_output: CodeGenerationOutput = await self.code_generator.agenerate_code(request)
            print(f"[{request_id}] ✅ Code generated ({len(code_output.code)} chars)")

            # Step 2: Explain line-by-line (Agent 2)
            print(f"[{request_id}] Step 2/3: Explaining code line-by-line...")
            line_output: LineExplanationOutput = await self.line_explainer.aexplain_code(code_output)
            print(f"[{request_id}] ✅ Explanations generated ({len(line_output.code)} lines)")

            # Step 3: Chunk code (Agent 3)
            print(f"[{request_id}] Step 3/3: Chunking code into sections...")
            chunk_output: CodeChunkOutput = await self.code_chunker.achunk_code(line_output)
            print(f"[{request_id}] ✅ Code chunked ({len(chunk_output.code)} chunks)")

            # Calculate processing time
            processing_time = time.time() - start_time

            # Build final response
            response = OrchestratorResponse(
                request_id=request_id,
                generated_code=code_output,
                line_explanations=line_output,
                chunked_code=chunk_output,
                processing_time_seconds=round(processing_time, 2),
                status="success"
            )

            print(f"[{request_id}] 🎉 Complete! Processing time: {processing_time:.2f}s")
            return response

        except Exception as e:
            processing_time = time.time() - start_time
            error_message = f"Async orchestration failed after {processing_time:.2f}s: {str(e)}"
            print(f"[{request_id}] ❌ {error_message}")
            raise Exception(error_message)

    def get_agent_info(self) -> dict:
        """Get information about all agents in the orchestrator.

        Returns:
            Dictionary with agent details and configuration
        """
        return {
            "orchestrator": {
                "model_id": self.model_id,
                "agents": 3,
            },
            "agents": {
                "code_generator": {
                    "id": "code-generator",
                    "model": self.model_id,
                    "purpose": "Generate educational code",
                },
                "line_explainer": {
                    "id": "line-explainer",
                    "model": self.model_id,
                    "purpose": "Explain code line-by-line",
                },
                "code_chunker": {
                    "id": "code-chunker",
                    "model": self.model_id,
                    "purpose": "Group code into logical chunks",
                },
            },
        }

    def __repr__(self) -> str:
        """String representation of the orchestrator."""
        return f"OrchestratorAgent(model_id='{self.model_id}', agents=3)"
