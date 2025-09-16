"""Rich UI components for progress tracking"""

from datetime import datetime
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

console = Console()


class ResearchProgressTracker:
    """Live progress tracking for research operations"""

    def __init__(self):
        self.agents_progress = {}
        self.overall_progress = 0
        self.start_time = datetime.now()
        self.current_phase = "Initializing"
        self.total_tasks = 0
        self.completed_tasks = 0

    def create_progress_layout(self):
        """Create the progress display layout"""
        # Overall progress bar
        overall_progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Due Diligence Research"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
        )

        # Agent-specific progress
        agent_progress = Progress(
            TextColumn("[bold]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=True,
        )

        return overall_progress, agent_progress

    def update_phase(self, phase: str):
        """Update current research phase"""
        self.current_phase = phase

    def update_agent_progress(self, agent: str, progress: float, status: str = ""):
        """Update progress for a specific agent"""
        self.agents_progress[agent] = {
            "progress": progress,
            "status": status,
            "emoji": self._get_agent_emoji(agent)
        }

    def _get_agent_emoji(self, agent: str) -> str:
        """Get emoji for agent type"""
        emoji_map = {
            "financial": "💰",
            "legal": "⚖️",
            "osint": "🔍",
            "verification": "✅",
            "research": "📊",
            "planner": "🗓️"
        }
        return emoji_map.get(agent, "🤖")

    def mark_agent_complete(self, agent: str, confidence: float = 0.0):
        """Mark agent as completed"""
        self.agents_progress[agent] = {
            "progress": 100.0,
            "status": f"Complete (confidence: {confidence:.1%})",
            "emoji": "✅"
        }
        self.completed_tasks += 1

    def mark_agent_failed(self, agent: str, error: str = ""):
        """Mark agent as failed"""
        self.agents_progress[agent] = {
            "progress": 0.0,
            "status": f"Failed: {error}",
            "emoji": "❌"
        }

    def get_summary_panel(self) -> Panel:
        """Get summary panel for research progress"""
        table = Table(show_header=False, box=None, padding=(0, 1))

        # Phase info
        elapsed = datetime.now() - self.start_time
        table.add_row("📋 Phase:", f"[bold]{self.current_phase}[/bold]")
        table.add_row("⏱️  Elapsed:", f"{elapsed.total_seconds():.0f}s")

        if self.total_tasks > 0:
            table.add_row("📊 Progress:", f"{self.completed_tasks}/{self.total_tasks} tasks completed")

        return Panel(table, title="🔍 Research Status", border_style="blue")

    def get_agents_panel(self) -> Panel:
        """Get agents progress panel"""
        table = Table(show_header=True, box=None)
        table.add_column("Agent", style="bold")
        table.add_column("Progress", style="green")
        table.add_column("Status", style="dim")

        for agent, data in self.agents_progress.items():
            emoji = data["emoji"]
            progress = data["progress"]
            status = data["status"]

            # Create progress bar
            if progress == 100:
                progress_bar = "[green]████████████[/green] 100%"
            elif progress >= 75:
                progress_bar = "[yellow]█████████░░░[/yellow] " + f"{progress:.0f}%"
            elif progress >= 50:
                progress_bar = "[orange1]██████░░░░░░[/orange1] " + f"{progress:.0f}%"
            elif progress >= 25:
                progress_bar = "[red]███░░░░░░░░░[/red] " + f"{progress:.0f}%"
            else:
                progress_bar = "[dim]░░░░░░░░░░░░[/dim] " + f"{progress:.0f}%"

            table.add_row(
                f"{emoji} {agent.title()}",
                progress_bar,
                status
            )

        return Panel(table, title="🤖 Agent Status", border_style="green")


class InteractivePrompter:
    """Interactive prompts for CLI"""

    @staticmethod
    def confirm(message: str, default: bool = True) -> bool:
        """Interactive confirmation prompt"""
        from rich.prompt import Confirm
        return Confirm.ask(message, default=default)

    @staticmethod
    def select_multiple(options: dict[str, str], title: str = "Select options") -> list[str]:
        """Multi-select prompt"""
        console.print(f"\n[bold]{title}[/bold]")
        console.print("Use space to toggle, enter to confirm:")

        selected = set()
        current = 0

        while True:
            console.clear()
            console.print(f"\n[bold]{title}[/bold]")
            console.print("Use ↑↓ to navigate, space to toggle, enter to confirm:\n")

            for i, (key, description) in enumerate(options.items()):
                if i == current:
                    marker = "→"
                    style = "bold"
                else:
                    marker = " "
                    style = "dim"

                checkbox = "☑" if key in selected else "☐"
                console.print(f"{marker} {checkbox} {key}: {description}", style=style)

            # Simple implementation - in real CLI would handle key events
            console.print("\n[dim]Enter selection as comma-separated values:[/dim]")
            user_input = input().strip()
            if user_input:
                return [s.strip() for s in user_input.split(",") if s.strip() in options]
            return list(selected)

    @staticmethod
    def text_prompt(message: str, default: str = "") -> str:
        """Text input prompt"""
        from rich.prompt import Prompt
        return Prompt.ask(message, default=default)

    @staticmethod
    def path_prompt(message: str, default: str = "") -> str:
        """File path input prompt with validation"""
        from pathlib import Path

        from rich.prompt import Prompt

        while True:
            path_str = Prompt.ask(message, default=default)
            if not path_str:
                continue

            path = Path(path_str)
            try:
                # Create parent directories if they don't exist
                path.parent.mkdir(parents=True, exist_ok=True)
                return str(path)
            except Exception as e:
                console.print(f"❌ Invalid path: {e}", style="red")
                continue


def show_completion_summary(results: dict[str, Any]):
    """Show research completion summary"""
    panel_content = Table(show_header=False, box=None)

    # Success metrics
    confidence = results.get("confidence", 0.0)
    sources_count = results.get("sources_count", 0)
    duration = results.get("duration", "Unknown")

    panel_content.add_row("✅ Status:", "[bold green]Research Complete[/bold green]")
    panel_content.add_row("📊 Confidence:", f"[bold]{confidence:.1%}[/bold]")
    panel_content.add_row("🔗 Sources:", f"[bold]{sources_count}[/bold]")
    panel_content.add_row("⏱️  Duration:", f"[bold]{duration}[/bold]")

    if "report_path" in results:
        panel_content.add_row("📝 Report:", f"[link]{results['report_path']}[/link]")

    console.print(Panel(panel_content, title="🎉 Research Complete", border_style="green"))


def show_error_summary(error: str):
    """Show error summary"""
    console.print(f"❌ [bold red]Research Failed[/bold red]: {error}")
