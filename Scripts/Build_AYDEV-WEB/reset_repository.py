#!/usr/bin/env python3
# File: reset_repository.py
# Path: ProjectHimalaya/reset_repository.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  4:15PM
# Description: Reset Project Himalaya repository and create fresh structure
# Author: Claude (Anthropic), as part of Project Himalaya

"""
Project Himalaya Repository Reset Script

This script resets the repository to a clean state and sets up the initial
structure for Project Himalaya, including proper attribution to Claude.
"""

import os
import subprocess
import shutil
import argparse
from pathlib import Path
import json
from datetime import datetime

class RepositoryReset:
    """Handles the reset of the Project Himalaya repository."""
    
    def __init__(self, RepoDir: str, Force: bool = False):
        """Initialize the repository reset tool."""
        self.RepoDir = Path(RepoDir).resolve()
        self.Force = Force
        self.Timestamp = datetime.now().strftime("%B %d, %Y  %I:%M%p")
        
        # Path to SSH key
        self.SshKeyPath = Path.home() / ".ssh" / "id_rsa"
        
        # Check if this is a valid directory
        if not self.RepoDir.exists():
            raise ValueError(f"Directory {self.RepoDir} does not exist")
    
    def RunCommand(self, Command: list, Cwd: Path = None) -> tuple:
        """Run a shell command and return the output."""
        try:
            Process = subprocess.Popen(
                Command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(Cwd or self.RepoDir)
            )
            Stdout, Stderr = Process.communicate()
            return Process.returncode, Stdout.decode('utf-8'), Stderr.decode('utf-8')
        except Exception as Ex:
            return 1, "", str(Ex)
    
    def IsGitRepository(self) -> bool:
        """Check if the directory is a Git repository."""
        GitDir = self.RepoDir / ".git"
        return GitDir.exists() and GitDir.is_dir()
    
    def BackupImportantFiles(self) -> Path:
        """Backup important files before reset."""
        print("Backing up important files...")
        
        # Create backup directory
        BackupDir = self.RepoDir.parent / f"ProjectHimalaya_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        BackupDir.mkdir(parents=True, exist_ok=True)
        
        # Files/directories to backup
        BackupPaths = [
            # Add specific files or directories you want to preserve
        ]
        
        for Path in BackupPaths:
            SourcePath = self.RepoDir / Path
            if SourcePath.exists():
                DestPath = BackupDir / Path
                DestPath.parent.mkdir(parents=True, exist_ok=True)
                
                if SourcePath.is_file():
                    shutil.copy2(SourcePath, DestPath)
                else:
                    shutil.copytree(SourcePath, DestPath)
                
                print(f"  Backed up: {Path}")
        
        print(f"Backup created at: {BackupDir}")
        return BackupDir
    
    def CleanRepository(self) -> bool:
        """Clean the repository by removing all files except .git."""
        print("Cleaning repository...")
        
        if not self.IsGitRepository():
            print("Warning: Directory is not a Git repository")
            if not self.Force:
                Response = input("Continue anyway? This will delete all files in the directory. (y/n): ")
                if Response.lower() != 'y':
                    print("Operation cancelled")
                    return False
        
        # Get all items in the directory
        for Item in self.RepoDir.iterdir():
            if Item.name == ".git" and Item.is_dir():
                continue  # Skip .git directory
            
            try:
                if Item.is_file():
                    Item.unlink()
                    print(f"  Removed file: {Item.name}")
                elif Item.is_dir():
                    shutil.rmtree(Item)
                    print(f"  Removed directory: {Item.name}")
            except Exception as Ex:
                print(f"  Error removing {Item}: {str(Ex)}")
        
        print("Repository cleaned")
        return True
    
    def InitializeNewRepository(self) -> bool:
        """Initialize a new repository or reset the existing one."""
        print("Initializing repository...")
        
        if self.IsGitRepository():
            # Reset existing repository
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "checkout", "--orphan", "temp_branch"])
            if ReturnCode != 0:
                print(f"Error creating temporary branch: {Stderr}")
                return False
            
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "add", "-A"])
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "commit", "--allow-empty", "-m", "Initial commit: Fresh start for Project Himalaya"])
            if ReturnCode != 0:
                print(f"Error committing: {Stderr}")
                return False
            
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "branch", "-D", "main"])
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "branch", "-m", "main"])
            
            print("Repository reset to a clean state")
        else:
            # Initialize new repository
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "init"])
            if ReturnCode != 0:
                print(f"Error initializing repository: {Stderr}")
                return False
            
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "checkout", "-b", "main"])
            if ReturnCode != 0:
                print(f"Error creating main branch: {Stderr}")
                return False
            
            print("New repository initialized")
        
        return True
    
    def ConfigureRepository(self, RepoName: str = "ProjectHimalaya", UserName: str = "CallMeChewy") -> bool:
        """Configure the repository with GitHub information."""
        print("Configuring repository for GitHub...")
        
        # Set remote origin
        RepoUrl = f"git@github.com:{UserName}/{RepoName}.git"
        
        if self.IsGitRepository():
            # Check if remote exists
            ReturnCode, Stdout, Stderr = self.RunCommand(["git", "remote"])
            if "origin" in Stdout:
                ReturnCode, Stdout, Stderr = self.RunCommand(["git", "remote", "set-url", "origin", RepoUrl])
            else:
                ReturnCode, Stdout, Stderr = self.RunCommand(["git", "remote", "add", "origin", RepoUrl])
            
            if ReturnCode != 0:
                print(f"Error setting remote: {Stderr}")
                return False
            
            print(f"Remote set to: {RepoUrl}")
        else:
            print("Warning: Not a Git repository, skipping remote configuration")
            return False
        
        return True
    
    def CreateInitialReadme(self, AuthorName: str = "Herbert J. Bowers") -> bool:
        """Create an initial README.md with proper attribution."""
        print("Creating initial README.md...")
        
        ReadmePath = self.RepoDir / "README.md"
        with open(ReadmePath, 'w') as f:
            f.write(f"""# Project Himalaya

A comprehensive framework demonstrating optimal AI-human collaboration, manifested through the development of practical applications that themselves leverage AI capabilities.

## Attribution

Project Himalaya is a collaborative effort between:

- **Herbert J. Bowers** (Project Creator and Director)
- **Claude** (Anthropic) - AI Assistant responsible for 99.99% of code and technical design

This project demonstrates the potential of AI-human collaboration by combining human vision and direction with AI implementation capabilities.

## Project Vision

Project Himalaya aims to create a comprehensive framework for AI-human collaborative development while building practical applications like the OllamaModelEditor. The project follows a layered architecture with a focus on documentation-driven development and knowledge persistence.

### Key Features

- 📚 **Documentation-Driven Development**: Documentation precedes implementation
- 🧩 **Modular Architecture**: Clear separation of concerns with no module exceeding 500 lines
- 🔄 **Knowledge Persistence**: Mechanisms for maintaining context across development sessions
- 🧪 **Systematic Testing**: Comprehensive testing integrated from the beginning
- 🤝 **AI-Human Collaboration**: Optimized workflow between human creativity and AI capabilities

## Repository Status

This repository is currently being initialized with a clean structure. More documentation and code will be added soon.

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— {AuthorName}, Project Creator
""")
        
        print("README.md created with attribution to Claude")
        return True
    
    def CreateAttributionFile(self, AuthorName: str = "Herbert J. Bowers") -> bool:
        """Create a dedicated ATTRIBUTION.md file."""
        print("Creating ATTRIBUTION.md...")
        
        AttributionPath = self.RepoDir / "ATTRIBUTION.md"
        with open(AttributionPath, 'w') as f:
            f.write(f"""# Project Himalaya Attribution

## Project Creator

**Herbert J. Bowers** - Project Creator and Director

## Primary Contributors

### Claude (Anthropic)

Claude is the AI assistant that has contributed approximately 99.99% of all code, design, and documentation for Project Himalaya. This includes:

- System architecture design
- Component specifications
- Implementation code
- Documentation generation
- Testing frameworks
- Website infrastructure
- Automation scripts
- Knowledge organization systems

## Contribution Model

Project Himalaya demonstrates a new paradigm of human-AI collaboration:

- **Human Role**: Vision, direction, requirements, and review
- **AI Role**: Architecture, design, implementation, documentation, and testing

This collaboration model leverages the complementary strengths of human creativity and AI implementation capabilities, allowing for rapid development of complex systems while maintaining high quality standards.

## Acknowledgment

Every file in this project should include this line in its header:

```
# Author: Claude (Anthropic), as part of Project Himalaya
```

This acknowledgment reflects the core philosophy of Project Himalaya: transparency about AI contributions while showcasing the potential of human-AI collaboration.

---

*"The attribution of AI contributions is not merely about giving credit—it's about honesty in the development process and recognizing the changing nature of creative and technical work in the age of advanced AI systems."*

— {AuthorName}, Project Creator
""")
        
        print("ATTRIBUTION.md created")
        return True
    
    def CreateDirectoryStructure(self) -> bool:
        """Create the basic directory structure for the project."""
        print("Creating directory structure...")
        
        Directories = [
            "docs",                          # Website and documentation
            "src",                           # Source code
            "src/core",                      # Core infrastructure components
            "src/communication",             # Communication framework
            "src/tools",                     # Development tools
            "src/applications",              # Applications
            "tests",                         # Tests
            "scripts",                       # Utility scripts
            ".github/workflows",             # GitHub Actions workflows
        ]
        
        for DirPath in Directories:
            Path = self.RepoDir / DirPath
            Path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {DirPath}")
        
        print("Directory structure created")
        return True
    
    def CreateGitAttributes(self) -> bool:
        """Create .gitattributes file."""
        print("Creating .gitattributes...")
        
        Path = self.RepoDir / ".gitattributes"
        with open(Path, 'w') as f:
            f.write("""# Set default behavior to automatically normalize line endings
* text=auto

# Explicitly declare text files to be normalized
*.py text
*.md text
*.txt text
*.html text
*.css text
*.js text
*.json text
*.yml text
*.yaml text

# Declare files that will always have CRLF line endings
*.bat text eol=crlf

# Declare files that will always have LF line endings
*.sh text eol=lf

# Denote binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.svg binary
*.pdf binary
""")
        
        print(".gitattributes created")
        return True
    
    def CreateGitIgnore(self) -> bool:
        """Create .gitignore file."""
        print("Creating .gitignore...")
        
        Path = self.RepoDir / ".gitignore"
        with open(Path, 'w') as f:
            f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
venv/
.venv/
ENV/

# Jekyll
_site/
.sass-cache/
.jekyll-cache/
.jekyll-metadata
docs/.bundle/
docs/vendor/

# IDE and editors
.idea/
.vscode/
*.swp
*.swo
*~
.project
.classpath
.settings/

# OS specific
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
temp_artifacts/
artifacts/
*.db
*.sqlite
*.log
""")
        
        print(".gitignore created")
        return True
    
    def CommitInitialStructure(self) -> bool:
        """Commit the initial structure to the repository."""
        print("Committing initial structure...")
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "add", "."])
        if ReturnCode != 0:
            print(f"Error staging files: {Stderr}")
            return False
        
        CommitMessage = "Initial repository structure with proper attribution"
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "commit", "-m", CommitMessage])
        if ReturnCode != 0:
            print(f"Error committing: {Stderr}")
            return False
        
        print("Initial structure committed")
        return True
    
    def PushToGitHub(self) -> bool:
        """Push the repository to GitHub."""
        print("Pushing to GitHub...")
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "push", "-u", "origin", "main", "--force"])
        if ReturnCode != 0:
            print(f"Error pushing to GitHub: {Stderr}")
            return False
        
        print("Repository pushed to GitHub")
        return True
    
    def Reset(self) -> bool:
        """Perform the complete repository reset process."""
        print(f"Resetting Project Himalaya repository at {self.RepoDir}")
        
        # Confirm reset
        if not self.Force:
            print("\nWARNING: This will delete all files in the repository and create a new history.")
            print("All existing work will be lost unless already pushed to a remote.")
            Response = input("Are you sure you want to proceed? (y/n): ")
            if Response.lower() != 'y':
                print("Operation cancelled")
                return False
        
        # Backup important files
        BackupDir = self.BackupImportantFiles()
        
        # Clean repository
        if not self.CleanRepository():
            return False
        
        # Initialize new repository
        if not self.InitializeNewRepository():
            return False
        
        # Create directory structure
        if not self.CreateDirectoryStructure():
            return False
        
        # Create initial files
        if not self.CreateInitialReadme():
            return False
        
        if not self.CreateAttributionFile():
            return False
        
        if not self.CreateGitAttributes():
            return False
        
        if not self.CreateGitIgnore():
            return False
        
        # Configure repository
        if not self.ConfigureRepository():
            return False
        
        # Commit initial structure
        if not self.CommitInitialStructure():
            return False
        
        # Ask about pushing to GitHub
        if not self.Force:
            Response = input("Push changes to GitHub? This will overwrite remote history! (y/n): ")
            if Response.lower() != 'y':
                print("Changes committed locally but not pushed to GitHub")
                return True
        
        # Push to GitHub
        if not self.PushToGitHub():
            return False
        
        print("\nRepository reset complete!")
        print("\nNext steps:")
        print("1. Review the repository structure")
        print("2. Set up GitHub Pages in repository settings")
        print("3. Run the website setup script to create the website infrastructure")
        print("4. Add documentation and code to the repository")
        
        return True

def Main():
    """Main entry point for the script."""
    Parser = argparse.ArgumentParser(description="Reset Project Himalaya repository")
    Parser.add_argument("--repo", dest="RepoDir", default=".", help="Path to repository directory")
    Parser.add_argument("--force", dest="Force", action="store_true", help="Skip confirmation prompts")
    
    Args = Parser.parse_args()
    
    try:
        Resetter = RepositoryReset(
            RepoDir=Args.RepoDir,
            Force=Args.Force
        )
        
        Success = Resetter.Reset()
        return 0 if Success else 1
    
    except Exception as Ex:
        print(f"Error: {str(Ex)}")
        return 1

if __name__ == "__main__":
    Exit = Main()
    import sys
    sys.exit(Exit)
