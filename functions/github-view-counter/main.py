import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from database import AppwriteDB
from badge import generate_badge, THEMES, FONTS

app = FastAPI(title="GitHub View Counter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = AppwriteDB()

async def handle_badge_request(username: str, repo: str, request_data: dict):
    style = request_data.get('style', 'flat')
    theme = request_data.get('theme', 'default')
    label = request_data.get('label', 'Views')
    size = request_data.get('size', 'normal')
    font = request_data.get('font', 'default')
    animation = request_data.get('animation', 'none')
    reverse = request_data.get('reverse', False)
    
    repository = f"{username}/{repo}"
    
    # Get visitor information from headers
    headers = request_data.get('headers', {})
    client_ip = headers.get('x-forwarded-for', '')
    user_agent = headers.get('user-agent', '')
    referrer = headers.get('referer', '')
    
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
    
    return {
        'content': svg,
        'headers': {
            'Content-Type': 'image/svg+xml',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    }

def main(context):
    """
    Appwrite function handler
    """
    request_data = context.req.body
    
    path = context.req.path or ''
    parts = path.strip('/').split('/')
    
    if not parts or parts[0] == '':
        return {
            'message': 'GitHub View Counter API',
            'usage': '![Views](https://your-domain/badge/username/repo)'
        }
    
    if len(parts) >= 2:
        username = parts[0]
        repo = parts[1]
        return handle_badge_request(username, repo, request_data)
    
    return {'error': 'Invalid path'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 