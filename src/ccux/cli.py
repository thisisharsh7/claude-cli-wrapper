#!/usr/bin/env python3
"""
CCUX - Claude Code UI Generator CLI
A sophisticated Python CLI tool that automatically generates conversion-optimized 
frontend landing pages using professional UX design thinking methodology.
"""

import os
import sys
import json
import time
import threading
import subprocess
import signal
import re
import importlib.metadata
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse

import typer
import yaml
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.status import Status
from rich.table import Table
from rich.prompt import Prompt, Confirm
from .scrape import capture_multiple_references
from .scrape_simple import capture
from .theme_specifications import (
    THEME_SPECIFICATIONS,
    get_theme_choices,
    get_theme_description,
    get_theme_design_system_rules,
    detect_theme_from_content
)
from .prompt_templates import (
    reference_discovery_prompt,
    deep_product_understanding_prompt,
    ux_analysis_prompt,
    empathize_prompt,
    define_prompt,
    ideate_prompt,
    wireframe_prompt,
    design_system_prompt,
    high_fidelity_design_prompt,
    prototype_prompt,
    implementation_prompt,
    landing_prompt,
    regeneration_prompt
)

app = typer.Typer(
    name="ccux",
    help="Claude Code UI Generator - Automatically generate conversion-optimized landing pages",
    no_args_is_help=True,
    rich_markup_mode="rich"
)
console = Console()

# Global variables for signal handling
current_subprocess = None
current_progress = None

def signal_handler(signum, frame):
    """Handle keyboard interrupts gracefully"""
    global current_subprocess, current_progress
    
    console.print("\n[yellow]⚠️  Interrupt received, cleaning up...[/yellow]")
    
    if current_subprocess:
        try:
            current_subprocess.terminate()
            current_subprocess.wait(timeout=5)
        except:
            try:
                current_subprocess.kill()
            except:
                pass
    
    if current_progress:
        current_progress.stop()
    
    console.print("[red]❌ Operation cancelled by user[/red]")
    sys.exit(1)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

class Config:
    """Configuration management for CCUX"""
    
    def __init__(self, config_path: str = "ccux.yaml"):
        self.config_path = config_path
        self.defaults = {
            'framework': 'html',
            'theme': 'minimal',
            'sections': ['hero', 'features', 'pricing', 'footer'],
            'claude_cmd': 'claude',
            'output_dir': 'output/landing-page'
        }
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f) or {}
                # Merge with defaults
                return {**self.defaults, **config}
            except Exception as e:
                console.print(f"[yellow]⚠️  Error loading config: {e}. Using defaults.[/yellow]")
        
        return self.defaults.copy()
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)

def run_claude_with_progress(prompt: str, description: str = "Claude Code is thinking...") -> tuple[str, Dict[str, Any]]:
    """Run Claude CLI with real-time progress indication and usage tracking"""
    global current_subprocess, current_progress
    
    config = Config()
    claude_cmd = config.get('claude_cmd', 'claude')
    
    # Prepare Claude command
    cmd = [claude_cmd, '--print', prompt]
    
    output_lines = []
    stderr_lines = []
    usage_stats = {}
    
    def read_stream(stream, lines_list):
        """Read from stream and collect output"""
        try:
            for line in iter(stream.readline, ''):
                if line:
                    lines_list.append(line.strip())
        except:
            pass
    
    with Progress(
        SpinnerColumn(),
        TextColumn(f"[bold blue]{description}"),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        current_progress = progress
        task = progress.add_task("Processing", total=None)
        
        try:
            # Start Claude process
            current_subprocess = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(
                target=read_stream, 
                args=(current_subprocess.stdout, output_lines)
            )
            stderr_thread = threading.Thread(
                target=read_stream, 
                args=(current_subprocess.stderr, stderr_lines)
            )
            
            stdout_thread.start()
            stderr_thread.start()
            
            # Wait for process with timeout (5 minutes)
            try:
                current_subprocess.wait(timeout=300)
            except subprocess.TimeoutExpired:
                current_subprocess.kill()
                raise Exception("Claude Code timed out after 5 minutes")
            
            # Wait for threads to finish
            stdout_thread.join(timeout=2)
            stderr_thread.join(timeout=2)
            
            if current_subprocess.returncode != 0:
                error_msg = '\n'.join(stderr_lines) if stderr_lines else "Claude Code execution failed"
                raise Exception(f"Claude Code failed: {error_msg}")
            
            # Parse usage statistics from stderr
            for line in stderr_lines:
                if "Input tokens:" in line:
                    try:
                        usage_stats['input_tokens'] = int(line.split(':')[1].strip())
                    except:
                        pass
                elif "Output tokens:" in line:
                    try:
                        usage_stats['output_tokens'] = int(line.split(':')[1].strip())
                    except:
                        pass
                elif "Cost:" in line or "$" in line:
                    try:
                        # Extract cost from line
                        import re
                        cost_match = re.search(r'\$([0-9]+\.?[0-9]*)', line)
                        if cost_match:
                            usage_stats['cost'] = float(cost_match.group(1))
                    except:
                        pass
            
        except Exception as e:
            current_progress = None
            current_subprocess = None
            raise e
        
        finally:
            current_progress = None
            current_subprocess = None
    
    # Combine output
    full_output = '\n'.join(output_lines)
    
    # Show usage statistics if available
    if usage_stats:
        console.print("\n[bold cyan]📊 Usage Statistics:[/bold cyan]")
        if 'input_tokens' in usage_stats:
            console.print(f"  Input tokens: [green]{usage_stats['input_tokens']:,}[/green]")
        if 'output_tokens' in usage_stats:
            console.print(f"  Output tokens: [green]{usage_stats['output_tokens']:,}[/green]")
        if 'cost' in usage_stats:
            console.print(f"  Estimated cost: [green]${usage_stats['cost']:.4f}[/green]")
        console.print()
    
    return full_output, usage_stats

def summarize_long_description(desc: str) -> str:
    """Summarize product description if longer than 300 words"""
    word_count = len(desc.split())
    
    if word_count <= 300:
        return desc
    
    console.print(f"[yellow]📝 Description has {word_count} words, summarizing to 200-300 words...[/yellow]")
    
    summarization_prompt = f"""You are given a long product description. 
If the text is fewer than 300 words, return it unchanged. 
If it is longer than 300 words, summarize it into 200–300 words while keeping only the most important details:

- Problem it solves
- Target user
- Unique differentiator
- Best feature

Make the summary clear, concise, and business-oriented. 
Do not include filler or marketing fluff. 
Output only the final text (no explanations).

Product description to summarize:
{desc}"""
    
    try:
        summary, _ = run_claude_with_progress(summarization_prompt, "Summarizing description...")
        return summary.strip()
    except Exception as e:
        console.print(f"[yellow]⚠️  Failed to summarize description: {e}. Using original.[/yellow]")
        return desc


def validate_html_output(html_content: str) -> bool:
    """Validate that HTML output is not an error message"""
    if not html_content or len(html_content.strip()) < 50:
        return False
    
    # Check for common error patterns first
    error_patterns = [
        "execution error",
        "error occurred", 
        "failed to generate",
        "timeout",
        "claude code failed"
    ]
    
    content_lower = html_content.lower()
    for pattern in error_patterns:
        if pattern in content_lower:
            return False
    
    # Check for basic HTML indicators (more lenient)
    html_indicators = [
        "<!doctype html",
        "<html",
        "<head>",
        "<body>",
        "<div",
        "<section",
        "tailwindcss"
    ]
    
    # Must have at least 2 HTML indicators
    found_indicators = 0
    for indicator in html_indicators:
        if indicator in content_lower:
            found_indicators += 1
    
    return found_indicators >= 2

def extract_brand_name(description: str) -> str:
    """Extract brand/product name from description for display (max 10 words)"""
    import re
    
    # Common patterns for product names
    patterns = [
        r'^([A-Z][A-Za-z0-9\s]{1,30})\s*[-–—]\s*',  # "ProductName - description"
        r'^([A-Z][A-Za-z0-9\s]{1,30})\s*\([^)]+\)',  # "ProductName (description)"  
        r'^([A-Z][A-Za-z0-9\s]{1,30})\s+is\s+',      # "ProductName is a..."
        r'^([A-Z][A-Za-z0-9\s]{1,30})\s*:\s*',       # "ProductName: description"
        r'^([A-Z][A-Za-z0-9\s]{1,30})\s*,\s*',       # "ProductName, description"
    ]
    
    for pattern in patterns:
        match = re.match(pattern, description.strip())
        if match:
            brand = match.group(1).strip()
            if len(brand.split()) <= 10:
                return brand
    
    # Enhanced fallback: look for capitalized words that might be brand names
    words = description.strip().split()
    
    # Look for sequences of capitalized words (likely brand names)
    brand_candidates = []
    current_brand = []
    
    for word in words[:15]:  # Check first 15 words only
        if word[0].isupper() or word.isdigit() or any(c.isupper() for c in word):
            current_brand.append(word)
        else:
            if current_brand and len(current_brand) <= 3:  # Max 3 words for brand name
                brand_candidates.append(' '.join(current_brand))
            current_brand = []
    
    # Add final candidate if exists
    if current_brand and len(current_brand) <= 3:
        brand_candidates.append(' '.join(current_brand))
    
    # Return the first reasonable brand candidate
    for candidate in brand_candidates:
        if len(candidate.split()) <= 4 and len(candidate) > 1:
            return candidate
    
    # Final fallback: first 8 words with ellipsis
    return ' '.join(words[:8]) + ('...' if len(words) > 8 else '')

def safe_json_parse(text: str) -> Dict[str, Any]:
    """Safely parse JSON from Claude output"""
    try:
        # Try to extract JSON from code blocks
        lines = text.strip().split('\n')
        json_lines = []
        in_json = False
        
        for line in lines:
            if line.strip().startswith('```json') or line.strip().startswith('```'):
                in_json = True
                continue
            elif line.strip() == '```' and in_json:
                break
            elif in_json:
                json_lines.append(line)
            elif line.strip().startswith('{'):
                # Direct JSON start
                json_lines = [line]
                in_json = True
            elif in_json and line.strip().endswith('}'):
                json_lines.append(line)
                break
            elif in_json:
                json_lines.append(line)
        
        if json_lines:
            json_text = '\n'.join(json_lines)
            return json.loads(json_text)
        
        # Fallback: try parsing entire text
        return json.loads(text)
        
    except Exception:
        return {}

def strip_code_blocks(text: str) -> str:
    """Strip markdown code blocks from Claude output"""
    lines = text.strip().split('\n')
    result_lines = []
    in_code_block = False
    
    for line in lines:
        # Check for start of code block
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        # If not in code block, include the line
        if not in_code_block:
            result_lines.append(line)
    
    return '\n'.join(result_lines).strip()

def find_landing_page_files(output_dir: str = None) -> Dict[str, str]:
    """Find existing landing page files in common locations"""
    if output_dir is None:
        output_dir = "output/landing-page"
    
    search_paths = [
        output_dir,
        ".",
        "dist",
        "build",
        "public"
    ]
    
    found_files = {}
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
            
        # Look for HTML files
        for file_name in ['index.html', 'landing.html', 'page.html']:
            file_path = os.path.join(search_path, file_name)
            if os.path.exists(file_path):
                found_files['html'] = file_path
                break
                
        # Look for React files
        for file_name in ['App.jsx', 'Landing.jsx', 'Page.jsx']:
            file_path = os.path.join(search_path, file_name)
            if os.path.exists(file_path):
                found_files['react'] = file_path
                break
    
    return found_files

def extract_page_context(file_path: str) -> Dict[str, Any]:
    """Extract metadata and context from existing landing page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        context = {
            'framework': 'react' if file_path.endswith('.jsx') else 'html',
            'sections': [],
            'theme': 'minimal',  # Default
            'other_sections': []
        }
        
        # Extract sections using markers
        section_patterns = [
            r'<!-- START: (\w+) -->(.*?)<!-- END: \1 -->',
            r'<!-- SECTION: (\w+) -->(.*?)<!-- END SECTION: \1 -->'
        ]
        
        sections = []
        for pattern in section_patterns:
            found = re.findall(pattern, content, re.DOTALL)
            sections.extend(found)
        
        for section_name, _ in sections:
            context['sections'].append(section_name)
        
        # Enhanced theme detection using new system
        context['theme'] = detect_theme_from_content(content)
            
        return context
        
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not extract context from {file_path}: {e}[/yellow]")
        return {'framework': 'html', 'sections': [], 'theme': 'minimal', 'other_sections': []}

def update_design_analysis_for_regen(output_dir: str, sections_regenerated: List[str], product_desc: str, usage_stats: Dict[str, Any]) -> None:
    """Update design_analysis.json file with regeneration information"""
    analysis_file = os.path.join(output_dir, 'design_analysis.json')
    
    try:
        # Load existing analysis or create new one
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
        else:
            analysis_data = {}
        
        # Update regeneration history
        if 'regeneration_history' not in analysis_data:
            analysis_data['regeneration_history'] = []
        
        # Add current regeneration record
        regen_record = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'sections_updated': sections_regenerated,
            'product_description': product_desc,
            'usage_stats': usage_stats,
            'method': 'regen_command'
        }
        
        analysis_data['regeneration_history'].append(regen_record)
        
        # Update last_updated timestamp
        analysis_data['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Update sections list
        if 'sections' not in analysis_data:
            analysis_data['sections'] = []
        
        # Add regenerated sections to sections list if not already present
        for section in sections_regenerated:
            if section not in analysis_data['sections']:
                analysis_data['sections'].append(section)
        
        # Update product understanding if provided
        if product_desc and product_desc != "Landing page product":
            if 'product_understanding' not in analysis_data:
                analysis_data['product_understanding'] = {}
            
            analysis_data['product_understanding']['description'] = product_desc
            analysis_data['product_understanding']['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save updated analysis
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        console.print(f"[cyan]📊 Updated design analysis: {analysis_file}[/cyan]")
        
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not update design analysis: {e}[/yellow]")


def replace_sections_in_file(file_path: str, new_sections_content: str, sections_to_replace: List[str]) -> bool:
    """Replace specific sections in the landing page file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        updated_content = original_content
        
        # Extract new sections from generated content
        new_section_pattern = r'<!-- START: (\w+) -->(.*?)<!-- END: \1 -->'
        new_sections = dict(re.findall(new_section_pattern, new_sections_content, re.DOTALL))
        
        # Replace each requested section
        for section_name in sections_to_replace:
            section_key = section_name.lower()
            if section_key in new_sections:
                new_section_code = f'<!-- START: {section_key} -->{new_sections[section_key]}<!-- END: {section_key} -->'
                
                # Try multiple patterns to find existing section
                patterns_to_try = [
                    f'<!-- START: {section_key} -->.*?<!-- END: {section_key} -->',
                    f'<!-- SECTION: {section_key} -->.*?<!-- END SECTION: {section_key} -->',
                    f'<!-- {section_name.title()} Section -->.*?(?=<!-- .* Section -->|</body>|$)',
                    f'<section[^>]*class="[^"]*{section_key}[^"]*"[^>]*>.*?</section>'
                ]
                
                section_replaced = False
                for pattern in patterns_to_try:
                    if re.search(pattern, updated_content, re.DOTALL | re.IGNORECASE):
                        updated_content = re.sub(pattern, new_section_code, updated_content, flags=re.DOTALL | re.IGNORECASE)
                        section_replaced = True
                        console.print(f"[green]✓ Replaced {section_name} section using pattern match[/green]")
                        break
                
                if not section_replaced:
                    # Section doesn't exist, append it (could be a new section)
                    # Try to find a good insertion point (before closing body tag)
                    if '</body>' in updated_content:
                        # Insert before </body> and after </script> if it exists
                        script_end = updated_content.rfind('</script>')
                        body_end = updated_content.rfind('</body>')
                        
                        if script_end > 0 and script_end < body_end:
                            # Insert after </script> but before </body>
                            insertion_point = script_end + len('</script>')
                            updated_content = updated_content[:insertion_point] + f'\n{new_section_code}\n' + updated_content[insertion_point:]
                        else:
                            # Insert just before </body>
                            updated_content = updated_content.replace('</body>', f'{new_section_code}\n</body>')
                    else:
                        updated_content += f'\n{new_section_code}'
                    
                    console.print(f"[yellow]⚠ Added new {section_name} section (original not found)[/yellow]")
        
        # Clean up any duplicate sections that might have been created
        for section_name in sections_to_replace:
            section_key = section_name.lower()
            # Find all instances of this section and keep only the first one
            section_pattern = f'<!-- START: {section_key} -->.*?<!-- END: {section_key} -->'
            matches = list(re.finditer(section_pattern, updated_content, re.DOTALL))
            if len(matches) > 1:
                # Keep the first match, remove the rest
                for i in range(len(matches) - 1, 0, -1):  # Remove from end to beginning
                    match = matches[i]
                    updated_content = updated_content[:match.start()] + updated_content[match.end():]
                console.print(f"[yellow]🧹 Cleaned up duplicate {section_name} sections[/yellow]")
        
        # Write updated content back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Error updating file {file_path}: {e}[/red]")
        return False

@app.command()
def init():
    """Initialize CCUX by installing Playwright browsers"""
    console.print("[bold blue]🚀 Initializing CCUX...[/bold blue]")
    
    try:
        # Install Playwright browsers
        with Status("[bold green]Installing Playwright browsers...", console=console):
            result = subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                check=True
            )
        
        console.print("[bold green]✅ CCUX initialized successfully![/bold green]")
        console.print("\nYou can now run:")
        console.print("  [bold]ccux gen --desc 'Your product description'[/bold]")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to initialize CCUX: {e.stderr}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error during initialization: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def gen(
    desc: Optional[str] = typer.Option(None, "--desc", "-d", help="Product description"),
    desc_file: Optional[str] = typer.Option(None, "--desc-file", help="Path to file containing product description"),
    urls: Optional[List[str]] = typer.Option(None, "--url", "-u", help="Reference URLs (can be used multiple times)"),
    framework: Optional[str] = typer.Option(None, "--framework", "-f", help="Output framework (html|react)"),
    theme: Optional[str] = typer.Option(None, "--theme", "-t", help=f"Design theme ({'/'.join(get_theme_choices())})"),
    no_design_thinking: bool = typer.Option(False, "--no-design-thinking", help="Skip design thinking process"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Generate a conversion-optimized landing page
    
    Run without arguments for interactive mode, or provide --desc for direct usage.
    Use --desc-file to load description from a text file for longer copy.
    """
    
    # Load configuration
    config = Config()
    
    # Handle desc from file or interactive mode
    if desc_file:
        # Read description from file
        if not os.path.exists(desc_file):
            console.print(f"[red]❌ Description file not found: {desc_file}[/red]")
            raise typer.Exit(1)
        try:
            with open(desc_file, 'r', encoding='utf-8') as f:
                desc = f.read().strip()
            console.print(f"[green]📄 Description loaded from: {desc_file}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error reading description file: {e}[/red]")
            raise typer.Exit(1)
    elif not desc:
        # Interactive mode - prompt for inputs
        console.print("[bold blue]🎨 Interactive Mode - CCUX Generator[/bold blue]")
        console.print("Let's create your landing page step by step.\n")
        
        # Get product description
        desc = Prompt.ask(
            "[bold]What product/service would you like to create a landing page for?[/bold]",
            default="",
            show_default=False
        )
        if not desc.strip():
            console.print("[red]❌ Product description is required.[/red]")
            raise typer.Exit(1)
        
        # Optional URLs
        if not urls:
            url_input = Prompt.ask(
                "[bold]Reference URLs (optional)[/bold]\nEnter competitor or inspiration websites (comma-separated)",
                default="",
                show_default=False
            )
            if url_input.strip():
                # Split by comma and filter valid URLs
                url_list = [u.strip() for u in url_input.split(',') if u.strip().startswith('http')]
                if url_list:
                    urls = url_list
        
        # Framework selection
        if not framework:
            framework_choices = ['html', 'react']
            framework = Prompt.ask(
                "[bold]Output framework[/bold]",
                choices=framework_choices,
                default='html'
            )
        
        # Theme selection with descriptions
        if not theme:
            theme_choices = get_theme_choices()
            console.print("\n[bold]Available themes:[/bold]")
            for i, choice in enumerate(theme_choices, 1):
                desc = get_theme_description(choice)
                console.print(f"  {i}. [cyan]{choice}[/cyan]: {desc[:60]}...")
            
            theme = Prompt.ask(
                "\n[bold]Select design theme[/bold]",
                choices=theme_choices,
                default='minimal'
            )
        
        # Design thinking process option
        if not no_design_thinking:
            use_design_thinking = Confirm.ask(
                "[bold]Run full design thinking process?[/bold]\n"
                "This includes competitor research, user analysis, and wireframing (takes longer but better results)",
                default=True
            )
            no_design_thinking = not use_design_thinking
        
        console.print(f"\n[bold green]✅ Configuration complete![/bold green]")
        console.print(f"Product: [cyan]{desc}[/cyan]")
        if urls:
            console.print(f"References: [cyan]{', '.join(urls)}[/cyan]")
        console.print(f"Framework: [cyan]{framework}[/cyan] | Theme: [cyan]{theme}[/cyan]")
        console.print(f"Design thinking: [cyan]{'Yes' if not no_design_thinking else 'No'}[/cyan]\n")
    
    # Summarize description if too long
    if desc:
        desc = summarize_long_description(desc)
    
    # Override config with CLI arguments
    framework = framework or config.get('framework', 'html')
    theme = theme or config.get('theme', 'minimal')
    output_dir = output_dir or config.get('output_dir', 'output/landing-page')
    sections = config.get('sections', ['hero', 'features', 'pricing', 'footer'])
    
    # Validate inputs
    valid_frameworks = ['html', 'react']
    valid_themes = get_theme_choices()
    
    if framework not in valid_frameworks:
        console.print(f"[red]❌ Invalid framework. Must be one of: {', '.join(valid_frameworks)}[/red]")
        raise typer.Exit(1)
    
    if theme not in valid_themes:
        console.print(f"[red]❌ Invalid theme. Must be one of: {', '.join(valid_themes)}[/red]")
        raise typer.Exit(1)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    brand_display = extract_brand_name(desc)
    console.print(f"[bold blue]🎨 Generating landing page for: {brand_display}[/bold blue]")
    console.print(f"Framework: [green]{framework}[/green] | Theme: [green]{theme}[/green]")
    
    if no_design_thinking:
        # Simple mode - direct generation
        console.print("\n[bold yellow]⚡ Quick generation mode (no design thinking)[/bold yellow]")
        
        screenshot_path = None
        if urls and len(urls) > 0:
            try:
                # Use the first URL for simple mode
                url = urls[0]
                console.print(f"[bold blue]📸 Capturing reference screenshot from {url}...[/bold blue]")
                _, screenshot_path = capture(url, output_dir)
            except Exception as e:
                console.print(f"[yellow]⚠️  Failed to capture screenshot: {e}[/yellow]")
        
        # Generate directly
        prompt = landing_prompt(desc, framework, theme, sections)
        output, stats = run_claude_with_progress(prompt, "Generating landing page...")
        
        # Save output
        if framework == 'react':
            # Save React component
            with open(os.path.join(output_dir, 'App.jsx'), 'w') as f:
                f.write(strip_code_blocks(output))
            
            # Create minimal index.html shell
            html_shell = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{desc}</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" src="App.jsx"></script>
</body>
</html>'''
            
            with open(os.path.join(output_dir, 'index.html'), 'w') as f:
                f.write(html_shell)
        else:
            # Save HTML
            with open(os.path.join(output_dir, 'index.html'), 'w') as f:
                f.write(strip_code_blocks(output))
        
        console.print(f"[bold green]✅ Landing page generated successfully![/bold green]")
        console.print(f"📁 Output saved to: [bold]{output_dir}[/bold]")
        
    else:
        # Full design thinking process
        console.print("\n[bold green]🧠 Running comprehensive design thinking process...[/bold green]")
        
        try:
            # Phase 1: Reference Discovery
            console.print("\n[bold]Phase 1: Reference Discovery[/bold]")
            prompt = reference_discovery_prompt(desc)
            refs_output, _ = run_claude_with_progress(prompt, "Discovering competitor references...")
            
            # Parse reference URLs
            ref_urls = []
            for line in refs_output.split('\n'):
                if '–' in line and 'http' in line:
                    try:
                        url_part = line.split('–')[1].strip()
                        if url_part.startswith('http'):
                            ref_urls.append(url_part.split()[0])
                    except:
                        continue
            
            # Add user-provided URLs if available
            if urls:
                # Insert user URLs at the beginning, maintaining order
                for i, user_url in enumerate(reversed(urls)):
                    ref_urls.insert(0, user_url)
            
            # Limit to 3 references for performance
            ref_urls = ref_urls[:3]
            
            # 🔍 Debug / confirmation log
            if ref_urls:
                console.print("\n[bold]Discovered Reference URLs:[/bold]")
                for i, u in enumerate(ref_urls, 1):
                    console.print(f"  {i}. {u}", style="cyan")

            
            if not ref_urls:
                console.print("[yellow]⚠️  No reference URLs found. Continuing without screenshots.[/yellow]")
                screenshot_refs = []
            else:
                # Phase 2: Screenshot Capture
                console.print(f"\n[bold]Phase 2: Capturing {len(ref_urls)} reference screenshots[/bold]")
                screenshot_results = capture_multiple_references(ref_urls, output_dir)
                screenshot_refs = [(url, screenshot_path) for url, _, screenshot_path in screenshot_results]
            
            # Phase 3: Product Analysis
            console.print("\n[bold]Phase 3: Product Analysis[/bold]")
            prompt = deep_product_understanding_prompt(desc)
            product_output, _ = run_claude_with_progress(prompt, "Analyzing product positioning...")
            product_understanding = safe_json_parse(product_output)
            
            # Phase 4: UX Research
            ux_analysis = {}
            if screenshot_refs:
                console.print("\n[bold]Phase 4: UX Research[/bold]")
                screenshot_paths = [screenshot_path for url, screenshot_path in screenshot_refs]
                prompt = ux_analysis_prompt(desc, screenshot_paths)
                ux_output, _ = run_claude_with_progress(prompt, "Analyzing competitor UX patterns...")
                ux_analysis = safe_json_parse(ux_output)
            
            # Phase 5: Empathy & User Research
            console.print("\n[bold]Phase 5: User Empathy Mapping[/bold]")
            prompt = empathize_prompt(desc, product_understanding, ux_analysis)
            empathy_output, _ = run_claude_with_progress(prompt, "Mapping user empathy...")
            user_research = safe_json_parse(empathy_output)
            
            # Phase 6: Define Site Flow
            console.print("\n[bold]Phase 6: Defining Site Flow[/bold]")
            prompt = define_prompt(desc, user_research)
            define_output, _ = run_claude_with_progress(prompt, "Defining site architecture...")
            site_flow = safe_json_parse(define_output)
            
            # Phase 7: Content Strategy
            console.print("\n[bold]Phase 7: Content Strategy[/bold]")
            prompt = ideate_prompt(desc, user_research, site_flow)
            strategy_output, _ = run_claude_with_progress(prompt, "Developing content strategy...")
            content_strategy = safe_json_parse(strategy_output)
            
            # Phase 8: Wireframes (depends on content strategy)
            console.print("\n[bold]Phase 8: Wireframes[/bold]")
            wireframe_prompt_call = wireframe_prompt(desc, content_strategy, site_flow)
            wireframe_output, _ = run_claude_with_progress(wireframe_prompt_call, "Creating wireframes...")
            wireframes = safe_json_parse(wireframe_output)
            
            # Phase 9: Design System
            console.print("\n[bold]Phase 9: Design System[/bold]")
            design_prompt_call = design_system_prompt(desc, wireframes, content_strategy, theme)
            design_output, _ = run_claude_with_progress(design_prompt_call, "Building design system...")
            design_system = safe_json_parse(design_output)
            
            # Phase 10: Hi-Fi Design
            console.print("\n[bold]Phase 10: Hi-Fi Design[/bold]")
            prompt = high_fidelity_design_prompt(desc, design_system, wireframes, content_strategy)
            hifi_output, _ = run_claude_with_progress(prompt, "Creating high-fidelity design...")
            hifi_design = safe_json_parse(hifi_output)
            
            # Phase 11: Copy Generation
            console.print("\n[bold]Phase 11: Copy Generation[/bold]")
            prompt = prototype_prompt(desc, content_strategy, design_system, wireframes)
            copy_output, _ = run_claude_with_progress(prompt, "Generating final copy...")
            final_copy = safe_json_parse(copy_output)
            
            # Phase 12: Implementation
            console.print("\n[bold]Phase 12: Code Implementation[/bold]")
            screenshot_path = screenshot_refs[0][1] if screenshot_refs else None
            design_data = {
                'design_system': design_system,
                'ux_analysis': ux_analysis,
                'wireframes': wireframes,
                'content_strategy': content_strategy
            }
            # Implementation with error detection and retry
            max_attempts = 2
            code_output = None
            
            for attempt in range(max_attempts):
                try:
                    attempt_desc = "Implementing landing page..." if attempt == 0 else f"Regenerating landing page (attempt {attempt + 1})..."
                    prompt = implementation_prompt(desc, final_copy, framework, theme, design_data)
                    code_output, _ = run_claude_with_progress(prompt, attempt_desc)
                    
                    # Validate the output
                    cleaned_output = strip_code_blocks(code_output)
                    if validate_html_output(cleaned_output) or framework == 'react':
                        break
                    else:
                        if attempt < max_attempts - 1:
                            console.print("[yellow]⚠️  Generated output appears to be an error message. Retrying...[/yellow]")
                            continue
                        else:
                            console.print("[red]❌ Failed to generate valid output after multiple attempts[/red]")
                            
                except Exception as e:
                    if attempt < max_attempts - 1:
                        console.print(f"[yellow]⚠️  Implementation failed: {e}. Retrying...[/yellow]")
                        continue
                    else:
                        raise e
            
            # Save all outputs
            analysis_data = {
                'product_understanding': product_understanding,
                'ux_analysis': ux_analysis,
                'user_research': user_research,
                'site_flow': site_flow,
                'content_strategy': content_strategy,
                'wireframes': wireframes,
                'design_system': design_system,
                'hifi_design': hifi_design,
                'final_copy': final_copy
            }
            
            with open(os.path.join(output_dir, 'design_analysis.json'), 'w') as f:
                json.dump(analysis_data, f, indent=2)
            
            # Save code output with final validation
            cleaned_code = strip_code_blocks(code_output)
            
            if framework == 'react':
                with open(os.path.join(output_dir, 'App.jsx'), 'w') as f:
                    f.write(cleaned_code)
                
                html_shell = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{desc}</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel" src="App.jsx"></script>
</body>
</html>'''
                
                with open(os.path.join(output_dir, 'index.html'), 'w') as f:
                    f.write(html_shell)
            else:
                # Final validation before writing HTML
                if not validate_html_output(cleaned_code):
                    console.print("[red]⚠️  Warning: Generated HTML may contain errors[/red]")
                    # Save the raw output for debugging
                    with open(os.path.join(output_dir, 'debug_output.txt'), 'w') as f:
                        f.write(code_output)
                    console.print(f"[yellow]Debug output saved to: {output_dir}/debug_output.txt[/yellow]")
                
                with open(os.path.join(output_dir, 'index.html'), 'w') as f:
                    f.write(cleaned_code)
            
            console.print(f"\n[bold green]✅ Comprehensive landing page generated successfully![/bold green]")
            console.print(f"📁 Output saved to: [bold]{output_dir}[/bold]")
            console.print(f"📊 Design analysis saved to: [bold]{output_dir}/design_analysis.json[/bold]")
            
        except Exception as e:
            console.print(f"[red]❌ Error during design thinking process: {e}[/red]")
            raise typer.Exit(1)
    
    # Show preview instructions
    console.print("\n[bold cyan]🌐 Preview your landing page:[/bold cyan]")
    console.print(f"  [bold]cd {output_dir}[/bold]")
    console.print("  [bold]python -m http.server 3000[/bold]")
    console.print("  Then open [bold]http://localhost:3000[/bold] in your browser")

@app.command()
def regen(
    section: Optional[str] = typer.Option(None, "--section", "-s", help="Section(s) to regenerate (comma-separated)"),
    all: bool = typer.Option(False, "--all", help="Regenerate all sections"),
    desc: Optional[str] = typer.Option(None, "--desc", "-d", help="Product description (auto-detected if not provided)"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to landing page file"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Regenerate specific sections of an existing landing page
    
    Examples:
      ccux regen --section hero
      ccux regen --section hero,features
      ccux regen --all
    """
    
    config = Config()
    output_dir = output_dir or config.get('output_dir', 'output/landing-page')
    
    # Find existing landing page files
    if file:
        if not os.path.exists(file):
            console.print(f"[red]❌ File not found: {file}[/red]")
            raise typer.Exit(1)
        target_file = file
    else:
        found_files = find_landing_page_files(output_dir)
        if not found_files:
            console.print(f"[red]❌ No landing page files found in {output_dir}[/red]")
            console.print("Run [bold]ccux gen[/bold] first to create a landing page")
            raise typer.Exit(1)
        
        # Prefer React if both exist, otherwise use what's available
        if 'react' in found_files:
            target_file = found_files['react']
        else:
            target_file = found_files['html']
    
    console.print(f"[bold blue]🔄 Regenerating sections in: {target_file}[/bold blue]")
    
    # Extract context from existing file
    context = extract_page_context(target_file)
    framework = context['framework']
    theme = context['theme']
    existing_sections = context['sections']
    
    console.print(f"Detected: [green]{framework}[/green] | Theme: [green]{theme}[/green] | Sections: [cyan]{', '.join(existing_sections)}[/cyan]")
    
    # Determine sections to regenerate
    if all:
        sections_to_regen = existing_sections if existing_sections else ['hero', 'features', 'pricing', 'footer']
    elif section:
        sections_to_regen = [s.strip() for s in section.split(',')]
    else:
        console.print("[red]❌ Must specify --section or --all[/red]")
        console.print("Examples:")
        console.print("  [bold]ccux regen --section hero[/bold]")
        console.print("  [bold]ccux regen --section hero,features[/bold]")
        console.print("  [bold]ccux regen --all[/bold]")
        raise typer.Exit(1)
    
    # Get product description
    if not desc:
        # Try to extract from existing metadata or config
        if os.path.exists(os.path.join(output_dir, 'design_analysis.json')):
            try:
                with open(os.path.join(output_dir, 'design_analysis.json'), 'r') as f:
                    analysis = json.load(f)
                    desc = analysis.get('product_understanding', {}).get('problem', 'Landing page product')[:100]
            except:
                pass
        
        if not desc:
            desc = Prompt.ask(
                "[bold]What is this landing page for?[/bold]",
                default="Product landing page",
                show_default=False
            )
    
    console.print(f"Regenerating sections: [bold]{', '.join(sections_to_regen)}[/bold]")
    
    try:
        # Build context for existing page
        other_sections = [s for s in existing_sections if s not in sections_to_regen]
        existing_context = {
            'theme': theme,
            'framework': framework,
            'other_sections': f"Already has: {', '.join(other_sections)}" if other_sections else "No other sections"
        }
        
        # Generate new sections
        prompt = regeneration_prompt(desc, framework, theme, sections_to_regen, existing_context)
        new_sections_content, stats = run_claude_with_progress(
            prompt, 
            f"Regenerating {len(sections_to_regen)} section(s)..."
        )
        
        # Replace sections in the file
        success = replace_sections_in_file(target_file, new_sections_content, sections_to_regen)
        
        if success:
            console.print(f"[bold green]✅ Successfully regenerated {len(sections_to_regen)} section(s)![/bold green]")
            console.print(f"📁 Updated file: [bold]{target_file}[/bold]")
            
            # Update design_analysis.json with regeneration info
            update_design_analysis_for_regen(output_dir, sections_to_regen, desc, stats)
            
            # Show preview instructions
            console.print(f"\n[bold cyan]🌐 Preview your updated page:[/bold cyan]")
            console.print(f"  [bold]cd {os.path.dirname(target_file)}[/bold]")
            console.print("  [bold]python -m http.server 3000[/bold]")
            console.print("  Then open [bold]http://localhost:3000[/bold] in your browser")
        else:
            console.print("[red]❌ Failed to update the landing page file[/red]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error during regeneration: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def theme(
    new_theme: str = typer.Argument(..., help=f"New design theme ({'/'.join(get_theme_choices())})"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to landing page file"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Change the design theme of an existing landing page
    
    This command re-runs the design system and implementation phases 
    while preserving all research and wireframe data from the original generation.
    
    Examples:
      ccux theme brutalist
      ccux theme playful --file custom/page.html
    """
    
    config = Config()
    output_dir = output_dir or config.get('output_dir', 'output/landing-page')
    
    # Validate theme
    valid_themes = get_theme_choices()
    if new_theme not in valid_themes:
        console.print(f"[red]❌ Invalid theme. Must be one of: {', '.join(valid_themes)}[/red]")
        console.print("\n[bold]Available themes:[/bold]")
        for choice in valid_themes:
            desc = get_theme_description(choice)
            console.print(f"  [cyan]{choice}[/cyan]: {desc}")
        raise typer.Exit(1)
    
    # Find existing landing page files
    if file:
        if not os.path.exists(file):
            console.print(f"[red]❌ File not found: {file}[/red]")
            raise typer.Exit(1)
        target_file = file
    else:
        found_files = find_landing_page_files(output_dir)
        if not found_files:
            console.print(f"[red]❌ No landing page files found in {output_dir}[/red]")
            console.print("Run [bold]ccux gen[/bold] first to create a landing page")
            raise typer.Exit(1)
        
        # Prefer React if both exist, otherwise use what's available
        if 'react' in found_files:
            target_file = found_files['react']
        else:
            target_file = found_files['html']
    
    # Check for design analysis file
    analysis_file = os.path.join(output_dir, 'design_analysis.json')
    if not os.path.exists(analysis_file):
        console.print(f"[red]❌ Design analysis not found: {analysis_file}[/red]")
        console.print("This command requires a landing page generated with full design thinking process")
        console.print("Run [bold]ccux gen --desc 'your product'[/bold] without --no-design-thinking flag")
        raise typer.Exit(1)
    
    # Load existing design analysis
    try:
        with open(analysis_file, 'r') as f:
            analysis_data = json.load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading design analysis: {e}[/red]")
        raise typer.Exit(1)
    
    # Extract context from existing file
    context = extract_page_context(target_file)
    framework = context['framework']
    current_theme = context['theme']
    
    console.print(f"[bold blue]🎨 Changing theme from {current_theme} to {new_theme}[/bold blue]")
    console.print(f"Target file: [cyan]{target_file}[/cyan]")
    console.print(f"Framework: [green]{framework}[/green]")
    
    # Get product description from analysis
    product_desc = analysis_data.get('product_understanding', {}).get('problem', 'Landing page product')
    if len(product_desc) > 100:
        product_desc = product_desc[:100] + "..."
    
    console.print(f"Product: [cyan]{product_desc}[/cyan]")
    
    try:
        # Get required data from previous phases
        content_strategy = analysis_data.get('content_strategy', {})
        wireframes = analysis_data.get('wireframes', {})
        user_research = analysis_data.get('user_research', {})
        
        # Phase 9: Regenerate Design System with new theme
        console.print(f"\n[bold]Phase 9: Design System ({new_theme} theme)[/bold]")
        prompt = design_system_prompt(product_desc, wireframes, content_strategy, new_theme)
        design_output, _ = run_claude_with_progress(prompt, f"Building {new_theme} design system...")
        design_system = safe_json_parse(design_output)
        
        # Phase 10: High-Fidelity Design with new theme
        console.print(f"\n[bold]Phase 10: High-Fidelity Design ({new_theme} theme)[/bold]")
        prompt = high_fidelity_design_prompt(product_desc, design_system, wireframes, content_strategy)
        hifi_output, _ = run_claude_with_progress(prompt, f"Creating {new_theme} high-fidelity design...")
        hifi_design = safe_json_parse(hifi_output)
        
        # Phase 11: Keep existing copy (no need to regenerate)
        final_copy = analysis_data.get('final_copy', {})
        
        # Phase 12: Implementation with new theme
        console.print(f"\n[bold]Phase 12: Code Implementation ({new_theme} theme)[/bold]")
        design_data = {
            'design_system': design_system,
            'ux_analysis': analysis_data.get('ux_analysis', {}),
            'wireframes': wireframes,
            'content_strategy': content_strategy
        }
        prompt = implementation_prompt(product_desc, final_copy, framework, new_theme, design_data)
        code_output, stats = run_claude_with_progress(prompt, f"Implementing {new_theme} themed page...")
        
        # Save the new themed code
        if framework == 'react':
            with open(target_file, 'w') as f:
                f.write(strip_code_blocks(code_output))
        else:
            with open(target_file, 'w') as f:
                f.write(strip_code_blocks(code_output))
        
        # Update design analysis with new theme data
        analysis_data['design_system'] = design_system
        analysis_data['hifi_design'] = hifi_design
        analysis_data['current_theme'] = new_theme
        analysis_data['last_updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add theme change to history
        if 'theme_history' not in analysis_data:
            analysis_data['theme_history'] = []
        
        theme_record = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'from_theme': current_theme,
            'to_theme': new_theme,
            'usage_stats': stats,
            'method': 'theme_command'
        }
        analysis_data['theme_history'].append(theme_record)
        
        # Save updated analysis
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        console.print(f"[bold green]✅ Successfully changed theme to {new_theme}![/bold green]")
        console.print(f"📁 Updated file: [bold]{target_file}[/bold]")
        console.print(f"📊 Design analysis updated: [bold]{analysis_file}[/bold]")
        
        # Show preview instructions
        console.print(f"\n[bold cyan]🌐 Preview your themed page:[/bold cyan]")
        console.print(f"  [bold]cd {os.path.dirname(target_file)}[/bold]")
        console.print("  [bold]python -m http.server 3000[/bold]")
        console.print("  Then open [bold]http://localhost:3000[/bold] in your browser")
        
    except Exception as e:
        console.print(f"[red]❌ Error during theme change: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def animate(
    state: str = typer.Argument(..., help="Animation state (on|off)"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to landing page file"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Control animations in landing pages
    
    Turn animations on or off in existing landing pages. When turned on,
    applies design-specific animations based on the detected theme.
    
    Examples:
      ccux animate off                    # Disable all animations
      ccux animate on                     # Enable theme-based animations  
      ccux animate off --file custom.html # Target specific file
    """
    
    config = Config()
    output_dir = output_dir or config.get('output_dir', 'output/landing-page')
    
    # Validate state argument
    if state not in ['on', 'off']:
        console.print("[red]❌ Animation state must be 'on' or 'off'[/red]")
        console.print("Examples:")
        console.print("  [cyan]ccux animate on[/cyan]   - Enable animations")
        console.print("  [cyan]ccux animate off[/cyan]  - Disable animations")
        raise typer.Exit(1)
    
    # Find target file
    if file:
        if not os.path.exists(file):
            console.print(f"[red]❌ File not found: {file}[/red]")
            raise typer.Exit(1)
        target_file = file
    else:
        found_files = find_landing_page_files(output_dir)
        if not found_files:
            console.print(f"[red]❌ No landing page files found in {output_dir}[/red]")
            console.print("Run [bold]ccux gen[/bold] first to create a landing page")
            raise typer.Exit(1)
        
        # Prefer HTML for animation control (React not supported yet)
        if 'html' in found_files:
            target_file = found_files['html']
        else:
            console.print("[red]❌ Only HTML files are supported for animation control[/red]")
            console.print("React animation control coming soon!")
            raise typer.Exit(1)
    
    console.print(f"[bold blue]🎬 {'Enabling' if state == 'on' else 'Disabling'} animations in: {target_file}[/bold blue]")
    
    try:
        # Read the current file
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract context for theme-based animations
        context = extract_page_context(target_file)
        theme = context['theme']
        
        if state == 'off':
            # Disable animations by adding no-animations class to body and CSS rules
            if 'class="' in content and 'data-animate="true"' in content:
                # Add no-animations class to body
                content = re.sub(
                    r'<body([^>]*?)class="([^"]*?)"', 
                    r'<body\1class="\2 no-animations"', 
                    content
                )
                
                # Add CSS to disable animations if not present
                animation_disable_css = """
.no-animations * {
  animation: none !important;
  transition: none !important;
}
.no-animations html {
  scroll-behavior: auto !important;
}"""
                
                # Insert CSS before closing </style> tag
                if '</style>' in content and animation_disable_css not in content:
                    content = content.replace('</style>', f'{animation_disable_css}\n</style>')
                
                console.print("[green]✅ Animations disabled[/green]")
            else:
                console.print("[yellow]⚠️  No animations found to disable[/yellow]")
        
        else:  # state == 'on'
            # Enable animations by removing no-animations class and ensuring animation system is present
            if 'no-animations' in content:
                # Remove no-animations class from body
                content = re.sub(
                    r'<body([^>]*?)class="([^"]*?)no-animations\s*([^"]*?)"', 
                    r'<body\1class="\2\3"', 
                    content
                )
                content = re.sub(r'\s+class=""', '', content)  # Clean up empty class attributes
                
                console.print(f"[green]✅ Animations enabled with {theme} theme styling[/green]")
            else:
                console.print("[yellow]⚠️  Animations are already enabled[/yellow]")
        
        # Write the updated content
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        console.print(f"📁 Updated: [bold]{target_file}[/bold]")
        
        # Show preview instructions
        console.print(f"\n[bold cyan]🌐 Preview your {'animated' if state == 'on' else 'static'} page:[/bold cyan]")
        console.print(f"  [bold]cd {os.path.dirname(target_file)}[/bold]")
        console.print("  [bold]python -m http.server 3000[/bold]")
        console.print("  Then open [bold]http://localhost:3000[/bold] in your browser")
        
    except Exception as e:
        console.print(f"[red]❌ Error controlling animations: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def help(
    topic: Optional[str] = typer.Argument(None, help="Specific help topic (quickstart|themes|examples|workflows)")
):
    """Show comprehensive help and usage examples
    
    Available help topics:
    - quickstart: Getting started guide
    - themes: Available design themes with descriptions
    - examples: Common usage examples  
    - workflows: Step-by-step workflows
    """
    
    if topic is None:
        # Show main help menu
        console.print("[bold blue]CCUX - Claude Code UI Generator[/bold blue]")
        console.print("Generate conversion-optimized landing pages using AI-powered design thinking\n")
        
        # Quick start section
        console.print("[bold green]Quick Start[/bold green]")
        console.print("1. Initialize: [cyan]ccux init[/cyan]")
        console.print("2. Generate: [cyan]ccux gen --desc 'Your product description'[/cyan]")
        console.print("3. Preview: [cyan]cd output/landing-page && python -m http.server 3000[/cyan]\n")
        
        # Main commands table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Command", style="green", width=15)
        table.add_column("Description", width=50)
        table.add_column("Example", style="dim")
        
        table.add_row("init", "Install Playwright browsers", "ccux init")
        table.add_row("gen", "Generate landing page", "ccux gen --desc 'AI tool' --theme brutalist")
        table.add_row("regen", "Regenerate specific sections", "ccux regen --section hero,pricing")
        table.add_row("theme", "Change design theme", "ccux theme minimal")
        table.add_row("animate", "Control page animations", "ccux animate off")
        table.add_row("help", "Show detailed help", "ccux help themes")
        table.add_row("version", "Show version info", "ccux version")
        
        console.print(table)
        
        # Available help topics
        console.print("\n[bold yellow]Detailed Help Topics[/bold yellow]")
        console.print("• [cyan]ccux help quickstart[/cyan] - Complete getting started guide")
        console.print("• [cyan]ccux help themes[/cyan] - All available design themes")
        console.print("• [cyan]ccux help examples[/cyan] - Common usage patterns")
        console.print("• [cyan]ccux help workflows[/cyan] - Step-by-step workflows")
        
        # Tips
        console.print("\n[bold magenta]Pro Tips[/bold magenta]")
        console.print("• Run [cyan]ccux gen[/cyan] (no args) for interactive mode")
        console.print("• Use [cyan]--no-design-thinking[/cyan] for faster generation")
        console.print("• Provide [cyan]--url[/cyan] references for better competitor analysis")
        console.print("• Save long descriptions in a file and use [cyan]--desc-file[/cyan]")
        
    elif topic == "quickstart":
        console.print("[bold blue]CCUX Quick Start Guide[/bold blue]\n")
        
        console.print("[bold green]Step 1: Installation & Setup[/bold green]")
        console.print("# Install CCUX")
        console.print("[cyan]pip install ccux[/cyan]")
        console.print("# Initialize (download browsers)")  
        console.print("[cyan]ccux init[/cyan]\n")
        
        console.print("[bold green]Step 2: Your First Landing Page[/bold green]")
        console.print("# Interactive mode (recommended for beginners)")
        console.print("[cyan]ccux gen[/cyan]")
        console.print("# Or direct mode")
        console.print("[cyan]ccux gen --desc 'AI-powered project management tool'[/cyan]\n")
        
        console.print("[bold green]Step 3: Preview Your Page[/bold green]")
        console.print("[cyan]cd output/landing-page[/cyan]")
        console.print("[cyan]python -m http.server 3000[/cyan]")
        console.print("Open http://localhost:3000 in your browser\n")
        
        console.print("[bold green]Step 4: Customize & Iterate[/bold green]")
        console.print("# Change theme")
        console.print("[cyan]ccux theme brutalist[/cyan]")
        console.print("# Regenerate specific sections")
        console.print("[cyan]ccux regen --section hero[/cyan]")
        console.print("# Add competitor references")
        console.print("[cyan]ccux gen --desc 'Your product' --url https://competitor.com[/cyan]\n")
        
        console.print("[bold yellow]What You Get[/bold yellow]")
        console.print("• Professional conversion-optimized landing page")
        console.print("• Mobile-responsive design with TailwindCSS")
        console.print("• SEO-optimized HTML structure")
        console.print("• Design analysis JSON with research insights")
        console.print("• Screenshot references from competitors")
        
    elif topic == "themes":
        console.print("[bold blue]Available Design Themes[/bold blue]\n")
        
        # Core themes
        console.print("[bold green]Core Themes[/bold green]")
        core_themes = [
            ("minimal", "Clean, content-focused design following Dieter Rams principles"),
            ("brutalist", "Raw, honest design inspired by Brutalist architecture"),
            ("playful", "Joyful, approachable design with organic shapes"),
            ("corporate", "Traditional, trustworthy business design")
        ]
        
        for theme, desc in core_themes:
            console.print(f"• [cyan]{theme:12}[/cyan] {desc}")
        
        # Modern themes
        console.print(f"\n[bold green]Modern Design Theory Themes[/bold green]")
        modern_themes = [
            ("morphism", "Soft, tactile design combining neumorphism and glassmorphism"),
            ("animated", "Motion-first design where animation drives experience"),
            ("terminal", "Monospace, CLI-inspired aesthetic for developers"),
            ("aesthetic", "Retro-futuristic design from Y2K and vaporwave")
        ]
        
        for theme, desc in modern_themes:
            console.print(f"• [cyan]{theme:12}[/cyan] {desc}")
            
        # Additional themes
        console.print(f"\n[bold green]Specialized Themes[/bold green]")
        specialized_themes = [
            ("dark", "Modern dark theme optimized for contrast"),
            ("vibrant", "Colorful, dopamine-rich design that energizes"),
            ("sustainable", "Nature-inspired design for eco-conscious branding"),
            ("data", "Information-dense design for dashboards/analytics"),
            ("illustrated", "Hand-drawn, custom illustration-driven design")
        ]
        
        for theme, desc in specialized_themes:
            console.print(f"• [cyan]{theme:12}[/cyan] {desc}")
        
        console.print(f"\n[bold yellow]Usage Examples[/bold yellow]")
        console.print("[cyan]ccux gen --desc 'SaaS platform' --theme minimal[/cyan]")
        console.print("[cyan]ccux gen --desc 'Creative agency' --theme brutalist[/cyan]")
        console.print("[cyan]ccux theme morphism  # Change existing page theme[/cyan]")
        
    elif topic == "examples":
        console.print("[bold blue]Common Usage Examples[/bold blue]\n")
        
        # Basic examples
        console.print("[bold green]Basic Generation[/bold green]")
        examples_basic = [
            ("Interactive mode", "ccux gen", "Guided setup with prompts"),
            ("Simple generation", "ccux gen --desc 'AI writing tool'", "Quick page with minimal theme"),
            ("From file", "ccux gen --desc-file product.txt", "Load long descriptions from file"),
            ("Fast mode", "ccux gen --desc 'SaaS tool' --no-design-thinking", "Skip full research process")
        ]
        
        for name, cmd, desc in examples_basic:
            console.print(f"• [bold]{name}[/bold]: [cyan]{cmd}[/cyan]")
            console.print(f"  {desc}\n")
        
        # Advanced examples  
        console.print("[bold green]Advanced Usage[/bold green]")
        examples_advanced = [
            ("With competitors", "ccux gen --desc 'Project tool' --url https://linear.app --url https://notion.so", "Include competitor analysis"),
            ("Custom theme", "ccux gen --desc 'Design portfolio' --theme aesthetic --framework react", "React output with aesthetic theme"),
            ("Custom output", "ccux gen --desc 'Marketing site' --output custom-dir --theme vibrant", "Custom directory and theme")
        ]
        
        for name, cmd, desc in examples_advanced:
            console.print(f"• [bold]{name}[/bold]: [cyan]{cmd}[/cyan]")
            console.print(f"  {desc}\n")
        
        # Regeneration examples
        console.print("[bold green]Section Regeneration[/bold green]")
        examples_regen = [
            ("Single section", "ccux regen --section hero", "Regenerate just the hero section"),
            ("Multiple sections", "ccux regen --section hero,pricing,footer", "Regenerate multiple sections"),
            ("All sections", "ccux regen --all", "Regenerate entire page"),
            ("With new description", "ccux regen --section features --desc 'Updated product description'", "Update with new context")
        ]
        
        for name, cmd, desc in examples_regen:
            console.print(f"• [bold]{name}[/bold]: [cyan]{cmd}[/cyan]")
            console.print(f"  {desc}\n")
        
        # Theme changes
        console.print("[bold green]Theme Management[/bold green]")
        console.print("• [bold]Change theme[/bold]: [cyan]ccux theme brutalist[/cyan]")
        console.print("  Apply brutalist theme to existing page")
        console.print("• [bold]Custom file[/bold]: [cyan]ccux theme minimal --file custom/page.html[/cyan]")
        console.print("  Change theme of specific file")
        
        # Animation control
        console.print("\n[bold green]Animation Control[/bold green]")
        console.print("• [bold]Disable animations[/bold]: [cyan]ccux animate off[/cyan]")
        console.print("  Turn off all animations for better performance")
        console.print("• [bold]Enable animations[/bold]: [cyan]ccux animate on[/cyan]")
        console.print("  Turn on theme-based animations")
        console.print("• [bold]Custom file[/bold]: [cyan]ccux animate off --file custom.html[/cyan]")
        console.print("  Control animations in specific file\n")
        
    elif topic == "workflows":
        console.print("[bold blue]Step-by-Step Workflows[/bold blue]\n")
        
        # Workflow 1: First-time user
        console.print("[bold green]Workflow 1: First Landing Page[/bold green]")
        steps_first = [
            "Install: pip install ccux",
            "Initialize: ccux init", 
            "Generate interactively: ccux gen",
            "Preview: cd output/landing-page && python -m http.server 3000",
            "Iterate: ccux regen --section hero (if needed)"
        ]
        
        for i, step in enumerate(steps_first, 1):
            console.print(f"{i}. {step}")
        console.print()
        
        # Workflow 2: Competitive analysis
        console.print("[bold green]Workflow 2: With Competitor Research[/bold green]")
        steps_competitive = [
            "Find 2-3 competitor websites",
            "Generate with references: ccux gen --desc 'Your product' --url https://competitor1.com --url https://competitor2.com",
            "Review design_analysis.json for insights",
            "Refine sections: ccux regen --section pricing",
            "Experiment with themes: ccux theme brutalist"
        ]
        
        for i, step in enumerate(steps_competitive, 1):
            console.print(f"{i}. {step}")
        console.print()
        
        # Workflow 3: Production ready
        console.print("[bold green]Workflow 3: Production-Ready Process[/bold green]")  
        steps_production = [
            "Prepare detailed product description (save to file)",
            "Generate with full process: ccux gen --desc-file product.txt --theme corporate",
            "Review and customize sections: ccux regen --section hero,features",
            "Test different themes: ccux theme minimal, ccux theme dark",
            "Final review and deployment prep"
        ]
        
        for i, step in enumerate(steps_production, 1):
            console.print(f"{i}. {step}")
        console.print()
        
        # Workflow 4: Iterative design
        console.print("[bold green]Workflow 4: Iterative Design Process[/bold green]")
        steps_iterative = [
            "Start with quick generation: ccux gen --desc 'Product' --no-design-thinking",
            "Review initial version",
            "Add competitor research: ccux gen --desc 'Product' --url https://competitor.com",
            "Refine individual sections: ccux regen --section pricing --desc 'Updated positioning'",
            "Experiment with themes: ccux theme aesthetic, ccux theme terminal",
            "Final polish: ccux regen --section hero,footer"
        ]
        
        for i, step in enumerate(steps_iterative, 1):
            console.print(f"{i}. {step}")
            
    else:
        console.print(f"[red]❌ Unknown help topic: {topic}[/red]")
        console.print("Available topics: [cyan]quickstart[/cyan], [cyan]themes[/cyan], [cyan]examples[/cyan], [cyan]workflows[/cyan]")
        console.print("Run [cyan]ccux help[/cyan] for main help menu")
        raise typer.Exit(1)

@app.command()
def version():
    """Show version information"""
    try:
        package_version = importlib.metadata.version('ccux')
    except importlib.metadata.PackageNotFoundError:
        package_version = 'unknown'
    
    console.print(f"[bold blue]CCUX v{package_version}[/bold blue]")
    console.print("Claude Code UI Generator")

if __name__ == "__main__":
    app()