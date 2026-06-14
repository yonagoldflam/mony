import streamlit as st
import pandas as pd

df = pd.read_excel("מתנות_מירי_ושניאור (1).xlsx")

tags = ["הכל"] + sorted(df["תגית"].dropna().astype(str).unique())

selected_tag = st.selectbox("בחר תגית", tags)

if selected_tag != "הכל":
    filtered = df[df["תגית"].astype(str) == selected_tag]
else:
    filtered = df

st.metric("סה״כ כסף", f"{filtered['סכום'].sum():,} ₪")
st.metric("מספר אנשים", len(filtered))

st.dataframe(filtered)