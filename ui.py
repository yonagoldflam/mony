import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# =========================
# Google Sheets Setup
# =========================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "124tWLvgYhS8ONG9p_7Y_pjNHLL1IdnDUJYMUqq7Tmhk"

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# =========================
# Load Data
# =========================

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("מתנות מירי ושניאור")

# =========================
# Search
# =========================

search_text = st.text_input(
    "חיפוש לפי שם פרטי, שם משפחה או שם מלא"
)

# =========================
# Tag Filter
# =========================

existing_tags = sorted(df["תגית"].dropna().astype(str).unique())

tags = ["הכל"] + existing_tags

selected_tag = st.selectbox("בחר תגית", tags)

filtered = df.copy()

# Filter by tag
if selected_tag != "הכל":
    filtered = filtered[
        filtered["תגית"].astype(str) == selected_tag
    ]

# =========================
# SMART SEARCH (AND by words)
# =========================

if search_text:
    words = search_text.strip().split()

    for word in words:
        filtered = filtered[
            filtered["שם_פרטי"].astype(str).str.contains(word, case=False, na=False)
            |
            filtered["שם_משפחה"].astype(str).str.contains(word, case=False, na=False)
        ]

# =========================
# Metrics
# =========================

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "סה״כ כסף",
        f"{filtered['סכום'].sum():,.0f} ₪"
    )

with col2:
    st.metric(
        "מספר אנשים",
        len(filtered)
    )

# =========================
# Table
# =========================

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# =========================
# ADD NEW GIFT (BOTTOM)
# =========================

st.divider()
st.subheader("➕ הוספת מתנה חדשה")

with st.form("add_gift_form"):
    new_first_name = st.text_input("שם פרטי")
    new_last_name = st.text_input("שם משפחה")

    new_amount = st.number_input(
        "סכום",
        min_value=0,
        step=10
    )

    new_tag = st.selectbox(
        "תגית",
        existing_tags if existing_tags else ["כללי"]
    )

    submitted = st.form_submit_button("הוסף")

    if submitted:
        sheet.append_row([
            new_first_name,
            new_last_name,
            int(new_amount),
            new_tag
        ])

        st.success("המתנה נוספה בהצלחה 🎉")
        st.rerun()