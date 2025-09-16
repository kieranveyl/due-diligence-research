#!/usr/bin/env python
"""Setup script for development environment"""

import os
import subprocess
import sys


def run_command(command, check=True):
    """Run shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0

def setup_database():
    """Setup local database"""
    commands = [
        "docker-compose up -d postgres redis",
        "sleep 5",  # Wait for services
    ]

    for cmd in commands:
        if not run_command(cmd):
            print(f"Failed to run: {cmd}")
            return False
    return True

def setup_python_env():
    """Setup Python environment"""
    commands = [
        "uv sync --dev",
        "uv run python -m pytest tests/ --tb=short",  # Run quick test
    ]

    for cmd in commands:
        if not run_command(cmd, check=False):
            print(f"Warning: {cmd} failed")

def main():
    """Main setup function"""
    print("Setting up Due Diligence System...")

    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please copy .env.example to .env and configure.")
        sys.exit(1)

    # Setup database
    if setup_database():
        print("✅ Database services started")
    else:
        print("❌ Failed to start database services")
        sys.exit(1)

    # Setup Python environment
    setup_python_env()
    print("✅ Python environment configured")

    print("\n🎉 Setup complete!")
    print("Run: uv run uvicorn src.api.main:app --reload")

if __name__ == "__main__":
    main()
