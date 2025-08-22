"""
Claude Integration Module

Provides Claude API integration with progress indicators and error handling.
Manages subprocess execution with timeout protection and usage tracking.
"""

import subprocess
import threading
from typing import Dict, Any, Tuple
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.console import Console

from .usage_tracking import get_latest_usage, calculate_usage_difference
from .signal_handling import set_current_subprocess, set_current_progress, clear_current_subprocess, clear_current_progress
from .configuration import Config


def run_claude_with_progress(prompt: str, description: str = "Claude Code is thinking...") -> Tuple[str, Dict[str, Any]]:
    """Run Claude CLI with real-time progress indication and usage tracking via ccusage"""
    console = Console()
    config = Config()
    claude_cmd = config.get_claude_command()
    
    # Get usage before Claude call for comparison
    pre_usage = get_latest_usage()
    
    # Prepare Claude command
    cmd = [claude_cmd, '--print', prompt]
    
    output_lines = []
    stderr_lines = []
    
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
        set_current_progress(progress)
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
            set_current_subprocess(current_subprocess)
            
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
            
            # Clean up
            clear_current_subprocess()
            clear_current_progress()
            
            output_text = '\n'.join(output_lines)
            
            # Get usage after Claude call and calculate difference
            post_usage = get_latest_usage()
            usage_stats = calculate_usage_difference(pre_usage, post_usage)
            
            return output_text, usage_stats
            
        except Exception as e:
            clear_current_subprocess()
            clear_current_progress()
            raise e


def summarize_long_description(desc: str) -> str:
    """Summarize long product descriptions to optimize token usage"""
    console = Console()
    
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


def validate_claude_command(claude_cmd: str = None) -> bool:
    """Validate that Claude CLI is available and working"""
    if not claude_cmd:
        config = Config()
        claude_cmd = config.get_claude_command()
    
    try:
        result = subprocess.run([claude_cmd, '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False


def get_claude_version(claude_cmd: str = None) -> str:
    """Get Claude CLI version information"""
    if not claude_cmd:
        config = Config()
        claude_cmd = config.get_claude_command()
    
    try:
        result = subprocess.run([claude_cmd, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return "Unknown"