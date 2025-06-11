import os
import sys
import streamlit as st
import json
import tempfile
import uuid
import pandas as pd

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import from the utils package
from utils.azure_openai_utils import analyze_resume as analyze_resume_openai,standardize_skill_output,extract_employee_name
from utils.resume_parser import load_sample_data
from utils.azure_utils import upload_file_to_blob, extract_markdown_doc_intel, get_container, add_item
from datetime import datetime

# Initialize session state variables if they don't exist
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_resume' not in st.session_state:
    st.session_state.current_resume = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'skills' not in st.session_state:
    st.session_state.skills = None
if 'employee_name' not in st.session_state:
    st.session_state.employee_name = None

def save_uploaded_file(uploaded_file): 
# Upload to Azure Blob Storage
    upload_file_to_blob(uploaded_file.read(), uploaded_file.name)
    

    return uploaded_file.name

def display_resume():
    """Display the current resume text in the app"""
    if 'resume_text' in st.session_state and st.session_state.resume_text:        
        with st.expander("Resume Content", expanded=True):
            st.text_area("Resume Content", value=st.session_state.resume_text, height=300, disabled=True, label_visibility="collapsed")

st.title('Upload New Employee Resume')

# File uploader
uploaded_file = st.file_uploader("Choose a resume file", type=["pdf"])

st.markdown("### Enter more details")
division_option = st.selectbox(
    "Select Division",
    ["Investment", "Digital Technology"],
    index=1  # Default to Digital Technology
)

# Load job roles from resume_parser
job_roles, _, _ = load_sample_data()
role_titles = [role["title"] for role in job_roles]
role_desc_map = {role["title"]: role["job_description"] for role in job_roles}

st.markdown("#### Current Job Role and Description")
job_role = st.selectbox(
    "Select Current Job Role",
    role_titles,
    key="job_role_select"
)

job_description = st.text_area(
    "Edit the job description here",
    value=role_desc_map.get(job_role, ""),
    height=200,
    key="job_description"
)


st.markdown("#### Future Job Role and Description")
future_job_role = st.selectbox(
    "Select Future Job Role",
    role_titles,
    key="future_job_role_select"
)

future_job_description = st.text_area(
    "Edit the future job description here",
    value=role_desc_map.get(future_job_role, ""),
    height=200,
    key="future_job_description"
)

# Date picker for "Date Joined"
date_joined = st.date_input(
    "Select Date Joined",
    key="date_joined"
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
            resume_text = extract_markdown_doc_intel(uploaded_file.read()).content
            st.session_state.current_resume = uploaded_file.name
            ## Need to process the resume text
            st.session_state.skills = standardize_skill_output(resume_text, type="Digital Technology")
            st.session_state.employee_name  = extract_employee_name(resume_text)
            st.session_state.resume_text = resume_text

            if division_option == "Investment":
                # Set the manager for Investment division
                manager = "Adrian Tan"
            else:
                manager = "Aisyah Rahman"

            payload = {
                "employee_name": st.session_state.employee_name,
                "id": str(uuid.uuid4()),  # Generate a unique ID for the employee
                "role": job_role,
                "job_desc": job_description,
                "manager": manager,
                "division": division_option,
                "date_joined": date_joined.strftime("%Y-%m-%d"),
                "skills": st.session_state.skills,
                "date_updated": datetime.today().strftime("%Y-%m-%d"),
                "future_role": future_job_role,
                "future_job_desc": future_job_description,
                "pdf_name": uploaded_file.name
            }

            cosmos_container = get_container()
            # Upload the resume data to Azure Cosmos DB

            add_item(cosmos_container, payload)

            # Show success message
            st.success(f"Resume '{uploaded_file.name}' processed successfully!")
    
            # Get the project root directory
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
 
            st.session_state.resume_text = resume_text
        
        else:
            st.error("Please upload a file or select a sample resume.")

# Display the current resume
if 'resume_text' in st.session_state and st.session_state.resume_text:
    display_resume()
    df = pd.DataFrame(st.session_state.skills["skills"])
    st.write(df)

