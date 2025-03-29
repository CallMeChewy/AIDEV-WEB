#!/usr/bin/env python3
# File: website_setup.py
# Path: AIDEV-WEB/scripts/website_setup.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  08:48PM
# Description: Script to set up the AIDEV-WEB documentation website
# Author: Claude (Anthropic), as part of Project Himalaya
# Human Collaboration: Herbert J. Bowers

"""
Website Setup Script

This script automates the setup and deployment of the AIDEV-WEB documentation website.
It creates the necessary directory structure, configuration files, and sets up GitHub Pages.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse
from datetime import datetime
from typing import Optional

class WebsiteSetup:
    """Handles the setup of the AIDEV-WEB documentation website."""

    # Corrected type hint for BaseDir
    def __init__(self, BaseDir: Optional[str] = None):
        """Initialize the website setup tool."""
        self.BaseDir = Path(BaseDir) if BaseDir else Path.cwd()
        self.DocsDir = self.BaseDir / "docs"

        # Check if docs directory exists
        if not self.DocsDir.exists():
            print(f"Error: Docs directory not found at {self.DocsDir}")
            sys.exit(1)

    def InstallJekyllDependencies(self) -> None:
        """Set up Jekyll dependencies for the documentation site."""
        print("Setting up Jekyll dependencies...")

        # Check if Gemfile exists
        GemfilePath = self.DocsDir / "Gemfile"
        if not GemfilePath.exists():
            print(f"Error: Gemfile not found at {GemfilePath}")
            print("Please create a Gemfile first using the main setup script.")
            return

        # Run bundle install
        try:
            print(f"Running 'bundle install' in {self.DocsDir}...")
            Result = subprocess.run(
                ["bundle", "install"],
                cwd=self.DocsDir,
                capture_output=True,
                text=True,
                check=True # Raise exception on non-zero exit code
            )
            print("  Jekyll dependencies installed successfully.")
            print(Result.stdout)
        except FileNotFoundError:
             print("  Error: 'bundle' command not found. Is Ruby/Bundler installed and in PATH?")
        except subprocess.CalledProcessError as Ex:
            print(f"  Error installing Jekyll dependencies (Return Code: {Ex.returncode}):")
            print(Ex.stderr)
        except Exception as Ex:
            print(f"  An unexpected error occurred: {str(Ex)}")
            print("  Make sure Ruby and Bundler are installed correctly.")

    def CreateCustomTheme(self) -> None:
        """Create custom theme files for Jekyll."""
        print("Creating custom theme files...")

        # Create _sass directory if it doesn't exist
        SassDir = self.DocsDir / "_sass"
        ColorSchemesDir = SassDir / "color_schemes"
        ColorSchemesDir.mkdir(parents=True, exist_ok=True)

        # Create custom color scheme
        ThemePath = ColorSchemesDir / "himalaya.scss"
        with open(ThemePath, 'w') as f_theme:
            f_theme.write("""// Himalaya theme for AIDEV-WEB
// Author: Claude (Anthropic), as part of Project Himalaya

$himalaya-blue: #4575b4;
$himalaya-dark: #27374D;
$himalaya-light: #F7F7F7;

$link-color: $himalaya-blue;
$btn-primary-color: $himalaya-blue;
$body-background-color: #ffffff;
$sidebar-color: $himalaya-light;
$body-heading-color: $himalaya-dark;
""")

        print(f"  Created: {ThemePath}")

        # Create custom styles
        CustomSassDir = SassDir / "custom"
        CustomSassDir.mkdir(parents=True, exist_ok=True)

        CustomCssPath = CustomSassDir / "custom.scss"
        with open(CustomCssPath, 'w') as f_css:
            f_css.write("""// Custom styles for AIDEV-WEB
// Author: Claude (Anthropic), as part of Project Himalaya

// Add your custom styles here
""")

        print(f"  Created: {CustomCssPath}")

    def CreateSampleBlogPost(self) -> None:
        """Create a sample blog post."""
        print("Creating sample blog post...")

        # Create _posts directory if it doesn't exist
        PostsDir = self.DocsDir / "_posts"
        PostsDir.mkdir(parents=True, exist_ok=True)

        # Get current date
        Today = datetime.now().strftime("%Y-%m-%d")

        # Create sample post
        PostPath = PostsDir / f"{Today}-welcome-to-aidev-web.md"
        with open(PostPath, 'w') as f_post:
            # Note: Using f-string here is correct as it's evaluated when this script runs
            f_post.write(f"""---
layout: post
title: Welcome to AIDEV-WEB!
date: {Today}
categories: project update
author: Claude (Anthropic)
---

## Welcome!

This is the first post on the AIDEV-WEB development blog.

AIDEV-WEB is the web interface and documentation hub for Project Himalaya,
a project focused on exploring optimal AI-human collaboration in software
development.

This site, built with Jekyll and the Just the Docs theme, serves as both
documentation and a demonstration of the collaborative process.

Stay tuned for more updates!

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods."*

— Herbert J. Bowers
""")
        print(f"  Created sample post: {PostPath}")

    def BuildSite(self) -> None:
        """Build the Jekyll site."""
        print("Building Jekyll site...")
        try:
            print(f"Running 'bundle exec jekyll build' in {self.DocsDir}...")
            Result = subprocess.run(
                ["bundle", "exec", "jekyll", "build"],
                cwd=self.DocsDir,
                capture_output=True,
                text=True,
                check=True,
                env={**os.environ, "JEKYLL_ENV": "production"}
            )
            print("  Site built successfully.")
            print(Result.stdout)
        except FileNotFoundError:
             print("  Error: 'bundle' or 'jekyll' command not found.")
        except subprocess.CalledProcessError as Ex:
            print(f"  Error building site (Return Code: {Ex.returncode}):")
            print(Ex.stderr)
        except Exception as Ex:
            print(f"  An unexpected error occurred during build: {str(Ex)}")

def main():
    """Main execution function for website_setup.py script."""
    parser = argparse.ArgumentParser(description="Setup and manage the AIDEV-WEB documentation website.")
    parser.add_argument(
        "--base-dir",
        help="Specify the project base directory (default: current directory)",
        default=None
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install Jekyll dependencies using bundle install"
    )
    parser.add_argument(
        "--create-theme",
        action="store_true",
        help="Create custom theme files"
    )
    parser.add_argument(
        "--create-post",
        action="store_true",
        help="Create a sample blog post"
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build the Jekyll site"
    )

    args = parser.parse_args()

    Setup = WebsiteSetup(BaseDir=args.base_dir)

    if args.install_deps:
        Setup.InstallJekyllDependencies()
    if args.create_theme:
        Setup.CreateCustomTheme()
    if args.create_post:
        Setup.CreateSampleBlogPost()
    if args.build:
        Setup.BuildSite()

    if not any([args.install_deps, args.create_theme, args.create_post, args.build]):
        print("No actions specified. Use --help for options.")
        print("Example: python scripts/website_setup.py --install-deps --build")

if __name__ == "__main__":
    main()
