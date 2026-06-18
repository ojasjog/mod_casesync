# app.py
import streamlit as st
from ss import process_screenshot_to_pdf 

st.set_page_config(page_title="CaseSync Mobile Core", layout="centered")

st.title("📱 CaseSync Mobile Parser")
st.write("Upload court details via screenshot, type your custom notes, and export.")

# 1. Capture the screenshot from the mobile device
uploaded_file = st.file_uploader("1. Upload Case Details Screenshot", type=["png", "jpg", "jpeg"])

# 2. Native interactive text block for typing custom notes
user_notes = st.text_area(
    label="2. Append Custom Case Notes / Next Action Items",
    placeholder="Type any ongoing notes, attorney instructions, or scheduling nuances here...",
    height=150
)

st.write("---")

# 3. Execution & Print Button Block
if uploaded_file is not None:
    # A distinct button to trigger compilation so it doesn't run prematurely while typing
    if st.button("🚀 Compile Document Portfolio", use_container_width=True):
        st.info("Executing OCR matrix parsing and merging custom notes...")
        
        image_bytes = uploaded_file.getvalue()
        pdf_path = "final_output.pdf"
        
        # Pass BOTH the raw screenshot data AND the text entry field data to your engine
        process_screenshot_to_pdf(image_bytes, user_notes, pdf_path)
        
        st.success("PDF Dossier compiled perfectly!")
        
        # Read file out to mobile user browser print manager
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Open & Print PDF Document",
                data=f,
                file_name="CaseSync_Structured_Brief.pdf",
                mime="application/pdf",
                use_container_width=True
            )
else:
    st.caption("⚠️ Please upload a case screenshot above to enable PDF printing options.")