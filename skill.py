import json
import re
from datetime import datetime
from typing import Dict, List, Any
import google.generativeai as genai



# Configure Gemini API (free tier)
def configure_gemini(api_key: str = None):
    """Configure Gemini API with your API key"""
    if api_key is None:
        api_key = "AIzaSyDNt8HX0Qr5GvghQb1MrjzdMLEtz4O3o7w"  # Replace with actual key from https://makersuite.google.com/app/apikeys
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

class StudentProfile:
    """Manage student profile data"""
    def __init__(self):
        self.profile = {
            "name": "",
            "age": 0,
            "grade": "",
            "skills": {},
            "fav_subject": [],
            "interested_fields": [],
            "strengths": [],
            "weaknesses": [],
            "goals": [],
            "learning_style": "",
            "time_available": 0
        }
    
    def update_profile(self, data: Dict):
        """Update student profile with new data"""
        self.profile.update(data)
        return self.profile
    
    def add_skill(self, skill_name: str, proficiency: int):
        """Add or update a skill (1-10 scale)"""
        self.profile["skills"][skill_name] = {
            "proficiency": proficiency,
            "date_added": datetime.now().isoformat(),
            "progress": []
        }
    
    def get_profile(self):
        """Get current profile"""
        return self.profile

class SkillAnalyzer:
    """Analyze student skills using AI"""
    def __init__(self, model=None):
        self.model = model or configure_gemini()
    
    def analyze_skills(self, profile: Dict) -> Dict:
        """Analyze skills and provide AI insights"""
        prompt = f"""
        Analyze this student profile and provide structured analysis:
        {json.dumps(profile, indent=2)}
        
        Provide a JSON response with:
        1. skill_assessment: Overall assessment of current skills
        2. strength_areas: Top 3 strength areas
        3. improvement_areas: Top 3 areas needing improvement
        4. learning_path: Recommended learning progression
        
        Format as valid JSON only.
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"analysis": text}
    
    def identify_learning_gaps(self, skills: Dict, interested_fields: List) -> Dict:
        """Identify gaps between current skills and target fields"""
        prompt = f"""
        Student current skills: {json.dumps(skills, indent=2)}
        Interested fields: {', '.join(interested_fields)}
        
        Identify learning gaps in JSON format with:
        1. required_skills: Skills needed for each interested field
        2. current_gaps: Specific skills lacking
        3. gap_priority: Priority order to fill gaps
        
        Return only valid JSON.
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"gap_analysis": text}

class DevelopmentStrategy:
    """Generate personalized development strategies"""
    def __init__(self, model=None):
        self.model = model or configure_gemini()
    
    def create_strategy(self, profile: Dict, fav_subjects: List, 
                       interested_fields: List) -> Dict:
        """Create personalized development strategy"""
        prompt = f"""
        Create a detailed development strategy for:
        Student Profile: {json.dumps(profile, indent=2)}
        Favorite Subjects: {', '.join(fav_subjects)}
        Interested Fields: {', '.join(interested_fields)}
        
        Provide JSON response with:
        1. strategy_overview: 2-3 line overview
        2. short_term_goals: 3 goals for next 3 months
        3. medium_term_goals: 3 goals for next 6 months
        4. long_term_goals: 2 goals for next 1-2 years
        5. monthly_milestones: Key milestones for each month
        6. estimated_timeline: How long to reach proficiency
        
        Return only valid JSON.
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"strategy": text}

class TipsAndRecommendations:
    """Generate personalized tips and recommendations"""
    def __init__(self, model=None):
        self.model = model or configure_gemini()
    
    def generate_tips(self, profile: Dict, skill: str, 
                     interested_field: str) -> Dict:
        """Generate tips for improving a specific skill"""
        prompt = f"""
        Generate practical tips for:
        Student: {json.dumps(profile, indent=2)}
        Skill to improve: {skill}
        Target field: {interested_field}
        
        Provide JSON response with:
        1. practical_tips: 5 actionable tips
        2. resources: Online courses, books, tools recommendations
        3. practice_exercises: 3 specific exercises to practice
        4. time_commitment: Suggested daily/weekly time
        5. success_indicators: How to measure progress
        6. common_mistakes: 3 common mistakes to avoid
        
        Return only valid JSON.
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"tips": text}
    
    def get_field_recommendations(self, profile: Dict, 
                                 interested_fields: List) -> Dict:
        """Get recommendations for interested fields"""
        prompt = f"""
        Based on this student profile:
        {json.dumps(profile, indent=2)}
        
        And interested fields: {', '.join(interested_fields)}
        
        Provide JSON response with for EACH field:
        1. field_overview: What this field involves
        2. required_skills: Core skills needed
        3. career_paths: 3-4 career options
        4. salary_outlook: General salary range
        5. job_demand: Current job market demand
        6. recommended_qualifications: Degrees or certifications needed
        7. learning_resources: Top 5 resources to start
        8. industry_trends: Current trends in 2025
        
        Return only valid JSON.
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"recommendations": text}

class DevelopmentProgram:
    """Create comprehensive development programs"""
    def __init__(self, model=None):
        self.model = model or configure_gemini()
    
    def create_program(self, profile: Dict, fav_subjects: List,
                      interested_fields: List, duration_months: int = 12) -> Dict:
        """Create a comprehensive development program"""
        prompt = f"""
        Design a comprehensive {duration_months}-month development program:
        Student Profile: {json.dumps(profile, indent=2)}
        Favorite Subjects: {', '.join(fav_subjects)}
        Interested Fields: {', '.join(interested_fields)}
        Duration: {duration_months} months
        
        Provide JSON response with:
        1. program_name: Catchy program name
        2. program_description: Overall description
        3. learning_modules: List of modules with duration
        4. weekly_schedule: Recommended hours per skill
        5. projects: 3-5 projects to complete
        6. certifications: Recommended certifications to pursue
        7. mentorship: Type of mentorship suggested
        8. assessment_methods: How to evaluate progress
        9. total_hours_required: Estimated total hours
        10. expected_outcomes: What student will achieve
        
        Return only valid JSON.
        """
        
        response = self.model.generate_content(prompt)
        text = response.text
        
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {"program": text}