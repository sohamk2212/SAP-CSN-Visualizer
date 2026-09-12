# Changelog

All notable changes to CSN Object Visualizer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-12

### Added
- Initial release of CSN Object Visualizer
- Core CSN parser for extracting entity and column metadata
- Beautiful Streamlit-based web interface
- Multiple visualization options:
  - Table view with sorting and filtering
  - Key columns and associations highlighting
  - Detailed column information panel
  - Summary statistics dashboard
- Advanced filtering by:
  - Column name/description (free text search)
  - Data type (String, Integer, Date, etc.)
  - Key status (key columns, non-key columns)
  - Association status
- Export capabilities:
  - Multi-sheet Excel reports
  - Interactive HTML reports
  - CSV format export
- Comprehensive documentation:
  - README with features and usage guide
  - Getting Started guide for new users
  - FAQ with common questions
  - API reference for developers
  - Contributing guidelines
- Automated setup scripts:
  - `setup.sh` for macOS/Linux
  - `setup.bat` for Windows
- Support for:
  - JSON CSN files
  - TXT files with JSON content
  - Large files (up to 500MB)

### Features
- **Parse Metadata**: Extract entity names, labels, columns, associations
- **Smart Analysis**: Identify key columns, references, constraints
- **Beautiful UI**: Modern, responsive interface with Streamlit
- **Filter & Search**: Multiple ways to find relevant columns
- **Export Reports**: Professional-grade documentation in multiple formats
- **Beginner-Friendly**: Easy to understand visualizations and explanations

### Documentation
- Comprehensive README.md
- GETTING_STARTED.md for quick onboarding
- FAQ.md with troubleshooting
- API.md with full Python API reference
- CONTRIBUTING.md for developers
- This CHANGELOG.md

### Technical
- Python 3.8+ support
- Modular code structure (src/parser.py, src/visualizer.py)
- Type hints for better code documentation
- Dataclass-based ColumnMetadata
- Comprehensive error handling

## [Unreleased]

### Planned Features
- Entity relationship diagrams (ERD)
- Multi-entity comparison
- Batch processing multiple CSN files
- REST API for integration
- Command-line interface (CLI)
- Data sample generation
- Integration with SAP systems
- Custom data type mapping
- Advanced filtering UI
- Favorites/bookmarks

### Under Consideration
- Dark mode theme
- Multi-language support
- Real-time SAP system connection
- Schema change tracking
- Collaborative documentation

---

## Migration Guide

### From Version 0.x to 1.0.0

1. **Project Structure**: Updated to use modular `src/` package
2. **API Changes**: 
   - Use `CSNParser` and `CSNVisualizer` from src modules
   - Old inline parsing removed
3. **Dependencies**: Updated requirements - see requirements.txt
4. **UI**: Complete redesign with new features

---

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2024-09-12 | Stable | Initial release |

---

## Support

- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Share ideas in GitHub Discussions
- **Documentation**: See docs/ folder
- **Contributing**: See CONTRIBUTING.md

---

**Last Updated:** September 12, 2024
