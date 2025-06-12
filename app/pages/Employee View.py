import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import json 
import os 

from utils.training_plan import get_employee_skill_gaps, prepare_lt_st_training_plan

st.set_page_config(layout = "wide")

def load_json_data():
    # Get the base directory
    base_dir = Path(__file__).parent.parent.parent
    
    # Load employees data
    employees_path = os.path.join(base_dir, 'data', 'sample_data', 'employees.json')
    with open(employees_path, 'r') as f:
        employees_data = json.load(f)

    return employees_data[0]
    

employee_data = load_json_data()
# Hardcoded employee information
employee_name = employee_data['name']
employee_role = employee_data['role']
job_description = employee_data['job_desc']

st.markdown(f"<h1 class='main-header'>Welcome, {employee_name}! 👋</h1>", unsafe_allow_html=True)

# Create a container for the button
button_container = st.empty()
submit = button_container.button("Analyze My Profile")

if submit:
    # Show loading spinner while processing
    with st.spinner('Analyzing your profile...'):
        # Get analysis results
        output = get_employee_skill_gaps(employee_data, employee_data['skills'])
        training_output = prepare_lt_st_training_plan(output['short_term_gaps'], output['long_term_gaps'])
        
        # Clear the button after processing is complete
        button_container.empty()
        
        def process_skills(skills_list):
            """Process skills list into technical and soft skills dictionaries"""
            technical_skills = {}
            soft_skills = {}
            
            for skill in skills_list:
                skill_name = skill['skill_name']
                rating = skill['rating']
                skill_type = skill['type']
                
                if skill_type == 'technical':
                    technical_skills[skill_name] = {"rating": rating}
                else:
                    soft_skills[skill_name] = {"rating": rating}
                    
            return technical_skills, soft_skills

        skill_list = [
        {'skill_name': 'Python', 'rating': 4, 'type': 'technical'},
        {'skill_name': 'Java Script Framework (VUE)', 'rating': 3, 'type': 'technical'},
        {'skill_name': 'Structured Thinking and Presentation', 'rating': 3, 'type': 'soft'},
        {'skill_name': 'Stakeholder Management', 'rating': 2, 'type': 'soft'}]

        technical_skills, soft_skills = process_skills(skill_list)




        tab1, tab2 = st.tabs(["Current Role & Skills", "Skill Analysis & Training"])


        st.markdown("""
            <style>
            .main-header {
                font-size: 2.5rem;
                color: #1E88E5;
                padding-bottom: 20px;
            }
            .section-header {
                font-size: 28px;
                font-weight: bold;
                color: #000000;
                border-bottom: 2px solid #bdbdbd;
                padding: 4;                /* Remove all padding */
                margin: 0 0 12px 0;        /* Keep only bottom margin */
                line-height: 1.5;          /* Reduce line height further */
                padding-bottom: 0.2px;
                display: inline-block;
            }
            }
            .skill-container {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            }
            .vertical-divider {
                border-left: 2px solid #e0e0e0;
                margin: 0 20px;
            }
            .job-description {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True)

        # Title section with styled welcome message


        # ...existing tab definition...

        with tab1:
            # Role and Job Description section
            st.markdown("<div class='section-header'>Current Role & Job Description</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='job-description'>
                <h3 style='color: #1976D2;'>{employee_role}</h3>
                <p style='font-size: 1.1em;'>{job_description}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Skills section
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("<div class='section-header'>Technical Skills</div>", unsafe_allow_html=True)
                skills_html = "".join([
                    f"""
                    <div class='skill-item'>
                        <strong style='color: #1976D2;'>{skill}</strong><br>
                        {"⭐" * info["rating"] + "☆" * (5 - info["rating"])}
                    </div>
                    """ for skill, info in technical_skills.items()
                ])
                st.markdown(f"""
                    <div class='skill-container'>
                        {skills_html}
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='section-header'>Soft Skills</div>", unsafe_allow_html=True)
                skills_html = "".join([
                    f"""
                    <div class='skill-item'>
                        <strong style='color: #1976D2;'>{skill}</strong><br>
                        {"⭐" * info["rating"] + "☆" * (5 - info["rating"])}
                    </div>
                    """ for skill, info in soft_skills.items()
                ])
                st.markdown(f"""
                    <div class='skill-container'>
                        {skills_html}
                    </div>
                """, unsafe_allow_html=True)
            
            # Radar Chart section
            st.markdown("<div class='section-header'>Skills Overview</div>", unsafe_allow_html=True)
            
                # Create a dataframe for better visualization

            all_skills = {}
            for skill_info in output['skills_data']['skills']:
                skill_name = skill_info["skill_name"]
                rating = skill_info["rating"]
                all_skills[f"{skill_name}"] = rating


            # Update radar chart styling
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=list(all_skills.values()),
                theta=list(all_skills.keys()),
                fill='toself',
                name='Skills Profile',
                line=dict(color='#1976D2'),
                fillcolor='rgba(25, 118, 210, 0.3)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5],
                        tickfont=dict(size=20),
                        gridcolor='#e0e0e0'
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=20)
                    ),
                    bgcolor='#f8f9fa'
                ),
                font = dict(size =50),
                showlegend=False,
                height=375,
                margin=dict(t=30, b=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with tab2:

            st.markdown("""
            <style>
            .skill-container {
                padding: 5px;
                min-height: 150px; /* adjust based on expected content */
                background-color: #f8f9fa;
                border-radius: 6px;
            }
            .skill-item {
                margin-bottom: 12px;
                font-size: 16px;
            }
            .section-header {
                font-size: 20px;
                margin-bottom: 12px;
                color: #1976D2;
            }
            </style>
            """, unsafe_allow_html=True)
            

            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("<div class='section-header'>Short Term Gap</div>", unsafe_allow_html=True)
                skills_html = "".join([
                    f"""
                    <div class='skill-item'>
                        <strong style='color: #1976D2;font-size: 16px'>{i+1}. {skill}</strong>
                    </div>
                    """ for i,skill in enumerate(output['short_term_gaps'])  # replace with your actual list
                ])
                st.markdown(f"""
                    <div class='skill-container'>
                        {skills_html}
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='section-header'>Long Term Gap</div>", unsafe_allow_html=True)
                skills_html = "".join([
                    f"""
                    <div class='skill-item'>
                        <strong style='color: #1976D2; font-size: 16px'>{i+1}. {skill}</strong>
                    </div>
                    """ for i, skill in enumerate(output['long_term_gaps'])  # replace with your actual list
                ])
                st.markdown(f"""
                    <div class='skill-container'>
                        {skills_html}
                    </div>
                """, unsafe_allow_html=True)


            # st.markdown("<div class='section-header'>Training Plan</div>", unsafe_allow_html=True) 


            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("<div class='section-header'>Short Term Training</div>", unsafe_allow_html=True)
                skills_html = "".join([
                    f"""
                    <div class='skill-item'>
                        <strong style='color: #1976D2; font-size: 16px'>{i+1}. {training['skill']}</strong><br>
                        Course: {training['course_name']}<br>
                        Duration: {training['duration_days']} days<br>
                        Cost: {training['cost']}<br>
                        Description: {training['description']}
                    </div>
                    """ for i, training in enumerate(training_output['short_term_training'])
                ])
                st.markdown(f"""
                    <div class='skill-container'>
                        {skills_html}
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='section-header'>Long Term Training</div>", unsafe_allow_html=True)
                skills_html = "".join([
                    f"""
                    <div class='skill-item'>
                        <strong style='color: #1976D2; font-size: 16px'>{i+1}. {training['skill']}</strong><br>
                        Course: {training['course_name']}<br>
                        Duration: {training['duration_weeks']} weeks<br>
                        Cost: {training['cost']}<br>
                        Description: {training['description']}
                    </div>
                    """ for i, training in enumerate(training_output['long_term_training'])
                ])
                st.markdown(f"""
                    <div class='skill-container'>
                        {skills_html}
                    </div>
                """, unsafe_allow_html=True)

