AI Interview Agent
==================

A Streamlit-based AI Interview Agent that parses resumes, generates tailored interview questions, and evaluates candidate responses using advanced LLMs—all powered by Python.

Features
--------

*   **Resume Upload & Parsing**
    
    *   Upload PDF, DOCX, or TXT resumes.
        
    *   Extracts and parses candidate information into a structured profile using LLMs.
        
*   **Intelligent Question Generation**
    
    *   Generates technical, behavioral, and situational interview questions based on the candidate's profile and job description.
        
*   **Automated Answer Evaluation**
    
    *   Scores and provides feedback on candidate answers using LLM-powered agents.
        
*   **Simple, Interactive UI**
    
    *   Built with Streamlit for an intuitive, browser-based workflow.
        

Directory Structure
-------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   textai_interview_agent/  ├── app.py               # Main Streamlit application  ├── utils.py             # Utility functions for text extraction and JSON parsing  ├── requirements.txt     # Python dependencies  ├── .env                 # Environment variables (API keys, etc.)  └── README.md   `

Getting Started
---------------

1\. Clone the Repository
------------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashgit clone https://github.com/yourusername/ai-interview-agent.git  cd ai-interview-agent   `

2\. Install Dependencies
------------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashpip install -r requirements.txt   `

3\. Configure Environment
-------------------------

Create a .env file in the project root and add your API keys or environment variables as needed.

4\. Run the Application
-----------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashstreamlit run app.py   `

Core Modules
------------

app.py
------

*   Handles the main application flow using Streamlit.
    
*   Loads environment variables and initializes the LLM.
    
*   Provides sidebar UI for uploading resumes and entering job details.
    
*   Orchestrates resume parsing, question generation, answer input, and evaluation.
    
*   Uses modular agents for parsing, question generation, and evaluation.
    

utils.py
--------

*   Extracts text from PDF and DOCX files.
    
*   Handles text extraction errors gracefully.
    
*   Converts LLM outputs into structured JSON for further processing.
    

Example Usage
-------------

1.  **Upload Resume:**Upload your resume in PDF, DOCX, or TXT format using the sidebar.
    
2.  **Enter Job Details:**Specify the job position and description.
    
3.  **Generate Questions:**Click to get a set of tailored interview questions.
    
4.  **Answer & Evaluate:**Enter your answers and receive instant feedback with scores and comments.
    

Tech Stack
----------

*   **Python 3.12+**
    
*   **Streamlit** (for UI)
    
*   **PyPDF2** / **python-docx** (for document parsing)
    
*   **LLM Integration** (via crewai and custom agents)
    
*   **Pydantic** (for data validation)
    

Customization
-------------

*   **LLM Integration:**Easily switch or extend the LLM provider in app.py for different models or APIs.
    
*   **Question & Evaluation Logic:**Modify or enhance the agents and tasks for domain-specific interviews.
    

Contributing
------------

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.


Acknowledgements
----------------

*   Inspired by the need for automated, intelligent interview preparation tools.
    
*   Utilizes open-source libraries for NLP and document processing.
    

**Build your own AI-powered interview assistant and streamline your hiring or preparation process!**
