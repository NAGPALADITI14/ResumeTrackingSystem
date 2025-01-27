import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from  PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_text(uploaded_file):
    ## convert the pdf to image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title="Resume Application Tracker")
st.header("ATS TRACKING SYSTEM")
jd = st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")

# submit2 = st.button("How can I Improvise my Skills")

submit2 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of 
data science, Data analysis, Software Engineer, Full stack developer, Web developer,
Big data engineer,Frontend Developer, Backend Developer,Your task is to review
the resume based on the given job description.
please share your professional evaluation on whether the candidate's profile align with the job description
or not.Highlight the strengths and weaknesses of the applicant in relation to specified job description. """

input_prompt2="""
you are a skilled ATS(APPLICANT TRACKING SYSTEM) scanner with deep understanding of data science, Data analysis, Software Engineer, Full stack developer, Web developer,
Big data engineer,Frontend Developer, Backend Developer and ATS functionality.your task is to evaluate the resume against the rpovided job description. give me the 
percentage match for the provided job description. first the ouptut should come as percentage and the keywords missing and last final thoughts
"""


input_prompt = """You are an experienced HR with Tech Experience in the field of 
data science, Data analysis, Software Engineer, Full stack developer, Web developer,
Big data engineer,Frontend Developer, Backend Developer,Your task is to evaluate 
the resume based on the given job description. You must consider the job market is very competitive
and you should provide best assistance for improving the resumes. assign the percentage matching based 
on job description and missing keywords with high accuracy
resume: {text}
description: {jd} 
I want the response in one single string having the structure 
{{"JD Match: "%","MissingKeywords:[]","Profile Summary":""}}\\n"""


# st.title("Smart Resume Application Tracker")
# st.text("Improve your  Resume ATS")
# jd = st.text_area("Paste the Job Description")
# uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please Upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(jd,text,input_prompt)
        st.subheader("The Response is: ")
        st.write(response)

if submit1:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(jd,text,input_prompt1)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the Resume")

if submit2:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(jd,text,input_prompt2)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the Resume")
