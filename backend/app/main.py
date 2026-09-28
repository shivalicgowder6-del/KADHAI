from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, media, sessions, stories, tts

app = FastAPI(
    title="KADHAI API",
    description="Backend API for the KADHAI interactive storytelling platform.",
    version="0.1.0",
)

# Permissive CORS for local development. Phase 2's React dev server (Vite,
# typically http://localhost:5173) needs to call this API from the browser.
# Tighten this to an explicit allow-list before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(stories.router)
app.include_router(sessions.router)
app.include_router(media.router)
app.include_router(tts.router)