# GitHub Views Counter

A beautiful, customizable view counter for your GitHub repositories. Built with FastAPI and Appwrite.

## Features

- 🎨 Multiple themes (including gradients and rainbow!)
- 🎯 Different styles (flat, flat-square, plastic)
- 📏 Adjustable sizes (small, normal, large)
- 🏷️ Custom labels
- ✨ Animations (pulse, bounce, glow)
- 🔤 Custom fonts
- 🔄 Reversible layout (number/label order)
- ⚡ Fast
- 🔒 Secure and non-tamperable with Appwrite backend

## Quick Start

```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo})
```

## Customization

Customize your badge using URL parameters:

```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=rainbow&style=flat&label=Views&size=large&font=fira&animation=pulse&reverse=true)
```

### Available Options

- **Themes**: 
  - Basic: `default`, `dark`, `light`, `blue`, `purple`, `github`
  - Gradient: `gradient-blue`, `gradient-purple`
  - Vibrant: `rainbow`, `sunset`, `candy`, `ocean`, `fire`, `cyberpunk`, `retro`, `neon-pink`, `cosmic`, `neon`

- **Styles**: `flat`, `flat-square`, `plastic`
- **Sizes**: `small`, `normal`, `large`
- **Layout**: `reverse=true/false` (switches number/label order)
- **Fonts**: 
  - `default` (Segoe UI)
  - `mono` (SFMono)
  - `serif` (Times New Roman)
  - `comic` (Comic Sans MS)
  - `fira` (Fira Code)
  - `roboto` (Roboto)

- **Animations**:
  - `none` (default)
  - `pulse` (fade in/out)
  - `bounce` (subtle bounce)
  - `glow` (glowing effect)

- **Label**: Any text (default: "Views")

## Cool Examples

Rainbow theme with reversed layout:
```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=rainbow&reverse=true)
```

Cyberpunk with glow:
```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=cyberpunk&animation=glow)
```

Sunset theme with custom label:
```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=sunset&label=Total)
```

## License

MIT License

## Credits

Built with:
- FastAPI
- Appwrite
- Python 3.9+
