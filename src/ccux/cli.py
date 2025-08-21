#!/usr/bin/env python3
"""
CCUX - Claude Code UI Generator CLI (Interactive Version)
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
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel

# Import all the existing functionality we need
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
    regeneration_prompt,
    editgen_prompt,
    editgen_sections_prompt,
    get_animation_requirements,
    form_on_prompt,
    form_off_prompt,
    form_edit_prompt
)

app = typer.Typer(
    name="ccux",
    help="CCUX - Interactive AI Landing Page Generator",
    no_args_is_help=False,
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

def get_next_available_output_dir() -> str:
    """Find the next available output directory"""
    # Check base 'output' directory first
    if not os.path.exists("output"):
        return "output"
    
    # If output exists, check output1, output2, etc.
    for i in range(1, 100):  # Support up to 99 projects
        output_dir = f"output{i}"
        if not os.path.exists(output_dir):
            return output_dir
    
    # Fallback if somehow we have 100+ projects
    import time
    return f"output-{int(time.time())}"

def discover_existing_projects() -> List[Dict[str, str]]:
    """Discover all existing CCUX projects in current directory
    Only includes projects with both index.html and design_analysis.json
    """
    projects = []
    
    # Check for output directory
    if (os.path.exists("output") and 
        os.path.exists(os.path.join("output", "index.html")) and
        os.path.exists(os.path.join("output", "design_analysis.json"))):
        project_name = extract_project_name_from_dir("output")
        projects.append({
            "directory": "output",
            "name": project_name,
            "path": os.path.join("output", "index.html")
        })
    
    # Check for output1, output2, etc.
    for i in range(1, 100):
        output_dir = f"output{i}"
        if (os.path.exists(output_dir) and 
            os.path.exists(os.path.join(output_dir, "index.html")) and
            os.path.exists(os.path.join(output_dir, "design_analysis.json"))):
            project_name = extract_project_name_from_dir(output_dir)
            projects.append({
                "directory": output_dir,
                "name": project_name,
                "path": os.path.join(output_dir, "index.html")
            })
    
    return projects

def extract_project_name_from_dir(output_dir: str) -> str:
    """Extract project name from design analysis or HTML content"""
    try:
        # Try to get from design_analysis.json first
        analysis_file = os.path.join(output_dir, "design_analysis.json")
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r') as f:
                analysis = json.load(f)
                # Look for brand name or product description
                if 'brand_name' in analysis:
                    return analysis['brand_name'][:30]
                if 'product_description' in analysis:
                    return analysis['product_description'][:30] + "..."
        
        # Fallback: extract from HTML title or first heading
        html_file = os.path.join(output_dir, "index.html")
        if os.path.exists(html_file):
            with open(html_file, 'r') as f:
                content = f.read()
                # Try to extract title
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                if title_match:
                    return title_match.group(1)[:30]
                # Try to extract first h1
                h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                if h1_match:
                    # Remove HTML tags
                    clean_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
                    return clean_text[:30].strip()
    except:
        pass
    
    return f"Project in {output_dir}"

# Import Claude runner and other utilities from the original cli.py
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
                if 'Input tokens:' in line:
                    try:
                        tokens = int(re.search(r'(\d+)', line).group(1))
                        usage_stats['input_tokens'] = tokens
                    except:
                        pass
                elif 'Output tokens:' in line:
                    try:
                        tokens = int(re.search(r'(\d+)', line).group(1))
                        usage_stats['output_tokens'] = tokens
                    except:
                        pass
                elif 'Cost:' in line:
                    try:
                        cost_match = re.search(r'\$([0-9.]+)', line)
                        if cost_match:
                            usage_stats['cost'] = float(cost_match.group(1))
                    except:
                        pass
            
            # Clean up
            current_subprocess = None
            current_progress = None
            
            output_text = '\n'.join(output_lines)
            return output_text, usage_stats
            
        except Exception as e:
            current_subprocess = None
            current_progress = None
            raise e

def summarize_long_description(desc: str) -> str:
    """Summarize long product descriptions to optimize token usage"""
    if len(desc.split()) <= 100:
        return desc
    
    console.print(f"[yellow]📝 Description is {len(desc.split())} words, summarizing to optimize Claude token usage...[/yellow]")
    
    summary_prompt = f"""Please summarize this product description in 100-150 words while preserving all key details, features, and benefits:

{desc}

Return only the summary, no additional text."""
    
    try:
        summary, _ = run_claude_with_progress(summary_prompt, "Summarizing product description...")
        return summary.strip()
    except Exception as e:
        console.print(f"[yellow]⚠️  Summarization failed: {e}. Using original description.[/yellow]")
        return desc

def safe_json_parse(text: str) -> Dict[str, Any]:
    """Safely parse JSON from Claude output with fallback"""
    try:
        # Try direct JSON parse first
        return json.loads(text.strip())
    except:
        # Try to extract JSON from code blocks
        import re
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except:
                pass
        
        # Try to find JSON-like content
        json_pattern = r'\{.*\}'
        json_match = re.search(json_pattern, text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except:
                pass
        
        # Fallback to empty dict
        console.print(f"[yellow]⚠️  Could not parse JSON from Claude output[/yellow]")
        return {}

def strip_code_blocks(text: str) -> str:
    """Remove code block markers from Claude output"""
    # Remove ```html and ``` markers
    text = re.sub(r'^```html\s*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'```$', '', text)
    return text.strip()

@app.command()
def init():
    """Launch CCUX Interactive Application (Main Entry Point)"""
    try:
        from .interactive import run_interactive_app
        run_interactive_app()
    except ImportError as e:
        console.print(f"[red]❌ Error importing interactive module: {e}[/red]")
        console.print("Please ensure all dependencies are installed.")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error running interactive app: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def version():
    """Show version information"""
    try:
        package_version = importlib.metadata.version('ccux')
    except importlib.metadata.PackageNotFoundError:
        package_version = '1.0.1'
    
    console.print(f"[bold blue]CCUX v{package_version}[/bold blue]")
    console.print("Claude Code UI Generator - Interactive landing page creator")
    console.print("\n[dim]Run 'ccux init' to start the interactive application[/dim]")

@app.command()
def projects():
    """List all existing CCUX projects in the current directory"""
    projects = discover_existing_projects()
    
    if not projects:
        console.print("[yellow]No CCUX projects found in current directory.[/yellow]")
        console.print("Run [bold]ccux init[/bold] to create your first project!")
        return
    
    console.print(f"\n[bold cyan]📁 Found {len(projects)} CCUX project(s):[/bold cyan]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Directory", style="cyan", width=15)
    table.add_column("Project Name", style="green")
    table.add_column("Status", style="yellow", width=10)
    
    for project in projects:
        # All projects now have design analysis (since we filter for it)
        status = "Full"
        
        table.add_row(
            project['directory'] + "/",
            project['name'],
            status
        )
    
    console.print(table)
    
    console.print(f"\n[dim]💡 Run 'ccux init' to manage these projects interactively[/dim]")

@app.command()
def help(topic: Optional[str] = typer.Argument(None, help="Help topic (quickstart|themes|examples|workflows)")):
    """Show comprehensive help and usage examples"""
    # Import and use the help function from cli_old
    from . import cli_old
    cli_old.help(topic)

@app.command()
def gen(
    desc: Optional[str] = typer.Option(None, "--desc", "-d", help="Product description"),
    desc_file: Optional[str] = typer.Option(None, "--desc-file", help="Path to file containing product description"),
    url: Optional[List[str]] = typer.Option(None, "--url", "-u", help="Reference URLs (can be used multiple times, max 3)"),
    framework: Optional[str] = typer.Option("html", "--framework", "-f", help="Output framework (html|react)"),
    theme: Optional[str] = typer.Option("minimal", "--theme", "-t", help="Design theme"),
    no_design_thinking: bool = typer.Option(False, "--no-design-thinking", help="Skip full design thinking process"),
    include_forms: bool = typer.Option(False, "--include-forms", help="Include contact forms"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Generate conversion-optimized landing page"""
    # Import and use the gen function from cli_old
    from . import cli_old
    cli_old.gen(desc, desc_file, url, framework, theme, no_design_thinking, include_forms, output_dir)

@app.command()
def regen(
    section: Optional[str] = typer.Option(None, "--section", "-s", help="Section(s) to regenerate (comma-separated)"),
    all: bool = typer.Option(False, "--all", help="Regenerate all sections"),
    desc: Optional[str] = typer.Option(None, "--desc", "-d", help="Product description"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to landing page file"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Regenerate specific sections of existing landing page"""
    # Import and use the regen function from cli_old
    from . import cli_old
    cli_old.regen(section, all, desc, file, output_dir)

@app.command()
def init():
    """Launch CCUX Interactive Application (Main Entry Point)"""
    try:
        from .interactive import run_interactive_app
        run_interactive_app()
    except ImportError as e:
        console.print(f"[red]❌ Error importing interactive module: {e}[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("[yellow]👋 Goodbye![/yellow]")
        raise typer.Exit(0)

# Default command when no arguments provided
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """CCUX - Interactive AI Landing Page Generator
    
    Run 'ccux init' to start the interactive application.
    """
    if ctx.invoked_subcommand is None:
        # If no command is provided, launch the interactive app
        ctx.invoke(init)

if __name__ == "__main__":
    app()