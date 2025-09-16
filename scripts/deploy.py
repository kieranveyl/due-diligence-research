#!/usr/bin/env python
"""Deployment script"""

import argparse
import subprocess


def run_command(command, check=True):
    """Run shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0

def deploy_local():
    """Deploy locally with Docker Compose"""
    commands = [
        "docker-compose build",
        "docker-compose up -d",
        "sleep 10",
        "curl -f http://localhost:8000/health || echo 'Health check failed'"
    ]

    for cmd in commands:
        if not run_command(cmd, check=False):
            print(f"Warning: {cmd} may have failed")

def run_tests():
    """Run test suite"""
    commands = [
        "uv run python -m pytest tests/ -v --tb=short",
        "uv run python -m pytest tests/ --cov=src --cov-report=html"
    ]

    for cmd in commands:
        if not run_command(cmd, check=False):
            print(f"Warning: {cmd} failed")

def main():
    parser = argparse.ArgumentParser(description="Deploy Due Diligence System")
    parser.add_argument("--env", choices=["local", "staging", "production"], default="local")
    parser.add_argument("--test", action="store_true", help="Run tests before deployment")

    args = parser.parse_args()

    if args.test:
        print("Running tests...")
        run_tests()

    if args.env == "local":
        print("Deploying locally...")
        deploy_local()
    else:
        print(f"Deployment to {args.env} not implemented yet")

if __name__ == "__main__":
    main()
