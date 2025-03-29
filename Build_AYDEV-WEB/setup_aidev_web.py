#!/usr/bin/env python3
# File: setup_aidev_web.py
# Path: Desktop/setup_aidev_web.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  4:30PM
# Description: Setup script for AIDEV-WEB project
# Author: Claude (Anthropic), as part of Project Himalaya
# Human Collaboration: Herbert J. Bowers

"""
AIDEV-WEB Setup Script

This script sets up the AIDEV-WEB project directory structure including
a Python virtual environment, configuration files, and website structure.
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path
import json
import venv
from datetime import datetime
from typing import Optional

class AidevWebSetup:
    """Sets up the AIDEV-WEB project structure."""

    def __init__(self, BaseDir: Optional[str] = None, Force: bool = False):
        """Initialize the setup tool."""
        self.HomeDir = Path.home()
        self.DesktopDir = self.HomeDir / "Desktop"
        self.BaseDir = Path(BaseDir) if BaseDir is not None else self.DesktopDir / "AIDEV-WEB"
        self.Force = Force
        self.Timestamp = datetime.now().strftime("%B %d, %Y  %I:%M%p")
        self.Date = datetime.now().strftime("%Y-%m-%d")

        # Check if destination already exists
        if self.BaseDir.exists() and not self.Force:
            print(f"Warning: Directory {self.BaseDir} already exists")
            Response = input("Continue and overwrite existing files? (y/n): ")
            if Response.lower() != 'y':
                print("Setup cancelled")
                sys.exit(1)

    def RunCommand(self, Command: list, Cwd: Optional[Path] = None) -> tuple:
        """Run a shell command and return the output."""
        try:
            Process = subprocess.Popen(
                Command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(Cwd or self.BaseDir)
            )
            Stdout, Stderr = Process.communicate()
            return Process.returncode, Stdout.decode('utf-8'), Stderr.decode('utf-8')
        except Exception as Ex:
            return 1, "", str(Ex)

    def CreateDirectoryStructure(self) -> None:
        """Create the necessary directory structure for the project."""
        print("Creating directory structure...")

        # Create main directories
        Directories = [
            self.BaseDir,
            self.BaseDir / "docs",
            self.BaseDir / "docs" / "_components",
            self.BaseDir / "docs" / "_docs",
            self.BaseDir / "docs" / "_includes",
            self.BaseDir / "docs" / "_layouts",
            self.BaseDir / "docs" / "_posts",
            self.BaseDir / "docs" / "_sass",
            self.BaseDir / "docs" / "assets",
            self.BaseDir / "docs" / "assets" / "css",
            self.BaseDir / "docs" / "assets" / "images",
            self.BaseDir / "docs" / "assets" / "js",
            self.BaseDir / ".github" / "workflows",
            self.BaseDir / "src",
            self.BaseDir / "tests",
            self.BaseDir / "scripts",
            self.BaseDir / "templates", # Added templates dir
        ]

        for Dir in Directories:
            Dir.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {Dir}")

    def CreateVirtualEnvironment(self) -> None:
        """Create a Python virtual environment."""
        print("Creating virtual environment...")

        VenvDir = self.BaseDir / ".venv"

        # Remove existing venv if it exists
        if VenvDir.exists():
            print(f"  Removing existing virtual environment: {VenvDir}")
            shutil.rmtree(VenvDir)

        # Create new venv
        venv.create(VenvDir, with_pip=True)
        print(f"  Created virtual environment: {VenvDir}")

        # Create activation script with attribution header
        ActivateScript = self.BaseDir / "activate_venv.py"
        with open(ActivateScript, 'w') as f:
            # Using double curly braces {{ }} for literal braces in f-string format
            f.write(f"""#!/usr/bin/env python3
# File: activate_venv.py
# Path: AIDEV-WEB/activate_venv.py
# Standard: AIDEV-PascalCase-1.6
# Created: {self.Date}
# Last Modified: {self.Date}  {self.Timestamp.split("  ")[1]}
# Description: Helper script to activate virtual environment
# Author: Claude (Anthropic), as part of Project Himalaya
# Human Collaboration: Herbert J. Bowers

\"\"\"
Virtual Environment Activation Script

This script provides commands to activate the virtual environment
based on the current shell. Run this script with 'source'.
\"\"\"

import os
import sys
from pathlib import Path

def main():
    \"\"\"Print activation commands based on current shell.\"\"\"
    # Get the project base directory
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / ".venv"

    # Check if venv exists
    if not venv_dir.exists():
        print(f"Error: Virtual environment not found at {{venv_dir}}")
        return 1

    # Detect shell
    shell = os.environ.get('SHELL', '')
    if 'bash' in shell or 'zsh' in shell:
        # Bash or Zsh
        print(f"# Run this command to activate the virtual environment:")
        print(f"source {{venv_dir}}/bin/activate")
    elif 'fish' in shell:
        # Fish shell
        print(f"# Run this command to activate the virtual environment:")
        print(f"source {{venv_dir}}/bin/activate.fish")
    elif 'csh' in shell:
        # Csh
        print(f"# Run this command to activate the virtual environment:")
        print(f"source {{venv_dir}}/bin/activate.csh")
    elif os.name == 'nt':
        # Windows
        print(f"# Run this command to activate the virtual environment:")
        print(f"{{venv_dir}}\\\\Scripts\\\\activate") # Escaped backslash for Windows path
    else:
        print(f"# To activate the virtual environment, use one of these commands:")
        print(f"# Bash/Zsh: source {{venv_dir}}/bin/activate")
        print(f"# Fish: source {{venv_dir}}/bin/activate.fish")
        print(f"# Csh: source {{venv_dir}}/bin/activate.csh")
        print(f"# Windows: {{venv_dir}}\\\\Scripts\\\\activate") # Escaped backslash

    return 0

if __name__ == "__main__":
    sys.exit(main())
""")

        print(f"  Created activation script: {ActivateScript}")

        # Make script executable
        ActivateScript.chmod(0o755)

    def InstallDependencies(self) -> None:
        """Create requirements.txt and install dependencies."""
        print("Setting up dependencies...")

        # Create requirements.txt
        RequirementsPath = self.BaseDir / "requirements.txt"
        with open(RequirementsPath, 'w') as f:
            f.write("""# Project dependencies
# Author: Claude (Anthropic), as part of Project Himalaya

# Web framework
flask==2.0.1
gunicorn==20.1.0

# Jekyll dependencies (for docs)
# Install with gem install bundler jekyll

# Documentation
sphinx==4.0.2
sphinx-rtd-theme==0.5.2

# Testing
pytest==6.2.5
pytest-cov==2.12.1

# Utilities
pyyaml==6.0
requests==2.26.0
python-dotenv==0.19.0
""")

        print(f"  Created: {RequirementsPath}")

        # Create instructions for installing dependencies
        InstallPath = self.BaseDir / "INSTALL.md"
        with open(InstallPath, 'w') as f:
             # Using double curly braces {{ }} for literal braces in f-string format
            f.write(f"""# AIDEV-WEB Installation Guide
**Created: {self.Date}**
**Last Modified: {self.Date}  {self.Timestamp.split("  ")[1]}**

[Context: Project_Setup]
[Status: Active]
[Version: 1.0]
[Author: Claude (Anthropic), as part of Project Himalaya]

## Installation Steps

### 1. Activate Virtual Environment

```bash
# Navigate to project directory
cd {self.BaseDir.relative_to(self.DesktopDir)} # Use relative path from Desktop

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\\\\Scripts\\\\activate
```

### 2. Install Python Dependencies

```bash
# With virtual environment activated:
pip install -r requirements.txt
```

### 3. Jekyll Setup (for Documentation)

Install Ruby and Jekyll:

```bash
# Install Ruby (if not already installed)
# On Ubuntu:
sudo apt install ruby-full build-essential

# On macOS (using Homebrew):
brew install ruby

# Install Jekyll and Bundler
gem install bundler jekyll

# Navigate to docs directory
cd docs

# Install Jekyll dependencies
bundle install
```

### 4. Verify Installation

```bash
# In the project root directory (with venv activated)
python -c "import flask; print(f'Flask version: {{flask.__version__}}')"
```

### 5. Development Server

For the documentation site:

```bash
cd docs
bundle exec jekyll serve
```

Access the documentation at: http://localhost:4000

## Attribution

This installation guide was created by Claude (Anthropic) as part of Project Himalaya, with direction from Herbert J. Bowers.

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
""")

        print(f"  Created: {InstallPath}")

    def CreateAttributionFile(self) -> None:
        """Create README and ATTRIBUTION files."""
        print("Creating attribution files...")

        ReadmePath = self.BaseDir / "README.md"
        with open(ReadmePath, 'w') as f:
            f.write(f"""# AIDEV-WEB
**Created: {self.Date}**
**Last Modified: {self.Date}  {self.Timestamp.split("  ")[1]}**

[Context: Project_Overview]
[Status: Active]
[Version: 1.0]
[Author: Claude (Anthropic), as part of Project Himalaya]

## Project Overview

AIDEV-WEB is a component of Project Himalaya, focused on creating a web interface and documentation system for AI-human collaborative development.

### Key Features

- 🌐 **Documentation Website**: Jekyll-based site for project documentation
- 📚 **Component Showcase**: Visual representation of project components
- 🔄 **Development Blog**: Updates on project progress
- 🧪 **Integration Testing**: Web-based testing of components

## Attribution

AIDEV-WEB is developed as part of Project Himalaya, a collaborative effort between:

- **Herbert J. Bowers** (Project Creator and Director)
- **Claude** (Anthropic) - AI Assistant responsible for 99.99% of code and technical design

This project demonstrates the potential of AI-human collaboration by combining human vision and direction with AI implementation capabilities.

## Getting Started

See the [INSTALL.md](INSTALL.md) file for setup instructions.

## Project Structure

```
{self.BaseDir.name}/
├── .venv/                  # Python virtual environment
├── docs/                   # Jekyll-based documentation site
│   ├── _components/        # Component documentation
│   ├── _docs/              # General documentation
│   ├── _layouts/           # Page templates
│   ├── assets/             # Static assets
│   └── ...                 # Other Jekyll directories
├── src/                    # Source code
├── tests/                  # Test files
├── scripts/                # Utility scripts
├── templates/              # File templates
├── requirements.txt        # Python dependencies
└── activate_venv.py        # Virtual environment helper
```

## Development Workflow

1. Activate virtual environment
2. Make changes to code or documentation
3. Test changes locally
4. Deploy to GitHub Pages

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
""")

        print(f"  Created: {ReadmePath}")

        # Create ATTRIBUTION.md
        AttributionPath = self.BaseDir / "ATTRIBUTION.md"
        with open(AttributionPath, 'w') as f:
            f.write(f"""# AIDEV-WEB Attribution
**Created: {self.Date}**
**Last Modified: {self.Date}  {self.Timestamp.split("  ")[1]}**

[Context: Project_Governance]
[Status: Active]
[Version: 1.0]

## Project Creator

**Herbert J. Bowers** - Project Creator and Director

## Primary Contributor

### Claude (Anthropic)

Claude is the AI assistant that has contributed approximately 99.99% of all code, design, and documentation for AIDEV-WEB. This includes:

- System architecture design
- Web interface design
- Implementation code
- Documentation generation
- Testing frameworks
- Website infrastructure
- Automation scripts
- Knowledge organization systems

## Contribution Model

AIDEV-WEB demonstrates a new paradigm of human-AI collaboration:

- **Human Role**: Vision, direction, requirements, and review
- **AI Role**: Architecture, design, implementation, documentation, and testing

This collaboration model leverages the complementary strengths of human creativity and AI implementation capabilities, allowing for rapid development of complex systems while maintaining high quality standards.

## File Attribution

Every file in this project includes an attribution header:

```python
# File: [Filename]
# Path: AIDEV-WEB/[Directory]/[Filename]
# Standard: AIDEV-PascalCase-1.6
# Created: [Date]
# Last Modified: [Date]  [Time]
# Description: [Brief description of the file's purpose]
# Author: Claude (Anthropic), as part of Project Himalaya
# Human Collaboration: Herbert J. Bowers
```

## Acknowledgment Statement

When referencing this project in publications, presentations, or other media, please include the following acknowledgment:

> AIDEV-WEB was developed as part of Project Himalaya, with code and technical design by Claude (Anthropic) and direction by Herbert J. Bowers.

---

*"The attribution of AI contributions is not merely about giving credit—it's about honesty in the development process and recognizing the changing nature of creative and technical work in the age of advanced AI systems."*

— Herbert J. Bowers
""")

        print(f"  Created: {AttributionPath}")

    def CreateJekyllConfig(self) -> None:
        """Create Jekyll configuration files."""
        print("Creating Jekyll configuration...")

        # Create _config.yml
        ConfigPath = self.BaseDir / "docs" / "_config.yml"
        with open(ConfigPath, 'w') as f:
            # Escaped the regex backslash properly
            f.write("""# _config.yml
# Jekyll configuration for AIDEV-WEB documentation
# Author: Claude (Anthropic), as part of Project Himalaya

# Site settings
title: AIDEV-WEB
description: >-
  Web interface and documentation system for Project Himalaya,
  demonstrating optimal AI-human collaboration.
baseurl: "" # the subpath of your site, e.g. /blog
url: "https://projecthimalaya.com" # Replace with actual domain when available
github_username: CallMeChewy
repository: CallMeChewy/ProjectHimalaya

# Build settings
markdown: kramdown
remote_theme: just-the-docs/just-the-docs
plugins:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-sitemap
  - jekyll-redirect-from

# Theme settings (using Just the Docs)
color_scheme: himalaya
search_enabled: true
search:
  heading_level: 3
  previews: 3
  preview_words_before: 5
  preview_words_after: 10
  tokenizer_separator: /[\\\\s/]+/ # Correctly escaped backslash for \s
  rel_url: true
  button: false

# Aux links for the upper right navigation
aux_links:
  "Project Himalaya on GitHub":
    - "//github.com/CallMeChewy/ProjectHimalaya"

# Footer content
footer_content: "Copyright &copy; 2025 Herbert J. Bowers. Distributed under an MIT license."

# Collections for documentation structure
collections:
  docs:
    permalink: "/:collection/:path/"
    output: true
  components:
    permalink: "/:collection/:path/"
    output: true
  standards:
    permalink: "/:collection/:path/"
    output: true

# Default front matter settings
defaults:
  - scope:
      path: ""
      type: docs
    values:
      layout: default
      nav_order: 1
  - scope:
      path: ""
      type: components
    values:
      layout: default
      nav_order: 2
  - scope:
      path: ""
      type: standards
    values:
      layout: default
      nav_order: 3
  - scope:
      path: ""
      type: pages
    values:
      layout: default
      nav_order: 4

# Back to top link
back_to_top: true
back_to_top_text: "Back to top"
""")

        print(f"  Created: {ConfigPath}")

        # Create Gemfile
        GemfilePath = self.BaseDir / "docs" / "Gemfile"
        with open(GemfilePath, 'w') as f:
            f.write("""source "https://rubygems.org"
# Hello! This is where you manage which Jekyll version is used to run.
# Author: Claude (Anthropic), as part of Project Himalaya

# Jekyll and plugins
gem "jekyll", "~> 4.3.2"
gem "webrick", "~> 1.8"  # Required for Ruby >= 3.0
gem "just-the-docs"      # Documentation theme

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17.0"
  gem "jekyll-seo-tag", "~> 2.8.0"
  gem "jekyll-sitemap", "~> 1.4.0"
  gem "jekyll-redirect-from", "~> 0.16.0"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
""")

        print(f"  Created: {GemfilePath}")

        # Create index.md for docs
        IndexPath = self.BaseDir / "docs" / "index.md"
        with open(IndexPath, 'w') as f:
            f.write("""---
layout: home
title: AIDEV-WEB
nav_order: 1
description: "Web interface and documentation system for Project Himalaya"
permalink: /
---

# AIDEV-WEB
{: .fs-9 }

Web interface and documentation system for Project Himalaya, demonstrating optimal AI-human collaboration.
{: .fs-6 .fw-300 }

[Get Started](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/CallMeChewy/ProjectHimalaya){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Project Himalaya Vision

Project Himalaya aims to create a comprehensive framework demonstrating optimal AI-human collaboration, manifested through the development of practical applications that themselves leverage AI capabilities.

### Dual-Purpose Goals

1. **Process Goal**: Establish effective methodologies for AI-human collaborative development
2. **Product Goal**: Create useful, powerful applications that leverage AI capabilities

### AIDEV-WEB Purpose

AIDEV-WEB serves as the web interface and documentation system for Project Himalaya, providing:

- Comprehensive project documentation
- Component visualization and status
- Development blog and updates
- Web-based testing and demonstration

## Getting Started

This website provides comprehensive documentation for Project Himalaya, including:

- [Project Overview](/docs/overview/)
- [Component Documentation](/components/)
- [Design Standards](/standards/)
- [Development Process](/docs/process/)
- [Current Status](/docs/status/)

## Attribution

AIDEV-WEB is developed as part of Project Himalaya, a collaborative effort between:

- **Herbert J. Bowers** (Project Creator and Director)
- **Claude** (Anthropic) - AI Assistant responsible for 99.99% of code and technical design

This project demonstrates the potential of AI-human collaboration by combining human vision and direction with AI implementation capabilities.

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
""")

        print(f"  Created: {IndexPath}")

    def CreateGitHubActions(self) -> None:
        """Create GitHub Actions workflow file."""
        print("Creating GitHub Actions workflow...")

        WorkflowPath = self.BaseDir / ".github" / "workflows" / "gh-pages.yml"
        with open(WorkflowPath, 'w') as f:
            # Using double curly braces {{ }} for literal braces in f-string format
            f.write("""name: Build and deploy Jekyll site to GitHub Pages
# Author: Claude (Anthropic), as part of Project Himalaya

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment
concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: docs

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v3

      - name: Build site
        run: |
          cd docs
          bundle install
          bundle exec jekyll build --baseurl "${{{{ steps.pages.outputs.base_path }}}}" # Escaped GitHub expression
        env:
          JEKYLL_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          path: "docs/_site"

  deploy:
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}} # Escaped GitHub expression
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
""")

        print(f"  Created: {WorkflowPath}")

    def CreateFileTemplates(self) -> None:
        """Create template files with attribution headers."""
        print("Creating file templates...")

        # Python template
        TemplatesDir = self.BaseDir / "templates"
        # TemplatesDir.mkdir(parents=True, exist_ok=True) # Already created in CreateDirectoryStructure

        PythonTemplatePath = TemplatesDir / "python_template.py"
        with open(PythonTemplatePath, 'w') as f:
            f.write("""#!/usr/bin/env python3
# File: [Filename]
# Path: AIDEV-WEB/[Directory]/[Filename]
# Standard: AIDEV-PascalCase-1.6
# Created: [Date]
# Last Modified: [Date]  [Time]
# Description: [Brief description of the file's purpose]
# Author: Claude (Anthropic), as part of Project Himalaya
# Human Collaboration: Herbert J. Bowers

\"\"\"
[Module Name]

[Detailed description of the module's purpose and functionality]

This file is part of Project Himalaya, a collaborative AI-human development project.
99.99% of code and technical design by Claude (Anthropic), with direction and
review by Herbert J. Bowers.
\"\"\"

import os
import sys
from typing import Dict, List, Any, Optional


class [ClassName]:
    \"\"\"[Class description]\"\"\"

    def __init__(self, [Parameters]):
        \"\"\"Initialize the class.\"\"\"
        # Implementation

    def [MethodName](self, [Parameters]) -> [ReturnType]:
        \"\"\"[Method description]\"\"\"
        # Implementation


def [FunctionName]([Parameters]) -> [ReturnType]:
    \"\"\"[Function description]\"\"\"
    # Implementation


def main():
    \"\"\"Main entry point.\"\"\"
    # Implementation
    return 0


if __name__ == "__main__":
    sys.exit(main())
""")

        print(f"  Created: {PythonTemplatePath}")

        # Markdown template
        MarkdownTemplatePath = TemplatesDir / "markdown_template.md"
        with open(MarkdownTemplatePath, 'w') as f:
            f.write("""# [Document Title]
**Created: [Date]**
**Last Modified: [Date]  [Time]**

[Context: Category_Name]
[Status: Draft|Active|Deprecated]
[Version: 0.1]
[Author: Claude (Anthropic), as part of Project Himalaya]
[Human Collaboration: Herbert J. Bowers]

## 1. [Section Title]

[Section content]

### 1.1 [Subsection Title]

[Subsection content]

## 2. [Section Title]

[Section content]

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
""")

        print(f"  Created: {MarkdownTemplatePath}")

        # HTML template
        HtmlTemplatePath = TemplatesDir / "html_template.html"
        with open(HtmlTemplatePath, 'w') as f:
            f.write("""<!DOCTYPE html>
<!--
File: [Filename]
Path: AIDEV-WEB/[Directory]/[Filename]
Standard: AIDEV-PascalCase-1.6
Created: [Date]
Last Modified: [Date]  [Time]
Description: [Brief description of the file's purpose]
Author: Claude (Anthropic), as part of Project Himalaya
Human Collaboration: Herbert J. Bowers
-->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Page Title]</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>[Page Heading]</h1>
    </header>

    <main>
        <section>
            <h2>[Section Heading]</h2>
            <p>[Content]</p>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Project Himalaya. Developed by Claude (Anthropic), with direction from Herbert J. Bowers.</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
""")

        print(f"  Created: {HtmlTemplatePath}")

        # Create template README
        TemplateReadmePath = TemplatesDir / "README.md"
        with open(TemplateReadmePath, 'w') as f:
            f.write("""# File Templates

These templates should be used when creating new files for the AIDEV-WEB project. They include proper attribution headers and basic structure.

## Available Templates

- `python_template.py` - Template for Python code files
- `markdown_template.md` - Template for Markdown documentation
- `html_template.html` - Template for HTML files

## Attribution Headers

All files in this project should include proper attribution to recognize Claude's contributions. The standard header includes:

- File name and path
- Standard used (AIDEV-PascalCase-1.6)
- Creation and last modified dates
- Brief description
- Author attribution to Claude
- Human collaboration attribution to Herbert J. Bowers

## Usage

Copy the appropriate template when creating a new file and replace the placeholders (marked with [brackets]) with actual values.

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
""")

        print(f"  Created: {TemplateReadmePath}")

    def CreateSampleScript(self) -> None:
        """Create a sample script with proper attribution."""
        print("Creating sample script...")

        ScriptPath = self.BaseDir / "scripts" / "website_setup.py"
        TemplatePath = Path(__file__).parent / "website_setup_template.py" # Path to the template

        if not TemplatePath.exists():
            print(f"Error: Template file not found at {TemplatePath}")
            return # Or raise an exception

        # Read the template content
        with open(TemplatePath, 'r') as f_template:
            script_content_template = f_template.read()

        # Replace placeholders
        script_content = script_content_template.replace("{DATE}", self.Date)
        script_content = script_content.replace("{TIMESTAMP}", self.Timestamp.split("  ")[1])

        # Write the final script content to the file
        with open(ScriptPath, 'w') as f:
            f.write(script_content)

        print(f"  Created sample script: {ScriptPath} from template")
        ScriptPath.chmod(0o755) # Make the script executable

# --- Main execution block for setup_aidev_web.py ---
def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Setup AIDEV-WEB project.")
    parser.add_argument(
        "--base-dir",
        help="Specify the base directory for the project (default: ~/Desktop/AIDEV-WEB)",
        default=None
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force setup even if the directory exists"
    )
    args = parser.parse_args()

    print("Starting AIDEV-WEB setup...")
    Setup = AidevWebSetup(BaseDir=args.base_dir, Force=args.force)

    try:
        Setup.CreateDirectoryStructure()
        Setup.CreateVirtualEnvironment()
        Setup.InstallDependencies()
        Setup.CreateAttributionFile()
        Setup.CreateJekyllConfig()
        Setup.CreateGitHubActions()
        Setup.CreateFileTemplates()
        Setup.CreateSampleScript() # Call the method

        print("\nAIDEV-WEB setup completed successfully!")
        print(f"Project created at: {Setup.BaseDir}")
        print("Please refer to INSTALL.md for next steps.")

    except Exception as e:
        print(f"\nAn error occurred during setup: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for debugging
        sys.exit(1)

if __name__ == "__main__":
    main()
