
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Sample & Location Management",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM UI STYLING
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F4F7FB;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 1.7rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}

[data-testid="stSidebar"] {
    background: #10243E;
    border-right: 1px solid #203A59;
}

[data-testid="stSidebar"] * {
    color: #E7EEF8;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #CBD8E8;
}

[data-testid="stSidebar"] .stRadio label {
    color: #FFFFFF !important;
    font-weight: 500;
}

.hero {
    background: linear-gradient(115deg, #102D50, #1766A5);
    padding: 27px 30px;
    border-radius: 17px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 7px 22px rgba(16,45,80,0.12);
}

.hero h1 {
    color: white;
    font-size: 27px;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #D9E9F8;
    margin: 8px 0 0 0;
    font-size: 13px;
}

.section-title {
    font-size: 19px;
    font-weight: 750;
    color: #18324F;
    margin: 18px 0 12px 0;
}

.kpi-card {
    background: white;
    border: 1px solid #E5EBF2;
    border-radius: 13px;
    padding: 19px;
    min-height: 112px;
    box-shadow: 0 3px 12px rgba(20,50,80,0.035);
}

.kpi-label {
    font-size: 12px;
    color: #75849A;
    font-weight: 600;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 27px;
    color: #18324F;
    font-weight: 800;
}

.kpi-icon {
    font-size: 20px;
    float: right;
}

.sample-card {
    background: white;
    border: 1px solid #E3EAF2;
    border-radius: 14px;
    padding: 20px;
    margin: 10px 0 16px 0;
    box-shadow: 0 3px 12px rgba(20,50,80,0.035);
}

.sample-id {
    color: #1766A5;
    font-size: 17px;
    font-weight: 800;
}

.sample-meta {
    color: #718096;
    font-size: 12px;
}

.location-tag {
    display: inline-block;
    background: #EAF3FF;
    color: #1766A5;
    padding: 6px 11px;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 700;
}

.status-tag {
    display: inline-block;
    background: #E7F7EE;
    color: #16834A;
    padding: 6px 11px;
    border-radius: 7px;
    font-size: 11px;
    font-weight: 700;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: #1766A5;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 650;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: #104D80;
    color: white;
    border: none;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] {
    border-radius: 8px;
}

.stTextInput label, .stSelectbox label,
.stTextArea label, .stFileUploader label {
    font-weight: 650;
    color: #314761;
}

hr {
    border-color: #E6ECF3;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
COLUMNS = [
    "Sample ID", "Lot Number", "Sample Type",
    "Product Name", "Location", "Image Path",
    "Image Data", "Date"
]

if "samples_db" not in st.session_state:
    st.session_state.samples_db = pd.DataFrame(columns=COLUMNS)

if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

# =========================================================
# CONSTANTS
# =========================================================
SAMPLE_TYPES = [
    "Underpad Sample",
    "Retention Sample",
    "Evaluation Sample",
    "Competitive Sample"
]

LOCATIONS = [
    "Store A - Rack A1",
    "Store A - Rack A2",
    "Store A - Rack A3",
    "Lab Room B - Rack B1",
    "Lab Room B - Rack B2",
    "Quality Room C - Rack C1",
    "Quality Room C - Rack C2"
]

df = st.session_state.samples_db

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("""
    <div style="padding:15px 5px 25px 5px;">
        <div style="font-size:32px;">📦</div>
        <div style="font-size:19px;font-weight:800;color:white;">
            SAMPLE TRACKER
        </div>
        <div style="font-size:11px;color:#9FB5CE;">
            QUALITY MANAGEMENT SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### MAIN MENU")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Search Samples",
            "Register Sample",
            "Sample Database"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div style="font-size:11px;color:#A8BCD2;line-height:1.8;">
        <b>MODULE</b><br>
        Sample Management<br>
        Storage & Location Tracking<br>
        Quality Reference Samples<br><br>
        <b>VERSION</b><br>
        Version 2.0
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
    <h1>Sample & Location Tracking System</h1>
    <p>Centralized sample registration, identification,
    search and physical storage location management.</p>
</div>
""", unsafe_allow_html=True)

# Refresh database reference
df = st.session_state.samples_db

# =========================================================
# KPI FUNCTION
# =========================================================
def kpi_card(label, value, icon):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SAMPLE CARD FUNCTION
# =========================================================
def display_sample(row):

    st.markdown('<div class="sample-card">', unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            f'<div class="sample-id">{row["Sample ID"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="sample-meta">Registered: {row["Date"]}</div>',
            unsafe_allow_html=True
        )

        st.write("")
        st.write(f"**Lot Number:** {row['Lot Number']}")
        st.write(f"**Sample Type:** {row['Sample Type']}")
        st.write(f"**Product:** {row['Product Name']}")

        st.markdown(
            f'<span class="location-tag">📍 {row["Location"]}</span>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<span class="status-tag">● REGISTERED</span>',
            unsafe_allow_html=True
        )

    with right:
        image_data = row.get("Image Data")
        image_path = row.get("Image Path")

        if isinstance(image_data, bytes):
            st.image(image_data, use_container_width=True)
        elif isinstance(image_path, str) and image_path.strip():
            try:
                st.image(image_path, use_container_width=True)
            except Exception:
                st.info("No valid location image available.")
        else:
            st.info("No location image available.")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 1. DASHBOARD
# =========================================================
if page == "Dashboard":

    st.markdown('<div class="section-title">Management Overview</div>',
                unsafe_allow_html=True)

    total = len(df)

    underpad = (
        df["Sample Type"].eq("Underpad Sample").sum()
        if total else 0
    )

    retention = (
        df["Sample Type"].eq("Retention Sample").sum()
        if total else 0
    )

    evaluation = (
        df["Sample Type"].eq("Evaluation Sample").sum()
        if total else 0
    )

    competitive = (
        df["Sample Type"].eq("Competitive Sample").sum()
        if total else 0
    )

    locations = df["Location"].nunique() if total else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("TOTAL REGISTERED SAMPLES", total, "📦")
    with c2:
        kpi_card("UNDERPAD SAMPLES", underpad, "🧾")
    with c3:
        kpi_card("RETENTION SAMPLES", retention, "🔒")

    st.write("")

    c4, c5, c6 = st.columns(3)
    with c4:
        kpi_card("EVALUATION SAMPLES", evaluation, "🧪")
    with c5:
        kpi_card("COMPETITIVE SAMPLES", competitive, "📊")
    with c6:
        kpi_card("ACTIVE STORAGE LOCATIONS", locations, "📍")

    st.markdown('<div class="section-title">Sample Distribution</div>',
                unsafe_allow_html=True)

    if total:
        col1, col2 = st.columns([1, 1])

        with col1:
            distribution = (
                df["Sample Type"].value_counts().rename_axis("Sample Type")
                .reset_index(name="Quantity")
            )
            st.bar_chart(
                distribution.set_index("Sample Type"),
                y="Quantity"
            )

        with col2:
            location_distribution = (
                df["Location"].value_counts().rename_axis("Location")
                .reset_index(name="Quantity")
            )
            st.bar_chart(
                location_distribution.set_index("Location"),
                y="Quantity"
            )

        st.markdown('<div class="section-title">Recently Registered Samples</div>',
                    unsafe_allow_html=True)

        recent = df.tail(5).iloc[::-1]

        for _, row in recent.iterrows():
            display_sample(row)

    else:
        st.info("No samples registered yet. Go to Register Sample to add your first record.")

# =========================================================
# 2. SEARCH SAMPLES
# =========================================================
elif page == "Search Samples":

    st.markdown('<div class="section-title">Find Your Sample</div>',
                unsafe_allow_html=True)

    st.caption("Search using Sample ID, Lot Number or Product Name.")

    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input(
            "Search",
            placeholder="Enter Sample ID, Lot Number or Product Name..."
        )

    with col2:
        search_type = st.selectbox(
            "Sample Category",
            ["All Categories"] + SAMPLE_TYPES
        )

    if search_query or search_type != "All Categories":

        results = df.copy()

        if search_query.strip():
            query = search_query.strip()

            search_columns = ["Sample ID", "Lot Number", "Product Name"]

            mask = pd.Series(False, index=results.index)

            for column in search_columns:
                mask |= results[column].fillna("").astype(str).str.contains(
                    query, case=False, regex=False
                )

            results = results[mask]

        if search_type != "All Categories":
            results = results[
                results["Sample Type"] == search_type
            ]

        st.markdown(
            f"**Search Results: {len(results)} sample(s) found**"
        )

        if not results.empty:
            for _, row in results.iterrows():
                display_sample(row)
        else:
            st.warning(
                "No matching sample found. Please check the Sample ID or Lot Number."
            )

    else:
        st.info("Enter a Sample ID, Lot Number or Product Name to search.")

# =========================================================
# 3. REGISTER NEW SAMPLE
# =========================================================
elif page == "Register Sample":

    st.markdown('<div class="section-title">Register New Sample</div>',
                unsafe_allow_html=True)

    st.caption("Complete the required information to register a new sample.")

    with st.form("sample_registration_form", clear_on_submit=True):

        st.markdown("#### 01 — Sample Identification")

        c1, c2 = st.columns(2)

        with c1:
            sample_id = st.text_input(
                "Sample ID / Serial Number *",
                placeholder="SMP-2026-001"
            )

            lot_number = st.text_input(
                "Lot Number *",
                placeholder="LOT-2026-001"
            )

            sample_type = st.selectbox(
                "Sample Type *",
                SAMPLE_TYPES
            )

        with c2:
            product_name = st.text_input(
                "Product Name & Size",
                placeholder="Adult Underpad 60 x 90 cm"
            )

            location = st.selectbox(
                "Storage Location / Rack *",
                LOCATIONS
            )

        st.markdown("---")
        st.markdown("#### 02 — Storage Reference Image")

        image_file = st.file_uploader(
            "Upload Rack / Storage Location Image",
            type=["png", "jpg", "jpeg"]
        )

        image_path = st.text_input(
            "Or enter Image URL",
            placeholder="https://example.com/rack-a2.jpg"
        )

        if image_file:
            st.image(
                image_file,
                caption="Uploaded storage reference",
                width=300
            )

        st.markdown("---")

        submitted = st.form_submit_button(
            "💾  SAVE SAMPLE RECORD",
            use_container_width=True
        )

        if submitted:

            if not sample_id.strip() or not lot_number.strip():
                st.error("Sample ID and Lot Number are mandatory.")

            elif (
                not st.session_state.samples_db.empty
                and st.session_state.samples_db["Sample ID"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.casefold()
                    .eq(sample_id.strip().casefold())
                    .any()
            ):
                st.error("This Sample ID already exists. Please enter a unique Sample ID.")

            else:

                image_bytes = (
                    image_file.getvalue()
                    if image_file else None
                )

                new_record = {
                    "Sample ID": sample_id.strip(),
                    "Lot Number": lot_number.strip(),
                    "Sample Type": sample_type,
                    "Product Name": product_name.strip(),
                    "Location": location,
                    "Image Path": image_path.strip(),
                    "Image Data": image_bytes,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

                st.session_state.samples_db = pd.concat(
                    [
                        st.session_state.samples_db,
                        pd.DataFrame([new_record])
                    ],
                    ignore_index=True
                )

                st.success(
                    f"Sample {sample_id} successfully registered!"
                )

                st.balloons()

# =========================================================
# 4. SAMPLE DATABASE
# =========================================================
elif page == "Sample Database":

    st.markdown('<div class="section-title">Complete Sample Database</div>',
                unsafe_allow_html=True)

    if not df.empty:

        col1, col2 = st.columns([2, 1])

        with col1:
            db_filter = st.selectbox(
                "Filter by Sample Type",
                ["All Categories"] + SAMPLE_TYPES
            )

        with col2:
            st.metric("Total Records", len(df))

        view_df = df.copy()

        if db_filter != "All Categories":
            view_df = view_df[
                view_df["Sample Type"] == db_filter
            ]

        display_df = view_df.drop(
            columns=["Image Data", "Image Path"],
            errors="ignore"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = display_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Sample Database (CSV)",
            data=csv_data,
            file_name="Sample_Location_Database.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.markdown("#### View Individual Sample")

        selected_id = st.selectbox(
            "Select Sample ID",
            view_df["Sample ID"].tolist()
        )

        selected = view_df[
            view_df["Sample ID"] == selected_id
        ]

        if not selected.empty:
            display_sample(selected.iloc[0])

    else:
        st.info("The sample database is currently empty.")

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown("""
<div style="text-align:center;color:#8290A3;font-size:11px;padding:8px;">
    SAMPLE & LOCATION MANAGEMENT SYSTEM
    &nbsp; | &nbsp; QUALITY MANAGEMENT
    &nbsp; | &nbsp; VERSION 2.0
</div>
""", unsafe_allow_html=True)
