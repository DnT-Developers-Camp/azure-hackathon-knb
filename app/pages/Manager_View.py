import streamlit as st

st.title('Manager View')

# Create tabs
tabs = st.tabs([
    'Team Snapshot',
    'Employee Drill Down',
    'Secondment/Project Matching'
])

with tabs[0]:
    st.header('Team Snapshot')
    st.write('Placeholder for Team Snapshot content.')

with tabs[1]:
    st.header('Employee Drill Down')
    st.write('Placeholder for Employee Drill Down content.')

with tabs[2]:
    st.header('Secondment/Project Matching')
    st.write('Placeholder for Secondment/Project Matching content.')
