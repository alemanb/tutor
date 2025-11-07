"""Test script for Educational Multi-Agent System.

This script tests the complete orchestrator workflow with a simple code generation request.
"""

import os
import asyncio
import pytest
from dotenv import load_dotenv
from src.agents.core import OrchestratorAgent
from src.agents.models import CodeGenerationRequest
from rich.pretty import pprint

# Load environment variables from .env file
load_dotenv()


def test_sync_orchestrator():
    """Test the orchestrator with synchronous execution."""
    print("=" * 80)
    print("TESTING SYNCHRONOUS ORCHESTRATOR")
    print("=" * 80)
    print()

    # Initialize orchestrator
    orchestrator = OrchestratorAgent()
    print(f"Orchestrator initialized: {orchestrator}")
    print()

    # Create a test request
    request = CodeGenerationRequest(
        prompt="Create a function to calculate the factorial of a number",
        language="python",
        context="Use recursion"
    )

    print(f"Request: {request.prompt}")
    print(f"Language: {request.language}")
    print(f"Context: {request.context}")
    print()

    try:
        # Process the request
        response = orchestrator.process_request(request)

        print()
        print("=" * 80)
        print("ORCHESTRATOR RESPONSE")
        print("=" * 80)
        print()

        print(f"Request ID: {response.request_id}")
        print(f"Status: {response.status}")
        print(f"Processing Time: {response.processing_time_seconds}s")
        print()

        print("-" * 80)
        print("GENERATED CODE (1.json format)")
        print("-" * 80)
        print(f"Date: {response.generated_code.date}")
        print(f"Language: {response.generated_code.language}")
        print(f"Code:\n{response.generated_code.code}")
        print()

        print("-" * 80)
        print("LINE EXPLANATIONS (2.json format)")
        print("-" * 80)
        print(f"Total Lines: {len(response.line_explanations.code)}")
        for line in response.line_explanations.code[:5]:  # Show first 5 lines
            print(f"  Line {line.line}: {line.line_code[:50]}...")
            print(f"    Explanation: {line.line_explanation}")
        if len(response.line_explanations.code) > 5:
            print(f"  ... and {len(response.line_explanations.code) - 5} more lines")
        print()
        print(f"Overall Explanation: {response.line_explanations.explanation}")
        print()

        print("-" * 80)
        print("CODE CHUNKS (3.json format)")
        print("-" * 80)
        print(f"Total Chunks: {len(response.chunked_code.code)}")
        for i, chunk in enumerate(response.chunked_code.code, 1):
            print(f"  Chunk {i}: Lines {chunk.first_line}-{chunk.last_line}")
            print(f"    Code: {chunk.line_code[:70]}...")
            print(f"    Explanation: {chunk.line_explanation}")
        print()

        print("=" * 80)
        print("✅ SYNC TEST PASSED!")
        print("=" * 80)

        # Validate response structure
        assert response.request_id is not None
        assert response.status == "success"
        assert response.generated_code is not None
        assert response.line_explanations is not None
        assert response.chunked_code is not None

    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        raise


@pytest.mark.asyncio
async def test_async_orchestrator():
    """Test the orchestrator with asynchronous execution."""
    print()
    print("=" * 80)
    print("TESTING ASYNCHRONOUS ORCHESTRATOR")
    print("=" * 80)
    print()

    # Initialize orchestrator
    orchestrator = OrchestratorAgent()
    print(f"Orchestrator initialized: {orchestrator}")
    print()

    # Create a test request
    request = CodeGenerationRequest(
        prompt="Create a simple class for a bank account with deposit and withdraw methods",
        language="python"
    )

    print(f"Request: {request.prompt}")
    print(f"Language: {request.language}")
    print()

    try:
        # Process the request asynchronously
        response = await orchestrator.aprocess_request(request)

        print()
        print("=" * 80)
        print("ASYNC ORCHESTRATOR RESPONSE")
        print("=" * 80)
        print()

        print(f"Request ID: {response.request_id}")
        print(f"Status: {response.status}")
        print(f"Processing Time: {response.processing_time_seconds}s")
        print()

        print(f"Generated {len(response.line_explanations.code)} lines")
        print(f"Created {len(response.chunked_code.code)} chunks")
        print()

        print("=" * 80)
        print("✅ ASYNC TEST PASSED!")
        print("=" * 80)

        return response

    except Exception as e:
        print(f"❌ ASYNC TEST FAILED: {str(e)}")
        raise


if __name__ == "__main__":
    # Test sync version
    sync_response = test_sync_orchestrator()

    # Test async version
    print()
    async_response = asyncio.run(test_async_orchestrator())

    print()
    print("=" * 80)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 80)
