# Educational Multi-Agent System

Production-ready FastAPI system for generating educational code with AI-powered explanations.

## 🎯 Overview

This system uses three specialized AI agents working together to generate educational code with comprehensive explanations:

1. **Code Generator Agent** - Generates code from natural language prompts
2. **Line Explainer Agent** - Provides line-by-line educational explanations
3. **Code Chunker Agent** - Groups code into logical sections

All coordinated by an **Orchestrator Agent** that manages the complete workflow.

**Built With**: FastAPI, Agno Framework, Claude AI, Pydantic

## ✨ Features

- 🤖 Multi-agent AI system with specialized roles
- 📚 Educational line-by-line code explanations
- 🔧 Support for multiple programming languages
- 📊 Structured JSON output (3 formats: code, lines, chunks)
- ⚡ Fast async processing with uvicorn
- 🧪 95 comprehensive tests (100% pass rate)
- 📖 Interactive API documentation (Swagger/ReDoc)
- 🐳 Docker-ready deployment
- 🔒 Type-safe with Pydantic validation

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- `uv` package manager
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

```bash
# Clone repository
git clone https://github.com/your-repo/tutor.git
cd tutor/back-end

# Install dependencies
uv sync

# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Running the Server

```bash
# Development mode (with auto-reload)
uv run uvicorn src.agents.server:app --reload --host 0.0.0.0 --port 8000

# Production mode
uv run uvicorn src.agents.server:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will start at: **http://localhost:8000**

## 📡 API Endpoints

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Generate Code**: POST http://localhost:8000/api/v1/generate
- **System Status**: http://localhost:8000/api/v1/status

### Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to calculate factorial",
    "language": "python"
  }'
```

### Example Response

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "code_output": {
    "date": "2025-11-02T10:30:00",
    "language": "python",
    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)"
  },
  "line_output": {
    "code": [
      {
        "line": 1,
        "line_code": "def factorial(n):",
        "line_explanation": "Define factorial function..."
      }
    ],
    "explanation": "Overall code explanation..."
  },
  "chunk_output": {
    "code": [
      {
        "first_line": 1,
        "last_line": 4,
        "line_code": "def factorial(n):...",
        "line_explanation": "Complete function with recursion"
      }
    ],
    "explanation": "Code structure explanation..."
  },
  "processing_time": 12.5,
  "timestamp": "2025-11-02T10:30:02.500000"
}
```

## 🧪 Testing

```bash
# Run all tests (fast, no API key needed)
uv run pytest -m "not requires_api_key"

# Run full test suite (requires API key)
export ANTHROPIC_API_KEY="your-key"
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

**Test Suite**: 95 tests with 100% pass rate
- Unit tests for all 4 agents
- Integration tests for FastAPI server
- Comprehensive fixtures and edge cases

## 📚 Documentation

### User Documentation
- **[API Documentation](back-end/docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Setup Guide](back-end/docs/SETUP_GUIDE.md)** - Development environment setup
- **[Deployment Guide](back-end/docs/DEPLOYMENT_GUIDE.md)** - Production deployment

### Developer Documentation
- **[Test Documentation](back-end/src/tests/README.md)** - Testing guide
- **[File Structure](back-end/docs/file_structure.md)** - Project organization
- **[Implementation Workflow](back-end/docs/agents_plan/implementation_workflow.md)** - Complete workflow

### Phase Documentation
- ✅ [Phase 1: Foundation](back-end/docs/agents_plan/PHASE1_COMPLETE.md) - Models & dependencies
- ✅ [Phase 2: Agents](back-end/docs/agents_plan/PHASE2_COMPLETE.md) - 4 agent implementations
- ✅ [Phase 3: Server](back-end/docs/agents_plan/PHASE3_COMPLETE.md) - FastAPI integration
- ✅ [Phase 4: Testing](back-end/docs/agents_plan/PHASE4_COMPLETE.md) - 95 comprehensive tests
- ✅ [Phase 5: Documentation](back-end/docs/agents_plan/PHASE5_COMPLETE.md) - Complete docs & deployment

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.120+
- **AI Framework**: Agno 2.2+
- **AI Model**: Claude Sonnet 4.0
- **Validation**: Pydantic 2.12+
- **Server**: Uvicorn (ASGI)
- **Package Manager**: uv
- **Testing**: pytest + pytest-asyncio
- **Python**: 3.12+

## 📊 Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Pydantic models & dependencies |
| Phase 2 | ✅ Complete | 4 AI agents implemented |
| Phase 3 | ✅ Complete | FastAPI server integration |
| Phase 4 | ✅ Complete | 95 comprehensive tests |
| Phase 5 | ✅ Complete | Documentation & deployment |

**Ready for Production** 🚀

## 🏗️ Project Structure

```
tutor/
├── back-end/                 # FastAPI server & agents
│   ├── src/
│   │   ├── agents/
│   │   │   ├── core/         # Agent implementations
│   │   │   ├── models/       # Pydantic schemas
│   │   │   └── server.py     # FastAPI server
│   │   └── tests/            # 95 comprehensive tests
│   ├── docs/                 # Documentation
│   └── pyproject.toml        # Dependencies
└── front-end/                # Frontend (future)
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Run tests (`uv run pytest`)
4. Submit a pull request

## 📝 License

[Add your license here]

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/tutor/issues)
- **Documentation**: See `docs/` folder
- **Email**: support@example.com

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Uses [Agno Framework](https://docs.agno.com/)

---

**Made with ❤️ for education**
