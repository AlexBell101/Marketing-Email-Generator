import streamlit as st
from openai import OpenAI
import PyPDF2
from openai import OpenAIError
import os

# Configure OpenAI API key via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom CSS injection for modern design
def add_custom_css():
    st.markdown("""
        <style>
            /* Background and body styling */
            body {
                background: linear-gradient(135deg, #f0f9ff, #ffffff);
                font-family: 'Inter', sans-serif;
            }

            /* Main container style */
            .main-container {
                padding: 2rem;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
                margin: 2rem auto;
                max-width: 800px;
            }

            /* Headings */
            h1 {
                font-size: 2.5rem;
                font-weight: 600;
                text-align: center;
                color: #007bff;
                margin-bottom: 2rem;
            }

            h2, h3 {
                color: #333;
                font-size: 1.5rem;
                margin-bottom: 1rem;
                font-weight: 500;
            }

            /* Sub-heading for prompt preview */
            .stTextArea label {
                font-size: 1.2rem;
                font-weight: 500;
                margin-bottom: 1rem;
                color: #007bff;
            }

            /* Input fields */
            .stTextInput > div > input, .stTextArea textarea {
                padding: 1rem;
                border-radius: 10px;
                background-color: #f7f9fc;
                border: 1px solid #e3e4e8;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                font-size: 1rem;
            }

            /* File uploader */
            .stFileUploader label {
                font-size: 1.2rem;
                font-weight: 500;
                color: #007bff;
            }

            /* Slider styling */
            .stSlider > div {
                padding: 1rem 0;
                font-size: 1.2rem;
            }

            /* Button styles */
            .stButton button {
                background-color: #007bff;
                color: white;
                font-size: 1.2rem;
                padding: 0.75rem 1.5rem;
                border-radius: 10px;
                border: none;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                cursor: pointer;
                transition: transform 0.2s ease;
            }

            .stButton button:hover {
                background-color: #0056b3;
                transform: translateY(-3px);
            }

            /* Success message */
            .stAlert {
                background-color: #e3f7ed;
                border: 1px solid #d4edda;
                color: #155724;
                padding: 1rem;
                border-radius: 8px;
            }
            
            /* Error message styling */
            .stAlert .error {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
                border-radius: 8px;
                padding: 1rem;
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

# Function to call OpenAI API
def generate_marketing_email(prompt, touches, persona, marketing_asset, objective):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a marketing copywriter tasked with writing compelling B2B emails."},
                {"role": "user", "content": f"Write an email to a {persona} based on this asset: {marketing_asset}. The goal of the email is to {objective}."}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to process uploaded file
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

# Streamlit App Main
def main():
    add_custom_css()

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.title("Marketing Email Copy Generator")

    st.subheader("Provide the details for your email copy")

    # Marketing asset file upload
    marketing_asset = st.file_uploader("Upload a Marketing Asset (PDF)", type=['pdf'])
    marketing_asset_text = None
    if marketing_asset is not None:
        marketing_asset_text = process_uploaded_file(marketing_asset)
        if marketing_asset_text:
            st.success("File uploaded and processed successfully.")

    # Target persona
    target_persona = st.text_area("Target Persona", placeholder="Describe your target audience")

    # Outreach type select box
    outreach_type = st.selectbox(
        "Select Outreach Type",
        ("Post MQL Outreach", "Nurturing Email")
    )

    # Slider for number of touches
    num_touches = st.slider("Number of touches", 1, 10, 3) if outreach_type == "Post MQL Outreach" else 1

    # Prompt preview
    st.subheader("Generated Prompt Preview")
    prompt = f"Create a {outreach_type} for the following target persona:\n{target_persona}\nUsing the marketing asset:\n{marketing_asset_text or 'No asset uploaded'}."

    st.text_area("Prompt to be sent to ChatGPT", prompt, height=150)

    # Button to generate email
    if st.button("Generate Email Copy"):
        with st.spinner("Generating marketing email..."):
            result = generate_marketing_email(prompt, num_touches, target_persona, marketing_asset_text, "email engagement")
            if result:
                st.subheader("Generated Marketing Email Copy")
                st.write(result)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
