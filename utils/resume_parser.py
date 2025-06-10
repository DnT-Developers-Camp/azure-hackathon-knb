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
            "job_description": "Designs, develops, tests, and maintains software applications and systems. Collaborates with cross-functional teams to deliver scalable and robust solutions.",
            "required_skills": ["Python", "JavaScript", "Git", "AWS", "Database Design"],
            "preferred_skills": ["React", "Node.js", "CI/CD", "Docker", "Kubernetes"],
            "level": "Mid-level",
            "type": "Digital Technology"
        },
        {
            "title": "Data Scientist",
            "job_description": "Analyzes complex data sets to extract insights, build predictive models, and support data-driven decision making. Works with stakeholders to solve business problems using statistical and machine learning techniques.",
            "required_skills": ["Python", "R", "Statistics", "SQL", "Data Visualization"],
            "preferred_skills": ["Machine Learning", "Deep Learning", "NLP", "Big Data", "Azure ML"],
            "level": "Senior",
            "type": "Digital Technology"
        },
        {
            "title": "DevOps Engineer",
            "job_description": "Implements and manages CI/CD pipelines, automates infrastructure, and ensures reliable deployment of applications. Collaborates with development and operations teams to improve system reliability and scalability.",
            "required_skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "Infrastructure as Code"],
            "preferred_skills": ["AWS", "Azure", "GCP", "Terraform", "Ansible"],
            "level": "Mid-level",
            "type": "Digital Technology"
        },
        {
            "title": "Product Manager",
            "job_description": "Leads product strategy, defines requirements, and manages product lifecycle. Works with engineering, design, and business teams to deliver products that meet user needs and business goals.",
            "required_skills": ["Product Strategy", "Agile Methodology", "User Research", "Data Analysis", "Stakeholder Management"],
            "preferred_skills": ["Technical Background", "UX Design", "Market Research", "Product Analytics", "A/B Testing"],
            "level": "Senior",
            "type": "Digital Technology"
        },
        {
            "title": "Senior Digital & Technology Specialist",
            "job_description": "Architects and implements digital solutions, leads technology transformation initiatives, and ensures best practices in cloud and full-stack development.",
            "required_skills": ["Cloud Architecture", "Microservices", "CI/CD", "Full-Stack Development", "Data Engineering"],
            "preferred_skills": ["AWS Solutions Architect", "Azure Solutions Architect", "Kubernetes", "Terraform", "Scrum Master"],
            "level": "Senior",
            "type": "Digital Technology"
        },
        {
            "title": "Cybersecurity Engineer",
            "job_description": "Protects systems and networks from cyber threats, manages security operations, and responds to incidents. Conducts vulnerability assessments and implements security best practices.",
            "required_skills": ["Network Security", "Security Operations", "Incident Response", "Security Tools", "Vulnerability Assessment"],
            "preferred_skills": ["CISSP", "CEH", "Python", "Cloud Security", "Security Architecture"],
            "level": "Senior",
            "type": "Digital Technology"
        },
        {
            "title": "Network Engineer",
            "job_description": "Designs, configures, and maintains network infrastructure. Troubleshoots network issues and ensures secure and efficient network operations.",
            "required_skills": ["Network Protocols", "Routing & Switching", "Network Security", "Troubleshooting", "Network Design"],
            "preferred_skills": ["CCNP", "Network Automation", "SDN", "Cloud Networking", "Python"],
            "level": "Mid-level",
            "type": "Digital Technology"
        },
        {
            "title": "Security Operations Analyst",
            "job_description": "Monitors security events, detects threats, and responds to incidents. Analyzes logs and supports the security operations center (SOC) in maintaining organizational security.",
            "required_skills": ["SIEM", "Threat Detection", "Security Monitoring", "Incident Response", "Log Analysis"],
            "preferred_skills": ["Security+", "SIEM Tools", "Threat Intelligence", "Forensics", "Automation"],
            "level": "Mid-level",
            "type": "Digital Technology"
        },
        {
            "title": "Senior Investment Analyst",
            "job_description": "Conducts in-depth investment research and analysis across asset classes, builds financial models, and presents recommendations to investment committees. Leads reporting and mentoring within the investment team.",
            "required_skills": [
                "Equity Research and Valuation",
                "Fixed Income and Credit Analysis",
                "Financial Modelling (DCF, LBO, M&A)",
                "Portfolio Construction and Risk Management",
                "Macroeconomic and Market Analysis",
                "ESG Integration",
                "Client and Stakeholder Reporting",
                "Investment Committee Presentation Skills",
                "Bloomberg Terminal and FactSet Expertise",
                "Team Mentoring and Leadership"
            ],
            "preferred_skills": [
                "CFA Charterholder",
                "Certificate in ESG Investing",
                "CIPM Certificate"
            ],
            "level": "Senior",
            "type": "Investment"
        },
        {
            "title": "Investment Operations Manager",
            "job_description": "Oversees investment operations including trade settlement, fund accounting, and regulatory reporting. Manages operational risk, process automation, and team leadership in investment operations.",
            "required_skills": [
                "Trade Settlement and Reconciliation",
                "Fund Accounting",
                "Regulatory Reporting",
                "Custodian and Counterparty Management",
                "Process Automation",
                "Risk and Compliance Oversight",
                "Performance Measurement",
                "Cash Management",
                "System Implementation",
                "Team Leadership"
            ],
            "preferred_skills": [
                "CFA Charterholder",
                "CAIA Certification",
                "IMC Qualification"
            ],
            "level": "Senior",
            "type": "Investment"
        },
        {
            "title": "Private Equity Analyst",
            "job_description": "Supports private equity deal sourcing, due diligence, and portfolio monitoring. Builds financial models, prepares investment memos, and assists in exit strategy analysis.",
            "required_skills": [
                "Deal Sourcing and Screening",
                "Financial Modelling (LBO, DCF)",
                "Due Diligence",
                "Industry and Market Research",
                "Portfolio Monitoring",
                "Investment Memo Preparation",
                "Valuation Analysis",
                "Stakeholder Communication",
                "Data Room Management",
                "Exit Strategy Analysis"
            ],
            "preferred_skills": [
                "CFA Level II or above",
                "CAIA Level I or above",
                "Excel Modelling Certification"
            ],
            "level": "Mid-level",
            "type": "Investment"
        }
    ]
    
    # Training programs data
    training_programs = [
        {
            "name": "Advanced Python Programming",
            "skills": ["Python", "Object-Oriented Programming", "Python Libraries", "Testing"],
            "duration": "4 weeks",
            "level": "Intermediate",
            "description": "Covers advanced Python concepts, OOP, libraries, and testing best practices.",
            "type": "Digital Technology"
        },
        {
            "name": "Machine Learning Fundamentals",
            "skills": ["Python", "Statistics", "Machine Learning Algorithms", "Data Preprocessing"],
            "duration": "6 weeks",
            "level": "Beginner",
            "description": "Introduction to machine learning concepts, algorithms, and data preparation.",
            "type": "Digital Technology"
        },
        {
            "name": "Advanced Machine Learning",
            "skills": ["Deep Learning", "Neural Networks", "NLP", "Computer Vision"],
            "duration": "8 weeks",
            "level": "Advanced",
            "description": "Deep dive into advanced ML topics including deep learning, NLP, and computer vision.",
            "type": "Digital Technology"
        },
        {
            "name": "Cloud Architecture on Azure",
            "skills": ["Azure", "Cloud Architecture", "Serverless Computing", "Azure DevOps"],
            "duration": "6 weeks",
            "level": "Intermediate",
            "description": "Covers Azure cloud architecture, serverless, and DevOps practices.",
            "type": "Digital Technology"
        },
        {
            "name": "Leadership and Management",
            "skills": ["Team Management", "Leadership", "Conflict Resolution", "Performance Management"],
            "duration": "4 weeks",
            "level": "Intermediate",
            "description": "Develops leadership and management skills for team leads and managers.",
            "type": "Digital Technology"
        },
        {
            "name": "Agile Project Management",
            "skills": ["Agile Methodology", "Scrum", "Kanban", "Project Planning"],
            "duration": "3 weeks",
            "level": "Beginner",
            "description": "Introduction to Agile, Scrum, Kanban, and project planning techniques.",
            "type": "Digital Technology"
        },
        {
            "name": "Modern JavaScript and Frontend Frameworks",
            "skills": ["JavaScript", "React", "Vue.js", "Angular"],
            "duration": "5 weeks",
            "level": "Intermediate",
            "description": "Covers modern JavaScript and popular frontend frameworks.",
            "type": "Digital Technology"
        },
        {
            "name": "DevOps Practices and Tools",
            "skills": ["CI/CD", "Docker", "Kubernetes", "Infrastructure as Code"],
            "duration": "6 weeks",
            "level": "Intermediate",
            "description": "Explores DevOps tools and practices for automation and deployment.",
            "type": "Digital Technology"
        },
        {
            "name": "AWS Cloud Architecture",
            "skills": ["AWS Lambda", "AWS Services", "Cloud Design Patterns", "AWS Security"],
            "duration": "8 weeks",
            "level": "Advanced",
            "description": "Advanced AWS architecture, design patterns, and security.",
            "type": "Digital Technology"
        },
        {
            "name": "Microservices Architecture",
            "skills": ["API Design", "Service Mesh", "Event-Driven Architecture", "Containerization"],
            "duration": "6 weeks",
            "level": "Advanced",
            "description": "Design and implementation of microservices and containerized systems.",
            "type": "Digital Technology"
        },
        {
            "name": "Data Engineering Fundamentals",
            "skills": ["Apache Spark", "Data Pipelines", "ETL", "Data Warehousing"],
            "duration": "7 weeks",
            "level": "Intermediate",
            "description": "Fundamentals of data engineering, ETL, and big data tools.",
            "type": "Digital Technology"
        },
        {
            "name": "MLOps and AI Pipeline Development",
            "skills": ["MLflow", "Model Deployment", "Pipeline Automation", "Model Monitoring"],
            "duration": "5 weeks",
            "level": "Advanced",
            "description": "Covers MLOps practices for deploying and monitoring AI models.",
            "type": "Digital Technology"
        },
        {
            "name": "Advanced DevSecOps",
            "skills": ["Security Testing", "Compliance Automation", "Threat Modeling", "Security as Code"],
            "duration": "6 weeks",
            "level": "Advanced",
            "description": "Advanced security practices in DevOps pipelines.",
            "type": "Digital Technology"
        },
        {
            "name": "Enterprise API Development",
            "skills": ["RESTful Design", "GraphQL", "API Security", "API Gateway"],
            "duration": "4 weeks",
            "level": "Intermediate",
            "description": "Enterprise-level API design, security, and management.",
            "type": "Digital Technology"
        },
        {
            "name": "Cloud Native Development",
            "skills": ["Kubernetes", "Service Mesh", "Cloud Native Patterns", "Microservices"],
            "duration": "8 weeks",
            "level": "Advanced",
            "description": "Developing applications using cloud-native patterns and tools.",
            "type": "Digital Technology"
        },
        {
            "name": "Data Lake Implementation",
            "skills": ["Azure Data Lake", "Data Modeling", "Big Data Processing", "Data Governance"],
            "duration": "6 weeks",
            "level": "Advanced",
            "description": "Implementing and managing data lakes on Azure.",
            "type": "Digital Technology"
        },
        {
            "name": "Network Security Fundamentals",
            "skills": ["Network Protocols", "Firewall Configuration", "VPN Setup", "Network Monitoring"],
            "duration": "6 weeks",
            "level": "Intermediate",
            "description": "Covers network security basics, firewalls, and monitoring.",
            "type": "Digital Technology"
        },
        {
            "name": "Advanced Security Operations",
            "skills": ["SIEM Implementation", "Threat Hunting", "Incident Response", "Security Automation"],
            "duration": "8 weeks",
            "level": "Advanced",
            "description": "Advanced security operations, SIEM, and threat hunting.",
            "type": "Digital Technology"
        },
        {
            "name": "Enterprise Network Design",
            "skills": ["Network Architecture", "SDN", "Network Automation", "Performance Optimization"],
            "duration": "7 weeks",
            "level": "Advanced",
            "description": "Designing and optimizing enterprise networks.",
            "type": "Digital Technology"
        },
        {
            "name": "Cloud Security Architecture",
            "skills": ["AWS Security", "Azure Security", "Zero Trust", "Security Controls"],
            "duration": "6 weeks",
            "level": "Advanced",
            "description": "Cloud security architecture and zero trust principles.",
            "type": "Digital Technology"
        },
        {
            "name": "Penetration Testing Essentials",
            "skills": ["Vulnerability Assessment", "Ethical Hacking", "Security Tools", "Report Writing"],
            "duration": "8 weeks",
            "level": "Advanced",
            "description": "Essentials of penetration testing and ethical hacking.",
            "type": "Digital Technology"
        },
        {
            "name": "Security Automation with Python",
            "skills": ["Python Scripting", "Security Tools API", "Automation Frameworks", "Security Testing"],
            "duration": "5 weeks",
            "level": "Intermediate",
            "description": "Automating security tasks using Python scripting.",
            "type": "Digital Technology"
        },
        {
            "name": "Network Automation and Programmability",
            "skills": ["Network APIs", "Python for Networks", "Ansible", "Network CI/CD"],
            "duration": "6 weeks",
            "level": "Intermediate",
            "description": "Network automation using APIs, Python, and Ansible.",
            "type": "Digital Technology"
        },
        {
            "name": "CFA Exam Preparation Program",
            "skills": ["Ethical and Professional Standards", "Quantitative Methods", "Economics", "Financial Reporting and Analysis", "Equity Investments", "Fixed Income", "Portfolio Management", "Derivatives", "Alternative Investments"],
            "duration": "16 weeks",
            "level": "Advanced",
            "description": "Comprehensive preparation for all levels of the CFA exam.",
            "type": "Investment"
        },
        {
            "name": "Certificate in ESG Investing Bootcamp",
            "skills": ["ESG Fundamentals", "ESG Integration", "Sustainable Investing", "ESG Reporting", "ESG Risk Analysis"],
            "duration": "8 weeks",
            "level": "Intermediate",
            "description": "Intensive bootcamp for ESG investing and integration.",
            "type": "Investment"
        },
        {
            "name": "CIPM Certificate Training",
            "skills": ["Performance Measurement", "Performance Attribution", "GIPS Standards", "Risk-adjusted Returns", "Reporting and Compliance"],
            "duration": "6 weeks",
            "level": "Intermediate",
            "description": "Training for the CIPM certificate, focusing on performance measurement and attribution.",
            "type": "Investment"
        },
        {
            "name": "CAIA Level I Preparation Course",
            "skills": ["Alternative Investments", "Private Equity", "Real Assets", "Hedge Funds", "Structured Products"],
            "duration": "10 weeks",
            "level": "Intermediate",
            "description": "Preparation for CAIA Level I, covering alternative investments.",
            "type": "Investment"
        },
        {
            "name": "Investment Management Certificate (IMC) Revision Program",
            "skills": ["Investment Environment", "Asset Classes", "Portfolio Construction", "Regulation", "Ethics"],
            "duration": "8 weeks",
            "level": "Beginner",
            "description": "Revision program for IMC, covering investment environment and ethics.",
            "type": "Investment"
        },
        {
            "name": "Excel Modelling for Private Equity",
            "skills": ["LBO Modelling", "DCF Modelling", "Scenario Analysis", "Sensitivity Analysis", "Valuation Techniques"],
            "duration": "4 weeks",
            "level": "Intermediate",
            "description": "Excel modelling techniques for private equity professionals.",
            "type": "Investment"
        }
    ]
    
    # Secondment projects data
    secondment_projects = [
        {
            "name": "Customer Data Analytics Platform",
            "required_skills": ["Python", "Data Analysis", "SQL", "Visualization"],
            "duration": "3 months",
            "department": "Marketing Analytics",
            "goals": ["Implement predictive customer behavior models", "Design interactive dashboards"],
            "description": "Developed a platform for customer analytics and predictive modeling.",
            "type": "Digital Technology"
        },
        {
            "name": "Cloud Migration Initiative",
            "required_skills": ["Cloud Architecture", "AWS", "Azure", "Migration Strategy"],
            "duration": "6 months",
            "department": "IT Infrastructure",
            "goals": ["Migrate on-premise applications to cloud", "Implement cloud security best practices"],
            "description": "Led migration of legacy systems to cloud infrastructure.",
            "type": "Digital Technology"
        },
        {
            "name": "Mobile App Development",
            "required_skills": ["React Native", "JavaScript", "UI/UX Design", "API Integration"],
            "duration": "4 months",
            "department": "Digital Products",
            "goals": ["Develop cross-platform mobile application", "Implement offline functionality"],
            "description": "Developed a cross-platform mobile app with offline capabilities.",
            "type": "Digital Technology"
        },
        {
            "name": "AI Chatbot Implementation",
            "required_skills": ["NLP", "Python", "Azure Bot Service", "Conversation Design"],
            "duration": "3 months",
            "department": "Customer Support",
            "goals": ["Develop automated customer support chatbot", "Integrate with existing support systems"],
            "description": "Implemented an AI-powered chatbot for customer support.",
            "type": "Digital Technology"
        },
        {
            "name": "Data Governance Framework",
            "required_skills": ["Data Management", "Compliance", "Data Quality", "Documentation"],
            "duration": "5 months",
            "department": "Data Office",
            "goals": ["Design data governance policies", "Implement data quality monitoring"],
            "description": "Established data governance policies and quality monitoring.",
            "type": "Digital Technology"
        },
        {
            "name": "Agile Transformation",
            "required_skills": ["Agile Methodology", "Change Management", "Training", "Process Design"],
            "duration": "6 months",
            "department": "Project Management Office",
            "goals": ["Transform traditional processes to Agile", "Train teams on Agile practices"],
            "description": "Led Agile transformation and team training initiatives.",
            "type": "Digital Technology"
        },
        {
            "name": "Cloud-Native Platform Modernisation",
            "required_skills": ["AWS Lambda", "Docker", "Terraform", "React", "Node.js"],
            "duration": "9 months",
            "department": "Platform Engineering",
            "goals": ["Re-architect legacy system into microservices", "Implement serverless architecture"],
            "description": "Modernized legacy platform using microservices and serverless.",
            "type": "Digital Technology"
        },
        {
            "name": "Enterprise Data Lake and Analytics Hub",
            "required_skills": ["Azure Data Lake", "Spark", "Databricks", "Power BI"],
            "duration": "12 months",
            "department": "Data & Analytics",
            "goals": ["Build centralized data lakehouse", "Implement real-time business intelligence"],
            "description": "Built a centralized data lake and analytics hub for real-time BI.",
            "type": "Digital Technology"
        },
        {
            "name": "AI-Powered Predictive Maintenance System",
            "required_skills": ["Python", "TensorFlow", "Docker", "Kubernetes"],
            "duration": "8 months",
            "department": "IoT Solutions",
            "goals": ["Develop predictive analytics for equipment", "Implement industrial IoT monitoring"],
            "description": "Developed predictive maintenance using AI and IoT.",
            "type": "Digital Technology"
        },
        {
            "name": "Secure DevOps Automation Framework",
            "required_skills": ["GitHub Actions", "Terraform", "AWS CodePipeline", "OWASP ZAP"],
            "duration": "6 months",
            "department": "DevSecOps",
            "goals": ["Implement security-first CI/CD", "Automate vulnerability scanning"],
            "description": "Implemented secure DevOps automation and vulnerability scanning.",
            "type": "Digital Technology"
        },
        {
            "name": "Enterprise Network Security Transformation",
            "required_skills": ["Network Security", "Zero Trust", "SIEM", "Firewall Management"],
            "duration": "9 months",
            "department": "Network Security",
            "goals": ["Implement Zero Trust architecture", "Enhance network monitoring and threat detection"],
            "description": "Transformed enterprise network security with Zero Trust and SIEM.",
            "type": "Digital Technology"
        },
        {
            "name": "Security Operations Center Modernization",
            "required_skills": ["SIEM", "Security Automation", "Incident Response", "Threat Intelligence"],
            "duration": "8 months",
            "department": "Security Operations",
            "goals": ["Modernize SOC infrastructure", "Implement automated incident response"],
            "description": "Modernized SOC with automation and threat intelligence.",
            "type": "Digital Technology"
        },
        {
            "name": "ESG Investment Strategy Implementation",
            "required_skills": ["ESG Integration", "Sustainable Investing", "Portfolio Construction", "Stakeholder Reporting"],
            "duration": "6 months",
            "department": "Investment Management",
            "goals": ["Develop and implement ESG-focused investment strategies", "Integrate ESG data into portfolio analytics", "Prepare ESG impact reports for clients"],
            "description": "Developed and implemented ESG investment strategies and reporting.",
            "type": "Investment"
        },
        {
            "name": "Private Equity Fund Launch Support",
            "required_skills": ["Deal Sourcing", "Due Diligence", "Financial Modelling (LBO, DCF)", "Data Room Management"],
            "duration": "9 months",
            "department": "Private Markets",
            "goals": ["Support the launch of a new private equity fund", "Coordinate due diligence and deal screening", "Develop investment memos and support fundraising"],
            "description": "Supported private equity fund launch, due diligence, and fundraising.",
            "type": "Investment"
        },
        {
            "name": "Investment Performance Attribution Enhancement",
            "required_skills": ["Performance Measurement", "CIPM Standards", "Risk-adjusted Returns", "Reporting Automation"],
            "duration": "5 months",
            "department": "Performance & Analytics",
            "goals": ["Automate performance attribution reporting", "Enhance risk-adjusted return analysis", "Align reporting with GIPS standards"],
            "description": "Enhanced investment performance attribution and reporting automation.",
            "type": "Investment"
        },
        {
            "name": "Alternative Investments Platform Integration",
            "required_skills": ["Alternative Investments", "System Implementation", "Process Automation", "Stakeholder Communication"],
            "duration": "7 months",
            "department": "Operations & Technology",
            "goals": ["Integrate new alternative investments platform", "Automate fund accounting and reconciliation", "Train team on new workflows"],
            "description": "Integrated alternative investments platform and automated workflows.",
            "type": "Investment"
        },
        {
            "project_name": "Multi-Asset Portfolio Optimisation Initiative",
            "technologies": [
                "Excel VBA",
                "Python",
                "Aladdin"
            ],
            "description": "Developing advanced risk-return models and portfolio optimisation tools for institutional clients.",
            "estimated_duration_months": 7,
            "type": "Investment"
        },
        {
            "project_name": "Emerging Markets Equity Research Expansion",
            "technologies": [
                "Bloomberg Terminal",
                "FactSet",
                "Excel Modelling"
            ],
            "description": "Establishing new equity research coverage in emerging market sectors and integrating ESG metrics.",
            "estimated_duration_months": 10,
            "type": "Investment"
        },
        {
            "project_name": "Fixed Income Credit Risk Assessment Framework",
            "technologies": [
                "Power BI",
                "Python"
            ],
            "description": "Building a new credit risk model and reporting framework for fixed income investments.",
            "estimated_duration_months": 6,
            "type": "Investment"
        },
        {
            "project_name": "AI-Powered Market Sentiment Analysis Tool",
            "technologies": [
                "Python",
                "Natural Language Processing (NLP)"
            ],
            "description": "Implementing AI-driven sentiment analysis for market insights and trade ideas.",
            "estimated_duration_months": 8,
            "type": "Investment"
        }
    ]
    
    return job_roles, training_programs, secondment_projects


skills_definition_dnt ={  
  "skills_rating_definition": {  
    "Zscaler": {  
      "1": "Beginner: Has heard of Zscaler, basic understanding of its purpose.",  
      "2": "Novice: Can navigate the Zscaler interface, perform simple configurations.",  
      "3": "Intermediate: Can manage user policies, troubleshoot common issues.",  
      "4": "Advanced: Designs security policies, integrates Zscaler with other systems, mentors others.",  
      "5": "Expert: Provides strategic guidance on Zscaler deployments, implements advanced features, resolves complex technical issues."  
    },  
    "Zimperium": {  
      "1": "Beginner: Familiar with Zimperium as a mobile security platform.",  
      "2": "Novice: Can install and configure basic Zimperium settings.",  
      "3": "Intermediate: Manages policies, monitors threats, performs basic troubleshooting.",  
      "4": "Advanced: Integrates with MDMs, customizes alerts and policies, leads deployments.",  
      "5": "Expert: Architects organization-wide solutions, resolves escalated issues, optimizes implementation."  
    },  
    "Workday Studio (Configure, Manage & Support)": {  
      "1": "Beginner: Aware of Workday Studio's existence, basic navigation.",  
      "2": "Novice: Can perform simple configurations or support tasks with guidance.",  
      "3": "Intermediate: Independently configures integrations, monitors and manages processes.",  
      "4": "Advanced: Designs complex workflows, resolves advanced issues, trains others.",  
      "5": "Expert: Architect-level knowledge, leads projects, defines best practices for large-scale deployments."  
    },  
    "Waterfall Project Management": {  
      "1": "Beginner: Understands basics of the waterfall model.",  
      "2": "Novice: Participates in waterfall projects, follows processes.",  
      "3": "Intermediate: Manages small projects, applies methodology with some independence.",  
      "4": "Advanced: Leads large projects, optimizes processes, handles complex dependencies.",  
      "5": "Expert: Strategic expert, consults on best practices, innovates in waterfall methodology."  
    },  
    "SuccessFactors (Configure, Manage & Support)": {  
      "1": "Beginner: Basic knowledge of SuccessFactors modules.",  
      "2": "Novice: Can perform entry-level support, changes to user data.",  
      "3": "Intermediate: Configures modules, manages workflows, resolves common issues.",  
      "4": "Advanced: Customizes system for business needs, handles integrations.",  
      "5": "Expert: Designs architectures, resolves the most complex technical and business challenges."  
    },  
    "Structured Thinking and Presentation": {  
      "1": "Beginner: Can organize thoughts simply, limited in presentation.",  
      "2": "Novice: Creates basic organized outlines and simple presentations.",  
      "3": "Intermediate: Structures and presents information clearly, adapts to audience feedback.",  
      "4": "Advanced: Distills complex ideas into compelling stories, uses visuals effectively.",  
      "5": "Expert: Exceptionally clear and persuasive communicator, influences important decisions."  
    },  
    "Stakeholder Management": {  
      "1": "Beginner: Aware of who stakeholders are, limited interaction.",  
      "2": "Novice: Interacts with stakeholders with support, maintains basic relationships.",  
      "3": "Intermediate: Manages relationships, balances competing interests, effective communication.",  
      "4": "Advanced: Resolves conflicts, influences outcomes, drives stakeholder engagement.",  
      "5": "Expert: Builds strategic alliances, manages highly complex or sensitive relationships."  
    },  
    "SQL": {  
      "1": "Beginner: Can write simple SELECT queries.",  
      "2": "Novice: Modifies basic queries, uses WHERE, GROUP BY, and simple joins.",  
      "3": "Intermediate: Writes complex queries, understands indexing, subqueries, and optimization.",  
      "4": "Advanced: Designs database schemas, optimizes performance, implements advanced features.",  
      "5": "Expert: Deep expertise in database architecture, tuning and query optimization at scale."  
    },  
    "Simcorp (Configure, Manage & Support)": {  
      "1": "Beginner: Aware of Simcorp as a financial platform.",  
      "2": "Novice: Can perform basic configurations or tasks with guidance.",  
      "3": "Intermediate: Manages multiple modules, customizes settings, troubleshoots issues.",  
      "4": "Advanced: Leads implementations, resolves advanced technical and functional issues.",  
      "5": "Expert: Provides strategic advice, optimizes and extends the platform for complex needs."  
    },  
    "Risk Management Fundamentals": {  
      "1": "Beginner: Basic understanding of risk management concepts.",  
      "2": "Novice: Identifies simple risks, uses checklists.",  
      "3": "Intermediate: Assesses risks systematically, develops mitigation strategies.",  
      "4": "Advanced: Implements risk frameworks, manages risk at project/organizational level.",  
      "5": "Expert: Defines risk strategy, manages enterprise risk portfolios."  
    },  
    "React JS": {  
      "1": "Beginner: Basic understanding of React and component structure.",  
      "2": "Novice: Creates simple components, manages state.",  
      "3": "Intermediate: Builds dynamic applications, handles routing, uses hooks.",  
      "4": "Advanced: Optimizes performance, manages complex state, uses context, mentors others.",  
      "5": "Expert: Creates scalable architectures, contributes to open source, solves advanced problems."  
    },  
    "Python": {  
      "1": "Beginner: Writes simple scripts, understands basic syntax.",  
      "2": "Novice: Uses standard libraries, writes basic functions and loops.",  
      "3": "Intermediate: Implements object-oriented programming, uses packages, handles exceptions.",  
      "4": "Advanced: Develops complex applications, optimizes code, contributes to libraries.",  
      "5": "Expert: Deep mastery, develops libraries/frameworks, optimizes for large-scale systems."  
    },  
    "Outsystems": {  
      "1": "Beginner: Understands Outsystems platform fundamentals.",  
      "2": "Novice: Can build simple apps or workflows.",  
      "3": "Intermediate: Develops moderate applications, integrates basic APIs, resolves common issues.",  
      "4": "Advanced: Designs enterprise solutions, manages advanced integrations and performance tuning.",  
      "5": "Expert: Leads architecture, maximizes platform capabilities, resolves critical issues."  
    },  
    "Microsoft Power Platform": {  
      "1": "Beginner: Familiar with platform and its components (Power BI, Power Apps, Power Automate).",  
      "2": "Novice: Builds simple flows and apps, connects to basic data sources.",  
      "3": "Intermediate: Automates workflows, builds dashboards, integrates data sources.",  
      "4": "Advanced: Develops enterprise solutions, implements advanced workflows, mentors users.",  
      "5": "Expert: Defines data strategy, architects large-scale deployments, solves complex integration challenges."  
    },  
    "Microsoft Power BI Data Analyst": {  
      "1": "Beginner: Creates basic reports and visualizations.",  
      "2": "Novice: Uses data modeling, basic DAX, shares dashboards.",  
      "3": "Intermediate: Performs advanced analytics, custom calculations, manages workspaces.",  
      "4": "Advanced: Optimizes data models, leads data projects, implements security.",  
      "5": "Expert: Designs BI strategies, architects enterprise solutions, teaches and mentors others."  
    },  
    "Microsoft Azure Security": {  
      "1": "Beginner: Recognizes Azure security features and concepts.",  
      "2": "Novice: Configures basic security settings (e.g., user roles).",  
      "3": "Intermediate: Implements security best practices, manages compliance, monitors threats.",  
      "4": "Advanced: Designs secure solutions, manages identity, responds to incidents.",  
      "5": "Expert: Advises on security strategy, implements cutting-edge solutions, audits and remediates threats at enterprise scale."  
    },  
    "Microsoft Azure Administrator": {  
      "1": "Beginner: Navigates the Azure Portal, basic understanding of services.",  
      "2": "Novice: Creates and configures basic resources (VMs, storage, networking).",  
      "3": "Intermediate: Manages deployments, automates tasks, monitors environments.",  
      "4": "Advanced: Designs architectures, optimizes performance, handles scaling and disaster recovery.",  
      "5": "Expert: Provides strategic guidance, leads enterprise rollouts, integrates hybrid/cloud environments."  
    },  
    "Microsoft 365 Fundamentals (Foundational-level knowledge of Microsoft 365 solutions to facilitate productivity and collaboration among the users)": {  
      "1": "Beginner: Knows Microsoft 365 products and their general purpose.",  
      "2": "Novice: Can access and use primary features (Outlook, Teams, OneDrive).",  
      "3": "Intermediate: Integrates applications, manages settings, supports end users.",  
      "4": "Advanced: Manages security/compliance, supports large groups/offices.",  
      "5": "Expert: Plans rollouts, optimizes configurations, trains and supports complex deployments."  
    },  
    "Managing Microsoft Teams": {  
      "1": "Beginner: Joins or creates basic Teams, starts chats and calls.",  
      "2": "Novice: Schedules meetings, creates channels, shares files.",  
      "3": "Intermediate: Manages team settings, permissions, and integrations.",  
      "4": "Advanced: Supports organization-wide adoption, enforces policies, manages lifecycle.",  
      "5": "Expert: Architects Teams strategy, implements solutions for complex organizations."  
    },  
    "Manage Engine Service Desk Plus": {  
      "1": "Beginner: Uses portal, logs tickets, familiar with interface.",  
      "2": "Novice: Manages basic tickets, performs simple configurations.",  
      "3": "Intermediate: Customizes workflows, manages automations, generates reports.",  
      "4": "Advanced: Integrates with other tools, implements advanced features, troubleshoots complex issues.",  
      "5": "Expert: Optimizes Service Desk operations, defines best practices, leads training."  
    },  
    "Java Script Framework (VUE)": {  
      "1": "Beginner: Basic understanding of Vue.js concepts.",  
      "2": "Novice: Writes simple components, handles events and data binding.",  
      "3": "Intermediate: Builds full applications, manages state, handles routing and APIs.",  
      "4": "Advanced: Optimizes performance, scales apps, mentors others.",  
      "5": "Expert: Contributes to framework, architects large-scale projects, solves advanced technical problems."  
    },   
    "Information Technology Fundamentals": {  
      "1": "Beginner: Recognizes key IT concepts and terminology.",  
      "2": "Novice: Can perform basic IT tasks, understands simple networks.",  
      "3": "Intermediate: Troubleshoots common issues, supports users.",  
      "4": "Advanced: Manages systems, ensures security and reliability.",  
      "5": "Expert: Designs IT infrastructure, leads projects, innovates in IT operations."  
    },  
    "Informatica (Configure, Manage & Support)": {  
      "1": "Beginner: Understands Informatica's core components.",  
      "2": "Novice: Performs basic ETL configurations and jobs.",  
      "3": "Intermediate: Builds workflows, manages data integrations, troubleshoots jobs.",  
      "4": "Advanced: Leads data migration projects, customizes advanced transformations.",  
      "5": "Expert: Architects enterprise ETL solutions, resolves complex performance challenges."  
    },  
    "Develop Strategic Planning / KPI": {  
      "1": "Beginner: Recognizes the purpose of planning and KPIs.",  
      "2": "Novice: Contributes to planning sessions, understands basic KPIs.",  
      "3": "Intermediate: Develops plans, defines and monitors KPIs for projects.",  
      "4": "Advanced: Aligns KPIs with strategy, analyzes results, drives improvements.",  
      "5": "Expert: Implements planning frameworks, leads strategy at organizational level."  
    },  
    "DealCloud (Configure, Manage & Support)": {  
      "1": "Beginner: Understands DealCloud's purpose in deal management.",  
      "2": "Novice: Manages simple records and basic configurations.",  
      "3": "Intermediate: Configures workflows, supports users, troubleshoots issues.",  
      "4": "Advanced: Customizes the platform, integrates with other systems, trains users.",  
      "5": "Expert: Architects complex DealCloud solutions, leads large implementations."  
    },  
    "Data Story Telling": {  
      "1": "Beginner: Presents data in basic tables or charts.",  
      "2": "Novice: Selects basic visuals to highlight trends or key points.",  
      "3": "Intermediate: Crafts coherent narratives with visuals for diverse audiences.",  
      "4": "Advanced: Adapts stories to stakeholder needs, influences decisions.",  
      "5": "Expert: Drives organizational change with persuasive, actionable data stories."  
    },  
    "Data Analytics Fundamentals": {  
      "1": "Beginner: Knows basic analytics concepts and terminology.",  
      "2": "Novice: Uses basic analytic tools, interprets straightforward results.",  
      "3": "Intermediate: Analyzes datasets, identifies trends and patterns.",  
      "4": "Advanced: Conducts advanced analyses, applies statistical models.",  
      "5": "Expert: Innovates analytic techniques, leads major analytic initiatives."  
    },  
    "Cyber Security Operation Center (CSOC)": {  
      "1": "Beginner: Aware of CSOC function.",  
      "2": "Novice: Monitors basic security events, reports simple issues.",  
      "3": "Intermediate: Analyzes alerts, handles incidents, applies procedures.",  
      "4": "Advanced: Leads incident response, refines processes, mentors team.",  
      "5": "Expert: Defines CSOC strategy, manages critical incidents, innovates defense techniques."  
    },  
    "CrowdStrike": {  
      "1": "Beginner: Recognizes CrowdStrike’s endpoint protection.",  
      "2": "Novice: Monitors endpoints, understands alert interface.",  
      "3": "Intermediate: Investigates and responds to incidents, configures policies.",  
      "4": "Advanced: Designs deployment architecture, implements advanced threat hunting.",  
      "5": "Expert: Leads organization-wide deployments, directs custom threat intelligence."  
    },  
    "Concur (Configure, Manage & Support)": {  
      "1": "Beginner: Recognizes Concur for expense management.",  
      "2": "Novice: Processes basic reports, manages simple workflows.",  
      "3": "Intermediate: Configures policies, supports integrations, troubleshoots issues.",  
      "4": "Advanced: Optimizes system usage, trains users, manages complex workflows.",  
      "5": "Expert: Leads large-scale implementations, customizes for organizational needs."  
    },  
    "Comptia Security+ Certification": {  
      "1": "Beginner: Knows Security+ exam syllabus topics.",  
      "2": "Novice: Possesses basic understanding of security concepts.",  
      "3": "Intermediate: Applies Security+ knowledge to tasks, solves standard scenarios.",  
      "4": "Advanced: Mentors others, applies Security+ concepts in advanced troubleshooting.",  
      "5": "Expert: Recognized authority on Security+, leads security initiatives."  
    },  
    "Communicating with Executive Presence": {  
      "1": "Beginner: Delivers clear information, lacks confidence in front of executives.",  
      "2": "Novice: Communicates effectively but needs support in high-pressure settings.",  
      "3": "Intermediate: Commands attention and respect, adapts style for leaders.",  
      "4": "Advanced: Influences decisions, handles challenging questions with ease.",  
      "5": "Expert: Sets communication standards, inspires and leads executive conversations."  
    },  
    "Charles River Development (CRD) - Configure, Manage & Support": {  
      "1": "Beginner: Familiar with CRD’s purpose in financial management.",  
      "2": "Novice: Performs simple tasks or configurations.",  
      "3": "Intermediate: Supports users, configures modules, troubleshoots issues.",  
      "4": "Advanced: Customizes workflows, integrates CRD with other platforms.",  
      "5": "Expert: Architects end-to-end solutions, leads large-scale implementations."  
    },  
    "Certified Information Security Manager Certification": {  
      "1": "Beginner: Has basic awareness of CISM domains.",  
      "2": "Novice: Understands risk and governance concepts.",  
      "3": "Intermediate: Applies CISM practices, manages small projects.",  
      "4": "Advanced: Implements and oversees security management programs.",  
      "5": "Expert: Is a thought leader in information security management, shapes policy."  
    },  
    "Certified Ethical Hacker": {  
      "1": "Beginner: Understands what ethical hacking is.",  
      "2": "Novice: Uses basic tools for vulnerability scanning.",  
      "3": "Intermediate: Conducts penetration tests, documents findings.",  
      "4": "Advanced: Leads red and blue team exercises, develops new tools.",  
      "5": "Expert: Recognized cybersecurity authority, innovates ethical hacking methodologies."  
    },  
    "Business Analyst Foundation": {  
      "1": "Beginner: Aware of business analysis principles.",  
      "2": "Novice: Participates in requirements gathering, uses standard templates.",  
      "3": "Intermediate: Guides stakeholders, develops process maps, analyzes data.",  
      "4": "Advanced: Facilitates workshops, mentors analysts, leads complex initiatives.",  
      "5": "Expert: Thought leader in business analysis, develops methodologies."  
    },  
    "Budget Management Fundamentals": {  
      "1": "Beginner: Recognizes principles of budgeting.",  
      "2": "Novice: Tracks simple budgets, performs basic calculations.",  
      "3": "Intermediate: Prepares, manages, and monitors budgets with some autonomy.",  
      "4": "Advanced: Optimizes budget processes, creates forecasts, analyzes variances.",  
      "5": "Expert: Leads strategic budgeting, advises executives."  
    },  
    "AWS Technical Essentials": {  
      "1": "Beginner: Knows basic AWS service names and their purpose.",  
      "2": "Novice: Launches and manages basic AWS resources.",  
      "3": "Intermediate: Builds scalable solutions, implements basic security.",  
      "4": "Advanced: Designs enterprise-level architectures, optimizes AWS cost/performance.",  
      "5": "Expert: Strategic expert, manages multi-account environments, sets AWS standards."  
    },  
    "AI Fundamentals": {  
      "1": "Beginner: Aware of AI concepts and common use cases.",  
      "2": "Novice: Understands types of AI, basic algorithms.",  
      "3": "Intermediate: Applies AI concepts to simple projects, interprets results.",  
      "4": "Advanced: Designs and trains basic models, explains AI decisions.",  
      "5": "Expert: Innovates algorithms, leads complex AI projects."  
    },  
    "Agile Project Management": {  
      "1": "Beginner: Knows Agile principles and roles.",  
      "2": "Novice: Participates in sprints, uses scrum boards.",  
      "3": "Intermediate: Facilitates Agile ceremonies, manages backlogs.",  
      "4": "Advanced: Coaches teams, adapts frameworks, optimizes delivery.",  
      "5": "Expert: Leads Agile transformations, shapes organizational culture."  
    }

}}

skills_definition_iv ={  
  "skills_rating_definition": {  
    "Accounting Fundamentals (CFI Certification)": {  
      "1": "Beginner: Recognizes core accounting concepts.",  
      "2": "Novice: Records simple transactions, prepares basic statements.",  
      "3": "Intermediate: Interprets financial data, manages ledgers.",  
      "4": "Advanced: Analyzes statements, ensures compliance, supports audits.",  
      "5": "Expert: Provides strategic financial advice, leads accounting policy."  
    },
    "Equity Research and Valuation": {
      "1": "Beginner: Understands basic equity concepts and valuation methods.",
      "2": "Novice: Can perform simple equity analysis and use basic valuation models.",
      "3": "Intermediate: Conducts detailed equity research, applies DCF and comparable analysis.",
      "4": "Advanced: Leads equity research projects, builds complex valuation models, mentors others.",
      "5": "Expert: Recognized authority, innovates valuation techniques, presents to investment committees."
    },
    "Fixed Income and Credit Analysis": {
      "1": "Beginner: Knows basic fixed income instruments and credit concepts.",
      "2": "Novice: Can analyze simple bond structures and credit ratings.",
      "3": "Intermediate: Performs credit risk analysis, models fixed income portfolios.",
      "4": "Advanced: Leads credit research, develops risk frameworks, mentors team.",
      "5": "Expert: Sets credit policy, innovates risk models, presents to senior stakeholders."
    },
    "Financial Modelling (DCF, LBO, M&A)": {
      "1": "Beginner: Understands the purpose of financial models.",
      "2": "Novice: Can use basic Excel models for DCF or simple scenarios.",
      "3": "Intermediate: Builds DCF, LBO, and M&A models for investment analysis.",
      "4": "Advanced: Designs complex, dynamic models, reviews others' work, automates processes.",
      "5": "Expert: Develops new modelling standards, trains teams, leads model audit and validation."
    },
    "Portfolio Construction and Risk Management": {
      "1": "Beginner: Knows portfolio basics and risk concepts.",
      "2": "Novice: Assists in portfolio monitoring and simple risk calculations.",
      "3": "Intermediate: Constructs portfolios, applies risk metrics, rebalances assets.",
      "4": "Advanced: Designs portfolio strategies, optimizes risk-return, mentors others.",
      "5": "Expert: Leads portfolio strategy, innovates risk frameworks, presents to boards."
    },
    "Macroeconomic and Market Analysis": {
      "1": "Beginner: Understands macroeconomic indicators and market basics.",
      "2": "Novice: Tracks economic data, summarizes market trends.",
      "3": "Intermediate: Analyzes macro trends, forecasts market movements.",
      "4": "Advanced: Leads economic research, develops market outlooks, mentors team.",
      "5": "Expert: Sets economic strategy, presents to investment committees, recognized as thought leader."
    },
    "ESG Integration": {
      "1": "Beginner: Aware of ESG concepts and terminology.",
      "2": "Novice: Applies basic ESG screens to investments.",
      "3": "Intermediate: Integrates ESG data into analysis, prepares ESG reports.",
      "4": "Advanced: Designs ESG frameworks, leads integration projects, mentors others.",
      "5": "Expert: Sets ESG policy, innovates integration methods, presents to clients and boards."
    },
    "Client and Stakeholder Reporting": {
      "1": "Beginner: Prepares simple reports for clients or stakeholders.",
      "2": "Novice: Assists in preparing presentations and regular updates.",
      "3": "Intermediate: Develops detailed reports, tailors content to audience.",
      "4": "Advanced: Leads reporting processes, ensures compliance, mentors team.",
      "5": "Expert: Sets reporting standards, innovates communication, presents to senior stakeholders."
    },
    "Investment Committee Presentation Skills": {
      "1": "Beginner: Understands the basics of investment committee meetings.",
      "2": "Novice: Supports preparation of materials for committee.",
      "3": "Intermediate: Presents analysis to committee, answers questions.",
      "4": "Advanced: Leads presentations, manages Q&A, mentors others.",
      "5": "Expert: Sets presentation standards, recognized for clarity and influence."
    },
    "Bloomberg Terminal and FactSet Expertise": {
      "1": "Beginner: Can log in and navigate basic functions.",
      "2": "Novice: Uses Bloomberg/FactSet for data retrieval and simple analysis.",
      "3": "Intermediate: Performs advanced queries, builds custom screens and reports.",
      "4": "Advanced: Automates workflows, integrates data, mentors others.",
      "5": "Expert: Develops best practices, trains teams, innovates data usage."
    },
    "Team Mentoring and Leadership": {
      "1": "Beginner: Participates in team activities, observes leaders.",
      "2": "Novice: Assists peers, shares knowledge informally.",
      "3": "Intermediate: Mentors junior staff, leads small teams or projects.",
      "4": "Advanced: Leads teams, develops talent, manages performance.",
      "5": "Expert: Sets leadership standards, recognized for team development and culture."
    },
    "Trade Settlement and Reconciliation": {
      "1": "Beginner: Understands trade lifecycle basics.",
      "2": "Novice: Assists with simple settlements and reconciliations.",
      "3": "Intermediate: Manages daily settlements, resolves discrepancies.",
      "4": "Advanced: Optimizes processes, leads reconciliation projects, mentors others.",
      "5": "Expert: Sets policy, innovates settlement processes, recognized for accuracy and efficiency."
    },
    "Fund Accounting": {
      "1": "Beginner: Knows basic fund accounting principles.",
      "2": "Novice: Assists with NAV calculations and reporting.",
      "3": "Intermediate: Manages fund accounting processes, prepares financial statements.",
      "4": "Advanced: Leads fund audits, optimizes accounting workflows, mentors team.",
      "5": "Expert: Sets accounting policy, innovates processes, recognized for expertise."
    },
    "Regulatory Reporting": {
      "1": "Beginner: Understands regulatory requirements for investment reporting.",
      "2": "Novice: Assists in preparing regulatory filings.",
      "3": "Intermediate: Prepares and reviews reports, ensures compliance.",
      "4": "Advanced: Leads regulatory projects, manages audits, mentors others.",
      "5": "Expert: Sets reporting policy, innovates compliance processes, recognized by regulators."
    },
    "Custodian and Counterparty Management": {
      "1": "Beginner: Knows the role of custodians and counterparties.",
      "2": "Novice: Assists with account setup and basic communications.",
      "3": "Intermediate: Manages relationships, resolves issues, ensures compliance.",
      "4": "Advanced: Leads negotiations, optimizes processes, mentors team.",
      "5": "Expert: Sets relationship strategy, recognized for expertise and influence."
    },
    "Process Automation": {
      "1": "Beginner: Understands the basics of automation in investment operations.",
      "2": "Novice: Uses simple automation tools (e.g., Excel macros).",
      "3": "Intermediate: Designs and implements automation for routine tasks.",
      "4": "Advanced: Leads automation projects, integrates systems, mentors others.",
      "5": "Expert: Sets automation strategy, innovates solutions, recognized for efficiency gains."
    },
    "Risk and Compliance Oversight": {
      "1": "Beginner: Knows basic risk and compliance concepts.",
      "2": "Novice: Assists with compliance checks and risk reviews.",
      "3": "Intermediate: Manages compliance processes, monitors risk metrics.",
      "4": "Advanced: Leads risk and compliance projects, mentors others.",
      "5": "Expert: Sets policy, innovates frameworks, recognized for risk management expertise."
    },
    "Performance Measurement": {
      "1": "Beginner: Understands performance measurement basics.",
      "2": "Novice: Assists with data collection and simple calculations.",
      "3": "Intermediate: Calculates returns, prepares performance reports.",
      "4": "Advanced: Leads performance analysis, optimizes reporting, mentors team.",
      "5": "Expert: Sets measurement standards, innovates analysis, recognized for expertise."
    },
    "Cash Management": {
      "1": "Beginner: Knows cash management basics.",
      "2": "Novice: Assists with cash flow tracking and simple reconciliations.",
      "3": "Intermediate: Manages cash positions, forecasts needs.",
      "4": "Advanced: Optimizes cash management, leads projects, mentors others.",
      "5": "Expert: Sets policy, innovates cash strategies, recognized for expertise."
    },
    "System Implementation": {
      "1": "Beginner: Understands the basics of investment systems.",
      "2": "Novice: Assists with system setup and user support.",
      "3": "Intermediate: Manages system rollouts, customizes workflows.",
      "4": "Advanced: Leads implementations, integrates platforms, mentors team.",
      "5": "Expert: Sets system strategy, innovates solutions, recognized for expertise."
    },
    "Deal Sourcing and Screening": {
      "1": "Beginner: Knows the basics of deal sourcing.",
      "2": "Novice: Assists with market research and initial screening.",
      "3": "Intermediate: Sources deals, conducts screening, prepares summaries.",
      "4": "Advanced: Leads sourcing strategy, manages pipeline, mentors team.",
      "5": "Expert: Sets sourcing standards, recognized for deal origination expertise."
    },
    "Due Diligence": {
      "1": "Beginner: Understands due diligence basics.",
      "2": "Novice: Assists with data collection and checklists.",
      "3": "Intermediate: Conducts due diligence, prepares reports.",
      "4": "Advanced: Leads due diligence teams, manages complex reviews, mentors others.",
      "5": "Expert: Sets due diligence policy, innovates processes, recognized for expertise."
    },
    "Industry and Market Research": {
      "1": "Beginner: Knows basic industry and market research concepts.",
      "2": "Novice: Assists with data gathering and simple analysis.",
      "3": "Intermediate: Conducts research, prepares industry reports.",
      "4": "Advanced: Leads research projects, develops insights, mentors team.",
      "5": "Expert: Sets research standards, recognized for market expertise."
    },
    "Portfolio Monitoring": {
      "1": "Beginner: Understands portfolio monitoring basics.",
      "2": "Novice: Assists with data collection and reporting.",
      "3": "Intermediate: Monitors portfolio performance, identifies issues.",
      "4": "Advanced: Leads monitoring processes, optimizes reporting, mentors others.",
      "5": "Expert: Sets monitoring standards, innovates tools, recognized for expertise."
    },
    "Investment Memo Preparation": {
      "1": "Beginner: Knows the purpose of investment memos.",
      "2": "Novice: Assists with memo drafting and data collection.",
      "3": "Intermediate: Prepares investment memos, tailors content to audience.",
      "4": "Advanced: Leads memo preparation, reviews others' work, mentors team.",
      "5": "Expert: Sets memo standards, recognized for clarity and influence."
    },
    "Valuation Analysis": {
      "1": "Beginner: Understands basic valuation concepts.",
      "2": "Novice: Assists with data collection and simple models.",
      "3": "Intermediate: Performs valuation analysis, builds models.",
      "4": "Advanced: Leads valuation projects, reviews others' work, mentors team.",
      "5": "Expert: Sets valuation standards, innovates techniques, recognized for expertise."
    },
    "Stakeholder Communication": {
      "1": "Beginner: Knows basics of stakeholder communication.",
      "2": "Novice: Assists with meeting preparation and follow-ups.",
      "3": "Intermediate: Communicates with stakeholders, prepares updates.",
      "4": "Advanced: Leads communication strategy, manages complex relationships, mentors others.",
      "5": "Expert: Sets communication standards, recognized for influence and clarity."
    },
    "Data Room Management": {
      "1": "Beginner: Understands the basics of data rooms.",
      "2": "Novice: Assists with data uploads and access management.",
      "3": "Intermediate: Manages data rooms, ensures compliance and security.",
      "4": "Advanced: Leads data room projects, optimizes processes, mentors others.",
      "5": "Expert: Sets data room policy, innovates solutions, recognized for expertise."
    },
    "Exit Strategy Analysis": {
      "1": "Beginner: Knows basic exit strategies.",
      "2": "Novice: Assists with data collection and simple analysis.",
      "3": "Intermediate: Analyzes exit options, prepares recommendations.",
      "4": "Advanced: Leads exit analysis, reviews others' work, mentors team.",
      "5": "Expert: Sets exit strategy standards, recognized for expertise and innovation."
    },
    "Alternative Investments": {
      "1": "Beginner: Understands the basics of alternative investments.",
      "2": "Novice: Assists with data collection and simple analysis.",
      "3": "Intermediate: Analyzes alternative investment opportunities, prepares reports.",
      "4": "Advanced: Leads alternative investment projects, mentors team.",
      "5": "Expert: Sets strategy, innovates approaches, recognized for expertise."
    },
       "Investment Foundations": {  
      "1": "Beginner: Aware of core investment concepts.",  
      "2": "Novice: Understands financial instruments and market basics.",  
      "3": "Intermediate: Applies investment principles in analysis or reporting.",  
      "4": "Advanced: Makes informed investment decisions, mentors others.",  
      "5": "Expert: Provides strategic investment advice, leads educational efforts."  
    }, 
  }  
}

