import os
import streamlit as st
import google.generativeai as genai


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


st.title("⚖️ LegalEase")
st.subheader("AI Powered Legal Document Generator")

st.info(
    "LegalEase generates AI-assisted legal document drafts. "
    "Always review the generated document with a qualified legal "
    "professional before official use."
)


# -----------------------------
# Gemini API Configuration
# -----------------------------

api_key = None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    st.warning(
        "Gemini API key is not configured. "
        "Add GEMINI_API_KEY to Streamlit secrets or environment variables."
    )
    st.stop()


genai.configure(api_key=api_key)


# -----------------------------
# Document Types
# -----------------------------

document_types = [
    "Rental Agreement",
    "Non-Disclosure Agreement (NDA)",
    "Offer Letter",
    "Affidavit"
]


document_type = st.selectbox(
    "Select Document Type",
    document_types
)


# -----------------------------
# User Inputs
# -----------------------------

st.subheader("Document Information")

user_name = st.text_input("Full Name")

address = st.text_area("Address")

additional_information = st.text_area(
    "Additional Information",
    placeholder="Enter any other information required for the document..."
)


# -----------------------------
# Generate Document
# -----------------------------

if st.button("Generate Legal Document", type="primary"):

    if not user_name.strip():
        st.error("Please enter your full name.")
        st.stop()

    if not additional_information.strip():
        st.error("Please enter the required document information.")
        st.stop()

    prompt = f"""
You are a legal document drafting assistant.

Create a professional and clearly structured draft for the following
document type:

Document Type:
{document_type}

User Name:
{user_name}

Address:
{address}

Additional Information:
{additional_information}

Requirements:

1. Create a clear document title.
2. Use appropriate sections.
3. Include relevant clauses.
4. Use professional and formal language.
5. Do not invent personal information.
6. Use placeholders where information is missing.
7. Format the document clearly.
8. Include a signature section where appropriate.
9. Add a short note that the document should be reviewed by a
   qualified legal professional.

This is a document draft and not legal advice.
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        generated_text = response.text

        st.success("Document generated successfully!")

        st.subheader("Generated Legal Document")

        st.text_area(
            "Document",
            generated_text,
            height=500
        )

        st.download_button(
            label="Download Document",
            data=generated_text,
            file_name="LegalEase_Document.txt",
            mime="text/plain"
        )

    except Exception as error:
        st.error(
            "Unable to generate the document. "
            "Please check your Gemini API configuration and try again."
        )

        st.caption(f"Error: {error}")


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "LegalEase is an AI-assisted document drafting tool and does not "
    "provide professional legal advice."
)
