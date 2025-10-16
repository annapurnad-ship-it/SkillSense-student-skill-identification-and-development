# 🎓 AI Student Skill Developer

An intelligent, personalized learning platform powered by Google Gemini AI that helps students identify their strengths, discover learning gaps, and create customized development programs.

## ✨ Features

- **📝 Student Profile Management** - Create comprehensive profiles with skills, interests, and goals
- **🔍 AI-Powered Skill Analysis** - Get detailed assessments of your current skill levels
- **🔗 Learning Gap Identification** - Discover what skills you need to reach your career goals
- **🎯 Personalized Development Strategy** - Receive tailored learning paths based on your profile
- **💡 Smart Recommendations** - Get AI-generated tips for specific skills and career fields
- **📅 Development Programs** - Create 3-24 month structured learning programs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one free here](https://makersuite.google.com/app/apikeys))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd student-development
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run streamlit_app.py
```

4. **Enter your API key** in the sidebar when the app opens

## 📁 Project Structure

```
student-development/
├── streamlit_app.py      # Main Streamlit application
├── skill.py              # Core logic (StudentProfile, SkillAnalyzer, etc.)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎯 How to Use

1. **Configure API Key** - Enter your Gemini API key in the sidebar
2. **Create Profile** - Fill in your personal information, skills, and interests
3. **Analyze Skills** - Use AI to assess your current skill levels and identify gaps
4. **Get Strategy** - Generate a personalized development strategy
5. **Receive Tips** - Get specific recommendations for skills and career fields
6. **Build Program** - Create a comprehensive month-by-month development plan

## 🔧 Configuration

The app uses Google's Gemini AI model. Make sure you have:
- A valid API key from Google AI Studio
- Internet connection for API calls
- Python environment with required packages

## 📦 Dependencies

- **streamlit** - Web application framework
- **google-generativeai** - Google Gemini AI integration
- **python-dotenv** - Environment variable management

## 🛠️ Troubleshooting

**Error: "API Error"**
- Check if your API key is valid
- Verify internet connection
- Ensure API quota is available

**Error: "Value below minimum"**
- This has been fixed in the latest version
- Update to the corrected `streamlit_app.py`

**Skills not appearing**
- Make sure to click "Add Skill" button
- Save your profile after adding skills

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Powered by Google Gemini AI
- Built with Streamlit
- Designed for student success

---

**Need Help?** Check the [Streamlit Documentation](https://docs.streamlit.io) or [Google AI Documentation](https://ai.google.dev/)