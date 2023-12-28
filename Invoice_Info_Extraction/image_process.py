#from pdf_converter import full_image
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_path,convert_from_bytes
from PIL import Image
from io import BytesIO
# take environment variables from .env.
load_dotenv()  
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# generate response
def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text

#convert pdf to image

def pdf_to_single_image(pdf):
    images = convert_from_bytes(pdf_file=pdf)
    width, height = images[0].size
    combined_image = Image.new("RGB", (width, height * len(images)))
    for i, image in enumerate(images):
        combined_image.paste(image, (0, i * height))
    image = combined_image
    return image


# extract image information
def input_image_setup(image):
    # Check if an image has been provided
    if image is not None:
    # Convert the image to bytes
        image_bytes_io = BytesIO()
        image.save(image_bytes_io, format='PNG')
        image_bytes_data = image_bytes_io.getvalue()

        # Get the MIME type
        mime_type = "image/png"  # Change as needed based on the actual image format
        image_parts = [
            {
                "mime_type": mime_type,  # Get the mime type of the uploaded file
                "data": image_bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
    
st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Vision Pro Invoice Info Extraction Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
image=""   
if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    get_image = pdf_to_single_image(pdf_bytes)
    st.image(get_image, caption="PDF Converted to Single Image.", use_column_width=True)


submit=st.button("Generate Answer")


input_prompt = """
               You are an expert in understanding invoices & extracting information from invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(get_image)
    #print(image_data[0])
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("Respone:")
    st.write(response)