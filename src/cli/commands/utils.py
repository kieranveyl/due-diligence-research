"""Utility functions for CLI commands"""

import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

# Graceful imports with fallbacks
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    # Fallback console class
    class Console:
        def print(self, *args, **kwargs):
            print(*args)

try:
    from src.config.settings import settings
    HAS_SETTINGS = True
except ImportError:
    HAS_SETTINGS = False
    # Fallback settings
    class MockSettings:
        openai_api_key = None
        exa_api_key = None
        anthropic_api_key = None
        langsmith_api_key = None
        has_openai_key = False
        has_exa_key = False
        has_anthropic_key = False
        has_langsmith_key = False
    settings = MockSettings()

try:
    from src.cli.models.config import CLIConfig
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False
    # Fallback config class
    class CLIConfig:
        def __init__(self):
            self.default_output_dir = "./reports"
            self.default_format = "markdown"
            self.confidence_threshold = 0.8
            self.max_sources = 50
        @classmethod
        def load(cls):
            return cls()
        def save(self):
            pass

console = Console()


def detect_entity_type(entity_name: str) -> str:
    """Auto-detect entity type from name"""
    entity_lower = entity_name.lower()

    # Company indicators
    company_patterns = [
        r'\b(corp|corporation|inc|incorporated|llc|ltd|limited|company|co)\b',
        r'\b(group|holdings|enterprises|solutions|technologies|tech)\b'
    ]

    for pattern in company_patterns:
        if re.search(pattern, entity_lower):
            return "company"

    # Person indicators (basic)
    if len(entity_name.split()) >= 2 and entity_name.istitle():
        return "person"

    # Default to company for ambiguous cases
    return "company"


def generate_report_path(entity_name: str, output_dir: str = None, custom_path: str = None) -> Path:
    """Generate smart report path with timestamp"""
    if custom_path:
        return Path(custom_path)

    if not output_dir:
        config = CLIConfig.load()
        output_dir = config.default_output_dir

    # Create reports directory
    reports_dir = Path(output_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    safe_name = re.sub(r'[^a-zA-Z0-9\-_]', '-', entity_name.lower())
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{safe_name}-{timestamp}.md"

    return reports_dir / filename


def validate_api_keys() -> dict[str, bool]:
    """Validate API key availability"""
    if not HAS_SETTINGS:
        return {"openai": False, "exa": False, "anthropic": False, "langsmith": False}

    validation_results = {}

    # Required keys
    validation_results["openai"] = getattr(settings, 'has_openai_key', False) if hasattr(settings, 'has_openai_key') else bool(getattr(settings, 'openai_api_key', None) and settings.openai_api_key != "your_openai_key_here")
    validation_results["exa"] = getattr(settings, 'has_exa_key', False) if hasattr(settings, 'has_exa_key') else bool(getattr(settings, 'exa_api_key', None) and settings.exa_api_key != "your_exa_key_here")

    # Optional keys
    validation_results["anthropic"] = getattr(settings, 'has_anthropic_key', False) if hasattr(settings, 'has_anthropic_key') else bool(getattr(settings, 'anthropic_api_key', None) and settings.anthropic_api_key != "your_anthropic_key_here")
    validation_results["langsmith"] = getattr(settings, 'has_langsmith_key', False) if hasattr(settings, 'has_langsmith_key') else bool(getattr(settings, 'langsmith_api_key', None) and settings.langsmith_api_key != "your_langsmith_key_here")

    return validation_results


def check_system_health():
    """Check system health and show status"""
    print("🔍 System Health Check\n")

    # API Keys validation
    api_status = validate_api_keys()

    if HAS_RICH:
        api_table = Table(title="API Keys Status")
        api_table.add_column("Service", style="bold")
        api_table.add_column("Status", justify="center")
        api_table.add_column("Required", justify="center")

        for service, is_valid in api_status.items():
            status_icon = "✅" if is_valid else "❌"
            required = "Yes" if service in ["openai", "exa"] else "No"
            api_table.add_row(service.title(), status_icon, required)

        console.print(api_table)
    else:
        print("API Keys Status:")
        for service, is_valid in api_status.items():
            status_icon = "✅" if is_valid else "❌"
            required = "Yes" if service in ["openai", "exa"] else "No"
            print(f"  {service.title()}: {status_icon} (Required: {required})")

    # Configuration check
    if HAS_CONFIG:
        config = CLIConfig.load()
        if HAS_RICH:
            config_table = Table(title="Configuration")
            config_table.add_column("Setting", style="bold")
            config_table.add_column("Value", style="green")

            config_table.add_row("Output Directory", config.default_output_dir)
            config_table.add_row("Default Format", config.default_format)
            config_table.add_row("Confidence Threshold", f"{config.confidence_threshold:.1%}")
            config_table.add_row("Max Sources", str(config.max_sources))

            console.print(config_table)
        else:
            print("\nConfiguration:")
            print(f"  Output Directory: {config.default_output_dir}")
            print(f"  Default Format: {config.default_format}")
            print(f"  Confidence Threshold: {config.confidence_threshold:.1%}")
            print(f"  Max Sources: {config.max_sources}")

    # Overall status
    required_keys_valid = api_status["openai"] and api_status["exa"]
    if required_keys_valid:
        print("\n✅ System Ready - All required APIs configured")
    else:
        print("\n❌ System Not Ready - Missing required API keys")
        print("💡 Add API keys to .env file or environment variables")


def create_session_id() -> str:
    """Generate unique session ID"""
    return str(uuid.uuid4())[:8]


def format_duration(seconds: float) -> str:
    """Format duration in human-readable form"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:.0f}m {secs:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {minutes:.0f}m"


def parse_scope_string(scope_str: str) -> list[str]:
    """Parse comma-separated scope string"""
    valid_scopes = {"financial", "legal", "osint", "verification", "research"}
    scopes = [s.strip().lower() for s in scope_str.split(",") if s.strip()]
    return [s for s in scopes if s in valid_scopes]


def get_scope_description(scope: str) -> str:
    """Get description for research scope"""
    descriptions = {
        "financial": "Financial analysis, SEC filings, market data",
        "legal": "Legal compliance, litigation, sanctions screening",
        "osint": "Digital footprint, social media, domain analysis",
        "verification": "Fact-checking, source validation, cross-referencing",
        "research": "General web research and background information"
    }
    return descriptions.get(scope, "Unknown scope")


def show_scope_selection() -> list[str]:
    """Interactive scope selection"""
    scope_options = {
        "financial": get_scope_description("financial"),
        "legal": get_scope_description("legal"),
        "osint": get_scope_description("osint"),
        "verification": get_scope_description("verification")
    }

    print("\n📋 Select Research Areas")
    print("Choose which types of analysis to perform:\n")

    selected = []
    for scope, description in scope_options.items():
        try:
            if HAS_RICH:
                from rich.prompt import Confirm
                if Confirm.ask(f"Include {scope} analysis? ({description})", default=True):
                    selected.append(scope)
            else:
                response = input(f"Include {scope} analysis? ({description}) [Y/n]: ").strip().lower()
                if response in ('', 'y', 'yes'):
                    selected.append(scope)
        except (EOFError, KeyboardInterrupt):
            break

    return selected if selected else ["financial", "legal"]  # Default fallback


def save_report_content(content: str, file_path: Path) -> bool:
    """Save report content to file"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Failed to save report: {e}")
        return False


def format_report_summary(results: dict[str, Any]) -> str:
    """Format research results into markdown report"""
    entity_name = results.get("entity_name", "Unknown Entity")
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    report = f"""# Due Diligence Report: {entity_name}
*Generated on {timestamp}*

## Executive Summary

{results.get('executive_summary', 'Comprehensive due diligence analysis completed.')}

## Research Scope
"""

    # Add scope details
    confidence_scores = results.get("confidence_scores", {})
    for scope in results.get("scopes", []):
        if isinstance(confidence_scores, dict):
            confidence = confidence_scores.get(scope, 0.0)
        else:
            confidence = 0.75  # Default confidence for demo mode

        status = "✅" if confidence > 0.8 else "⚠️" if confidence > 0.6 else "❌"
        report += f"- {status} **{scope.title()} Analysis** (Confidence: {confidence:.1%})\n"

    report += "\n## Key Findings\n\n"

    # Add findings from each scope
    findings = results.get("findings", {})
    if findings:
        for scope, scope_findings in findings.items():
            if scope_findings:
                report += f"### {scope.title()} Analysis\n\n"
                if isinstance(scope_findings, dict):
                    for key, value in scope_findings.items():
                        if isinstance(value, list):
                            report += f"- **{key.replace('_', ' ').title()}**:\n"
                            for item in value:
                                report += f"  - {item}\n"
                        else:
                            report += f"- **{key.replace('_', ' ').title()}**: {value}\n"
                elif isinstance(scope_findings, list):
                    for finding in scope_findings:
                        report += f"- {finding}\n"
                else:
                    report += f"{scope_findings}\n"
                report += "\n"

    # Add sources and citations
    citations = results.get("citations", [])
    if citations:
        report += "## Sources & Citations\n\n"
        for i, citation in enumerate(citations, 1):
            report += f"{i}. {citation}\n"

    # Add metadata
    sources_count = results.get('sources_count', len(citations))
    overall_confidence = results.get('overall_confidence', 0.0)
    duration = results.get('duration', 0)
    session_id = results.get('session_id', 'N/A')

    report += f"""
## Research Metadata

- **Total Sources**: {sources_count}
- **Overall Confidence**: {overall_confidence:.1%}
- **Duration**: {format_duration(duration)}
- **Session ID**: {session_id}

---

*Report generated by Due Diligence CLI - Multi-Agent AI Research Tool*
"""

    return report
