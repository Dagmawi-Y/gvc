import os
import sys
import asyncio
import json
import base64

# Add the current directory to Python path
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

async def handle_badge_request(username: str, repo: str, context):
    # Get query parameters from context
    query = context.req.query or {}
    style = query.get('style', 'flat')
    theme = query.get('theme', 'default')
    label = query.get('label', 'Views')
    size = query.get('size', 'normal')
    font = query.get('font', 'default')
    animation = query.get('animation', 'none')
    reverse = query.get('reverse', 'false').lower() == 'true'
    
    repository = f"{username}/{repo}"
    
    # Get visitor information from headers
    headers = context.req.headers or {}
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
    
    svg_bytes = svg.encode('utf-8')
    svg_base64 = base64.b64encode(svg_bytes).decode('utf-8')
    data_uri = f'data:image/svg+xml;base64,{svg_base64}'
    
    return {
        'body': data_uri,
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    }

async def main(context):
    """
    Appwrite function handler
    """
    path = context.req.path or ''
    parts = path.strip('/').split('/')
    
    if not parts or parts[0] == '':
        return {
            'body': json.dumps({
                'message': 'GitHub View Counter API',
                'usage': '![Views](https://your-domain/badge/username/repo)'
            }),
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    if len(parts) >= 2:
        username = parts[0]
        repo = parts[1]
        return await handle_badge_request(username, repo, context)
    
    return {
        'body': json.dumps({
            'error': 'Invalid path'
        }),
        'statusCode': 400,
        'headers': {
            'Content-Type': 'application/json'
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 