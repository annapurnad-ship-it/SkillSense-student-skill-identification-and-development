import streamlit as st
import json
from datetime import datetime
from skill import (
    StudentProfile, SkillAnalyzer, DevelopmentStrategy,
    TipsAndRecommendations, DevelopmentProgram, configure_gemini
)

# Page configuration
st.set_page_config(
    page_title="AI Student Skill Developer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
    h1 { color: #1f77b4; }
    h2 { color: #2ca02c; }
    .success-box { background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; }
    .info-box { background-color: #d1ecf1; padding: 1rem; border-radius: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'student_profile' not in st.session_state:
    st.session_state.student_profile = StudentProfile()
if 'model' not in st.session_state:
    st.session_state.model = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# Sidebar - API Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        help="Get your free API key from https://makersuite.google.com/app/apikeys"
    )
    
    if api_key:
        try:
            st.session_state.model = configure_gemini(api_key)
            st.success("✅ API Connected!")
        except Exception as e:
            st.error(f"API Error: {str(e)}")
    
    st.divider()
    st.header("📊 Quick Stats")
    profile = st.session_state.student_profile.get_profile()
    st.metric("Name", profile["name"] or "Not Set")
    st.metric("Skills Added", len(profile["skills"]))
    st.metric("Favorite Subjects", len(profile["fav_subject"]))
    st.metric("Interested Fields", len(profile["interested_fields"]))

# Main Header
st.title("🎓 AI Student Skill Developer")
st.subheader("Personalized Learning Path & Development Strategy")

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Student Profile",
    "🔍 Skill Analysis",
    "🎯 Development Strategy",
    "💡 Tips & Recommendations",
    "📅 Development Program"
])

# TAB 1: Student Profile
with tab1:
    st.header("Create Your Student Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("Full Name", value=profile["name"])
        # FIX: Use max of profile age and min_value to avoid the error
        age = st.number_input("Age", min_value=5, max_value=100, value=max(profile["age"], 5))
        grade = st.selectbox(
            "Grade/Year",
            ["Primary", "Secondary", "High School", "Undergraduate", "Postgraduate"],
            index=0 if not profile["grade"] else 2
        )
    
    with col2:
        learning_style = st.selectbox(
            "Preferred Learning Style",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"],
            index=0 if not profile["learning_style"] else 2
        )
        time_available = st.slider(
            "Hours Available Per Week",
            min_value=0,
            max_value=40,
            value=profile["time_available"] or 10,
            step=1
        )
    
    with col3:
        st.write("")
        st.write("")
        st.info("Fill all sections to get AI-powered recommendations!")
    
    # Favorite Subjects
    st.subheader("📚 Favorite Subjects")
    fav_subjects = st.multiselect(
        "Select your favorite subjects",
        [
            "Mathematics", "Science", "Literature", "History", "Languages",
            "Computer Science", "Physics", "Chemistry", "Biology", "Economics",
            "Art", "Music", "Physical Education", "Social Studies", "Other"
        ],
        default=profile["fav_subject"]
    )
    
    # Interested Fields
    st.subheader("🌟 Career Interests")
    interested_fields = st.multiselect(
        "Select fields you're interested in",
        [
            "Software Development", "Data Science", "AI/Machine Learning",
            "Web Development", "Mobile App Development", "Cloud Computing",
            "Cybersecurity", "Game Development", "UI/UX Design",
            "Digital Marketing", "Business Analysis", "Project Management",
            "Biotechnology", "Environmental Science", "Medicine",
            "Engineering", "Finance", "Education", "Other"
        ],
        default=profile["interested_fields"]
    )
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 Your Strengths")
        strengths = st.text_area(
            "List your academic/skill strengths",
            value="\n".join(profile["strengths"]),
            height=100,
            placeholder="e.g., Problem solving, Communication, Creativity"
        )
    
    with col2:
        st.subheader("📉 Areas to Improve")
        weaknesses = st.text_area(
            "List areas where you want to improve",
            value="\n".join(profile["weaknesses"]),
            height=100,
            placeholder="e.g., Time management, Public speaking, Math concepts"
        )
    
    # Goals
    st.subheader("🎯 Your Goals")
    goals = st.text_area(
        "Write your short-term and long-term goals",
        value="\n".join(profile["goals"]),
        height=100,
        placeholder="e.g., Learn Python in 3 months, Get internship in Data Science"
    )
    
    # Add Skills
    st.subheader("🛠️ Current Skills")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        skill_name = st.text_input("Add a skill")
    with col2:
        skill_proficiency = st.slider("Proficiency (1-10)", 1, 10, 5)
    
    if st.button("➕ Add Skill"):
        if skill_name:
            st.session_state.student_profile.add_skill(skill_name, skill_proficiency)
            st.success(f"✅ Added: {skill_name} - Level {skill_proficiency}")
            st.rerun()
    
    # Display existing skills
    if profile["skills"]:
        st.write("**Current Skills:**")
        for skill, data in profile["skills"].items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(data["proficiency"] / 10, text=f"{skill}")
            with col2:
                st.write(f"{data['proficiency']}/10")
    
    # Save Profile
    if st.button("💾 Save Profile", key="save_profile", use_container_width=True):
        profile_data = {
            "name": name,
            "age": age,
            "grade": grade,
            "fav_subject": fav_subjects,
            "interested_fields": interested_fields,
            "strengths": [s.strip() for s in strengths.split("\n") if s.strip()],
            "weaknesses": [w.strip() for w in weaknesses.split("\n") if w.strip()],
            "goals": [g.strip() for g in goals.split("\n") if g.strip()],
            "learning_style": learning_style,
            "time_available": time_available
        }
        st.session_state.student_profile.update_profile(profile_data)
        st.success("✅ Profile saved successfully!")

# TAB 2: Skill Analysis
with tab2:
    st.header("🔍 AI-Powered Skill Analysis")
    
    if not st.session_state.model:
        st.warning("⚠️ Please configure your API key in the sidebar first!")
    else:
        profile = st.session_state.student_profile.get_profile()
        
        if not profile["name"]:
            st.info("📝 Please complete your profile first!")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Analyze My Skills", use_container_width=True):
                    with st.spinner("Analyzing your skills..."):
                        analyzer = SkillAnalyzer(st.session_state.model)
                        analysis = analyzer.analyze_skills(profile)
                        st.session_state.analysis_results['skills'] = analysis
                        st.success("✅ Analysis complete!")
            
            with col2:
                if st.button("🔗 Identify Learning Gaps", use_container_width=True):
                    with st.spinner("Identifying learning gaps..."):
                        analyzer = SkillAnalyzer(st.session_state.model)
                        gaps = analyzer.identify_learning_gaps(
                            profile["skills"],
                            profile["interested_fields"]
                        )
                        st.session_state.analysis_results['gaps'] = gaps
                        st.success("✅ Gap analysis complete!")
            
            # Display Analysis Results
            if 'skills' in st.session_state.analysis_results:
                st.subheader("📊 Skill Assessment")
                st.json(st.session_state.analysis_results['skills'])
            
            if 'gaps' in st.session_state.analysis_results:
                st.subheader("🔗 Learning Gaps")
                st.json(st.session_state.analysis_results['gaps'])

# TAB 3: Development Strategy
with tab3:
    st.header("🎯 Personalized Development Strategy")
    
    if not st.session_state.model:
        st.warning("⚠️ Please configure your API key in the sidebar first!")
    else:
        profile = st.session_state.student_profile.get_profile()
        
        if not profile["name"] or not profile["fav_subject"] or not profile["interested_fields"]:
            st.info("📝 Please complete your profile with favorite subjects and interests!")
        else:
            if st.button("🚀 Generate Development Strategy", use_container_width=True):
                with st.spinner("Creating your personalized strategy..."):
                    strategy_gen = DevelopmentStrategy(st.session_state.model)
                    strategy = strategy_gen.create_strategy(
                        profile,
                        profile["fav_subject"],
                        profile["interested_fields"]
                    )
                    st.session_state.analysis_results['strategy'] = strategy
                    st.success("✅ Strategy created!")
            
            if 'strategy' in st.session_state.analysis_results:
                st.subheader("📋 Your Development Strategy")
                st.json(st.session_state.analysis_results['strategy'])

# TAB 4: Tips & Recommendations
with tab4:
    st.header("💡 AI Tips & Recommendations")
    
    if not st.session_state.model:
        st.warning("⚠️ Please configure your API key in the sidebar first!")
    else:
        profile = st.session_state.student_profile.get_profile()
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_skill = st.selectbox(
                "Select a skill to improve",
                list(profile["skills"].keys()) if profile["skills"] else ["No skills added"]
            )
        
        with col2:
            selected_field = st.selectbox(
                "Select interested field",
                profile["interested_fields"] if profile["interested_fields"] else ["No fields selected"]
            )
        
        if st.button("💡 Get Tips & Recommendations", use_container_width=True):
            if selected_skill and selected_field and selected_skill != "No skills added" and selected_field != "No fields selected":
                with st.spinner("Generating personalized tips..."):
                    tips_gen = TipsAndRecommendations(st.session_state.model)
                    tips = tips_gen.generate_tips(profile, selected_skill, selected_field)
                    st.session_state.analysis_results['tips'] = tips
                    st.success("✅ Tips generated!")
            else:
                st.warning("⚠️ Please add skills and select a field first!")
        
        if 'tips' in st.session_state.analysis_results:
            st.subheader(f"📚 Tips for {selected_skill} in {selected_field}")
            st.json(st.session_state.analysis_results['tips'])
        
        st.divider()
        
        if st.button("🎓 Get Field Recommendations", use_container_width=True):
            if profile["interested_fields"]:
                with st.spinner("Analyzing career fields..."):
                    tips_gen = TipsAndRecommendations(st.session_state.model)
                    recommendations = tips_gen.get_field_recommendations(
                        profile,
                        profile["interested_fields"]
                    )
                    st.session_state.analysis_results['field_rec'] = recommendations
                    st.success("✅ Recommendations generated!")
            else:
                st.warning("⚠️ Please select interested fields first!")
        
        if 'field_rec' in st.session_state.analysis_results:
            st.subheader("🌟 Field Recommendations")
            st.json(st.session_state.analysis_results['field_rec'])

# TAB 5: Development Program
with tab5:
    st.header("📅 Comprehensive Development Program")
    
    if not st.session_state.model:
        st.warning("⚠️ Please configure your API key in the sidebar first!")
    else:
        profile = st.session_state.student_profile.get_profile()
        
        duration = st.slider(
            "Program Duration (months)",
            min_value=3,
            max_value=24,
            value=12,
            step=3
        )
        
        if st.button("📅 Create Development Program", use_container_width=True):
            if not profile["name"] or not profile["fav_subject"] or not profile["interested_fields"]:
                st.warning("⚠️ Please complete your profile first!")
            else:
                with st.spinner(f"Creating {duration}-month development program..."):
                    program_gen = DevelopmentProgram(st.session_state.model)
                    program = program_gen.create_program(
                        profile,
                        profile["fav_subject"],
                        profile["interested_fields"],
                        duration
                    )
                    st.session_state.analysis_results['program'] = program
                    st.success("✅ Program created!")
        
        if 'program' in st.session_state.analysis_results:
            st.subheader(f"📅 Your {duration}-Month Development Program")
            st.json(st.session_state.analysis_results['program'])

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; margin-top: 2rem;'>
    🎓 AI Student Skill Developer | Powered by Google Gemini AI<br>
    <small>This tool uses AI to provide personalized learning recommendations.</small>
    </div>
""", unsafe_allow_html=True)