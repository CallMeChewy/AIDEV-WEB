# Project Himalaya Website Scripts

This directory contains scripts for automating the Project Himalaya website infrastructure setup, configuration, and deployment.

## Available Scripts

1. **himalaya_website.py** - Main script for managing the Project Himalaya website
2. **setup_website.py** - Script focused on setting up the website structure
3. **generate_config.py** - Script for generating website configuration files
4. **deploy_website.py** - Script for deploying the website to GitHub Pages

## Main Script: himalaya_website.py

The `himalaya_website.py` script is the primary tool for managing all aspects of the Project Himalaya website. It combines the functionality of the other scripts.

### Features

- Generate configuration files and content
- Create website directory structure
- Install configuration files
- Set up custom theme
- Create sample blog post
- Deploy changes to GitHub Pages

### Usage

```bash
# Generate website configuration files
python himalaya_website.py generate [--config CONFIG_FILE] [--output OUTPUT_DIR]

# Set up website structure
python himalaya_website.py setup [--repo REPO_DIR] [--artifacts ARTIFACTS_DIR] [--config CONFIG_FILE]

# Deploy website to GitHub Pages
python himalaya_website.py deploy [--repo REPO_DIR] [--message COMMIT_MESSAGE]

# All-in-one: generate, setup, and deploy
python himalaya_website.py all [--repo REPO_DIR] [--config CONFIG_FILE] [--message COMMIT_MESSAGE]
```

### Examples

```bash
# Generate configuration files with default settings
python himalaya_website.py generate

# Generate configuration files with custom settings
python himalaya_website.py generate --config config.json --output custom_artifacts

# Set up website in the current repository
python himalaya_website.py setup

# Set up website using previously generated artifacts
python himalaya_website.py setup --artifacts custom_artifacts

# Deploy website with custom commit message
python himalaya_website.py deploy --message "Update documentation"

# Complete process: generate, setup, and deploy
python himalaya_website.py all
```

### Configuration

You can customize the website settings by providing a JSON configuration file:

```json
{
  "title": "Project Himalaya",
  "description": "A comprehensive framework for AI-human collaborative development",
  "url": "https://projecthimalaya.com",
  "repository": "CallMeChewy/ProjectHimalaya",
  "author": "Herbert J. Bowers",
  "theme": "just-the-docs",
  "primary_color": "#4575b4"
}
```

## Individual Scripts

While the main script provides all functionality, the individual scripts can be used for more focused tasks:

### setup_website.py

Sets up the website directory structure and installs configuration files.

```bash
python setup_website.py [--base-dir BASE_DIR] [--config CONFIG_FILE] [--artifacts ARTIFACTS_DIR]
```

### generate_config.py

Generates website configuration files without modifying the repository.

```bash
python generate_config.py [--output OUTPUT_DIR] [--config CONFIG_FILE]
```

### deploy_website.py

Deploys the website to GitHub Pages.

```bash
python deploy_website.py [--repo REPO_DIR] [--message COMMIT_MESSAGE]
```

## Requirements

- Python 3.8+
- Git
- PyYAML library (`pip install pyyaml`)

## Setting Up Your Project Himalaya Website

### Step 1: Generate Configuration

```bash
python himalaya_website.py generate --config config.json
```

This generates all the necessary configuration files in the `artifacts` directory.

### Step 2: Set Up Website Structure

```bash
python himalaya_website.py setup
```

This creates the directory structure and installs the configuration files.

### Step 3: Deploy to GitHub Pages

```bash
python himalaya_website.py deploy
```

This commits and pushes the changes to GitHub, triggering the GitHub Actions workflow to build and deploy the website.

### Step 4: Configure GitHub Pages

In your GitHub repository settings:
1. Go to "Settings" > "Pages"
2. Set source to GitHub Actions
3. Configure your custom domain if desired

## Customization

### Custom Domain

To use a custom domain:
1. Update the `url` in your configuration file
2. Run the setup process
3. Configure your domain DNS settings as described in the deployment output
4. Enable HTTPS in your GitHub repository settings

### Custom Theme

The setup process creates a custom color scheme based on your `primary_color` setting. You can further customize the appearance by modifying:
1. `docs/_sass/color_schemes/himalaya.scss`
2. `docs/_sass/custom/custom.scss` (create if it doesn't exist)

### Custom Content

After setup, you can add your own content:
1. Add documentation pages in `docs/_docs/`
2. Add component documentation in `docs/_components/`
3. Add blog posts in `docs/_posts/`
4. Add images and other assets in `docs/assets/`

## Troubleshooting

### Website Not Deploying

1. Check the GitHub Actions workflow in the Actions tab of your repository
2. Verify that the workflow file exists at `.github/workflows/gh-pages.yml`
3. Make sure you're pushing to the correct branch (usually `main`)

### Custom Domain Not Working

1. Verify that the `CNAME` file exists in the `docs` directory
2. Check your DNS configuration
3. Give DNS propagation time to complete (can take up to 48 hours)

### Local Testing

To test the website locally before deployment:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Then open your browser to http://localhost:4000
