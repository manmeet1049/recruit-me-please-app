
RESUME_PROMPT = """
    You are an expert resume parser.
    Respond back in a structured json.
    Extract the following details from the resume text below:
    1. Name
    2. Contact information (email, phone)
    3. Skills: For each skill, include:
    - Name
    - Total years of experience
    - Most recent year the skill was used
    - Context (job, project, or certification)
    - Weightage (1.0 for job, 0.7 for project, 0.5 for certification)
    4. Experience: For each job, include:
    - Role
    - Company
    - Start date (YYYY-MM)
    - End date (YYYY-MM)
    - Skills used
    5. Projects: For each project, include:
    - Title
    - Description
    - Start date (YYYY-MM)
    - End date (YYYY-MM)
    - Skills used
    6. Certifications: For each certification, include:
    - Name
    - Issuer
    - Date earned (YYYY-MM)
    - Skills covered
    7. Education: For each degree, include:
    - Degree name
    - Institution
    - Graduation year (YYYY)

    Resume Text: {text}
"""
