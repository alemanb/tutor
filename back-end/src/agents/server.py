"""FastAPI Server with AgentOS Integration for Educational Multi-Agent System.

This server provides REST API endpoints for the multi-agent code generation system.
It integrates with AgentOS for enhanced UI and monitoring capabilities.
"""

import os
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agno.os import AgentOS

from .core.orchestrator import OrchestratorAgent
from .models.schemas import CodeGenerationRequest, OrchestratorResponse

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.getenv("ANTHROPIC_API_KEY"):
    raise EnvironmentError(
        "ANTHROPIC_API_KEY not found in environment. "
        "Please set it in your .env file or environment variables."
    )

# Initialize the orchestrator
orchestrator = OrchestratorAgent()

# Create FastAPI application
app = FastAPI(
    title="Educational Multi-Agent System",
    version="1.0.0",
    description="""
    Generate code and educational explanations using a multi-agent AI system.

    This API coordinates three specialized agents:
    1. Code Generator - Creates educational code based on prompts
    2. Line Explainer - Provides line-by-line explanations
    3. Code Chunker - Groups code into logical sections

    The system uses Claude Sonnet 4.0 and outputs structured JSON matching
    the educational format specifications.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Middleware
# ============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = datetime.now()

    # Process the request
    response = await call_next(request)

    # Calculate processing time
    process_time = (datetime.now() - start_time).total_seconds()

    # Log request details
    print(f"[{start_time.isoformat()}] {request.method} {request.url.path} - {response.status_code} ({process_time:.2f}s)")

    # Add custom header with processing time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    print(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "path": str(request.url.path),
            "timestamp": datetime.now().isoformat(),
        }
    )


# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring and load balancers.

    Returns:
        Dictionary with service status, timestamp, and system information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "educational-multi-agent-system",
        "version": "1.0.0",
        "agents": {
            "orchestrator": orchestrator.model_id,
            "total_agents": 3,
        },
        "api_key_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
    }


@app.get("/health/ready")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes and container orchestration.

    Returns:
        Dictionary with readiness status and checks
    """
    checks = {
        "api_key": bool(os.getenv("ANTHROPIC_API_KEY")),
        "orchestrator": orchestrator is not None,
    }

    is_ready = all(checks.values())

    return {
        "ready": is_ready,
        "timestamp": datetime.now().isoformat(),
        "checks": checks,
    }


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information.

    Returns:
        Dictionary with API welcome message and documentation links
    """
    return {
        "message": "Educational Multi-Agent System API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
        },
        "endpoints": {
            "health": "/health",
            "generate_code": "/api/v1/generate",
            "agent_info": "/api/v1/agents/info",
        },
        "timestamp": datetime.now().isoformat(),
    }


# ============================================================================
# Agent Information Endpoints
# ============================================================================

@app.get("/api/v1/agents/info")
async def get_agent_info() -> Dict[str, Any]:
    """Get information about the multi-agent system.

    Returns:
        Dictionary with agent configuration and capabilities
    """
    return orchestrator.get_agent_info()


# ============================================================================
# Code Generation Endpoints
# ============================================================================

@app.post("/api/v1/generate", response_model=OrchestratorResponse)
async def generate_educational_code(request: CodeGenerationRequest) -> OrchestratorResponse:
    """Generate educational code with explanations and chunking.

    This endpoint coordinates all three agents to:
    1. Generate clean, educational code based on the prompt
    2. Explain the code line-by-line with educational focus
    3. Group code lines into logical chunks

    Args:
        request: CodeGenerationRequest with prompt, language, and optional context

    Returns:
        OrchestratorResponse with complete educational package:
        - generated_code: The generated code (1.json format)
        - line_explanations: Line-by-line breakdown (2.json format)
        - chunked_code: Logical code sections (3.json format)
        - processing_time_seconds: Total processing time
        - request_id: Unique identifier for this request

    Raises:
        HTTPException: If code generation fails or validation errors occur

    Example:
        ```python
        request = {
            "prompt": "Create a function to calculate factorial",
            "language": "python",
            "context": "Use recursion"
        }
        ```
    """
    try:
        # Validate request
        if not request.prompt or len(request.prompt.strip()) == 0: # type: ignore
            raise HTTPException(
                status_code=400,
                detail="Prompt cannot be empty"
            )

        # Process request using orchestrator (async)
        response = await orchestrator.aprocess_request(request)

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Log error and return 500
        error_message = f"Code generation failed: {str(e)}"
        print(f"❌ {error_message}")

        raise HTTPException(
            status_code=500,
            detail=error_message
        )


# ============================================================================
# AgentOS Integration (Optional)
# ============================================================================

# Note: AgentOS is available but not required since we use a custom orchestrator
# To enable AgentOS UI, you would need to create AgentOS-compatible agent wrappers
# For now, we're using the standard FastAPI app with our custom orchestrator


# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("🚀 Starting Educational Multi-Agent System Server")
    print("=" * 80)
    print(f"API Documentation: http://localhost:8000/docs")
    print(f"ReDoc: http://localhost:8000/redoc")
    print(f"Health Check: http://localhost:8000/health")
    print(f"Generate Endpoint: http://localhost:8000/api/v1/generate")
    print("=" * 80)

    # Run the server
    uvicorn.run(
        "src.agents.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
