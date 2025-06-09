# Talent Management System - POC

A Streamlit application for talent management with resume analysis using Azure OpenAI.

## Features

1. Resume Upload and Processing
   - Upload employee resumes (PDF, DOCX, TXT)
   - Extract and display resume content

2. AI-Powered Analysis using Azure OpenAI
   - Analyze employee skill gaps
   - Recommend training and development opportunities
   - Suggest secondment projects for skill enhancement
   - Provide career path guidance

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- Visual Studio Code (recommended for development)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/talent-management-system.git
   cd talent-management-system
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Azure OpenAI credentials:
   - Rename `.env.sample` to `.env`
   - Add your Azure OpenAI API key, endpoint, and deployment name in the `.env` file

### Running the Application

Run the Streamlit application:
```bash
streamlit run app/main.py
```

The application will be available at `http://localhost:8501`

## Application Structure

```
talent-management-system/
├── app/
│   └── main.py              # Main Streamlit application
├── data/
│   ├── resumes/             # Uploaded resumes storage
│   └── sample_data/         # Sample resumes and data
├── utils/
│   ├── azure_openai_utils.py # Azure OpenAI integration
│   └── resume_parser.py     # Resume parsing utilities
├── .env                     # Environment variables (not tracked in git)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## How to Use

1. Upload an employee's resume or select one of the sample resumes
2. Click "Process Resume" to extract the resume content
3. Click "Analyze Resume" to run the AI analysis
4. View the detailed analysis in the "Analysis Results" tab

## Azure OpenAI Integration

This application uses Azure OpenAI to analyze resumes and provide insights. The integration:

1. Connects to Azure OpenAI using your API credentials
2. Sends the resume and contextual data for analysis
3. Processes the AI-generated insights for display in the application

## Sample Data

The application includes sample data for:
- Job roles and required skills
- Training programs
- Potential secondment projects

This data is used to provide context to Azure OpenAI for generating relevant recommendations.
