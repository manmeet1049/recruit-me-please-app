from fastapi import FastAPI

from app.routes import candidates_router

app = FastAPI(title="FastAPI Modular App")
app.include_router(candidates_router)
