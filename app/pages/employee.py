import streamlit as st
import pandas as pd
import plotly.graph_objects as go 

# Hardcoded employee information
employee_name = "Hao Yee"
employee_role = "Software Engineer"
job_description = "Responsible for developing and maintaining software applications, collaborating with cross-functional teams, and ensuring high-quality code standards."
employee_skills = [
    "Python",
    "Data Analysis",
    "Machine Learning",
    "Project Management",
    "Azure Cloud Services"
]

technical_skills = {
    "Python": {"level": "Advanced", "rating": 5},
    "Data Analysis": {"level": "Intermediate", "rating": 4},
    "Machine Learning": {"level": "Intermediate", "rating": 3},
    "Azure Cloud Services": {"level": "Intermediate", "rating": 4},
    "SQL": {"level": "Advanced", "rating": 5}
}

soft_skills = {
    "Project Management": {"level": "Intermediate", "rating": 4},
    "Team Leadership": {"level": "Basic", "rating": 3},
    "Communication": {"level": "Advanced", "rating": 5},
    "Problem Solving": {"level": "Advanced", "rating": 5},
    "Time Management": {"level": "Intermediate", "rating": 4}
}


st.title(f"Welcome, {employee_name}!")

tab1, tab2, tab3 = st.tabs(["Current Role & Skills", "Tasks", "Settings"])

# with tab1:
#     st.subheader(f"Current Role & Job Description")
#     st.markdown("""
#     **Current Role:** {}  
#     **Job Description:** {}
#     """.format(employee_role, job_description), unsafe_allow_html=True)
#     st.markdown("<hr style='margin: 5px 0px'>", unsafe_allow_html=True)
    
#     # Display skills
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.markdown("### Technical Skills")
#         st.markdown("<hr style='margin: 5px 0px'>", unsafe_allow_html=True)
#         for skill, info in technical_skills.items():
#             rating = "⭐" * info["rating"]
#             st.markdown(f"**{skill}** ({info['level']})  \n{rating}")
    
#     # Add vertical line
#     # st.markdown("<div class='vertical-line'></div>", unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("### Soft Skills")
#         st.markdown("<hr style='margin: 5px 0px'>", unsafe_allow_html=True)
#         for skill, info in soft_skills.items():
#             rating = "⭐" * info["rating"]
#             st.markdown(f"**{skill}** ({info['level']})  \n{rating}")
    
#     # Create a dataframe for better visualization
#     all_skills = {}
#     for skill, info in technical_skills.items():
#         all_skills[f"Technical: {skill}"] = info["rating"]
#     for skill, info in soft_skills.items():
#         all_skills[f"Soft: {skill}"] = info["rating"]
    
#     # Create radar chart
#     st.subheader("Skill Chart")
#     st.markdown("<hr style='margin: 5px 0px'>", unsafe_allow_html=True)

#     fig = go.Figure()
    
#     fig.add_trace(go.Scatterpolar(
#         r=list(all_skills.values()),
#         theta=list(all_skills.keys()),
#         fill='toself',
#         name='Skills Profile'
#     ))
    
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=False,
#                 range=[0, 5]
#             )
#         ),
#         showlegend=False,
#         height = 400
#     )
    
#     # Display the chart
#     st.plotly_chart(fig, use_container_width=True)

# with tab2:
#     st.header("Tasks")
#     st.write("Employee tasks and assignments go here.")

# with tab3:
#     st.header("Settings")
#     st.write("Employee settings and preferences go here.")


st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        padding-bottom: 20px;
    }
    .section-header {
        color: #0D47A1;
        padding: 10px 0;
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
st.markdown(f"<h1 class='main-header'>Welcome, {employee_name}! 👋</h1>", unsafe_allow_html=True)

# ...existing tab definition...

with tab1:
    # Role and Job Description section
    st.markdown("<h3 class='section-header'>Current Role & Job Description</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='job-description'>
        <h3 style='color: #1976D2;'>{employee_role}</h3>
        <p style='font-size: 1.1em;'>{job_description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Skills section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h3 class='section-header'>Technical Skills</h3>", unsafe_allow_html=True)
        st.markdown("<div class='skill-container'>", unsafe_allow_html=True)
        for skill, info in technical_skills.items():
            rating = "⭐" * info["rating"] + "☆" * (5 - info["rating"])
            st.markdown(f"""
                <div style='margin-bottom: 15px;'>
                    <strong style='color: #1976D2;'>{skill}</strong> 
                    <span style='color: #666; font-size: 0.9em;'>({info['level']})</span><br>
                    {rating}
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 class='section-header'>Soft Skills</h3>", unsafe_allow_html=True)
        st.markdown("<div class='skill-container'>", unsafe_allow_html=True)
        for skill, info in soft_skills.items():
            rating = "⭐" * info["rating"] + "☆" * (5 - info["rating"])
            st.markdown(f"""
                <div style='margin-bottom: 15px;'>
                    <strong style='color: #1976D2;'>{skill}</strong>
                    <span style='color: #666; font-size: 0.9em;'>({info['level']})</span><br>
                    {rating}
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Radar Chart section
    st.markdown("<h3 class='section-header'>Skills Overview</h3>", unsafe_allow_html=True)
    
        # Create a dataframe for better visualization
    all_skills = {}
    for skill, info in technical_skills.items():
        all_skills[f"Technical: {skill}"] = info["rating"]
    for skill, info in soft_skills.items():
        all_skills[f"Soft: {skill}"] = info["rating"]
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
                tickfont=dict(size=10),
                gridcolor='#e0e0e0'
            ),
            angularaxis=dict(
                tickfont=dict(size=8)
            ),
            bgcolor='#f8f9fa'
        ),
        showlegend=False,
        height=375,
        margin=dict(t=30, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)