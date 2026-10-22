import streamlit as st
import os
from pipeline import extract_text_from_pdf, annotate_paper

st.set_page_config(page_title="AI Research Rigour Annotator", layout="wide")

st.title("Automated Research Rigour Annotation Pipeline")

st.subheader("Project Prototype")

uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type=["pdf"])
if uploaded_file is not None:
    # Ensure the sample directory exists
    os.makedirs("sample_papers", exist_ok=True)
    temp_path = os.path.join("sample_papers", uploaded_file.name)
    
    # Write file out locally to give it a file path for parsing
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.success(f"Successfully uploaded: {uploaded_file.name}")

    with st.spinner("Parsing text and running automated annotation logic..."):
        raw_text = extract_text_from_pdf(temp_path)
        labels = annotate_paper(raw_text)
        
    # Split UI into two logical review columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🎯 Programmatic Annotations")
        st.metric(label="Calculated Rigour Score", value=f"{labels['Rigour_Score']} / 3")
        
        st.write("**Automated Data Quality Checkmarks:**")
        st.checkbox("Open Source Code Repository Found", value=labels["Has_Public_Code"], disabled=True)
        st.checkbox("Data Availability Statement Found", value=labels["Has_Data_Statement"], disabled=True)
        st.checkbox("Institutional Ethics Documentation Found", value=labels["Has_Ethics_Clearance"], disabled=True)


    with col2:
        st.header("📄 Extracted Text Preview")
        # Display the first 1500 characters of the parsed text
        st.text_area("Raw Text Body", raw_text[:1500] + "\n...[Truncated Output]...", height=300)
        
    # Clean up the temp file after processing
    if os.path.exists(temp_path):
        os.remove(temp_path)
        