import json
import os
from functools import lru_cache
from openai import AzureOpenAI
from utils.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_DEPLOYMENT_NAME
)

def get_openai_client():
    """Create and return an Azure OpenAI client"""
    return AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

def create_skill_gap_prompt(current_jd, future_jd):
    """Create a prompt for skill gap analysis without using f-strings for the JSON part"""
    # Use string concatenation instead of f-strings for the JSON example part
    json_format_example = '[{"skill": "skill name", "effort": 3}, {"skill": "another skill", "effort": 7}]'
    
    prompt = (
        "Please analyze the following job descriptions and identify the skills that are missing from the current role but needed for the future role:\n\n"
        "CURRENT JOB DESCRIPTION:\n"
        f"{current_jd}\n\n"
        "FUTURE JOB DESCRIPTION:\n"
        f"{future_jd}\n\n"
        "Based on these job descriptions, identify the specific skills that the person would need to acquire to move from the current role to the future role.\n"
        "For each missing skill, provide an effort score from 1-10 that represents how difficult or time-consuming it would be to acquire this skill.\n\n"
        "Effort score guidelines:\n"
        "- 1-4: Skills that can be acquired in the short term (weeks to a few months)\n"
        "- 5-10: Skills that require long-term development (several months to years)\n\n"
        "Return ONLY the missing skills in the following JSON format:\n"
        f"{json_format_example}\n\n"
        "If there are no missing skills, return an empty array [].\n"
    )
    return prompt

@lru_cache(maxsize=128)
def analyze_skill_gaps(current_jd, future_jd):
    """Analyze the gap between current and future job descriptions using Azure OpenAI."""
    # Create a mock response for testing without calling the API
    # This helps avoid API errors during development
    mock_mode = False
    
    if mock_mode:
        # Mock data for testing
        skill_gaps = [
            {"skill": "Project Management", "effort": 3},
            {"skill": "Team Leadership", "effort": 4},
            {"skill": "Strategic Planning", "effort": 6},
            {"skill": "Budget Management", "effort": 5}
        ]
    else:
        try:
            # Get the OpenAI client
            client = get_openai_client()
            
            # Create the prompt
            prompt = create_skill_gap_prompt(current_jd, future_jd)
            
            # Define the function calling schema
            functions = [
                {
                    "name": "get_skill_gaps",
                    "description": "Get the skills gaps between current and future job descriptions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "skill_gaps": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "skill": {"type": "string"},
                                        "effort": {"type": "integer", "minimum": 1, "maximum": 10}
                                    },
                                    "required": ["skill", "effort"]
                                }
                            }
                        },
                        "required": ["skill_gaps"]
                    }
                }
            ]
            
            # Call the API
            response = client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a career development expert specializing in skill gap analysis."},
                    {"role": "user", "content": prompt}
                ],
                functions=functions,
                function_call={"name": "get_skill_gaps"},
                temperature=0.0  # Ensure deterministic output
            )
            
            # Parse the response
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "get_skill_gaps":
                try:
                    result = json.loads(function_call.arguments)
                    skill_gaps = result.get("skill_gaps", [])
                except json.JSONDecodeError:
                    skill_gaps = []
            else:
                # Fallback to parsing the content if function call fails
                try:
                    content = response.choices[0].message.content
                    skill_gaps = json.loads(content)
                except (json.JSONDecodeError, AttributeError):
                    skill_gaps = []
        except Exception as e:
            print(f"Error calling Azure OpenAI API: {str(e)}")
            # Return empty list in case of error
            skill_gaps = []
    
    # Categorize skills into short-term and long-term gaps
    short_term_gaps = [item["skill"] for item in skill_gaps if item["effort"] <= 4]
    long_term_gaps = [item["skill"] for item in skill_gaps if item["effort"] > 4]
    
    # Calculate match percentage based on current skills and gaps
    def calculate_match_percent(current_skill_count):
        total_skills = current_skill_count + len(short_term_gaps) + len(long_term_gaps)
        if total_skills == 0:
            return 100.0  # If no skills are needed, it's a perfect match
        return (current_skill_count / total_skills) * 100.0
    
    return {
        "short_term_gaps": short_term_gaps,
        "long_term_gaps": long_term_gaps,
        "match_percent": calculate_match_percent
    }

def get_employee_skill_gaps(employee_data, skill_sets):
    """Analyze skill gaps for a specific employee based on their current and future roles."""
    # Get job descriptions
    current_jd = employee_data.get("job_desc", "")
    future_jd = employee_data.get("future_job_desc", "")
    
    # Get the skill gaps analysis
    result = analyze_skill_gaps(current_jd, future_jd)
    
    # Calculate match percentage based on employee's current skills
    current_skill_count = len(employee_data.get("skills", []))
    match_percent = result["match_percent"](current_skill_count)

    prompt = f"""
    You are an expert HR analyst. Your task is to extract and evaluate only the skills listed below.

    1. Based on the provided resume, categorize them into the five groups listed below and give a fair score based on the information
        - Programming Languages
        - Cloud Platforms
        - Data Analysis
        - Leadership
        - Communication Skills
    2. Assign a proficiency rating from 1 to 5 based on the context provided in the resume.
    - If a rating is not explicitly mentioned, estimate it based on context.

    Return the result strictly in the following JSON format:

    {{
    "skills": [
        {{"skill_name": "<Skill>", "rating": <1-5>}},
        ...
    ]
    }}

    Skill Set:
    {employee_data}
    """

    client = get_openai_client()

    new_response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert HR analyst. You are skilled at standardizing the skillset of an individual."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the content from the response
    content = new_response.choices[0].message.content
    # Parse the JSON content
    skills_data = json.loads(content)

    prompt = f""" 
    You are an expert HR analyst. Your task is to evaluate the future job description and identify the rating required for the job itself. 

    1. Based on the provided job description and typical similar role, categorize them into the five groups listed below and give a fair score based on the information 
    - Programming Languages
    - Cloud Platforms
    - Data Analysis
    - Leadership
    - Communication Skills
    2. Assign a proficiency rating from 1 to 5 based on the context provided in the job description.
    - If a rating is not explicitly mentioned, estimate it based on context.

    Return the result strictly in the following JSON format:

    {{
    "skills": [
        {{"skill_name": "<Skill>", "rating": <1-5>}},
        ...
    ]
    }}

    Skill Set:
    {employee_data['future_role'], employee_data['future_job_desc']}
    """

    client = get_openai_client()

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert HR analyst. You are skilled at evaluating the rating based on a future job description for an individual."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the content from the response
    content = response.choices[0].message.content
    # Parse the JSON content
    future_jd_skill_data = json.loads(content)

    
    return {
        "short_term_gaps": result["short_term_gaps"],
        "long_term_gaps": result["long_term_gaps"],
        "match_percent": match_percent,
        "skills_data": skills_data,
        "future_jd_skill_data": future_jd_skill_data
    }

def prepare_lt_st_training_plan(short_term_gaps, long_term_gaps):
    prompt = f"""
    You are an expert HR training analyst. Your task is to create a training plan for an employee based on their long-term and short-term skill gaps.
    1. For each long-term skill gap, suggest a comprehensive training program that includes:
    - Course name
    - Duration (in weeks)
    - Estimated cost
    - Short description of the course 
    2. For each short-term skill gap, suggest a quick training or resource that includes:
        - Course name
        - Duration (in days)
        - Estimated cost
        - Short description of the course 

    Return the result strictly in the following JSON format:
    {{
        "long_term_training": [
            {{
                "skill": "<Skill Name>",
                "course_name": "<Course Name>",
                "duration_weeks": "<Duration in weeks>",
                "cost": "<Estimated cost>",
                "description": "<Short description>"
            }},
            ...
        ],
        "short_term_training": [
            {{
                "skill": "<Skill Name>",
                "course_name": "<Course Name>",
                "duration_days": "<Duration in days>",
                "cost": "<Estimated cost>",
                "description": "<Short description>"
            }},
            ...
        ]
    }}

    Long-term and short-term skill gaps:
        Long-term skill gaps: {long_term_gaps} 
        Short-term skill gaps: {short_term_gaps}
    """

    
    client = get_openai_client()

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert HR analyst. You are skilled providing training plan for employees."},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    parsed_content = json.loads(content)

    return {"long_term_training" : parsed_content['long_term_training'],
            "short_term_training": parsed_content['short_term_training']}
