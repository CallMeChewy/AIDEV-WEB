# Project Himalaya

![Project Himalaya Logo](docs/assets/images/logo.png)

[![GitHub Pages](https://github.com/CallMeChewy/ProjectHimalaya/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/CallMeChewy/ProjectHimalaya/actions/workflows/gh-pages.yml)
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

Project documentation is available at our website: [projecthimalaya.com](https://projecthimalaya.com)

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
   git clone https://github.com/CallMeChewy/ProjectHimalaya.git
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

- Herbert J. Bowers (Project Creator)
- AI collaborators (Claude and others)

---

*"Code is not merely functional—it is a visual medium that developers interact with for extended periods. The choices made in these standards prioritize the axis of symmetry, character distinction, readability at scale, and visual hierarchy."*

— Herbert J. Bowers