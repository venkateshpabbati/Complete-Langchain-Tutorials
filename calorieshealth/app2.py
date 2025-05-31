import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Constants
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-1.5-flash"

def configure_genai(api_key: str):
    """
    Configure the Google Generative AI client.
    """
    if not api_key:
        st.error("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
        st.stop()
    genai.configure(api_key=api_key)

def get_gemini_response(prompt: str, image_parts: list, user_input: str) -> str:
    """
    Generate a response using Gemini's vision model.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([prompt, image_parts[0], user_input])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return ""

def prepare_image_parts(uploaded_file) -> list:
    """
    Prepare the uploaded image for the generative AI model.
    """
    if not uploaded_file:
        raise FileNotFoundError("No image file uploaded.")
    return [{
        "mime_type": uploaded_file.type,
        "data": uploaded_file.getvalue()
    }]

def main():
    st.set_page_config(page_title="Gemini Nutritionist Demo")
    st.header("Gemini Nutritionist Application")

    configure_genai(GOOGLE_API_KEY)

    user_input = st.text_input("Describe your dietary context or preferences (optional):", key="input")
    uploaded_file = st.file_uploader("Upload an image of your meal", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Meal Image", use_column_width=True)

    if st.button("Analyze Image"):
        if uploaded_file:
            try:
                image_parts = prepare_image_parts(uploaded_file)
                nutritionist_prompt = (
                    "You are an expert nutritionist. Analyze the foods visible in the image, "
                    "calculate the total calories, and provide details for each food item in the following format:\n"
                    "1. Item 1 - number of calories\n"
                    "2. Item 2 - number of calories\n"
                    "...\n"
                )
                response = get_gemini_response(nutritionist_prompt, image_parts, user_input)
                if response:
                    st.subheader("Nutrition Analysis")
                    st.write(response)
                else:
                    st.warning("No response received from Gemini. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload an image before analyzing.")

if __name__ == "__main__":
    main()
