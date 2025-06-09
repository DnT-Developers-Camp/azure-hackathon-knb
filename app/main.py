import os
import streamlit as st
import json
import pandas as pd
from utils.azure_openai_utils import AzureOpenAIService
from utils.resume_parser import parse_resume, load_sample_data
import tempfile
import uuid

# Set page configuration and title
st.set_page_config(page_title="Talent Management System", page_icon="👩‍💼", layout="wide")

# Initialize session state variables if they don't exist
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_resume' not in st.session_state:
    st.session_state.current_resume = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to the data/resumes directory and return the file path"""
    # Create a unique filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Ensure the directory exists
    os.makedirs("data/resumes", exist_ok=True)
    
    # Save the file
    file_path = os.path.join("data/resumes", unique_filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def display_resume():
    """Display the current resume text in the app"""
    if st.session_state.resume_text:
        with st.expander("Resume Content", expanded=True):
            st.text_area("", value=st.session_state.resume_text, height=300, disabled=True)

def display_analysis_results():
    """Display the analysis results in a structured format"""
    if st.session_state.analysis_results:
        try:
            # Try to parse the results as JSON
            results = json.loads(st.session_state.analysis_results)
            
            # Skills Assessment
            with st.expander("Skills Assessment", expanded=True):
                if "skills_assessment" in results:
                    st.write(results["skills_assessment"])
                    # If the skills assessment is a list, display as a table
                    if isinstance(results["skills_assessment"], list):
                        df = pd.DataFrame(results["skills_assessment"])
                        st.dataframe(df)
            
            # Skill Gaps
            with st.expander("Skill Gaps", expanded=True):
                if "skill_gaps" in results:
                    st.write(results["skill_gaps"])
            
            # Training Recommendations
            with st.expander("Training Recommendations", expanded=True):
                if "training_recommendations" in results:
                    st.write(results["training_recommendations"])
                    # If the training recommendations is a list, display as a table
                    if isinstance(results["training_recommendations"], list):
                        df = pd.DataFrame(results["training_recommendations"])
                        st.dataframe(df)
            
            # Secondment Recommendations
            with st.expander("Secondment Project Recommendations", expanded=True):
                if "secondment_recommendations" in results:
                    st.write(results["secondment_recommendations"])
                    # If the secondment recommendations is a list, display as a table
                    if isinstance(results["secondment_recommendations"], list):
                        df = pd.DataFrame(results["secondment_recommendations"])
                        st.dataframe(df)
            
            # Career Path
            with st.expander("Career Path", expanded=True):
                if "career_path" in results:
                    st.write(results["career_path"])
                    
        except json.JSONDecodeError:
            # If the results are not in JSON format, display as raw text
            st.subheader("Analysis Results")
            st.write(st.session_state.analysis_results)

def main():
    # App header
    st.title("👩‍💼 Talent Management System")
    st.markdown("### Employee Skill Gap Analysis & Career Development")
    
    # Initialize Azure OpenAI service
    azure_openai_service = AzureOpenAIService()
    
    # Load sample data for analysis
    job_roles_data, trainings_data, projects_data = load_sample_data()
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Upload Resume", "Analysis Results", "System Information"])
    
    with tab1:
        st.header("Upload Employee Resume")
        
        # File uploader
        uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"])
        
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
                    # Load sample resume
                    if sample_option == "John Doe - Software Developer":
                        sample_path = "data/sample_data/john_doe_resume.txt"
                    else:  # Sarah Johnson
                        sample_path = "data/sample_data/sarah_johnson_resume.txt"
                    
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
    
    with tab2:
        st.header("Analysis Results")
        
        if st.session_state.current_resume:
            st.subheader(f"Resume: {st.session_state.current_resume}")
            
            # Display the analysis results
            if st.session_state.analysis_results:
                display_analysis_results()
            else:
                st.info("No analysis results available. Please analyze a resume first.")
        else:
            st.info("No resume uploaded or selected. Please upload or select a resume in the Upload Resume tab.")
    
    with tab3:
        st.header("System Information")
        
        st.subheader("Sample Data")
        
        # Display sample job roles
        with st.expander("Job Roles Data"):
            st.json(job_roles_data)
        
        # Display sample training programs
        with st.expander("Training Programs Data"):
            st.json(trainings_data)
        
        # Display sample secondment projects
        with st.expander("Secondment Projects Data"):
            st.json(projects_data)
        
        st.subheader("Instructions")
        st.markdown("""
        ### How to use this system:
        
        1. Upload an employee's resume (PDF, DOCX, or TXT format) or select a sample resume
        2. Process the resume to extract the text content
        3. Click "Analyze Resume" to perform the skill gap analysis using Azure OpenAI
        4. View the analysis results in the "Analysis Results" tab
        
        ### Analysis includes:
        
        - Skills Assessment: Current skills and expertise levels
        - Skill Gaps: Missing skills for current role or career advancement
        - Training Recommendations: Suggested courses based on skill gaps
        - Secondment Project Recommendations: Potential projects for skill development
        - Career Path: Recommended next career moves within the organization
        """)

if __name__ == "__main__":
    main()
