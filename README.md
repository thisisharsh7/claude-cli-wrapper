# CCUX — Claude Code UI Generator

> Professional landing pages from your terminal using AI

**Open source and completely free**

## What is CCUX?

CCUX is a powerful CLI tool that uses Claude AI to generate conversion-optimized landing pages in minutes. It features both interactive and command-line interfaces, making it perfect for developers who want professional results without leaving the terminal.

## Core Features

### 🎨 **Interactive Application**
Launch with `ccux init` for a guided experience:
- **Project Wizard**: Step-by-step landing page creation
- **Visual Management**: Manage multiple projects with rich terminal UI  
- **Live Editing**: Edit content, regenerate sections, change themes
- **Smart Detection**: Auto-discovers existing projects and configurations
- **ESC Key Support**: Press ESC anywhere to immediately exit

### 🚀 **AI-Powered Generation**
- **12-Phase Design Process**: Professional UX methodology used by agencies
- **Competitor Analysis**: Automatically finds and analyzes 3 competitor sites
- **Smart Copy**: Generates conversion-optimized headlines and content
- **User Research**: Creates personas, empathy maps, and user journeys

### 🎭 **13 Professional Themes**
Choose from carefully designed themes:
- **Core**: minimal, brutalist, playful, corporate
- **Modern**: morphism, animated, terminal, aesthetic  
- **Specialized**: dark, vibrant, sustainable, data, illustrated

### ⚡ **Advanced Section Management**
- **Precision Regeneration**: Update only specific sections (hero, features, pricing, etc.)
- **Content Editing**: Make targeted changes through interactive interface
- **Theme Switching**: Change visual style while preserving content  
- **Form Management**: Add, remove, or customize contact forms

*Advanced editing, theming, and form features are available through the interactive application (`ccux init`).*

### 🔧 **Developer Experience**
- **Two Output Formats**: HTML with TailwindCSS or React components
- **Production Ready**: Clean, semantic code with SEO optimization
- **Mobile First**: Responsive design for all screen sizes
- **Accessibility**: WCAG compliant with proper ARIA labels
- **Cost Tracking**: Monitor token usage and estimated costs with `ccux cost`

## Quick Start

### Interactive Mode (Recommended)
```bash
# Install
pip install ccux

# Launch interactive app
ccux init
```

### Command Line Mode
```bash
# Generate a landing page
ccux gen --desc "AI-powered project management tool" --theme brutalist

# Regenerate specific sections
ccux regen --section hero,pricing

# List existing projects
ccux projects

# Get help
ccux help themes
```

## Available Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `ccux init` | Launch interactive app | `ccux init` |
| `ccux gen` | Generate landing page | `ccux gen --desc "SaaS platform"` |  
| `ccux regen` | Regenerate sections | `ccux regen --section hero` |
| `ccux projects` | List projects | `ccux projects` |
| `ccux cost` | Show cost analysis | `ccux cost --detailed` |
| `ccux help` | Get help | `ccux help themes` |
| `ccux version` | Show version | `ccux version` |

**Note:** Advanced features like `editgen`, `theme`, and `form` commands are available through the interactive application (`ccux init`).

## Design Process

CCUX uses a comprehensive 12-phase methodology:

1. **Reference Discovery** - Finds competitor sites automatically
2. **Screenshot Analysis** - Captures and analyzes competitor designs  
3. **Product Understanding** - Deep analysis of value proposition
4. **UX Research** - Creates user personas and empathy maps
5. **Site Flow** - Maps user journeys and conversion paths
6. **Content Strategy** - Develops strategic messaging
7. **Wireframing** - Validates layout structure
8. **Design System** - Creates consistent visual language
9. **High-Fidelity Design** - Polishes visual elements
10. **Prototyping** - Adds interactive elements
11. **Copy Refinement** - Optimizes conversion copy
12. **Implementation** - Generates production code

## Theme Showcase

### Core Themes
- **Minimal**: Clean, content-focused design following Dieter Rams' principles
- **Brutalist**: Raw, honest design inspired by Brutalist architecture
- **Playful**: Joyful, approachable design with organic shapes
- **Corporate**: Traditional, trustworthy business design

### Modern Themes  
- **Morphism**: Soft, tactile design combining neumorphism and glassmorphism
- **Animated**: Motion-first design where animation drives experience
- **Terminal**: Monospace, CLI-inspired aesthetic for developers
- **Aesthetic**: Retro-futuristic Y2K and vaporwave styling

### Specialized Themes
- **Dark**: Modern dark theme optimized for reduced eye strain
- **Vibrant**: Colorful, dopamine-rich design that energizes users
- **Sustainable**: Nature-inspired design for eco-conscious brands
- **Data**: Information-dense design for dashboards and analytics
- **Illustrated**: Hand-drawn, custom illustration-driven design

## Output Examples

Generated pages include:
- **Semantic HTML** with proper structure and SEO tags
- **TailwindCSS** styling with custom design systems
- **Responsive Design** that works on all devices
- **Accessibility Features** with WCAG compliance
- **Performance Optimization** with clean, minimal code
- **Section Markers** for easy regeneration and editing

## Prerequisites

- **Claude CLI** - Get it from [claude.ai/code](https://claude.ai/code)
- **Python 3.9+** - Standard on most systems
- **Internet Connection** - For competitor analysis

## Installation

```bash
# Production install
pip install ccux

# Development install
git clone https://github.com/thisisharsh7/claude-cli-wrapper.git
cd claude-cli-wrapper
pip install -e .
```

## Preview Your Pages

```bash
# Navigate to your project
cd output/  # or output1/, output2/, etc.

# Start local server
python -m http.server 3000

# Open http://localhost:3000 in browser
```

## Project Structure

```
output/                 # Your generated landing page
├── index.html         # Main landing page file
├── design_analysis.json  # Complete design research data
└── *.jpg              # Competitor screenshots (if any)
```

## Get Help

- `ccux help` - Comprehensive command guide
- `ccux help quickstart` - Step-by-step setup
- `ccux help themes` - All theme descriptions  
- `ccux help workflows` - Common usage patterns

## Links

- **PyPI**: [https://pypi.org/project/ccux/](https://pypi.org/project/ccux/)
- **GitHub**: [https://github.com/thisisharsh7/claude-cli-wrapper](https://github.com/thisisharsh7/claude-cli-wrapper)
- **Claude CLI**: [https://claude.ai/code](https://claude.ai/code)

---

**⭐ Star this project if you find it useful!**

Made with ❤️ for developers who live in the terminal.