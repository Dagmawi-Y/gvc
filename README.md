# GitHub Views Counter

A beautiful, customizable view counter for your GitHub repositories. Built with FastAPI and Appwrite.

## Features

- 🎨 Multiple themes (including gradient themes!)
- 🎯 Different styles (flat, flat-square, plastic)
- 📏 Adjustable sizes (small, normal, large)
- 🏷️ Custom labels
- ✨ Animations (pulse, bounce, glow)
- 🔤 Custom fonts
- ⚡ Fast
- 🔒 Secure and non-tamperable with Appwrite backend

## Quick Start

```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo})
```

## Customization

Customize your badge using URL parameters:

```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=gradient-purple&style=flat&label=Views&size=large&font=fira&animation=pulse)
```

### Available Options

- **Themes**: 
  - Basic: `default`, `dark`, `light`, `blue`, `purple`, `github`
  - Gradient: `gradient-blue`, `gradient-purple`
  - Special: `neon`

- **Styles**: `flat`, `flat-square`, `plastic`
- **Sizes**: `small`, `normal`, `large`
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

Default with animation:
```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?animation=pulse)
```

Gradient theme with custom font:
```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=gradient-purple&font=fira)
```

Neon theme with glow:
```markdown
![Views](https://gh-views-counter.onrender.com/badge/{username}/{repo}?theme=neon&animation=glow)
```

## What Makes This Counter Special?

1. **Unique Gradient Themes**: Beautiful gradient color schemes
2. **Animations**: Add life to your badges with subtle animations
3. **Font Choices**: Match your repository's style
4. **Neon Theme**: Stand out with a cyberpunk-style badge
5. **Smart Number Formatting**: Clean display of large numbers
6. **Real-time Updates**: Instant view counting
7. **Non-tamperable**: Secure backend with Appwrite

## License

MIT License

## Credits

Built with:
- FastAPI
- Appwrite
- Python 3.9+
