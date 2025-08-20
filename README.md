# CCUX — Claude Code UI Generator

> Generate professional landing pages from your terminal

**Open source and completely free**

## What is this?

CCUX is an open-source CLI tool that uses Claude AI to generate conversion-optimized landing pages in minutes. It analyzes competitors, creates user research, and outputs production-ready HTML/React code with TailwindCSS.

## Why I built this

As a developer, I was tired of:
- Switching between multiple design tools
- Spending hours on landing page decisions  
- Getting mediocre results from drag-and-drop builders

I wanted professional landing pages generated with proven UX methodology, straight from my terminal.

## Who is it for?

- **Indie hackers** testing product ideas quickly
- **Startups** shipping MVPs without design bottlenecks
- **Developers** who want to stay in terminal workflow
- **Freelancers/Agencies** needing faster client deliverables
- **Anyone** who prefers code they own over SaaS builders

## How it helps

- **Save time**: Generate pages in 3 minutes vs 3 days
- **Better conversions**: Uses 12-phase UX methodology agencies charge $1000s for
- **Stay focused**: No context switching from terminal to design tools
- **Own your code**: React/HTML output you can modify and deploy anywhere
- **Smart research**: Automatically analyzes 3 competitors for design inspiration

## What problem it solves

**The Problem**: Creating professional landing pages requires design skills, UX knowledge, competitor research, and hours of work.

**The Solution**: CCUX automates the entire process:
1. Finds and analyzes 3 competitor sites automatically
2. Runs professional UX research (personas, user journeys, wireframes)
3. Generates strategic copy and design system
4. Outputs production-ready code you can deploy immediately

## Prerequisites

- **Claude CLI** - Install from [claude.ai/code](https://www.anthropic.com/api)
- **Python 3.9+** - Most systems have this
- **Internet connection** - For competitor analysis

That's it! If you already use Claude Code CLI, you're ready.

## Quick Start

```bash
# Install
pip install ccux

# Initialize (one-time setup)
ccux init

# Generate your first landing page
ccux gen --desc "AI-powered project management tool"
```

Your professional landing page is ready in `output/landing-page/`.

## Development Installation

```bash
# Clone and setup
git clone https://github.com/thisisharsh7/claude-cli-wrapper.git
cd claude-cli-wrapper

# Install dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .

# Initialize and test
ccux init
ccux gen --desc "Your product description"
```

## Key Commands

```bash
# Generate page
ccux gen --desc "Product description" --theme brutalist

# Regenerate sections
ccux regen --section hero,pricing

# Change theme
ccux theme minimal

# Control animations
ccux animate off  # Better performance
ccux animate on   # Enable animations

# Get help
ccux help
```

## Important Links

- **PyPI Package**: [https://pypi.org/project/ccux/](https://pypi.org/project/ccux/)
- **GitHub Repository**: [https://github.com/thisisharsh7/claude-cli-wrapper](https://github.com/thisisharsh7/claude-cli-wrapper)
- **Claude Code CLI**: [https://claude.ai/code](https://claude.ai/code)
- **Theme Guide**: [THEME_IMPLEMENTATION_GUIDE.md](THEME_IMPLEMENTATION_GUIDE.md)

## Available Themes

**Core**: minimal, brutalist, playful, corporate  
**Modern**: morphism, animated, terminal, aesthetic  
**Additional**: dark, vibrant, sustainable, data, illustrated

Run `ccux help themes` to see detailed descriptions.

## Preview Pages

```bash
# Start local server
python -m http.server -d output/landing-page 3000
# Open http://localhost:3000
```

## Get Help

- Run `ccux help` for comprehensive guidance
- Use `ccux help quickstart` for step-by-step setup
- Check GitHub issues for community support

## Contributing & Support

**⭐ Star this project** if you find it useful! It helps others discover CCUX.

**🐛 Found a bug or want a feature?** Open an issue in the [GitHub Issues](https://github.com/thisisharsh7/claude-cli-wrapper/issues) tab.

---

Made with ❤️ for developers who live in the terminal.