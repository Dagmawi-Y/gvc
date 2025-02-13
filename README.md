# GitHub Views Counter

A beautiful, customizable view counter for your GitHub repositories. Built with FastAPI and Appwrite.

## Features

- 🎨 Multiple themes (default, dark, light, blue, purple, github)
- 🎯 Different styles (flat, flat-square, plastic)
- 📏 Adjustable sizes (small, normal, large)
- 🏷️ Custom labels
- ⚡ Fast and reliable
- 🔒 Secure and non-tamperable with Appwrite backend

## Quick Start

```markdown
![Views](https://your-domain/badge/username/repo)
```

## Customization

Customize your badge using URL parameters:

```markdown
![Views](https://your-domain/badge/username/repo?theme=dark&style=flat-square&label=Visitors&size=large)
```

### Available Options

- **Themes**: `default`, `dark`, `light`, `blue`, `purple`, `github`
- **Styles**: `flat`, `flat-square`, `plastic`
- **Sizes**: `small`, `normal`, `large`
- **Label**: Any text (default: "Views")

## Examples

Default:
```markdown
![Views](https://your-domain/badge/username/repo)
```

Dark theme, large size:
```markdown
![Views](https://your-domain/badge/username/repo?theme=dark&size=large)
```

Custom label, flat-square style:
```markdown
![Views](https://your-domain/badge/username/repo?label=Total%20Views&style=flat-square)
```

## License

MIT License

## Credits

Built with:
- FastAPI
- Appwrite
- Python 3.9+
