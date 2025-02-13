def format_number(count: int) -> str:
    if count < 1000:
        return str(count)
    elif count < 1000000:
        return f"{count/1000:.1f}k".rstrip('0').rstrip('.')
    elif count < 1000000000:
        return f"{count/1000000:.1f}M".rstrip('0').rstrip('.')
    else:
        return f"{count/1000000000:.1f}B".rstrip('0').rstrip('.')

# Predefined color themes
THEMES = {
    "default": {"bg": "#555", "count": "#4c1", "text": "#fff"},
    "dark": {"bg": "#222", "count": "#6f42c1", "text": "#fff"},
    "light": {"bg": "#eee", "count": "#4c1", "text": "#333"},
    "blue": {"bg": "#007acc", "count": "#2ea44f", "text": "#fff"},
    "purple": {"bg": "#6f42c1", "count": "#2ea44f", "text": "#fff"},
    "github": {"bg": "#24292e", "count": "#2ea44f", "text": "#fff"},
}

def generate_badge(
    count: int,
    style: str = "flat",
    theme: str = "default",
    label: str = "Views",
    size: str = "normal"
) -> str:
    count_str = format_number(count)
    
    # Get theme colors
    colors = THEMES.get(theme, THEMES["default"])
    
    # Adjust sizes based on size parameter
    if size == "small":
        height = 16
        font_size = 9
        label_width = 55
    elif size == "large":
        height = 24
        font_size = 13
        label_width = 85
    else:  # normal
        height = 20
        font_size = 11
        label_width = 70

    # Calculate widths
    count_width = len(count_str) * (font_size - 3) + 15
    total_width = label_width + count_width

    if style == "flat":
        svg = f'''
        <svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height}">
            <linearGradient id="b" x2="0" y2="100%">
                <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
                <stop offset="1" stop-opacity=".1"/>
            </linearGradient>
            <mask id="a">
                <rect width="{total_width}" height="{height}" rx="3" fill="#fff"/>
            </mask>
            <g mask="url(#a)">
                <path fill="{colors['bg']}" d="M0 0h{label_width}v{height}H0z"/>
                <path fill="{colors['count']}" d="M{label_width} 0h{count_width}v{height}H{label_width}z"/>
                <path fill="url(#b)" d="M0 0h{total_width}v{height}H0z"/>
            </g>
            <g fill="{colors['text']}" text-anchor="middle" font-family="Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji" font-size="{font_size}">
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
            <g fill="{colors['text']}" text-anchor="middle" font-family="Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji" font-size="{font_size}">
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
            <g fill="{colors['text']}" text-anchor="middle" font-family="Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji" font-size="{font_size}">
                <text x="{label_width/2}" y="{height*0.7}">{label}</text>
                <text x="{label_width + count_width/2}" y="{height*0.7}">{count_str}</text>
            </g>
        </svg>
        '''
    else:
        svg = generate_badge(count, "flat", theme, label, size)

    return svg.strip() 