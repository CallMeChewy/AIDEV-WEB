#!/usr/bin/env python3
# File: activate_venv.py
# Path: AIDEV-WEB/activate_venv.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  08:48PM
# Description: Helper script to activate virtual environment
# Author: Claude (Anthropic), as part of Project Himalaya
# Human Collaboration: Herbert J. Bowers

"""
Virtual Environment Activation Script

This script provides commands to activate the virtual environment
based on the current shell. Run this script with 'source'.
"""

import os
import sys
from pathlib import Path

def main():
    """Print activation commands based on current shell."""
    # Get the project base directory
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / ".venv"

    # Check if venv exists
    if not venv_dir.exists():
        print(f"Error: Virtual environment not found at {venv_dir}")
        return 1

    # Detect shell
    shell = os.environ.get('SHELL', '')
    if 'bash' in shell or 'zsh' in shell:
        # Bash or Zsh
        print(f"# Run this command to activate the virtual environment:")
        print(f"source {venv_dir}/bin/activate")
    elif 'fish' in shell:
        # Fish shell
        print(f"# Run this command to activate the virtual environment:")
        print(f"source {venv_dir}/bin/activate.fish")
    elif 'csh' in shell:
        # Csh
        print(f"# Run this command to activate the virtual environment:")
        print(f"source {venv_dir}/bin/activate.csh")
    elif os.name == 'nt':
        # Windows
        print(f"# Run this command to activate the virtual environment:")
        print(f"{venv_dir}\\Scripts\\activate") # Escaped backslash for Windows path
    else:
        print(f"# To activate the virtual environment, use one of these commands:")
        print(f"# Bash/Zsh: source {venv_dir}/bin/activate")
        print(f"# Fish: source {venv_dir}/bin/activate.fish")
        print(f"# Csh: source {venv_dir}/bin/activate.csh")
        print(f"# Windows: {venv_dir}\\Scripts\\activate") # Escaped backslash

    return 0

if __name__ == "__main__":
    sys.exit(main())
