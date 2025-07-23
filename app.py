
import streamlit as st
import pandas as pd

# Load postal code reference data
@st.cache_data
def load_reference_data():
    df = pd.read_excel("postal_code_information_FULL.xlsx")
    df['Postal Code'] = df['Postal Code'].astype(str).str.strip()
    return df

postal_df = load_reference_data()

st.title("📍 Singapore Postal Code Region Finder")

# --- Manual Lookup ---
st.header("🔎 Manual Postal Code Lookup")

postal_input = st.text_input("Enter a postal code (e.g. 510301):")

if postal_input:
    postal_input = postal_input.strip()
    match = postal_df[postal_df['Postal Code'] == postal_input]
    if not match.empty:
        region = match.iloc[0]['Region']
        st.success(f"Region: {region}")
    else:
        st.error("Postal code not found in reference data.")

# --- File Upload ---
st.header("📁 Batch Lookup via Excel File")

uploaded_file = st.file_uploader("Upload an Excel file with a 'Postal Code' column", type=["xlsx"])

if uploaded_file:
    try:
        user_df = pd.read_excel(uploaded_file)
        user_df['Postal Code'] = user_df['Postal Code'].astype(str).str.strip()

        merged_df = user_df.merge(postal_df, on='Postal Code', how='left')

        st.subheader("✅ Preview of Results:")
        st.dataframe(merged_df.head())

        # Download button
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')

        st.download_button(
            label="📥 Download File with Regions",
            data=convert_df(merged_df),
            file_name="address_with_regions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")
