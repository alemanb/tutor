"""Pytest configuration and fixtures for Educational Multi-Agent System tests.

This module provides shared fixtures and configuration for all tests.
"""

import os
from pathlib import Path
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

# Load environment variables from back-end/.env
# Get the back-end directory (3 levels up from conftest.py location)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


# ============================================================================
# Session-scope Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def api_key():
    """Ensure ANTHROPIC_API_KEY is available."""
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("ANTHROPIC_API_KEY not set in environment")
    return key


# ============================================================================
# Module-scope Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def orchestrator():
    """Create an OrchestratorAgent instance for testing."""
    from src.agents.core import OrchestratorAgent
    return OrchestratorAgent()


@pytest.fixture(scope="module")
def code_generator():
    """Create a CodeGeneratorAgent instance for testing."""
    from src.agents.core import CodeGeneratorAgent
    return CodeGeneratorAgent()


@pytest.fixture(scope="module")
def line_explainer():
    """Create a LineExplainerAgent instance for testing."""
    from src.agents.core import LineExplainerAgent
    return LineExplainerAgent()


@pytest.fixture(scope="module")
def code_chunker():
    """Create a CodeChunkerAgent instance for testing."""
    from src.agents.core import CodeChunkerAgent
    return CodeChunkerAgent()


# ============================================================================
# Function-scope Fixtures
# ============================================================================

@pytest.fixture
def simple_code_request():
    """Create a simple code generation request."""
    from src.agents.models import CodeGenerationRequest
    return CodeGenerationRequest(
        prompt="Create a function to add two numbers",
        language="python",
        context="Keep it simple"
    )


@pytest.fixture
def factorial_request():
    """Create a factorial code generation request."""
    from src.agents.models import CodeGenerationRequest
    return CodeGenerationRequest(
        prompt="Create a function to calculate factorial",
        language="python",
        context="Use recursion"
    )


@pytest.fixture
def class_request():
    """Create a class generation request."""
    from src.agents.models import CodeGenerationRequest
    return CodeGenerationRequest(
        prompt="Create a simple class for a bank account with deposit and withdraw methods",
        language="python"
    )


@pytest.fixture
def sample_code_output():
    """Create a sample CodeGenerationOutput."""
    from src.agents.models import CodeGenerationOutput
    return CodeGenerationOutput(
        date="2025-11-06T12:00:00",
        language="python",
        code="def add(a, b):\n    return a + b\n\n# Example usage\nresult = add(5, 3)\nprint(result)"
    )


@pytest.fixture
def sample_line_output():
    """Create a sample LineExplanationOutput."""
    from src.agents.models import LineExplanationOutput, CodeLine
    return LineExplanationOutput(
        date="2025-11-06T12:00:00",
        language="python",
        code=[
            CodeLine(line=1, line_code="def add(a, b):", line_explanation="Define a function"),
            CodeLine(line=2, line_code="    return a + b", line_explanation="Return the sum"),
            CodeLine(line=3, line_code="", line_explanation=None),
            CodeLine(line=4, line_code="# Example usage", line_explanation="Comment for usage"),
            CodeLine(line=5, line_code="result = add(5, 3)", line_explanation="Call the function"),
        ],
        explanation="A simple addition function with usage example"
    )


# ============================================================================
# FastAPI Test Client
# ============================================================================

@pytest.fixture(scope="module")
def test_client():
    """Create a FastAPI TestClient for integration tests."""
    from src.agents.server import app
    return TestClient(app)


# ============================================================================
# Markers
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "agents: marks tests for agent functionality"
    )
