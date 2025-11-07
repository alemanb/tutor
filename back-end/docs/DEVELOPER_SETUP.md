# Developer Setup Guide

Complete guide for setting up the Educational Multi-Agent System development environment.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Server](#running-the-server)
- [Running Tests](#running-tests)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose |
|----------|----------------|---------|
| **Python** | 3.11+ | Runtime environment |
| **uv** | Latest | Package manager |
| **Git** | 2.0+ | Version control |

### Optional Software

| Software | Purpose |
|----------|---------|
| **Docker** | Containerization |
| **PostgreSQL** | Database (for AgentOS features) |
| **VS Code** | Recommended IDE |

### System Requirements

- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB for dependencies and cache

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/tutor.git
cd tutor/back-end
```

### Step 2: Install uv Package Manager

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip**:
```bash
pip install uv
```

**Verify Installation**:
```bash
uv --version
```

### Step 3: Install Dependencies

```bash
# Install all dependencies
uv sync

# Or add dependencies manually
uv add agno pydantic fastapi uvicorn sqlalchemy psycopg pgvector python-multipart anthropic openai python-dotenv

# Install development dependencies
uv add --dev pytest pytest-asyncio pytest-cov black ruff mypy
```

This will:
- Create a virtual environment in `.venv/`
- Install all project dependencies
- Generate `uv.lock` file

### Step 4: Verify Installation

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Test imports
python -c "import agno, pydantic, fastapi; print('✅ All dependencies installed')"
```

---

## Environment Configuration

### Step 1: Create .env File

```bash
cp .env.example .env  # If example exists
# or create manually
touch .env
```

### Step 2: Configure Environment Variables

Edit `.env` file:

```bash
# Required: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Optional: Development Settings
DEBUG=true
LOG_LEVEL=INFO

# Optional: Database (for AgentOS features)
DATABASE_URL=postgresql+psycopg://ai:ai@localhost:5532/ai

# Optional: Server Settings
HOST=0.0.0.0
PORT=8000
```

### Step 3: Get Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy key to `.env` file

**Security**: Never commit `.env` to version control!

### Step 4: Verify Environment

```bash
# Load environment variables
source .env  # macOS/Linux
# or
set -a; source .env; set +a  # Explicit export

# Check API key is set
echo $ANTHROPIC_API_KEY
```

---

## Running the Server

### Development Server (with Hot Reload)

```bash
# Method 1: Using Python module
python -m src.agents.server

# Method 2: Using uvicorn directly
uvicorn src.agents.server:app --reload --host 0.0.0.0 --port 8000

# Method 3: Using uv run
uv run uvicorn src.agents.server:app --reload
```

**Server Output**:
```
================================================================================
🚀 Starting Educational Multi-Agent System Server
================================================================================
API Documentation: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
Health Check: http://localhost:8000/health
Generate Endpoint: http://localhost:8000/api/v1/generate
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access Points

| Resource | URL |
|----------|-----|
| **API Root** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |
| **OpenAPI JSON** | http://localhost:8000/openapi.json |

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Generate code
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a hello world function", "language": "python"}'
```

---

## Running Tests

### Run All Tests

```bash
# Using pytest directly
pytest

# Using uv
uv run pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=src/agents --cov-report=html
```

### Run Specific Tests

```bash
# Specific test file
pytest src/tests/integration/test_api_endpoints.py

# Specific test function
pytest src/tests/integration/test_api_endpoints.py::test_health_endpoint

# By marker
pytest -m integration  # Only integration tests
pytest -m unit         # Only unit tests
pytest -m "not slow"   # Skip slow tests
```

### Coverage Report

```bash
# Generate coverage report
pytest --cov=src/agents --cov-report=html

# View in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Output Example

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/user/back-end
configfile: pytest.ini
plugins: cov-7.0.0, anyio-4.11.0, asyncio-1.2.0
collected 8 items

src/tests/integration/test_api_endpoints.py::test_root_endpoint PASSED   [ 12%]
src/tests/integration/test_api_endpoints.py::test_health_endpoint PASSED [ 25%]
...

============================== 8 passed in 2.15s ===============================
```

---

## Development Workflow

### 1. Code Style and Formatting

```bash
# Format code with Black
black src/

# Lint with Ruff
ruff check src/

# Type checking with mypy
mypy src/
```

### 2. Pre-commit Checks

Before committing code:

```bash
# Format code
black src/

# Run linter
ruff check --fix src/

# Run tests
pytest

# Check coverage
pytest --cov=src/agents
```

### 3. Making Changes

**Recommended Workflow**:

1. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
   - Update code
   - Add/update tests
   - Update documentation

3. Run tests
   ```bash
   pytest
   ```

4. Commit changes
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

5. Push and create PR
   ```bash
   git push origin feature/your-feature-name
   ```

### 4. Adding Dependencies

```bash
# Add production dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv sync

# Commit uv.lock
git add uv.lock pyproject.toml
git commit -m "chore: update dependencies"
```

---

## Project Structure

```
back-end/
├── .env                    # Environment variables (gitignored)
├── .env.example            # Environment template
├── pytest.ini              # Pytest configuration
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Dependency lock file
├── README.md               # Project README
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── DEVELOPER_SETUP.md  # This file
│   └── agents_plan/
│       └── phases/         # Phase completion docs
├── src/
│   ├── agents/
│   │   ├── models/         # Pydantic schemas
│   │   ├── core/           # Agent implementations
│   │   └── server.py       # FastAPI server
│   └── tests/
│       ├── conftest.py     # Test fixtures
│       ├── agents/         # Agent tests
│       └── integration/    # API tests
└── htmlcov/                # Coverage reports (generated)
```

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"

**Solution**:
```bash
# Check if .env exists
ls -la .env

# Check if API key is set
cat .env | grep ANTHROPIC_API_KEY

# Manually export
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Issue: "ModuleNotFoundError"

**Solution**:
```bash
# Reinstall dependencies
uv sync

# Verify virtual environment
which python  # Should show .venv/bin/python

# Activate venv if needed
source .venv/bin/activate
```

### Issue: "Port 8000 already in use"

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
uvicorn src.agents.server:app --port 8001
```

### Issue: Tests fail with "RuntimeError: Event loop is closed"

**Solution**:
```bash
# Ensure pytest-asyncio is installed
uv add --dev pytest-asyncio

# Check pytest.ini has asyncio_mode = auto
cat pytest.ini | grep asyncio_mode
```

### Issue: "403 Forbidden" from Anthropic API

**Solution**:
- Verify API key is valid
- Check API key has credits
- Ensure no typos in `.env` file

### Issue: Slow test execution

**Solution**:
```bash
# Skip slow tests during development
pytest -m "not slow"

# Run tests in parallel (install pytest-xdist)
uv add --dev pytest-xdist
pytest -n auto
```

### Issue: Import errors in VS Code

**Solution**:
1. Open Command Palette (Cmd/Ctrl + Shift + P)
2. Select "Python: Select Interpreter"
3. Choose `.venv/bin/python`
4. Reload VS Code

---

## IDE Setup

### VS Code

**Recommended Extensions**:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- Python Test Explorer

**Settings** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "src/tests"
  ],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### PyCharm

1. Open project
2. Configure Python interpreter: Settings → Project → Python Interpreter
3. Select `.venv/bin/python`
4. Enable pytest: Settings → Tools → Python Integrated Tools → Default test runner → pytest

---

## Useful Commands

### Development

```bash
# Start server
python -m src.agents.server

# Run tests
pytest

# Format code
black src/

# Lint code
ruff check src/

# Type check
mypy src/

# Coverage
pytest --cov=src/agents --cov-report=html
```

### Dependency Management

```bash
# Add dependency
uv add package-name

# Remove dependency
uv remove package-name

# Update all dependencies
uv lock --upgrade

# Show dependency tree
uv tree
```

### Database (if using AgentOS features)

```bash
# Start PostgreSQL with Docker
docker run -d \
  --name postgres-ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e POSTGRES_DB=ai \
  -p 5532:5432 \
  pgvector/pgvector:pg16

# Connect to database
psql postgresql://ai:ai@localhost:5532/ai
```

---

## Next Steps

After setup:

1. ✅ Read [API Documentation](API_DOCUMENTATION.md)
2. ✅ Explore code in `src/agents/`
3. ✅ Run existing tests
4. ✅ Try the Swagger UI at `/docs`
5. ✅ Make a test request to `/api/v1/generate`

---

## Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: Create GitHub issue
- **Tests**: Look at `src/tests/` for examples
- **API**: Use Swagger UI at http://localhost:8000/docs

---

**Last Updated**: November 6, 2025
