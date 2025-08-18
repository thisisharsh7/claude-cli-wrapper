#!/usr/bin/env python3
"""
CCUI - Claude Code UI Generator CLI
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

from . import __version__
from .scrape import capture_multiple_references
from .scrape_simple import capture
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
    landing_prompt
)

app = typer.Typer(
    name="ccui",
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
    """Configuration management for CCUI"""
    
    def __init__(self, config_path: str = "ccui.yaml"):
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

@app.command()
def init():
    """Initialize CCUI by installing Playwright browsers"""
    console.print("[bold blue]🚀 Initializing CCUI...[/bold blue]")
    
    try:
        # Install Playwright browsers
        with Status("[bold green]Installing Playwright browsers...", console=console):
            result = subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                check=True
            )
        
        console.print("[bold green]✅ CCUI initialized successfully![/bold green]")
        console.print("\nYou can now run:")
        console.print("  [bold]ccui gen --desc 'Your product description'[/bold]")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Failed to initialize CCUI: {e.stderr}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Error during initialization: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def gen(
    desc: str = typer.Option(..., "--desc", "-d", help="Product description"),
    url: Optional[str] = typer.Option(None, "--url", "-u", help="Reference URL"),
    framework: Optional[str] = typer.Option(None, "--framework", "-f", help="Output framework (html|react)"),
    theme: Optional[str] = typer.Option(None, "--theme", "-t", help="Design theme (minimal|brutalist|playful|corporate)"),
    no_design_thinking: bool = typer.Option(False, "--no-design-thinking", help="Skip design thinking process"),
    output_dir: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory")
):
    """Generate a conversion-optimized landing page"""
    
    # Load configuration
    config = Config()
    
    # Override config with CLI arguments
    framework = framework or config.get('framework', 'html')
    theme = theme or config.get('theme', 'minimal')
    output_dir = output_dir or config.get('output_dir', 'output/landing-page')
    sections = config.get('sections', ['hero', 'features', 'pricing', 'footer'])
    
    # Validate inputs
    valid_frameworks = ['html', 'react']
    valid_themes = ['minimal', 'brutalist', 'playful', 'corporate']
    
    if framework not in valid_frameworks:
        console.print(f"[red]❌ Invalid framework. Must be one of: {', '.join(valid_frameworks)}[/red]")
        raise typer.Exit(1)
    
    if theme not in valid_themes:
        console.print(f"[red]❌ Invalid theme. Must be one of: {', '.join(valid_themes)}[/red]")
        raise typer.Exit(1)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    console.print(f"[bold blue]🎨 Generating landing page for: {desc}[/bold blue]")
    console.print(f"Framework: [green]{framework}[/green] | Theme: [green]{theme}[/green]")
    
    if no_design_thinking:
        # Simple mode - direct generation
        console.print("\n[bold yellow]⚡ Quick generation mode (no design thinking)[/bold yellow]")
        
        screenshot_path = None
        if url:
            try:
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
                f.write(output)
            
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
                f.write(output)
        
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
            
            # Add user-provided URL if available
            if url:
                ref_urls.insert(0, url)
            
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
            
            # Phase 3: Deep Product Understanding
            console.print("\n[bold]Phase 3: Deep Product Understanding[/bold]")
            prompt = deep_product_understanding_prompt(desc)
            product_output, _ = run_claude_with_progress(prompt, "Analyzing product positioning...")
            product_understanding = safe_json_parse(product_output)
            
            # Phase 4: UX Analysis
            if screenshot_refs:
                console.print("\n[bold]Phase 4: Competitive UX Analysis[/bold]")
                # Extract just the screenshot paths from the tuples
                screenshot_paths = [screenshot_path for url, screenshot_path in screenshot_refs]
                prompt = ux_analysis_prompt(desc, screenshot_paths)
                ux_output, _ = run_claude_with_progress(prompt, "Analyzing competitor UX patterns...")
                ux_analysis = safe_json_parse(ux_output)
            else:
                ux_analysis = {}
            
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
            ideate_output, _ = run_claude_with_progress(prompt, "Developing content strategy...")
            content_strategy = safe_json_parse(ideate_output)
            
            # Phase 8: Wireframes
            console.print("\n[bold]Phase 8: Wireframe Validation[/bold]")
            prompt = wireframe_prompt(desc, content_strategy, site_flow)
            wireframe_output, _ = run_claude_with_progress(prompt, "Creating wireframes...")
            wireframes = safe_json_parse(wireframe_output)
            
            # Phase 9: Design System
            console.print("\n[bold]Phase 9: Design System[/bold]")
            prompt = design_system_prompt(desc, wireframes, content_strategy)
            design_output, _ = run_claude_with_progress(prompt, "Building design system...")
            design_system = safe_json_parse(design_output)
            
            # Phase 10: High-Fidelity Design
            console.print("\n[bold]Phase 10: High-Fidelity Design[/bold]")
            prompt = high_fidelity_design_prompt(desc, design_system, wireframes, content_strategy)
            hifi_output, _ = run_claude_with_progress(prompt, "Creating high-fidelity design...")
            hifi_design = safe_json_parse(hifi_output)
            
            # Phase 11: Final Copy Generation
            console.print("\n[bold]Phase 11: Final Copy Generation[/bold]")
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
            prompt = implementation_prompt(desc, final_copy, framework, theme, design_data)
            code_output, _ = run_claude_with_progress(prompt, "Implementing landing page...")
            
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
            
            # Save code output
            if framework == 'react':
                with open(os.path.join(output_dir, 'App.jsx'), 'w') as f:
                    f.write(code_output)
                
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
                with open(os.path.join(output_dir, 'index.html'), 'w') as f:
                    f.write(code_output)
            
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
def version():
    """Show version information"""
    console.print(f"[bold blue]CCUI v{__version__}[/bold blue]")
    console.print("Claude Code UI Generator")

if __name__ == "__main__":
    app()