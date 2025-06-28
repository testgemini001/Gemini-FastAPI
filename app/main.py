from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

from .server.chat import router as chat_router
from .server.health import router as health_router
from .server.middleware import add_cors_middleware, add_exception_handler
from .services.pool import GeminiClientPool


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        pool = GeminiClientPool()
        await pool.init()
    except Exception as e:
        logger.exception(f"Failed to initialize Gemini clients: {e}")
        raise

    logger.success(f"Gemini clients initialized: {[c.id for c in pool.clients]}.")
    logger.success("Gemini API Server ready to serve requests.")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Gemini API Server",
        description="OpenAI-compatible API for Gemini Web",
        version="1.0.0",
        lifespan=lifespan,
    )

    # 添加根路径端点
    @app.get("/")
    async def root():
        return JSONResponse({
            "message": "Gemini FastAPI Server",
            "description": "OpenAI-compatible API for Gemini Web",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "models": "/v1/models",
                "chat": "/v1/chat/completions",
                "docs": "/docs",
                "openapi": "/openapi.json"
            },
            "status": "running"
        })

    add_cors_middleware(app)
    add_exception_handler(app)

    app.include_router(health_router, tags=["Health"])
    app.include_router(chat_router, tags=["Chat"])

    return app
