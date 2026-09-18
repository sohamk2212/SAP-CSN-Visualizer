"""CSN Parser - Extract and structure CSN metadata"""

import json
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class ColumnMetadata:
    """Represents a single column/element in CSN"""
    name: str
    description: str = ""
    datatype: str = ""  # CDS type name (e.g., PRODUCTNUMBER)
    sap_datatype: str = ""  # SAP ABAP type (e.g., CHAR, DEC, DATS, TIMS, QUAN)
    is_key: bool = False
    is_association: bool = False
    target_entity: str = ""
    cardinality: str = ""
    reference_table: str = ""
    reference_column: str = ""
    constrained_column: str = ""
    check_table: str = ""  # Actual table reference (from associations)
    sap_domain: str = ""  # SAP domain name (e.g., MATNR, DATUM, TIME)
    constraints: str = ""
    length: str = ""  # For CHAR, RAW, STRING
    nullable: bool = True
    precision: str = ""  # For DECIMAL, QUAN
    scale: str = ""  # For DECIMAL, QUAN
    default_value: str = ""


class CSNParser:
    """Parse CSN JSON format and extract structured metadata"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.raw_data = {}
        self.parsed_entities = {}
        self.type_definitions = {}  # Cache for type definitions
        self.localization_data = {}  # Cache for localization/i18n data

    def load_file(self) -> bool:
        """Load CSN JSON file (handles both .json and .txt formats)"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.raw_data = json.loads(content)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def extract_entity_name(self) -> str:
        """Extract entity name from CSN data"""
        return self.raw_data.get("EntityName", "Unknown")

    def extract_entity_label(self) -> str:
        """Extract entity label/description"""
        return self.raw_data.get("EntityLabel", "")

    def extract_release_state(self) -> str:
        """Extract release state"""
        return self.raw_data.get("ReleaseState", "")

    def get_definitions(self) -> Dict[str, Any]:
        """Extract definitions from nested SourceString if needed"""
        # First check if definitions exist at top level
        if "definitions" in self.raw_data:
            return self.raw_data["definitions"]

        # Try to parse SourceString
        if "_Source" in self.raw_data and "SourceString" in self.raw_data["_Source"]:
            try:
                source_str = self.raw_data["_Source"]["SourceString"]
                # Parse the nested JSON string
                parsed = json.loads(source_str)
                return parsed.get("definitions", {})
            except:
                return {}

        return {}

    def _build_type_definitions_map(self, definitions: Dict[str, Any]) -> None:
        """Build a cache map of type definitions for quick lookup"""
        self.type_definitions = {}
        for name, defn in definitions.items():
            if defn.get("kind") == "type":
                self.type_definitions[name] = defn

    def _build_localization_map(self, entity_name: str) -> None:
        """Build localization map from _LocalizationData
        
        Extracts actual labels and descriptions from i18n data
        Maps: {field_name: {"label": "...", "description": "..."}}
        """
        self.localization_data = {}
        
        try:
            # Check if _LocalizationData exists in response
            if "_LocalizationData" not in self.raw_data:
                return
            
            localization_array = self.raw_data["_LocalizationData"]
            if not localization_array:
                return
            
            # Get the first localization entry (usually English)
            for loc_entry in localization_array:
                if loc_entry.get("Kind") == "entity" and loc_entry.get("Locale") == "en":
                    i18n_string = loc_entry.get("I18nString", "{}")
                    
                    # Parse the I18n JSON string
                    i18n_data = json.loads(i18n_string)
                    i18n_dict = i18n_data.get("i18n", {}).get("en", {})
                    
                    # Build mapping: extract field descriptions
                    # Pattern: "I_<ENTITY>.<FIELD>@ENDUSERTEXT.LABEL"
                    for i18n_key, i18n_value in i18n_dict.items():
                        # Extract field name from i18n key
                        # Format: "ENTITY.FIELDNAME@ENDUSERTEXT.LABEL" or "ENTITY.FIELDNAME@ENDUSERTEXT.QUICKINFO"
                        if "@ENDUSERTEXT.LABEL" in i18n_key or "@ENDUSERTEXT.QUICKINFO" in i18n_key:
                            parts = i18n_key.split(".")
                            if len(parts) >= 2:
                                # Get field name (second part, before @)
                                field_part = parts[1].split("@")[0]
                                
                                if field_part not in self.localization_data:
                                    self.localization_data[field_part] = {}
                                
                                # Determine if this is LABEL or QUICKINFO
                                if "@ENDUSERTEXT.LABEL" in i18n_key:
                                    self.localization_data[field_part]["label"] = i18n_value
                                elif "@ENDUSERTEXT.QUICKINFO" in i18n_key:
                                    self.localization_data[field_part]["description"] = i18n_value
                    
                    break
        except Exception as e:
            print(f"Error building localization map: {e}")
            self.localization_data = {}

    def _extract_sap_type_info(self, type_name: str) -> Dict[str, str]:
        """Extract SAP ABAP type info from type definition
        
        Returns dict with keys: sap_datatype, length, precision, scale, check_table
        """
        if not type_name or type_name not in self.type_definitions:
            return {}

        type_def = self.type_definitions[type_name]
        
        # Extract SAP ABAP type (e.g., 'CHAR' from 'abap.char')
        abap_type = type_def.get("type", "")
        sap_type_map = {
            "abap.char": "CHAR",
            "abap.nchar": "NCHAR",
            "abap.raw": "RAW",
            "abap.string": "STRING",
            "abap.int8": "INT8",
            "abap.int16": "INT16",
            "abap.int32": "INT32",
            "abap.int64": "INT64",
            "abap.integer": "INTEGER",
            "abap.dec": "DECIMAL",
            "abap.decfloat": "DECFLOAT",
            "abap.float": "FLOAT",
            "abap.date": "DATS",
            "abap.time": "TIMS",
            "abap.daytime": "DAYTIME",
            "abap.timestamp": "TIMESTAMP",
            "abap.utcdatetime": "UTCDATETIME",
            "abap.bool": "BOOLEAN",
            "abap.boolean": "BOOLEAN",
            "abap.guid": "GUID",
            "abap.quantity": "QUAN",
            "abap.quan": "QUAN",
            "abap.amount": "CURR",
            "abap.curr": "CURR",
            "abap.unit": "UNIT",
        }
        
        sap_datatype = sap_type_map.get(abap_type, abap_type.replace("abap.", "").upper())
        
        result = {"sap_datatype": sap_datatype}
        
        # Extract length (or use standard sizes for date/time types)
        if type_def.get("length"):
            result["length"] = str(type_def.get("length"))
        elif sap_datatype == "DATS":
            result["length"] = "8"  # Standard DATS size
        elif sap_datatype == "TIMS":
            result["length"] = "6"  # Standard TIMS size
        
        # Extract precision and scale
        if type_def.get("precision"):
            result["precision"] = str(type_def.get("precision"))
        if type_def.get("scale"):
            result["scale"] = str(type_def.get("scale"))
        
        # Extract domain name (SAP domain, not check table)
        if type_def.get("abap_meta", {}).get("domainName"):
            result["sap_domain"] = type_def.get("abap_meta", {}).get("domainName")
        
        return result

    def _get_localized_description(self, field_name: str) -> str:
        """Get localized description for a field from i18n data
        
        Prefers QUICKINFO (tooltip) over LABEL (field name)
        """
        # Convert to uppercase to match localization keys (they're stored in UPPERCASE)
        field_key = field_name.upper()
        
        if field_key not in self.localization_data:
            return ""
        
        loc_data = self.localization_data[field_key]
        # Prefer description (QUICKINFO) over label
        return loc_data.get("description") or loc_data.get("label") or ""

    def parse_columns(self, entity_name: str, elements: Dict) -> List[ColumnMetadata]:
        """Parse columns/elements from entity definition"""
        columns = []

        for col_name, col_meta in elements.items():
            col = ColumnMetadata(name=col_name)

            # Extract description/label
            # First try localization data (actual descriptions from i18n)
            col.description = self._get_localized_description(col_name)
            
            # Fall back to inline metadata if localization not available
            if not col.description:
                col.description = (
                    col_meta.get("@EndUserText.label") or
                    col_meta.get("@title") or
                    col_meta.get("@UI.label") or
                    ""
                )

            # Extract datatype
            datatype = col_meta.get("type", "unknown")
            col.datatype = datatype

            # Extract SAP ABAP type info (CHAR, DEC, DATS, etc.)
            sap_type_info = self._extract_sap_type_info(datatype)
            if sap_type_info:
                col.sap_datatype = sap_type_info.get("sap_datatype", "")
                if "length" in sap_type_info:
                    col.length = sap_type_info["length"]
                if "precision" in sap_type_info:
                    col.precision = sap_type_info["precision"]
                if "scale" in sap_type_info:
                    col.scale = sap_type_info["scale"]
                if "sap_domain" in sap_type_info and not col.sap_domain:
                    col.sap_domain = sap_type_info["sap_domain"]

            # Check if association or composition
            if "cds.Association" in str(datatype):
                col.is_association = True
                col.target_entity = col_meta.get("target", "")
                cardinality = col_meta.get("cardinality", {})
                col.cardinality = str(cardinality.get("max", "1"))
                col.reference_table = col.target_entity

                # Extract ON clause for reference column
                if "on" in col_meta:
                    col.constrained_column = self._format_on_clause(col_meta["on"])

            elif "cds.Composition" in str(datatype):
                col.is_association = True
                col.target_entity = col_meta.get("target", "")
                col.cardinality = "*"
                col.reference_table = col.target_entity

            # Check if key
            if col_meta.get("key"):
                col.is_key = True

            # Extract length (override if already set from type definition)
            if col_meta.get("length"):
                col.length = col_meta.get("length", "")

            # Extract precision and scale (override if already set from type definition)
            if col_meta.get("precision"):
                col.precision = col_meta.get("precision", "")
            if col_meta.get("scale"):
                col.scale = col_meta.get("scale", "")

            # Extract default value
            col.default_value = col_meta.get("default", "")

            # Extract constraints
            constraints = []
            if col_meta.get("notNull"):
                constraints.append("NOT NULL")
                col.nullable = False
            if col_meta.get("unique"):
                constraints.append("UNIQUE")
            col.constraints = ", ".join(constraints)

            # Try to extract check table from annotations if not already set
            if not col.check_table and "@Semantics.valueList" in col_meta:
                col.check_table = col_meta["@Semantics.valueList"].get("entity", "")

            columns.append(col)

        return columns

    def _format_on_clause(self, on_clause: Any) -> str:
        """Format ON clause for readability"""
        try:
            if isinstance(on_clause, list):
                parts = []
                for item in on_clause:
                    if isinstance(item, dict) and "ref" in item:
                        parts.append(".".join(item["ref"]))
                    elif isinstance(item, str) and item not in ["=", "==", "<", ">"]:
                        parts.append(item)
                return " ".join(parts)
            return str(on_clause)
        except:
            return str(on_clause)

    def get_associations(self, elements: Dict) -> List[Dict]:
        """Extract all associations from entity"""
        associations = []
        for col_name, col_meta in elements.items():
            datatype = col_meta.get("type", "")
            if "Association" in str(datatype) or "Composition" in str(datatype):
                associations.append({
                    "name": col_name,
                    "type": "Association" if "Association" in str(datatype) else "Composition",
                    "target": col_meta.get("target", ""),
                    "cardinality": str(col_meta.get("cardinality", {}).get("max", "1")),
                    "description": col_meta.get("@EndUserText.label", "")
                })
        return associations

    def parse_full_entity(self) -> Tuple[str, str, List[ColumnMetadata], List[Dict]]:
        """Parse complete entity and return metadata"""
        entity_name = self.extract_entity_name()
        entity_label = self.extract_entity_label()
        
        definitions = self.get_definitions()
        
        # Build type definitions map for quick lookup
        self._build_type_definitions_map(definitions)
        
        # Build localization map for actual descriptions from i18n data
        self._build_localization_map(entity_name)
        
        # Get the main entity definition
        entity_def = None
        if entity_name in definitions:
            entity_def = definitions[entity_name]
        elif definitions and len(definitions) > 0:
            # Use first definition if exact match not found
            entity_def = list(definitions.values())[0]

        if not entity_def:
            return entity_name, entity_label, [], []

        elements = entity_def.get("elements", {})
        columns = self.parse_columns(entity_name, elements)
        associations = self.get_associations(elements)

        return entity_name, entity_label, columns, associations
