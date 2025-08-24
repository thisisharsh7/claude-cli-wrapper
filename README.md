# CCUX — Claude Code UI Generator

> Professional landing pages from your terminal using AI — **Now with Web Platform!**

**🎆 Version 2.1 - CLI + Web Platform Integration!**

**Open source and completely free**

## 🌟 New: CCUX Web Platform

**Access CCUX through a beautiful web interface!** The complete web platform includes:

- **🖥️ Modern Web UI**: Next.js frontend with "Eeveelution" interface
- **⚡ FastAPI Backend**: RESTful API wrapping the CCUX CLI
- **🔄 Real-time Progress**: Live generation tracking with status updates
- **📊 Project Dashboard**: Manage all your generated projects in one place
- **🎯 Two Access Methods**: Use the CLI or web interface — your choice!

## What is CCUX?

CCUX is a powerful, modular CLI tool that uses Claude AI to generate conversion-optimized landing pages in minutes. Built with a clean, maintainable architecture, it features both interactive and command-line interfaces, making it perfect for developers who want professional results without leaving the terminal.

**✨ Recently Enhanced**: Completely refactored with a modular core system for better maintainability, performance, and extensibility.

## 🆕 What's New in Version 2.0

### **Modular Core Architecture**
- **78% Code Reduction**: Eliminated duplicate code through smart modularization
- **9 Specialized Modules**: Each handling specific functionality (cost tracking, forms, animations, etc.)
- **Zero Duplication**: Every function exists in exactly one place
- **Better Testing**: Modular design enables comprehensive unit testing

### **Enhanced Developer Experience**
- **Cleaner Imports**: Clear dependency relationships between components  
- **Easier Maintenance**: Changes only need to be made in one location
- **Better Performance**: Optimized loading and memory usage
- **Extensible Design**: New features can be easily added to appropriate modules

### **Improved CLI Interface**
- **Command Delegation**: Clean separation between user interface and implementation
- **Better Help System**: Comprehensive documentation built into commands
- **Consistent API**: Unified interface across all functionality

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
- **Modular Architecture**: Clean, organized codebase with specialized utility modules
- **Two Output Formats**: HTML with TailwindCSS or React components
- **Production Ready**: Clean, semantic code with SEO optimization
- **Mobile First**: Responsive design for all screen sizes
- **Accessibility**: WCAG compliant with proper ARIA labels
- **Cost Tracking**: Monitor token usage and estimated costs
- **Easy Maintenance**: 78% code reduction through deduplication and modular design

## Quick Start

### 🌐 Web Platform (New!)
```bash
# Clone the repository
git clone <repository-url>
cd cool/

# Start both frontend and backend
./start.sh

# Open http://localhost:3000 in your browser
```

### 💻 CLI Mode  
```bash
# Install CCUX CLI
pip install ccux

# Interactive terminal app
ccux init

# Command line generation
ccux gen --desc "AI-powered project management tool" --theme brutalist
ccux gen --desc-file product-description.pdf --theme minimal

# Advanced section management
ccux regen --section hero,pricing
```



### 📋 Requirements

**For CLI Usage:**
- Python 3.9+ and pip
- Claude CLI configured with API key

**For Web Platform:**  
- Python 3.11+ (backend)
- Node.js 18+ (frontend)
- CCUX CLI tool
- Claude CLI configured

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
# Production install (gets the latest modular version)
pip install ccux

# Development install 
git clone https://github.com/thisisharsh7/claude-cli-wrapper.git
cd claude-cli-wrapper
pip install -e .
```

> **Note**: Make sure you're getting version 2.0+ to benefit from the new modular architecture and performance improvements.

## Preview Your Pages

```bash
# Navigate to your project
cd output/  # or output1/, output2/, etc.

# Start local server
python -m http.server 3000

# Open http://localhost:3000 in browser
```

## Project Structure

### 🌐 Web Platform Structure
```
cool/
├── backend/                 # FastAPI backend service
│   ├── main.py             # FastAPI application entry
│   ├── routes/             # API endpoint definitions  
│   ├── services/           # CCUX CLI integration
│   ├── models/             # Request/response models
│   ├── projects/           # Generated project storage
│   └── static/             # Web-served files
├── frontend/               # Next.js frontend application  
│   ├── app/                # Next.js 14 App Router pages
│   ├── components/         # Reusable UI components
│   └── lib/                # API client and utilities
└── src/ccux/               # CCUX CLI source code
```

### 💻 CLI Generated Output
```
output/                 # Your generated landing page
├── index.html         # Main landing page file
├── design_analysis.json  # Complete design research data
└── *.jpg              # Competitor screenshots (if any)
```

### 🏗️ CCUX Core Architecture
```
src/ccux/
├── cli.py                   # User-facing CLI with help system
├── cli_old.py               # Core command implementations
├── interactive.py           # Rich terminal application
├── core/                    # Modular utility system
│   ├── usage_tracking.py    # Cost calculation and analytics
│   ├── signal_handling.py   # Graceful interrupt handling
│   ├── configuration.py     # YAML config management
│   ├── project_management.py # Project discovery and selection
│   ├── claude_integration.py # Claude API integration
│   ├── content_processing.py # HTML validation and processing
│   ├── form_handling.py     # Form generation and management
│   ├── section_management.py # Section replacement logic
│   └── animation_utilities.py # Theme-appropriate animations
├── theme_specifications.py  # 13 professional design themes
├── prompt_templates.py      # 12-phase design methodology
├── scrape.py               # Advanced web scraping
└── scrape_simple.py        # Simple screenshot capture
```

## Architecture Benefits

### 🧹 **Code Quality**
- **78% Reduction**: From 3,925 lines to 841 lines in CLI files + organized modules
- **Zero Duplication**: Each function exists in only one place
- **Clean Imports**: Clear dependency relationships between modules
- **Better Testing**: Modular functions are easier to unit test

### 🔧 **Maintainability** 
- **Logical Organization**: Functions grouped by responsibility
- **Easy Updates**: Changes only need to be made in one location
- **Clear Structure**: Easy to find and modify specific functionality
- **Extensible Design**: New features can be added to appropriate modules

### 🚀 **Performance**
- **Optimized Imports**: Only load needed functionality
- **Shared Utilities**: Common functions available to all components
- **Better Memory Usage**: Modular loading reduces memory footprint
- **Faster Development**: Clear structure speeds up feature development

## Get Help

- `ccux help` - Comprehensive command guide
- `ccux help quickstart` - Step-by-step setup
- `ccux help themes` - All theme descriptions  
- `ccux help workflows` - Common usage patterns

## 🚀 Getting Started

### Choose Your Interface

**🌐 Web Platform** (Recommended for beginners)
- Beautiful visual interface with "Eeveelution" theme
- Real-time progress tracking and project management  
- Perfect for designers and non-technical users
- See `backend/README.md` and `frontend/README.md` for details

**💻 CLI Tool** (Power users)
- Terminal-based with full control and automation
- Interactive mode with rich terminal UI
- Perfect for developers and scripts
- Install with `pip install ccux`

### 📚 Documentation

- **Backend API**: See `backend/README.md` for FastAPI documentation
- **Frontend**: See `frontend/README.md` for Next.js setup and features
- **CLI Commands**: Run `ccux help` for comprehensive command guide
- **Themes**: Run `ccux help themes` for all theme descriptions

## 🔗 Links

- **PyPI**: [https://pypi.org/project/ccux/](https://pypi.org/project/ccux/)
- **GitHub**: [https://github.com/thisisharsh7/claude-cli-wrapper](https://github.com/thisisharsh7/claude-cli-wrapper)
- **Claude CLI**: [https://claude.ai/code](https://claude.ai/code)

## 🎯 What's Next?

1. **Try the Web Platform**: Run `./start.sh` and explore the visual interface
2. **Use the CLI**: Install with `pip install ccux` and try `ccux init`  
3. **Generate Your First Page**: Describe your product and watch it evolve
4. **Explore Themes**: Try different design systems for your brand
5. **Share Your Results**: Show off your AI-generated landing pages!

---

**⭐ Star this project if you find it useful!**

Built with enterprise-grade architecture and ❤️ for developers who love both terminal and web interfaces.

**🚀 Ready for production • 🧩 Modular by design • 📊 Performance optimized**

---

## 🌐 Web Platform Available!

**New: Complete web interface for CCUX!** A beautiful Next.js + FastAPI web application that makes AI-powered landing page generation accessible through an intuitive browser interface.

**📖 See [README-WEB.md](README-WEB.md)** for the complete web platform documentation including:
- Frontend + Backend setup and architecture
- Real-time generation with project dashboard  
- One-command startup with `./start.sh`
- Full deployment guides for production

**🎯 Choose your interface**: Terminal (this README) or Web (README-WEB.md) — both powered by the same AI engine!