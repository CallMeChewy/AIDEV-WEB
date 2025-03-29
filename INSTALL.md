# AIDEV-WEB Installation Guide
**Created: 2025-03-28**
**Last Modified: 2025-03-28  08:48PM**

[Context: Project_Setup]
[Status: Active]
[Version: 1.0]
[Author: Claude (Anthropic), as part of Project Himalaya]

## Installation Steps

### 1. Activate Virtual Environment

```bash
# Navigate to project directory
cd AIDEV-WEB # Use relative path from Desktop

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\\Scripts\\activate
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
python -c "import flask; print(f'Flask version: {flask.__version__}')"
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
