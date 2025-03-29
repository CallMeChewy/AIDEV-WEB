# Project Himalaya Website

This directory contains the source files for the Project Himalaya website, which is built using Jekyll and deployed via GitHub Pages.

## Local Development

### Prerequisites

1. Ruby (version 2.7.0 or higher)
2. Bundler
3. Git

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/CallMeChewy/ProjectHimalaya.git
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
