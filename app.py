import streamlit as st
from google import genai
from scrape import get_profile
import json
from pydantic import BaseModel, ValidationError

# Setup Gemini client
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

# Defineing Pydantic model
class ProfileContext(BaseModel):
    experience_level: str
    industry: str
    career_stage: str
    recent_career_type: str
    total_work_experience: float
    role_type: str
    profile_completeness: int

# Initialize session state
if 'profile_context' not in st.session_state:
    st.session_state.profile_context = None
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
#memory 
def get_conversation_memory():
    """Get the last 10 conversations for context"""
    if len(st.session_state.chat_history) <= 1:
        return ""
    
    recent_messages = st.session_state.chat_history[-20:]
    
    memory_context = "\n\nPREVIOUS CONVERSATION CONTEXT:\n"
    for i, message in enumerate(recent_messages):
        role = "User" if message["role"] == "user" else "Assistant"
        memory_context += f"{role}: {message['content']}\n"
    
    memory_context += "\nEND OF PREVIOUS CONVERSATION CONTEXT\n"
    memory_context += "Please use this context to provide more relevant and personalized responses. Reference previous discussions when appropriate.\n\n"
    
    return memory_context
# Function to get profile context from scraped data
def get_profile_context(profile_data):
    prompt = f"""
    Analyze this LinkedIn profile and return JSON:
    {profile_data}
    
    JSON format:
    {{
        "experience_level": "junior/mid-level/senior",
        "industry": "Tech/Financial Services/Healthcare/Marketing and Advertising/Construction/Education/Retail" based on thair complete profile,
        "career_stage": "early career/mid-career/late career/Director",
        "recent_career_type": "full-time/part-time/internship/freelance/Founder/leadership/consulting/entrepreneurial",
        "total_work_experience": work experience in Years in Float,
        "role_type": "current role title",
        "profile_completeness": "percentage completeness only in integer"
    }}
    """

    response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
    text_response = response.text.strip()
    
    if text_response.startswith("```"):
        text_response = text_response.strip("```json").strip("```").strip()

    try:
        parsed_dict = json.loads(text_response)
        return ProfileContext(**parsed_dict)
    except (json.JSONDecodeError, ValidationError) as e:
        st.error(f"Error parsing profile context: {e}")
        return None
# getting industry based context 
def industry_based_context():
    industry_contexts = {
        "Tech": "Fast-paced, emphasize technical skills, adaptability, innovation.",
        "Financial Services": "Focus on analytical skills, attention to detail, financial regulations.",
        "Healthcare": "Highlight empathy, patient care, medical practices knowledge.",
        "Marketing and Advertising": "Emphasize creativity, communication, market trends.",
        "Construction": "Value safety, project management, technical building expertise.",
        "Education": "Focus on teaching methods, student engagement, curriculum development.",
        "Retail": "Emphasize customer service, sales techniques, inventory management."
    }
    return industry_contexts.get(st.session_state.profile_context.industry, "General industry guidance.")
#Content generation and rewrite agent based on experience and industry context
def content_rewrite_or_generation(context, user_input):
    memory_context = get_conversation_memory()
    
    if context.experience_level == "junior":
        return f"""{memory_context}You are a linkedin guru. Be concise and give friendly response to the user
        Optimizing or generating content asked in the query of the user
        {user_input}
        to the following LinkedIn profile's to match a junior level experience in the {context.industry} industry.
        
        PROFILE DATA:
        {st.session_state.profile_data}

        Following are the industry based context: {industry_based_context()}
        
        1. The asked section should be rewritten and optimized according to the years of experience {context.total_work_experience} and recently working in role {context.role_type} as {context.recent_career_type}.
        2. Simplify technical language.
        3. Include step-by-step guidance if needed.
        4. Help user Optimize the section asked by the user to increase its hiring chances.
        5. Include the Options or examples in markdown format that is easy to copy and paste.
        6. Improve profile completeness from {context.profile_completeness}.
        7. check if the number of connections is less i.e. number of connections in{st.session_state.profile_data},if so suggest to increase connections.
        avoide leadership advice
        """
    elif context.experience_level == "mid-level":
        return f"""{memory_context}You are a linkedin guru. Be concise and give professional response to the user
        Optimizing or generating content asked in the query of the user
        {user_input}
        to the following LinkedIn profile's to match a mid-level level experience in the {context.industry} industry.
        
        PROFILE DATA:
        {st.session_state.profile_data}

        Following are the industry based context: {industry_based_context()}
        
        1. The asked section should be rewritten and optimized according to the years of experience {context.total_work_experience} and recently working in role {context.role_type} as {context.recent_career_type}.
        2. Use technical language.
        3. Include growth and leadership qualities.
        4. Help user Optimize the section asked by the user to increase its future hiring chances and expand its reach.
        5. Include the Options or examples in markdown format that is easy to copy and paste.
        6. Improve profile completeness from {context.profile_completeness}.
        """
    elif context.experience_level == "senior":
        return f"""{memory_context}You are a linkedin guru. Be concise and give professional and specialised response to the user
        Optimizing or generating content asked in the query of the user
        {user_input}
        to the following LinkedIn profile's to match a senior level experience in the {context.industry} industry.
        
        PROFILE DATA:
        {st.session_state.profile_data}

        Following are the industry based context: {industry_based_context()}
        
        1. The asked section should be rewritten and optimized according to the years of experience {context.total_work_experience} and recently working in role {context.role_type} as {context.recent_career_type}.
        2. Use technical language.
        3. Include leadership and growth strategies if needed.
        4. Help user Optimize the section asked by the user to increase its reach and audience.
        5. Include the Options or examples in markdown format that is easy to copy and paste.
        6. Improve profile completeness from {context.profile_completeness}.
        """
#analysing the profile
def profile_analysis(context, user_input):
    memory_context = get_conversation_memory()
    
    if context.experience_level == "junior":
        return f"""{memory_context}You are a LinkedIn profile analysis expert. Be encouraging and provide friendly, supportive guidance for a junior professional.

        USER QUERY: {user_input}
        
        PROFILE DATA:
        {st.session_state.profile_data}

        CONTEXT:
        - Experience Level: {context.experience_level}
        - Industry: {context.industry}
        - Career Stage: {context.career_stage}
        - Recent Career Type: {context.recent_career_type}
        - Total Work Experience: {context.total_work_experience} years
        - Current Role: {context.role_type}
        - Profile Completeness: {context.profile_completeness}%

        Industry Context: {industry_based_context()}

        As a junior professional, focus your analysis on:

        1. **Profile Foundation Assessment**:
           - About Section: Is it clear, enthusiastic, and shows potential?
           - Experience Section: Are internships, projects, and part-time work well-described?
           - Skills Section: Balance of technical and soft skills for entry-level roles
           - Education Section: Academic projects, coursework, and achievements
           - Certifications: Entry-level certifications and online courses

        2. **Entry-Level Optimization**:
           - Highlighting transferable skills from education and internships
           - Showcasing personal projects and volunteer work
           - Demonstrating eagerness to learn and grow
           - Missing foundational skills for {context.industry}

        3. **Profile Building Strategy**:
           - Current completeness score: {context.profile_completeness}%
           - Quick wins to improve profile visibility
           - Essential sections to complete first
           - How to make the most of limited experience

        4. **Junior-Level Best Practices**:
           - How to stand out as a new graduate/junior professional
           - Keywords that recruiters look for in junior candidates
           - Building credibility with limited experience
           - Networking strategies for career starters

        5. **Growth-Focused Action Plan**:
           - Immediate steps to strengthen profile
           - Skills to develop and showcase
           - How to gain relevant experience
           - Building a professional network

        Use simple language, provide step-by-step guidance, and focus on building confidence. Format in markdown with clear sections.
        """
    
    elif context.experience_level == "mid-level":
        return f"""{memory_context}You are a LinkedIn profile analysis expert. Provide professional and strategic guidance for a mid-level professional.

        USER QUERY: {user_input}
        
        PROFILE DATA:
        {st.session_state.profile_data}

        CONTEXT:
        - Experience Level: {context.experience_level}
        - Industry: {context.industry}
        - Career Stage: {context.career_stage}
        - Recent Career Type: {context.recent_career_type}
        - Total Work Experience: {context.total_work_experience} years
        - Current Role: {context.role_type}
        - Profile Completeness: {context.profile_completeness}%

        Industry Context: {industry_based_context()}

        As a mid-level professional, focus your analysis on:

        1. **Professional Growth Assessment**:
           - About Section: Does it reflect career progression and future aspirations?
           - Experience Section: Are achievements quantified and impact clearly shown?
           - Skills Section: Advanced technical skills and emerging leadership abilities
           - Education Section: Continued learning and professional development
           - Certifications: Industry-relevant and advanced certifications

        2. **Career Advancement Optimization**:
           - Demonstrating progression from junior to mid-level responsibilities
           - Leadership experience and team collaboration
           - Strategic thinking and problem-solving capabilities
           - Industry expertise and specialized knowledge gaps

        3. **Competitive Positioning**:
           - Current completeness score: {context.profile_completeness}%
           - How to stand out among other mid-level professionals
           - Thought leadership opportunities
           - Building authority in {context.industry}

        4. **Mid-Level Professional Standards**:
           - Industry benchmarks for {context.total_work_experience} years of experience
           - Advanced keywords and technical terminology
           - Networking for career advancement
           - Building a professional brand

        5. **Strategic Career Development**:
           - Preparing for senior-level transitions
           - Skill gaps for next career level
           - Leadership development opportunities
           - Industry trend alignment

        Use professional language, focus on strategic career moves, and emphasize growth potential. Format in markdown with clear sections and be dynamic to the user query.
        """
    
    elif context.experience_level == "senior":
        return f"""{memory_context}You are a LinkedIn profile analysis expert. Provide sophisticated and strategic guidance for a senior professional.

        USER QUERY: {user_input}
        
        PROFILE DATA:
        {st.session_state.profile_data}

        CONTEXT:
        - Experience Level: {context.experience_level}
        - Industry: {context.industry}
        - Career Stage: {context.career_stage}
        - Recent Career Type: {context.recent_career_type}
        - Total Work Experience: {context.total_work_experience} years
        - Current Role: {context.role_type}
        - Profile Completeness: {context.profile_completeness}%

        Industry Context: {industry_based_context()}

        As a senior professional, focus your analysis on:

        1. **Executive Presence Assessment**:
           - About Section: Does it convey thought leadership and strategic vision?
           - Experience Section: Are major achievements and business impact highlighted?
           - Skills Section: Leadership competencies and industry expertise
           - Education Section: Executive education and board positions
           - Certifications: Executive-level credentials and thought leadership

        2. **Leadership and Impact Optimization**:
           - Demonstrating organizational influence and strategic decision-making
           - Mentorship and team development capabilities
           - Industry contributions and innovation leadership
           - Business transformation and growth initiatives

        3. **Executive-Level Positioning**:
           - Current completeness score: {context.profile_completeness}%
           - Thought leadership and industry recognition
           - Speaking engagements and publications
           - Board positions and advisory roles

        4. **Senior Professional Standards**:
           - C-suite and executive-level expectations
           - Industry thought leadership opportunities
           - Strategic networking and relationship building
           - Personal brand as an industry expert

        5. **Legacy and Succession Planning**:
           - Knowledge transfer and mentorship opportunities
           - Industry contributions and lasting impact
           - Succession planning and talent development
           - Future-proofing career trajectory

        Use sophisticated language, focus on strategic leadership, and emphasize industry influence. Format in markdown with clear sections dinamically chosen as per user query.
        """
#Job fit score to the given job titles
def job_fit_analysis(context, user_input):
    memory_context = get_conversation_memory()
    
    return f"""{memory_context}You are a job fit analysis expert. Analyze how well the LinkedIn profile matches the target job role{st.session_state.job_titles}. Be Short and concise in answering.

    USER QUERY (including target job role): {user_input}
    
    PROFILE DATA:
    {st.session_state.profile_data}

    CONTEXT:
    - Experience Level: {context.experience_level}
    - Industry: {context.industry}
    - Career Stage: {context.career_stage}
    - Recent Career Type: {context.recent_career_type}
    - Total Work Experience: {context.total_work_experience} years
    - Current Role: {context.role_type}
    - Profile Completeness: {context.profile_completeness}%

    Industry Context: {industry_based_context()}

    Please provide a comprehensive job fit analysis:

    

    1. **Match Score Analysis**:
       - **Overall match score (0-100%)** in Large text.
       - Skills match score
       - Experience match score
       - Education/certification match score
       - Industry experience match score
    2. **Job Role Understanding**:
       - Extract the target job role from the user query
       - Create a standard job description for this role in the {context.industry} industry
       - List key requirements, skills, and qualifications typically needed

    3. **Strengths Alignment**:
       - Profile elements that strongly match the job requirements
       - Relevant experience and achievements
       - Transferable skills that add value

    4. **Gap Analysis**:
       - Missing skills or qualifications
       - Experience gaps
       - Certification or education requirements not met
       - Industry-specific knowledge gaps

    5. **Improvement Recommendations**:
       - Immediate actions to improve match score
       - Skills to develop or highlight
       - Experience to emphasize or reframe
       - Keywords to add for ATS optimization
       - Sections to update or strengthen

    6. **Application Strategy**:
       - How to position the profile for this role
       - Cover letter key points
       - Interview preparation focus areas
       - Network targeting suggestions
    choose the answer structure dinamically according to user query.
    Format the response in markdown with clear sections, match scores, and actionable recommendations.
    """

def career_counseling_skill_gap_analysis(context, user_input):
    memory_context = get_conversation_memory()
    
    return f"""{memory_context}You are a career counseling expert specializing in skill gap analysis and career development,be short and concise in answering .

    USER QUERY: {user_input}
    TARGATING ROLS {st.session_state.job_titles}
    PROFILE DATA:
    {st.session_state.profile_data}

    CONTEXT:
    - Experience Level: {context.experience_level}
    - Industry: {context.industry}
    - Career Stage: {context.career_stage}
    - Recent Career Type: {context.recent_career_type}
    - Total Work Experience: {context.total_work_experience} years
    - Current Role: {context.role_type}
    - Profile Completeness: {context.profile_completeness}%

    Industry Context: {industry_based_context()}

    Please provide comprehensive career counseling and skill gap analysis based on the following structure which can be dimamically modified as per user need:

    1. **Current Skills Assessment**:
       - Technical skills inventory
       - Soft skills evaluation
       - Industry-specific competencies
       - Leadership and management capabilities
       - Certification and qualification status

    2. **Career Path Analysis**:
       - Potential career trajectories based on current profile
       - Natural progression opportunities in {context.industry}
       - Lateral movement possibilities
       - Industry transition opportunities

    3. **Target Role Requirements**:
       - Skills needed for desired career progression
       - Industry standards for next-level positions
       - Emerging skills in {context.industry}
       - Future-proof skills for career longevity

    4. **Skill Gap Identification**:
       - Critical missing skills for career advancement
       - Nice-to-have skills for competitive advantage
       - Outdated skills that need updating
       - Soft skills development needs

    5. **Learning and Development Plan**:
       - Priority skills to develop first
       - Recommended learning resources (courses, certifications, books)
       - Timeline for skill development
       - Budget considerations for training

    6. **Career Development Strategy**:
       - Short-term goals (3-6 months)
       - Medium-term objectives (6-18 months)
       - Long-term career vision (2-5 years)
       - Networking and mentorship recommendations

    7. **Action Plan**:
       - Immediate steps to take
       - Milestone tracking suggestions
       - Progress measurement methods
       - Regular review and adjustment schedule

    Format the response in markdown with clear sections, timelines, and specific resource recommendations.
    """
#Fallback handler
def general_prompt_handler(context, user_input):
    memory_context = get_conversation_memory()
    
    return f"""{memory_context}only solve the query 
    {user_input} in short and concise manner and as
    you are a linkedin expert only encorage the user to ask more questions and provide helpful insights like profile enhancement and job fit analysis in short for the profile{st.session_state.profile_data}.
    """
#Routing agent 
def classify_user_intent(user_input):
    classification_prompt = f"""
    Classify this query into one category:
    1. "content_rewrite" - optimize/rewrite LinkedIn sections/generate content/change content etc.
    2. "profile_analysis" - analyze profile gaps/evaluation/tell me about my profile/how is my profile etc.
    3. "job_fit_analysis" - analyze job role fit/what are my chances for this job/how do I fit for this role etc.
    4. "career_counseling" - career advice/skill gaps/how to advance my career/help in carrer progression etc.
    5. "general" - other questions if not fitting into above categories.
    
    Query: "{user_input}"
    
    Respond with only the category name.
    """

    try:
        response = client.models.generate_content(model='gemini-2.0-flash', contents=classification_prompt)
        intent = response.text.strip().lower()
        
        intent_mapping = {
            "content_rewrite": "content_rewrite_or_generation",
            "profile_analysis": "profile_analysis",
            "job_fit_analysis": "job_fit_analysis",
            "career_counseling": "career_counseling_skill_gap_analysis",
            "general": "general_prompt_handler"
        }
        
        return intent_mapping.get(intent, "general_prompt_handler")
    except Exception as e:
        st.error(f"Error in intent classification: {e}")
        return "general_prompt_handler"

def process_user_query(user_input):
    if not st.session_state.profile_context:
        return "Please provide a LinkedIn URL first to analyze your profile."
    
    context = st.session_state.profile_context
    intent_function = classify_user_intent(user_input)
    
    function_mapping = {
        "content_rewrite_or_generation": content_rewrite_or_generation,
        "profile_analysis": profile_analysis,
        "job_fit_analysis": job_fit_analysis,
        "career_counseling_skill_gap_analysis": career_counseling_skill_gap_analysis,
        "general_prompt_handler": general_prompt_handler
    }
    
    handler_function = function_mapping.get(intent_function, general_prompt_handler)
    prompt = handler_function(context, user_input)
    
    try:
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit App
def main():
    st.set_page_config(page_title="LinkedIn Profile Analyzer", layout="wide")
    
    st.title("🔗 LinkedIn Profile Analyzer")
    st.markdown("Analyze your LinkedIn profile and get personalized career guidance!")
    
    # Sidebar
    with st.sidebar:
        st.header("Profile Setup")
        
        # LinkedIn URL input
        linkedin_url = st.text_input(
            "LinkedIn Profile URL",
            placeholder="https://www.linkedin.com/in/username/",
            help="Enter your LinkedIn profile URL"
        )
        
        # Job titles input
        job_titles = st.text_area(
            "Target Job Titles",
            placeholder="Senior Software Engineer\nProduct Manager\nData Scientist",
            help="Enter job titles you're interested in (one per line)"
        )
        
        # Process profile button
        if st.button("🔍 Analyze Profile", type="primary"):
            if linkedin_url:
                with st.spinner("Analyzing LinkedIn profile..."):
                    try:
                        profile_data = get_profile(linkedin_url)
                        if profile_data:
                            st.session_state.profile_data = profile_data
                            context = get_profile_context(profile_data)
                            if context:
                                st.session_state.profile_context = context
                                st.success("✅ Profile analyzed successfully!")
                                
                                # Store job titles in session state
                                if job_titles:
                                    st.session_state.job_titles = [title.strip() for title in job_titles.split('\n') if title.strip()]
                                else:
                                    st.error("Failed to analyze profile context")
                        else:
                            st.error(" Failed to scrape profile data")
                    except Exception as e:
                        st.error(f" Error: {e}")
            else:
                st.warning("⚠️ Please enter a LinkedIn URL")
        
        # Display stored job titles
        if 'job_titles' in st.session_state and st.session_state.job_titles:
            st.subheader("Target Roles")
            for i, title in enumerate(st.session_state.job_titles, 1):
                st.write(f"{i}. {title}")
        
        # Quick action buttons
        if st.session_state.profile_context:
            st.header("📊 Profile Summary")
            col1, col2 = st.columns(2)
            with col1:
                                        st.metric("Experience Level", st.session_state.profile_context.experience_level.title())
                                        st.metric("Industry", st.session_state.profile_context.industry)
                                        st.metric("Career Stage", st.session_state.profile_context.career_stage.title())
            with col2:
                                        st.metric("Work Experience", f"{st.session_state.profile_context.total_work_experience} years")
                                        st.metric("Current Role", st.session_state.profile_context.role_type)
                                        st.metric("Profile Completeness", f"{st.session_state.profile_context.profile_completeness}%")
    
            st.subheader(" Quick Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Profile",use_container_width = True):
                    st.session_state.quick_query = "Analyze my LinkedIn profile and identify key gaps and improvement areas"
                if st.button("Improve About Section",use_container_width = True):
                    st.session_state.quick_query = "Rewrite and optimize my About section"
                if st.button("Improve Headline",use_container_width = True):
                    st.session_state.quick_query = "Rewrite and optimize my LinkedIn headline"
            with col2:
                if st.button("Optimize Skills",use_container_width = True):
                    st.session_state.quick_query = "Optimize my skills section for better visibility"
                if st.button("Job Fit Analysis",use_container_width = True):
                    if 'job_titles' in st.session_state and st.session_state.job_titles:
                        st.session_state.quick_query = f"Analyze my fit for {st.session_state.job_titles[0]} role"
                    else:
                        st.session_state.quick_query = "Analyze my profile for job opportunities"
                if st.button("Skill Gap Analysis",use_container_width = True):
                   st.session_state.quick_query = "What skills do I need to develop for career advancement?"
    st.sidebar.markdown("---")               
    st.sidebar.markdown("### 🧪Use Your Profile Or One Of the Example LinkedIn Profiles for Testing")
    st.sidebar.markdown("Use these public profiles to test application's analysis capabilities.")

    st.sidebar.markdown("#### 🌟 Different Experience Levels")
    st.sidebar.write("Entrepreneur")
    st.sidebar.code("https://www.linkedin.com/in/shronit/ ", language=None)
    st.sidebar.write("Senior Executive")
    st.sidebar.code("https://www.linkedin.com/in/ginnirometty  ", language=None)
    st.sidebar.write("Leadership")
    st.sidebar.code("https://www.linkedin.com/in/melindagates/ ", language=None)
    st.sidebar.write("Beginner")
    st.sidebar.code("https://www.linkedin.com/in/mukulsangamkar/ ", language=None)

    st.sidebar.markdown("#### 👨‍💻 Job Titles")
    st.sidebar.code(f"""
                    Senior Software Engineer
                    Product Manager
                    Data Scientist
                    Marketing Director
                    Business Analyst
                    UX Designer
                    DevOps Engineer
                    Sales Manager""", language=None)

    st.sidebar.markdown("---")
    st.sidebar.info("Note: These are public profiles of well-known professionals. Use them for **testing purposes** only.")

    # Main chat interface
    st.subheader("Chat with LinkedIn Expert")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Handle quick query
    if 'quick_query' in st.session_state:
        query = st.session_state.quick_query
        del st.session_state.quick_query
        
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        # Generate and add assistant response
        with st.spinner("Thinking..."):
            response = process_user_query(query)
            if response:
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your LinkedIn profile or career..."):
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        # Generate and add assistant response
        with st.chat_message("user"):
                st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Let me think..."):
                response = process_user_query(prompt)
                st.markdown(response)
                if response:
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history and st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    main()