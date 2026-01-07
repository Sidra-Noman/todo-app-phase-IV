from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import auth, todos
from .core.database import init_db

app = FastAPI(title="Todo App API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(todos.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}
