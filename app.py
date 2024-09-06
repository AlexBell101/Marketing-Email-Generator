import streamlit as st
from openai import OpenAI
import PyPDF2
from openai import OpenAIError  # Correct import for OpenAIError
import os  # For loading environment variables

import streamlit as st

# Set the page configuration to a wide layout and add a title
st.set_page_config(page_title="Marketing Email Generator", layout="wide")

# Custom CSS for styling the app
def add_custom_css():
    st.markdown(
        """
        <style>
            /* Background style */
            body {
                background: linear-gradient(135deg, #f8f9fa 30%, #e9ecef 100%);
                font-family: 'Inter', sans-serif;
            }
            /* Heading style */
            h1 {
                text-align: center;
                font-size: 3rem;
                color: #0d6efd;
                padding-top: 1rem;
                margin-bottom: 2rem;
            }
            /* Button styles */
            .stButton button {
                background-color: #0d6efd !important;
                color: white !important;
                font-size: 1.2rem !important;
                padding: 0.75rem 1.5rem !important;
                border-radius: 0.5rem !important;
                border: none !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            }
            .stButton button:hover {
                background-color: #0056b3 !important;
                transform: translateY(-2px);
            }
            /* Text input and Text area styling */
            .stTextInput > div > input, .stTextArea textarea {
                padding: 1rem !important;
                border: 1px solid #ced4da !important;
                border-radius: 0.5rem !important;
                background-color: #f8f9fa !important;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            }
            /* Form section card styling */
            .st-form-section {
                padding: 2rem;
                background: white;
                border-radius: 1rem;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
            }
            /* Footer styling */
            footer {
                text-align: center;
                padding: 1rem;
                font-size: 0.9rem;
                color: #6c757d;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Inject the custom CSS
add_custom_css()



# Configure OpenAI API key via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure OpenAI API key via Streamlit secrets

# Function to call OpenAI ChatCompletion API
def generate_marketing_email(prompt, touches, persona, marketing_asset, objective):
    try:
        # Use the ChatCompletion method, not the older Completion method
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a marketing copywriter tasked with writing compelling B2B emails."},
            {"role": "user", "content": f"Write an email to a {persona} based on this asset: {marketing_asset}. The goal of the email is to {objective}."}
        ],
        max_tokens=300,
        temperature=0.7)
        return response.choices[0].message.content  # Extract the generated email content
    except OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to process uploaded files
def process_uploaded_file(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        st.error("Unsupported file type")
        return None

# Streamlit App
def main():
    st.title("Marketing Email Copy Generator")

    # Input fields
    st.subheader("Provide the details for your email copy")

    marketing_asset = st.file_uploader("Upload a Marketing Asset", type=['pdf'])
    marketing_asset_text = None
    if marketing_asset is not None:
        marketing_asset_text = process_uploaded_file(marketing_asset)
        if marketing_asset_text:
            st.write("File uploaded and processed successfully.")

    target_persona = st.text_area("Target Persona")

    outreach_type = st.selectbox(
        "Select Outreach Type",
        ("Post MQL Outreach", "Nurturing Email")
    )

    num_touches = st.slider("Number of touches", 1, 10, 3) if outreach_type == "Post MQL Outreach" else 1

    # Prompt generation
    st.subheader("Generated Prompt Preview")
    prompt = f"Create a {outreach_type} for the following target persona:\n{target_persona}\nUsing the marketing asset:\n{marketing_asset_text}."

    st.text_area("Prompt to be sent to ChatGPT", prompt, height=150)

    # Button to submit the inputs to ChatGPT
    if st.button("Generate Email Copy"):
        with st.spinner("Generating marketing email..."):
            result = generate_marketing_email(prompt, num_touches, target_persona, marketing_asset_text, "email engagement")
            if result:
                st.subheader("Generated Marketing Email Copy")
                st.write(result)

if __name__ == '__main__':
    main()
