# FAQ - CSN Object Visualizer

## General Questions

### Q: What is CSN?
**A:** Core Schema Notation (CSN) is SAP's format for describing data models, entities, and their relationships in a structured JSON format. It's commonly used in SAP Analytics Cloud, CAP (Cloud Application Programming), and other SAP systems.

### Q: Do I need a SAP account to use this tool?
**A:** No! You only need a CSN JSON file. If you have one, you can use this tool. The file can be exported from any SAP system that supports CSN format.

### Q: Is this tool open source?
**A:** Yes! CSN Object Visualizer is licensed under MIT, which means you can use, modify, and distribute it freely.

---

## Technical Questions

### Q: What versions of Python are supported?
**A:** Python 3.8 or higher. We recommend Python 3.9+.

### Q: Can I run this on Windows?
**A:** Yes! Use `setup.bat` for automated setup on Windows, or follow the manual steps in README.md.

### Q: Can I deploy this to a server?
**A:** Yes! Streamlit applications can be deployed to:
- Streamlit Cloud (free)
- AWS, Azure, Google Cloud
- Your own servers (Linux/Windows)

### Q: How large can CSN files be?
**A:** The default upload limit is 500MB. You can increase this in `.streamlit/config.toml` if needed.

### Q: Does this tool store my data?
**A:** No! All processing happens locally in your browser/server. Files are not stored or sent anywhere.

---

## Usage Questions

### Q: How do I get a CSN file?
**A:** 
1. Log into your SAP system (SAP Analytics Cloud, CAP, etc.)
2. Navigate to metadata or schema endpoint
3. Export the entity as JSON
4. Save it as `.json` or `.txt`

### Q: Can I process multiple CSN files?
**A:** Yes! Upload and process them one at a time through the UI. For batch processing, consider modifying the code or using the Python API directly.

### Q: What information can I export?
**A:** You can export:
- Excel files (with multiple sheets for different views)
- HTML reports (interactive, standalone)
- CSV format (for databases, spreadsheets)

### Q: How do I interpret the "Cardinality" field?
**A:**
- **1** = One (1:1 relationship)
- **\*** (asterisk) = Many (1:N relationship)
- Example: Product → ProductGroup has cardinality "1" (each product has one group)

---

## Filter & Search Questions

### Q: How do I search for associations only?
**A:** Use the filter panel:
1. In "Filter by data type", select "Association"
2. Or in the "Key & Associations" tab, jump directly to associations

### Q: Can I filter by multiple data types at once?
**A:** In the current version, you can filter by one type at a time. For advanced filtering, you can export to CSV and use Excel.

### Q: What happens if no results match my search?
**A:** The table will show 0 results. Try broadening your search terms or clearing filters.

---

## Export Questions

### Q: Which export format should I use?
**A:**
- **Excel** - Best for sharing with business teams, further analysis
- **HTML** - Best for documentation, presentations, sharing with non-technical users
- **CSV** - Best for data import, database loading, advanced analysis

### Q: Can I edit the exported Excel file?
**A:** Yes! The Excel export includes fully formatted, editable worksheets.

### Q: Do exported reports include formulas?
**A:** Excel exports include formatted data. CSV exports are plain text. Neither includes formulas currently.

---

## Troubleshooting Questions

### Q: "Invalid JSON" error when uploading
**A:** Ensure your file:
- Is valid JSON format
- Contains proper closing braces `}`
- Is saved as `.json` or `.txt`
- Uses UTF-8 encoding

You can validate JSON online at [jsonlint.com](https://www.jsonlint.com/)

### Q: "No entities found" error
**A:** Your CSN file may:
- Be incomplete or truncated
- Have a different structure than expected
- Not contain a `definitions` section

Try downloading a fresh CSN export from your SAP system.

### Q: Associations are not showing
**A:** Some CSN formats don't include association definitions. Check if your SAP export includes:
- Mixin definitions
- Association targets
- ON clauses

### Q: The app won't start
**A:** Try:
1. Verify Python is installed: `python --version`
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check for errors: `streamlit run app.py --logger.level=debug`

---

## Performance Questions

### Q: Why is it slow with large files?
**A:** Very large CSN files (100K+ lines) may take time to parse. This is normal. Consider:
- Breaking large CSN files into smaller ones
- Filtering data in the UI rather than loading all at once
- Using CSV export for data transfer

### Q: Can I run this offline?
**A:** Yes! Once installed, everything runs locally offline (except Streamlit's initial components).

---

## Development Questions

### Q: Can I contribute to this project?
**A:** Yes! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Q: How do I add custom parsing logic?
**A:** Modify `src/parser.py`:
```python
# Add new parsing method
def parse_custom_fields(self, elements):
    # Your logic here
    pass
```

### Q: Can I use this as a Python library?
**A:** Yes! Import the modules directly:
```python
from src.parser import CSNParser
from src.visualizer import CSNVisualizer
```

---

## License & Legal Questions

### Q: Can I use this commercially?
**A:** Yes! MIT license allows commercial use.

### Q: Do I need to attribute the project?
**A:** Attribution is appreciated but not legally required under MIT license.

### Q: Can I modify and redistribute the code?
**A:** Yes! Under MIT license terms. See LICENSE file for details.

---

## Still Have Questions?

- **GitHub Issues** - For bugs and features
- **GitHub Discussions** - For general questions
- **Wiki** - For advanced topics
- **Email** - [Add contact info if applicable]

---

**Last Updated:** September 2024
