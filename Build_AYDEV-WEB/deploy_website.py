#!/usr/bin/env python3
# File: deploy_website.py
# Path: ProjectHimalaya/deploy_website.py
# Standard: AIDEV-PascalCase-1.6
# Created: 2025-03-28
# Last Modified: 2025-03-28  3:45PM
# Description: Deploys the Project Himalaya website to GitHub Pages

"""
Project Himalaya Website Deployment Script

This script handles the deployment process for the Project Himalaya website.
It commits the website files to GitHub and triggers the GitHub Actions workflow.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json
from datetime import datetime

class WebsiteDeployer:
    """Handles the deployment of the Project Himalaya website."""
    
    def __init__(self, RepoDir: str, CommitMessage: str = None):
        """Initialize the website deployer."""
        self.RepoDir = Path(RepoDir)
        self.DocsDir = self.RepoDir / "docs"
        self.CommitMessage = CommitMessage or f"Update website: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Check if this is a Git repository
        if not (self.RepoDir / ".git").exists():
            raise ValueError(f"Directory {self.RepoDir} is not a Git repository")
        
        # Check if docs directory exists
        if not self.DocsDir.exists():
            raise ValueError(f"Docs directory {self.DocsDir} does not exist")
    
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
    
    def CheckGitStatus(self) -> tuple:
        """Check if there are uncommitted changes."""
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "status", "--porcelain"])
        
        if ReturnCode != 0:
            return False, f"Failed to check Git status: {Stderr}"
        
        HasChanges = len(Stdout.strip()) > 0
        return HasChanges, Stdout
    
    def StageChanges(self) -> bool:
        """Stage changes in the docs directory."""
        print("Staging changes in docs directory...")
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "add", "docs"])
        
        if ReturnCode != 0:
            print(f"Error staging changes: {Stderr}")
            return False
        
        print("  Changes staged successfully")
        return True
    
    def StageWorkflow(self) -> bool:
        """Stage GitHub Actions workflow file."""
        print("Staging GitHub Actions workflow...")
        
        WorkflowDir = self.RepoDir / ".github" / "workflows"
        if not WorkflowDir.exists():
            print("  Warning: Workflow directory does not exist")
            return False
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "add", ".github/workflows"])
        
        if ReturnCode != 0:
            print(f"Error staging workflow: {Stderr}")
            return False
        
        print("  Workflow staged successfully")
        return True
    
    def StageReadme(self) -> bool:
        """Stage README file."""
        print("Staging README file...")
        
        ReadmePath = self.RepoDir / "README.md"
        if not ReadmePath.exists():
            print("  Warning: README.md does not exist")
            return False
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "add", "README.md"])
        
        if ReturnCode != 0:
            print(f"Error staging README: {Stderr}")
            return False
        
        print("  README staged successfully")
        return True
    
    def CommitChanges(self) -> bool:
        """Commit the staged changes."""
        print(f"Committing changes with message: {self.CommitMessage}")
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "commit", "-m", self.CommitMessage])
        
        if ReturnCode != 0:
            print(f"Error committing changes: {Stderr}")
            return False
        
        print("  Changes committed successfully")
        return True
    
    def PushChanges(self) -> bool:
        """Push the committed changes to GitHub."""
        print("Pushing changes to GitHub...")
        
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "push"])
        
        if ReturnCode != 0:
            print(f"Error pushing changes: {Stderr}")
            return False
        
        print("  Changes pushed successfully")
        return True
    
    def GetCurrentBranch(self) -> str:
        """Get the name of the current Git branch."""
        ReturnCode, Stdout, Stderr = self.RunCommand(["git", "branch", "--show-current"])
        
        if ReturnCode != 0:
            print(f"Error getting current branch: {Stderr}")
            return "unknown"
        
        return Stdout.strip()
    
    def CheckGitHubActionsWorkflow(self) -> bool:
        """Check if the GitHub Actions workflow file exists."""
        WorkflowPath = self.RepoDir / ".github" / "workflows" / "gh-pages.yml"
        return WorkflowPath.exists()
    
    def Deploy(self) -> bool:
        """Deploy the website by committing and pushing changes."""
        print(f"Deploying Project Himalaya website from {self.RepoDir}")
        
        # Check current branch
        CurrentBranch = self.GetCurrentBranch()
        print(f"Current branch: {CurrentBranch}")
        
        if CurrentBranch != "main":
            Proceed = input("Warning: You are not on the main branch. Deployment may not trigger GitHub Actions. Proceed? (y/n): ")
            if Proceed.lower() != 'y':
                print("Deployment cancelled")
                return False
        
        # Check for GitHub Actions workflow
        if not self.CheckGitHubActionsWorkflow():
            print("Warning: GitHub Actions workflow file not found")
            print("Deployment may not automatically build the website")
            Proceed = input("Proceed with deployment anyway? (y/n): ")
            if Proceed.lower() != 'y':
                print("Deployment cancelled")
                return False
        
        # Check for uncommitted changes
        HasChanges, StatusOutput = self.CheckGitStatus()
        
        if not HasChanges:
            print("No changes to deploy")
            return True
        
        print("Changes to be deployed:")
        print(StatusOutput)
        
        # Stage changes
        if not self.StageChanges():
            return False
        
        if not self.StageWorkflow():
            print("  Continuing without workflow file")
        
        if not self.StageReadme():
            print("  Continuing without README file")
        
        # Commit and push
        if not self.CommitChanges():
            return False
        
        if not self.PushChanges():
            return False
        
        print("\nDeployment successful!")
        print("\nGitHub Actions should now build and deploy the website.")
        print("You can check the status of the deployment in the Actions tab of your GitHub repository.")
        print("After deployment completes, the website will be available at your configured domain.")
        
        return True

def Main():
    """Main entry point for the script."""
    Parser = argparse.ArgumentParser(description="Deploy Project Himalaya website to GitHub Pages")
    Parser.add_argument("--repo", dest="RepoDir", default=".", help="Path to repository directory")
    Parser.add_argument("--message", dest="CommitMessage", help="Git commit message")
    
    Args = Parser.parse_args()
    
    try:
        Deployer = WebsiteDeployer(
            RepoDir=Args.RepoDir,
            CommitMessage=Args.CommitMessage
        )
        
        Success = Deployer.Deploy()
        sys.exit(0 if Success else 1)
    
    except Exception as Ex:
        print(f"Error: {str(Ex)}")
        sys.exit(1)

if __name__ == "__main__":
    Main()
