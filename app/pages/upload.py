import os
import sys
import streamlit as st
import json
import tempfile
import uuid

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import from the utils package
from utils.azure_openai_utils import analyze_resume as analyze_resume_openai,standardize_skill_output
from utils.resume_parser import load_sample_data
from utils.azure_utils import upload_file_to_blob, extract_markdown_doc_intel

# Initialize session state variables if they don't exist
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_resume' not in st.session_state:
    st.session_state.current_resume = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
def save_uploaded_file(uploaded_file): 
# Upload to Azure Blob Storage
    upload_file_to_blob(uploaded_file.read(), uploaded_file.name)
    

    return uploaded_file.name

def display_resume():
    """Display the current resume text in the app"""
    if 'resume_text' in st.session_state and st.session_state.resume_text:        
        with st.expander("Resume Content", expanded=True):
            st.text_area("Resume Content", value=st.session_state.resume_text, height=300, disabled=True, label_visibility="collapsed")



st.header("Upload Employee Resume")

# File uploader
uploaded_file = st.file_uploader("Choose a resume file", type=["pdf"])

# Sample resume selection
st.markdown("### Or select a sample resume")
sample_option = st.selectbox(
    "Select a sample resume",
    ["None", "John Doe - Software Developer", "Sarah Johnson - Data Analyst"]
)

# Process the uploaded file or sample
process_clicked = st.button("Process Resume")

if process_clicked:
    with st.spinner("Processing resume..."):
        if uploaded_file is not None:
            # Save the uploaded file and parse it
            uploaded_file.seek(0)
            save_uploaded_file(uploaded_file)
           
            uploaded_file.seek(0)
            
            uploaded_file.seek(0)
            resume_text = extract_markdown_doc_intel(uploaded_file.read()).content
            st.session_state.current_resume = uploaded_file.name
            ## Need to process the resume text
            skills = standardize_skill_output(resume_text, type="digital technology")
            st.write(skills)
            st.session_state.resume_text = resume_text
            # Show success message
            st.success(f"Resume '{uploaded_file.name}' processed successfully!")
        elif sample_option != "None":
            # Get the project root directory
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            
            # Load sample resume
            if sample_option == "John Doe - Software Developer":
                sample_path = os.path.join(root_dir, "data", "sample_data", "john_doe_resume.txt")
            else:  # Sarah Johnson
                sample_path = os.path.join(root_dir, "data", "sample_data", "sarah_johnson_resume.txt")
            
            with open(sample_path, 'r') as file:
                resume_text = file.read()
            
            st.session_state.current_resume = sample_option
            st.session_state.resume_text = resume_text
            
            # Show success message
            st.success(f"Sample resume '{sample_option}' loaded successfully!")
        else:
            st.error("Please upload a file or select a sample resume.")

# Display the current resume
if 'resume_text' in st.session_state and st.session_state.resume_text:
    display_resume()
    
    # Load sample data for analysis
    job_roles_data, trainings_data, projects_data = load_sample_data()
      # Analysis button
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume with Azure OpenAI..."):
            analysis_result = analyze_resume_openai(
                st.session_state.resume_text,
                job_roles_data,
                trainings_data,
                projects_data
            )
            
            st.session_state.analysis_results = analysis_result
            st.success("Analysis completed successfully! Go to the Analysis Results tab to view the results.")
           