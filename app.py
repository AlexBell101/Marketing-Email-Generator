import streamlit as st
from openai import OpenAI
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
def generate_marketing_email(prompt, touches, persona, marketing_asset_url, objective):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a SaaS marketing copywriter tasked with writing compelling B2B emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to generate the prompt, referencing a URL instead of a file
def create_prompt(outreach_type, persona, marketing_asset_url, num_touches):
    if outreach_type == "Post MQL Outreach":
        prompt = (f"Write a follow-up email to a {persona} after they visited {marketing_asset_url}. "
                  f"The goal of the email is to see if anything resonated with them from a sales perspective. "
                  f"Please refer to www.astronomer.io for information about our company and docs.astronomer.io for technical details. "
                  f"The email should be no more than two paragraphs. Generate {num_touches} emails in a nurturing sequence.")
    else:
        prompt = (f"Create a {outreach_type} email for the following persona: {persona}. "
                  f"Use the information from this URL: {marketing_asset_url}. "
                  f"Refer to www.astronomer.io for our company's product information and docs.astronomer.io for technical insights. "
                  f"The email should be no more than two paragraphs. "
                  f"Generate {num_touches} emails in a nurturing sequence.")
    return prompt

# Streamlit App Main
def main():
    add_custom_css()

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.title("Marketing Email Copy Generator")

    st.subheader("Provide the details for your email copy")

    # Marketing asset URL input
    marketing_asset_url = st.text_input("Provide a URL for the marketing asset (optional)", placeholder="https://example.com/asset")

    # Persona picklist (dropdown)
    personas = [
        "Data Engineer",
        "Data Engineer Mgr",
        "Database Admin"
        "IT Admin"
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
        ("Post MQL Outreach", "Promotional Email")
    )

    # Slider for number of touches
    num_touches = st.slider("Number of touches", 1, 10, 3) if outreach_type == "Post MQL Outreach" else 1

    # Generate the email sequence prompt with the URL reference
    prompt = create_prompt(outreach_type, target_persona, marketing_asset_url or "No URL provided", num_touches)

    # Button to generate email
    if st.button("Generate Email Copy"):
        with st.spinner("Generating marketing email..."):
            result = generate_marketing_email(prompt, num_touches, target_persona, marketing_asset_url, "email engagement")
            if result:
                st.subheader("Generated Marketing Email Copy")
                st.write(result)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
