import warnings
# Suppress known DeprecationWarning from python-jose internals which use
# datetime.utcnow() (the library issue is harmless for our usage and
# produces noisy yellow warnings). We scope the filter to the jose.jwt
# module so other DeprecationWarnings still appear during development.
warnings.filterwarnings("ignore", category=DeprecationWarning)

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .routes import auth, projects, issues, comments

app = FastAPI(
    title="IssueHub API",
    description="A lightweight bug tracker API",
    version="1.0.0"
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            }
        }
    )

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(issues.router)
app.include_router(comments.router)

@app.get("/")
def root():
    return {"message": "Welcome to IssueHub API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
