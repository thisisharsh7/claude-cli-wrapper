# CCUX — Claude Code UI Generator

A sophisticated Python CLI tool that automatically generates conversion-optimized frontend landing pages using professional UX design thinking methodology. Leverages Claude AI to implement a comprehensive 12-phase design process used by professional UX agencies.

## ✨ What it does

1. **Automated Competitive Research**: Discovers 3 competitor websites and design showcases
2. **Screenshot Analysis**: Captures and analyzes competitor landing pages for design patterns
3. **Professional Design Process**: 12-phase UX methodology including user research, wireframing, and visual design
4. **Strategic Copy Generation**: Creates conversion-optimized copy based on competitive analysis
5. **Code Generation**: Outputs production-ready HTML or React components with TailwindCSS styling
6. **Section Management**: Regenerate specific sections or change themes without rebuilding

## 🧰 Prerequisites

- Python 3.9 or higher
- Claude CLI tool installed and configured
- macOS/Linux/Windows (WSL recommended for Windows)

## 🚀 Setup and Installation

### Install from PyPI (Recommended)

```bash
# Install directly from PyPI
pip install ccux

# Initialize Playwright browsers (required for screenshot capture)
ccux init

# Generate your first landing page
ccux gen --desc "AI-powered project management tool"
```

**📦 PyPI Package**: [https://pypi.org/project/ccux/](https://pypi.org/project/ccux/)

**🐙 GitHub Repository**: [https://github.com/thisisharsh7/claude-cli-wrapper](https://github.com/thisisharsh7/claude-cli-wrapper)

### Development Installation

```bash
# 1. Clone the repository
git clone https://github.com/thisisharsh7/claude-cli-wrapper.git
cd claude-cli-wrapper

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install package in development mode
pip install -e .

# 4. Initialize Playwright browsers (required for screenshot capture)
ccux init

# 5. Generate your first landing page
ccux gen --desc "AI-powered project management tool"
```

## 📋 Commands

### `ccux init`
Initialize CCUX by installing Playwright browsers.

**Usage:** `ccux init`

**Example:**
```bash
ccux init
```

---

### `ccux gen`
Generate a conversion-optimized landing page using AI-powered design thinking.

**Usage:** `ccux gen [OPTIONS]`

**Options:**
- `--desc, -d TEXT`: Product description
- `--desc-file FILE`: Load description from text file
- `--url, -u URL`: Reference URLs (can use multiple times, max 3)
- `--framework, -f [html|react]`: Output framework (default: html)
- `--theme, -t [minimal|brutalist|playful|corporate|morphism|animated|terminal|aesthetic|dark|vibrant|sustainable|data|illustrated]`: Design theme (default: minimal)
- `--no-design-thinking`: Skip design thinking for faster generation
- `--output, -o DIR`: Output directory

**Examples:**
```bash
# Interactive mode (recommended)
ccux gen

# Quick generation without design thinking
ccux gen --desc "AI project management tool" --no-design-thinking

# Full analysis with custom references and theme
ccux gen --url https://linear.app --desc "Project management tool" --theme brutalist

# Load from file with React output
ccux gen --desc-file product_desc.txt --framework react --theme corporate
```

---

### `ccux regen`
Regenerate specific sections of an existing landing page.

**Usage:** `ccux regen [OPTIONS]`

**Options:**
- `--section, -s TEXT`: Sections to regenerate (comma-separated)
- `--all`: Regenerate all sections
- `--desc, -d TEXT`: Product description
- `--file, -f FILE`: Path to landing page file
- `--output, -o DIR`: Output directory

**Examples:**
```bash
# Regenerate hero section
ccux regen --section hero

# Regenerate multiple sections
ccux regen --section hero,features,pricing

# Regenerate all sections
ccux regen --all
```

---

### `ccux theme`
Change the design theme of an existing landing page.

**Usage:** `ccux theme THEME [OPTIONS]`

**Options:**
- `--file, -f FILE`: Path to landing page file
- `--output, -o DIR`: Output directory

**Examples:**
```bash
# Change to brutalist theme
ccux theme brutalist

# Change theme for specific file
ccux theme playful --file custom/page.html
```

---

### `ccux help`
Show comprehensive help and usage examples with different topics.

**Usage:** `ccux help [TOPIC]`

**Topics:**
- `quickstart`: Complete getting started guide
- `themes`: All available design themes with descriptions
- `examples`: Common usage patterns and commands
- `workflows`: Step-by-step workflows for different scenarios

**Examples:**
```bash
# Show main help menu with command overview
ccux help

# Get detailed quickstart guide
ccux help quickstart

# Browse all available themes
ccux help themes

# View common usage examples
ccux help examples

# Learn step-by-step workflows
ccux help workflows
```

---

### `ccux version`
Show version information.

**Usage:** `ccux version`

**Example:**
```bash
ccux version
```

## 🎨 Themes

### Core Themes
- `minimal`: Clean, content-focused design following Dieter Rams' principles
- `brutalist`: Raw, honest design inspired by Brutalist architecture
- `playful`: Joyful, approachable design with organic shapes and vibrant colors
- `corporate`: Traditional, trustworthy design following business conventions

### Modern Design Theory Themes
- `morphism`: Soft, tactile design combining neumorphism and glassmorphism
- `animated`: Motion-first design where animation drives user experience
- `terminal`: CLI-inspired aesthetic for developers and tech enthusiasts
- `aesthetic`: Retro-futuristic Y2K, vaporwave, and cyber aesthetics

### Additional Theme Options
- `dark`: Modern dark theme optimized for contrast and reduced eye strain
- `vibrant`: Colorful, dopamine-rich design that energizes user interactions
- `sustainable`: Nature-inspired design emphasizing eco-conscious branding
- `data`: Information-dense design optimized for dashboards and analytics
- `illustrated`: Hand-drawn, custom illustration-driven design for humanized experiences

📖 **See [THEME_IMPLEMENTATION_GUIDE.md](THEME_IMPLEMENTATION_GUIDE.md) for detailed specifications and usage guidelines**

## 🛠️ Frameworks

- `html`: Single HTML file with inline TailwindCSS (default)
- `react`: React component with ESM imports

## ⚙️ Configuration

Create optional `ccux.yaml` in your working directory:

```yaml
framework: html    # html or react
theme: minimal     # minimal|brutalist|playful|corporate|morphism|animated|terminal|aesthetic|dark|vibrant|sustainable|data|illustrated
sections: [hero, features, pricing, footer]
claude_cmd: claude
output_dir: output/landing-page
```

CLI flags always override config values.

## 🔬 Design Thinking Process

When not using `--no-design-thinking`, CCUX implements a 12-phase professional UX methodology:

1. **Reference Discovery** - Auto-finds competitors using Claude AI
2. **Screenshot Capture** - Captures competitor landing pages
3. **Product Understanding** - Analyzes value proposition
4. **UX Analysis** - Identifies design patterns and opportunities
5. **User Research** - Creates empathy maps and personas
6. **Site Flow** - Maps user journeys and information architecture
7. **Content Strategy** - Develops strategic messaging
8. **Wireframing** - Validates mobile-first layouts
9. **Design System** - Creates typography, colors, and components
10. **High-Fidelity Design** - Adds interactive elements and polish
11. **Copy Generation** - Refines conversion-optimized copy
12. **Implementation** - Generates production-ready code

## 🌐 Preview Generated Pages

```bash
# Start local server to preview
python -m http.server -d output/landing-page 3000

# Or with Node.js
npx serve output/landing-page -p 3000

# Then open http://localhost:3000 in your browser
```

## 💡 Usage Tips

- **Get Help**: Run `ccux help` for comprehensive guidance and examples
- **Long Descriptions**: Files >100 words are automatically summarized to optimize processing
- **Reference Limit**: Maximum 3 reference URLs for optimal performance
- **Interactive Mode**: Run `ccux gen` without options for guided setup
- **Section Updates**: Use `ccux regen` to update specific parts without rebuilding
- **Theme Changes**: Use `ccux theme` to redesign with preserved content

## 🆘 Troubleshooting

- **Claude CLI Issues**: Ensure `claude` command is accessible on PATH
- **Playwright Errors**: Run `ccux init` to install required browsers
- **Screenshot Failures**: Tool continues without screenshots if capture fails
- **Generation Errors**: Try `--no-design-thinking` for simpler processing
- **Memory Issues**: Tool automatically cleans up between operations

## 🏗️ Architecture

- **CLI Interface**: Typer-based with rich terminal formatting
- **Web Scraping**: Playwright automation with error handling
- **AI Integration**: Claude CLI with timeout protection and usage tracking
- **Output Management**: Structured HTML/React with section markers
- **Configuration**: YAML-based with CLI override support