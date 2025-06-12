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

def main():
    # Set page configuration and title
    st.set_page_config(page_title="TalentLens", page_icon="👩‍💼", layout="wide")

    # Initialize session state variables if they don't exist
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'current_resume' not in st.session_state:
        st.session_state.current_resume = None
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None


    # Load sample data for analysis
    job_roles_data, trainings_data, projects_data = load_sample_data()
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("app/Poster.png", use_container_width=False)


if __name__ == "__main__":
    main()
