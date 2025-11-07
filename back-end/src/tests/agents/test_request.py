#!/usr/bin/env python3
"""
Interactive test script for Educational Multi-Agent System API.

This script allows you to test the /api/v1/generate endpoint with custom prompts.
Simply modify the PROMPT, LANGUAGE, and CONTEXT variables below and run the script.

Usage:
    python test_request.py

    Or make it executable:
    chmod +x test_request.py
    ./test_request.py
"""

import requests
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich import print as rprint

# ============================================================================
# CUSTOMIZE YOUR REQUEST HERE
# ============================================================================

# Change the prompt to whatever you want to generate
PROMPT = "Create a basic fastapi app with basic CRUD endpoints"

# Specify the programming language
LANGUAGE = "python"  # Options: python, javascript, java, rust, go, etc.

# Optional: Add additional context or requirements
CONTEXT = None  # Set to None if you don't need context

# ============================================================================
# API CONFIGURATION
# ============================================================================

# API endpoint (change if running on different host/port)
API_URL = "http://localhost:8000/api/v1/generate"

# Request timeout in seconds (code generation can take 60-90 seconds)
TIMEOUT = 120

# ============================================================================
# SCRIPT CODE (No need to modify below this line)
# ============================================================================

console = Console()


def make_request():
    """Send request to the API and display results."""

    # Build request payload
    request_data = {
        "prompt": PROMPT,
        "language": LANGUAGE,
    }

    if CONTEXT:
        request_data["context"] = CONTEXT

    # Display request information
    console.rule("[bold blue]Educational Code Generation Request[/bold blue]")
    console.print()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Prompt", PROMPT)
    table.add_row("Language", LANGUAGE)
    table.add_row("Context", CONTEXT or "(none)")
    table.add_row("API URL", API_URL)

    console.print(table)
    console.print()

    # Send request
    console.print("[yellow]⏳ Sending request (this may take 60-90 seconds)...[/yellow]")
    console.print()

    start_time = datetime.now()

    try:
        response = requests.post(
            API_URL,
            json=request_data,
            timeout=TIMEOUT,
            headers={"Content-Type": "application/json"}
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Check response status
        if response.status_code != 200:
            console.print(f"[red]❌ Error: HTTP {response.status_code}[/red]")
            console.print(f"[red]{response.text}[/red]")
            return

        # Parse response
        data = response.json()

        # Display results
        console.rule("[bold green]✅ Request Successful[/bold green]")
        console.print()

        # Summary
        summary_table = Table(show_header=True, header_style="bold cyan")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="yellow")

        summary_table.add_row("Request ID", data.get("request_id", "N/A"))
        summary_table.add_row("Status", data.get("status", "N/A"))
        summary_table.add_row("Processing Time", f"{data.get('processing_time_seconds', 0):.2f}s")
        summary_table.add_row("Total Request Time", f"{duration:.2f}s")

        console.print(Panel(summary_table, title="[bold]Response Summary[/bold]", border_style="green"))
        console.print()

        # Generated Code
        console.rule("[bold cyan]Generated Code[/bold cyan]")
        console.print()

        generated_code = data.get("generated_code", {})
        code = generated_code.get("code", "")

        if code:
            syntax = Syntax(code, LANGUAGE, theme="monokai", line_numbers=True)
            console.print(syntax)
        else:
            console.print("[yellow]No code generated[/yellow]")

        console.print()

        # Line-by-Line Explanations
        console.rule("[bold cyan]Line-by-Line Explanations[/bold cyan]")
        console.print()

        line_explanations = data.get("line_explanations", {}).get("code", [])

        if line_explanations:
            explanation_table = Table(show_header=True, header_style="bold magenta")
            explanation_table.add_column("Line", justify="right", style="cyan", width=6)
            explanation_table.add_column("Code", style="green", width=40)
            explanation_table.add_column("Explanation", style="yellow", width=50)

            for line_data in line_explanations:
                line_num = str(line_data.get("line", ""))
                line_code = line_data.get("line_code", "")
                explanation = line_data.get("line_explanation") or "[dim](blank line)[/dim]"

                # Truncate long code
                if len(line_code) > 40:
                    line_code = line_code[:37] + "..."

                # Truncate long explanations
                if len(explanation) > 50:
                    explanation = explanation[:47] + "..."

                explanation_table.add_row(line_num, line_code, explanation)

            console.print(explanation_table)
        else:
            console.print("[yellow]No explanations available[/yellow]")

        console.print()

        # Code Chunks
        console.rule("[bold cyan]Logical Code Chunks[/bold cyan]")
        console.print()

        chunked_code = data.get("chunked_code", {}).get("code", [])

        if chunked_code:
            for i, chunk in enumerate(chunked_code, 1):
                first_line = chunk.get("first_line", 0)
                last_line = chunk.get("last_line", 0)
                chunk_explanation = chunk.get("line_explanation") or "(no explanation)"

                chunk_panel = Panel(
                    f"[yellow]{chunk_explanation}[/yellow]",
                    title=f"[bold]Chunk {i}: Lines {first_line}-{last_line}[/bold]",
                    border_style="blue"
                )
                console.print(chunk_panel)
        else:
            console.print("[yellow]No chunks available[/yellow]")

        console.print()

        # Overall Explanation
        overall_explanation = data.get("chunked_code", {}).get("explanation")
        if overall_explanation:
            console.rule("[bold cyan]Overall Explanation[/bold cyan]")
            console.print()
            console.print(Panel(
                f"[green]{overall_explanation}[/green]",
                title="[bold]What This Code Does[/bold]",
                border_style="green"
            ))
            console.print()

        # Success message
        console.rule("[bold green]✨ Code Generation Complete[/bold green]")
        console.print()

        # Save option
        save_choice = console.input("[cyan]Save full response to JSON file? (y/n): [/cyan]")
        if save_choice.lower() in ['y', 'yes']:
            filename = f"response_{data.get('request_id', 'unknown')}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            console.print(f"[green]✅ Saved to {filename}[/green]")
            console.print()

    except requests.exceptions.Timeout:
        console.print(f"[red]❌ Request timeout after {TIMEOUT} seconds[/red]")
        console.print("[yellow]Tip: The server may be processing. Try increasing TIMEOUT.[/yellow]")

    except requests.exceptions.ConnectionError:
        console.print(f"[red]❌ Connection error: Could not connect to {API_URL}[/red]")
        console.print("[yellow]Tip: Make sure the server is running with: python -m src.agents.server[/yellow]")

    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")


if __name__ == "__main__":
    try:
        make_request()
    except KeyboardInterrupt:
        console.print("\n[yellow]Request cancelled by user[/yellow]")
