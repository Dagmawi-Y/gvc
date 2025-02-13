def format_number(count: int) -> str:
    if count < 1000:
        return str(count)
    elif count < 1000000:
        return f"{count/1000:.1f}k".rstrip('0').rstrip('.')
    elif count < 1000000000:
        return f"{count/1000000:.1f}M".rstrip('0').rstrip('.')
    else:
        return f"{count/1000000000:.1f}B".rstrip('0').rstrip('.')

def truncate_text(text: str, max_length: int = 15) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length-1] + "…"

THEMES = {
    "default": {"bg": "#555", "count": "#4c1", "text": "#fff"},
    "dark": {"bg": "#222", "count": "#6f42c1", "text": "#fff"},
    "light": {"bg": "#eee", "count": "#4c1", "text": "#333"},
    "blue": {"bg": "#007acc", "count": "#2ea44f", "text": "#fff"},
    "purple": {"bg": "#6f42c1", "count": "#2ea44f", "text": "#fff"},
    "github": {"bg": "#24292e", "count": "#2ea44f", "text": "#fff"},
    "gradient-blue": {"bg": "url(#grad1)", "count": "url(#grad2)", "text": "#fff"},
    "gradient-purple": {"bg": "url(#grad3)", "count": "url(#grad4)", "text": "#fff"},
    "neon": {"bg": "#000", "count": "#0ff", "text": "#fff"},
}

FONTS = {
    "default": "Segoe UI,Helvetica,Arial,sans-serif",
    "mono": "SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace",
    "serif": "Times New Roman,serif",
    "comic": "Comic Sans MS,cursive",
    "fira": "Fira Code,monospace",
    "roboto": "Roboto,sans-serif"
}

def generate_badge(
    count: int,
    style: str = "flat",
    theme: str = "default",
    label: str = "Views",
    size: str = "normal",
    font: str = "default",
    animation: str = "none"
) -> str:
    count_str = format_number(count)
    
    colors = THEMES.get(theme, THEMES["default"])
    font_family = FONTS.get(font, FONTS["default"])
    
    if size == "small":
        height = 16
        font_size = 9
        label_width = 55
        max_label_length = 10
    elif size == "large":
        height = 24
        font_size = 13
        label_width = 85
        max_label_length = 20
    else:  # normal
        height = 20
        font_size = 11
        label_width = 70
        max_label_length = 15

    label = truncate_text(label, max_label_length)

    count_width = len(count_str) * (font_size - 3) + 15
    total_width = label_width + count_width

    base_gradients = f'''
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#00356B;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#1E90FF;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#2ea44f;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#32CD32;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#6f42c1;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#DA70D6;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#FF69B4;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FF1493;stop-opacity:1" />
            </linearGradient>
        </defs>
    '''

    animation_style = ""
    if animation == "pulse":
        animation_style = '''
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.7; }
                100% { opacity: 1; }
            }
        '''
    elif animation == "bounce":
        animation_style = '''
            @keyframes bounce {
                0% { transform: translateY(0); }
                50% { transform: translateY(-2px); }
                100% { transform: translateY(0); }
            }
        '''
    elif animation == "glow":
        animation_style = '''
            @keyframes glow {
                0% { filter: brightness(1); }
                50% { filter: brightness(1.2); }
                100% { filter: brightness(1); }
            }
        '''

    if style == "flat":
        svg = f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}">
            <style>
                {animation_style}
                .animated {{ animation: {animation} 2s infinite; }}
            </style>
            {base_gradients}
            <linearGradient id="b" x2="0" y2="100%">
                <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
                <stop offset="1" stop-opacity=".1"/>
            </linearGradient>
            <mask id="a">
                <rect width="{total_width}" height="{height}" rx="3" fill="#fff"/>
            </mask>
            <g mask="url(#a)" class="{f'animated' if animation != 'none' else ''}">
                <path fill="{colors['bg']}" d="M0 0h{label_width}v{height}H0z"/>
                <path fill="{colors['count']}" d="M{label_width} 0h{count_width}v{height}H{label_width}z"/>
                <path fill="url(#b)" d="M0 0h{total_width}v{height}H0z"/>
            </g>
            <g fill="{colors['text']}" text-anchor="middle" font-family="{font_family}" font-size="{font_size}">
                <text x="{label_width/2}" y="{height*0.75}" fill-opacity=".3">{label}</text>
                <text x="{label_width/2}" y="{height*0.7}">{label}</text>
                <text x="{label_width + count_width/2}" y="{height*0.75}" fill-opacity=".3">{count_str}</text>
                <text x="{label_width + count_width/2}" y="{height*0.7}">{count_str}</text>
            </g>
        </svg>
        '''
    elif style == "flat-square":
        svg = f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}">
            <g>
                <rect fill="{colors['bg']}" width="{label_width}" height="{height}"/>
                <rect fill="{colors['count']}" x="{label_width}" width="{count_width}" height="{height}"/>
            </g>
            <g fill="{colors['text']}" text-anchor="middle" font-family="{font_family}" font-size="{font_size}">
                <text x="{label_width/2}" y="{height*0.7}">{label}</text>
                <text x="{label_width + count_width/2}" y="{height*0.7}">{count_str}</text>
            </g>
        </svg>
        '''
    elif style == "plastic":
        svg = f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}">
            <linearGradient id="b" x2="0" y2="100%">
                <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
                <stop offset=".1" stop-color="#aaa" stop-opacity=".1"/>
                <stop offset=".9" stop-opacity=".3"/>
                <stop offset="1" stop-opacity=".5"/>
            </linearGradient>
            <mask id="a">
                <rect width="{total_width}" height="{height}" rx="4" fill="#fff"/>
            </mask>
            <g mask="url(#a)">
                <path fill="{colors['bg']}" d="M0 0h{label_width}v{height}H0z"/>
                <path fill="{colors['count']}" d="M{label_width} 0h{count_width}v{height}H{label_width}z"/>
                <path fill="url(#b)" d="M0 0h{total_width}v{height}H0z"/>
            </g>
            <g fill="{colors['text']}" text-anchor="middle" font-family="{font_family}" font-size="{font_size}">
                <text x="{label_width/2}" y="{height*0.7}">{label}</text>
                <text x="{label_width + count_width/2}" y="{height*0.7}">{count_str}</text>
            </g>
        </svg>
        '''
    else:
        svg = generate_badge(count, "flat", theme, label, size, font, animation)

    return svg.strip() 