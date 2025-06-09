import os
import sys
import streamlit as st
import json
import tempfile
import uuid

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import from the utils package
from utils.azure_openai_utils import AzureOpenAIService
from utils.resume_parser import parse_resume, load_sample_data

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the data/resumes directory and return the file path"""
    # Create a unique filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Get the project root directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    # Ensure the directory exists
    resumes_dir = os.path.join(root_dir, "data", "resumes")
    os.makedirs(resumes_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(resumes_dir, unique_filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def display_resume():
    """Display the current resume text in the app"""
    if st.session_state.resume_text:
        with st.expander("Resume Content", expanded=True):
            st.text_area("", value=st.session_state.resume_text, height=300, disabled=True)



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
            temp_file_path = save_uploaded_file(uploaded_file)
            resume_text = parse_resume(temp_file_path)
            st.session_state.current_resume = uploaded_file.name
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
if st.session_state.resume_text:
    display_resume()
    
    # Load sample data for analysis
    job_roles_data, trainings_data, projects_data = load_sample_data()
    
    # Initialize Azure OpenAI service
    azure_openai_service = AzureOpenAIService()
    
    # Analysis button
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume with Azure OpenAI..."):
            try:
                analysis_result = azure_openai_service.analyze_resume(
                    st.session_state.resume_text,
                    job_roles_data,
                    trainings_data,
                    projects_data
                )
                
                st.session_state.analysis_results = analysis_result
                st.success("Analysis completed successfully! Go to the Analysis Results tab to view the results.")
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")