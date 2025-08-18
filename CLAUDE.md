# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CCUI (Claude Code UI Generator) is a sophisticated Python CLI tool that automatically generates conversion-optimized frontend landing pages using professional UX design thinking methodology. The tool leverages Claude AI to implement a comprehensive 10-phase design process used by professional UX agencies, combining automated competitor analysis with strategic design decisions.

### What This Project Does

1. **Automated Competitive Research**: Discovers 3 competitor websites and design showcases from Behance/Dribbble
2. **Professional Design Process**: Implements a 10-phase UX methodology including product understanding, user research, wireframing, and visual design
3. **Screenshot Analysis**: Uses Playwright to capture and analyze competitor landing pages for design patterns
4. **Strategic Copy Generation**: Creates conversion-optimized copy based on user research and competitive analysis  
5. **Code Generation**: Outputs production-ready HTML or React components with TailwindCSS styling
6. **Real-time Streaming**: Shows Claude's design thinking process in real-time with progress indicators

### Key Features

- **Automated Reference Discovery**: Finds competitors and design inspiration automatically using Claude AI
- **Multi-site Competitive Analysis**: Captures and analyzes 3 reference sites with screenshot comparison
- **Professional Design Process**: 10-phase methodology including empathy mapping, user journeys, and conversion optimization
- **Conversion-Optimized Copy**: Strategic messaging based on competitive analysis and user research
- **Multiple Output Formats**: Generates HTML with inline TailwindCSS or React components with ESM imports
- **Real-time Progress**: Streams Claude output live with rich terminal formatting and progress indicators
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

#### Quick Generation (Simple Mode)
```bash
# Fast generation without design thinking process
ccui gen --desc "AI-powered project management tool" --no-design-thinking
```

#### Comprehensive Analysis (Default Mode)
```bash
# Full 10-phase design thinking process with automated competitor discovery (3 references)
ccui gen --desc "AI-powered project management tool"
```

#### Custom Reference with Design Thinking
```bash
# Use specific reference URL as starting point, finds additional competitors
ccui gen --url https://linear.app --desc "AI-powered project management tool"
```

#### Advanced Options
```bash
# Generate React component instead of HTML
ccui gen --desc "Product description" --framework react

# Use specific design theme
ccui gen --desc "Product description" --theme brutalist

# Combine multiple options
ccui gen --desc "Product" --framework react --theme corporate --no-design-thinking
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
   - Main entry point with Typer-based commands (`init`, `gen`)
   - Handles command-line arguments and configuration loading
   - Orchestrates the entire automated design thinking workflow
   - Features robust subprocess handling with real-time output streaming

2. **Web Scraping** (`src/ccui/scrape.py`)
   - Uses Playwright to capture reference website screenshots
   - Handles cookie consent banners and modals automatically
   - Supports multiple reference capture for competitive analysis
   - Features comprehensive error handling and fallback strategies
   - Optimized resource blocking for faster page loads

3. **Prompt Templates** (`src/ccui/prompt_templates.py`)
   - Implements 10-phase professional design thinking workflow
   - Each phase has specialized prompts for structured outputs
   - Incorporates UI/UX best practices (Fitts's Law, Hick's Law, accessibility)
   - Supports both automated and simple generation modes

### Design Thinking Workflow (Default Mode)

The tool implements a comprehensive 10-phase design process:

1. **Reference Discovery** - Auto-finds 3 competitor sites + design showcases
2. **Deep Product Understanding** - Value proposition analysis and press release drafting
3. **Competitive Landscape Analysis** - Screenshot analysis for patterns and weaknesses
4. **Define Audience & Goals** - User research and persona development
5. **Draft Site Flow** - Journey mapping and lean sitemap creation
6. **Write Content First** - Strategic copy before visual design
7. **Rough Wireframes** - Mobile-first layout validation
8. **Visual Identity & Design System** - Typography, colors, WCAG compliance
9. **High-Fidelity Design** - Interactive elements and polish
10. **Final Copy Generation** - Professional conversion copy
11. **Implementation** - Code generation with strategic design decisions

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
- **Professional Design Process**: 10-phase methodology used by UX agencies
- **Conversion-Optimized Copy**: Strategic messaging based on user research
- **Real-time Streaming**: Claude output streams live to user with progress indication
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

## Development Notes

### Code Style
- The codebase currently contains emoji characters in print statements and CLI output
- Emojis are used for visual progress indicators and user feedback in the terminal
- These can be removed by replacing emoji characters with text-based alternatives
- All emoji usage is contained within the Rich formatting system for terminal output

### Implementation Details

The tool implements a sophisticated workflow:

1. **Reference Discovery Phase**: Uses Claude AI to find 3 competitor websites and design showcases
2. **Screenshot Capture**: Playwright automation captures competitor landing pages with error handling
3. **Design Thinking Process**: 10-phase methodology including:
   - Deep product understanding and value proposition analysis
   - Competitive landscape analysis of captured screenshots
   - User empathy mapping and persona development
   - Site flow and journey mapping
   - Content-first copywriting approach
   - Mobile-first wireframing validation
   - Visual identity and design system creation
   - High-fidelity design with interactive elements
   - Final copy refinement and polish
   - Strategic implementation with conversion optimization

4. **Code Generation**: Produces production-ready HTML or React components with:
   - Semantic HTML structure
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
├── prompt_templates.py  # 10-phase design thinking prompts
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


