import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Set your Gemini API key
# os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"  # Or use Streamlit secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Function to generate response using Gemini
def get_gemini_response(input_text, no_words, blog_style):
    # Initialize Gemini via LangChain
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

    # Prompt template
    template = """
    Write a blog for the {blog_style} job profile on the topic "{input_text}"
    within {no_words} words.
    """

    prompt = PromptTemplate(
        input_variables=["blog_style", "input_text", "no_words"],
        template=template
    )

    final_prompt = prompt.format(
        blog_style=blog_style, input_text=input_text, no_words=no_words
    )

    return llm.invoke(final_prompt)

# Streamlit UI
st.set_page_config(
    page_title="Generate Blogs with Gemini 🤖",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.header("Generate Blogs 🤖 (Powered by Google Gemini)")

input_text = st.text_input("Enter the Blog Topic")

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input("No. of Words")
with col2:
    blog_style = st.selectbox(
        "Writing the blog for",
        ("Researchers", "Data Scientist", "Common People"),
        index=0
    )

submit = st.button("Generate")

if submit:
    if not input_text or not no_words:
        st.warning("Please enter both the blog topic and number of words.")
    else:
        try:
            response = get_gemini_response(input_text, no_words, blog_style)
            st.subheader("Generated Blog")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")