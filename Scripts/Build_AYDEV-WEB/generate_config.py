#!/usr/bin/env python3
# File: generate_config.py
# Path: ProjectHimalaya/generate_config.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  3:45PM
# Description: Generates configuration files for Project Himalaya website

"""
Project Himalaya Configuration Generator

This script generates all the necessary configuration files for the Project Himalaya website.
It creates Jekyll configuration, GitHub Actions workflow, and essential content files.
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
import argparse

class ConfigGenerator:
    """Generates configuration files for Project Himalaya website."""
    
    def __init__(self, OutputDir: str, ConfigData: dict = None):
        """Initialize the configuration generator."""
        self.OutputDir = Path(OutputDir)
        self.OutputDir.mkdir(parents=True, exist_ok=True)
        
        # Default configuration if none provided
        self.Config = ConfigData if ConfigData else {
            "title": "Project Himalaya",
            "description": "A comprehensive framework for AI-human collaborative development",
            "url": "https://projecthimalaya.com",
            "repository": "CallMeChewy/ProjectHimalaya",
            "author": "Herbert J. Bowers",
            "theme": "just-the-docs",
            "primary_color": "#4575b4"
        }
        
        self.Timestamp = datetime.now().strftime("%B %d, %Y  %I:%M%p")
        self.Date = datetime.now().strftime("%Y-%m-%d")
    
    def GenerateJekyllConfig(self) -> None:
        """Generate Jekyll _config.yml file."""
        print("Generating Jekyll configuration...")
        
        ConfigData = {
            "title": self.Config["title"],
            "description": self.Config["description"],
            "baseurl": "",
            "url": self.Config["url"],
            "github_username": self.Config["repository"].split("/")[0],
            "repository": self.Config["repository"],
            "markdown": "kramdown",
            "remote_theme": "just-the-docs/just-the-docs",
            "plugins": [
                "jekyll-feed",
                "jekyll-seo-tag",
                "jekyll-sitemap",
                "jekyll-redirect-from"
            ],
            "color_scheme": "himalaya",
            "search_enabled": True,
            "search": {
                "heading_level": 3,
                "previews": 3,
                "preview_words_before": 5,
                "preview_words_after": 10,
                "tokenizer_separator": r"/[\s/]+/",
                "rel_url": True,
                "button": False
            },
            "aux_links": {
                f"{self.Config['title']} on GitHub": [
                    f"//github.com/{self.Config['repository']}"
                ]
            },
            "footer_content": f"Copyright &copy; {datetime.now().year} {self.Config['author']}. Distributed under an MIT license.",
            "collections": {
                "docs": {
                    "permalink": "/:collection/:path/",
                    "output": True
                },
                "components": {
                    "permalink": "/:collection/:path/",
                    "output": True
                },
                "standards": {
                    "permalink": "/:collection/:path/",
                    "output": True
                }
            },
            "defaults": [
                {
                    "scope": {
                        "path": "",
                        "type": "docs"
                    },
                    "values": {
                        "layout": "default",
                        "nav_order": 1
                    }
                },
                {
                    "scope": {
                        "path": "",
                        "type": "components"
                    },
                    "values": {
                        "layout": "default",
                        "nav_order": 2
                    }
                },
                {
                    "scope": {
                        "path": "",
                        "type": "standards"
                    },
                    "values": {
                        "layout": "default",
                        "nav_order": 3
                    }
                },
                {
                    "scope": {
                        "path": "",
                        "type": "pages"
                    },
                    "values": {
                        "layout": "default",
                        "nav_order": 4
                    }
                }
            ],
            "back_to_top": True,
            "back_to_top_text": "Back to top",
            "ga_tracking": "",
            "ga_tracking_anonymize_ip": True
        }
        
        OutputPath = self.OutputDir / "_config.yml"
        with open(OutputPath, 'w') as f:
            f.write("# _config.yml\n")
            f.write("# Jekyll configuration for Project Himalaya website\n\n")
            f.write("# Site settings\n")
            yaml.dump(ConfigData, f, sort_keys=False, default_flow_style=False)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateGemfile(self) -> None:
        """Generate Gemfile for Ruby dependencies."""
        print("Generating Gemfile...")
        
        GemfileContent = """source "https://rubygems.org"

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
"""
        
        OutputPath = self.OutputDir / "Gemfile"
        with open(OutputPath, 'w') as f:
            f.write(GemfileContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateGitHubWorkflow(self) -> None:
        """Generate GitHub Actions workflow file."""
        print("Generating GitHub Actions workflow...")
        
        WorkflowContent = """name: Build and deploy Jekyll site to GitHub Pages

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
          bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          path: "docs/_site"

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
"""
        
        OutputPath = self.OutputDir / "github-workflow.yml"
        with open(OutputPath, 'w') as f:
            f.write(WorkflowContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateHomepage(self) -> None:
        """Generate homepage content."""
        print("Generating homepage...")
        
        HomepageContent = """---
layout: home
title: Project Himalaya
nav_order: 1
description: "A comprehensive framework for AI-human collaborative development"
permalink: /
---

# Project Himalaya
{: .fs-9 }

A comprehensive framework demonstrating optimal AI-human collaboration, manifested through the development of practical applications that themselves leverage AI capabilities.
{: .fs-6 .fw-300 }

[Get Started](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/{repository}){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## The Vision

Project Himalaya aims to create a comprehensive framework demonstrating optimal AI-human collaboration, manifested through the development of practical applications that themselves leverage AI capabilities. This project acknowledges and embraces the constraints of current AI technology while pioneering new approaches to collaborative development.

### Dual-Purpose Goals

1. **Process Goal**: Establish effective methodologies for AI-human collaborative development that respect technological, resource, and personal constraints
2. **Product Goal**: Create useful, powerful applications that leverage AI capabilities while remaining accessible to the broader community

### Guiding Principles

- **Modularity**: No module exceeds 500 lines; clear separation of concerns
- **Documentation-Driven Development**: Documentation precedes implementation
- **Progressive Enhancement**: Start with core functionality, then expand methodically
- **Knowledge Persistence**: Establish mechanisms to maintain context across development sessions
- **Systematic Testing**: Comprehensive testing approach integrated from the beginning

## Project Structure

Project Himalaya follows a layered architecture:

### Layer 1: Core Infrastructure
- **DocumentManager**: Document storage and retrieval with metadata
- **StateManager**: Session state persistence and context management
- **StandardsValidator**: Validation against AIDEV-PascalCase and other standards

### Layer 2: Communication Framework
- **TaskManager**: Task definition and tracking
- **AIInterface**: Communication with cloud and local AI systems
- **KnowledgeTransfer**: Knowledge packaging and transfer

### Layer 3: Development Tools
- **CodeGenerator**: Standards-compliant code generation
- **TestFramework**: Test case creation and execution
- **DocumentationGenerator**: Automated documentation creation

### Layer 4: Applications
- **OllamaModelEditor**: Tool for customizing and optimizing Ollama AI models
- **AIDEV-Deploy**: File deployment with validation and rollback

## Getting Started

This website provides comprehensive documentation for Project Himalaya, including:

- [Project Overview](/docs/overview/)
- [Component Documentation](/components/)
- [Design Standards](/standards/)
- [Development Process](/docs/process/)
- [Current Status](/docs/status/)

## Recent Updates

{% for post in site.posts limit:3 %}
- **{{ post.date | date: "%b %d, %Y" }}** - [{{ post.title }}]({{ post.url }})
{% endfor %}

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— {author}
""".format(repository=self.Config["repository"], author=self.Config["author"])
        
        OutputPath = self.OutputDir / "index.md"
        with open(OutputPath, 'w') as f:
            f.write(HomepageContent)
        
        print(f"  Created: {OutputPath}")
    
    def Generate404Page(self) -> None:
        """Generate 404 error page."""
        print("Generating 404 page...")
        
        PageContent = """---
layout: default
title: 404
permalink: /404.html
nav_exclude: true
search_exclude: true
---

# 404 - Page Not Found
{: .text-center .fs-9 }

The requested page could not be found.
{: .text-center .fs-6 .fw-300 }

[Return to Home]({{ site.baseurl }}){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 .text-center}

---

## Looking for something?

Here are some helpful links to get you back on track:

- [Project Overview]({{ site.baseurl }}/)
- [Documentation]({{ site.baseurl }}/docs/)
- [Components]({{ site.baseurl }}/components/)
- [Project on GitHub](https://github.com/{repository})

If you believe this is a broken link, please [create an issue](https://github.com/{repository}/issues/new) on our GitHub repository.
""".format(repository=self.Config["repository"])
        
        OutputPath = self.OutputDir / "404.md"
        with open(OutputPath, 'w') as f:
            f.write(PageContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateDocsOverview(self) -> None:
        """Generate documentation overview page."""
        print("Generating docs overview page...")
        
        DocsContent = """---
layout: default
title: Documentation
nav_order: 2
has_children: true
permalink: /docs/
---

# Project Himalaya Documentation
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Documentation Structure

The Project Himalaya Knowledge Database uses a hierarchical numbering system to organize all documents. This system ensures intuitive navigation and clear relationships between documents.

### Numbering Format

Documents follow this naming pattern:
```
[Series]-[Subseries] [Type]-[Topic].md
```

Example: `10-20 SCOPE-ProjectHimalaya.md`

- **Series (first two digits)**: Major category
- **Subseries (second two digits)**: Specific area within category
- **Type**: Document purpose (e.g., SPEC, PLAN, GUIDE)
- **Topic**: Subject matter

### Series Categories

| Series | Purpose | Key Documents |
|--------|---------|---------------|
| 00     | Status & Navigation | Current project status, document maps, active sessions |
| 10     | Vision & Scope | Project vision, scope definition, roadmap |
| 20     | Standards | Coding standards, design principles, documentation standards |
| 30     | Templates | Reusable document templates for various purposes |
| 40     | Knowledge Organization | Database structure, metadata standards, taxonomy |
| 50     | Implementation | Implementation plans and details for active components |
| 60     | Testing | Test plans, test cases, testing frameworks |
| 70     | Documentation | User guides, API documentation, tutorials |
| 80     | Session Archives | Historical development session records |
| 90     | Reference Materials | External references, research notes, examples |

## Core Documents

### Project Foundation

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| [STATUS-ProjectHimalaya](/docs/status/) | Current project status | Every session |
| [GUIDE-ActiveSessions](/docs/sessions/) | Tracks ongoing and recent sessions | Every session |
| [LOG-Decisions](/docs/decisions/) | Record of key project decisions | As decisions occur |
| [VISION-ProjectHimalaya](/docs/vision/) | Project vision and philosophy | Quarterly review |
| [SCOPE-ProjectHimalaya](/docs/scope/) | Comprehensive scope definition | Monthly review |
| [STANDARD-AIDEV-PascalCase](/standards/pascalcase/) | Coding standards | As needed |
| [STANDARD-FoundationDesignPrinciples](/standards/design-principles/) | Core design principles | Quarterly review |

### Implementation Documents

| Document | Purpose | Update Frequency |
|----------|---------|------------------|
| [IMPL-DocumentManager](/components/document-manager/) | DocumentManager implementation | As developed |
| [IMPL-StateManager](/components/state-manager/) | StateManager implementation | As developed |
| [IMPL-StandardsValidator](/components/standards-validator/) | StandardsValidator implementation | As developed |

## Navigation Guidance

### For First-Time Visitors

If you're new to this project, follow this sequence:

1. Review [Project Status](/docs/status/) for current status
2. Examine [Project Scope](/docs/scope/) for project scope
3. Study [Foundation Design Principles](/standards/design-principles/) for design principles
4. Check [Recent Sessions](/docs/sessions/) for previous session context
5. Refer to component documentation for current implementation details

## Cross-Referencing System

All documents use the following cross-referencing approaches:

1. **Document References**: Use bracketed document numbers, e.g., [10-20]
2. **Section References**: Use document number plus section, e.g., [10-20 §3.2]
3. **Decision References**: Use decision log ID, e.g., [DECISION-2025-03-22-1]
4. **Component References**: Use component name with layer, e.g., [Layer1_DocumentManager]
"""
        
        OutputPath = self.OutputDir / "docs-overview.md"
        with open(OutputPath, 'w') as f:
            f.write(DocsContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateComponentsOverview(self) -> None:
        """Generate components overview page."""
        print("Generating components overview page...")
        
        ComponentsContent = """---
layout: default
title: Components
nav_order: 3
has_children: true
permalink: /components/
---

# Project Himalaya Components
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Component Hierarchy

Project Himalaya follows a layered architecture with components organized into four layers:

![Component Hierarchy](/assets/images/component-hierarchy.svg)

## Layer 1: Core Infrastructure

The foundation layer providing essential infrastructure services for all other components.

| Component | Status | Progress | Description |
|-----------|--------|----------|-------------|
| [DocumentManager](/components/document-manager/) | Specification | 30% | Document storage and retrieval with metadata |
| [StateManager](/components/state-manager/) | Planning | 10% | Session state persistence and context management |
| [StandardsValidator](/components/standards-validator/) | Concept | 5% | Validation against AIDEV-PascalCase and other standards |

## Layer 2: Communication Framework

Enables communication between different components and AI systems.

| Component | Status | Progress | Description |
|-----------|--------|----------|-------------|
| TaskManager | Planned | 0% | Task definition and tracking |
| AIInterface | Planned | 0% | Communication with cloud and local AI systems |
| KnowledgeTransfer | Planned | 0% | Knowledge packaging and transfer |

## Layer 3: Development Tools

Tools that assist in the development process.

| Component | Status | Progress | Description |
|-----------|--------|----------|-------------|
| CodeGenerator | Planned | 0% | Standards-compliant code generation |
| TestFramework | Planned | 0% | Test case creation and execution |
| DocumentationGenerator | Planned | 0% | Automated documentation creation |

## Layer 4: Applications

End-user applications that demonstrate the capabilities of the framework.

| Component | Status | Progress | Description |
|-----------|--------|----------|-------------|
| OllamaModelEditor | Planning | 15% | Tool for customizing and optimizing Ollama AI models |
| AIDEV-Deploy | Planned | 0% | File deployment with validation and rollback |

## Current Development Focus

The current development focus is on Layer 1 (Core Infrastructure) components, following a bottom-up approach. The DocumentManager component is the current priority, with implementation planned to begin soon.

### Development Sequence

1. Complete DocumentManager implementation
2. Begin StateManager implementation
3. Start StandardsValidator development
4. Move to Layer 2 components

## Component Status Definitions

| Status | Description |
|--------|-------------|
| Concept | Initial idea and basic requirements defined |
| Planning | Detailed planning and specification in progress |
| Specification | Detailed specification completed |
| Implementation | Active development of the component |
| Testing | Component implemented and undergoing testing |
| Complete | Component fully implemented, tested, and documented |
| Maintenance | Component in maintenance mode with ongoing updates |
"""
        
        OutputPath = self.OutputDir / "components-overview.md"
        with open(OutputPath, 'w') as f:
            f.write(ComponentsContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateDocsReadme(self) -> None:
        """Generate README for docs directory."""
        print("Generating docs README...")
        
        ReadmeContent = """# Project Himalaya Website

This directory contains the source files for the Project Himalaya website, which is built using Jekyll and deployed via GitHub Pages.

## Local Development

### Prerequisites

1. Ruby (version 2.7.0 or higher)
2. Bundler
3. Git

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/{repository}.git
   cd ProjectHimalaya/docs
   ```

2. Install dependencies:
   ```
   bundle install
   ```

3. Run the Jekyll server:
   ```
   bundle exec jekyll serve
   ```

4. Open your browser and navigate to http://localhost:4000

### File Structure

- `_config.yml`: Jekyll configuration
- `index.md`: Homepage
- `_docs/`: Documentation pages
- `_components/`: Component documentation
- `_standards/`: Standards documentation
- `_posts/`: Blog posts
- `_layouts/`: Page templates
- `_includes/`: Reusable components
- `assets/`: CSS, JavaScript, and images

## Adding Content

### Documentation Pages

Add documentation pages in the `_docs` directory:

```markdown
---
layout: default
title: Document Title
parent: Parent Category
nav_order: 1
---

# Document Title

Content goes here...
```

### Component Documentation

Add component documentation in the `_components` directory:

```markdown
---
layout: default
title: Component Name
parent: Layer 1
nav_order: 1
---

# Component Name

Component documentation goes here...
```

### Blog Posts

Add blog posts in the `_posts` directory with the filename format `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Post Title"
date: YYYY-MM-DD
categories: update
---

Post content goes here...
```

## Deployment

The website is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment process is managed by GitHub Actions as defined in `.github/workflows/gh-pages.yml`.

## Custom Domain

The website is configured to use a custom domain. The domain is specified in the `CNAME` file.

## SEO

SEO is managed using the Jekyll SEO Tag plugin. Make sure each page has appropriate front matter:

```yaml
---
title: Page Title
description: Page description for SEO
---
```

## Contribution Guidelines

1. Create a branch for your changes
2. Make your changes
3. Test locally with `bundle exec jekyll serve`
4. Commit and push your changes
5. Submit a pull request

## References

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Just the Docs Theme](https://pmarsceill.github.io/just-the-docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
""".format(repository=self.Config["repository"])
        
        OutputPath = self.OutputDir / "docs-readme.md"
        with open(OutputPath, 'w') as f:
            f.write(ReadmeContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateRepoReadme(self) -> None:
        """Generate README for repository root."""
        print("Generating repository README...")
        
        ReadmeContent = """# Project Himalaya

![Project Himalaya Logo](docs/assets/images/logo.png)

[![GitHub Pages](https://github.com/{repository}/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/{repository}/actions/workflows/gh-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A comprehensive framework demonstrating optimal AI-human collaboration, manifested through the development of practical applications that themselves leverage AI capabilities.

## Project Vision

Project Himalaya aims to create a comprehensive framework for AI-human collaborative development while building practical applications like the OllamaModelEditor. The project follows a layered architecture with a focus on documentation-driven development and knowledge persistence.

### Key Features

- 📚 **Documentation-Driven Development**: Documentation precedes implementation
- 🧩 **Modular Architecture**: Clear separation of concerns with no module exceeding 500 lines
- 🔄 **Knowledge Persistence**: Mechanisms for maintaining context across development sessions
- 🧪 **Systematic Testing**: Comprehensive testing integrated from the beginning
- 🤝 **AI-Human Collaboration**: Optimized workflow between human creativity and AI capabilities

## Project Structure

Project Himalaya follows a layered architecture:

### Layer 1: Core Infrastructure
- **DocumentManager**: Document storage and retrieval with metadata
- **StateManager**: Session state persistence and context management
- **StandardsValidator**: Validation against AIDEV-PascalCase and other standards

### Layer 2: Communication Framework
- **TaskManager**: Task definition and tracking
- **AIInterface**: Communication with cloud and local AI systems
- **KnowledgeTransfer**: Knowledge packaging and transfer

### Layer 3: Development Tools
- **CodeGenerator**: Standards-compliant code generation
- **TestFramework**: Test case creation and execution
- **DocumentationGenerator**: Automated documentation creation

### Layer 4: Applications
- **OllamaModelEditor**: Tool for customizing and optimizing Ollama AI models
- **AIDEV-Deploy**: File deployment with validation and rollback

## Current Status

The project is currently in the foundation phase, focusing on Layer 1 components. The DocumentManager component is the current priority.

## Documentation

Project documentation is available at our website: [{domain}]({url})

The documentation follows a standardized structure:

| Series | Purpose | Key Documents |
|--------|---------|---------------|
| 00     | Status & Navigation | Current project status, document maps, active sessions |
| 10     | Vision & Scope | Project vision, scope definition, roadmap |
| 20     | Standards | Coding standards, design principles, documentation standards |
| 30     | Templates | Reusable document templates for various purposes |
| 40     | Knowledge Organization | Database structure, metadata standards, taxonomy |
| 50     | Implementation | Implementation plans and details for active components |
| 60     | Testing | Test plans, test cases, testing frameworks |
| 70     | Documentation | User guides, API documentation, tutorials |

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- SQLite 3.35+

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/{repository}.git
   cd ProjectHimalaya
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Development Process

We follow a documentation-driven, bottom-up development approach:

1. Create comprehensive component specification
2. Define interfaces and data models
3. Implement unit tests
4. Develop the component
5. Document implementation details
6. Integrate with other components

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- {author} (Project Creator)
- AI collaborators (Claude and others)

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— {author}
""".format(repository=self.Config["repository"], domain=self.Config["url"].replace("https://", ""), url=self.Config["url"], author=self.Config["author"])
        
        OutputPath = self.OutputDir / "repo-readme.md"
        with open(OutputPath, 'w') as f:
            f.write(ReadmeContent)
        
        print(f"  Created: {OutputPath}")
    
    def GenerateCustomCSSVariables(self) -> None:
        """Generate custom CSS variables."""
        print("Generating custom CSS variables...")
        
        CSSContent = """$himalaya-blue: {primary_color};
$himalaya-dark: #27374D;
$himalaya-light: #F7F7F7;

$link-color: $himalaya-blue;
$btn-primary-color: $himalaya-blue;
$body-background-color: #ffffff;
$sidebar-color: $himalaya-light;
$body-heading-color: $himalaya-dark;
""".format(primary_color=self.Config["primary_color"])
        
        # Skip creating this file in the initial generation
        # This will be created by the setup script
        print("  Note: Custom CSS will be created during setup")
    
    def GenerateAll(self) -> None:
        """Generate all configuration and content files."""
        print(f"Generating configuration files for Project Himalaya website...")
        print(f"Timestamp: {self.Timestamp}")
        print(f"Output directory: {self.OutputDir}")
        print("")
        
        self.GenerateJekyllConfig()
        self.GenerateGemfile()
        self.GenerateGitHubWorkflow()
        self.GenerateHomepage()
        self.Generate404Page()
        self.GenerateDocsOverview()
        self.GenerateComponentsOverview()
        self.GenerateDocsReadme()
        self.GenerateRepoReadme()
        self.GenerateCustomCSSVariables()
        
        # Generate metadata about files for setup script
        FileManifest = {
            "timestamp": self.Timestamp,
            "date": self.Date,
            "files": [
                "_config.yml",
                "Gemfile",
                "github-workflow.yml",
                "index.md",
                "404.md",
                "docs-overview.md",
                "components-overview.md",
                "docs-readme.md",
                "repo-readme.md"
            ]
        }
        
        ManifestPath = self.OutputDir / "manifest.json"
        with open(ManifestPath, 'w') as f:
            json.dump(FileManifest, f, indent=2)
        
        print(f"\nGenerated {len(FileManifest['files'])} files.")
        print(f"Manifest saved to: {ManifestPath}")
        print("\nTo use these files, run the setup_website.py script.")

def Main():
    """Main entry point for the script."""
    Parser = argparse.ArgumentParser(description="Generate configuration files for Project Himalaya website")
    Parser.add_argument("--output", dest="OutputDir", default="artifacts", help="Output directory for generated files")
    Parser.add_argument("--config", dest="ConfigPath", help="Path to configuration JSON file")
    
    Args = Parser.parse_args()
    
    # Load custom configuration if provided
    ConfigData = None
    if Args.ConfigPath and os.path.exists(Args.ConfigPath):
        with open(Args.ConfigPath, 'r') as f:
            ConfigData = json.load(f)
    
    Generator = ConfigGenerator(Args.OutputDir, ConfigData)
    Generator.GenerateAll()

if __name__ == "__main__":
    Main()
