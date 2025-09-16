"""Configuration management commands"""


import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from src.cli.commands.utils import validate_api_keys
from src.cli.models.config import CLIConfig

console = Console()

# Create config subcommand
config_cmd = typer.Typer(help="⚙️ Manage configuration settings")


@config_cmd.command("show")
def show_config():
    """Display current configuration"""
    config = CLIConfig.load()

    # Configuration table
    config_table = Table(title="⚙️ Current Configuration")
    config_table.add_column("Setting", style="bold cyan")
    config_table.add_column("Value", style="green")
    config_table.add_column("Description", style="dim")

    # Output settings
    config_table.add_row("default_output_dir", config.default_output_dir, "Default reports directory")
    config_table.add_row("default_format", config.default_format, "Default output format")

    # Research settings
    config_table.add_row("default_scope", ", ".join(config.default_scope), "Default research areas")
    config_table.add_row("confidence_threshold", f"{config.confidence_threshold:.1%}", "Minimum confidence threshold")
    config_table.add_row("max_sources", str(config.max_sources), "Maximum sources per research")
    config_table.add_row("timeout", f"{config.timeout}s", "Research timeout")

    # Model settings
    config_table.add_row("model", config.model, "Default LLM model")
    config_table.add_row("parallel_tasks", str(config.parallel_tasks), "Max parallel tasks")

    # API settings
    config_table.add_row("auto_validate_keys", str(config.auto_validate_keys), "Auto-validate API keys")

    console.print(config_table)

    # API Keys status
    api_status = validate_api_keys()
    api_table = Table(title="🔑 API Keys Status")
    api_table.add_column("Service", style="bold")
    api_table.add_column("Status")
    api_table.add_column("Required")

    for service, is_valid in api_status.items():
        status_icon = "✅ Configured" if is_valid else "❌ Missing"
        required = "✅ Yes" if service in ["openai", "exa"] else "⚪ No"
        api_table.add_row(service.title(), status_icon, required)

    console.print(api_table)

    # Configuration file location
    config_path = CLIConfig.get_config_path()
    console.print(f"\n📁 Configuration file: [link]{config_path}[/link]")


@config_cmd.command("set")
def set_config(
    setting: str | None = typer.Argument(None, help="Setting to configure"),
    value: str | None = typer.Argument(None, help="New value"),
):
    """Set configuration values"""
    config = CLIConfig.load()

    if not setting:
        # Interactive configuration
        console.print("⚙️ [bold]Interactive Configuration[/bold]\n")

        # Output settings
        if Confirm.ask("Configure output settings?", default=True):
            new_output_dir = Prompt.ask("Default output directory", default=config.default_output_dir)
            config.default_output_dir = new_output_dir

            format_choices = ["markdown", "json", "pdf"]
            new_format = Prompt.ask("Default format", choices=format_choices, default=config.default_format)
            config.default_format = new_format

        # Research settings
        if Confirm.ask("Configure research settings?", default=True):
            scope_options = ["financial", "legal", "osint", "verification"]
            console.print(f"Available scopes: {', '.join(scope_options)}")
            scope_input = Prompt.ask("Default scope (comma-separated)", default=",".join(config.default_scope))
            config.default_scope = [s.strip() for s in scope_input.split(",")]

            threshold_input = Prompt.ask("Confidence threshold (0.0-1.0)", default=str(config.confidence_threshold))
            try:
                config.confidence_threshold = float(threshold_input)
            except ValueError:
                console.print("❌ Invalid threshold, keeping current value", style="yellow")

            sources_input = Prompt.ask("Max sources", default=str(config.max_sources))
            try:
                config.max_sources = int(sources_input)
            except ValueError:
                console.print("❌ Invalid max sources, keeping current value", style="yellow")

            timeout_input = Prompt.ask("Timeout (seconds)", default=str(config.timeout))
            try:
                config.timeout = int(timeout_input)
            except ValueError:
                console.print("❌ Invalid timeout, keeping current value", style="yellow")

        # Model settings
        if Confirm.ask("Configure model settings?", default=False):
            model_input = Prompt.ask("Default model", default=config.model)
            config.model = model_input

            parallel_input = Prompt.ask("Parallel tasks", default=str(config.parallel_tasks))
            try:
                config.parallel_tasks = int(parallel_input)
            except ValueError:
                console.print("❌ Invalid parallel tasks, keeping current value", style="yellow")

        config.save()
        console.print("✅ Configuration saved", style="green")

    else:
        # Direct setting configuration
        if not hasattr(config, setting):
            console.print(f"❌ Unknown setting: {setting}", style="red")
            console.print("Available settings: default_output_dir, default_format, default_scope, confidence_threshold, max_sources, timeout, model, parallel_tasks")
            raise typer.Exit(1)

        if not value:
            value = Prompt.ask(f"New value for {setting}")

        # Type conversion based on setting
        try:
            if setting == "confidence_threshold":
                value = float(value)
            elif setting in ["max_sources", "timeout", "parallel_tasks"]:
                value = int(value)
            elif setting == "default_scope":
                value = [s.strip() for s in value.split(",")]
            elif setting == "auto_validate_keys":
                value = value.lower() in ["true", "yes", "1", "on"]

            setattr(config, setting, value)
            config.save()
            console.print(f"✅ Set {setting} = {value}", style="green")

        except ValueError as e:
            console.print(f"❌ Invalid value for {setting}: {e}", style="red")
            raise typer.Exit(1)


@config_cmd.command("reset")
def reset_config(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation")
):
    """Reset configuration to defaults"""
    if not confirm:
        if not Confirm.ask("⚠️  Reset all configuration to defaults?", default=False):
            console.print("Configuration reset cancelled")
            return

    config = CLIConfig()
    config.save()
    console.print("✅ Configuration reset to defaults", style="green")


@config_cmd.command("validate")
def validate_config():
    """Validate current configuration and API keys"""
    console.print("🔍 [bold]Validating Configuration[/bold]\n")

    config = CLIConfig.load()
    validation_results = []

    # Validate output directory
    try:
        from pathlib import Path
        output_path = Path(config.default_output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        validation_results.append(("Output Directory", "✅", "Accessible"))
    except Exception as e:
        validation_results.append(("Output Directory", "❌", f"Error: {e}"))

    # Validate numeric settings
    if 0.0 <= config.confidence_threshold <= 1.0:
        validation_results.append(("Confidence Threshold", "✅", f"{config.confidence_threshold:.1%}"))
    else:
        validation_results.append(("Confidence Threshold", "❌", "Must be between 0.0 and 1.0"))

    if 1 <= config.max_sources <= 200:
        validation_results.append(("Max Sources", "✅", str(config.max_sources)))
    else:
        validation_results.append(("Max Sources", "❌", "Must be between 1 and 200"))

    if 60 <= config.timeout <= 3600:
        validation_results.append(("Timeout", "✅", f"{config.timeout}s"))
    else:
        validation_results.append(("Timeout", "❌", "Must be between 60 and 3600 seconds"))

    # Validate scope
    valid_scopes = {"financial", "legal", "osint", "verification", "research"}
    invalid_scopes = set(config.default_scope) - valid_scopes
    if not invalid_scopes:
        validation_results.append(("Default Scope", "✅", ", ".join(config.default_scope)))
    else:
        validation_results.append(("Default Scope", "❌", f"Invalid scopes: {invalid_scopes}"))

    # Create validation table
    table = Table(title="Configuration Validation")
    table.add_column("Setting", style="bold")
    table.add_column("Status", style="center")
    table.add_column("Details", style="dim")

    for setting, status, details in validation_results:
        table.add_row(setting, status, details)

    console.print(table)

    # API key validation
    api_status = validate_api_keys()
    console.print("\n🔑 [bold]API Keys Validation[/bold]")

    all_required_valid = api_status["openai"] and api_status["exa"]
    if all_required_valid:
        console.print("✅ All required API keys are configured", style="green")
    else:
        console.print("❌ Missing required API keys", style="red")
        if not api_status["openai"]:
            console.print("  - OpenAI API key missing", style="red")
        if not api_status["exa"]:
            console.print("  - Exa API key missing", style="red")

    # Optional keys
    optional_missing = []
    if not api_status["anthropic"]:
        optional_missing.append("Anthropic")
    if not api_status["langsmith"]:
        optional_missing.append("LangSmith")

    if optional_missing:
        console.print(f"⚠️  Optional API keys not configured: {', '.join(optional_missing)}", style="yellow")


@config_cmd.command("export")
def export_config(
    output_file: str | None = typer.Option(None, "--output", "-o", help="Output file path")
):
    """Export configuration to file"""
    config = CLIConfig.load()

    if not output_file:
        output_file = f"dd-config-export-{config.created_at if hasattr(config, 'created_at') else 'current'}.json"

    try:
        import json
        from pathlib import Path

        config_data = config.model_dump()
        output_path = Path(output_file)

        with open(output_path, 'w') as f:
            json.dump(config_data, f, indent=2)

        console.print(f"✅ Configuration exported to: {output_path}", style="green")

    except Exception as e:
        console.print(f"❌ Failed to export configuration: {e}", style="red")
        raise typer.Exit(1)


@config_cmd.command("import")
def import_config(
    config_file: str = typer.Argument(..., help="Configuration file to import"),
    merge: bool = typer.Option(False, "--merge", help="Merge with existing config instead of replacing")
):
    """Import configuration from file"""
    try:
        import json
        from pathlib import Path

        config_path = Path(config_file)
        if not config_path.exists():
            console.print(f"❌ Configuration file not found: {config_file}", style="red")
            raise typer.Exit(1)

        with open(config_path) as f:
            config_data = json.load(f)

        if merge:
            current_config = CLIConfig.load()
            # Update only provided fields
            for key, value in config_data.items():
                if hasattr(current_config, key):
                    setattr(current_config, key, value)
            current_config.save()
        else:
            # Replace entire configuration
            new_config = CLIConfig(**config_data)
            new_config.save()

        console.print(f"✅ Configuration {'merged' if merge else 'imported'} from: {config_path}", style="green")

    except Exception as e:
        console.print(f"❌ Failed to import configuration: {e}", style="red")
        raise typer.Exit(1)
