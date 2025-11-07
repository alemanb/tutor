"""Pydantic models for Educational Multi-Agent System."""

from .schemas import (
    # Input models
    CodeGenerationRequest,

    # Agent 1: Code Generator
    CodeGenerationOutput,

    # Agent 2: Line Explainer
    CodeLine,
    LineExplanationOutput,

    # Agent 3: Code Chunker
    CodeChunk,
    CodeChunkOutput,

    # Orchestrator
    OrchestratorResponse,

    # Utilities
    get_current_timestamp,
    validate_line_numbers,
)

__all__ = [
    "CodeGenerationRequest",
    "CodeGenerationOutput",
    "CodeLine",
    "LineExplanationOutput",
    "CodeChunk",
    "CodeChunkOutput",
    "OrchestratorResponse",
    "get_current_timestamp",
    "validate_line_numbers",
]
