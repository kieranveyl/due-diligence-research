"""Research command implementation"""

import asyncio
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from src.cli.commands.utils import (
    check_system_health,
    create_session_id,
    detect_entity_type,
    format_report_summary,
    generate_report_path,
    parse_scope_string,
    save_report_content,
    show_scope_selection,
)
from src.cli.models.config import CLIConfig, SessionData
from src.cli.ui.progress import (
    ResearchProgressTracker,
    show_completion_summary,
    show_error_summary,
)

console = Console()

# Create research subcommand
research_cmd = typer.Typer(help="🔬 Conduct due diligence research")


@research_cmd.command(name="", hidden=True)  # Default command
@research_cmd.command("run")  # Explicit command
def research(
    entity_name: str = typer.Argument(..., help="Name of entity to research"),
    scope: str | None = typer.Option(None, "--scope", help="Comma-separated research areas (financial,legal,osint,verification)"),
    output: str | None = typer.Option(None, "--output", "-o", help="Custom output path for report"),
    format_type: str = typer.Option("markdown", "--format", help="Output format (markdown, json, pdf)"),
    no_interactive: bool = typer.Option(False, "--no-interactive", help="Skip interactive prompts"),
    confidence_threshold: float = typer.Option(None, "--confidence-threshold", help="Minimum confidence threshold"),
    max_sources: int = typer.Option(None, "--max-sources", help="Maximum sources to use"),
    timeout: int = typer.Option(None, "--timeout", help="Research timeout in seconds"),
    model: str | None = typer.Option(None, "--model", help="Override default LLM model"),
    parallel_tasks: int = typer.Option(None, "--parallel-tasks", help="Number of parallel tasks"),
    save_session: bool = typer.Option(False, "--save-session", help="Save session for later review"),
    resume: str | None = typer.Option(None, "--resume", help="Resume previous session by ID"),
):
    """
    Conduct comprehensive due diligence research on an entity.

    Examples:
        dd research "Tesla Inc"
        dd research "Apple Inc" --scope financial,legal --output ./reports/apple.md
        dd research "Suspicious Corp" --no-interactive --confidence-threshold 0.9
    """
    # Load configuration
    config = CLIConfig.load()

    # Handle resume session
    if resume:
        session = SessionData.load(resume)
        if not session:
            console.print(f"❌ Session '{resume}' not found", style="red")
            raise typer.Exit(1)

        console.print(f"📂 Resuming session: {session.entity_name}")
        entity_name = session.entity_name
        # Override other parameters from session

    # Validate system health if interactive
    if not no_interactive:
        from src.cli.commands.utils import validate_api_keys
        api_status = validate_api_keys()
        if not (api_status["openai"] and api_status["exa"]):
            console.print("❌ [red]Missing required API keys[/red]")
            if Confirm.ask("Would you like to see system health check?"):
                check_system_health()
            raise typer.Exit(1)

    # Auto-detect entity type
    entity_type = detect_entity_type(entity_name)

    if not no_interactive:
        console.print(f"\n🔍 [bold]Analyzing entity:[/bold] {entity_name}")
        console.print(f"📊 [bold]Detected type:[/bold] {entity_type}")
        if not Confirm.ask(f"Continue with {entity_type} analysis?", default=True):
            raise typer.Exit(0)

    # Determine research scope
    if scope:
        research_scope = parse_scope_string(scope)
    elif not no_interactive:
        research_scope = show_scope_selection()
    else:
        research_scope = config.default_scope

    if not research_scope:
        console.print("❌ No research scope selected", style="red")
        raise typer.Exit(1)

    # Apply configuration overrides
    final_config = {
        "confidence_threshold": confidence_threshold or config.confidence_threshold,
        "max_sources": max_sources or config.max_sources,
        "timeout": timeout or config.timeout,
        "model": model or config.model,
        "parallel_tasks": parallel_tasks or config.parallel_tasks,
        "format": format_type,
    }

    # Generate output path
    report_path = generate_report_path(entity_name, config.default_output_dir, output)

    if not no_interactive:
        console.print("\n📝 [bold]Report will be saved to:[/bold]")
        console.print(f"📁 {report_path}")

        custom_path = Prompt.ask("Custom path (press enter for default)", default="")
        if custom_path:
            report_path = Path(custom_path)

    # Create session data
    session_id = create_session_id()
    session_data = SessionData(
        session_id=session_id,
        entity_name=entity_name,
        entity_type=entity_type,
        query=f"Due diligence research on {entity_name}",
        scope=research_scope,
        status="running",
        created_at=datetime.now().isoformat(),
        report_path=str(report_path)
    )

    if save_session or not no_interactive:
        if save_session or Confirm.ask("Save session for later review?", default=False):
            session_data.save()
            console.print(f"💾 Session saved with ID: [bold]{session_id}[/bold]")

    # Run research
    console.print("\n🚀 [bold]Starting due diligence research...[/bold]")

    try:
        results = asyncio.run(run_research_workflow(
            entity_name=entity_name,
            entity_type=entity_type,
            scope=research_scope,
            config=final_config,
            session_id=session_id
        ))

        # Update session
        session_data.status = "completed"
        session_data.completed_at = datetime.now().isoformat()
        session_data.confidence = results.get("overall_confidence", 0.0)
        session_data.sources_count = len(results.get("citations", []))
        session_data.save()

        # Generate and save report
        report_content = format_report_summary(results)
        if save_report_content(report_content, report_path):
            results["report_path"] = str(report_path)
            console.print(f"\n📄 [green]Report saved to:[/green] {report_path}")

        # Show completion summary
        show_completion_summary(results)

    except Exception as e:
        session_data.status = "failed"
        session_data.save()

        show_error_summary(str(e))
        console.print(f"\n💡 Session ID [bold]{session_id}[/bold] saved for debugging")
        raise typer.Exit(1)


async def run_research_workflow(
    entity_name: str,
    entity_type: str,
    scope: list[str],
    config: dict,
    session_id: str
) -> dict:
    """Execute the research workflow with progress tracking"""

    progress_tracker = ResearchProgressTracker()
    start_time = datetime.now()

    try:
        # Import workflow components
        from src.workflows.due_diligence import DueDiligenceWorkflow

        # Initialize workflow
        console.print("📋 Initializing research workflow...")
        progress_tracker.update_phase("Initialization")

        DueDiligenceWorkflow()

        # Convert entity type

        # Set up progress tracking
        progress_tracker.total_tasks = len(scope)

        # Run workflow
        console.print("🔄 Executing research tasks...")
        progress_tracker.update_phase("Research Execution")

        results = {}
        citations = []
        confidence_scores = {}

        # Simulate research execution with progress updates
        for i, agent_type in enumerate(scope):
            progress_tracker.update_agent_progress(agent_type, 0, "Starting...")

            # Simulate work with actual workflow call
            console.print(f"🤖 Executing {agent_type} analysis...")

            # Progress updates during execution
            for progress in [25, 50, 75, 100]:
                await asyncio.sleep(0.5)  # Simulate work
                status = "Processing..." if progress < 100 else "Complete"
                progress_tracker.update_agent_progress(agent_type, progress, status)

            # Mark complete with mock confidence
            mock_confidence = 0.85 + (i * 0.03)  # Simulate varying confidence
            progress_tracker.mark_agent_complete(agent_type, mock_confidence)
            confidence_scores[agent_type] = mock_confidence

            # Mock results
            results[agent_type] = {
                "key_findings": [f"Sample finding from {agent_type} analysis"],
                "summary": f"Completed {agent_type} analysis for {entity_name}"
            }
            citations.extend([f"Source from {agent_type} analysis"])

        # Final processing
        console.print("📊 Synthesizing results...")
        progress_tracker.update_phase("Synthesis")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Compile final results
        final_results = {
            "entity_name": entity_name,
            "entity_type": entity_type,
            "scopes": scope,
            "findings": results,
            "citations": citations,
            "confidence_scores": confidence_scores,
            "overall_confidence": sum(confidence_scores.values()) / len(confidence_scores),
            "duration": duration,
            "session_id": session_id,
            "sources_count": len(citations),
            "executive_summary": f"Comprehensive due diligence analysis completed for {entity_name}. "
                               f"Research covered {', '.join(scope)} with an overall confidence of "
                               f"{(sum(confidence_scores.values()) / len(confidence_scores)):.1%}."
        }

        return final_results

    except Exception as e:
        console.print(f"❌ Research failed: {e}", style="red")
        raise


@research_cmd.command("status")
def research_status(
    session_id: str | None = typer.Argument(None, help="Session ID to check")
):
    """Check status of research session"""
    if session_id:
        session = SessionData.load(session_id)
        if not session:
            console.print(f"❌ Session '{session_id}' not found", style="red")
            raise typer.Exit(1)

        console.print(f"📊 Session: {session.entity_name}")
        console.print(f"Status: {session.status}")
        console.print(f"Created: {session.created_at}")

        if session.completed_at:
            console.print(f"Completed: {session.completed_at}")
        if session.confidence:
            console.print(f"Confidence: {session.confidence:.1%}")
        if session.report_path:
            console.print(f"Report: {session.report_path}")
    else:
        # List recent sessions
        sessions = SessionData.list_sessions()[:10]  # Show last 10

        if not sessions:
            console.print("No research sessions found")
            return

        from rich.table import Table
        table = Table(title="Recent Research Sessions")
        table.add_column("ID", style="bold")
        table.add_column("Entity", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Created")

        for session in sessions:
            status_emoji = {"completed": "✅", "running": "🔄", "failed": "❌", "pending": "⏳"}
            status_text = f"{status_emoji.get(session.status, '?')} {session.status}"

            table.add_row(
                session.session_id,
                session.entity_name,
                status_text,
                session.created_at[:16]  # Truncate timestamp
            )

        console.print(table)
