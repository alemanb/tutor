# Educational Multi-Agent System

> Generate educational code with comprehensive line-by-line explanations using AI

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204.0-purple.svg)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI-powered educational code generation** with three specialized agents working together to create clean code, explain it line-by-line, and organize it into logical sections.

---

## ✨ Features

- 🤖 **Multi-Agent System** - Three specialized AI agents working in coordination
- 📚 **Educational Focus** - Line-by-line explanations perfect for learning
- 🎯 **Code Organization** - Automatic chunking into logical sections
- 🚀 **REST API** - Easy integration with any application
- 📖 **Interactive Docs** - Swagger UI and ReDoc included
- ⚡ **Fast & Reliable** - Built with FastAPI and Claude Sonnet 4.0
- 🔧 **Type-Safe** - Full Pydantic validation
- ✅ **Well-Tested** - Comprehensive test suite with pytest

---

## 🎬 Quick Start

### Prerequisites

- Python 3.12+
- uv package manager
- Anthropic API key

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/tutor.git
cd tutor/back-end

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Run the Server

```bash
# Start development server
python -m src.agents.server

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Make Your First Request

```bash
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a function to check if a number is prime",
    "language": "python"
  }'
```

---

## 📚 How It Works

The system uses **three specialized AI agents** that work sequentially:

```
┌─────────────────┐
│  Your Prompt    │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  1. Code Generator  │  Generates clean, educational code
│  (Agent 1)          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Line Explainer  │  Explains each line for learning
│  (Agent 2)          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Code Chunker    │  Groups code into logical sections
│  (Agent 3)          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Complete Response  │  Code + Explanations + Chunks
└─────────────────────┘
```

### Example Output

**Input**:
```json
{
  "prompt": "Create a function to add two numbers",
  "language": "python"
}
```

**Output** (simplified):
```json
{
  "generated_code": {
    "code": "def add(a, b):\n    return a + b"
  },
  "line_explanations": {
    "code": [
      {
        "line": 1,
        "line_code": "def add(a, b):",
        "line_explanation": "Define a function that takes two parameters"
      },
      {
        "line": 2,
        "line_code": "    return a + b",
        "line_explanation": "Return the sum of the two numbers"
      }
    ]
  },
  "chunked_code": {
    "code": [
      {
        "first_line": 1,
        "last_line": 2,
        "line_explanation": "Complete function definition"
      }
    ]
  }
}
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/health/ready` | Readiness probe |
| GET | `/api/v1/agents/info` | Agent information |
| POST | `/api/v1/generate` | Generate educational code |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc documentation |

---

## 📖 Documentation

- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Developer Setup](docs/DEVELOPER_SETUP.md)** - Development environment setup
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[Phase Documentation](docs/agents_plan/phases/)** - Implementation phases

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/agents --cov-report=html

# Run specific tests
pytest src/tests/integration/
pytest -m "not slow"  # Skip slow tests
```

**Current Coverage**: 44% (baseline established)

---

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check health
curl http://localhost:8000/health

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

---

## 🏗️ Architecture

### Project Structure

```
back-end/
├── src/
│   ├── agents/
│   │   ├── models/          # Pydantic schemas
│   │   ├── core/            # Agent implementations
│   │   │   ├── code_generator.py
│   │   │   ├── line_explainer.py
│   │   │   ├── code_chunker.py
│   │   │   └── orchestrator.py
│   │   └── server.py        # FastAPI application
│   └── tests/               # Test suite
├── docs/                    # Documentation
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
└── pytest.ini               # Test configuration
```

### Tech Stack

- **Framework**: [Agno](https://docs.agno.com) - Multi-agent orchestration
- **API**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **AI Model**: [Claude Sonnet 4.0](https://anthropic.com) - Anthropic's latest model
- **Validation**: [Pydantic](https://docs.pydantic.dev/) - Data validation
- **Testing**: [pytest](https://docs.pytest.org/) - Test framework
- **Package Manager**: [uv](https://github.com/astral-sh/uv) - Fast Python package manager

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | Anthropic API key |
| `HOST` | No | `0.0.0.0` | Server host |
| `PORT` | No | `8000` | Server port |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `DATABASE_URL` | No | - | PostgreSQL URL (optional) |

See `.env.example` for complete configuration options.

---

## 📊 Performance

- **Average Response Time**: 45-80 seconds
- **Throughput**: Designed for educational use (not high-throughput)
- **Concurrency**: Single request processing (sequential agents)

**Note**: Processing time depends on code complexity and involves three AI model calls.

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Development Phases

This project was implemented in 5 phases:

- ✅ **Phase 1**: Project Foundation & Pydantic Models
- ✅ **Phase 2**: Agent Implementation (4 agents)
- ✅ **Phase 3**: FastAPI Server Integration
- ✅ **Phase 4**: Testing Infrastructure
- ✅ **Phase 5**: Documentation & Deployment

See [docs/agents_plan/phases/](docs/agents_plan/phases/) for detailed phase documentation.

---

## 🔒 Security

- **API Keys**: Never commit `.env` to version control
- **Input Validation**: All inputs validated with Pydantic
- **CORS**: Configurable for production
- **Rate Limiting**: Recommended for production (not included)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for Claude API
- [Agno](https://docs.agno.com) for multi-agent framework
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [uv](https://github.com/astral-sh/uv) for fast package management

---

## 📞 Support

- **Documentation**: [/docs](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/tutor/issues)
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🗺️ Roadmap

- [ ] Add support for more programming languages
- [ ] Implement caching for common requests
- [ ] Add rate limiting
- [ ] Parallel agent processing for better performance
- [ ] Multi-language support for explanations
- [ ] Code quality analysis
- [ ] Integration with GitHub

---

**Made with ❤️ using Claude Sonnet 4.0**
