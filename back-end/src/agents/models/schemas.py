"""Pydantic models for Educational Multi-Agent System.

This module defines the JSON schemas used for communication between agents
and API endpoints, matching the format specifications in docs/ai_agent_json_format/.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# INPUT MODELS
# ============================================================================

class CodeGenerationRequest(BaseModel):
    """User's code generation request (API input)."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Create a function to calculate factorial",
                "language": "python",
                "context": "Use recursion"
            }
        }
    )

    prompt: str = Field(..., description="User's code request describing what to generate")
    language: str = Field(default="python", description="Programming language (python, javascript, etc.)")
    context: Optional[str] = Field(None, description="Additional context or requirements")


# ============================================================================
# AGENT 1: CODE GENERATOR OUTPUT (1.json format)
# ============================================================================

class CodeGenerationOutput(BaseModel):
    """Output from Code Generator Agent matching 1.json format."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-31T12:00:00",
                "language": "python",
                "code": "def factorial(n):\\n    if n <= 1:\\n        return 1\\n    return n * factorial(n - 1)"
            }
        }
    )

    date: str = Field(..., description="ISO format timestamp (YYYY-MM-DDTHH:MM:SS)")
    language: str = Field(..., description="Programming language of generated code")
    code: str = Field(..., description="Generated code with \\n for line breaks, \\n\\n for blank lines")


# ============================================================================
# AGENT 2: LINE EXPLAINER OUTPUT (2.json format)
# ============================================================================

class CodeLine(BaseModel):
    """Individual line of code with explanation."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "line": 1,
                "line_code": "def factorial(n):",
                "line_explanation": "Define a function named factorial that takes one parameter n"
            }
        }
    )

    line: int = Field(..., description="Line number (1-indexed)")
    line_code: str = Field(..., description="Exact code from this line")
    line_explanation: Optional[str] = Field(None, description="Educational explanation (null for blank lines)")


class LineExplanationOutput(BaseModel):
    """Output from Line Explainer Agent matching 2.json format."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-31T12:00:00",
                "language": "python",
                "code": [
                    {
                        "line": 1,
                        "line_code": "def factorial(n):",
                        "line_explanation": "Define a function named factorial that takes one parameter n"
                    },
                    {
                        "line": 2,
                        "line_code": "    if n <= 1:",
                        "line_explanation": "Base case: if n is 1 or less, stop recursion"
                    }
                ],
                "explanation": "This function calculates the factorial of a number using recursion"
            }
        }
    )

    date: str = Field(..., description="ISO format timestamp (preserved from code generation)")
    language: str = Field(..., description="Programming language (preserved from code generation)")
    code: List[CodeLine] = Field(..., description="List of code lines with individual explanations")
    explanation: str = Field(..., description="Overall explanation of what the entire code does")


# ============================================================================
# AGENT 3: CODE CHUNKER OUTPUT (3.json format)
# ============================================================================

class CodeChunk(BaseModel):
    """Logical grouping of related code lines."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_line": 1,
                "last_line": 2,
                "line_code": "import os\\nimport sys",
                "line_explanation": "Import statements - loading required system modules"
            }
        }
    )

    first_line: int = Field(..., description="Starting line number of chunk (1-indexed)")
    last_line: int = Field(..., description="Ending line number of chunk (inclusive)")
    line_code: str = Field(..., description="Code content from first_line to last_line")
    line_explanation: Optional[str] = Field(None, description="Explanation of why these lines are grouped")


class CodeChunkOutput(BaseModel):
    """Output from Code Chunker Agent matching 3.json format."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-10-31T12:00:00",
                "language": "python",
                "code": [
                    {
                        "first_line": 1,
                        "last_line": 1,
                        "line_code": "def factorial(n):",
                        "line_explanation": "Function definition"
                    },
                    {
                        "first_line": 2,
                        "last_line": 4,
                        "line_code": "    if n <= 1:\\n        return 1\\n    return n * factorial(n - 1)",
                        "line_explanation": "Function body with base case and recursive case"
                    }
                ],
                "explanation": "This function calculates the factorial of a number using recursion"
            }
        }
    )

    date: str = Field(..., description="ISO format timestamp (preserved from code generation)")
    language: str = Field(..., description="Programming language (preserved from code generation)")
    code: List[CodeChunk] = Field(..., description="List of logical code chunks with explanations")
    explanation: str = Field(..., description="Overall explanation (preserved from line explainer)")


# ============================================================================
# ORCHESTRATOR OUTPUT (Final API Response)
# ============================================================================

class OrchestratorResponse(BaseModel):
    """Final response from orchestrator containing all agent outputs."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "request_id": "123e4567-e89b-12d3-a456-426614174000",
                "generated_code": {"date": "2025-10-31T12:00:00", "language": "python", "code": "def factorial(n):\\n    return 1 if n <= 1 else n * factorial(n - 1)"},
                "line_explanations": {"date": "2025-10-31T12:00:00", "language": "python", "code": [], "explanation": "Recursive factorial function"},
                "chunked_code": {"date": "2025-10-31T12:00:00", "language": "python", "code": [], "explanation": "Recursive factorial function"},
                "processing_time_seconds": 12.5,
                "status": "success"
            }
        }
    )

    request_id: str = Field(..., description="Unique identifier for this request (UUID)")
    generated_code: CodeGenerationOutput = Field(..., description="Output from Code Generator (1.json format)")
    line_explanations: LineExplanationOutput = Field(..., description="Output from Line Explainer (2.json format)")
    chunked_code: CodeChunkOutput = Field(..., description="Output from Code Chunker (3.json format)")
    processing_time_seconds: float = Field(..., description="Total processing time for all agents")
    status: str = Field(default="success", description="Request status (success, error, partial)")


# ============================================================================
# HELPER UTILITIES
# ============================================================================

def get_current_timestamp() -> str:
    """Generate current timestamp in ISO format for consistency.

    Returns:
        str: ISO 8601 formatted timestamp (e.g., "2025-10-31T12:00:00")
    """
    return datetime.now().isoformat()


def validate_line_numbers(chunks: List[CodeChunk]) -> bool:
    """Validate that chunk line numbers are consistent.

    Args:
        chunks: List of code chunks to validate

    Returns:
        bool: True if all chunks have valid line numbers (first_line <= last_line)
    """
    return all(chunk.first_line <= chunk.last_line for chunk in chunks)
