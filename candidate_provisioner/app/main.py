from fastapi import FastAPI

from app.routes import candidates_router
from app.middleware import APIKeyMiddleware

app = FastAPI(title="FastAPI Modular App")

# Middlewares
app.add_middleware(APIKeyMiddleware)


# Routers
app.include_router(candidates_router)
