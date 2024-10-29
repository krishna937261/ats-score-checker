import streamlit as st
import os
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv
# from dotenv import load_dotenv  # Uncomment this line if you're using .env file

# Load environment variables
# load_dotenv()  # Uncomment this line if you're using .env file

input_prompt = '''
As an ATS specialist, I meticulously evaluate resumes in tech, software, and data science for a fierce job market. Provide a percentage match, identify keywords, and offer top-tier guidance.

1. **Contact Information:**
   - Full name
   - Phone number (with country code)
   - Email address
   - LinkedIn profile
   - Location (City, State, ZIP code)

2. **Resume Format:**
   - Compatible formats (.docx, .pdf)
   - Proper naming convention

3. **Keywords and Phrases:**
   - Relevant to job description
   - Industry-specific terms
   - Synonyms and variations

4. **Formatting:**
   - Consistent and professional
   - Proper fonts, spacing, headers
   - Bulleted lists for clarity

5. **Work Experience:**
   - Job titles
   - Company names
   - Employment dates
   - Achievements, quantified

6. **Education:**
   - Degree earned
   - Institution name
   - Graduation date
   - Relevant coursework or honors

7. **Skills:**
   - Keywords from job description
   - Specific skills mentioned
   - Soft and hard skills

8. **Quantifiable Achievements:**
   - Measurable accomplishments
   - Metrics and data support

9. **Online Presence:**
   - LinkedIn and relevant profiles
   - Consistency with resume

10. **Customization:**
    - Tailored to job requirements
    - Avoid generic content
    - Address company's needs

11. **Gaps in Employment:**
    - Explain significant gaps
    - Provide context for career breaks

12. **Consistency:**
    - Consistent tense and formatting
    - Uniform language and style

13. **Length:**
    - Appropriate for experience level
    - Concise without omitting key details

14. **Language and Grammar:**
    - Correct grammar and spelling
    - Avoid jargon not understood by ATS
    - Use impactful action verbs

15. **File Naming:**
    - Professional and identifiable (e.g., FirstName_LastName_Resume.pdf)
    - Avoid special characters

16. **Applicant's Contact:**
    - Track interactions or applications
    - Mention referrals or connections

**Evaluate and rank various sections of a CV based on their relevance to the job description:**
- For example, given a job description that mentions "experience with Python and machine learning," identify these skills on a CV and rank the corresponding sections higher.
- Output a ranked list of CV sections with relevancy scores (0 to 1).

**Overall CV Ranking:**
- Rank multiple CVs based on their match to the job description.
- Assign relevancy scores to each CV based on:
  - Skill match (programming languages, tools).
  - Experience relevance (years in specific roles).
  - Education match (degrees, certifications).
  - Soft skills (leadership, communication).

The model should also provide explanations for the rankings.

**If multiple CVs are uploaded**, rank them in descending order of ATS score and provide an explanation for each score.

*Resume:*
{text}

*Job Description:*
{jd}
'''

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("AIzaSyAfAzMdmrnZiSZRcAZsxb4uBaBeLMzS_pU")

# Configure API using a dedicated function
def configure_api():
    if API_KEY:
        genai.configure(api_key=API_KEY)
    else:
        st.error("API key not found. Please set it in the .env file.")
        st.stop()  # Stop execution if the API key is missing

# Function to get response from the Gemini API
def get_response_from_gemini(resume_text, job_description):
    input_prompt = f'''
    As an ATS specialist, evaluate resumes for a competitive market. Provide a match percentage, keywords, and top-tier guidance based on the job description and resume content.

    *Resume:*
    {resume_text}

    *Job Description:*
    {job_description}
    '''
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error("Error communicating with the Gemini API.")
        return None

# Function to extract text from an uploaded PDF file
def extract_text_from_pdf(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ''.join(page.extract_text() for page in reader.pages)
        return text
    except Exception as e:
        st.error("Error reading PDF file.")
        return None

# Main app function
def main():
    st.set_page_config(page_title='ATS Score Checker', page_icon=':shark', layout="wide")
    st.title('ATS Score Checker 📊')

    # Configure API at the start of the app
    configure_api()

    # Use columns for organized layout
    col1, col2 = st.columns(2)
    with col1:
        job_description = st.text_area('Paste the Job Description', help='Copy and paste the job description here.')
    with col2:
        uploaded_files = st.file_uploader('Upload Resumes (PDF)', type='pdf', accept_multiple_files=True)

    # Button to trigger the ATS scoring
    if st.button('Check ATS Score'):
        if uploaded_files and job_description:
            for uploaded_file in uploaded_files:
                resume_text = extract_text_from_pdf(uploaded_file)
                if resume_text:
                    response = get_response_from_gemini(resume_text, job_description)
                    if response:
                        st.success(f'Results for {uploaded_file.name}')
                        st.markdown(response)
                else:
                    st.error(f'Could not process {uploaded_file.name}.')
        else:
            st.error('Please upload a resume and provide a job description.')

if __name__ == "__main__":
    main()
