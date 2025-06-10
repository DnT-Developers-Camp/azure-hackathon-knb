import os
import sys
import streamlit as st
import json
import pandas as pd
import tempfile
import uuid

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import from the utils package and pages
from utils.resume_parser import  load_sample_data

# Set page configuration and title
st.set_page_config(page_title="Talent Management System", page_icon="👩‍💼", layout="wide")

# Initialize session state variables if they don't exist
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_resume' not in st.session_state:
    st.session_state.current_resume = None
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None



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

    # Load sample data for analysis
    job_roles_data, trainings_data, projects_data = load_sample_data()
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Tab1", "Analysis Results", "System Information"])
    with tab1:
        st.header("placeholder")
    
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
