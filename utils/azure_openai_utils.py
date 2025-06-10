import json
from openai import AzureOpenAI
from utils.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME
)

from utils.resume_parser import skills_definition_iv, skills_definition_dnt

def get_openai_client():
    """Create and return an Azure OpenAI client"""
    return AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

def create_analysis_prompt(resume_text, job_roles_data, trainings_data, projects_data):
    """Create a detailed prompt for resume analysis"""
    prompt = f"""
    Please analyze the following resume and provide a comprehensive talent management assessment:

    RESUME:
    {resume_text}

    AVAILABLE JOB ROLES IN THE ORGANIZATION:
    {json.dumps(job_roles_data, indent=2)}

    AVAILABLE TRAINING PROGRAMS:
    {json.dumps(trainings_data, indent=2)}

    POTENTIAL SECONDMENT PROJECTS:
    {json.dumps(projects_data, indent=2)}

    Please provide the following analysis in JSON format:
    1. Skills Assessment: Identify the candidate's current skills, expertise level for each skill (Beginner/Intermediate/Expert), and how they align with organizational needs.
    2. Skill Gaps: What critical skills is the employee missing for their current role or for career advancement?
    3. Training Recommendations: Based on the available training programs, recommend specific courses that would address the skill gaps.
    4. Secondment Project Recommendations: Suggest 2-3 potential secondment projects that would be a good fit based on their current skills and career development needs.
    5. Career Path: Recommend possible next career moves within the organization.

    Return the analysis in a structured JSON format with the following keys: "skills_assessment", "skill_gaps", "training_recommendations", "secondment_recommendations", "career_path".
    """
    return prompt

def analyze_resume(resume_text, job_roles_data, trainings_data, projects_data):
    """
    Analyze resume using Azure OpenAI to identify skill gaps, training recommendations,
    and potential secondment projects.
    """
    client = get_openai_client()
    prompt = create_analysis_prompt(resume_text, job_roles_data, trainings_data, projects_data)
    
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a talented HR professional and career advisor specializing in skill gap analysis and professional development recommendations."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def standardize_skill_output(md_text:str,type:str)->dict:
    """
    type can be Investment or Digital Technology
    Standardize the skill output from the Azure OpenAI response to a structured format.
    Extract into the format json
    {
    "skills":[
        {
            "skill_name": "Python",
            "rating": "1",
            "type":"technical"
        },
        {
            "skill_name": "Data Analysis",
            "rating": "2",
            "type":"technical"
        }
    ]
    }
    """
    # Use Azure OpenAI to extract skills and ratings from the resume text
    if type=="Investment":
        skills_reference = skills_definition_iv
    else:
        skills_reference = skills_definition_dnt
    client = get_openai_client()
    # Prepare a prompt to extract skills and their ratings from the resume
    skills_list = list(skills_reference.get('skills_rating_definition', {}).keys())
    prompt = f"""
    Given the following resume text, extract the skills and their proficiency level (1-5) for each skill. Only consider these skills from the reference below: {json.dumps(skills_reference, indent=2)}.
    For each skill found in the resume, output a JSON array in the format:
    {{
      "skills": [
        {{"skill_name": "<Skill>", "rating": "<1-5>", "type": "<technical/soft>"}},
        ...
      ]
    }}
    If a skill is not mentioned, do not include it. If a rating is not clear, estimate based on context.
    Resume:
    {md_text}
    """
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert HR analyst. Extract and rate only the listed skills from the resume."},
            {"role": "user", "content": prompt}
        ]
    )
    # Parse the response and filter only valid skills
    try:
        result = json.loads(response.choices[0].message.content)
        valid_skills = set(skills_list)
        standardized = {
            "skills": [
                s for s in result.get("skills", [])
                if s.get("skill_name") in valid_skills and str(s.get("rating")).isdigit()
            ]
        }
        return standardized
    except Exception:
        return {"skills": []}

def extract_employee_name(resume_text: str) -> str:
    """
    Extract the employee's name from the resume text using Azure OpenAI.
    Returns the name as a string, or an empty string if not found.
    """
    client = get_openai_client()
    prompt = f"""
    Given the following resume text, extract ONLY the full name of the employee. Return the result in JSON format as:
    {{"name": "<Full Name>"}}
    If the name cannot be determined, return {{"name": ""}}.
    Resume:
    {resume_text}
    """
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert HR analyst. Extract only the employee's full name from the resume."},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        result = json.loads(response.choices[0].message.content)
        return result.get("name", "")
    except Exception:
        return ""




