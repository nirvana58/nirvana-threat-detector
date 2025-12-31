# Contributing to AI Network Threat Detector

Thank you for your interest in contributing! 🎉

## 🚀 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/YOUR-USERNAME/ai-threat-detector/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages/logs

### Suggesting Features

1. Check [existing feature requests](https://github.com/YOUR-USERNAME/ai-threat-detector/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
2. Create a new issue with:
   - Clear description of the feature
   - Use case/motivation
   - Proposed implementation (if applicable)

### Pull Requests

1. **Fork** the repository
2. **Create** a new branch: `git checkout -b feature/your-feature-name`
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Commit** with clear messages: `git commit -m "Add feature: description"`
6. **Push** to your fork: `git push origin feature/your-feature-name`
7. **Create** a Pull Request

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ai-threat-detector.git
cd ai-threat-detector

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools

# Run tests
python -m pytest tests/

# Run local server
uvicorn app:app --reload
```

## 🧪 Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for 80%+ code coverage

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 📝 Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Add docstrings to functions/classes
- Keep functions focused and small
- Comment complex logic

```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy .
```

## 🔀 Git Workflow

1. **Main branch**: Production-ready code
2. **Dev branch**: Integration branch for features
3. **Feature branches**: Individual features/fixes

```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature

# After changes
git add .
git commit -m "Clear commit message"
git push origin feature/your-feature

# Create PR to dev branch
```

## 📦 Commit Messages

Use clear, descriptive commit messages:

```
Add: New feature or functionality
Fix: Bug fix
Update: Changes to existing features
Remove: Removed features or files
Refactor: Code restructuring
Docs: Documentation changes
Test: Test additions or changes
Style: Code style changes (formatting, etc.)
```

Example:
```
Add: Interactive mode for client CLI
Fix: Tabulate import error in admin tool
Update: Improve error handling in API
Docs: Add deployment guide for Railway
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Web dashboard for visualization
- [ ] Additional ML models (XGBoost, Neural Networks)
- [ ] Real-time streaming analysis
- [ ] Comprehensive test suite
- [ ] Performance optimizations

### Medium Priority
- [ ] Docker Compose setup
- [ ] Kubernetes deployment guides
- [ ] Multi-tenancy support
- [ ] Advanced analytics
- [ ] Integration tests

### Low Priority
- [ ] Mobile app
- [ ] Additional LLM models
- [ ] Custom themes for CLI
- [ ] Internationalization (i18n)

## 📚 Documentation

Documentation improvements are always welcome!

- Fix typos or unclear explanations
- Add examples
- Improve code comments
- Create tutorials
- Translate documentation

## 🐛 Bug Fixes

- Include tests that reproduce the bug
- Explain what caused the bug
- Describe the fix

## ✨ Feature Development

- Discuss major features in an issue first
- Keep PRs focused on single features
- Update documentation
- Add tests

## 🔍 Code Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer approval required
3. All comments addressed
4. Squash commits before merging

## 🎨 Design Principles

- **Simplicity**: Keep it simple and intuitive
- **Security**: Security first, always
- **Performance**: Optimize for speed and efficiency
- **Reliability**: Robust error handling
- **Usability**: Clear error messages and documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Communication

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Pull Requests**: Code contributions

## 🙏 Recognition

All contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## ❓ Questions?

Feel free to ask questions in:
- [GitHub Discussions](https://github.com/YOUR-USERNAME/ai-threat-detector/discussions)
- Issue comments
- Pull request comments

---

Thank you for contributing to AI Network Threat Detector! 🛡️