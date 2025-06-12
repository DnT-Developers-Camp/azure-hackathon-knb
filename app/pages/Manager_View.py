import streamlit as st
import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import importlib
from utils import skill_gap_engine as _sge, azure_openai_utils as ao_utils
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

# Load projects data
def load_projects_data():
    """Load projects data from sample JSON."""
    base_dir = Path(__file__).parent.parent.parent
    projects_path = os.path.join(base_dir, 'data', 'sample_data', 'projects_demo.json')
    with open(projects_path, 'r') as f:
        projects_data = json.load(f)
    return projects_data

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

# Helper: AI candidate matching using utils.azure_openai_utils
@st.cache_data(show_spinner=False)
def ai_match_candidate(project: dict, employee: dict, employee_skills: list):
    """Call Azure OpenAI to infer candidate fit. Returns (score 0-100, reasoning str)."""
    # If credentials are not set up in utils.config, fall back to heuristic
    try:
        client = ao_utils.get_openai_client()
        deployment_name = ao_utils.AZURE_OPENAI_DEPLOYMENT_NAME
    except Exception:
        client = None
        deployment_name = None

    if client is None or deployment_name is None:
        # Fallback simple heuristic if no API config
        proj_skills = {s['skill_name'] for s in project['required_skills']}
        emp_skill_names = {s['skill_name'] for s in employee_skills}
        overlap = len(proj_skills & emp_skill_names)
        score = round((overlap / len(proj_skills)) * 100, 1) if proj_skills else 0
        reasoning = "Fallback word-match heuristic used (no Azure OpenAI credentials)."
        return score, reasoning

    # Build prompt
    prompt_system = "You are an expert resource manager. You will evaluate candidate skills vs project requirements and return a numeric fit score and short reasoning."
    project_skill_str = "\n".join([f"- {s['skill_name']} (effort {s['effort']})" for s in project['required_skills']])
    employee_skill_str = "\n".join([f"- {s['skill_name']} (rating {s['rating']})" for s in employee_skills])
    prompt_user = (
        f"Project: {project['project_name']} ({project['project_id']})\n"
        f"Required skills:\n{project_skill_str}\n\n"
        f"Candidate: {employee['name']} ({employee['role']})\n"
        f"Candidate skills:\n{employee_skill_str}\n\n"
        "Respond in JSON with the following keys: match_score (0-100 numeric), reasoning (short)."
    )

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user}
            ],
            temperature=0.2,
            max_tokens=200
        )
        content = response.choices[0].message.content
        import json as _json
        data = _json.loads(content.strip())
        return float(data.get('match_score', 0)), data.get('reasoning', '')
    except Exception as e:
        return 0.0, f"Error from OpenAI: {str(e)[:100]}"

# Load data and create structures
employees_data, managers_data = load_json_data()
projects_data = load_projects_data()
employees_df, skills_df, managers_df = create_dataframes(employees_data, managers_data)
manager_employee_lookup = create_manager_employee_lookup(managers_data)

# Main app
st.set_page_config(page_title='Manager View', layout='wide')
st.title('Manager View')

# Create tabs
tabs = st.tabs([
    'Team Snapshot',
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
    
    # --- NEW: Manager context as title/subtitle ---
    st.markdown(f"""
        <div style='font-size: 1.6em; font-weight: 700;'>{selected_manager}</div>
        <div style='font-size: 1.1em; color: #666;'>Division: {manager_row['division']} &nbsp;|&nbsp; Role: {manager_row['role']}</div>
        <div style='font-size: 1em; color: #888;'>Direct Reports: {len(employee_ids)}</div>
    """, unsafe_allow_html=True)
    # --- Existing: Team Members and Skills (leave as is) ---
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
        col1.metric(
            "Team Average Skill Match",
            f"{avg_match:.1f}%",
            help="Average percentage indicating how closely your team's current skills align with required skills (100% = perfect match)."
        )
        
        # Count total gaps
        total_st_gaps = sum(len(data['short_term_gaps']) for data in team_skill_gaps.values())
        total_lt_gaps = sum(len(data['long_term_gaps']) for data in team_skill_gaps.values())
        col2.metric(
            "Total Skill Gaps",
            f"{total_st_gaps + total_lt_gaps}",
            f"ST: {total_st_gaps}, LT: {total_lt_gaps}",
            help="A skill gap is the difference between the skills an employee currently has and the skills required for their current or future role."
        )
        
        # Create a bar chart of match percentages
        st.subheader('Individual Skill Match', help='Bar chart showing each team member’s overall skill-match percentage (higher is better).')
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

        # --- Heatmap of skills vs employees ---
        def render_heatmap(team_skill_gaps: dict, skills_df: pd.DataFrame):
            """Render a skill vs. employee heatmap using Plotly."""
            skill_matrix = []
            names = []
            for emp_id, data in team_skill_gaps.items():
                emp_skills = skills_df[skills_df['employee_id'] == emp_id]
                row = {}
                for _, skill in emp_skills.iterrows():
                    row[skill['skill_name']] = skill['rating']
                skill_matrix.append(row)
                names.append(data['name'])
            skill_df = pd.DataFrame(skill_matrix, index=names).fillna(0)
            fig = px.imshow(skill_df, aspect='auto', color_continuous_scale='Blues',
                           labels=dict(x="Skill", y="Employee", color="Rating"),
                           title="Employee Skill Heatmap")
            st.plotly_chart(fig, use_container_width=True)

        render_heatmap(team_skill_gaps, skills_df)
        
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
        
        # --- Employee Capability Profile Table ---
        cap_df_key = "capability_df"
        if cap_df_key not in st.session_state:
            with st.spinner("Computing employee capability profiles..."):
                capability_rows = []
                total_emp = len(employees_df)
                progress_cap = st.progress(0, text="Computing capability profiles...")
                for idx, (_, emp) in enumerate(employees_df.iterrows()):
                    emp_data = emp.to_dict()
                    emp_skills = skills_df[skills_df['employee_id'] == emp['id']]
                    emp_data['skills'] = emp_skills.to_dict('records')
                    try:
                        gaps_emp = get_employee_skill_gaps(emp_data)
                        st_gaps = gaps_emp['short_term_gaps']
                        lt_gaps_e = gaps_emp['long_term_gaps']
                        capability_rows.append({
                            'id': emp['id'],
                            'name': emp['name'],
                            'role': emp['role'],
                            'manager': emp['manager'],
                            'st_gap_count': len(st_gaps),
                            'lt_gap_count': len(lt_gaps_e),
                            'match_pct': gaps_emp['match_percent'],
                            'st_gap_list': ", ".join(st_gaps),
                            'lt_gap_list': ", ".join(lt_gaps_e)
                        })
                    except Exception:
                        capability_rows.append({
                            'id': emp['id'],
                            'name': emp['name'],
                            'role': emp['role'],
                            'manager': emp['manager'],
                            'st_gap_count': 0,
                            'lt_gap_count': 0,
                            'match_pct': 100.0,
                            'st_gap_list': "",
                            'lt_gap_list': ""
                        })
                    progress_cap.progress((idx + 1) / total_emp)
                progress_cap.empty()
                capability_df = pd.DataFrame(capability_rows)
                st.session_state[cap_df_key] = capability_df
        else:
            capability_df = st.session_state[cap_df_key]

        # Filter to current manager's direct reports
        manager_cap_df = capability_df[capability_df['manager'] == selected_manager].copy()
        manager_cap_df['match_pct'] = manager_cap_df['match_pct'].round(1)

        st.subheader("Employee Capability Profile Table")
        st.dataframe(manager_cap_df, use_container_width=True)
    
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
        col1.markdown(f"""
            <div style='font-size: 14px; font-weight: 600;'>Current Role</div>
            <div style='font-size: 16px; font-weight: 700; color: #333;'>{gap_data['role']}</div>
        """, unsafe_allow_html=True)
        col2.markdown(f"""
            <div style='font-size: 14px; font-weight: 600;'>Future Role</div>
            <div style='font-size: 16px; font-weight: 700; color: #333;'>{gap_data['future_role']}</div>
        """, unsafe_allow_html=True)
        col3.metric("Skill Match", f"{gap_data['match_percent']:.1f}%")

        # Display short-term and long-term gap lists
        st.subheader("Skill Gap Lists")
        gap_col1, gap_col2 = st.columns(2)
        gap_col1.write("Short-term Gaps")
        if gap_data['short_term_gaps']:
            gap_col1.write(", ".join(gap_data['short_term_gaps']))
        else:
            gap_col1.write("None")
        gap_col2.write("Long-term Gaps")
        if gap_data['long_term_gaps']:
            gap_col2.write(", ".join(gap_data['long_term_gaps']))
        else:
            gap_col2.write("None")

        if not employee_skills.empty:
            skill_df = employee_skills[['skill_name', 'rating', 'type']].sort_values('rating', ascending=False)
            skill_df.columns = ['Skill', 'Rating', 'Type']
            st.dataframe(skill_df, use_container_width=True)
        else:
            st.write("No skills data available")


with tabs[1]:
    st.header('Secondment / Project Matching')

    # Select project dropdown
    project_options = [f"{proj['project_name']} ({proj['project_id']})" for proj in projects_data]
    selected_project_label = st.selectbox('Select Project', project_options)

    # Retrieve selected project dict
    selected_project = next(p for p in projects_data if f"{p['project_name']} ({p['project_id']})" == selected_project_label)

    # Display project details
    st.subheader('Project Details')
    st.markdown(f"**Project ID:** {selected_project['project_id']}")
    st.markdown(f"**Division:** {selected_project['division']}")
    st.markdown(f"**Duration (months):** {selected_project['duration_months']}")
    st.markdown(f"**Location:** {selected_project['location']}")
    st.write(selected_project['project_description'])

    # Display required skills table
    st.subheader('Required Skills & Effort')
    req_skills_df = pd.DataFrame(selected_project['required_skills'])
    req_skills_df.columns = ['Skill', 'Effort']
    st.dataframe(req_skills_df, use_container_width=True)

    # Button to find matches among manager's direct reports
    if st.button('Find Matches'):
        st.subheader('Candidate Matches (Direct Reports)')

        # Filter candidates by project division prefix (INV or DNT)
        proj_prefix = selected_project['project_id'].split('-')[0]  # e.g., 'INV' or 'DNT'
        candidate_df = team_df[team_df['id'].str.startswith(proj_prefix)].copy()

        total_emp = len(candidate_df)
        if total_emp == 0:
            st.info(f"No {proj_prefix} candidates found among your direct reports for this project.")
            st.stop()

        candidate_rows = []
        progress = st.progress(0, text="Evaluating candidates with Azure OpenAI...")
        for idx, (_, emp) in enumerate(candidate_df.iterrows()):
            emp_id = emp['id']
            emp_skills_records = skills_df[skills_df['employee_id'] == emp_id].to_dict('records')

            score, reasoning = ai_match_candidate(selected_project, emp.to_dict(), emp_skills_records)

            candidate_rows.append({
                'Employee': emp['name'],
                'Role': emp['role'],
                'Match %': round(score, 1),
                'Reasoning': reasoning
            })
            progress.progress((idx + 1) / total_emp, text=f"Evaluating: {emp['name']} ({emp['role']})")

        progress.empty()

        if candidate_rows:
            cand_df = pd.DataFrame(candidate_rows).sort_values('Match %', ascending=False)
            st.dataframe(cand_df, use_container_width=True)
        else:
            st.info('No direct reports found for this manager.')
