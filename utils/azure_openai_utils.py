import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

class AzureOpenAIService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def analyze_resume(self, resume_text, job_roles_data, trainings_data, projects_data):
        """
        Analyze resume using Azure OpenAI to identify skill gaps, training recommendations,
        and potential secondment projects.
        """
        prompt = self._create_analysis_prompt(resume_text, job_roles_data, trainings_data, projects_data)
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a talented HR professional and career advisor specializing in skill gap analysis and professional development recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )
        
        return response.choices[0].message.content
    
    def _create_analysis_prompt(self, resume_text, job_roles_data, trainings_data, projects_data):
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
