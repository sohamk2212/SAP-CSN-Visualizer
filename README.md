# 🧩 CSN Object Visualizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

**Transform massive, unreadable SAP Core Schema Notation (CSN) JSON responses into beautiful, interactive visualizations.**

This is an **open-source tool** that helps developers, data analysts, and business users understand complex database schemas from SAP systems without needing deep technical knowledge.

---

## 📸 Features

✅ **Parse Complex CSN Files** - Read and extract metadata from SAP CSN JSON responses  
✅ **Beautiful Visualizations** - Easy-to-understand tables, charts, and reports  
✅ **Smart Filtering** - Search and filter columns by name, type, key status, or associations  
✅ **Key Relationships** - Automatically highlight primary keys, foreign keys, and associations  
✅ **Reference Tracking** - See which tables reference each other and how  
✅ **Multiple Export Formats** - Download as Excel, HTML, or CSV  
✅ **Statistics Dashboard** - Quick overview of data types, nullability, and constraints  
✅ **Beginner-Friendly** - Even non-technical users can understand database structures  

---

## 🎯 Perfect For

- 👨‍💼 **Business Analysts** - Understanding data models without developer jargon
- 👨‍💻 **Developers** - Quick reference for schema documentation
- 📊 **Data Engineers** - Identifying relationships and data flows
- 🎓 **Beginners** - Learning SAP database structures
- 🔍 **Data Auditors** - Validating table structures and constraints

---

## 📋 What It Extracts

For each table/entity, the tool displays:

- **Column Names** - Full list of all table columns
- **Descriptions** - Business-friendly labels and documentation
- **Data Types** - CDS data types (String, Integer, Date, etc.)
- **Key Columns** - Primary key identification
- **Associations** - Links to other tables and reference relationships
- **Reference Tables** - Which tables this connects to
- **Constrained Columns** - Foreign key constraints and ON clauses
- **Check Tables** - Value lists and validations
- **Cardinality** - 1:1, 1:N relationships
- **Constraints** - NOT NULL, UNIQUE, etc.
- **Field Properties** - Length, precision, scale, defaults

---

## 🚀 Quick Start

### 1. **Clone or Download**
```bash
cd /path/to/CSN_Object_Visualizer
```

### 2. **Create Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Run the Application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
CSN_Object_Visualizer/
├── src/
│   ├── __init__.py           # Package initialization
│   ├── parser.py             # CSN parsing logic
│   └── visualizer.py         # Visualization and export utilities
├── app.py                    # Main Streamlit application
├── input_CSN.txt             # Sample CSN input file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # MIT License
```

---

## 📖 How to Use

### Step 1: Prepare Your CSN File
From your SAP system:
1. Navigate to the CSN metadata endpoint
2. Copy the complete JSON response
3. Paste it into a `.json` or `.txt` file

### Step 2: Upload to the Tool
1. Click **"Browse files"** in the left sidebar
2. Select your CSN JSON file
3. The parser will automatically extract all entities

### Step 3: Explore the Data
- **Quick Statistics Tab** - See total columns, keys, and associations
- **Table View Tab** - Browse all columns in an interactive table
- **Key & Associations Tab** - Focus on important relationships
- **Detailed Info Tab** - Deep dive into individual column properties
- **Export Tab** - Download reports in multiple formats

### Step 4: Filter & Search
Use the filter options to find specific columns:
- 🔎 **Search by Name/Description** - Free text search
- 📌 **Filter by Data Type** - String, Integer, Date, etc.
- 🔑 **Filter by Key Status** - Key columns only, non-key, or all

### Step 5: Export Results
- **📊 Excel Report** - Multi-sheet workbook with statistics
- **📄 HTML Report** - Beautiful standalone HTML document
- **📋 CSV Export** - For import into other tools

---

## 🛠️ Technical Details

### Input Format
The tool accepts:
- **`.json` files** - Standard JSON CSN format
- **`.txt` files** - JSON content in text format

### Supported CSN Metadata
- Entity definitions (tables/views)
- Element definitions (columns)
- Associations and compositions
- Cardinality constraints
- Data type information
- Semantic annotations (@EndUserText.label, @title, etc.)

### Output Formats

#### Excel Report
- **Columns Sheet** - Complete column metadata
- **Summary Sheet** - Statistics and overview
- **Associations Sheet** - Relationship details
- **Highlighted View** - Key information highlighted

#### HTML Report
- Responsive design
- Interactive tables
- Color-coded information
- Beautiful typography

#### CSV Export
- Standard CSV format
- Compatible with Excel, databases, etc.

---

## 🎓 Examples

### Example 1: Analyzing Product Master Data
```
Upload: I_Product CSN response
→ Discover: Product, ProductGroup, Division associations
→ Identify: Material as key column
→ Export: Excel report for business stakeholders
```

### Example 2: Understanding Sales Order Structure
```
Upload: I_SalesOrder CSN response
→ Filter: Association columns only
→ Analyze: References to Customer, Material, Plant
→ Export: HTML for documentation
```

### Example 3: Data Auditing
```
Upload: Vendor master CSN response
→ Check: Required fields (NOT NULL constraints)
→ Review: Reference tables and validations
→ Export: CSV for compliance report
```

---

## 🔧 Configuration

### Streamlit Configuration (optional)
Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
maxUploadSize = 500
```

### Environment Variables
None required - works out of the box!

---

## 📦 Dependencies

- **streamlit** - Interactive web interface
- **pandas** - Data manipulation
- **openpyxl** - Excel file generation
- **python-dateutil** - Date utilities

See `requirements.txt` for specific versions.

---

## 🐛 Troubleshooting

### Issue: "No definitions found in this CSN file"
**Solution:** Ensure your JSON is valid and contains a `definitions` section or proper CSN structure.

### Issue: "No columns/elements found"
**Solution:** The parser expects elements/properties in the entity definition. Check that your CSN response is complete.

### Issue: Associations not showing
**Solution:** Make sure your CSN includes mixin definitions for associations (common with SAP Analytics Cloud).

### Issue: File upload fails
**Solution:** Ensure file is valid JSON/TXT and size is under 500MB (adjustable in config).

---

## 📝 Usage Examples in Code

### Python Integration
```python
from src.parser import CSNParser
from src.visualizer import CSNVisualizer

# Parse CSN file
parser = CSNParser("input_CSN.txt")
parser.load_file()
entity_name, entity_label, columns, associations = parser.parse_full_entity()

# Generate visualizations
df = CSNVisualizer.columns_to_dataframe(columns)
stats = CSNVisualizer.get_summary_stats(columns)

# Export
CSNVisualizer.export_to_excel(columns, associations, entity_name, entity_label, "output.xlsx")
```

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) ❤️
- Inspired by the need for better CSN documentation tools
- Special thanks to SAP developers facing CSN parsing challenges

---

## 📞 Support & Feedback

- **Issues** - Report bugs on GitHub Issues
- **Discussions** - Share ideas in GitHub Discussions
- **Wiki** - Check our [Wiki](../../wiki) for advanced usage

---

## 🗺️ Roadmap

- [ ] Multi-entity comparison
- [ ] Entity relationship diagrams (ERD)
- [ ] Custom data type mapping
- [ ] Batch processing multiple CSN files
- [ ] REST API for integration
- [ ] Command-line interface (CLI)
- [ ] Data sample generation
- [ ] Integration with SAP systems

---

## 💡 Pro Tips

1. **Organize Your Files** - Keep CSN responses in a dedicated folder
2. **Use Sample Labels** - Export HTML reports for stakeholder presentations
3. **Excel Filters** - Use Excel's built-in filters on exported data
4. **Batch Processing** - Process multiple entities quickly
5. **Version Control** - Export reports for documentation purposes

---

## 📚 Documentation

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [API Reference](docs/API.md)
- [FAQ](docs/FAQ.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 🌟 Show Your Support

If this tool helped you, please:
- ⭐ Star the repository
- 🐛 Report issues
- 💬 Share feedback
- 🤝 Contribute improvements

---

**Made with ❤️ for the SAP Community**

Last Updated: September 2024
