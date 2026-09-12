"""Visualization utilities for CSN data"""

import pandas as pd
from typing import List, Dict
from src.parser import ColumnMetadata
import json


class CSNVisualizer:
    """Generate various visualizations and exports for CSN data"""

    @staticmethod
    def columns_to_dataframe(columns: List[ColumnMetadata]) -> pd.DataFrame:
        """Convert column metadata to pandas DataFrame"""
        data = []
        for col in columns:
            data.append({
                "Column Name": col.name,
                "Description": col.description,
                "Data Type": col.datatype,
                "Is Key": "✓" if col.is_key else "",
                "Is Association": "✓" if col.is_association else "",
                "Target Entity": col.target_entity,
                "Cardinality": col.cardinality,
                "Reference Table": col.reference_table,
                "Reference Column": col.reference_column,
                "Constrained Column": col.constrained_column,
                "Check Table": col.check_table,
                "Constraints": col.constraints,
                "Length": col.length,
                "Precision": col.precision,
                "Scale": col.scale,
                "Default": col.default_value,
                "Nullable": "No" if not col.nullable else "Yes",
            })
        return pd.DataFrame(data)

    @staticmethod
    def columns_to_professional_dataframe(columns: List[ColumnMetadata]) -> pd.DataFrame:
        """Convert column metadata to professional DataFrame (clean, minimal columns)
        
        Shows the most important metadata in a clean, business-friendly format.
        Similar to SAP table structure views.
        """
        data = []
        for idx, col in enumerate(columns, 1):
            # Determine if this is a key column (for distinct count concept)
            is_key = "Yes" if col.is_key else "No"
            
            # Get CDS type name (short form)
            cds_type = col.datatype.split('.')[-1] if '.' in col.datatype else col.datatype
            
            # Get SAP data type
            sap_type = col.sap_datatype or cds_type
            
            # Get size/length value
            length = str(col.length) if col.length else "0"
            
            # Get precision (handle empty string)
            precision = str(col.precision) if col.precision else "0"
            
            # Get scale (handle empty string)
            scale = str(col.scale) if col.scale else "0"
            
            # SAP Domain (e.g., MATNR, DATUM, TIME)
            sap_domain = col.sap_domain or ""
            
            # Check Table for associations (actual table reference)
            check_table = col.check_table or col.target_entity or ""
            
            data.append({
                "Index": idx,
                "Name": col.name,
                "Description": col.description or "",
                "Data Type": cds_type,
                "SAP Data Type": sap_type,
                "Size": length,
                "Precision": precision,
                "Scale": scale,
                "Key": is_key,
                "Allow Null": "Yes" if col.nullable else "No",
                "Domain": sap_domain,
                "Check Table": check_table,
                "Distinct Count": "1" if col.is_key else "",
            })
        
        df = pd.DataFrame(data)
        return df

    @staticmethod
    def columns_to_detailed_dataframe(columns: List[ColumnMetadata]) -> pd.DataFrame:
        """Convert column metadata to detailed DataFrame with all information
        
        Shows complete metadata for advanced users and documentation.
        """
        data = []
        for idx, col in enumerate(columns, 1):
            data.append({
                "Index": idx,
                "Column Name": col.name,
                "Description": col.description or "",
                "Data Type": col.datatype,
                "SAP Data Type": col.sap_datatype or "-",
                "Size": col.length or "-",
                "Precision": col.precision or "-",
                "Scale": col.scale or "-",
                "Key": "Yes" if col.is_key else "No",
                "Nullable": "Yes" if col.nullable else "No",
                "Association": "Yes" if col.is_association else "No",
                "Target Entity": col.target_entity or "-",
                "Reference Table": col.reference_table or "-",
                "Reference Column": col.reference_column or "-",
                "SAP Domain": col.sap_domain or "-",
                "Check Table": col.check_table or "-",
                "Constraints": col.constraints or "-",
                "Default": col.default_value or "-",
                "Cardinality": col.cardinality or "-",
                "Constrained Column": col.constrained_column or "-",
            })
        
        return pd.DataFrame(data)

    @staticmethod
    def columns_to_smart_detailed_dataframe(columns: List[ColumnMetadata]) -> pd.DataFrame:
        """Convert to smart detailed DataFrame - only shows relevant columns with data
        
        More responsive and user-friendly than the full detailed view.
        Automatically hides columns that are mostly empty.
        """
        data = []
        for idx, col in enumerate(columns, 1):
            row = {
                "Index": idx,
                "Name": col.name,
                "Description": col.description or "",
                "Type": col.datatype.split('.')[-1] if '.' in col.datatype else col.datatype,
                "Key": "🔑" if col.is_key else "•",
                "Nullable": "✓" if col.nullable else "✗",
            }
            
            # Add fields only if they have data
            if col.check_table:
                row["Check Table"] = col.check_table
            if col.reference_table or col.reference_column:
                row["Reference"] = f"{col.reference_table or ''}.{col.reference_column or ''}"
            if col.is_association:
                row["Assoc."] = f"{col.target_entity or 'N/A'}"
            if col.length:
                row["Length"] = col.length
            if col.precision or col.scale:
                row["Numeric"] = f"({col.precision or '0'},{col.scale or '0'})"
            if col.constraints:
                row["Constraints"] = col.constraints
            if col.default_value:
                row["Default"] = col.default_value
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Reorder columns to put important ones first
        important_cols = ["Index", "Name", "Description", "Type", "Key", "Nullable"]
        other_cols = [c for c in df.columns if c not in important_cols]
        return df[important_cols + other_cols]

    @staticmethod
    def get_summary_stats(columns: List[ColumnMetadata]) -> Dict:
        """Calculate summary statistics"""
        total_columns = len(columns)
        key_columns = sum(1 for c in columns if c.is_key)
        association_columns = sum(1 for c in columns if c.is_association)
        nullable_columns = sum(1 for c in columns if c.nullable)

        datatypes = {}
        for col in columns:
            dt = col.datatype.split('.')[-1] if '.' in col.datatype else col.datatype
            datatypes[dt] = datatypes.get(dt, 0) + 1

        return {
            "Total Columns": total_columns,
            "Key Columns": key_columns,
            "Association Columns": association_columns,
            "Nullable Columns": nullable_columns,
            "Not Nullable Columns": total_columns - nullable_columns,
            "Data Type Distribution": datatypes,
        }

    @staticmethod
    def filter_columns(
        columns: List[ColumnMetadata],
        by_type: str = None,
        by_key: bool = None,
        by_association: bool = None,
        search_text: str = None
    ) -> List[ColumnMetadata]:
        """Filter columns based on criteria"""
        filtered = columns

        if by_type:
            filtered = [c for c in filtered if by_type.lower() in c.datatype.lower()]

        if by_key is not None:
            filtered = [c for c in filtered if c.is_key == by_key]

        if by_association is not None:
            filtered = [c for c in filtered if c.is_association == by_association]

        if search_text:
            search_lower = search_text.lower()
            filtered = [
                c for c in filtered
                if search_lower in c.name.lower()
                or search_lower in c.description.lower()
                or search_lower in c.datatype.lower()
            ]

        return filtered

    @staticmethod
    def highlight_important_columns(columns: List[ColumnMetadata]) -> Dict:
        """Highlight key columns and associations for easy understanding"""
        result = {
            "Key Columns": [],
            "Associations & References": [],
            "Regular Columns": [],
        }

        for col in columns:
            if col.is_key:
                result["Key Columns"].append({
                    "name": col.name,
                    "description": col.description,
                    "datatype": col.datatype
                })
            elif col.is_association:
                result["Associations & References"].append({
                    "name": col.name,
                    "description": col.description,
                    "target": col.target_entity,
                    "cardinality": col.cardinality,
                    "on_clause": col.constrained_column
                })
            else:
                result["Regular Columns"].append({
                    "name": col.name,
                    "description": col.description,
                    "datatype": col.datatype,
                    "nullable": col.nullable
                })

        return result

    @staticmethod
    def get_foreign_key_mapping(columns: List[ColumnMetadata]) -> List[Dict]:
        """Create a mapping of foreign key columns with their associations
        
        Returns list of ForeignKey objects with column and related associations
        """
        fk_mapping = []
        
        # Find columns that have corresponding associations
        for col in columns:
            if col.is_association or col.reference_table:
                # Check if there's a matching non-association column
                base_name = col.name.lstrip('_')  # Remove leading underscore
                
                # Find if this references another column
                matching_assocs = []
                for other_col in columns:
                    if other_col.is_association and other_col.name.lstrip('_') == base_name:
                        matching_assocs.append({
                            "name": other_col.name,
                            "target": other_col.target_entity or other_col.reference_table,
                            "cardinality": other_col.cardinality or "N/A",
                            "datatype": other_col.datatype
                        })
                
                if matching_assocs:
                    fk_mapping.append({
                        "column_name": col.name,
                        "data_type": col.datatype,
                        "is_key": col.is_key,
                        "nullable": col.nullable,
                        "check_table": col.check_table,
                        "associations": matching_assocs
                    })
        
        return fk_mapping

    @staticmethod
    def get_associations_with_fk(columns: List[ColumnMetadata]) -> List[Dict]:
        """Get associations list with their linked foreign key columns"""
        associations = []
        
        for col in columns:
            if col.is_association:
                # Find the base column name (remove leading underscore)
                base_name = col.name.lstrip('_')
                
                # Try to find the foreign key column
                fk_column = None
                for other_col in columns:
                    if not other_col.is_association and other_col.name == base_name:
                        fk_column = other_col.name
                        break
                
                associations.append({
                    "name": col.name,
                    "target": col.target_entity or col.reference_table,
                    "cardinality": col.cardinality or "N/A",
                    "description": col.description or "-",
                    "on_clause": col.constrained_column or "-",
                    "foreign_key": fk_column or "No FK mapping",
                    "datatype": col.datatype
                })
        
        return associations

    @staticmethod
    def get_join_conditions(columns: List[ColumnMetadata], entity_name: str) -> List[Dict]:
        """Extract join conditions showing which columns link to which target views
        
        Format: Source Column = Target View.Target Column
        Example: Brand = I_Brand.Brand (from constrained_column: "Brand _Brand.Brand")
        """
        join_conditions = []
        
        for col in columns:
            if col.is_association and col.constrained_column:
                # Parse constrained column format: "SourceCol _TargetAssoc.TargetCol"
                # Example: "Brand _Brand.Brand" means I_Product.Brand = I_Brand.Brand
                
                parts = col.constrained_column.split()
                if len(parts) >= 2:
                    source_col = parts[0]
                    target_info = parts[1]  # e.g., "_Brand.Brand"
                    
                    # Extract target column name
                    if '.' in target_info:
                        target_col = target_info.split('.')[-1]
                    else:
                        target_col = target_info.lstrip('_')
                    
                    join_conditions.append({
                        "source_column": source_col,
                        "association": col.name,
                        "target_view": col.target_entity or col.reference_table or "N/A",
                        "target_column": target_col,
                        "cardinality": col.cardinality or "N/A",
                        "description": col.description or "-",
                        "full_condition": f"{entity_name}.{source_col} = {col.target_entity or col.reference_table}.{target_col}"
                    })
        
        return join_conditions

    @staticmethod
    def get_columns_by_datatype(columns: List[ColumnMetadata]) -> Dict[str, List[ColumnMetadata]]:
        """Group columns by their data type
        
        Returns a dictionary with data types as keys and lists of columns as values.
        Useful for organizing reports and understanding data structure.
        """
        grouped = {}
        for col in columns:
            dtype = col.datatype
            if dtype not in grouped:
                grouped[dtype] = []
            grouped[dtype].append(col)
        
        # Sort by type name for consistent ordering
        return dict(sorted(grouped.items()))

    @staticmethod
    def get_datatype_statistics(columns: List[ColumnMetadata]) -> pd.DataFrame:
        """Generate comprehensive statistics for each data type
        
        Returns DataFrame with:
        - Count: Number of columns of this type
        - Percentage: % of total columns
        - Avg Size: Average length (for sized types)
        - Max Size: Maximum length
        - Key Columns: Number that are keys
        - Associations: Number that are associations
        - Nullable: Number that allow nulls
        """
        grouped = CSNVisualizer.get_columns_by_datatype(columns)
        total = len(columns)
        
        stats = []
        for dtype, cols in grouped.items():
            # Calculate metrics
            count = len(cols)
            percentage = round((count / total) * 100, 2) if total > 0 else 0
            
            # Size metrics (for types that have length) - convert to int
            sizes = []
            for col in cols:
                if col.length:
                    try:
                        sizes.append(int(col.length))
                    except (ValueError, TypeError):
                        pass
            
            avg_size = round(sum(sizes) / len(sizes), 2) if sizes else "-"
            max_size = max(sizes) if sizes else "-"
            
            # Count key columns
            key_count = sum(1 for col in cols if col.is_key)
            
            # Count associations
            assoc_count = sum(1 for col in cols if col.is_association)
            
            # Count nullable
            nullable_count = sum(1 for col in cols if col.nullable)
            
            stats.append({
                "Data Type": dtype,
                "Count": count,
                "Percentage": f"{percentage}%",
                "Avg Size": avg_size,
                "Max Size": max_size,
                "Key Columns": key_count,
                "Associations": assoc_count,
                "Nullable": nullable_count,
            })
        
        return pd.DataFrame(stats)

    @staticmethod
    def get_columns_by_datatype_dataframe(columns: List[ColumnMetadata]) -> pd.DataFrame:
        """Get all columns organized by data type with all details"""
        grouped = CSNVisualizer.get_columns_by_datatype(columns)
        
        data = []
        for dtype, cols in grouped.items():
            data.append([dtype, "", "", "", "", "", "", "", "", ""])  # Header row
            for col in cols:
                data.append([
                    "",  # Skip data type (shown in header)
                    col.name,
                    col.description or "-",
                    "🔑" if col.is_key else "•",
                    "→" if col.is_association else "•",
                    col.target_entity or col.reference_table or "-",
                    col.check_table or "-",
                    col.length or "-",
                    "Yes" if col.nullable else "No",
                    col.constraints or "-",
                ])
        
        df = pd.DataFrame(data, columns=[
            "Data Type", "Column Name", "Description", "Key", "Assoc",
            "Target/Reference", "Check Table", "Length", "Nullable", "Constraints"
        ])
        
        return df

    @staticmethod
    def export_to_excel(
        columns: List[ColumnMetadata],
        associations: List[Dict],
        entity_name: str,
        entity_label: str,
        output_path: str
    ):
        """Export data to Excel with multiple sheets"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Sheet 1: Professional View (Simple & Clean)
                df_professional = CSNVisualizer.columns_to_professional_dataframe(columns)
                df_professional.to_excel(writer, sheet_name='Columns - Simple View', index=False)

                # Sheet 2: Detailed View (All Metadata)
                df_detailed = CSNVisualizer.columns_to_detailed_dataframe(columns)
                df_detailed.to_excel(writer, sheet_name='Columns - Detailed View', index=False)

                # Sheet 3: Data Type Statistics (NEW)
                df_dtype_stats = CSNVisualizer.get_datatype_statistics(columns)
                df_dtype_stats.to_excel(writer, sheet_name='Data Type Statistics', index=False)

                # Sheet 4: Columns by Data Type (NEW - Organized by Type)
                df_by_type = CSNVisualizer.get_columns_by_datatype_dataframe(columns)
                df_by_type.to_excel(writer, sheet_name='Columns by Type', index=False)

                # Sheet 5: Summary Statistics
                stats = CSNVisualizer.get_summary_stats(columns)
                summary_data = []
                for key, value in stats.items():
                    if isinstance(value, dict):
                        summary_data.append([key, json.dumps(value, indent=2)])
                    else:
                        summary_data.append([key, value])

                df_summary = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
                df_summary.to_excel(writer, sheet_name='Summary', index=False)

                # Sheet 6: Associations
                if associations:
                    df_assoc = pd.DataFrame(associations)
                    df_assoc.to_excel(writer, sheet_name='Associations', index=False)

                # Sheet 7: Highlighted View (Key Columns & Relationships)
                highlighted = CSNVisualizer.highlight_important_columns(columns)
                highlight_rows = []
                for category, items in highlighted.items():
                    highlight_rows.append([category, ""])
                    for item in items:
                        highlight_rows.append(["", json.dumps(item, indent=2)])

                df_highlighted = pd.DataFrame(highlight_rows, columns=['Category', 'Details'])
                df_highlighted.to_excel(writer, sheet_name='Highlighted View', index=False)

                return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False

    @staticmethod
    def export_to_html(
        columns: List[ColumnMetadata],
        entity_name: str,
        entity_label: str,
        output_path: str
    ):
        """Export to interactive HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CSN Report: {entity_name}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background: #f5f5f5; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 5px; }}
                .header h1 {{ margin: 0; font-size: 2.5em; }}
                .header p {{ margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9; }}
                .container {{ background: white; padding: 30px; border-radius: 5px; margin-top: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .section {{ margin-bottom: 40px; }}
                .section h2 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
                .section h3 {{ color: #555; margin-top: 25px; padding: 10px; background: #f0f0f0; border-left: 4px solid #667eea; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                th {{ background: #667eea; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background: #f9f9f9; }}
                .key {{ background: #fff3cd; padding: 3px 8px; border-radius: 3px; font-weight: bold; }}
                .association {{ background: #d1ecf1; padding: 3px 8px; border-radius: 3px; color: #0c5460; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }}
                .stat-card {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #667eea; }}
                .stat-card .value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
                .stat-card .label {{ color: #666; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧩 CSN Object Visualizer Report</h1>
                <p>{entity_label or entity_name}</p>
            </div>

            <div class="container">
                <div class="section">
                    <h2>📊 Overview</h2>
                    <div class="stats">
                        <div class="stat-card">
                            <div class="value">{len(columns)}</div>
                            <div class="label">Total Columns</div>
                        </div>
        """

        # Add summary statistics
        stats = CSNVisualizer.get_summary_stats(columns)
        html_content += f"""
                        <div class="stat-card">
                            <div class="value">{stats['Key Columns']}</div>
                            <div class="label">Key Columns</div>
                        </div>
                        <div class="stat-card">
                            <div class="value">{stats['Association Columns']}</div>
                            <div class="label">Associations</div>
                        </div>
                    </div>
                </div>

                <div class="section">
                    <h2>📈 Data Type Statistics</h2>
                    <table>
                        <tr>
                            <th>Data Type</th>
                            <th>Count</th>
                            <th>Percentage</th>
                            <th>Avg Size</th>
                            <th>Max Size</th>
                            <th>Key Columns</th>
                            <th>Associations</th>
                            <th>Nullable</th>
                        </tr>
        """
        
        # Add data type statistics
        df_dtype_stats = CSNVisualizer.get_datatype_statistics(columns)
        for _, row in df_dtype_stats.iterrows():
            html_content += f"""
                        <tr>
                            <td><strong>{row['Data Type']}</strong></td>
                            <td>{row['Count']}</td>
                            <td>{row['Percentage']}</td>
                            <td>{row['Avg Size']}</td>
                            <td>{row['Max Size']}</td>
                            <td>{row['Key Columns']}</td>
                            <td>{row['Associations']}</td>
                            <td>{row['Nullable']}</td>
                        </tr>
            """
        
        html_content += """
                    </table>
                </div>

                <div class="section">
                    <h2>📋 Columns Organized by Data Type</h2>
        """

        # Add columns grouped by data type
        grouped = CSNVisualizer.get_columns_by_datatype(columns)
        for dtype, cols in grouped.items():
            html_content += f"""
                    <h3>{dtype} ({len(cols)} columns)</h3>
                    <table>
                        <tr>
                            <th>Column Name</th>
                            <th>Description</th>
                            <th>Key</th>
                            <th>Target/Check Table</th>
                            <th>Length</th>
                            <th>Nullable</th>
                        </tr>
            """
            for col in cols:
                key_badge = '<span class="key">KEY</span>' if col.is_key else ""
                target_info = col.target_entity or col.check_table or "-"
                nullable = "Yes" if col.nullable else "No"
                
                html_content += f"""
                        <tr>
                            <td><strong>{col.name}</strong></td>
                            <td>{col.description or '-'}</td>
                            <td>{key_badge}</td>
                            <td>{target_info}</td>
                            <td>{col.length or '-'}</td>
                            <td>{nullable}</td>
                        </tr>
            """
            
            html_content += """
                    </table>
            """

        html_content += """
                </div>
            </div>
        </body>
        </html>
        """

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error exporting to HTML: {e}")
            return False
