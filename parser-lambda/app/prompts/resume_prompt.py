RESUME_PROMPT = """
You are an expert resume parser and data extractor.

Your task is to extract structured information from the resume text provided below. Return your response strictly in JSON format with the following fields:

1. **name**: Full name of the candidate.
2. **contact**:
    - email
    - mobile

3. **skills**: List each skill as a separate object with:
    - `name`: Name of the skill
    - `last_used`: Most recent year the skill was used (strictly ignore if not mentioned) (only if mentioned explicitly; if a date range is given like "Oct 2023 - Present", use the upper bound, e.g., 2025)
    - `experience_years`: Total years of experience (only if derivable from a job's date range; include months and round up)
    - `context`: One of `job`, `project`, or `certification`
    - `weightage`: Use 1.0 for `job`, 0.6 for `project`, and 0.5 for `certification`

4. **experience**: List each job as an object with:
    - `role`
    - `company`
    - `start_date`: In `YYYY-MM` format
    - `end_date`: In `YYYY-MM` format
    - `skills_used`: List of relevant skills used in this job

5. **projects**: List each project (combine freelance projects if mentioned) as an object with:
    - `title`
    - `description`: derive a small technical summary of 15 words max.
    - `type`: `personal` or `freelance` (if not mentioned consider personal)
    - `start_date`: In `YYYY-MM` format
    - `end_date`: In `YYYY-MM` format
    - `skills_used`: List of skills used in this project

6. **certifications**: List each certification as an object with:
    - `name`
    - `issuer`
    - `date_earned`: In `YYYY-MM` format
    - `skills_covered`: List of skills covered in the certification

7. **education**: List each degree as an object with:
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
