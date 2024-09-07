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
            /* Custom styles omitted for brevity */
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to call OpenAI API
def generate_marketing_email(prompt, touches, persona, marketing_asset, objective):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a marketing copywriter tasked with writing compelling B2B emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to generate the prompt
def create_prompt(outreach_type, persona, marketing_asset, num_touches):
    if outreach_type == "Post MQL Outreach":
        prompt = (f"Write a follow-up email to a {persona} after they have read the marketing asset: {marketing_asset}. "
                  f"The goal of the email is to see if anything resonated with them from a sales perspective. "
                  f"Please refer to www.astronomer.io for information about our company and docs.astronomer.io for technical details. "
                  f"The email should be no more than two paragraphs. Generate {num_touches} emails in a nurturing sequence.")
    else:
        prompt = (f"Create a {outreach_type} email for the following persona: {persona}. "
                  f"Use the marketing asset: {marketing_asset}. "
                  f"Refer to www.astronomer.io for our company's product information and docs.astronomer.io for technical insights. "
                  f"The email should be no more than two paragraphs. "
                  f"Generate {num_touches} emails in a nurturing sequence.")
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

    # Persona picklist (dropdown)
    personas = [
        "Data Engineer",
        "Data Engineer Mgr",
        "ML/AI Engineer",
        "ML/AI Engineer Mgr",
        "VP/CTO",
        "VP/CXO",
        "Analyst/Scientist"
    ]
    target_persona = st.selectbox("Select Target Persona", options=personas)

    # Outreach type select box
    outreach_type = st.selectbox(
        "Select Outreach Type",
        ("Post MQL Outreach", "Nurturing Email")
    )

    # Slider for number of touches
    num_touches = st.slider("Number of touches", 1, 10, 3) if outreach_type == "Post MQL Outreach" else 1

    # Generate the email sequence prompt
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
