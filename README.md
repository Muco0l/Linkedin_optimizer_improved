# LinkedIn Profile Analyzer 🔗

A comprehensive AI-powered LinkedIn profile analysis and optimization tool that provides personalized career guidance, content optimization, and job fit analysis using Google's Gemini AI and Apify web scraping.

## Features ✨

### 🔍 Profile Analysis
- **Comprehensive Profile Scraping**: Extracts complete LinkedIn profile data including experience, education, skills, and connections
- **Intelligent Context Analysis**: Analyzes experience level, industry, career stage, and profile completeness
- **Multi-Agent Routing**: Automatically routes queries to specialized agents based on user intent

### 📝 Content Optimization
- **Section Rewriting**: Optimize LinkedIn sections (About, Headline, Experience, etc.)
- **Experience-Level Tailoring**: Customized advice for junior, mid-level, and senior professionals
- **Industry-Specific Guidance**: Tailored recommendations for Tech, Finance, Healthcare, Marketing, Construction, Education, and Retail

### 🎯 Job Fit Analysis
- **Match Score Calculation**: Provides detailed scoring (0-100%) for job role compatibility
- **Gap Analysis**: Identifies missing skills and experience gaps
- **Application Strategy**: Actionable recommendations for job applications

### 🚀 Career Counseling
- **Skill Gap Analysis**: Identifies critical skills needed for career advancement
- **Learning Path Recommendations**: Suggests courses, certifications, and development resources
- **Career Progression Planning**: Short-term and long-term career development strategies

### 💬 Conversational AI Interface
- **Chat-Based Interaction**: Natural language conversations with memory context
- **Quick Action Buttons**: One-click access to common optimization tasks
- **Conversation History**: Maintains context across multiple interactions

## Technology Stack 🛠️

- **Frontend**: Streamlit (Web UI)
- **AI/ML**: Google Gemini 2.0 Flash (Content Generation & Analysis)
- **Web Scraping**: Apify Client (LinkedIn Data Extraction)
- **Data Validation**: Pydantic (Data Models)
- **Language**: Python 3.10+

## Installation 📦

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key
- Apify API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkedin-multiagent-optimizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or if using the project configuration:
   ```bash
   pip install -e .
   ```

3. **Set up API keys**
   Create a `.streamlit/secrets.toml` file in your project root:
   ```toml
   [secrets]
   GOOGLE_API_KEY = "your-google-gemini-api-key"
   APIFY_API_KEY = "your-apify-api-key"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Configuration ⚙️

### Environment Variables
The application requires two API keys configured in Streamlit secrets:

- `GOOGLE_API_KEY`: Your Google Gemini API key for AI content generation
- `APIFY_API_KEY`: Your Apify API key for LinkedIn profile scraping

### API Keys Setup

#### Google Gemini API
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your secrets.toml file

#### Apify API
1. Sign up at [Apify](https://apify.com/)
2. Navigate to Settings → Integrations
3. Copy your API token
4. Add it to your secrets.toml file

## Usage Guide 📋

### Getting Started

1. **Launch the Application**
   ```bash
   streamlit run app.py
   ```

2. **Enter LinkedIn Profile URL**
   - Paste your LinkedIn profile URL in the sidebar
   - Add target job titles (optional)
   - Click "Analyze Profile"

3. **Start Chatting**
   - Use the chat interface to ask questions
   - Try quick action buttons for common tasks
   - Get personalized recommendations

### Common Use Cases

#### Profile Optimization
```
"Optimize my About section for a senior software engineer role"
"Rewrite my LinkedIn headline to attract recruiters"
"Help me improve my skills section"
```

#### Job Fit Analysis
```
"Analyze my fit for Product Manager role at Google"
"What are my chances for a Data Scientist position?"
"How well do I match this job description?"
```

#### Career Guidance
```
"What skills do I need to become a senior developer?"
"How can I transition from marketing to tech?"
"What certifications should I pursue?"
```

## Architecture 🏗️

### Multi-Agent System
The application uses a sophisticated multi-agent architecture:

1. **Intent Classification Agent**: Routes queries to appropriate handlers
2. **Content Optimization Agent**: Handles profile section improvements
3. **Profile Analysis Agent**: Provides comprehensive profile evaluation
4. **Job Fit Analysis Agent**: Analyzes compatibility with target roles
5. **Career Counseling Agent**: Offers strategic career advice

### Data Flow
```
LinkedIn URL → Apify Scraper → Profile Data → Gemini Analysis → 
Context Extraction → User Query → Intent Classification → 
Specialized Agent → AI Response → User Interface
```

## Project Structure 📁

```
linkedin-multiagent-optimizer/
├── app.py                 # Main Streamlit application
├── scrape.py             # LinkedIn profile scraping logic
├── pyproject.toml        # Project configuration
├── README.md            # This file
├── .streamlit/
│   └── secrets.toml     # API keys (not tracked)
└── requirements.txt     # Python dependencies
```

## Features Deep Dive 🔍

### Profile Context Analysis
The system extracts and analyzes:
- **Experience Level**: Junior, Mid-level, Senior
- **Industry Classification**: Tech, Finance, Healthcare, etc.
- **Career Stage**: Early career, Mid-career, Director level
- **Employment Type**: Full-time, Part-time, Freelance, etc.
- **Profile Completeness**: Percentage score with improvement suggestions

### Industry-Specific Optimization
Each industry receives tailored advice:
- **Tech**: Technical skills, innovation, adaptability
- **Finance**: Analytical skills, regulations, attention to detail
- **Healthcare**: Patient care, empathy, medical knowledge
- **Marketing**: Creativity, communication, market trends
- **Construction**: Safety, project management, technical expertise
- **Education**: Teaching methods, curriculum development
- **Retail**: Customer service, sales, inventory management

### Experience-Level Customization
- **Junior**: Encouraging, skill-building focused, entry-level guidance
- **Mid-level**: Professional growth, leadership development, strategic thinking
- **Senior**: Executive presence, thought leadership, industry influence

## API Integration 🔌

### Apify Integration
The application uses Apify's LinkedIn scraper actor (`2SyF0bVxmgGr8IVCZ`) to extract:
- Basic profile information
- Work experience
- Education history
- Skills and endorsements
- Connection count
- Company information

### Google Gemini Integration
Leverages Gemini 2.0 Flash model for:
- Profile context analysis
- Content generation and optimization
- Intent classification
- Conversational responses

## Customization Options 🎨

### Adding New Industries
Extend the `industry_contexts` dictionary in `industry_based_context()`:
```python
industry_contexts = {
    "Your_Industry": "Specific guidance for your industry",
    # Add more industries here
}
```

### Custom Prompt Templates
Modify the prompt templates in each agent function to customize:
- Response tone and style
- Analysis focus areas
- Recommendation types
- Output format

## Troubleshooting 🔧

### Common Issues

1. **Profile Scraping Fails**
   - Verify LinkedIn URL format
   - Check Apify API key
   - Ensure profile is public

2. **AI Responses Are Generic**
   - Verify Google Gemini API key
   - Check API quotas and limits
   - Ensure profile data was extracted successfully

3. **Session State Issues**
   - Refresh the page
   - Clear browser cache
   - Restart the Streamlit server

### Debug Mode
Enable debug information by adding:
```python
st.write(st.session_state)  # View current session state
```

## Contributing 🤝

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes
5. Add tests if applicable
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Comment complex logic

## Limitations ⚠️

- **LinkedIn Rate Limits**: Apify may have scraping limitations
- **API Costs**: Google Gemini API usage incurs costs
- **Profile Privacy**: Can only scrape public LinkedIn profiles
- **Data Accuracy**: AI responses are generated and may need verification

## Future Enhancements 🚀

- [ ] Resume generation from LinkedIn data
- [ ] Bulk profile analysis
- [ ] Integration with job boards
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Export functionality for recommendations


## Support 

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

## Acknowledgments 

- Google Gemini for AI capabilities
- Apify for web scraping infrastructure
- Streamlit for the web framework
- The open-source community for inspiration

---

**Note**: This tool is for educational and professional development purposes. Always respect LinkedIn's terms of service and data privacy guidelines.