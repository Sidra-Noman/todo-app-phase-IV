from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import auth, todos
from .api.chat_router import router as chat_router
from .api.conversation_router import router as conversation_router
from .core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (if needed)
    pass

app = FastAPI(title="Todo App API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(todos.router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(conversation_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}
