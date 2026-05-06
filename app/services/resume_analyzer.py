"""
Advanced Resume Analyzer Service
Extracts and categorizes resume sections using NLP and regex pattern matching
Includes ATS scoring, keyword analysis, and skill matching
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
import math


def analyze_resume_sections(text: str) -> Dict[str, any]:
    """
    Parse resume text and extract sections using regex patterns
    
    Args:
        text: Raw resume text
        
    Returns:
        Dictionary containing extracted sections
    """
    sections = {
        'contact': extract_contact_info(text),
        'summary': extract_section(text, r'(?:summary|objective|profile|about\s+me)', r'(?:experience|education|skills|projects)'),
        'education': extract_section(text, r'education', r'(?:experience|skills|projects|certifications)'),
        'experience': extract_section(text, r'(?:experience|work\s+history|employment)', r'(?:education|skills|projects|certifications)'),
        'skills': extract_skills(text),
        'projects': extract_section(text, r'projects', r'(?:education|experience|skills|certifications)'),
        'certifications': extract_section(text, r'(?:certifications?|certificates?|licenses?)', r'(?:education|experience|skills|projects)')
    }
    
    return sections


def advanced_resume_analysis(text: str, job_description: str = "") -> Dict[str, any]:
    """
    Advanced resume analysis with ATS scoring, keyword matching, and insights
    
    Args:
        text: Raw resume text
        job_description: Job description for matching
        
    Returns:
        Dictionary with advanced analytics
    """
    sections = analyze_resume_sections(text)
    
    # Calculate ATS score
    ats_score = calculate_ats_score(text, sections)
    
    # Keyword analysis
    keyword_analysis = analyze_keywords(text, job_description) if job_description else None
    
    # Experience analysis
    experience_years = extract_years_of_experience(text)
    
    # Education level
    education_level = determine_education_level(sections.get('education', ''))
    
    # Skill categories
    skill_categories = categorize_skills(sections.get('skills', []))
    
    # Resume strength indicators
    strengths = identify_resume_strengths(text, sections)
    weaknesses = identify_resume_weaknesses(text, sections)
    
    return {
        'sections': sections,
        'ats_score': ats_score,
        'keyword_analysis': keyword_analysis,
        'experience_years': experience_years,
        'education_level': education_level,
        'skill_categories': skill_categories,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'word_count': len(text.split()),
        'readability_score': calculate_readability_score(text)
    }


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information from resume"""
    contact = {}
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact['email'] = email_match.group(0)
    
    # Extract phone
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact['phone'] = phone_match.group(0)
    
    # Extract LinkedIn
    linkedin_pattern = r'(?:linkedin\.com/in/|linkedin\.com/pub/)[\w-]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_match:
        contact['linkedin'] = linkedin_match.group(0)
    
    # Extract GitHub
    github_pattern = r'(?:github\.com/)[\w-]+'
    github_match = re.search(github_pattern, text, re.IGNORECASE)
    if github_match:
        contact['github'] = github_match.group(0)
    
    # Extract name (first few lines, typically)
    lines = text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if line and len(line) < 50 and not re.search(r'[@\d]', line):
            contact['name'] = line
            break
    
    return contact


def extract_section(text: str, start_pattern: str, end_pattern: str) -> str:
    """
    Extract a section from resume text between start and end patterns
    
    Args:
        text: Resume text
        start_pattern: Regex pattern for section start
        end_pattern: Regex pattern for section end
        
    Returns:
        Extracted section text
    """
    # Find section start
    start_match = re.search(start_pattern, text, re.IGNORECASE | re.MULTILINE)
    if not start_match:
        return ""
    
    start_pos = start_match.end()
    
    # Find section end
    end_match = re.search(end_pattern, text[start_pos:], re.IGNORECASE | re.MULTILINE)
    if end_match:
        end_pos = start_pos + end_match.start()
        section_text = text[start_pos:end_pos]
    else:
        # Take next 500 chars if no end found
        section_text = text[start_pos:start_pos + 500]
    
    return section_text.strip()


def extract_skills(text: str) -> List[str]:
    """
    Extract skills from resume text
    
    Returns:
        List of skill strings
    """
    skills = []
    
    # Common skill keywords
    skill_keywords = [
        # Programming Languages
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C\\+\\+', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
        'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS',
        
        # Frameworks & Libraries
        'React', 'Angular', 'Vue', 'Node\\.js', 'Express', 'Django', 'Flask', 'FastAPI',
        'Spring', 'Hibernate', '\\.NET', 'ASP\\.NET', 'Laravel', 'Rails',
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy',
        
        # Databases
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server', 'DynamoDB',
        'Cassandra', 'Elasticsearch',
        
        # Cloud & DevOps
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'Git',
        'Terraform', 'Ansible', 'Linux', 'Unix',
        
        # Data & Analytics
        'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision', 'Data Science',
        'Data Analysis', 'Big Data', 'Hadoop', 'Spark', 'Tableau', 'Power BI',
        
        # Other
        'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'JIRA',
        'Testing', 'Unit Testing', 'Integration Testing', 'Selenium'
    ]
    
    # Find skills section
    skills_section = extract_section(text, r'skills?', r'(?:experience|education|projects|certifications)')
    
    # If no dedicated skills section, search entire text
    search_text = skills_section if skills_section else text
    
    # Extract matching skills
    for skill in skill_keywords:
        pattern = r'\b' + skill + r'\b'
        if re.search(pattern, search_text, re.IGNORECASE):
            # Get the actual matched text to preserve casing
            match = re.search(pattern, search_text, re.IGNORECASE)
            if match:
                skills.append(match.group(0))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            unique_skills.append(skill)
    
    return unique_skills


def format_section_html(section_name: str, content: str) -> str:
    """Format section content as HTML"""
    if not content:
        return ""
    
    # Replace newlines with <br> and preserve formatting
    formatted = content.replace('\n', '<br>')
    return formatted


def calculate_ats_score(text: str, sections: Dict) -> Dict[str, any]:
    """
    Calculate ATS (Applicant Tracking System) compatibility score
    
    Returns:
        Dictionary with overall score and component scores
    """
    scores = {
        'contact_info': 0,
        'formatting': 0,
        'keywords': 0,
        'experience': 0,
        'education': 0,
        'skills': 0
    }
    
    # Contact info (20 points)
    contact = sections.get('contact', {})
    if contact.get('email'): scores['contact_info'] += 7
    if contact.get('phone'): scores['contact_info'] += 7
    if contact.get('linkedin') or contact.get('github'): scores['contact_info'] += 6
    
    # Formatting (15 points)
    if len(text) > 200: scores['formatting'] += 5
    if len(text.split('\n')) > 10: scores['formatting'] += 5
    if not re.search(r'[^\x00-\x7F]', text): scores['formatting'] += 5  # ASCII check
    
    # Keywords (20 points)
    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 'designed', 'built', 'achieved']
    verb_count = sum(1 for verb in action_verbs if verb in text.lower())
    scores['keywords'] = min(20, verb_count * 3)
    
    # Experience (20 points)
    if sections.get('experience'): scores['experience'] = 20
    
    # Education (15 points)
    if sections.get('education'): scores['education'] = 15
    
    # Skills (10 points)
    skill_count = len(sections.get('skills', []))
    scores['skills'] = min(10, skill_count)
    
    total = sum(scores.values())
    
    return {
        'total': total,
        'percentage': round(total, 1),
        'components': scores,
        'grade': get_grade(total)
    }


def get_grade(score: float) -> str:
    """Convert score to letter grade"""
    if score >= 90: return 'A+'
    elif score >= 85: return 'A'
    elif score >= 80: return 'A-'
    elif score >= 75: return 'B+'
    elif score >= 70: return 'B'
    elif score >= 65: return 'B-'
    elif score >= 60: return 'C+'
    elif score >= 55: return 'C'
    else: return 'D'


def analyze_keywords(resume_text: str, job_description: str) -> Dict[str, any]:
    """
    Analyze keyword matching between resume and job description
    
    Returns:
        Dictionary with matched keywords, missing keywords, and match percentage
    """
    # Extract important words from JD (excluding common words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can'}
    
    jd_words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', job_description) if w.lower() not in stop_words]
    resume_words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', resume_text) if w.lower() not in stop_words]
    
    jd_counter = Counter(jd_words)
    resume_counter = Counter(resume_words)
    
    # Get top keywords from JD
    top_jd_keywords = [word for word, count in jd_counter.most_common(30)]
    
    # Find matched and missing keywords
    matched = []
    missing = []
    
    for keyword in top_jd_keywords:
        if keyword in resume_counter:
            matched.append({
                'keyword': keyword,
                'jd_count': jd_counter[keyword],
                'resume_count': resume_counter[keyword]
            })
        else:
            missing.append({
                'keyword': keyword,
                'jd_count': jd_counter[keyword]
            })
    
    match_percentage = (len(matched) / len(top_jd_keywords) * 100) if top_jd_keywords else 0
    
    return {
        'matched_keywords': matched[:15],
        'missing_keywords': missing[:10],
        'match_percentage': round(match_percentage, 1),
        'total_jd_keywords': len(top_jd_keywords),
        'total_matched': len(matched)
    }


def extract_years_of_experience(text: str) -> int:
    """Extract years of experience from resume"""
    # Look for patterns like "5 years", "5+ years", "5-7 years"
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience[:\s]+(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s+in'
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(m) for m in matches])
    
    return max(years) if years else 0


def determine_education_level(education_text: str) -> str:
    """Determine highest education level"""
    education_lower = education_text.lower()
    
    if any(word in education_lower for word in ['phd', 'ph.d', 'doctorate', 'doctoral']):
        return 'PhD'
    elif any(word in education_lower for word in ['master', 'msc', 'm.sc', 'mba', 'm.b.a', 'ma', 'm.a']):
        return 'Masters'
    elif any(word in education_lower for word in ['bachelor', 'bsc', 'b.sc', 'ba', 'b.a', 'btech', 'b.tech', 'be', 'b.e']):
        return 'Bachelors'
    elif any(word in education_lower for word in ['diploma', 'associate']):
        return 'Diploma'
    else:
        return 'Not Specified'


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """Categorize skills into different categories"""
    categories = {
        'Programming Languages': [],
        'Frameworks & Libraries': [],
        'Databases': [],
        'Cloud & DevOps': [],
        'Data Science & AI': [],
        'Other': []
    }
    
    skill_mapping = {
        'Programming Languages': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'scala', 'r'],
        'Frameworks & Libraries': ['react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', '.net', 'laravel', 'rails'],
        'Databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'dynamodb', 'cassandra', 'elasticsearch'],
        'Cloud & DevOps': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd', 'git', 'terraform', 'ansible', 'linux'],
        'Data Science & AI': ['machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'tableau', 'power bi']
    }
    
    for skill in skills:
        skill_lower = skill.lower()
        categorized = False
        
        for category, keywords in skill_mapping.items():
            if any(keyword in skill_lower for keyword in keywords):
                categories[category].append(skill)
                categorized = True
                break
        
        if not categorized:
            categories['Other'].append(skill)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def identify_resume_strengths(text: str, sections: Dict) -> List[str]:
    """Identify resume strengths"""
    strengths = []
    
    if len(sections.get('skills', [])) >= 10:
        strengths.append('Strong technical skill set')
    
    if sections.get('certifications'):
        strengths.append('Professional certifications included')
    
    if sections.get('projects'):
        strengths.append('Relevant projects showcased')
    
    if len(text.split()) > 300:
        strengths.append('Comprehensive work history')
    
    # Check for quantifiable achievements
    if re.search(r'\d+%|\$\d+|increased|improved|reduced|saved', text.lower()):
        strengths.append('Quantifiable achievements mentioned')
    
    contact = sections.get('contact', {})
    if contact.get('linkedin') or contact.get('github'):
        strengths.append('Professional online presence')
    
    return strengths


def identify_resume_weaknesses(text: str, sections: Dict) -> List[str]:
    """Identify areas for improvement"""
    weaknesses = []
    
    if len(sections.get('skills', [])) < 5:
        weaknesses.append('Limited skills listed')
    
    if not sections.get('summary'):
        weaknesses.append('Missing professional summary')
    
    if not sections.get('certifications'):
        weaknesses.append('No certifications mentioned')
    
    if len(text.split()) < 200:
        weaknesses.append('Resume appears too brief')
    
    contact = sections.get('contact', {})
    if not contact.get('linkedin') and not contact.get('github'):
        weaknesses.append('No professional links (LinkedIn/GitHub)')
    
    # Check for action verbs
    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 'designed', 'built', 'achieved']
    verb_count = sum(1 for verb in action_verbs if verb in text.lower())
    if verb_count < 3:
        weaknesses.append('Limited use of strong action verbs')
    
    return weaknesses


def calculate_readability_score(text: str) -> float:
    """Calculate simple readability score (0-100)"""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    
    if not words or not sentences:
        return 0
    
    avg_word_length = sum(len(word) for word in words) / len(words)
    avg_sentence_length = len(words) / len(sentences)
    
    # Simple readability formula (lower is better for resumes)
    score = 100 - (avg_word_length * 5 + avg_sentence_length * 2)
    return max(0, min(100, score))
