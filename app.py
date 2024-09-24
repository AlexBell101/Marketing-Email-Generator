import streamlit as st
from openai import OpenAI
from openai import OpenAIError
import os

# Configure OpenAI API key via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Inject custom CSS to load Roboto font and apply globally
def add_custom_css():
    st.markdown(
        """
        <style>
            /* Import Roboto font from Google */
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

            /* Apply Roboto font to the whole app */
            html, body, [class*="css"]  {
                font-family: 'Roboto', sans-serif;
            }
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

# Function to generate the prompt with both URL/Description and company domain
def create_prompt(outreach_type, persona, marketing_asset_or_description, num_touches, company_domain):
    if company_domain:
        domain_text = f"Refer to {company_domain} for more information about the company."
    else:
        domain_text = ""

    if outreach_type == "Post MQL Outreach":
        prompt = (f"Write a follow-up email to a {persona} after they engaged with {marketing_asset_or_description}. "
                  f"The goal of the email is to see if anything resonated with them from a sales perspective. "
                  f"{domain_text} The email should be no more than two paragraphs. Generate {num_touches} emails in a nurturing sequence.")
    else:
        prompt = (f"Create a {outreach_type} email for the following persona: {persona}. "
                  f"Use the information from this {marketing_asset_or_description}. "
                  f"{domain_text} The email should be no more than two paragraphs. "
                  f"Generate {num_touches} emails in a nurturing sequence.")
    return prompt

# Streamlit App Main
def main():
    add_custom_css()

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.title("Marketing Email Copy Generator")

    st.subheader("Provide the details for your email copy")

    # Company Domain input (optional)
    company_domain = st.text_input("Enter your company domain (optional)", placeholder="e.g., www.example.com")

    # Marketing asset or description input
    marketing_asset_or_description = st.text_input("Provide an asset URL, landing page link or a description of the promotion/call to action", placeholder="Enter URL or description")

    # Free text input for persona
    target_persona = st.text_input("Enter Target Persona", placeholder="e.g., Data Engineer, Marketing Manager")

    # Outreach type select box
    outreach_type = st.selectbox(
        "Select Outreach Type",
        ("Post MQL Outreach", "Promotional Email")
    )

    # Slider for number of touches
    num_touches = st.slider("Number of touches", 1, 10, 3) if outreach_type == "Post MQL Outreach" else 1

    # Generate the email sequence prompt
    prompt = create_prompt(outreach_type, target_persona, marketing_asset_or_description or "No URL/Description provided", num_touches, company_domain)

    # Button to generate email
    if st.button("Generate Email Copy"):
        with st.spinner("Generating marketing email..."):
            result = generate_marketing_email(prompt, num_touches, target_persona, marketing_asset_or_description, "email engagement")
            if result:
                st.subheader("Generated Marketing Email Copy")
                st.write(result)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
