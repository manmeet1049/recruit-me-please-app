# RESUME_PROMPT = """
#     You are an expert resume parser.
#     Respond back in a structured json.
#     Extract the following details from the resume text below:
#     1. Name
#     2. Contact information (email, phone)
#     3. Skills: For each skill, include:
#     - Name
#     - Most recent year the skill was used (do not assume any year, only respond if mentioned, most resumes have ranges like oct,2023 - present in this case always consider the upper limit; like here it was present so 2025)
#     - Total years of experience (if derving  from a date range mentioned in the resume, always consider the upper limit; like here it was present so 2025, also consider months into calculations if mentioned, round it off to higher number, only mention if the source of skill is job)
#     - Context (job, project, or certification)
#     - Weightage (1.0 for job, 0.6 for project, 0.5 for certification)
#     4. Experience: For each job, include:
#     - Role
#     - Company
#     - Start date (YYYY-MM)
#     - End date (YYYY-MM)
#     - Skills used
#     5. Projects: For each project, include:
#     - Title
#     - Description
#     - Start date (YYYY-MM)
#     - End date (YYYY-MM) 
#     - Skills used
#     6. Certifications: For each certification, include:
#     - Name
#     - Issuer
#     - Date earned (YYYY-MM)
#     - Skills covered
#     7. Education: For each degree, include:
#     - Degree name
#     - Institution
#     - Graduation year (YYYY)

#     Resume Text: {text}
# """


RESUME_PROMPT = """
You are an expert resume parser and data extractor.

Your task is to extract structured information from the resume text provided below. Return your response strictly in JSON format with the following fields:

1. **name**: Full name of the candidate.
2. **contact**:
    - email
    - mobile

3. **Skills**: List each skill as a separate object with:
    - `name`: Name of the skill
    - `last_used`: Most recent year the skill was used (strictly ignore if not mentioned) (only if mentioned explicitly; if a date range is given like "Oct 2023 - Present", use the upper bound, e.g., 2025)
    - `experience_years`: Total years of experience (only if derivable from a job's date range; include months and round up)
    - `context`: One of `job`, `project`, or `certification`
    - `weightage`: Use 1.0 for `job`, 0.6 for `project`, and 0.5 for `certification`

4. **Experience**: List each job as an object with:
    - `role`
    - `company`
    - `start_date`: In `YYYY-MM` format
    - `end_date`: In `YYYY-MM` format
    - `skills_used`: List of relevant skills used in this job

5. **Projects**: List each project as an object with:
    - `title`
    - `description`
    - `start_date`: In `YYYY-MM` format
    - `end_date`: In `YYYY-MM` format
    - `skills_used`: List of skills used in this project

6. **Certifications**: List each certification as an object with:
    - `name`
    - `issuer`
    - `date_earned`: In `YYYY-MM` format
    - `skills_covered`: List of skills covered in the certification

7. **Education**: List each degree as an object with:
    - `degree_name`
    - `institution`
    - `graduation_year`: In `YYYY` format

**Guidelines**:
- Do not infer any missing information.
- Only include years or dates if they are clearly mentioned.
- If a date range includes “present”, use 2025 as the upper bound.
- For duration calculations, always round months up to the next full year.
- All extracted information must come from the resume text provided.

Resume Text:
{text}
"""
