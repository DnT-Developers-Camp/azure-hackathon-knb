import streamlit as st
import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import importlib
from utils import skill_gap_engine as _sge
importlib.reload(_sge)
from utils.skill_gap_engine import get_employee_skill_gaps
import plotly.express as px

# Load JSON data
def load_json_data():
    # Get the base directory
    base_dir = Path(__file__).parent.parent.parent
    
    # Load employees data
    employees_path = os.path.join(base_dir, 'data', 'sample_data', 'employees.json')
    with open(employees_path, 'r') as f:
        employees_data = json.load(f)
    
    # Load managers data
    managers_path = os.path.join(base_dir, 'data', 'sample_data', 'managers.json')
    with open(managers_path, 'r') as f:
        managers_data = json.load(f)
    
    return employees_data, managers_data

# Convert to pandas DataFrames
def create_dataframes(employees_data, managers_data):
    # Create employees DataFrame
    employees_df = pd.DataFrame(employees_data)
    
    # Extract skills into separate columns
    skill_dfs = []
    for i, employee in enumerate(employees_data):
        for skill in employee['skills']:
            skill_df = pd.DataFrame({
                'employee_id': employee['id'],
                'skill_name': skill['skill_name'],
                'rating': skill['rating'],
                'type': skill['type']
            }, index=[i])
            skill_dfs.append(skill_df)
    
    skills_df = pd.concat(skill_dfs, ignore_index=True) if skill_dfs else pd.DataFrame()
    
    # Create managers DataFrame
    managers_df = pd.DataFrame(managers_data)
    
    return employees_df, skills_df, managers_df

# Create manager to employee lookup dictionary
def create_manager_employee_lookup(managers_data):
    manager_employee_lookup = {}
    for manager in managers_data:
        manager_employee_lookup[manager['id']] = manager['direct_reports']
    return manager_employee_lookup

# Load data and create structures
employees_data, managers_data = load_json_data()
employees_df, skills_df, managers_df = create_dataframes(employees_data, managers_data)
manager_employee_lookup = create_manager_employee_lookup(managers_data)

# Main app
st.set_page_config(page_title='Manager View', layout='wide')
st.title('Manager View')

# Create tabs
tabs = st.tabs([
    'Team Snapshot',
    'Employee Drill Down',
    'Secondment/Project Matching'
])

with tabs[0]:
    st.header('Team Snapshot')
    
    # Select manager
    manager_options = managers_df['name'].tolist()
    selected_manager = st.selectbox('Select Manager', manager_options)
    
    # Get manager details
    manager_row = managers_df[managers_df['name'] == selected_manager].iloc[0]
    manager_id = manager_row['id']
    
    # Get employees for the selected manager
    employee_ids = manager_employee_lookup[manager_id]
    team_df = employees_df[employees_df['id'].isin(employee_ids)]
    
    # Display team information
    st.subheader(f'Team: {manager_row["division"]}')
    st.write(f'Manager: {selected_manager} ({manager_row["role"]})')
    st.write(f'Number of Direct Reports: {len(employee_ids)}')
    
    # Display team members and team skills side by side
    col_members, col_skills = st.columns(2)
    with col_members:
        st.subheader('Team Members')
        st.dataframe(
            team_df[['name', 'id', 'role', 'date_joined']],
            column_config={
                'name': 'Name',
                'id': 'ID',
                'role': 'Role',
                'date_joined': 'Date Joined'
            },
            use_container_width=True
        )
    with col_skills:
        st.subheader('Team Skills')
        team_skills = skills_df[skills_df['employee_id'].isin(employee_ids)]
        skill_summary = team_skills.groupby('skill_name')['rating'].agg(['mean', 'count']).reset_index()
        skill_summary.columns = ['Skill', 'Average Rating', 'Count']
        skill_summary = skill_summary.sort_values('Count', ascending=False)
        st.dataframe(
            skill_summary,
            use_container_width=True
        )
    
    # Skill Gap Analysis
    st.subheader('Skill Gap Analysis')

    # Compute team_skill_gaps once per manager and cache in session_state
    cache_key = f"team_skill_gaps_{manager_id}"
    if cache_key not in st.session_state:
        with st.spinner('Analyzing skill gaps for your team. This may take a few seconds...'):
            team_skill_gaps = {}
            total_employees = len(team_df)
            progress = st.progress(0, text='Starting skill gap analysis...')
            for idx, (_, employee) in enumerate(team_df.iterrows()):
                employee_data = employee.to_dict()
                employee_skills = skills_df[skills_df['employee_id'] == employee['id']]
                employee_data['skills'] = employee_skills.to_dict('records')
                progress.progress((idx + 1) / total_employees, text=f"Analyzing: {employee['name']} ({employee['role']})")
                try:
                    gaps = get_employee_skill_gaps(employee_data)
                    team_skill_gaps[employee['id']] = {
                        'name': employee['name'],
                        'role': employee['role'],
                        'future_role': employee['future_role'],
                        'short_term_gaps': gaps['short_term_gaps'],
                        'long_term_gaps': gaps['long_term_gaps'],
                        'match_percent': gaps['match_percent']
                    }
                except Exception as e:
                    team_skill_gaps[employee['id']] = {
                        'name': employee['name'],
                        'role': employee['role'],
                        'future_role': employee['future_role'],
                        'short_term_gaps': [],
                        'long_term_gaps': [],
                        'match_percent': 100.0
                    }
            progress.empty()
            st.session_state[cache_key] = team_skill_gaps
    else:
        team_skill_gaps = st.session_state[cache_key]
    
    # Create tabs for different views
    gap_tabs = st.tabs(['Team Overview', 'Individual Analysis'])
    
    with gap_tabs[0]:
        # Team overview of skill gaps
        col1, col2 = st.columns(2)
        
        # Calculate average match percentage
        match_percentages = [data['match_percent'] for data in team_skill_gaps.values()]
        avg_match = sum(match_percentages) / len(match_percentages) if match_percentages else 0
        
        # Display average match percentage
        col1.metric("Team Average Skill Match", f"{avg_match:.1f}%")
        
        # Count total gaps
        total_st_gaps = sum(len(data['short_term_gaps']) for data in team_skill_gaps.values())
        total_lt_gaps = sum(len(data['long_term_gaps']) for data in team_skill_gaps.values())
        col2.metric("Total Skill Gaps", f"{total_st_gaps + total_lt_gaps}", 
                   f"ST: {total_st_gaps}, LT: {total_lt_gaps}")
        
        # Create a bar chart of match percentages
        st.subheader('Individual Skill Match')
        team_skill_gap_df = pd.DataFrame([
            {"Name": gap['name'], "Skill Match": gap['match_percent']} for gap in team_skill_gaps.values()
        ])
        fig = px.bar(
            team_skill_gap_df,
            x="Skill Match",
            y="Name",
            orientation="h",
            color="Skill Match",
            color_continuous_scale="Blues",
            labels={"Skill Match": "Skill Match Percentage", "Name": "Team Member"},
            title="Team Skill Match Percentage"
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display most common skill gaps
        st.subheader("Most Common Skill Gaps")
        
        # Collect all skill gaps
        all_st_gaps = [gap for data in team_skill_gaps.values() for gap in data['short_term_gaps']]
        all_lt_gaps = [gap for data in team_skill_gaps.values() for gap in data['long_term_gaps']]
        
        # Count occurrences
        from collections import Counter
        st_counter = Counter(all_st_gaps)
        lt_counter = Counter(all_lt_gaps)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Short-term Gaps (Top 5)")
            if st_counter:
                st_df = pd.DataFrame(st_counter.most_common(5), columns=['Skill', 'Count'])
                st.dataframe(st_df, use_container_width=True)
            else:
                st.write("No short-term gaps identified")
                
        with col2:
            st.write("Long-term Gaps (Top 5)")
            if lt_counter:
                lt_df = pd.DataFrame(lt_counter.most_common(5), columns=['Skill', 'Count'])
                st.dataframe(lt_df, use_container_width=True)
            else:
                st.write("No long-term gaps identified")
    
    with gap_tabs[1]:
        # Individual employee analysis
        selected_employee = st.selectbox(
            "Select Employee", 
            options=team_df['name'].tolist(),
            format_func=lambda x: f"{x} ({team_df[team_df['name'] == x].iloc[0]['role']})"
        )
        
        # Get employee details
        employee_row = team_df[team_df['name'] == selected_employee].iloc[0]
        employee_id = employee_row['id']
        
        # Run skill gap analysis only for the selected employee
        employee_data = employee_row.to_dict()
        employee_skills = skills_df[skills_df['employee_id'] == employee_id]
        employee_data['skills'] = employee_skills.to_dict('records')
        with st.spinner(f"Analyzing skill gaps for {employee_row['name']} ({employee_row['role']})..."):
            try:
                gaps = get_employee_skill_gaps(employee_data)
                gap_data = {
                    'name': employee_row['name'],
                    'role': employee_row['role'],
                    'future_role': employee_row['future_role'],
                    'short_term_gaps': gaps['short_term_gaps'],
                    'long_term_gaps': gaps['long_term_gaps'],
                    'match_percent': gaps['match_percent']
                }
            except Exception as e:
                st.error(f"Error analyzing skill gaps for {employee_row['name']}: {str(e)}")
                gap_data = {
                    'name': employee_row['name'],
                    'role': employee_row['role'],
                    'future_role': employee_row['future_role'],
                    'short_term_gaps': [],
                    'long_term_gaps': [],
                    'match_percent': 100.0
                }
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Role", gap_data['role'])
        col2.metric("Future Role", gap_data['future_role'])
        col3.metric("Skill Match", f"{gap_data['match_percent']:.1f}%")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Short-term Skill Gaps")
            if gap_data['short_term_gaps']:
                for skill in gap_data['short_term_gaps']:
                    st.markdown(f"- {skill}")
            else:
                st.write("No short-term gaps identified")
        with col2:
            st.write("Long-term Skill Gaps")
            if gap_data['long_term_gaps']:
                for skill in gap_data['long_term_gaps']:
                    st.markdown(f"- {skill}")
            else:
                st.write("No long-term gaps identified")
        st.write("Current Skills")
        if not employee_skills.empty:
            skill_df = employee_skills[['skill_name', 'rating', 'type']].sort_values('rating', ascending=False)
            skill_df.columns = ['Skill', 'Rating', 'Type']
            st.dataframe(skill_df, use_container_width=True)
        else:
            st.write("No skills data available")


with tabs[1]:
    st.header('Employee Drill Down')
    st.write('Placeholder for Employee Drill Down content.')

with tabs[2]:
    st.header('Secondment/Project Matching')
    st.write('Placeholder for Secondment/Project Matching content.')
