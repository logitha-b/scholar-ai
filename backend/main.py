from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.database import engine
from app.models.user import Base
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.learning import router as learning_router
from app.api.admin import router as admin_router
from app.api.other_routes import (
    comm_router, placement_router,
    resources_router, aptitude_router
)

# Create all DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Scholr AI API",
    description="AI-powered student learning platform for India",
    version="1.0.0",
)

# CORS – allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(learning_router)
app.include_router(admin_router)
app.include_router(comm_router)
app.include_router(placement_router)
app.include_router(resources_router)
app.include_router(aptitude_router)

# Serve uploaded files (optional, for local dev)
uploads_dir = Path("./uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def root():
    return {"message": "Scholr AI API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}
