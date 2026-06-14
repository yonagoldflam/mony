import streamlit as st
import pandas as pd

# Load data
df = pd.read_excel("מתנות_מירי_ושניאור (1).xlsx")

st.title("מתנות מירי ושניאור")

# Search box
search_text = st.text_input(
    "חיפוש לפי שם פרטי, שם משפחה או שם מלא"
)

# Tag filter
tags = ["הכל"] + sorted(df["תגית"].dropna().astype(str).unique())
selected_tag = st.selectbox("בחר תגית", tags)

filtered = df.copy()

# Filter by tag
if selected_tag != "הכל":
    filtered = filtered[
        filtered["תגית"].astype(str) == selected_tag
    ]

# Filter by name
if search_text:
    first_name = filtered["שם_פרטי"].astype(str)
    last_name = filtered["שם_משפחה"].astype(str)

    full_name = first_name + " " + last_name
    reverse_full_name = last_name + " " + first_name

    filtered = filtered[
        first_name.str.contains(search_text, case=False, na=False)
        |
        last_name.str.contains(search_text, case=False, na=False)
        |
        full_name.str.contains(search_text, case=False, na=False)
        |
        reverse_full_name.str.contains(search_text, case=False, na=False)
    ]

# Metrics
st.metric("סה״כ כסף", f"{filtered['סכום'].sum():,.0f} ₪")
st.metric("מספר אנשים", len(filtered))

# Table
st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)