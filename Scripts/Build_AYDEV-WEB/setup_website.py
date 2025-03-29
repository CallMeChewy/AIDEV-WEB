#!/usr/bin/env python3
# File: setup_website.py
# Path: ProjectHimalaya/setup_website.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  3:45PM
# Description: Automates the setup of Project Himalaya website infrastructure

"""
Project Himalaya Website Setup Script

This script automates the creation of the website infrastructure for Project Himalaya.
It sets up the GitHub Pages directory structure, creates necessary configuration files,
and initializes the basic content structure.
"""

import os
import shutil
import argparse
import json
import yaml
from pathlib import Path
import re

class WebsiteSetup:
    """Handles the setup of the Project Himalaya website infrastructure."""
    
    def __init__(self, BaseDir: str, ConfigPath: str = None, Artifacts: list = None):
        """Initialize the website setup tool."""
        self.BaseDir = Path(BaseDir)
        self.DocsDir = self.BaseDir / "docs"
        self.GithubDir = self.BaseDir / ".github" / "workflows"
        self.ArtifactsDir = Path("artifacts") if Artifacts is None else Path(Artifacts)
        self.Config = self.LoadConfig(ConfigPath)
        
    def LoadConfig(self, ConfigPath: str = None) -> dict:
        """Load configuration from file or use default."""
        if ConfigPath and os.path.exists(ConfigPath):
            with open(ConfigPath, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            "domain": "projecthimalaya.com",
            "repository": "CallMeChewy/ProjectHimalaya",
            "author": "Herbert J. Bowers",
            "theme": "just-the-docs",
            "primary_color": "#4575b4"
        }
    
    def CreateDirectoryStructure(self) -> None:
        """Create the necessary directory structure for the website."""
        print("Creating directory structure...")
        
        # Create main directories
        Directories = [
            self.DocsDir,
            self.DocsDir / "_components",
            self.DocsDir / "_docs",
            self.DocsDir / "_docs" / "overview",
            self.DocsDir / "_docs" / "process",
            self.DocsDir / "_docs" / "status",
            self.DocsDir / "_includes",
            self.DocsDir / "_layouts",
            self.DocsDir / "_posts",
            self.DocsDir / "_sass",
            self.DocsDir / "_sass" / "color_schemes",
            self.DocsDir / "_standards",
            self.DocsDir / "assets",
            self.DocsDir / "assets" / "css",
            self.DocsDir / "assets" / "images",
            self.DocsDir / "assets" / "js",
            self.GithubDir
        ]
        
        for Dir in Directories:
            Dir.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {Dir}")
    
    def CopyArtifactToFile(self, ArtifactName: str, DestinationPath: Path) -> None:
        """Copy an artifact file to its destination."""
        ArtifactPath = self.ArtifactsDir / ArtifactName
        
        if ArtifactPath.exists():
            shutil.copy2(ArtifactPath, DestinationPath)
            print(f"  Copied: {ArtifactName} -> {DestinationPath}")
        else:
            print(f"  Warning: Artifact {ArtifactName} not found")
    
    def CreateConfigurationFiles(self) -> None:
        """Create the Jekyll configuration files."""
        print("Creating configuration files...")
        
        # Map artifacts to their destination paths
        FileMap = {
            "_config.yml": self.DocsDir / "_config.yml",
            "Gemfile": self.DocsDir / "Gemfile",
            "github-workflow.yml": self.GithubDir / "gh-pages.yml",
            "404.md": self.DocsDir / "404.md",
            "index.md": self.DocsDir / "index.md",
            "docs-overview.md": self.DocsDir / "_docs" / "index.md",
            "components-overview.md": self.DocsDir / "_components" / "index.md",
            "docs-readme.md": self.DocsDir / "README.md",
            "repo-readme.md": self.BaseDir / "README.md"
        }
        
        for ArtifactName, DestinationPath in FileMap.items():
            self.CopyArtifactToFile(ArtifactName, DestinationPath)
    
    def CreateCNAMEFile(self) -> None:
        """Create the CNAME file for custom domain."""
        print("Creating CNAME file...")
        
        CNAMEPath = self.DocsDir / "CNAME"
        with open(CNAMEPath, 'w') as f:
            f.write(self.Config["domain"])
        
        print(f"  Created: {CNAMEPath}")
    
    def CreateCustomTheme(self) -> None:
        """Create custom theme files."""
        print("Creating custom theme files...")
        
        # Create custom color scheme
        ThemePath = self.DocsDir / "_sass" / "color_schemes" / "himalaya.scss"
        with open(ThemePath, 'w') as f:
            f.write(f"""$link-color: {self.Config["primary_color"]};
$btn-primary-color: {self.Config["primary_color"]};
$body-background-color: #ffffff;
$sidebar-color: #f7f7f7;
$body-heading-color: #27374D;
""")
        
        print(f"  Created: {ThemePath}")
    
    def CreateSampleBlogPost(self) -> None:
        """Create a sample blog post."""
        print("Creating sample blog post...")
        
        PostsDir = self.DocsDir / "_posts"
        PostsDir.mkdir(parents=True, exist_ok=True)
        
        PostPath = PostsDir / "2025-03-28-website-launch.md"
        with open(PostPath, 'w') as f:
            f.write("""---
layout: post
title: "Project Himalaya Website Launch"
date: 2025-03-28
categories: news
---

Welcome to the new Project Himalaya website! This site will serve as the central hub for documentation, component status, and development updates.

## What's Included

The website provides access to:

- Project documentation
- Component specifications
- Development standards
- Current project status
- Development blog

## Next Steps

We're currently focusing on implementing the DocumentManager component, which will provide a foundation for storing and retrieving project documentation with rich metadata.

Stay tuned for more updates as the project develops!

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers
""")
        
        print(f"  Created: {PostPath}")
    
    def Setup(self) -> None:
        """Run the complete setup process."""
        print(f"Setting up Project Himalaya website in {self.BaseDir}")
        
        self.CreateDirectoryStructure()
        self.CreateConfigurationFiles()
        self.CreateCNAMEFile()
        self.CreateCustomTheme()
        self.CreateSampleBlogPost()
        
        print("\nWebsite setup complete!")
        print("\nNext steps:")
        print("1. Review the created files and customize if needed")
        print("2. Commit the changes to your GitHub repository")
        print("3. Configure GitHub Pages in repository settings")
        print("4. Set up your custom domain DNS")
        print("\nOnce GitHub Actions completes the build, your site will be available at:")
        print(f"https://{self.Config['domain']}")

def Main():
    """Main entry point for the script."""
    Parser = argparse.ArgumentParser(description="Set up Project Himalaya website infrastructure")
    Parser.add_argument("--base-dir", dest="BaseDir", default=".", help="Base directory for the repository")
    Parser.add_argument("--config", dest="ConfigPath", help="Path to configuration JSON file")
    Parser.add_argument("--artifacts", dest="ArtifactsDir", help="Directory containing artifact files")
    
    Args = Parser.parse_args()
    
    Setup = WebsiteSetup(
        BaseDir=Args.BaseDir,
        ConfigPath=Args.ConfigPath,
        Artifacts=Args.ArtifactsDir
    )
    
    Setup.Setup()

if __name__ == "__main__":
    Main()
