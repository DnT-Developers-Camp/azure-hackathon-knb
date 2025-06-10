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
        },
        {
            "title": "Senior Digital & Technology Specialist",
            "required_skills": ["Cloud Architecture", "Microservices", "CI/CD", "Full-Stack Development", "Data Engineering"],
            "preferred_skills": ["AWS Solutions Architect", "Azure Solutions Architect", "Kubernetes", "Terraform", "Scrum Master"],
            "level": "Senior"
        },
        {
            "title": "Cybersecurity Engineer",
            "required_skills": ["Network Security", "Security Operations", "Incident Response", "Security Tools", "Vulnerability Assessment"],
            "preferred_skills": ["CISSP", "CEH", "Python", "Cloud Security", "Security Architecture"],
            "level": "Senior"
        },
        {
            "title": "Network Engineer",
            "required_skills": ["Network Protocols", "Routing & Switching", "Network Security", "Troubleshooting", "Network Design"],
            "preferred_skills": ["CCNP", "Network Automation", "SDN", "Cloud Networking", "Python"],
            "level": "Mid-level"
        },
        {
            "title": "Security Operations Analyst",
            "required_skills": ["SIEM", "Threat Detection", "Security Monitoring", "Incident Response", "Log Analysis"],
            "preferred_skills": ["Security+", "SIEM Tools", "Threat Intelligence", "Forensics", "Automation"],
            "level": "Mid-level"
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
        },
        {
            "name": "AWS Cloud Architecture",
            "skills": ["AWS Lambda", "AWS Services", "Cloud Design Patterns", "AWS Security"],
            "duration": "8 weeks",
            "level": "Advanced"
        },
        {
            "name": "Microservices Architecture",
            "skills": ["API Design", "Service Mesh", "Event-Driven Architecture", "Containerization"],
            "duration": "6 weeks",
            "level": "Advanced"
        },
        {
            "name": "Data Engineering Fundamentals",
            "skills": ["Apache Spark", "Data Pipelines", "ETL", "Data Warehousing"],
            "duration": "7 weeks",
            "level": "Intermediate"
        },
        {
            "name": "MLOps and AI Pipeline Development",
            "skills": ["MLflow", "Model Deployment", "Pipeline Automation", "Model Monitoring"],
            "duration": "5 weeks",
            "level": "Advanced"
        },
        {
            "name": "Advanced DevSecOps",
            "skills": ["Security Testing", "Compliance Automation", "Threat Modeling", "Security as Code"],
            "duration": "6 weeks",
            "level": "Advanced"
        },
        {
            "name": "Enterprise API Development",
            "skills": ["RESTful Design", "GraphQL", "API Security", "API Gateway"],
            "duration": "4 weeks",
            "level": "Intermediate"
        },
        {
            "name": "Cloud Native Development",
            "skills": ["Kubernetes", "Service Mesh", "Cloud Native Patterns", "Microservices"],
            "duration": "8 weeks",
            "level": "Advanced"
        },
        {
            "name": "Data Lake Implementation",
            "skills": ["Azure Data Lake", "Data Modeling", "Big Data Processing", "Data Governance"],
            "duration": "6 weeks",
            "level": "Advanced"
        },
        {
            "name": "Network Security Fundamentals",
            "skills": ["Network Protocols", "Firewall Configuration", "VPN Setup", "Network Monitoring"],
            "duration": "6 weeks",
            "level": "Intermediate"
        },
        {
            "name": "Advanced Security Operations",
            "skills": ["SIEM Implementation", "Threat Hunting", "Incident Response", "Security Automation"],
            "duration": "8 weeks",
            "level": "Advanced"
        },
        {
            "name": "Enterprise Network Design",
            "skills": ["Network Architecture", "SDN", "Network Automation", "Performance Optimization"],
            "duration": "7 weeks",
            "level": "Advanced"
        },
        {
            "name": "Cloud Security Architecture",
            "skills": ["AWS Security", "Azure Security", "Zero Trust", "Security Controls"],
            "duration": "6 weeks",
            "level": "Advanced"
        },
        {
            "name": "Penetration Testing Essentials",
            "skills": ["Vulnerability Assessment", "Ethical Hacking", "Security Tools", "Report Writing"],
            "duration": "8 weeks",
            "level": "Advanced"
        },
        {
            "name": "Security Automation with Python",
            "skills": ["Python Scripting", "Security Tools API", "Automation Frameworks", "Security Testing"],
            "duration": "5 weeks",
            "level": "Intermediate"
        },
        {
            "name": "Network Automation and Programmability",
            "skills": ["Network APIs", "Python for Networks", "Ansible", "Network CI/CD"],
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
        },
        {
            "name": "Cloud-Native Platform Modernisation",
            "required_skills": ["AWS Lambda", "Docker", "Terraform", "React", "Node.js"],
            "duration": "9 months",
            "department": "Platform Engineering",
            "goals": ["Re-architect legacy system into microservices", "Implement serverless architecture"]
        },
        {
            "name": "Enterprise Data Lake and Analytics Hub",
            "required_skills": ["Azure Data Lake", "Spark", "Databricks", "Power BI"],
            "duration": "12 months",
            "department": "Data & Analytics",
            "goals": ["Build centralized data lakehouse", "Implement real-time business intelligence"]
        },
        {
            "name": "AI-Powered Predictive Maintenance System",
            "required_skills": ["Python", "TensorFlow", "Docker", "Kubernetes"],
            "duration": "8 months",
            "department": "IoT Solutions",
            "goals": ["Develop predictive analytics for equipment", "Implement industrial IoT monitoring"]
        },
        {
            "name": "Secure DevOps Automation Framework",
            "required_skills": ["GitHub Actions", "Terraform", "AWS CodePipeline", "OWASP ZAP"],
            "duration": "6 months",
            "department": "DevSecOps",
            "goals": ["Implement security-first CI/CD", "Automate vulnerability scanning"]
        },
        {
            "name": "Enterprise Network Security Transformation",
            "required_skills": ["Network Security", "Zero Trust", "SIEM", "Firewall Management"],
            "duration": "9 months",
            "department": "Network Security",
            "goals": ["Implement Zero Trust architecture", "Enhance network monitoring and threat detection"]
        },
        {
            "name": "Security Operations Center Modernization",
            "required_skills": ["SIEM", "Security Automation", "Incident Response", "Threat Intelligence"],
            "duration": "8 months",
            "department": "Security Operations",
            "goals": ["Modernize SOC infrastructure", "Implement automated incident response"]
        }
    ]
    
    return job_roles, training_programs, secondment_projects


skills_definition ={  
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
    "Investment Foundations (CFA Institute certification)": {  
      "1": "Beginner: Aware of core investment concepts.",  
      "2": "Novice: Understands financial instruments and market basics.",  
      "3": "Intermediate: Applies investment principles in analysis or reporting.",  
      "4": "Advanced: Makes informed investment decisions, mentors others.",  
      "5": "Expert: Provides strategic investment advice, leads educational efforts."  
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
    },  
    "Accounting Fundamentals (CFI Certification)": {  
      "1": "Beginner: Recognizes core accounting concepts.",  
      "2": "Novice: Records simple transactions, prepares basic statements.",  
      "3": "Intermediate: Interprets financial data, manages ledgers.",  
      "4": "Advanced: Analyzes statements, ensures compliance, supports audits.",  
      "5": "Expert: Provides strategic financial advice, leads accounting policy."  
    }  
  }  
}
