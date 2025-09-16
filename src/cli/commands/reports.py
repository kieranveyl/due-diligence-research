"""Reports management commands"""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from src.cli.models.config import CLIConfig, SessionData

console = Console()

# Create reports subcommand
reports_cmd = typer.Typer(help="📊 Manage and export reports")


@reports_cmd.command("list")
def list_reports(
    directory: str | None = typer.Option(None, "--dir", "-d", help="Reports directory to scan"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum number of reports to show")
):
    """List all available reports"""
    config = CLIConfig.load()
    reports_dir = Path(directory) if directory else Path(config.default_output_dir)

    if not reports_dir.exists():
        console.print(f"❌ Reports directory not found: {reports_dir}", style="red")
        raise typer.Exit(1)

    # Find all report files
    report_files = []
    for pattern in ["*.md", "*.json", "*.pdf"]:
        report_files.extend(reports_dir.glob(pattern))

    if not report_files:
        console.print(f"📂 No reports found in {reports_dir}")
        return

    # Sort by modification time (newest first)
    report_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # Create table
    table = Table(title=f"📊 Reports in {reports_dir}")
    table.add_column("Name", style="bold cyan")
    table.add_column("Size", style="green")
    table.add_column("Modified", style="dim")
    table.add_column("Format", style="yellow")

    for report_file in report_files[:limit]:
        stat = report_file.stat()
        size = format_file_size(stat.st_size)
        modified = format_timestamp(stat.st_mtime)
        file_format = report_file.suffix[1:].upper() if report_file.suffix else "Unknown"

        table.add_row(
            report_file.name,
            size,
            modified,
            file_format
        )

    console.print(table)

    if len(report_files) > limit:
        console.print(f"\n📝 Showing {limit} of {len(report_files)} reports. Use --limit to show more.")


@reports_cmd.command("show")
def show_report(
    report_name: str = typer.Argument(..., help="Report filename or session ID"),
    directory: str | None = typer.Option(None, "--dir", "-d", help="Reports directory"),
    lines: int | None = typer.Option(None, "--lines", "-n", help="Number of lines to show")
):
    """Display report content"""
    config = CLIConfig.load()

    # Try to load as session ID first
    if len(report_name) == 8 and not report_name.endswith(('.md', '.json', '.pdf')):
        session = SessionData.load(report_name)
        if session and session.report_path:
            report_path = Path(session.report_path)
        else:
            console.print(f"❌ Session '{report_name}' not found or no report available", style="red")
            raise typer.Exit(1)
    else:
        # Treat as filename
        reports_dir = Path(directory) if directory else Path(config.default_output_dir)
        report_path = reports_dir / report_name

    if not report_path.exists():
        console.print(f"❌ Report not found: {report_path}", style="red")
        raise typer.Exit(1)

    try:
        with open(report_path, encoding='utf-8') as f:
            content = f.read()

        if lines:
            content_lines = content.split('\n')[:lines]
            content = '\n'.join(content_lines)
            if len(content.split('\n')) < len(content_lines):
                content += "\n\n... (truncated)"

        # Display with syntax highlighting for markdown
        if report_path.suffix == '.md':
            from rich.markdown import Markdown
            console.print(Markdown(content))
        else:
            console.print(content)

    except Exception as e:
        console.print(f"❌ Error reading report: {e}", style="red")
        raise typer.Exit(1)


@reports_cmd.command("export")
def export_report(
    report_name: str = typer.Argument(..., help="Report filename or session ID"),
    output_format: str = typer.Option("pdf", "--format", "-f", help="Output format (pdf, json, markdown)"),
    output_path: str | None = typer.Option(None, "--output", "-o", help="Output file path"),
    directory: str | None = typer.Option(None, "--dir", "-d", help="Reports directory")
):
    """Export report to different format"""
    config = CLIConfig.load()

    # Find source report
    if len(report_name) == 8 and not report_name.endswith(('.md', '.json', '.pdf')):
        session = SessionData.load(report_name)
        if session and session.report_path:
            source_path = Path(session.report_path)
        else:
            console.print(f"❌ Session '{report_name}' not found", style="red")
            raise typer.Exit(1)
    else:
        reports_dir = Path(directory) if directory else Path(config.default_output_dir)
        source_path = reports_dir / report_name

    if not source_path.exists():
        console.print(f"❌ Source report not found: {source_path}", style="red")
        raise typer.Exit(1)

    # Determine output path
    if not output_path:
        output_path = source_path.with_suffix(f".{output_format}")

    output_path = Path(output_path)

    try:
        if output_format.lower() == "pdf":
            export_to_pdf(source_path, output_path)
        elif output_format.lower() == "json":
            export_to_json(source_path, output_path)
        elif output_format.lower() == "markdown":
            if source_path.suffix != '.md':
                console.print("⚠️  Converting non-markdown to markdown may lose formatting", style="yellow")
            export_to_markdown(source_path, output_path)
        else:
            console.print(f"❌ Unsupported format: {output_format}", style="red")
            raise typer.Exit(1)

        console.print(f"✅ Report exported to: {output_path}", style="green")

    except Exception as e:
        console.print(f"❌ Export failed: {e}", style="red")
        raise typer.Exit(1)


@reports_cmd.command("cleanup")
def cleanup_reports(
    directory: str | None = typer.Option(None, "--dir", "-d", help="Reports directory"),
    older_than: int = typer.Option(30, "--older-than", help="Delete reports older than N days"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be deleted without deleting"),
    confirm_all: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts")
):
    """Clean up old reports"""
    import time

    config = CLIConfig.load()
    reports_dir = Path(directory) if directory else Path(config.default_output_dir)

    if not reports_dir.exists():
        console.print(f"❌ Reports directory not found: {reports_dir}", style="red")
        raise typer.Exit(1)

    # Find old reports
    cutoff_time = time.time() - (older_than * 24 * 60 * 60)
    old_reports = []

    for pattern in ["*.md", "*.json", "*.pdf"]:
        for report_file in reports_dir.glob(pattern):
            if report_file.stat().st_mtime < cutoff_time:
                old_reports.append(report_file)

    if not old_reports:
        console.print(f"✅ No reports older than {older_than} days found")
        return

    # Show what will be deleted
    console.print(f"📂 Found {len(old_reports)} reports older than {older_than} days:")

    table = Table()
    table.add_column("File", style="bold")
    table.add_column("Age", style="yellow")
    table.add_column("Size", style="green")

    total_size = 0
    for report_file in old_reports:
        stat = report_file.stat()
        age_days = (time.time() - stat.st_mtime) / (24 * 60 * 60)
        size = stat.st_size
        total_size += size

        table.add_row(
            report_file.name,
            f"{age_days:.0f} days",
            format_file_size(size)
        )

    console.print(table)
    console.print(f"\n💾 Total size: {format_file_size(total_size)}")

    if dry_run:
        console.print("🔍 Dry run - no files were deleted")
        return

    # Confirm deletion
    if not confirm_all:
        if not Confirm.ask(f"Delete {len(old_reports)} old reports?", default=False):
            console.print("Cleanup cancelled")
            return

    # Delete files
    deleted_count = 0
    for report_file in old_reports:
        try:
            report_file.unlink()
            deleted_count += 1
        except Exception as e:
            console.print(f"❌ Failed to delete {report_file.name}: {e}", style="red")

    console.print(f"✅ Deleted {deleted_count} old reports", style="green")


@reports_cmd.command("summary")
def reports_summary(
    directory: str | None = typer.Option(None, "--dir", "-d", help="Reports directory")
):
    """Show reports summary statistics"""
    config = CLIConfig.load()
    reports_dir = Path(directory) if directory else Path(config.default_output_dir)

    if not reports_dir.exists():
        console.print(f"❌ Reports directory not found: {reports_dir}", style="red")
        raise typer.Exit(1)

    # Gather statistics
    stats = {
        "total_files": 0,
        "total_size": 0,
        "by_format": {},
        "by_age": {"last_7_days": 0, "last_30_days": 0, "older": 0}
    }

    import time
    current_time = time.time()
    week_ago = current_time - (7 * 24 * 60 * 60)
    month_ago = current_time - (30 * 24 * 60 * 60)

    for pattern in ["*.md", "*.json", "*.pdf"]:
        for report_file in reports_dir.glob(pattern):
            stat = report_file.stat()
            file_format = report_file.suffix[1:].upper() if report_file.suffix else "Unknown"

            stats["total_files"] += 1
            stats["total_size"] += stat.st_size

            # By format
            stats["by_format"][file_format] = stats["by_format"].get(file_format, 0) + 1

            # By age
            if stat.st_mtime > week_ago:
                stats["by_age"]["last_7_days"] += 1
            elif stat.st_mtime > month_ago:
                stats["by_age"]["last_30_days"] += 1
            else:
                stats["by_age"]["older"] += 1

    # Display summary
    summary_panel = Panel(
        f"""📊 **Total Reports**: {stats['total_files']}
💾 **Total Size**: {format_file_size(stats['total_size'])}
📁 **Directory**: {reports_dir}""",
        title="📈 Reports Summary",
        border_style="blue"
    )

    console.print(summary_panel)

    # Format breakdown
    if stats["by_format"]:
        format_table = Table(title="By Format")
        format_table.add_column("Format", style="bold")
        format_table.add_column("Count", style="green")

        for file_format, count in stats["by_format"].items():
            format_table.add_row(file_format, str(count))

        console.print(format_table)

    # Age breakdown
    age_table = Table(title="By Age")
    age_table.add_column("Period", style="bold")
    age_table.add_column("Count", style="green")

    age_table.add_row("Last 7 days", str(stats["by_age"]["last_7_days"]))
    age_table.add_row("Last 30 days", str(stats["by_age"]["last_30_days"]))
    age_table.add_row("Older than 30 days", str(stats["by_age"]["older"]))

    console.print(age_table)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def format_timestamp(timestamp: float) -> str:
    """Format timestamp in human readable format"""
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M")


def export_to_pdf(source_path: Path, output_path: Path):
    """Export report to PDF (placeholder implementation)"""
    # This would require a library like weasyprint or reportlab
    # For now, just copy the file and show a message
    console.print("⚠️  PDF export not yet implemented. Use markdown2pdf or similar tool.", style="yellow")
    console.print(f"Source: {source_path}")
    raise typer.Exit(1)


def export_to_json(source_path: Path, output_path: Path):
    """Export report to JSON format"""
    # Convert markdown to structured JSON
    with open(source_path, encoding='utf-8') as f:
        content = f.read()

    # Simple parsing - could be enhanced with proper markdown parser
    import json
    structured_data = {
        "source_file": str(source_path),
        "exported_at": format_timestamp(time.time()),
        "content": content,
        "format": "markdown_to_json"
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2)


def export_to_markdown(source_path: Path, output_path: Path):
    """Export/copy to markdown format"""
    import shutil
    shutil.copy2(source_path, output_path)
