import PyPDF2
import pandas as pd
import io

def load_sample_data():
    """
    Load sample data for job roles, training programs, and secondment projects
    """
    # Job roles data
    job_roles = [
        {
            "title": "Software Engineer",
            "required_skills": ["Python", "JavaScript", "Git", "AWS", "Database Design"],
            "preferred_skills": ["React", "Node.js", "CI/CD", "Docker", "Kubernetes"],
            "level": "Mid-level"
        },
        {
            "title": "Data Scientist",
            "required_skills": ["Python", "R", "Statistics", "SQL", "Data Visualization"],
            "preferred_skills": ["Machine Learning", "Deep Learning", "NLP", "Big Data", "Azure ML"],
            "level": "Senior"
        },
        {
            "title": "DevOps Engineer",
            "required_skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "Infrastructure as Code"],
            "preferred_skills": ["AWS", "Azure", "GCP", "Terraform", "Ansible"],
            "level": "Mid-level"
        },
        {
            "title": "Product Manager",
            "required_skills": ["Product Strategy", "Agile Methodology", "User Research", "Data Analysis", "Stakeholder Management"],
            "preferred_skills": ["Technical Background", "UX Design", "Market Research", "Product Analytics", "A/B Testing"],
            "level": "Senior"
        }
    ]
    
    # Training programs data
    training_programs = [
        {
            "name": "Advanced Python Programming",
            "skills": ["Python", "Object-Oriented Programming", "Python Libraries", "Testing"],
            "duration": "4 weeks",
            "level": "Intermediate"
        },
        {
            "name": "Machine Learning Fundamentals",
            "skills": ["Python", "Statistics", "Machine Learning Algorithms", "Data Preprocessing"],
            "duration": "6 weeks",
            "level": "Beginner"
        },
        {
            "name": "Advanced Machine Learning",
            "skills": ["Deep Learning", "Neural Networks", "NLP", "Computer Vision"],
            "duration": "8 weeks",
            "level": "Advanced"
        },
        {
            "name": "Cloud Architecture on Azure",
            "skills": ["Azure", "Cloud Architecture", "Serverless Computing", "Azure DevOps"],
            "duration": "6 weeks",
            "level": "Intermediate"
        },
        {
            "name": "Leadership and Management",
            "skills": ["Team Management", "Leadership", "Conflict Resolution", "Performance Management"],
            "duration": "4 weeks",
            "level": "Intermediate"
        },
        {
            "name": "Agile Project Management",
            "skills": ["Agile Methodology", "Scrum", "Kanban", "Project Planning"],
            "duration": "3 weeks",
            "level": "Beginner"
        },
        {
            "name": "Modern JavaScript and Frontend Frameworks",
            "skills": ["JavaScript", "React", "Vue.js", "Angular"],
            "duration": "5 weeks",
            "level": "Intermediate"
        },
        {
            "name": "DevOps Practices and Tools",
            "skills": ["CI/CD", "Docker", "Kubernetes", "Infrastructure as Code"],
            "duration": "6 weeks",
            "level": "Intermediate"
        }
    ]
    
    # Secondment projects data
    secondment_projects = [
        {
            "name": "Customer Data Analytics Platform",
            "required_skills": ["Python", "Data Analysis", "SQL", "Visualization"],
            "duration": "3 months",
            "department": "Marketing Analytics",
            "goals": ["Implement predictive customer behavior models", "Design interactive dashboards"]
        },
        {
            "name": "Cloud Migration Initiative",
            "required_skills": ["Cloud Architecture", "AWS", "Azure", "Migration Strategy"],
            "duration": "6 months",
            "department": "IT Infrastructure",
            "goals": ["Migrate on-premise applications to cloud", "Implement cloud security best practices"]
        },
        {
            "name": "Mobile App Development",
            "required_skills": ["React Native", "JavaScript", "UI/UX Design", "API Integration"],
            "duration": "4 months",
            "department": "Digital Products",
            "goals": ["Develop cross-platform mobile application", "Implement offline functionality"]
        },
        {
            "name": "AI Chatbot Implementation",
            "required_skills": ["NLP", "Python", "Azure Bot Service", "Conversation Design"],
            "duration": "3 months",
            "department": "Customer Support",
            "goals": ["Develop automated customer support chatbot", "Integrate with existing support systems"]
        },
        {
            "name": "Data Governance Framework",
            "required_skills": ["Data Management", "Compliance", "Data Quality", "Documentation"],
            "duration": "5 months",
            "department": "Data Office",
            "goals": ["Design data governance policies", "Implement data quality monitoring"]
        },
        {
            "name": "Agile Transformation",
            "required_skills": ["Agile Methodology", "Change Management", "Training", "Process Design"],
            "duration": "6 months",
            "department": "Project Management Office",
            "goals": ["Transform traditional processes to Agile", "Train teams on Agile practices"]
        }
    ]
    
    return job_roles, training_programs, secondment_projects
