from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health
from app.routes import parse

app = FastAPI()

# 1. Define who is allowed to talk to your backend
origins = [
    "http://localhost:5173",    # Default Vite port
    "http://127.0.0.1:5173",    # Alternate local port
]

# 2. Add the safety pass-through middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Gives your Vue app permission
    allow_credentials=True,
    allow_methods=["*"],        # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],        # Allows headers like Content-Type
)

# 3. Your existing routes
app.include_router(health.router)
app.include_router(parse.router)