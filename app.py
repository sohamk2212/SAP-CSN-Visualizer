import streamlit as st
import json
import pandas as pd
from pathlib import Path
from src.parser import CSNParser
from src.visualizer import CSNVisualizer

# Page Configuration
st.set_page_config(
    page_title="CSN Object Visualizer",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Make table responsive */
    [data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
    }
    
    /* Fancy cards and containers */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card-alt {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Styled boxes */
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(255, 193, 7, 0.2);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
    }
    
    /* Styled tabs */
    [data-baseweb="tab-list"] {
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 0.75rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    
    /* Better text input and select */
    [data-testid="stTextInput"] input {
        border-radius: 0.5rem;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
    }
    
    [data-testid="stTextInput"] input:focus {
        border: 2px solid #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    button {
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Responsive grid for columns */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        .metric-container {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "datatype_filter" not in st.session_state:
    st.session_state.datatype_filter = None
if "other_types" not in st.session_state:
    st.session_state.other_types = []

# Title
st.markdown("""
    # 🧩 CSN Object Visualizer
    ### Simplify, Parse & Visualize SAP Core Schema Notation (CSN) Files
    #### Perfect for understanding complex database structures - even for beginners!
""")

# ============ HOW TO GET CSN SECTION ============
with st.expander("📖 **How to Get CSN Data from SAP?**", expanded=False):
    st.markdown("""
    ### Step-by-Step Guide to Fetch CSN
    
    #### **1. URL Construction**
    To fetch CSN data from your SAP system, use this generic URL pattern:
    
    ```
    https://<YOUR_SAP_SYSTEM_URL>/sap/opu/odata4/sap/csn_exposure_v4/srvd_a2x/sap/csn_exposure/0001/Entities('<ENTITY_NAME>')?$expand=_Source
    ```
    
    **Replace the following:**
    - `<YOUR_SAP_SYSTEM_URL>` → Your SAP Cloud or On-Premise system URL
      - Example: `my407343-api.s4hana.cloud.sap`
      - Or: `sap-prod.yourcompany.com:8000`
    - `<ENTITY_NAME>` → The entity you want to explore
      - Example: `I_Product`, `I_Customer`, `I_SalesOrder`, etc.
    
    #### **2. How to Get It**
    
    **Option A: Using Browser/Postman**
    - Open your browser or Postman
    - Navigate to the constructed URL
    - Authenticate with your SAP credentials
    - The response will be a JSON object - copy the entire response
    
    **Option B: Using SAP OData Test Client**
    - Go to: `/ui/tools/osdata/` on your SAP system
    - Navigate to: `csn_exposure_v4` service
    - Select an entity and fetch the data
    
    **Option C: Using cURL (Command Line)**
    ```bash
    curl -X GET "https://<YOUR_SYSTEM>/sap/opu/odata4/sap/csn_exposure_v4/srvd_a2x/sap/csn_exposure/0001/Entities('I_Product')?\\$expand=_Source" \\
         -u username:password \\
         -H "Accept: application/json"
    ```
    
    #### **3. What CSN Response Looks Like**
    
    Here's a sample structure (simplified):
    """)
    
    # Show sample CSN response
    sample_csn = {
        "@odata.context": "$metadata#Entities/$entity",
        "@odata.metadataEtag": "W/\"20260801T042100Z\"",
        "EntityName": "I_Product",
        "EntityLabel": "Product",
        "ReleaseContract": "C1",
        "ReleaseState": "RELEASED",
        "ModelingPattern": "",
        "LastModifiedAt": "2026-08-01T04:21:00Z",
        "_Source": {
            "ObjectName": "I_Product",
            "Kind": "entity",
            "SourceString": "[Contains full type definitions and column metadata - shown as collapsed in this view]"
        }
    }
    
    st.json(sample_csn)
    
    st.markdown("""
    #### **4. What to Do With the Response**
    
    1. **Copy the entire JSON response** from your browser/Postman
    2. **Save it to a file** (name it anything, e.g., `I_Product.json` or `I_Product.txt`)
    3. **Upload here** ↙️ in the sidebar under "📂 File Upload"
    4. **Visualizer will parse it** automatically and show you:
       - All columns/elements with their data types
       - SAP ABAP types (CHAR, DATS, TIMS, QUAN, DECIMAL, etc.)
       - Field sizes, precision, and scale
       - Key fields, nullable fields, and associations
       - Data type distribution charts
       - Relationship mappings between entities
    
    #### **⚠️ Common Issues**
    
    | Issue | Solution |
    |-------|----------|
    | Authentication failed | Ensure you're using correct credentials for your SAP system |
    | Empty response | The entity name might be incorrect - check exact spelling (case-sensitive) |
    | Invalid JSON | Make sure you copied the entire response, not just part of it |
    | "No columns found" | Some entities may not expose element information - try a different entity |
    """)

# Sidebar
st.sidebar.title("📂 File Upload")
st.sidebar.markdown("---")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSN JSON file",
    type=["json", "txt"],
    help="Paste your full CSN response from SAP in a .json or .txt file"
)

# Sample data option
if st.sidebar.checkbox("Use sample data for demo", value=False):
    sample_path = Path("input_CSN.txt")
    if sample_path.exists():
        uploaded_file = sample_path

# Main content
if uploaded_file is not None:
    try:
        # Save uploaded file temporarily and parse
        with open("temp_csn.json", "w", encoding="utf-8") as f:
            if isinstance(uploaded_file, str):
                with open(uploaded_file, "r", encoding="utf-8") as src:
                    f.write(src.read())
            else:
                f.write(uploaded_file.read().decode("utf-8"))

        # Parse CSN
        parser = CSNParser("temp_csn.json")
        if not parser.load_file():
            st.error("❌ Failed to load CSN file. Please ensure it's valid JSON.")
        else:
            # Extract metadata
            entity_name, entity_label, columns, associations = parser.parse_full_entity()

            if not columns:
                st.error("❌ No columns/elements found in this CSN file.")
            else:
                # ============ HEADER SECTION ============
                st.markdown(f"### 📋 Entity: **{entity_name}**")
                if entity_label:
                    st.caption(f"📝 Label: {entity_label}")

                # ============ STATISTICS SECTION ============
                st.subheader("📊 Quick Statistics")
                stats = CSNVisualizer.get_summary_stats(columns)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Columns", stats["Total Columns"])
                with col2:
                    st.metric("🔑 Key Columns", stats["Key Columns"])
                with col3:
                    st.metric("🔗 Associations", stats["Association Columns"])
                with col4:
                    st.metric("Empty Allowed", stats["Nullable Columns"])

                # Data Type Distribution - IMPROVED
                st.markdown("#### 📊 Data Type Distribution")
                dt_dist = stats["Data Type Distribution"]
                
                if dt_dist:
                    # Group rare types as "Other" (threshold: < 2 occurrences)
                    threshold = 2
                    main_types = {}
                    other_types = []  # Track which types are in "Other"
                    other_count = 0
                    
                    for dtype, count in sorted(dt_dist.items(), key=lambda x: x[1], reverse=True):
                        if count >= threshold:
                            main_types[dtype] = count
                        else:
                            other_types.append(dtype)
                            other_count += count
                    
                    if other_count > 0:
                        main_types["Other"] = other_count
                    
                    # Store other_types in session for filtering
                    st.session_state.other_types = other_types
                    
                    # Create tabs for different visualizations
                    chart_col1, chart_col2 = st.columns([2, 1])
                    
                    with chart_col1:
                        # Visualization type selector
                        viz_type = st.radio(
                            "Visualization",
                            ["📊 Bar Chart", "🥧 Pie Chart"],
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                        
                        # Determine chart data based on active filter
                        if st.session_state.datatype_filter:
                            # Show only selected type
                            chart_data = {st.session_state.datatype_filter: main_types.get(st.session_state.datatype_filter, 0)}
                        else:
                            # Show all types
                            chart_data = main_types
                        
                        if viz_type == "📊 Bar Chart":
                            # Interactive bar chart
                            df_chart = pd.DataFrame(list(chart_data.items()), columns=["Type", "Count"]).set_index("Type")
                            st.bar_chart(df_chart)
                        else:
                            # Pie chart with proportions
                            import plotly.express as px
                            df_pie = pd.DataFrame(list(chart_data.items()), columns=["Type", "Count"])
                            fig = px.pie(df_pie, values="Count", names="Type", 
                                        title="Data Type Distribution",
                                        hole=0.3)  # Donut chart for better look
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with chart_col2:
                        # Interactive filter buttons
                        st.markdown("**Click to Filter:**")
                        
                        # Clear filter button
                        if st.button("🔄 Show All", use_container_width=True):
                            st.session_state.datatype_filter = None
                            st.rerun()
                        
                        st.divider()
                        
                        # Filter by data type (top 5 + Other)
                        for dtype in list(main_types.keys())[:5]:
                            col_text = f"{dtype} ({main_types[dtype]})"
                            if st.button(col_text, use_container_width=True):
                                st.session_state.datatype_filter = dtype
                                st.rerun()
                    
                    # Show summary statistics
                    st.caption(f"📌 Total data types: {len(dt_dist)} | Grouped view: {len(main_types)}")
                    
                    # Expandable detailed list
                    with st.expander("📋 View all data types (detailed)"):
                        cols_for_types = st.columns(3)
                        type_items = sorted(dt_dist.items(), key=lambda x: x[1], reverse=True)
                        for idx, (dt, count) in enumerate(type_items):
                            col_idx = idx % 3
                            with cols_for_types[col_idx]:
                                st.metric(dt, count)

                st.markdown("---")

                # ============ FILTER & SEARCH SECTION ============
                st.subheader("🔍 Filter & Search Columns")

                col_search1, col_search2, col_search3 = st.columns(3)

                with col_search1:
                    search_text = st.text_input("🔎 Search by name or description", placeholder="e.g., Product, Date")

                with col_search2:
                    # Build dynamic list of all data types from actual data
                    all_datatype_options = ["All"] + sorted([dt for dt in dt_dist.keys() if dt != "Other"]) + (["Other"] if "Other" in dt_dist else [])
                    
                    # Determine current selection for the selectbox
                    if st.session_state.datatype_filter:
                        current_selection = st.session_state.datatype_filter
                    else:
                        current_selection = "All"
                    
                    selected_type = st.selectbox(
                        "📌 Filter by data type",
                        all_datatype_options,
                        index=all_datatype_options.index(current_selection) if current_selection in all_datatype_options else 0
                    )
                    
                    # Update session state and rerun if selection changed
                    if selected_type != "All":
                        if st.session_state.datatype_filter != selected_type:
                            st.session_state.datatype_filter = selected_type
                            st.rerun()
                        filter_type = selected_type
                    else:
                        if st.session_state.datatype_filter:
                            st.session_state.datatype_filter = None
                            st.rerun()
                        filter_type = "All"

                with col_search3:
                    filter_key = st.selectbox(
                        "🔑 Filter by key status",
                        ["All", "Key Columns Only", "Non-Key Columns Only"]
                    )

                # Apply filters
                filtered_columns = columns
                if search_text:
                    filtered_columns = CSNVisualizer.filter_columns(filtered_columns, search_text=search_text)

                if filter_type != "All":
                    if filter_type == "Other":
                        # Filter to only show columns with data types in "Other" category
                        filtered_columns = [col for col in filtered_columns if col.datatype in st.session_state.get("other_types", [])]
                    else:
                        filtered_columns = CSNVisualizer.filter_columns(filtered_columns, by_type=filter_type)

                if filter_key == "Key Columns Only":
                    filtered_columns = CSNVisualizer.filter_columns(filtered_columns, by_key=True)
                elif filter_key == "Non-Key Columns Only":
                    filtered_columns = CSNVisualizer.filter_columns(filtered_columns, by_key=False)

                st.caption(f"Showing {len(filtered_columns)} of {len(columns)} columns")

                st.markdown("---")

                # ============ DETAILED VIEW SECTION ============
                st.subheader("📊 Column Details")

                # Tabs for different views
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["📋 Table View", "🔑 Key & Associations", "📦 Detailed Info", "⬇️ Export"]
                )

                with tab1:
                    # Table View - with view toggle
                    st.markdown("#### 📋 All Columns in Table Format")
                    
                    # Toggle between simple and detailed view
                    col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 1, 2])
                    with col_toggle1:
                        view_type = st.radio(
                            "View Type",
                            ["Simple", "Detailed"],
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                    
                    if view_type == "Simple":
                        st.caption("📌 Simple view: Most important columns for quick reference")
                        df_columns = CSNVisualizer.columns_to_professional_dataframe(filtered_columns)
                        
                        # Display with styling
                        st.dataframe(
                            df_columns,
                            width='stretch',
                            hide_index=False,
                            height=600,
                            column_config={
                                "Index": st.column_config.NumberColumn("📍", width=40),
                                "Name": st.column_config.TextColumn("Name", width=150),
                                "Description": st.column_config.TextColumn("Description", width=200),
                                "Data Type": st.column_config.TextColumn("Type", width=100),
                                "Size": st.column_config.TextColumn("Size", width=50),
                                "Key": st.column_config.TextColumn("🔑", width=40),
                                "Allow Null": st.column_config.TextColumn("Null", width=50),
                                "Check Table": st.column_config.TextColumn("Check Table", width=120),
                            }
                        )
                    else:
                        st.caption("📚 Smart view: Relevant columns with data only (responsive & clean)")
                        df_columns = CSNVisualizer.columns_to_smart_detailed_dataframe(filtered_columns)
                        
                        # Display with better styling
                        st.dataframe(
                            df_columns,
                            width='stretch',
                            hide_index=False,
                            height=600,
                        )
                    
                    st.info(f"📊 Total Columns: **{len(filtered_columns)}** | Showing: **{len(df_columns)}**")

                with tab2:
                    # Associations & Reference Tables
                    st.markdown("#### 🔗 Relationships & Foreign Keys")

                    highlighted = CSNVisualizer.highlight_important_columns(filtered_columns)
                    
                    # ===== SECTION 0: JOIN CONDITIONS (NEW!) =====
                    st.markdown("##### 🔀 JOIN CONDITIONS - Column Relationships")
                    st.caption("Shows which columns in this view link to which columns in other views")
                    
                    join_conditions = CSNVisualizer.get_join_conditions(filtered_columns, entity_name)
                    
                    if join_conditions:
                        # Filter join conditions
                        col_jc1, col_jc2 = st.columns([2, 1])
                        with col_jc1:
                            search_jc = st.text_input(
                                "🔍 Search join conditions",
                                placeholder="Search by source column or target view...",
                                key="join_search"
                            )
                        with col_jc2:
                            card_filter_jc = st.selectbox(
                                "Cardinality",
                                ["All", "1", "*"],
                                key="join_cardinality"
                            )
                        
                        # Filter
                        filtered_jc = join_conditions
                        if search_jc:
                            search_lower = search_jc.lower()
                            filtered_jc = [
                                j for j in filtered_jc
                                if search_lower in j['source_column'].lower() or 
                                   search_lower in j['target_view'].lower()
                            ]
                        
                        if card_filter_jc != "All":
                            filtered_jc = [j for j in filtered_jc if j['cardinality'] == card_filter_jc]
                        
                        if filtered_jc:
                            jc_data = []
                            for idx, jc in enumerate(filtered_jc, 1):
                                jc_data.append({
                                    "#": idx,
                                    "Source Column": jc['source_column'],
                                    "Links To": jc['target_view'],
                                    "Target Column": jc['target_column'],
                                    "Cardinality": f"1:{jc['cardinality']}",
                                    "Join Condition": jc['full_condition'],
                                    "Via": jc['association']
                                })
                            
                            df_jc = pd.DataFrame(jc_data)
                            st.dataframe(
                                df_jc,
                                width='stretch',
                                hide_index=True,
                                height=400,
                                column_config={
                                    "#": st.column_config.NumberColumn("#", width=40),
                                    "Source Column": st.column_config.TextColumn("Source Column", width=120),
                                    "Links To": st.column_config.TextColumn("Links To", width=180),
                                    "Target Column": st.column_config.TextColumn("Target Column", width=120),
                                    "Cardinality": st.column_config.TextColumn("Cardinality", width=100),
                                    "Join Condition": st.column_config.TextColumn("Join Condition", width=250),
                                    "Via": st.column_config.TextColumn("Via", width=150),
                                }
                            )
                            
                            st.caption(f"Showing {len(filtered_jc)} of {len(join_conditions)} join condition(s)")
                        else:
                            st.info("No join conditions found matching your filters.")
                    else:
                        st.info("No join conditions defined (no associations with constrained columns).")
                    
                    st.markdown("---")
                    
                    # ===== SECTION 1: KEY COLUMNS =====
                    if highlighted["Key Columns"]:
                        st.markdown("##### 🔑 Key Columns (Unique Identifiers)")
                        key_cols_data = []
                        for item in highlighted["Key Columns"]:
                            key_cols_data.append({
                                "Column": item['name'],
                                "Description": item['description'],
                                "Data Type": item['datatype']
                            })
                        if key_cols_data:
                            df_keys = pd.DataFrame(key_cols_data)
                            st.dataframe(df_keys, width='stretch', hide_index=True)
                        st.markdown("---")

                    # ===== SECTION 2: FOREIGN KEY MAPPING =====
                    st.markdown("##### 🗝️ Foreign Key Mappings")
                    
                    fk_mapping = CSNVisualizer.get_foreign_key_mapping(filtered_columns)
                    
                    if fk_mapping:
                        # Create FK mapping display
                        fk_data = []
                        for fk in fk_mapping:
                            assoc_names = ", ".join([a["name"] for a in fk["associations"]])
                            assoc_targets = ", ".join([a["target"] for a in fk["associations"]])
                            
                            fk_data.append({
                                "🔑 Foreign Key": fk["column_name"],
                                "Data Type": fk["data_type"],
                                "Check Table": fk["check_table"] or "-",
                                "Associated Entities": assoc_targets,
                                "Navigation Columns": assoc_names,
                                "Cardinality": ", ".join([a["cardinality"] for a in fk["associations"]])
                            })
                        
                        if fk_data:
                            df_fk = pd.DataFrame(fk_data)
                            st.dataframe(
                                df_fk,
                                width='stretch',
                                hide_index=True,
                                height=400,
                                column_config={
                                    "🔑 Foreign Key": st.column_config.TextColumn("🔑 Foreign Key", width=150),
                                    "Data Type": st.column_config.TextColumn("Data Type", width=120),
                                    "Check Table": st.column_config.TextColumn("Check Table", width=150),
                                    "Associated Entities": st.column_config.TextColumn("Associated Entities", width=200),
                                    "Navigation Columns": st.column_config.TextColumn("Navigation Columns", width=180),
                                    "Cardinality": st.column_config.TextColumn("Cardinality", width=100),
                                }
                            )
                            st.caption(f"Showing {len(fk_data)} foreign key mapping(s)")
                        st.markdown("---")
                    else:
                        st.info("No foreign key mappings found.")
                        st.markdown("---")

                    # ===== SECTION 3: DETAILED ASSOCIATIONS TABLE =====
                    st.markdown("##### 🔗 Detailed Associations")
                    
                    # Get associations with FK info
                    all_associations = CSNVisualizer.get_associations_with_fk(filtered_columns)
                    
                    if all_associations:
                        # Add filters at the top
                        col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 1])
                        with col_filter1:
                            search_assoc = st.text_input(
                                "🔍 Search associations",
                                placeholder="Search by name or target entity...",
                                key="assoc_search"
                            )
                        with col_filter2:
                            filter_fk = st.selectbox(
                                "Filter by FK Column",
                                ["All"] + sorted(list(set([a["foreign_key"] for a in all_associations if a["foreign_key"] != "No FK mapping"]))),
                                key="assoc_fk_filter"
                            )
                        with col_filter3:
                            filter_card = st.selectbox(
                                "Cardinality",
                                ["All", "1", "*"],
                                key="assoc_cardinality"
                            )
                        
                        # Filter associations
                        filtered_assoc = all_associations
                        
                        if search_assoc:
                            search_lower = search_assoc.lower()
                            filtered_assoc = [
                                a for a in filtered_assoc
                                if search_lower in a['name'].lower() or search_lower in a['target'].lower()
                            ]
                        
                        if filter_fk != "All":
                            filtered_assoc = [a for a in filtered_assoc if a['foreign_key'] == filter_fk]
                        
                        if filter_card != "All":
                            filtered_assoc = [a for a in filtered_assoc if a['cardinality'] == filter_card]
                        
                        # Display associations in table format
                        if filtered_assoc:
                            assoc_data = []
                            for idx, item in enumerate(filtered_assoc, 1):
                                assoc_data.append({
                                    "#": idx,
                                    "Association": item['name'],
                                    "Target Entity": item['target'],
                                    "Based On FK": item['foreign_key'],
                                    "Cardinality": item['cardinality'],
                                    "Description": item['description'],
                                    "Join Condition": item['on_clause']
                                })
                            
                            df_assoc = pd.DataFrame(assoc_data)
                            st.dataframe(
                                df_assoc,
                                width='stretch',
                                hide_index=True,
                                height=600,
                                column_config={
                                    "#": st.column_config.NumberColumn("#", width=40),
                                    "Association": st.column_config.TextColumn("Association", width=200),
                                    "Target Entity": st.column_config.TextColumn("Target Entity", width=180),
                                    "Based On FK": st.column_config.TextColumn("🔑 Based On FK", width=150),
                                    "Cardinality": st.column_config.TextColumn("Cardinality", width=80),
                                    "Description": st.column_config.TextColumn("Description", width=150),
                                    "Join Condition": st.column_config.TextColumn("Join Condition", width=200),
                                }
                            )
                            
                            st.caption(f"Showing {len(filtered_assoc)} of {len(all_associations)} associations")
                        else:
                            st.info("No associations found matching your filters.")
                    else:
                        st.info("No associations found.")

                with tab3:
                    # Detailed Information
                    st.markdown("#### 📖 Detailed Column Information")

                    # Search box to narrow down columns
                    col_search = st.text_input(
                        "🔍 Search columns",
                        placeholder="Type column name to search...",
                        key="detail_search"
                    )

                    # Filter columns based on search
                    search_results = [
                        c for c in filtered_columns 
                        if col_search.lower() in c.name.lower() or col_search.lower() in (c.description or "").lower()
                    ] if col_search else filtered_columns

                    if search_results:
                        col_selector = st.selectbox(
                            "Select a column to view details",
                            [c.name for c in search_results],
                            key="detail_selector"
                        )

                        selected_col = next((c for c in search_results if c.name == col_selector), None)
                        if selected_col:
                            col_info = {
                                "Column Name": selected_col.name,
                                "Description": selected_col.description or "N/A",
                                "Data Type": selected_col.datatype,
                                "Is Key": "Yes" if selected_col.is_key else "No",
                                "Is Association": "Yes" if selected_col.is_association else "No",
                                "Target Entity": selected_col.target_entity or "-",
                                "Reference Table": selected_col.reference_table or "-",
                                "Reference Column": selected_col.reference_column or "-",
                                "Constrained Column": selected_col.constrained_column or "-",
                                "Check Table": selected_col.check_table or "-",
                                "Cardinality": selected_col.cardinality or "-",
                                "Constraints": selected_col.constraints or "None",
                                "Length": selected_col.length or "-",
                                "Precision": selected_col.precision or "-",
                                "Scale": selected_col.scale or "-",
                                "Default Value": selected_col.default_value or "-",
                                "Nullable": "Yes" if selected_col.nullable else "No",
                            }

                            for key, value in col_info.items():
                                st.write(f"**{key}**: {value}")
                    else:
                        st.info("No columns found matching your search. Try a different keyword.")

                with tab4:
                    # Export Options
                    st.markdown("#### ⬇️ Export Results")

                    # Export to Excel
                    if st.button("📊 Generate Excel Report"):
                        excel_path = f"CSN_Report_{entity_name}.xlsx"
                        if CSNVisualizer.export_to_excel(
                            filtered_columns if filtered_columns != columns else columns,
                            associations,
                            entity_name,
                            entity_label,
                            excel_path
                        ):
                            with open(excel_path, "rb") as f:
                                st.download_button(
                                    label="💾 Download Excel Report",
                                    data=f.read(),
                                    file_name=excel_path,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            st.success("✅ Excel report generated successfully!")
                        else:
                            st.error("❌ Error generating Excel report.")

                    st.markdown("---")

                    # Export to HTML
                    if st.button("📄 Generate HTML Report"):
                        html_path = f"CSN_Report_{entity_name}.html"
                        if CSNVisualizer.export_to_html(
                            filtered_columns if filtered_columns != columns else columns,
                            entity_name,
                            entity_label,
                            html_path
                        ):
                            with open(html_path, "r", encoding="utf-8") as f:
                                st.download_button(
                                    label="💾 Download HTML Report",
                                    data=f.read(),
                                    file_name=html_path,
                                    mime="text/html"
                                )
                            st.success("✅ HTML report generated successfully!")
                        else:
                            st.error("❌ Error generating HTML report.")

                    st.markdown("---")

                    # Export to CSV
                    if st.button("📄 Download as CSV"):
                        df_export = CSNVisualizer.columns_to_dataframe(
                            filtered_columns if filtered_columns != columns else columns
                        )
                        csv_data = df_export.to_csv(index=False)
                        st.download_button(
                            label="💾 Download CSV",
                            data=csv_data,
                            file_name=f"CSN_Report_{entity_name}.csv",
                            mime="text/csv"
                        )

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please ensure your file is a valid CSN JSON format.")

else:
    # Default welcome screen
    st.markdown("""
    ---
    ### 🚀 Welcome to CSN Object Visualizer!

    This tool helps you **understand complex SAP Core Schema Notation (CSN)** files by breaking them down into:

    ✅ **Key Columns** - Unique identifiers  
    ✅ **Data Types** - Column format information (CDS + SAP ABAP types)  
    ✅ **Relationships** - JOIN conditions and associations between entities  
    ✅ **Field Metadata** - Sizes, precision, scale, domains  
    ✅ **Descriptions** - What each column means  
    """)
    
    # Features overview in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 📊 **Data Analysis**
        - Type distribution charts
        - Statistics & metrics
        - Column grouping by type
        - Size & precision analysis
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 **Search & Filter**
        - Quick text search
        - Filter by data type
        - View key columns
        - Find associations
        """)
    
    with col3:
        st.markdown("""
        ### 📤 **Export Reports**
        - Excel (7 sheets)
        - HTML (formatted)
        - CSV (for analysis)
        - Print-ready layouts
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Quick Start:

    **Step 1: Get Your CSN**
    - Expand the "📖 How to Get CSN Data from SAP?" section above
    - Follow the URL pattern and fetch from your SAP system
    - Copy the entire JSON response
    
    **Step 2: Upload File**
    - Save the response to a `.json` or `.txt` file
    - Click "Browse files" in the sidebar ⬅️
    - Select your file
    
    **Step 3: Explore**
    - View statistics and data type distribution
    - Click on data type buttons to filter
    - Switch between Table, Key & Associations, and Detailed Info tabs
    - Search for specific columns
    
    **Step 4: Export**
    - Generate Excel report with 7 detailed sheets
    - Export as HTML for sharing
    - Download CSV for further analysis

    ### 💡 Perfect For:
    - 👨‍💼 Business Analysts (understanding entity relationships)
    - 👨‍💻 Developers (API integration & field mapping)
    - 📊 Data Analysts (data type analysis & distribution)
    - 🎓 Beginners (learning SAP database schemas)
    - 🏢 Enterprise teams (documentation & onboarding)

    ### 📚 Need Help?
    - **Don't know how to get CSN?** → Expand "📖 How to Get CSN Data from SAP?" above
    - **Sample data available** → Check "Use sample data for demo" in sidebar
    - **Questions?** → Read the docs or check FAQ

    ---
    """)

    # Display current workspace info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📁 Current Workspace")
    st.sidebar.write("📍 Location: `/CSN_Object_Visualizer`")

    # Instructions
    st.sidebar.markdown("### 📖 Instructions")
    st.sidebar.markdown("""
    1. Click "Browse files" above
    2. Select your CSN JSON file
    3. Explore the data with filters and search
    4. Export your findings
    """)
