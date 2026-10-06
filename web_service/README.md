## Project layout

- Refer [Anatomy of a Scalable Python Project (FastAPI)](https://youtu.be/Af6Zr0tNNdE?si=z06UFfdJ5pXXd9nR) by [@ArjanCodes](https://www.youtube.com/@ArjanCodes)

```text
my_project/
├── .github/              # CI/CD workflows (GitHub Actions)
├── docs/                 # Project documentation
├── src/                  # Source code root layout
│   └── app/              # Main application package
│       ├── api/          # HTTP routes / endpoints (FastAPI, Flask)
│       │   ├── v1/       # API versioning
│       │   │   ├── endpoints/
│       │   │   └── router.py
│       │   └── deps.py   # Shared dependencies (e.g., auth, get_db)
│       ├── core/         # Global configuration & security
│       │   ├── config.py # Pydantic settings (.env parser)
│       │   ├── security.py # Password hashing, JWT tokens
│       │   └── database.py # SQLAlchemy session maker / engine setup
│       ├── models/       # Database ORM models (SQLAlchemy, Tortoise)
│       ├── schemas/      # Pydantic validation / serialization models
│       ├── services/     # Pure business logic (framework independent)
│       ├── repositories/ # Database query abstraction layer
│       ├── utils/        # Small, focused helper functions
│       └── main.py       # Thin entry point for app initialization
├── tests/                # Automated tests (mirrors src/app structure)
│   ├── conftest.py       # Pytest fixtures
│   ├── unit/
│   └── integration/
├── .env                  # Local environment variables (never committed)
├── .env.example          # Template for required environment variables
├── .gitignore            # Git exclusion rules
├── pyproject.toml        # Dependencies and build system configuration
└── README.md             # Project overview and run instructions
```

## Running the Application

### 1. Install Dependencies
First, ensure all dependencies are installed:

```bash
uv sync
# OR if you don't have uv set up as a tool
pip install -e .
```

### 2. Run the Application
You can run the application using `uvicorn`. Since the FastAPI app is defined in `app/main.py`, you should point it to the app object:

```bash
# Using uvicorn directly
uv run uvicorn app.main:app --reload
```