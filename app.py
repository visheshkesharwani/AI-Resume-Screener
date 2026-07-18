import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
import pandas as pd
import json
import time

# ----------------------------------------------------
# Environment Setup
# ----------------------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ----------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page]
        text += page_obj.extract_text()
    return text

def get_gemini_ai_analysis(jd, resume_text, job_role, exp_level):
    prompt = f"""
    You are an expert HR and highly advanced Applicant Tracking System (ATS). 
    Evaluate the following resume against the provided job description.
    
    Target Job Role: {job_role}
    Expected Experience: {exp_level}
    
    Job Description: {jd}
    Candidate Resume: {resume_text}
    
    Please provide the output STRICTLY as a JSON object with exactly these three keys:
    "Match_Percentage": (Provide ONLY an integer number between 0 and 100)
    "Missing_Skills": (List the key skills missing in a single string)
    "Profile_Summary": (Write a short 2-3 line summary)
    
    Do not add any text or markdown formatting outside the JSON object.
    """
    
    model = genai.GenerativeModel(
        model_name='gemini-3.1-flash-lite',
        generation_config={"temperature": 0.0}
    )
    response = model.generate_content(prompt)
    return response.text

# ----------------------------------------------------
# UI Setup (Streamlit)
# ----------------------------------------------------
st.set_page_config(page_title="AI Resume Screener", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

# --- ULTRA MODERN CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC; 
    }
    
    .glass-header {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    .glass-header h1 {
        color: #38BDF8;
        font-weight: 700;
        font-size: 3.2rem;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .glass-header p {
        color: #E2E8F0;
        font-size: 1.2rem;
        font-weight: 300;
    }

    /* Big Action Button */
    .stButton>button {
        background: linear-gradient(90deg, #10B981 0%, #059669 100%);
        color: white;
        border-radius: 8px;
        padding: 0.8rem 2rem;
        font-size: 18px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
        height: 60px;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
        color: white;
        border: 1px solid white;
    }

    /* Custom Cards for Steps */
    .step-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #38BDF8;
        height: 100%;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #64748B;
        font-size: 14px;
        margin-top: 50px;
        border-top: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class="glass-header">
        <h1>📑 RESUME SCANNER 📌</h1>
        <p>Enterprise Applicant Tracking & Smart Resume Analysis System</p>
    </div>
""", unsafe_allow_html=True)

# --- QUICK GUIDE (Fills top space nicely) ---
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("""<div class="step-card"><b>1️⃣ Configure Parameters</b><br><span style="color:gray; font-size:14px;">Set the job role, experience level, and passing score in the sidebar.</span></div>""", unsafe_allow_html=True)
with col_b:
    st.markdown("""<div class="step-card"><b>2️⃣ Input Details</b><br><span style="color:gray; font-size:14px;">Paste the exact JD and bulk-upload candidate PDF resumes.</span></div>""", unsafe_allow_html=True)
with col_c:
    st.markdown("""<div class="step-card"><b>3️⃣ Get AI Insights</b><br><span style="color:gray; font-size:14px;">Review instant Match Scores, missing skills, and visual graphs.</span></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- SIDEBAR (Advanced Controls) ---
with st.sidebar:
    st.image("https://tse2.mm.bing.net/th/id/OIP.N_kkeOOdQckSZrEmMAs7lgAAAA?r=0&pid=ImgDet&w=172&h=172&c=7&dpr=1.1&o=7&rm=3", width=80)
    st.markdown("<h2 style='color: #0F172A; font-weight: 700;'>⚙️ ATS Parameters</h2>", unsafe_allow_html=True)
    
    st.markdown("### Job Specifications")
    job_role = st.selectbox("Target Job Role", ["Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer", "HR Manager", "Other"])
    exp_level = st.select_slider("Required Experience", options=["Entry Level (0-1 yrs)", "Junior (1-3 yrs)", "Mid-Level (3-5 yrs)", "Senior (5-8 yrs)", "Director/Lead (8+ yrs)"])
    
    st.markdown("---")
    st.markdown("### Screening Strictness")
    cut_off_score = st.slider("Minimum Match Required (%)", 0, 100, 75, help="Candidates scoring below this will be marked as Rejected.")
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.info("System Status: Online 🟢\n\nPowered by Google Gemini AI")

# --- MAIN INPUT SECTION ---
tab1, tab2 = st.tabs(["📋 Data Input & Processing", "📊 Analytics Dashboard"])

with tab1:
    col1, space, col2 = st.columns([1, 0.05, 1])

    with col1:
        st.markdown("<h3 style='color: #1E293B;'>📄 Job Description</h3>", unsafe_allow_html=True)
        jd_text = st.text_area("Paste the job requirements here", height=300, label_visibility="collapsed", placeholder="Enter the detailed job description, responsibilities, and required skills here...")

    with col2:
        st.markdown("<h3 style='color: #1E293B;'>📂 Upload Candidate Resumes</h3>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload PDF files", 
            type=["pdf"], 
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        st.success("✨ **Pro Tip:** Upload 3-4 resumes together to see the comparison graph in the Analytics Tab!")

    st.markdown("<br>", unsafe_allow_html=True)

    results_data = []

    # Centered Action Button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
    with col_btn2:
        process_btn = st.button("🚀 Execute AI Screening Pipeline", use_container_width=True)

    # --- PROCESSING SECTION ---
    if process_btn:
        if jd_text and uploaded_files:
            st.markdown("<hr style='border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #1E293B;'>🤖 Live AI Evaluation</h2><br>", unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            
            for index, file in enumerate(uploaded_files):
                with st.container():
                    with st.spinner(f"Scanning and analyzing '{file.name}' against requirements..."):
                        
                        resume_text = extract_text_from_pdf(file)
                        ai_response = get_gemini_ai_analysis(jd_text, resume_text, job_role, exp_level)
                        
                        try:
                            clean_json = ai_response.replace('```json', '').replace('```', '').strip()
                            data = json.loads(clean_json)
                            
                            match_score_str = str(data.get("Match_Percentage", "0")).replace('%', '').strip()
                            try:
                                match_score = int(float(match_score_str))
                            except ValueError:
                                match_score = 0
                                
                            missing_skills = data.get("Missing_Skills", "Not Available")
                            summary = data.get("Profile_Summary", "Not Available")
                            
                            if match_score >= cut_off_score:
                                status = "Shortlisted"
                                status_color = "normal"
                                emoji = "✅"
                            else:
                                status = "Rejected"
                                status_color = "inverse"
                                emoji = "❌"
                            
                            # Elegant Result Display
                            with st.expander(f"Applicant: {file.name} | Status: {status} {emoji} | Score: {match_score}%", expanded=True):
                                res_col1, res_col2 = st.columns([1.2, 2.8])
                                
                                with res_col1:
                                    st.metric(label="ATS Match Score", value=f"{match_score}%", delta=status, delta_color=status_color)
                                    st.progress(match_score / 100.0)
                                
                                with res_col2:
                                    st.markdown("**🌟 AI Profile Summary:**")
                                    st.info(summary)
                                    st.markdown("**⚠️ Critical Missing Skills:**")
                                    st.warning(missing_skills)
                            
                            results_data.append({
                                "Candidate Name": file.name,
                                "Match Score (%)": match_score,
                                "Status": status,
                                "Missing Skills": missing_skills,
                                "Profile Summary": summary
                            })
                            time.sleep(1) # Prevent API limits
                            
                        except Exception as e:
                            st.error(f"Error parsing JSON for {file.name}. Ensure Gemini output is strict JSON.")
                            st.write("Raw Output:", ai_response)
                            
                progress_bar.progress((index + 1) / total_files)
            
            # Save results to session state
            st.session_state['results_data'] = results_data
            st.success("🎉 Batch Processing Complete! Navigate to the 'Analytics Dashboard' tab for visual insights.")
                        
        else:
            st.error("⚠️ Validation Error: Please provide the Job Description and upload at least one Resume.")

# --- ANALYTICS TAB ---
with tab2:
    st.markdown("<h3 style='color: #1E293B;'>📊 Executive Analytics Dashboard</h3>", unsafe_allow_html=True)
    
    if 'results_data' in st.session_state and st.session_state['results_data']:
        df = pd.DataFrame(st.session_state['results_data'])
        
        # Display Top Metrics
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        col_stat1.metric("Total Candidates", len(df))
        col_stat2.metric("✅ Shortlisted", len(df[df["Status"] == "Shortlisted"]))
        col_stat3.metric("❌ Rejected", len(df[df["Status"] == "Rejected"]))
        col_stat4.metric("🏆 Highest Score", f"{df['Match Score (%)'].max()}%")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # --- THE NEW CHART SECTION ---
        st.markdown("#### 📈 Candidate Performance Graph")
        chart_data = df[['Candidate Name', 'Match Score (%)']].set_index('Candidate Name')
        st.bar_chart(chart_data, color="#38BDF8")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Data Table
        st.markdown("#### 🗄️ Detailed Database")
        st.dataframe(df.style.highlight_max(subset=['Match Score (%)'], color='lightgreen'), use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.download_button(
                label="📥 Download Full Audit Report (CSV)",
                data=csv,
                file_name="hire_scout_ats_report.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("📈 No analytical data available yet. Please run a batch process in the first tab to generate the dashboard.")

# Footer
st.markdown("""
    <div class="footer">
        © 2026 HireScout AI Systems | Engineered for Modern HR Teams<br>
        <i>Strictly Confidential & Automated Processing</i>
    </div>
""", unsafe_allow_html=True)