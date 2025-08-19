# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CCUI (Claude Code UI Generator) is a sophisticated Python CLI tool that automatically generates conversion-optimized frontend landing pages using professional UX design thinking methodology. The tool leverages Claude AI to implement a comprehensive 12-phase design process used by professional UX agencies, combining automated competitor analysis with strategic design decisions.

### What This Project Does

1. **Automated Competitive Research**: Discovers 3 competitor websites and design showcases
2. **Professional Design Process**: Implements a 12-phase UX methodology including product understanding, user research, wireframing, and visual design
3. **Screenshot Analysis**: Uses Playwright to capture and analyze competitor landing pages for design patterns
4. **Strategic Copy Generation**: Creates conversion-optimized copy based on user research and competitive analysis  
5. **Code Generation**: Outputs production-ready HTML or React components with TailwindCSS styling
6. **Real-time Streaming**: Shows Claude's design thinking process in real-time with progress indicators
7. **Section Regeneration**: Allows regenerating specific sections of existing landing pages

### Key Features

- **Automated Reference Discovery**: Finds competitors and design inspiration automatically using Claude AI
- **Multi-site Competitive Analysis**: Captures and analyzes 3 reference sites with screenshot comparison
- **Professional Design Process**: 12-phase methodology including empathy mapping, user journeys, and conversion optimization
- **Conversion-Optimized Copy**: Strategic messaging based on competitive analysis and user research
- **Multiple Output Formats**: Generates HTML with inline TailwindCSS or React components with ESM imports
- **Real-time Progress**: Streams Claude output live with rich terminal formatting and progress indicators
- **Section Regeneration**: Regenerate specific sections (hero, features, pricing, etc.) of existing landing pages
- **Interactive Mode**: Guided setup for users without command-line arguments
- **Robust Error Handling**: Timeout protection, graceful fallbacks, and comprehensive error reporting
- **Cross-platform Support**: Works on Windows, macOS, and Linux
- **Memory Efficient**: Cleanup between captures for large reference sets

## How to Run

### Prerequisites
- Python 3.9 or higher
- Claude CLI tool installed and configured

### Setup and Installation
```bash
# Clone the repository (if applicable)
# cd into the project directory

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install package in development mode
pip install -e .

# Install Playwright browsers (required for screenshot capture)
ccui init
```

### Basic Usage

#### Interactive Mode (Recommended)
```bash
# Guided setup - prompts for all options
ccui gen
```

#### Quick Generation (Simple Mode)
```bash
# Fast generation without design thinking process
ccui gen --desc "AI-powered project management tool" --no-design-thinking
```

#### Comprehensive Analysis (Default Mode)
```bash
# Full 12-phase design thinking process with automated competitor discovery (3 references)
ccui gen --desc "AI-powered project management tool"
```

#### Custom Reference with Design Thinking
```bash
# Use specific reference URL as starting point, finds additional competitors
ccui gen --url https://linear.app --desc "AI-powered project management tool"

# Use multiple reference URLs (up to 3 will be used)
ccui gen --url https://linear.app --url https://notion.so --desc "AI-powered project management tool"
```

ccui gen --url https://strapi.io --url https://discord.com --desc "Journify makes self-reflection effortless. Instead of long, overwhelming diary entries, Journify turns journaling into a fast, 5-minute habit powered by AI prompts that feel personal and meaningful. Capture your thoughts on the go with voice journaling in under 3 minutes, break free from writer’s block with customizable templates, and instantly find past memories with smart search & insights. It’s not just about writing—it’s about building your story, one moment at a time. With community features, you can connect with others, celebrate milestones, and stay inspired along the way. Whether you want clarity, growth, or just a simple way to track your life, Journify helps you do it—stress-free, hands-free, every day." --theme brutalist

#### Advanced Options
```bash
# Generate React component instead of HTML
ccui gen --desc "Product description" --framework react

# Use specific design theme
ccui gen --desc "Product description" --theme brutalist

# Combine multiple options
ccui gen --desc "Product" --framework react --theme corporate --no-design-thinking

# Load description from file
ccui gen --desc-file product_description.txt
```

#### Regenerate Sections
```bash
# Regenerate specific sections
ccui regen --section hero
ccui regen --section hero,features
ccui regen --all

# Regenerate with custom description
ccui regen --section hero --desc "Updated product description"
```

#### Change Theme
```bash
# Change the design theme of existing landing page
ccui theme brutalist
ccui theme playful
ccui theme corporate
ccui theme minimal

# Change theme for specific file
ccui theme brutalist --file custom/page.html
```

### Preview Generated Output
```bash
# Start local server to preview the generated landing page
python -m http.server -d output/landing-page 3000

# Then open http://localhost:3000 in your browser
```

### Available Themes
- `minimal`: Clean, minimal design with subtle styling
- `brutalist`: Bold, high-contrast design with strong visual elements  
- `playful`: Colorful, engaging design with rounded elements
- `corporate`: Professional, business-focused design

### Available Frameworks
- `html`: Single HTML file with inline TailwindCSS (default)
- `react`: React component with ESM imports

## Architecture Overview

This is a Python CLI tool (`ccui`) that wraps Claude Code to automatically generate conversion-optimized frontend landing pages using professional design thinking methodology.

### Core Components

1. **CLI Interface** (`src/ccui/cli.py`)
   - Main entry point with Typer-based commands (`init`, `gen`, `regen`)
   - Handles command-line arguments and configuration loading
   - Orchestrates the entire automated design thinking workflow
   - Features robust subprocess handling with real-time output streaming
   - Interactive mode for guided user experience
   - Section regeneration capabilities

2. **Web Scraping** (`src/ccui/scrape.py` & `src/ccui/scrape_simple.py`)
   - Uses Playwright to capture reference website screenshots
   - Handles cookie consent banners and modals automatically
   - Supports multiple reference capture for competitive analysis
   - Features comprehensive error handling and fallback strategies
   - Optimized resource blocking for faster page loads
   - Simple and advanced scraping modes

3. **Prompt Templates** (`src/ccui/prompt_templates.py`)
   - Implements 12-phase professional design thinking workflow
   - Each phase has specialized prompts for structured outputs
   - Incorporates UI/UX best practices (Fitts's Law, Hick's Law, accessibility)
   - Supports both automated and simple generation modes
   - Section regeneration prompts

### Design Thinking Workflow (Default Mode)

The tool implements a comprehensive 12-phase design process:

1. **Reference Discovery** - Auto-finds 3 competitor sites using Claude AI
2. **Screenshot Capture** - Playwright automation captures competitor landing pages
3. **Deep Product Understanding** - Value proposition analysis and problem identification
4. **Competitive UX Analysis** - Screenshot analysis for patterns and weaknesses
5. **User Empathy Mapping** - User research and persona development
6. **Define Site Flow** - Journey mapping and lean sitemap creation
7. **Content Strategy** - Strategic copy development before visual design
8. **Wireframe Validation** - Mobile-first layout validation
9. **Design System** - Typography, colors, WCAG compliance
10. **High-Fidelity Design** - Interactive elements and polish
11. **Final Copy Generation** - Professional conversion copy refinement
12. **Implementation** - Code generation with strategic design decisions

### Configuration

Optional `ccui.yaml` config file in working directory:
```yaml
framework: html    # html or react
theme: minimal     # minimal|brutalist|playful|corporate
sections: [hero, features, pricing, footer]
claude_cmd: claude
output_dir: output/landing-page
```

### Key Features

- **Automated Reference Discovery**: Finds competitors and design inspiration automatically
- **Multi-site Competitive Analysis**: Captures and analyzes 3 reference sites
- **Professional Design Process**: 12-phase methodology used by UX agencies
- **Conversion-Optimized Copy**: Strategic messaging based on user research
- **Real-time Streaming**: Claude output streams live to user with progress indication
- **Section Regeneration**: Update specific sections without rebuilding entire page
- **Interactive Mode**: Guided setup for all options and preferences
- **Robust Error Handling**: Timeout protection, graceful fallbacks, comprehensive error reporting
- **Cross-platform**: Works on Windows, macOS, Linux
- **Thread-safe I/O**: Non-blocking stdout/stderr handling
- **Memory Efficient**: Cleanup between captures for large reference sets

### Dependencies

- **Typer** (≥0.12.0): CLI framework with rich terminal features
- **Rich** (≥13.7.0): Terminal formatting, progress bars, and user interaction
- **Playwright** (≥1.45.0): Web scraping and screenshot capture with Chromium
- **PyYAML** (≥6.0.1): Configuration file parsing

### Output Structure

- **HTML mode**: Single `index.html` file with inline TailwindCSS
- **React mode**: `App.jsx` component + `index.html` shell with ESM imports
- **Both modes**: SEO-optimized HTML with meta tags, schema markup, and performance optimizations
- **Screenshots**: Saved as `.jpg` files in output directory for debugging/reference

### Claude CLI Integration

Uses `--print` flag with prompt content as argument (not stdin redirection):
```bash
claude --print "prompt content here"
```

Features:
- Real-time output streaming via threading
- 5-minute timeout protection per Claude invocation
- Usage statistics parsing from stderr
- Proper error capture and user-friendly error messages
- Keyboard interrupt handling with graceful cleanup

### Usage Patterns

**Interactive Mode (Recommended)**:
```bash
ccui gen
# Guided setup with prompts for all options
```

**Quick Generation (Simple Mode)**:
```bash
ccui gen --desc "AI-powered project management tool" --no-design-thinking
```

**Comprehensive Analysis (Default)**:
```bash
ccui gen --desc "AI-powered project management tool"
# Automatically finds competitors, analyzes 3 sites, runs full design process
```

**Custom Reference with Design Thinking**:
```bash
ccui gen --url https://linear.app --desc "AI-powered project management tool"
# Uses provided URL as primary reference, finds additional competitors
```

**Section Regeneration**:
```bash
ccui regen --section hero,features
# Regenerates specific sections of existing landing page
```

## Development Notes

### Code Style
- The codebase currently contains emoji characters in print statements and CLI output
- Emojis are used for visual progress indicators and user feedback in the terminal
- These can be removed by replacing emoji characters with text-based alternatives
- All emoji usage is contained within the Rich formatting system for terminal output

### Implementation Details

The tool implements a sophisticated workflow:

1. **Reference Discovery Phase**: Uses Claude AI to find 3 competitor websites
2. **Screenshot Capture**: Playwright automation captures competitor landing pages with error handling  
3. **Design Thinking Process**: 12-phase methodology including:
   - Deep product understanding and value proposition analysis
   - Competitive UX analysis of captured screenshots
   - User empathy mapping and persona development
   - Site flow and journey mapping
   - Content strategy development
   - Mobile-first wireframing validation
   - Visual identity and design system creation
   - High-fidelity design with interactive elements
   - Final copy refinement and polish
   - Strategic implementation with conversion optimization

4. **Section Management**: Advanced section handling including:
   - HTML comment markers for section identification
   - Individual section regeneration without affecting other parts
   - Context preservation during section updates
   - Design analysis tracking for regeneration history

5. **Code Generation**: Produces production-ready HTML or React components with:
   - Semantic HTML structure with section markers
   - TailwindCSS styling with custom design system
   - SEO optimization with meta tags and schema markup
   - Responsive design patterns
   - Accessibility compliance (WCAG guidelines)
   - Performance optimizations

### File Structure
```
src/ccui/
├── __init__.py          # Package initialization
├── __main__.py          # Entry point for python -m ccui
├── cli.py              # Main CLI interface with Typer commands
├── prompt_templates.py  # 12-phase design thinking prompts
├── scrape.py           # Advanced Playwright web scraping
└── scrape_simple.py    # Simplified screenshot capture
```

### Configuration Options

Create optional `ccui.yaml` in your working directory:
```yaml
framework: html    # html or react
theme: minimal     # minimal|brutalist|playful|corporate
sections: [hero, features, pricing, footer]
claude_cmd: claude
output_dir: output/landing-page
```


