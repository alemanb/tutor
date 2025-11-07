# Educational Multi-Agent System - API Documentation

**Version**: 1.0.0
**Base URL**: `http://localhost:8000`
**API Type**: REST
**Content-Type**: `application/json`

---

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URLs](#base-urls)
- [Endpoints](#endpoints)
  - [Root Endpoint](#root-endpoint)
  - [Health Check](#health-check)
  - [Readiness Check](#readiness-check)
  - [Agent Information](#agent-information)
  - [Generate Educational Code](#generate-educational-code)
- [Request/Response Formats](#requestresponse-formats)
- [Error Codes](#error-codes)
- [Rate Limits](#rate-limits)
- [Examples](#examples)

---

## Overview

The Educational Multi-Agent System API provides endpoints for generating educational code with comprehensive explanations. The system uses three specialized AI agents:

1. **Code Generator** - Creates clean, educational code based on prompts
2. **Line Explainer** - Provides line-by-line educational explanations
3. **Code Chunker** - Groups code into logical sections

All code generation is powered by Claude Sonnet 4.0 from Anthropic.

---

## Authentication

Currently, the API does not require authentication for endpoint access. However, the backend requires an `ANTHROPIC_API_KEY` environment variable to function.

**Future Versions**: API key authentication will be added for production deployments.

---

## Base URLs

| Environment | Base URL |
|-------------|----------|
| Development | `http://localhost:8000` |
| Production | `https://your-domain.com` |

---

## Endpoints

### Root Endpoint

**GET** `/`

Returns API information and available endpoints.

**Response**: `200 OK`

```json
{
  "message": "Educational Multi-Agent System API",
  "version": "1.0.0",
  "documentation": {
    "swagger_ui": "/docs",
    "redoc": "/redoc"
  },
  "endpoints": {
    "health": "/health",
    "generate_code": "/api/v1/generate",
    "agent_info": "/api/v1/agents/info"
  },
  "timestamp": "2025-11-06T12:00:00.000000"
}
```

---

### Health Check

**GET** `/health`

Health check endpoint for monitoring and load balancers.

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2025-11-06T12:00:00.000000",
  "service": "educational-multi-agent-system",
  "version": "1.0.0",
  "agents": {
    "orchestrator": "claude-sonnet-4-20250514",
    "total_agents": 3
  },
  "api_key_configured": true
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Service health status (`healthy` or `unhealthy`) |
| `timestamp` | string | ISO 8601 timestamp |
| `service` | string | Service name |
| `version` | string | API version |
| `agents.orchestrator` | string | Claude model ID being used |
| `agents.total_agents` | integer | Number of agents in the system |
| `api_key_configured` | boolean | Whether ANTHROPIC_API_KEY is set |

---

### Readiness Check

**GET** `/health/ready`

Kubernetes/container readiness probe endpoint.

**Response**: `200 OK`

```json
{
  "ready": true,
  "timestamp": "2025-11-06T12:00:00.000000",
  "checks": {
    "api_key": true,
    "orchestrator": true
  }
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `ready` | boolean | Overall readiness status |
| `timestamp` | string | ISO 8601 timestamp |
| `checks.api_key` | boolean | ANTHROPIC_API_KEY is configured |
| `checks.orchestrator` | boolean | Orchestrator is initialized |

---

### Agent Information

**GET** `/api/v1/agents/info`

Returns information about the multi-agent system configuration.

**Response**: `200 OK`

```json
{
  "orchestrator": {
    "model_id": "claude-sonnet-4-20250514",
    "agents": 3
  },
  "agents": {
    "code_generator": {
      "id": "code-generator",
      "model": "claude-sonnet-4-20250514",
      "purpose": "Generate educational code"
    },
    "line_explainer": {
      "id": "line-explainer",
      "model": "claude-sonnet-4-20250514",
      "purpose": "Explain code line-by-line"
    },
    "code_chunker": {
      "id": "code-chunker",
      "model": "claude-sonnet-4-20250514",
      "purpose": "Group code into logical chunks"
    }
  }
}
```

---

### Generate Educational Code

**POST** `/api/v1/generate`

Generates educational code with line-by-line explanations and logical chunking.

**Request Body**:

```json
{
  "prompt": "Create a function to calculate factorial",
  "language": "python",
  "context": "Use recursion"
}
```

**Request Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Description of the code to generate |
| `language` | string | No | Programming language (default: `python`) |
| `context` | string | No | Additional context or requirements |

**Supported Languages**:
- `python`
- `javascript`
- `typescript`
- `java`
- `c++`
- `go`
- `rust`
- And any language supported by Claude

**Response**: `200 OK`

```json
{
  "request_id": "82db599d-de59-44df-b525-35b6065eaad6",
  "status": "success",
  "processing_time_seconds": 47.01,
  "generated_code": {
    "date": "2025-11-06T12:00:00",
    "language": "python",
    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
  },
  "line_explanations": {
    "date": "2025-11-06T12:00:00",
    "language": "python",
    "code": [
      {
        "line": 1,
        "line_code": "def factorial(n):",
        "line_explanation": "Define a function called factorial that takes one parameter n"
      },
      {
        "line": 2,
        "line_code": "    if n <= 1:",
        "line_explanation": "Base case: if n is 1 or less, stop recursion"
      }
    ],
    "explanation": "This function calculates the factorial using recursion"
  },
  "chunked_code": {
    "date": "2025-11-06T12:00:00",
    "language": "python",
    "code": [
      {
        "first_line": 1,
        "last_line": 4,
        "line_code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
        "line_explanation": "Complete function definition with base case and recursive case"
      }
    ],
    "explanation": "This function calculates the factorial using recursion"
  }
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | string (UUID) | Unique identifier for this request |
| `status` | string | Request status (`success` or `error`) |
| `processing_time_seconds` | float | Total processing time in seconds |
| `generated_code` | object | Generated code (1.json format) |
| `generated_code.date` | string | ISO 8601 timestamp of generation |
| `generated_code.language` | string | Programming language |
| `generated_code.code` | string | Generated code with `\n` line breaks |
| `line_explanations` | object | Line-by-line explanations (2.json format) |
| `line_explanations.code` | array | Array of line objects |
| `line_explanations.code[].line` | integer | Line number (1-indexed) |
| `line_explanations.code[].line_code` | string | Code on this line |
| `line_explanations.code[].line_explanation` | string\|null | Explanation (null for blank lines) |
| `line_explanations.explanation` | string | Overall code explanation |
| `chunked_code` | object | Logical code chunks (3.json format) |
| `chunked_code.code` | array | Array of chunk objects |
| `chunked_code.code[].first_line` | integer | First line of chunk |
| `chunked_code.code[].last_line` | integer | Last line of chunk |
| `chunked_code.code[].line_code` | string | Code in this chunk |
| `chunked_code.code[].line_explanation` | string | Why these lines are grouped |

**Error Response**: `400 Bad Request`

```json
{
  "detail": "Prompt cannot be empty"
}
```

**Error Response**: `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Error Response**: `500 Internal Server Error`

```json
{
  "detail": "Code generation failed: [error message]"
}
```

**Performance**:
- Average processing time: 45-80 seconds
- Depends on code complexity and length
- Three sequential AI model calls

---

## Request/Response Formats

### Content Type

All requests and responses use `application/json`.

**Request Headers**:
```
Content-Type: application/json
```

**Response Headers**:
```
Content-Type: application/json
X-Process-Time: 47.01
```

### Line Breaks in Code

Generated code uses `\n` for line breaks and `\n\n` for blank lines.

**Example**:
```json
{
  "code": "def add(a, b):\n    return a + b\n\n# Example\nresult = add(5, 3)"
}
```

**Rendered**:
```python
def add(a, b):
    return a + b

# Example
result = add(5, 3)
```

---

## Error Codes

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| `200` | OK | Successful request |
| `400` | Bad Request | Empty prompt or invalid request data |
| `422` | Unprocessable Entity | Missing required fields or validation error |
| `500` | Internal Server Error | Code generation failed or server error |

### Error Response Format

All errors return a JSON object with a `detail` field:

```json
{
  "detail": "Description of the error"
}
```

For validation errors (422), the response includes field-specific errors:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

---

## Rate Limits

**Current**: No rate limits implemented

**Recommended for Production**:
- 10 requests per minute per IP
- 100 requests per hour per IP
- Implement using middleware (e.g., `slowapi`)

---

## Examples

### Example 1: Simple Function Generation

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to check if a number is prime",
    "language": "python"
  }'
```

**Response** (abbreviated):
```json
{
  "request_id": "abc123...",
  "status": "success",
  "processing_time_seconds": 52.3,
  "generated_code": {
    "language": "python",
    "code": "def is_prime(n):\n    if n < 2:\n        return False\n    ..."
  }
}
```

---

### Example 2: Class Generation with Context

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a Stack class",
    "language": "python",
    "context": "Implement push, pop, and peek methods"
  }'
```

---

### Example 3: JavaScript Function

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to debounce user input",
    "language": "javascript"
  }'
```

---

### Example 4: Using Python Requests Library

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "prompt": "Create a binary search function",
        "language": "python",
        "context": "Handle edge cases"
    }
)

data = response.json()
print(f"Request ID: {data['request_id']}")
print(f"Generated Code:\n{data['generated_code']['code']}")
```

---

### Example 5: Using JavaScript Fetch

```javascript
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'Create a function to merge two sorted arrays',
    language: 'javascript'
  })
});

const data = await response.json();
console.log('Request ID:', data.request_id);
console.log('Code:', data.generated_code.code);
```

---

## Interactive Documentation

### Swagger UI

Interactive API documentation with "Try it out" functionality:

**URL**: `http://localhost:8000/docs`

**Features**:
- Test endpoints directly from browser
- See request/response examples
- Automatic schema validation
- Download OpenAPI specification

### ReDoc

Beautiful, responsive API documentation:

**URL**: `http://localhost:8000/redoc`

**Features**:
- Clean, professional layout
- Search functionality
- Code samples
- Three-column layout

---

## OpenAPI Specification

Download the complete OpenAPI 3.0 specification:

**URL**: `http://localhost:8000/openapi.json`

Use with API clients like:
- Postman
- Insomnia
- Swagger Editor
- Redocly

---

## SDK Examples

### Python SDK Example

```python
from dataclasses import dataclass
import requests

@dataclass
class CodeRequest:
    prompt: str
    language: str = "python"
    context: str = None

class EducationalCodeClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def generate_code(self, request: CodeRequest):
        response = requests.post(
            f"{self.base_url}/api/v1/generate",
            json={
                "prompt": request.prompt,
                "language": request.language,
                "context": request.context
            }
        )
        response.raise_for_status()
        return response.json()

    def health_check(self):
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage
client = EducationalCodeClient()
result = client.generate_code(
    CodeRequest(
        prompt="Create a linked list class",
        language="python"
    )
)
print(result['generated_code']['code'])
```

---

## Best Practices

### 1. Handle Long Processing Times

Code generation takes 45-80 seconds. Implement:
- Loading indicators in UI
- Timeout handling (90+ seconds)
- Retry logic for failures

### 2. Validate Input

Always validate before sending:
- Non-empty prompt
- Valid language identifier
- Reasonable prompt length (<1000 chars recommended)

### 3. Error Handling

```python
try:
    response = requests.post(url, json=data, timeout=90)
    response.raise_for_status()
    result = response.json()
except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as e:
    print(f"HTTP error: {e.response.json()['detail']}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 4. Use Request IDs

Store `request_id` for:
- Debugging
- Support requests
- Audit trails
- Analytics

---

## Changelog

### Version 1.0.0 (2025-11-06)

**Initial Release**:
- POST /api/v1/generate endpoint
- GET /health endpoint
- GET /health/ready endpoint
- GET /api/v1/agents/info endpoint
- OpenAPI documentation
- Claude Sonnet 4.0 integration

---

## Support

**Issues**: Report bugs or request features via GitHub Issues
**Email**: support@example.com
**Documentation**: http://localhost:8000/docs

---

**Last Updated**: November 6, 2025
**API Version**: 1.0.0
