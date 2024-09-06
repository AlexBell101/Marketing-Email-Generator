import streamlit as st
from openai import OpenAI
import PyPDF2
from openai import OpenAIError
import os

# Configure OpenAI API key via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inject custom CSS with the background image
def add_custom_css():
    st.markdown(
        """
        <style>
            /* Set background image */
            body {
                background-image: url('https://i.ibb.co/72VZc2K/dark-blue-technology-background-free-vector-1.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                font-family: 'Inter', sans-serif;
            }

            /* Main content container to ensure readability over the background */
            .main-container {
                padding: 2rem;
                background-color: rgba(255, 255, 255, 0.85); /* Semi-transparent white background */
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
                margin: 2rem auto;
                max-width: 800px;
                color: #333; /* Text color */
            }

            /* Headings */
            h1 {
                font-size: 2.5rem;
                font-weight: 600;
                text-align: center;
                color: #007bff;
                margin-bottom: 2rem;
            }

            /* Fix text input and textarea text color */
            .stTextInput > div > input, .stTextArea textarea {
                padding: 1rem;
                border-radius: 10px;
                background-color: #f7f9fc;
                border: 1px solid #e3e4e8;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                font-size: 1rem;
                color: #333; /* Set input text color to dark gray */
            }

            /* Placeholder text color */
            .stTextInput > div > input::placeholder, .stTextArea textarea::placeholder {
                color: #adb5bd;
            }

            /* Buttons */
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

            /* Success and error messages */
            .stAlert {
                background-color: #e3f7ed;
                border: 1px solid #d4edda;
                color: #155724;
                padding: 1rem;
                border-radius: 8px;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

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

# Updated prompt generation logic
def create_prompt(outreach_type, persona, marketing_asset, num_touches):
    if outreach_type == "Post MQL Outreach":
        # Post MQL outreach email logic
        prompt = (f"Write a follow-up email to a {persona} after they have read the marketing asset: {marketing_asset}. "
                  f"The goal of the email is to see if anything resonated with them from a sales perspective. "
                  f"The email should be no more than two paragraphs. Generate {num_touches} emails in a nurturing sequence.")
    else:
        # General nurturing email logic
        prompt = (f"Create a {outreach_type} email for the following persona: {persona}. "
                  f"Use the marketing asset: {marketing_asset}. "
                  f"Generate {num_touches} emails in a nurturing sequence.")
                  f"The email should be no more than two paragraphs. Generate {num_touches} emails in a nurturing sequence.")
    return prompt

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

    # Generate the email sequence prompt without showing it
    prompt = create_prompt(outreach_type, target_persona, marketing_asset_text or "No asset uploaded", num_touches)

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
