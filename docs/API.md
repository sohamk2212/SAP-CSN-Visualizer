# API Reference - CSN Object Visualizer

Complete API reference for CSN Object Visualizer Python modules.

## Module: `src.parser`

### Class: `ColumnMetadata`

Data class representing a single column/element in CSN.

**Attributes:**
```python
name: str                    # Column name
description: str           # Column description/label
datatype: str             # CDS data type
is_key: bool              # Is this a key column?
is_association: bool      # Is this an association?
target_entity: str        # Target entity for associations
cardinality: str          # 1:1 or 1:N relationship
reference_table: str      # Referenced table name
reference_column: str     # Referenced column name
constrained_column: str   # Foreign key constraint clause
check_table: str          # Value list table
constraints: str          # NOT NULL, UNIQUE, etc.
length: str              # Column length
nullable: bool           # Can be NULL?
precision: str           # Numeric precision
scale: str               # Numeric scale
default_value: str       # Default value
```

**Example:**
```python
col = ColumnMetadata(
    name="ProductID",
    description="Unique Product Identifier",
    datatype="cds.UUID",
    is_key=True,
    nullable=False
)
```

---

### Class: `CSNParser`

Main parser for CSN JSON files.

#### `__init__(file_path: str)`
Initialize parser with file path.

```python
parser = CSNParser("data/product_csn.json")
```

#### `load_file() -> bool`
Load and parse the CSN JSON file.

**Returns:** `True` if successful, `False` otherwise

```python
if parser.load_file():
    print("File loaded successfully")
else:
    print("Error loading file")
```

#### `extract_entity_name() -> str`
Get the entity name from CSN data.

```python
entity_name = parser.extract_entity_name()
# Returns: "I_Product"
```

#### `extract_entity_label() -> str`
Get the entity label/description.

```python
label = parser.extract_entity_label()
# Returns: "Product"
```

#### `extract_release_state() -> str`
Get the release state (e.g., RELEASED, DRAFT).

```python
state = parser.extract_release_state()
# Returns: "RELEASED"
```

#### `get_definitions() -> Dict[str, Any]`
Extract entity definitions from CSN.

```python
definitions = parser.get_definitions()
# Returns dictionary of entities
```

#### `parse_columns(entity_name: str, elements: Dict) -> List[ColumnMetadata]`
Parse column metadata from entity elements.

**Args:**
- `entity_name`: Name of the entity
- `elements`: Dictionary of element definitions

**Returns:** List of `ColumnMetadata` objects

```python
columns = parser.parse_columns("I_Product", elements_dict)
for col in columns:
    print(f"{col.name}: {col.datatype}")
```

#### `get_associations(elements: Dict) -> List[Dict]`
Extract all associations from entity.

**Returns:** List of association dictionaries

```python
assocs = parser.get_associations(elements_dict)
for assoc in assocs:
    print(f"{assoc['name']} -> {assoc['target']}")
```

#### `parse_full_entity() -> Tuple[str, str, List[ColumnMetadata], List[Dict]]`
Parse complete entity and return all metadata.

**Returns:** Tuple of:
- Entity name (str)
- Entity label (str)
- Columns list (List[ColumnMetadata])
- Associations list (List[Dict])

```python
entity_name, label, columns, associations = parser.parse_full_entity()
```

---

## Module: `src.visualizer`

### Class: `CSNVisualizer`

Static utility class for visualization and export.

#### `columns_to_dataframe(columns: List[ColumnMetadata]) -> pd.DataFrame`
Convert column metadata to pandas DataFrame.

**Returns:** DataFrame with all column information

```python
df = CSNVisualizer.columns_to_dataframe(columns)
print(df.head())
```

**DataFrame Columns:**
- Column Name
- Description
- Data Type
- Is Key
- Is Association
- Target Entity
- Cardinality
- Reference Table
- Reference Column
- Constrained Column
- Check Table
- Constraints
- Length
- Precision
- Scale
- Default
- Nullable

#### `get_summary_stats(columns: List[ColumnMetadata]) -> Dict`
Calculate summary statistics about columns.

**Returns:** Dictionary with statistics

```python
stats = CSNVisualizer.get_summary_stats(columns)

# Returns:
{
    "Total Columns": 50,
    "Key Columns": 3,
    "Association Columns": 5,
    "Nullable Columns": 45,
    "Not Nullable Columns": 5,
    "Data Type Distribution": {
        "cds.String": 30,
        "cds.Integer": 10,
        "cds.Association": 5,
        "cds.UUID": 5
    }
}
```

#### `filter_columns(columns: List[ColumnMetadata], **kwargs) -> List[ColumnMetadata]`
Filter columns based on criteria.

**Parameters:**
- `by_type` (str, optional): Filter by data type
- `by_key` (bool, optional): Filter by key status
- `by_association` (bool, optional): Filter by association
- `search_text` (str, optional): Free text search

**Returns:** Filtered list of columns

```python
# Find all key columns
key_cols = CSNVisualizer.filter_columns(columns, by_key=True)

# Search for "Product" columns
prod_cols = CSNVisualizer.filter_columns(columns, search_text="Product")

# Find all associations
assoc_cols = CSNVisualizer.filter_columns(columns, by_association=True)

# Filter by type
string_cols = CSNVisualizer.filter_columns(columns, by_type="String")
```

#### `highlight_important_columns(columns: List[ColumnMetadata]) -> Dict`
Highlight key columns and associations.

**Returns:** Organized dictionary with categories:
- "Key Columns"
- "Associations & References"
- "Regular Columns"

```python
highlighted = CSNVisualizer.highlight_important_columns(columns)

# Access different categories
for col in highlighted["Key Columns"]:
    print(col["name"])
```

#### `export_to_excel(columns, associations, entity_name, entity_label, output_path) -> bool`
Export data to Excel file with multiple sheets.

**Parameters:**
- `columns`: List of ColumnMetadata
- `associations`: List of association dictionaries
- `entity_name`: Entity name
- `entity_label`: Entity label
- `output_path`: Output file path (e.g., "report.xlsx")

**Returns:** `True` if successful, `False` otherwise

**Excel Sheets Created:**
- Columns
- Summary
- Associations (if any)
- Highlighted View

```python
success = CSNVisualizer.export_to_excel(
    columns,
    associations,
    "I_Product",
    "Product Master",
    "product_report.xlsx"
)
```

#### `export_to_html(columns, entity_name, entity_label, output_path) -> bool`
Export data to interactive HTML report.

**Parameters:**
- `columns`: List of ColumnMetadata
- `entity_name`: Entity name
- `entity_label`: Entity label
- `output_path`: Output file path (e.g., "report.html")

**Returns:** `True` if successful, `False` otherwise

```python
success = CSNVisualizer.export_to_html(
    columns,
    "I_Product",
    "Product Master",
    "product_report.html"
)
```

---

## Complete Example

```python
from src.parser import CSNParser
from src.visualizer import CSNVisualizer
import pandas as pd

# 1. Parse CSN file
parser = CSNParser("data/product.json")
if not parser.load_file():
    print("Error loading file")
    exit(1)

# 2. Extract metadata
entity_name, label, columns, associations = parser.parse_full_entity()
print(f"Entity: {entity_name} ({label})")
print(f"Columns: {len(columns)}")
print(f"Associations: {len(associations)}")

# 3. Get statistics
stats = CSNVisualizer.get_summary_stats(columns)
print(f"\nKey Columns: {stats['Key Columns']}")
print(f"Nullable Columns: {stats['Nullable Columns']}")
print(f"Data Types: {stats['Data Type Distribution']}")

# 4. Filter columns
key_columns = CSNVisualizer.filter_columns(columns, by_key=True)
associations_only = CSNVisualizer.filter_columns(columns, by_association=True)

# 5. Convert to DataFrame
df = CSNVisualizer.columns_to_dataframe(columns)
print(f"\nDataFrame Shape: {df.shape}")

# 6. Highlight important columns
highlighted = CSNVisualizer.highlight_important_columns(columns)
print(f"\nKey Columns: {len(highlighted['Key Columns'])}")
print(f"Associations: {len(highlighted['Associations & References'])}")

# 7. Export
CSNVisualizer.export_to_excel(columns, associations, entity_name, label, "output.xlsx")
CSNVisualizer.export_to_html(columns, entity_name, label, "output.html")

# 8. Save as CSV
df.to_csv("output.csv", index=False)

print("\nExport complete!")
```

---

## Error Handling

```python
from src.parser import CSNParser

try:
    parser = CSNParser("nonexistent.json")
    if not parser.load_file():
        raise FileNotFoundError("Could not load CSN file")
    
    entity_name, label, columns, assoc = parser.parse_full_entity()
    
    if not columns:
        print("Warning: No columns found")
    
except FileNotFoundError as e:
    print(f"File error: {e}")
except Exception as e:
    print(f"Parsing error: {e}")
```

---

## Advanced Usage

### Custom Parsing

```python
from src.parser import CSNParser, ColumnMetadata

class CustomParser(CSNParser):
    def custom_parse(self, entity_name):
        """Add custom parsing logic"""
        entity_name, label, cols, assoc = self.parse_full_entity()
        
        # Custom filtering
        custom_cols = [c for c in cols if len(c.name) > 5]
        return custom_cols
```

### Batch Processing

```python
from pathlib import Path
from src.parser import CSNParser
from src.visualizer import CSNVisualizer

# Process multiple files
csn_files = Path("data/").glob("*.json")

for csn_file in csn_files:
    parser = CSNParser(str(csn_file))
    if parser.load_file():
        entity_name, label, columns, _ = parser.parse_full_entity()
        output = f"reports/{entity_name}_report.xlsx"
        CSNVisualizer.export_to_excel(columns, [], entity_name, label, output)
        print(f"Processed: {entity_name}")
```

---

## Version Information

- **Latest Version:** 1.0.0
- **Python:** 3.8+
- **Dependencies:** pandas, openpyxl

---

**Last Updated:** September 2024
