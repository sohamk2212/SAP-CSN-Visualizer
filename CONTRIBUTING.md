# Contributing to CSN Object Visualizer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

- **Report Bugs** - Found an issue? Let us know!
- **Suggest Features** - Have an idea for improvement?
- **Submit Code** - Fix bugs or add new features
- **Improve Documentation** - Better docs help everyone
- **Share Feedback** - Your experience matters

## 🐛 Reporting Bugs

Before reporting, please:
1. Check existing issues to avoid duplicates
2. Provide a clear, descriptive title
3. Include steps to reproduce
4. Share your environment (Python version, OS, etc.)
5. Attach sample CSN file if possible (sanitized)

**Example bug report:**
```
Title: Parser fails on CSN with nested associations

Description: When parsing CSN files with multi-level nested associations, the parser crashes with KeyError.

Steps to reproduce:
1. Upload attached sample CSN file
2. Click parse
3. Error occurs

Environment:
- Python 3.9
- Streamlit 1.28
- Windows 10
```

## ✨ Suggesting Features

When suggesting features:
1. Check if similar feature exists
2. Provide clear use case
3. Explain expected behavior
4. Include mockups if applicable

**Example feature request:**
```
Title: Add entity comparison view

Use Case: When migrating between systems, need to compare table structures

Expected Behavior: 
- Upload two CSN files
- Select entities from each
- Show side-by-side comparison highlighting differences
```

## 🔧 Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/your-fork/CSN_Object_Visualizer.git
cd CSN_Object_Visualizer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest
```

## 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Format code with Black: `black src/`
- Lint with Flake8: `flake8 src/`

**Example:**
```python
def parse_columns(self, entity_name: str, elements: Dict) -> List[ColumnMetadata]:
    """Parse columns/elements from entity definition.
    
    Args:
        entity_name: Name of the entity
        elements: Dictionary of element definitions
        
    Returns:
        List of ColumnMetadata objects
    """
    columns = []
    for col_name, col_meta in elements.items():
        # Implementation...
    return columns
```

## 🔄 Pull Request Process

1. **Fork and Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes**
   - Keep commits atomic and descriptive
   - Update documentation if needed
   - Add tests for new features

3. **Write Descriptive Commit Messages**
   ```
   feat: Add entity comparison view
   
   - Upload two CSN files
   - Side-by-side comparison
   - Highlight differences
   ```

4. **Test Locally**
   ```bash
   streamlit run app.py
   pytest
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/my-feature
   ```

6. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update

   ## Testing Done
   Describe testing performed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] No breaking changes
   ```

## 📋 Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Example:**
```
feat: Add ERD visualization

Implement entity relationship diagram generation for better
schema visualization. Includes support for associations and
cardinality display.

Fixes #123
```

## 🧪 Testing

Add tests for new features:

```python
# tests/test_parser.py
import pytest
from src.parser import CSNParser

def test_parse_simple_entity():
    parser = CSNParser("test_input.json")
    assert parser.load_file()
    entity_name, _, columns, _ = parser.parse_full_entity()
    assert entity_name == "I_Product"
    assert len(columns) > 0
```

Run tests:
```bash
pytest tests/
pytest -v  # Verbose
pytest --cov=src  # With coverage
```

## 📖 Documentation

When adding features, update:
- Code docstrings
- README.md (if user-facing)
- docs/API.md (if new APIs)
- docs/TROUBLESHOOTING.md (if common issues)

## 🎨 Code Review Guidelines

When reviewing PRs, check:
- ✅ Code quality and style
- ✅ Test coverage
- ✅ Documentation completeness
- ✅ No breaking changes
- ✅ Performance impact
- ✅ Security considerations

## 📦 Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

1. Update version in `src/__init__.py`
2. Update CHANGELOG.md
3. Create release branch
4. Tag release: `git tag v1.2.3`
5. Create GitHub release with notes

## ❓ Questions?

- **Discussions** - Use GitHub Discussions for questions
- **Issues** - Bug reports and feature requests
- **Wiki** - Reference and guides

## 🙏 Thank You!

Your contributions make this tool better for everyone. We appreciate:
- Your time and effort
- Thoughtful feedback
- Quality code
- Patient collaboration

---

**Happy Contributing! 🚀**
