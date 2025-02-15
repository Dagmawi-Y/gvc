from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from .database import AppwriteDB
from .badge import generate_badge, THEMES, FONTS
import asyncio
from fastapi import Request as FastAPIRequest
from typing import Any

app = FastAPI(title="GitHub View Counter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = AppwriteDB()

@app.get("/")
async def root():
    return {
        "message": "GitHub View Counter API",
        "usage": "![Views](https://your-domain/badge/username/repo)"
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
    animation: str = "none",
    reverse: bool = False
):
    repository = f"{username}/{repo}"
    
    # Get visitor information
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    referrer = request.headers.get("referer", "")
    
    can_increment = await db.can_increment_view(
        username=username,
        ip=client_ip,
        referrer=referrer,
        user_agent=user_agent,
        rate_limit_minutes=5
    )
    
    if can_increment:
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
        animation=animation,
        reverse=reverse
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

async def main(context: Any) -> Any:
    request = FastAPIRequest(scope={
        'type': 'http',
        'method': context.req.method,
        'path': context.req.path,
        'query_string': context.req.query_string.encode(),
        'headers': [[k.lower().encode(), v.encode()] for k, v in context.req.headers.items()],
        'client': ('127.0.0.1', 0),
    })
    
    path_parts = context.req.path.strip('/').split('/')
    if len(path_parts) < 2:
        return {
            "message": "GitHub View Counter API",
            "usage": "![Views](https://your-domain/badge/username/repo)"
        }
    
    username, repo = path_parts[-2:]
    
    query_params = context.req.query
    style = query_params.get('style', 'flat')
    theme = query_params.get('theme', 'default')
    label = query_params.get('label', 'Views')
    size = query_params.get('size', 'normal')
    font = query_params.get('font', 'default')
    animation = query_params.get('animation', 'none')
    reverse = query_params.get('reverse', 'false').lower() == 'true'
    
    response = await get_badge(
        username=username,
        repo=repo,
        request=request,
        style=style,
        theme=theme,
        label=label,
        size=size,
        font=font,
        animation=animation,
        reverse=reverse
    )
    
    return response.body, response.media_type, dict(response.headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 