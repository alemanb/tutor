"""Test script for FastAPI server endpoints.

This script tests all API endpoints using the FastAPI TestClient.
"""

import json
from fastapi.testclient import TestClient
from src.agents.server import app

# Create test client
client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    print("=" * 80)
    print("Testing Root Endpoint: GET /")
    print("=" * 80)

    response = client.get("/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

    print("✅ Root endpoint test passed!\n")


def test_health_endpoint():
    """Test the health check endpoint."""
    print("=" * 80)
    print("Testing Health Endpoint: GET /health")
    print("=" * 80)

    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "service" in data
    assert data["api_key_configured"] is True

    print("✅ Health endpoint test passed!\n")


def test_readiness_endpoint():
    """Test the readiness check endpoint."""
    print("=" * 80)
    print("Testing Readiness Endpoint: GET /health/ready")
    print("=" * 80)

    response = client.get("/health/ready")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

    assert response.status_code == 200
    data = response.json()
    assert data["ready"] is True
    assert "checks" in data

    print("✅ Readiness endpoint test passed!\n")


def test_agent_info_endpoint():
    """Test the agent info endpoint."""
    print("=" * 80)
    print("Testing Agent Info Endpoint: GET /api/v1/agents/info")
    print("=" * 80)

    response = client.get("/api/v1/agents/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))

    assert response.status_code == 200
    data = response.json()
    assert "orchestrator" in data
    assert "agents" in data

    print("✅ Agent info endpoint test passed!\n")


def test_generate_endpoint_validation():
    """Test request validation on the generate endpoint."""
    print("=" * 80)
    print("Testing Generate Endpoint Validation: POST /api/v1/generate")
    print("=" * 80)

    # Test with missing prompt
    print("\n1. Testing with missing prompt...")
    response = client.post("/api/v1/generate", json={
        "language": "python"
    })
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 422  # Validation error
    print("✅ Missing prompt validation works!")

    # Test with empty prompt
    print("\n2. Testing with empty prompt...")
    response = client.post("/api/v1/generate", json={
        "prompt": "",
        "language": "python"
    })
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400  # Bad request
    print("✅ Empty prompt validation works!")

    print("\n✅ All validation tests passed!\n")


def test_generate_endpoint_success():
    """Test successful code generation."""
    print("=" * 80)
    print("Testing Generate Endpoint Success: POST /api/v1/generate")
    print("=" * 80)

    request_data = {
        "prompt": "Create a simple function to add two numbers",
        "language": "python",
        "context": "Keep it very simple"
    }

    print(f"Request:")
    print(json.dumps(request_data, indent=2))
    print()

    print("⏳ Sending request (this will take ~60-90 seconds)...")
    response = client.post("/api/v1/generate", json=request_data)

    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        print("\n" + "=" * 80)
        print("RESPONSE SUMMARY")
        print("=" * 80)
        print(f"Request ID: {data['request_id']}")
        print(f"Status: {data['status']}")
        print(f"Processing Time: {data['processing_time_seconds']}s")
        print()

        print("-" * 80)
        print("GENERATED CODE")
        print("-" * 80)
        print(f"Date: {data['generated_code']['date']}")
        print(f"Language: {data['generated_code']['language']}")
        print(f"Code Length: {len(data['generated_code']['code'])} characters")
        print(f"\nCode:\n{data['generated_code']['code']}")
        print()

        print("-" * 80)
        print("LINE EXPLANATIONS")
        print("-" * 80)
        print(f"Total Lines: {len(data['line_explanations']['code'])}")
        for i, line in enumerate(data['line_explanations']['code'][:3], 1):
            print(f"\nLine {line['line']}: {line['line_code']}")
            print(f"  Explanation: {line['line_explanation']}")
        if len(data['line_explanations']['code']) > 3:
            print(f"\n... and {len(data['line_explanations']['code']) - 3} more lines")
        print()

        print("-" * 80)
        print("CODE CHUNKS")
        print("-" * 80)
        print(f"Total Chunks: {len(data['chunked_code']['code'])}")
        for i, chunk in enumerate(data['chunked_code']['code'], 1):
            print(f"\nChunk {i}: Lines {chunk['first_line']}-{chunk['last_line']}")
            print(f"  Explanation: {chunk['line_explanation']}")
        print()

        # Validate response structure
        assert "request_id" in data
        assert "generated_code" in data
        assert "line_explanations" in data
        assert "chunked_code" in data
        assert "processing_time_seconds" in data
        assert data["status"] == "success"

        # Validate generated_code structure
        assert "date" in data["generated_code"]
        assert "language" in data["generated_code"]
        assert "code" in data["generated_code"]

        # Validate line_explanations structure
        assert "code" in data["line_explanations"]
        assert isinstance(data["line_explanations"]["code"], list)
        assert len(data["line_explanations"]["code"]) > 0

        # Validate chunked_code structure
        assert "code" in data["chunked_code"]
        assert isinstance(data["chunked_code"]["code"], list)
        assert len(data["chunked_code"]["code"]) > 0

        print("=" * 80)
        print("✅ Generate endpoint test passed!")
        print("=" * 80)

    else:
        print(f"❌ Test failed with status code: {response.status_code}")
        print(f"Response: {response.json()}")
        raise AssertionError(f"Expected status code 200, got {response.status_code}")


def run_all_tests():
    """Run all tests in sequence."""
    print("\n" + "=" * 80)
    print("🧪 RUNNING FASTAPI SERVER TESTS")
    print("=" * 80 + "\n")

    try:
        # Quick tests
        test_root_endpoint()
        test_health_endpoint()
        test_readiness_endpoint()
        test_agent_info_endpoint()
        test_generate_endpoint_validation()

        # Long test (actual code generation)
        test_generate_endpoint_success()

        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 80 + "\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}\n")
        raise
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
