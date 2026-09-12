# Getting Started with CSN Object Visualizer

This guide will help you get up and running with CSN Object Visualizer in 5 minutes.

## Prerequisites

- **Python 3.8+** installed on your computer
- A CSN JSON file (exported from SAP)
- ~500MB disk space for dependencies

## Step-by-Step Setup

### 1. **Get the Code**

```bash
# Navigate to your project directory
cd /path/to/CSN_Object_Visualizer

# Or clone from GitHub
git clone https://github.com/youruser/CSN_Object_Visualizer.git
cd CSN_Object_Visualizer
```

### 2. **Run the Setup Script** (Recommended)

**On macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```cmd
setup.bat
```

The script will:
- Create a virtual environment
- Install all dependencies
- Verify the installation
- Show next steps

### 3. **Manual Setup** (Alternative)

If the script doesn't work, follow these steps:

**Create Virtual Environment:**
```bash
python3 -m venv .venv
```

**Activate It:**
- **macOS/Linux:** `source .venv/bin/activate`
- **Windows:** `.venv\Scripts\activate`

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

### 4. **Launch the App**

```bash
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`

## Getting Your First CSN File

### From SAP Analytics Cloud
1. Log in to your SAP Analytics Cloud instance
2. Navigate to **Metadata** or **Data Models**
3. Find your entity (e.g., I_Product, I_Customer)
4. Export as JSON
5. Save the file

### From a REST API
```bash
# Example using curl
curl "https://your-sap-system.com/api/csn/I_Product" \
  -u "username:password" \
  > product_csn.json
```

## First Use Walkthrough

### 1. **Upload Your CSN File**
- Click "Browse files" in the left sidebar
- Select your CSN JSON file
- The parser loads and displays the entity

### 2. **View Quick Statistics**
You'll immediately see:
- 📊 Total number of columns
- 🔑 Number of key columns
- 🔗 Number of associations
- 📦 Field type distribution

### 3. **Explore the Data**

**Table View:**
- See all columns in a sortable, filterable table
- Click column headers to sort
- Scroll right to see more information

**Key & Associations Tab:**
- Quickly identify important columns
- See relationship mappings
- Understand data flow between tables

**Detailed Info:**
- Click on any column name
- View complete metadata
- See constraints and defaults

### 4. **Export Your Results**

**Create Excel Report:**
- Click "Generate Excel Report"
- Download multi-sheet workbook
- Share with your team

**Create HTML Report:**
- Click "Generate HTML Report"
- Get a standalone, professional-looking document
- Perfect for documentation

**Download as CSV:**
- Use for data import
- Compatible with Excel, databases

## Common Tasks

### Task 1: Understanding a Table Structure
```
1. Upload I_Product CSN
2. View "Quick Statistics" for overview
3. Check "Key & Associations" tab for relationships
4. Export to Excel for your documentation
```

### Task 2: Finding All References to Another Table
```
1. Upload your CSN
2. Use Search: type the table name
3. Review "Constrained Column" for JOIN conditions
4. Note cardinality for relationship type
```

### Task 3: Identifying Required Fields
```
1. Upload your CSN
2. Go to "Table View" tab
3. Check "Constraints" column for "NOT NULL"
4. Export to Excel and filter NOT NULL fields
```

### Task 4: Preparing Documentation
```
1. Upload your CSN
2. Export to HTML Report
3. Share with business stakeholders
4. Or print to PDF for records
```

## Tips for Success

✅ **Do's:**
- Keep your CSN files in a dedicated folder
- Name files clearly: `product_master_2024.json`
- Export reports for different audiences
- Use Excel filters for deeper analysis

❌ **Don'ts:**
- Don't modify CSN JSON manually
- Don't expect real-time updates (refresh manually)
- Don't share CSN files with sensitive data without sanitizing

## Troubleshooting First Run

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python from python.org |
| "Permission denied" | Run `chmod +x setup.sh` before running |
| "Module not found" | Ensure virtual environment is active (see prompt like `(.venv)`) |
| "Port 8501 in use" | Run `streamlit run app.py --server.port 8502` |
| "File too large" | Ensure file is valid JSON, not exceeding 500MB |

## Next Steps

- **Read** the full [README.md](../README.md)
- **Explore** the [FAQ](FAQ.md)
- **Check** [Advanced Usage](ADVANCED.md) for power user features
- **Contribute** via [CONTRIBUTING.md](../CONTRIBUTING.md)

## Quick Reference

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Run the app
streamlit run app.py

# Install additional packages
pip install package_name

# Deactivate virtual environment
deactivate
```

## Need Help?

- 💬 GitHub Discussions
- 🐛 GitHub Issues
- 📚 Wiki
- 📧 Community Forums

---

**Happy CSN Exploring! 🚀**

Last Updated: September 2024
