from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from database import AppwriteDB
from badge import generate_badge, THEMES, FONTS
from urllib.parse import urlparse

app = FastAPI(title="GitHub View Counter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = AppwriteDB()
RATE_LIMIT_MINUTES = 60

@app.get("/")
async def root():
    return {
        "message": "GitHub View Counter API",
        "usage": {
            "basic": "![Views](https://your-domain/badge/username/repo)",
            "with_options": "![Views](https://your-domain/badge/username/repo?theme=gradient-purple&style=flat&label=Views&size=large&font=fira&animation=pulse)",
            "options": {
                "theme": list(THEMES.keys()),
                "style": ["flat", "flat-square", "plastic"],
                "size": ["small", "normal", "large"],
                "font": list(FONTS.keys()),
                "animation": ["none", "pulse", "bounce", "glow"],
                "label": "any text (default: Views)"
            }
        }
    }

@app.get("/badge/{username}/{repo}")
async def get_badge(
    username: str,
    repo: str,
    request: Request,
    style: str = "flat",
    theme: str = "default",
    label: str = "Views",
    size: str = "normal",
    font: str = "default",
    animation: str = "none"
):
    repository = f"{username}/{repo}"
    
    # Check if we can increment the view count
    if await db.can_increment_view(request.client.host, username, RATE_LIMIT_MINUTES):
        count = await db.increment_views(repository)
    else:
        count = await db.get_views(repository)
    
    svg = generate_badge(
        count=count,
        style=style,
        theme=theme,
        label=label,
        size=size,
        font=font,
        animation=animation
    )
    
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 