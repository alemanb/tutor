# Educational Multi-Agent System Implementation Workflow

## Executive Summary

**Project**: Educational Code Generation & Explanation Multi-Agent System
**Framework**: Agno (https://docs.agno.com)
**Server**: FastAPI with AgentOS Integration
**Purpose**: Generate code, provide line-by-line explanations, and group code sections for educational purposes

**Key Components**:
- 4 Agents: Orchestrator, Code Generator, Line Explainer, Code Chunker
- Pydantic models for type-safe JSON schemas
- FastAPI server with AgentOS
- Comprehensive test suite
- DateTime integration for accurate timestamps

---

## Phase 1: Project Foundation & Setup (Week 1)

### Task 1.1: Environment & Dependencies Setup
**Estimated Time**: 2 hours
**Persona**: Backend Developer
**Dependencies**: None

#### Steps:
1. **Install uv Package Manager**
   ```bash
   # Install uv (if not already installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or using pip
   pip install uv
   ```

2. **Install Core Dependencies with uv**
   ```bash
   uv add agno pydantic fastapi uvicorn sqlalchemy psycopg pgvector python-multipart anthropic openai
   ```

3. **Update pyproject.toml**
   - Add dependencies to `[project.dependencies]`
   - Specify version constraints
   - Configure development dependencies

4. **Verify Installation**
   ```bash
   python -c "import agno, pydantic, fastapi; print('Dependencies installed successfully')"
   ```

**Acceptance Criteria**:
- ✅ All dependencies installed without errors
- ✅ pyproject.toml updated with proper versioning
- ✅ Import verification passes

---

### Task 1.2: Define Pydantic Models for JSON Schemas
**Estimated Time**: 4 hours
**Persona**: Backend Developer
**Dependencies**: Task 1.1
**Location**: `back-end/src/agents/models/schemas.py`

#### Implementation:

**Step 1**: Create base models matching JSON formats (1.json, 2.json, 3.json)

**File Structure**:
```
back-end/src/agents/models/
├── __init__.py
├── schemas.py          # Pydantic models for agent I/O
└── agent_config.py     # Agent configuration models
```

**Pydantic Models to Create**:

1. **CodeGenerationRequest** (Input from user)
   ```python
   from pydantic import BaseModel, Field
   from datetime import datetime

   class CodeGenerationRequest(BaseModel):
       prompt: str = Field(..., description="User's code request")
       language: str = Field(default="python", description="Programming language")
       context: str | None = Field(None, description="Additional context")
   ```

2. **CodeGenerationOutput** (Agent 1 → 1.json format)
   ```python
   class CodeGenerationOutput(BaseModel):
       date: str = Field(..., description="ISO format timestamp")
       language: str
       code: str = Field(..., description="Generated code with \\n for line breaks")
   ```

3. **LineExplanationOutput** (Agent 2 → 2.json format)
   ```python
   from typing import List, Optional

   class CodeLine(BaseModel):
       line: int
       line_code: str
       line_explanation: Optional[str] = None

   class LineExplanationOutput(BaseModel):
       date: str
       language: str
       code: List[CodeLine]
       explanation: str = Field(..., description="Overall code explanation")
   ```

4. **CodeChunkOutput** (Agent 3 → 3.json format)
   ```python
   class CodeChunk(BaseModel):
       first_line: int
       last_line: int
       line_code: str
       line_explanation: Optional[str] = None

   class CodeChunkOutput(BaseModel):
       date: str
       language: str
       code: List[CodeChunk]
       explanation: str
   ```

5. **OrchestratorResponse** (Final output)
   ```python
   class OrchestratorResponse(BaseModel):
       request_id: str
       generated_code: CodeGenerationOutput
       line_explanations: LineExplanationOutput
       chunked_code: CodeChunkOutput
       processing_time_seconds: float
       status: str = Field(default="success")
   ```

**Acceptance Criteria**:
- ✅ All Pydantic models match JSON format specifications
- ✅ Type hints and Field descriptions complete
- ✅ Models validate test data successfully
- ✅ Optional fields handled correctly (null values)

---

## Phase 2: Agent Implementation (Week 1-2)

### Task 2.1: Implement Code Generator Agent
**Estimated Time**: 6 hours
**Persona**: Backend Developer + AI Specialist
**Dependencies**: Task 1.2
**Location**: `back-end/src/agents/core/code_generator.py`

#### Implementation Steps:

**Step 1**: Create Agent Class
```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from datetime import datetime
from ..models.schemas import CodeGenerationRequest, CodeGenerationOutput

class CodeGeneratorAgent:
    """Agent responsible for generating educational code based on user prompts."""

    def __init__(self, model_id: str = "claude-sonnet-4-0"):
        self.agent = Agent(
            id="code-generator",
            name="Code Generator",
            model=Claude(id=model_id),
            instructions=[
                "You are an educational code generator.",
                "Generate clean, well-structured code based on user requests.",
                "Use \\n for line breaks and \\n\\n for blank lines.",
                "Focus on educational clarity and best practices.",
                "Keep code concise and well-commented."
            ],
            markdown=False,
            output_schema=CodeGenerationOutput
        )

    async def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationOutput:
        """Generate code based on user request."""
        current_date = datetime.now().isoformat()

        prompt = f"""Generate {request.language} code for the following request:

{request.prompt}

Additional context: {request.context or 'None'}

Return the code in the specified format with proper line breaks."""

        response = await self.agent.arun(prompt)

        # Ensure date is added
        if hasattr(response, 'date') and not response.date:
            response.date = current_date

        return response
```

**Step 2**: Add Error Handling & Validation
- Validate output format
- Handle model failures
- Retry logic for transient errors

**Acceptance Criteria**:
- ✅ Agent generates valid code matching 1.json format
- ✅ DateTime integration works correctly
- ✅ Error handling prevents crashes
- ✅ Output validates against CodeGenerationOutput schema

---

### Task 2.2: Implement Line-by-Line Explainer Agent
**Estimated Time**: 8 hours
**Persona**: Backend Developer + AI Specialist
**Dependencies**: Task 2.1
**Location**: `back-end/src/agents/core/line_explainer.py`

#### Implementation Steps:

**Step 1**: Create Explainer Agent
```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from ..models.schemas import CodeGenerationOutput, LineExplanationOutput, CodeLine

class LineExplainerAgent:
    """Agent that provides line-by-line educational explanations."""

    def __init__(self, model_id: str = "claude-sonnet-4-0"):
        self.agent = Agent(
            id="line-explainer",
            name="Line Explainer",
            model=Claude(id=model_id),
            instructions=[
                "You are an educational code explainer.",
                "Explain each line of code from a teaching perspective.",
                "For blank lines (\\n\\n), set line_explanation to null.",
                "Provide clear, beginner-friendly explanations.",
                "Focus on the 'why' not just the 'what'.",
                "Include an overall explanation of the entire code."
            ],
            markdown=False,
            output_schema=LineExplanationOutput
        )

    async def explain_code(self, code_output: CodeGenerationOutput) -> LineExplanationOutput:
        """Split code into lines and provide educational explanations."""

        prompt = f"""Analyze this {code_output.language} code and provide line-by-line explanations:

Code:
{code_output.code}

For each line:
1. Identify the line number
2. Extract the exact code
3. Provide an educational explanation (or null for blank lines)

Also provide an overall explanation of what the code does."""

        response = await self.agent.arun(prompt)

        # Ensure date and language are preserved
        response.date = code_output.date
        response.language = code_output.language

        return response
```

**Step 2**: Implement Line Parsing Logic
- Split code by `\n` correctly
- Handle `\n\n` (blank lines) → null explanations
- Maintain line number accuracy

**Acceptance Criteria**:
- ✅ Correctly splits code into individual lines
- ✅ Handles blank lines with null explanations
- ✅ Provides educational explanations for each code line
- ✅ Overall explanation is comprehensive
- ✅ Output validates against LineExplanationOutput schema

---

### Task 2.3: Implement Code Chunker Agent
**Estimated Time**: 8 hours
**Persona**: Backend Developer + AI Specialist
**Dependencies**: Task 2.2
**Location**: `back-end/src/agents/core/code_chunker.py`

#### Implementation Steps:

**Step 1**: Create Chunker Agent
```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from ..models.schemas import LineExplanationOutput, CodeChunkOutput, CodeChunk

class CodeChunkerAgent:
    """Agent that groups related code lines into logical chunks."""

    def __init__(self, model_id: str = "claude-sonnet-4-0"):
        self.agent = Agent(
            id="code-chunker",
            name="Code Chunker",
            model=Claude(id=model_id),
            instructions=[
                "You are a code organization specialist.",
                "Group related lines of code into logical chunks.",
                "Common groups: imports, class definitions, functions, main logic.",
                "Each chunk should represent a cohesive concept.",
                "Provide explanations for why lines are grouped together.",
                "Preserve the overall code explanation."
            ],
            markdown=False,
            output_schema=CodeChunkOutput
        )

    async def chunk_code(self, line_output: LineExplanationOutput) -> CodeChunkOutput:
        """Group code lines into logical educational chunks."""

        # Build context from line explanations
        lines_context = "\n".join([
            f"Line {line.line}: {line.line_code} - {line.line_explanation or 'blank'}"
            for line in line_output.code
        ])

        prompt = f"""Group this {line_output.language} code into logical chunks:

{lines_context}

Group related lines together (e.g., all imports, class definition, methods, etc.).
For each chunk, specify:
- first_line: starting line number
- last_line: ending line number
- line_code: the code in that chunk
- line_explanation: why these lines are grouped together

Overall explanation: {line_output.explanation}"""

        response = await self.agent.arun(prompt)

        # Preserve metadata
        response.date = line_output.date
        response.language = line_output.language

        return response
```

**Step 2**: Implement Intelligent Grouping Logic
- Detect import statements
- Group class/function definitions
- Identify main execution blocks
- Handle edge cases (single-line chunks)

**Acceptance Criteria**:
- ✅ Groups imports together
- ✅ Identifies logical code sections
- ✅ Provides explanations for groupings
- ✅ Maintains line number references
- ✅ Output validates against CodeChunkOutput schema

---

### Task 2.4: Implement Orchestrator Agent
**Estimated Time**: 10 hours
**Persona**: Backend Developer + Architect
**Dependencies**: Tasks 2.1, 2.2, 2.3
**Location**: `back-end/src/agents/core/orchestrator.py`

#### Implementation Steps:

**Step 1**: Create Orchestrator Class
```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from datetime import datetime
import uuid
import time
from .code_generator import CodeGeneratorAgent
from .line_explainer import LineExplainerAgent
from .code_chunker import CodeChunkerAgent
from ..models.schemas import (
    CodeGenerationRequest,
    OrchestratorResponse
)

class OrchestratorAgent:
    """Coordinates the multi-agent educational code generation workflow."""

    def __init__(self):
        self.code_generator = CodeGeneratorAgent()
        self.line_explainer = LineExplainerAgent()
        self.code_chunker = CodeChunkerAgent()

    async def process_request(self, request: CodeGenerationRequest) -> OrchestratorResponse:
        """
        Orchestrate the full workflow:
        1. Generate code (Agent 1)
        2. Explain line-by-line (Agent 2)
        3. Chunk code sections (Agent 3)
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Step 1: Generate code
            code_output = await self.code_generator.generate_code(request)

            # Step 2: Explain line-by-line
            line_output = await self.line_explainer.explain_code(code_output)

            # Step 3: Chunk code
            chunk_output = await self.code_chunker.chunk_code(line_output)

            processing_time = time.time() - start_time

            return OrchestratorResponse(
                request_id=request_id,
                generated_code=code_output,
                line_explanations=line_output,
                chunked_code=chunk_output,
                processing_time_seconds=processing_time,
                status="success"
            )

        except Exception as e:
            processing_time = time.time() - start_time
            raise Exception(f"Orchestration failed: {str(e)}")
```

**Step 2**: Add Monitoring & Logging
- Log each agent transition
- Track processing time per agent
- Handle partial failures gracefully

**Acceptance Criteria**:
- ✅ Successfully coordinates all 3 agents
- ✅ Handles errors at each stage
- ✅ Returns complete OrchestratorResponse
- ✅ Processing time tracked accurately
- ✅ Request ID generated for tracing

---

## Phase 3: FastAPI Server Integration (Week 2)

### Task 3.1: Setup AgentOS with FastAPI
**Estimated Time**: 6 hours
**Persona**: Backend Developer + DevOps
**Dependencies**: Task 2.4
**Location**: `back-end/src/agents/server.py`

#### Implementation Steps:

**Step 1**: Create FastAPI Application with AgentOS
```python
from fastapi import FastAPI, HTTPException
from agno.os import AgentOS
from agno.db.postgres import PostgresDb
from datetime import datetime
from .core.orchestrator import OrchestratorAgent
from .models.schemas import CodeGenerationRequest, OrchestratorResponse

# Initialize database (for agent session tracking)
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# Custom FastAPI app
app = FastAPI(
    title="Educational Multi-Agent System",
    version="1.0.0",
    description="Generate code and educational explanations using multi-agent AI"
)

# Initialize orchestrator
orchestrator = OrchestratorAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "educational-multi-agent-system"
    }

@app.post("/api/v1/generate", response_model=OrchestratorResponse)
async def generate_educational_code(request: CodeGenerationRequest):
    """
    Main endpoint for educational code generation.

    Workflow:
    1. User submits code request
    2. Code Generator creates code (1.json format)
    3. Line Explainer breaks down line-by-line (2.json format)
    4. Code Chunker groups sections (3.json format)
    5. Returns complete educational package
    """
    try:
        response = await orchestrator.process_request(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code generation failed: {str(e)}"
        )

# Setup AgentOS (for UI and additional features)
agent_os = AgentOS(
    description="Educational Multi-Agent Code Generation System",
    agents=[],  # We're using custom orchestrator
    base_app=app
)

# Get the combined app
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="agents.server:app", reload=True, port=8000)
```

**Step 2**: Add CORS Middleware
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Step 3**: Add Request Validation Middleware
- Validate request payload
- Rate limiting
- Request logging

**Acceptance Criteria**:
- ✅ FastAPI server starts without errors
- ✅ AgentOS integrated successfully
- ✅ `/health` endpoint returns 200
- ✅ `/api/v1/generate` endpoint accepts requests
- ✅ CORS configured correctly
- ✅ API docs available at `/docs`

---

## Phase 4: Testing Implementation (Week 2-3)

### Task 4.1: Unit Tests for Individual Agents
**Estimated Time**: 12 hours
**Persona**: QA Engineer + Backend Developer
**Dependencies**: Tasks 2.1, 2.2, 2.3
**Location**: `back-end/src/tests/agents/`

#### Test Structure:
```
back-end/src/tests/agents/
├── __init__.py
├── test_code_generator.py
├── test_line_explainer.py
├── test_code_chunker.py
├── test_orchestrator.py
├── test_schemas.py
└── fixtures/
    ├── __init__.py
    ├── sample_requests.py
    └── expected_outputs.py
```

#### Test Cases:

**test_code_generator.py**:
```python
import pytest
from back_end.src.agents.core.code_generator import CodeGeneratorAgent
from back_end.src.agents.models.schemas import CodeGenerationRequest

@pytest.mark.asyncio
async def test_code_generator_basic():
    """Test basic code generation."""
    agent = CodeGeneratorAgent()
    request = CodeGenerationRequest(
        prompt="Create a function to calculate factorial",
        language="python"
    )

    result = await agent.generate_code(request)

    assert result.language == "python"
    assert result.code is not None
    assert len(result.code) > 0
    assert result.date is not None
    assert "def" in result.code or "function" in result.code

@pytest.mark.asyncio
async def test_code_generator_with_context():
    """Test code generation with additional context."""
    agent = CodeGeneratorAgent()
    request = CodeGenerationRequest(
        prompt="Create a REST API endpoint",
        language="python",
        context="Use FastAPI framework"
    )

    result = await agent.generate_code(request)

    assert "fastapi" in result.code.lower() or "FastAPI" in result.code
```

**test_line_explainer.py**:
```python
import pytest
from back_end.src.agents.core.line_explainer import LineExplainerAgent
from back_end.src.agents.models.schemas import CodeGenerationOutput

@pytest.mark.asyncio
async def test_line_explainer_basic():
    """Test line-by-line explanation."""
    agent = LineExplainerAgent()
    code_output = CodeGenerationOutput(
        date="2025-10-31T12:00:00",
        language="python",
        code="def add(a, b):\n    return a + b"
    )

    result = await agent.explain_code(code_output)

    assert len(result.code) >= 2  # At least 2 lines
    assert all(line.line > 0 for line in result.code)
    assert result.explanation is not None

@pytest.mark.asyncio
async def test_line_explainer_blank_lines():
    """Test handling of blank lines."""
    agent = LineExplainerAgent()
    code_output = CodeGenerationOutput(
        date="2025-10-31T12:00:00",
        language="python",
        code="import os\n\ndef main():\n    pass"
    )

    result = await agent.explain_code(code_output)

    # Check that blank line has null explanation
    blank_lines = [line for line in result.code if not line.line_code.strip()]
    assert all(line.line_explanation is None for line in blank_lines)
```

**test_code_chunker.py**:
```python
import pytest
from back_end.src.agents.core.code_chunker import CodeChunkerAgent
from back_end.src.agents.models.schemas import LineExplanationOutput, CodeLine

@pytest.mark.asyncio
async def test_code_chunker_groups_imports():
    """Test that imports are grouped together."""
    agent = CodeChunkerAgent()
    line_output = LineExplanationOutput(
        date="2025-10-31T12:00:00",
        language="python",
        code=[
            CodeLine(line=1, line_code="import os", line_explanation="Import OS module"),
            CodeLine(line=2, line_code="import sys", line_explanation="Import sys module"),
            CodeLine(line=3, line_code="", line_explanation=None),
            CodeLine(line=4, line_code="def main():", line_explanation="Main function")
        ],
        explanation="Simple Python script"
    )

    result = await agent.chunk_code(line_output)

    # Should have at least 2 chunks (imports and function)
    assert len(result.code) >= 2

    # First chunk should contain imports
    first_chunk = result.code[0]
    assert "import" in first_chunk.line_code.lower()
```

**test_orchestrator.py**:
```python
import pytest
from back_end.src.agents.core.orchestrator import OrchestratorAgent
from back_end.src.agents.models.schemas import CodeGenerationRequest

@pytest.mark.asyncio
async def test_orchestrator_full_workflow():
    """Test complete orchestration workflow."""
    orchestrator = OrchestratorAgent()
    request = CodeGenerationRequest(
        prompt="Create a simple Hello World function",
        language="python"
    )

    result = await orchestrator.process_request(request)

    assert result.status == "success"
    assert result.request_id is not None
    assert result.generated_code is not None
    assert result.line_explanations is not None
    assert result.chunked_code is not None
    assert result.processing_time_seconds > 0

@pytest.mark.asyncio
async def test_orchestrator_error_handling():
    """Test orchestrator handles errors gracefully."""
    orchestrator = OrchestratorAgent()
    request = CodeGenerationRequest(
        prompt="",  # Empty prompt should cause error
        language="python"
    )

    with pytest.raises(Exception):
        await orchestrator.process_request(request)
```

**test_schemas.py**:
```python
import pytest
from pydantic import ValidationError
from back_end.src.agents.models.schemas import (
    CodeGenerationRequest,
    CodeGenerationOutput,
    LineExplanationOutput,
    CodeLine,
    CodeChunkOutput,
    CodeChunk
)

def test_code_generation_request_validation():
    """Test request model validation."""
    # Valid request
    request = CodeGenerationRequest(
        prompt="Create a function",
        language="python"
    )
    assert request.prompt == "Create a function"

    # Invalid request (missing required field)
    with pytest.raises(ValidationError):
        CodeGenerationRequest(language="python")

def test_code_line_blank_explanation():
    """Test that blank lines can have null explanations."""
    line = CodeLine(
        line=1,
        line_code="",
        line_explanation=None
    )
    assert line.line_explanation is None

def test_code_chunk_validation():
    """Test chunk validation."""
    chunk = CodeChunk(
        first_line=1,
        last_line=3,
        line_code="import os\nimport sys",
        line_explanation="Import statements"
    )
    assert chunk.first_line < chunk.last_line
```

**Acceptance Criteria**:
- ✅ All unit tests pass
- ✅ Code coverage ≥80% for agent modules
- ✅ Edge cases handled (blank lines, errors, etc.)
- ✅ Pydantic validation tested
- ✅ DateTime handling verified

---

### Task 4.2: Integration Tests for FastAPI Server
**Estimated Time**: 8 hours
**Persona**: QA Engineer + Backend Developer
**Dependencies**: Task 3.1
**Location**: `back-end/src/tests/integration/`

#### Test Structure:
```
back-end/src/tests/integration/
├── __init__.py
├── test_api_endpoints.py
├── test_full_workflow.py
└── conftest.py  # Pytest fixtures
```

#### Test Cases:

**conftest.py**:
```python
import pytest
from fastapi.testclient import TestClient
from back_end.src.agents.server import app

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

@pytest.fixture
def sample_request():
    """Sample code generation request."""
    return {
        "prompt": "Create a function to reverse a string",
        "language": "python",
        "context": "Use built-in methods"
    }
```

**test_api_endpoints.py**:
```python
def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_generate_endpoint_success(client, sample_request):
    """Test successful code generation."""
    response = client.post("/api/v1/generate", json=sample_request)
    assert response.status_code == 200
    data = response.json()

    assert "request_id" in data
    assert "generated_code" in data
    assert "line_explanations" in data
    assert "chunked_code" in data
    assert data["status"] == "success"

def test_generate_endpoint_validation(client):
    """Test request validation."""
    # Missing required field
    response = client.post("/api/v1/generate", json={"language": "python"})
    assert response.status_code == 422  # Validation error

def test_generate_endpoint_empty_prompt(client):
    """Test handling of empty prompt."""
    response = client.post("/api/v1/generate", json={
        "prompt": "",
        "language": "python"
    })
    assert response.status_code in [400, 500]
```

**test_full_workflow.py**:
```python
import pytest

def test_complete_python_workflow(client):
    """Test complete workflow for Python code."""
    request = {
        "prompt": "Create a class for a simple calculator with add and subtract methods",
        "language": "python"
    }

    response = client.post("/api/v1/generate", json=request)
    assert response.status_code == 200

    data = response.json()

    # Validate generated code (1.json format)
    assert data["generated_code"]["language"] == "python"
    assert "class" in data["generated_code"]["code"].lower()
    assert data["generated_code"]["date"] is not None

    # Validate line explanations (2.json format)
    assert len(data["line_explanations"]["code"]) > 0
    for line in data["line_explanations"]["code"]:
        assert "line" in line
        assert "line_code" in line

    # Validate chunked code (3.json format)
    assert len(data["chunked_code"]["code"]) > 0
    for chunk in data["chunked_code"]["code"]:
        assert "first_line" in chunk
        assert "last_line" in chunk
        assert chunk["first_line"] <= chunk["last_line"]

def test_complete_javascript_workflow(client):
    """Test complete workflow for JavaScript code."""
    request = {
        "prompt": "Create an async function to fetch data from an API",
        "language": "javascript"
    }

    response = client.post("/api/v1/generate", json=request)
    assert response.status_code == 200

    data = response.json()
    assert data["generated_code"]["language"] == "javascript"
    assert "async" in data["generated_code"]["code"].lower()

@pytest.mark.slow
def test_performance_benchmark(client, sample_request):
    """Test response time is acceptable."""
    import time

    start = time.time()
    response = client.post("/api/v1/generate", json=sample_request)
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 30.0  # Should complete within 30 seconds
```

**Acceptance Criteria**:
- ✅ All API endpoints tested
- ✅ Complete workflow validated
- ✅ Request/response validation working
- ✅ Error handling verified
- ✅ Performance benchmarks met

---

## Phase 5: Documentation & Deployment (Week 3)

### Task 5.1: API Documentation
**Estimated Time**: 4 hours
**Persona**: Technical Writer
**Dependencies**: All previous tasks
**Location**: `back-end/docs/agents_plan/api_documentation.md`

#### Documentation Sections:
1. **API Overview**
2. **Authentication** (if applicable)
3. **Endpoints Reference**
4. **Request/Response Examples**
5. **Error Codes**
6. **Rate Limits**

---

### Task 5.2: Developer Setup Guide
**Estimated Time**: 3 hours
**Persona**: Technical Writer
**Dependencies**: All previous tasks
**Location**: `back-end/docs/agents_plan/setup_guide.md`

#### Guide Sections:
1. **Prerequisites**
2. **Installation Steps**
3. **Environment Configuration**
4. **Running the Server**
5. **Testing the System**
6. **Troubleshooting**

---

### Task 5.3: Deployment Configuration
**Estimated Time**: 6 hours
**Persona**: DevOps Engineer
**Dependencies**: Task 3.1
**Location**: `back-end/scripts/deploy_agents.sh`

#### Deployment Steps:
1. **Docker Configuration**
   - Create Dockerfile
   - Docker Compose setup
   - Environment variables

2. **Production Server Setup**
   - Gunicorn/Uvicorn configuration
   - Nginx reverse proxy
   - SSL certificates

3. **Monitoring & Logging**
   - Application logs
   - Error tracking
   - Performance monitoring

---

## File Structure Summary

```
back-end/
├── docs/
│   └── agents_plan/
│       ├── implementation_workflow.md     (this file)
│       ├── api_documentation.md
│       └── setup_guide.md
│
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── server.py                      # FastAPI + AgentOS server
│   │   │
│   │   ├── core/                          # Agent implementations
│   │   │   ├── __init__.py
│   │   │   ├── code_generator.py          # Agent 1: Code generation
│   │   │   ├── line_explainer.py          # Agent 2: Line-by-line explanation
│   │   │   ├── code_chunker.py            # Agent 3: Code chunking
│   │   │   └── orchestrator.py            # Orchestrator agent
│   │   │
│   │   └── models/                        # Pydantic schemas
│   │       ├── __init__.py
│   │       ├── schemas.py                 # JSON format models
│   │       └── agent_config.py            # Agent configuration
│   │
│   └── tests/
│       └── agents/                        # Test suite
│           ├── __init__.py
│           ├── test_code_generator.py
│           ├── test_line_explainer.py
│           ├── test_code_chunker.py
│           ├── test_orchestrator.py
│           ├── test_schemas.py
│           │
│           ├── integration/
│           │   ├── __init__.py
│           │   ├── test_api_endpoints.py
│           │   └── test_full_workflow.py
│           │
│           └── fixtures/
│               ├── __init__.py
│               ├── sample_requests.py
│               └── expected_outputs.py
│
└── scripts/
    └── deploy_agents.sh                   # Deployment script
```

---

## Dependencies & Prerequisites

### Package Manager
This project uses **uv** for fast, reliable Python package management.

**Install uv**:
```bash
# Using the install script (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv

# Verify installation
uv --version
```

### Required Libraries:
```toml
[project.dependencies]
agno = "^0.2.0"
pydantic = "^2.0.0"
fastapi = "^0.100.0"
uvicorn = "^0.23.0"
sqlalchemy = "^2.0.0"
psycopg = "^3.1.0"
pgvector = "^0.2.0"
python-multipart = "^0.0.6"
anthropic = "^0.25.0"
openai = "^1.0.0"
```

**Install with uv**:
```bash
uv add agno pydantic fastapi uvicorn sqlalchemy psycopg pgvector python-multipart anthropic openai
```

### Development Dependencies:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.0.280",
    "mypy>=1.4.0"
]
```

**Install dev dependencies with uv**:
```bash
uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy
```

### External Services:
- PostgreSQL database (for agent session tracking)
- Anthropic API key (for Claude models)
- OpenAI API key (optional, for alternative models)

---

## Risk Assessment & Mitigation

### Technical Risks:

1. **Agent Response Quality**
   - **Risk**: AI agents may generate incorrect or poorly structured code
   - **Mitigation**:
     - Implement output validation
     - Add retry logic with improved prompts
     - Human review for critical applications

2. **Performance Bottlenecks**
   - **Risk**: Sequential agent processing may be slow
   - **Mitigation**:
     - Implement caching for common requests
     - Consider parallel processing where possible
     - Set reasonable timeout limits

3. **API Rate Limits**
   - **Risk**: External AI API rate limits may cause failures
   - **Mitigation**:
     - Implement exponential backoff
     - Queue requests during high load
     - Multiple API key rotation

4. **Type Safety**
   - **Risk**: JSON schema mismatches between agents
   - **Mitigation**:
     - Strict Pydantic validation
     - Comprehensive unit tests
     - Schema version management

---

## Success Metrics

### Quality Metrics:
- ✅ **Code Coverage**: ≥80% for all agent modules
- ✅ **Test Pass Rate**: 100% for unit and integration tests
- ✅ **Type Safety**: Zero Pydantic validation errors in production
- ✅ **API Response Time**: <30 seconds for complete workflow

### Functional Metrics:
- ✅ **Code Generation Accuracy**: 90%+ of generated code is syntactically correct
- ✅ **Explanation Quality**: 85%+ of explanations are educationally valuable
- ✅ **Chunking Accuracy**: 90%+ of chunks are logically grouped

### Operational Metrics:
- ✅ **Uptime**: 99.5%
- ✅ **Error Rate**: <1% of requests fail
- ✅ **DateTime Accuracy**: 100% of timestamps are correctly formatted

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 1: Foundation | Week 1 | Pydantic models, dependencies |
| Phase 2: Agents | Week 1-2 | All 4 agents implemented |
| Phase 3: Server | Week 2 | FastAPI + AgentOS integration |
| Phase 4: Testing | Week 2-3 | Complete test suite |
| Phase 5: Documentation | Week 3 | Docs and deployment |

**Total Estimated Time**: 3 weeks (120 hours)

---

## Next Steps

1. **Review this workflow** with stakeholders
2. **Approve technology stack** (Agno, FastAPI, Pydantic)
3. **Set up development environment**
4. **Begin Phase 1 implementation**
5. **Schedule weekly progress reviews**

---

## References

- [Agno Documentation](https://docs.agno.com)
- [Agno FastAPI Integration](https://docs.agno.com/agent-os/customize/custom-fastapi)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- Project File Structure: `back-end/docs/file_structure.md`
- JSON Format Specifications: `back-end/docs/ai_agent_json_format/`
