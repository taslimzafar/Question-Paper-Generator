from __future__ import annotations
import json
import os
import re
import time
import urllib.request
from pathlib import Path
import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PaperForge Studio | AI Question Paper Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS / DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #4f46e5;
    --primary-light: #eef2ff;
    --primary-hover: #4338ca;
    --accent: #06b6d4;
    --surface: #ffffff;
    --surface-alt: #f8fafc;
    --border: #e2e8f0;
    --border-hover: #cbd5e1;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-main);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div,
section[data-testid="stSidebar"] .stNumberInput input {
    background-color: #1e293b !important;
    border-color: #334155 !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div {
    color: #818cf8 !important;
}

/* Hero Banner */
.hero-wrapper {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
    position: relative;
    overflow: hidden;
}

.hero-wrapper::after {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(99, 102, 241, 0) 70%);
    pointer-events: none;
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    padding: 5px 14px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #c7d2fe;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin: 0;
    letter-spacing: -0.02em;
}

.hero-title span {
    background: linear-gradient(135deg, #a5b4fc 0%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-top: 0.6rem;
    max-width: 780px;
    line-height: 1.5;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 1.2rem;
}

.pill-feature {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: 0.82rem;
    color: #e2e8f0;
}

/* Metric Cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: #cbd5e1;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.06);
    transform: translateY(-1px);
}

.metric-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #64748b;
}

.metric-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: #0f172a;
    margin-top: 0.2rem;
    letter-spacing: -0.02em;
}

.metric-sub {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

/* Question Review Card */
.q-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.badge-format {
    background: #eef2ff;
    color: #4338ca;
    border: 1px solid #c7d2fe;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
}

.badge-marks {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.82rem;
    font-weight: 700;
}

.badge-source {
    background: #f8fafc;
    color: #475569;
    border: 1px dashed #cbd5e1;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
}

.mcq-option-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 10px 0;
}

.mcq-option-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.9rem;
    color: #1e293b;
}

/* Formal Academic Paper Preview */
.exam-paper-container {
    background: #ffffff;
    border: 2px solid #0f172a;
    border-radius: 4px;
    padding: 2.5rem 3rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    font-family: 'Times New Roman', Times, serif;
    color: #000;
    line-height: 1.6;
}

.exam-header {
    text-align: center;
    border-bottom: 2px solid #000;
    padding-bottom: 1.2rem;
    margin-bottom: 1.5rem;
}

.exam-header h2 {
    font-size: 1.7rem;
    font-weight: bold;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.exam-header h3 {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0.3rem 0;
}

.exam-meta-grid {
    display: flex;
    justify-content: space-between;
    font-size: 0.95rem;
    font-weight: bold;
    margin-top: 0.6rem;
}

.exam-instructions {
    background: #f9f9f9;
    border-left: 3px solid #333;
    padding: 10px 14px;
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}

.exam-question-item {
    margin-bottom: 1.2rem;
    page-break-inside: avoid;
}

/* Buttons */
.stButton>button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    border: none !important;
    padding: 0.65rem 1.4rem !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}

.stButton>button[kind="primary"]:hover {
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
    transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SAMPLE CONTENT PRESETS
# -----------------------------------------------------------------------------
SAMPLE_NOTES = {
    "Operating Systems & Process Management": (
        "Operating systems coordinate CPU execution, memory allocation, and peripheral access across competing tasks. "
        "A process represents an active program state comprising program counter values, CPU registers, and stack frames. "
        "Context switching preserves processor registers so that another runnable process can acquire CPU cycles. "
        "Preemptive scheduling permits high-priority tasks to interrupt executing lower-priority processes. "
        "Deadlocks arise when multiple processes enter circular wait conditions holding non-shareable resources. "
        "The critical section problem requires mutual exclusion, progress, and bounded waiting guarantees. "
        "Virtual memory decouples logical process address space from physical RAM through page mapping tables. "
        "Paging divides physical memory into fixed-size frames while dividing logical memory into blocks of the same size. "
        "Thrashing occurs when the operating system spends more execution cycles swapping pages than executing user instructions."
    ),
    "Machine Learning & Deep Neural Networks": (
        "Machine learning focuses on algorithmic systems that infer general predictive patterns from observed training datasets. "
        "Supervised learning constructs mapping functions from labeled input-output pairs to forecast unseen targets. "
        "Gradient descent minimizes scalar objective functions by iteratively updating weight tensors in the direction of steepest descent. "
        "Overfitting manifests when excessive model capacity memorizes training noise at the expense of generalization. "
        "Cross-entropy loss quantifies divergence between predicted softmax probability distributions and one-hot ground truth labels. "
        "Convolutional layers exploit spatial locality and weight sharing to extract hierarchical visual representations from raw image grids. "
        "Attention mechanisms compute dynamic query-key compatibility matrices to weight context representations across sequence sequences. "
        "Regularization techniques such as weight decay and dropout constrain model parameters to prevent co-adaptation."
    ),
    "Environmental Science & Biodiversity": (
        "Ecosystems consist of biological communities interacting with their physical abiotic environment through biogeochemical cycles. "
        "Primary productivity measures the rate at which photosynthetic autotrophs convert radiant solar energy into chemical biomass. "
        "Trophic efficiency reflects the fraction of energy transferred between sequential consumer tiers along ecological food webs. "
        "Keystone species exert disproportionately significant regulatory control over ecological community structure relative to their numerical abundance. "
        "Habitat fragmentation isolates wildlife populations, decreasing effective gene flow and amplifying vulnerability to localized extinction. "
        "Carbon sequestration captures atmospheric carbon dioxide into oceanic, soil, and vegetative reservoirs to attenuate global climate forcing. "
        "Biodiversity encompasses genetic diversity within species, species richness across taxa, and ecosystem diversity over geographical landscapes."
    )
}

# -----------------------------------------------------------------------------
# CORE GENERATION & TEXT EXTRACTION LOGIC
# -----------------------------------------------------------------------------
def extract_text(upload) -> str:
    if not upload:
        return ""
    suffix = Path(upload.name).suffix.lower()
    try:
        if suffix == ".txt":
            return upload.getvalue().decode("utf-8", errors="replace")
        if suffix == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(upload)
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        if suffix == ".docx":
            from docx import Document
            import io
            d = Document(io.BytesIO(upload.getvalue()))
            return "\n".join(p.text for p in d.paragraphs if p.text.strip())
    except Exception as e:
        st.error(f"Could not read {upload.name}: {e}")
    return ""

def split_sentences(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", clean) if len(s.strip().split()) >= 5]
    return sentences

def extract_key_concepts(sentence: str) -> str:
    words = sentence.split()
    return " ".join(words[:min(6, len(words))]).rstrip(".,:;")

def offline_generate(notes: str, subject: str, grade: str, exam_type: str, total_marks: int, n_questions: int, formats: list[str], difficulty: str) -> list[dict]:
    sentences = split_sentences(notes)
    if not sentences:
        raise ValueError("Please provide syllabus notes containing at least one complete sentence.")
    
    verbs = {
        "Easy": ["Define and explain", "State the core characteristics of", "Identify the primary role of", "Summarize"],
        "Moderate": ["Describe how", "Explain the operational mechanism of", "Illustrate the relationship between concepts in", "Differentiate and discuss"],
        "Challenging": ["Critically analyze the significance of", "Evaluate the structural impact of", "Synthesize the principles governing", "Investigate the theoretical implications of"]
    }
    action_verbs = verbs.get(difficulty, verbs["Moderate"])

    out = []
    for i in range(n_questions):
        source = sentences[i % len(sentences)]
        keyphrase = extract_key_concepts(source)
        fmt = formats[i % len(formats)]
        action = action_verbs[i % len(action_verbs)]
        
        if fmt == "Multiple choice":
            other = [s for s in sentences if s != source]
            if len(other) >= 3:
                # Build an extractive concept question
                other_phrases = [extract_key_concepts(s) for s in other[:3]]
                options = [keyphrase] + other_phrases
                import random
                rnd = random.Random(i * 19 + 7)
                rnd.shuffle(options)
                
                # Mask keyphrase from sentence
                masked_prompt = source
                if keyphrase in source:
                    masked_prompt = source.replace(keyphrase, "_______________", 1)
                
                question_text = f"Which concept accurately completes the following statement regarding {subject}?\n\n\"{masked_prompt}\""
                out.append({
                    "type": "Multiple choice",
                    "marks": 1,
                    "question": question_text,
                    "options": options[:4],
                    "answer": keyphrase,
                    "explanation": f"The statement directly corresponds to: \"{source}\"",
                    "source": f"Syllabus notes, sentence {(i % len(sentences)) + 1}"
                })
                continue
            else:
                fmt = "Short answer"

        if fmt == "Short answer":
            prompt = f"{action} the concept of \"{keyphrase}\" as outlined in {subject}."
            explanation = "Award marks for clear identification of core terms, definitions, and immediate relevance."
        elif fmt == "Long answer":
            prompt = f"{action} \"{keyphrase}\". Provide comprehensive supporting arguments and theoretical grounding from the provided {subject} material."
            explanation = "Award marks for analytical depth, accurate context reproduction, and systematic explanation."
        else:
            prompt = f"{action} \"{keyphrase}\" in the context of {subject}."
            explanation = "Evaluate accuracy according to the cited reference."

        out.append({
            "type": fmt,
            "marks": 1,
            "question": prompt,
            "options": [],
            "answer": source,
            "explanation": explanation,
            "source": f"Syllabus notes, sentence {(i % len(sentences)) + 1}"
        })

    # Marks budget distribution
    base, rem = divmod(total_marks, n_questions)
    for i, item in enumerate(out):
        item["marks"] = base + (1 if i < rem else 0)

    return out

def llm_generate(notes: str, subject: str, grade: str, exam_type: str, total_marks: int, n_questions: int, formats: list[str], difficulty: str, model: str, api_key: str, base_url: str) -> list[dict]:
    prompt = f"""Create an original, rigorously designed {exam_type} question paper for {grade} students in {subject}.
Return ONLY a valid JSON object with a single top-level key "questions" containing an array of question objects.
Requirements:
- Exactly {n_questions} questions.
- Marks across all questions must sum EXACTLY to {total_marks}.
- Allowed question formats: {formats}.
- Difficulty standard: {difficulty}.
- Ground every item strictly in the provided syllabus notes below; do not fabricate facts.
- Each question object must have:
  - "type": string ("Short answer", "Long answer", or "Multiple choice")
  - "marks": integer
  - "question": string
  - "options": array of 4 distinct strings for Multiple choice, or empty array [] otherwise
  - "answer": string (the exact correct answer)
  - "explanation": string (scoring criteria or rationale)
  - "source": string (quoted excerpt from source notes)

SOURCE SYLLABUS NOTES:
{notes[:18000]}"""

    url = base_url.rstrip("/") + "/chat/completions"
    payload_dict = {
        "model": model,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": "You are an expert academic examiner. You output strictly valid JSON conforming to the requested schema."},
            {"role": "user", "content": prompt}
        ]
    }
    body = json.dumps(payload_dict).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        payload = json.loads(response.read().decode("utf-8"))
    
    content = payload["choices"][0]["message"]["content"]
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.I)
    result = json.loads(content)
    questions = result.get("questions", [])
    
    if len(questions) != n_questions:
        raise ValueError(f"Model returned {len(questions)} items; requested {n_questions}.")
    
    total_assigned = sum(int(q.get("marks", 0)) for q in questions)
    if total_assigned != total_marks:
        # Auto-adjust if off by small difference
        diff = total_marks - total_assigned
        questions[-1]["marks"] = int(questions[-1].get("marks", 1)) + diff
    
    for q in questions:
        q.setdefault("options", [])
        q.setdefault("source", "Provided course material")
        q.setdefault("explanation", "Grade according to canonical course notes.")

    return questions

# -----------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Blueprint Settings")
    st.caption("Define the academic profile for your assessment.")

    subject = st.text_input("Subject / Course", value="Operating Systems")
    grade = st.selectbox("Academic Level", ["Undergraduate", "Postgraduate", "High School (11th-12th)", "Middle School", "Professional Certification"])
    exam_type = st.selectbox("Assessment Type", ["Midterm Examination", "Final Examination", "Unit Assessment Test", "Pop Quiz", "Practice / Mock Exam"])
    
    st.markdown("---")
    st.markdown("### ⚖️ Structure & Weightage")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        n_questions = st.number_input("Questions", min_value=1, max_value=50, value=6, step=1)
    with col_sb2:
        total_marks = st.number_input("Total Marks", min_value=5, max_value=200, value=30, step=5)

    difficulty = st.select_slider("Target Difficulty", options=["Easy", "Moderate", "Challenging"], value="Moderate")
    formats = st.multiselect("Format Distribution", ["Short answer", "Long answer", "Multiple choice"], default=["Short answer", "Long answer", "Multiple choice"])

    st.markdown("---")
    st.markdown("### 🧠 Intelligence Engine")
    use_llm = st.toggle("Enable External LLM API", value=False)
    
    if use_llm:
        api_key = st.text_input("API Key", type="password", help="Kept in-memory for this session only.")
        model = st.text_input("Model Name", value="gpt-4o-mini")
        base_url = st.text_input("Base URL", value="https://api.openai.com/v1")
    else:
        api_key = ""
        model = ""
        base_url = ""
        st.info("🔒 **Offline Mode Active**: Generates questions locally using extractive NLP. No network calls or API keys required.")

# -----------------------------------------------------------------------------
# HERO BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-tag">⚡ PaperForge Studio • v2.0</div>
    <h1 class="hero-title">Intelligent <span>Question Paper</span> Studio</h1>
    <p class="hero-subtitle">Design rigorous, accredited, and balanced assessment papers from raw course notes, syllabi, or textbook chapters in seconds.</p>
    <div class="hero-pills">
        <span class="pill-feature">🛡️ 100% Offline Generation Ready</span>
        <span class="pill-feature">🤖 OpenAI / LocalAI Compatible</span>
        <span class="pill-feature">📄 TXT, PDF, DOCX Ingestion</span>
        <span class="pill-feature">🖨️ Printable Academic Layout</span>
        <span class="pill-feature">📊 Grounded Sourcing</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN WORKSPACE TABS
# -----------------------------------------------------------------------------
tab_studio, tab_eda, tab_docs = st.tabs(["📝 Studio & Generator", "📊 Data & EDA Analytics", "ℹ️ System Manual"])

# =============================================================================
# TAB 1: STUDIO & GENERATOR
# =============================================================================
with tab_studio:
    st.markdown("#### 1. Ingest Course Materials")
    
    # Preset sample selector
    col_preset1, col_preset2 = st.columns([3, 1.2])
    with col_preset1:
        st.caption("Upload documents or paste lecture notes below. Alternatively, load a sample domain dataset to test immediately:")
    with col_preset2:
        sample_choice = st.selectbox("💡 Load Demo Preset", ["-- Select a Preset --"] + list(SAMPLE_NOTES.keys()), label_visibility="collapsed")

    default_text = ""
    if sample_choice in SAMPLE_NOTES:
        default_text = SAMPLE_NOTES[sample_choice]

    col_in1, col_in2 = st.columns([1.2, 0.8])
    with col_in1:
        upload = st.file_uploader("Upload Notes or Syllabus (PDF, Word, or Plaintext)", type=["txt", "pdf", "docx"], help="Parsed locally in memory.")
        if upload:
            extracted = extract_text(upload)
            if extracted:
                default_text = extracted

        notes = st.text_area(
            "Source Syllabus / Chapter Notes",
            value=default_text,
            height=230,
            placeholder="Paste syllabus modules, course objectives, definitions, or textbook excerpts here. Every generated question and answer key will be grounded in this material..."
        )

    with col_in2:
        st.markdown("""
        <div class="metric-card" style="margin-bottom: 12px;">
            <div class="metric-label">Document Diagnostics</div>
        """, unsafe_allow_html=True)
        
        words = len(notes.split()) if notes else 0
        sentences = len(split_sentences(notes)) if notes else 0
        reading_time = round(words / 200, 1) if words else 0
        
        c_diag1, c_diag2, c_diag3 = st.columns(3)
        with c_diag1:
            st.metric("Total Words", f"{words:,}")
        with c_diag2:
            st.metric("Sentences", sentences)
        with c_diag3:
            st.metric("Read Time", f"{reading_time}m")
            
        st.markdown(f"""
        <div style="font-size: 0.82rem; color: #64748b; margin-top: 8px;">
            <strong>Readiness:</strong> {'🟢 Optimal context length' if words >= 50 else '🟡 Add more notes for best variety'}
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Workflow Guide</div>
            <ol style="font-size: 0.85rem; color: #475569; padding-left: 1.2rem; margin-top: 6px; margin-bottom: 0;">
                <li>Set exam parameters in the left sidebar.</li>
                <li>Add notes or click <em>Load Demo Preset</em>.</li>
                <li>Click <strong>Generate Question Paper</strong>.</li>
                <li>Review, edit, and export student or teacher copies.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generation Action Trigger
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "meta" not in st.session_state:
        st.session_state.meta = {}

    gen_clicked = st.button(
        "🚀 Generate Balanced Question Paper",
        type="primary",
        use_container_width=True,
        disabled=not notes.strip() or not formats
    )

    if gen_clicked:
        if use_llm and not api_key:
            st.error("⚠️ API key required for LLM mode. Either supply an API key in the sidebar or disable LLM mode for local generation.")
        elif not subject.strip():
            st.error("⚠️ Please specify a Subject.")
        else:
            with st.spinner("Compiling blueprint and synthesizing grounded questions..."):
                try:
                    start_t = time.time()
                    if use_llm:
                        res = llm_generate(notes, subject, grade, exam_type, int(total_marks), int(n_questions), formats, difficulty, model, api_key, base_url)
                    else:
                        res = offline_generate(notes, subject, grade, exam_type, int(total_marks), int(n_questions), formats, difficulty)
                    
                    elapsed = round(time.time() - start_t, 2)
                    st.session_state.questions = res
                    st.session_state.meta = {
                        "subject": subject,
                        "grade": grade,
                        "exam_type": exam_type,
                        "total_marks": int(total_marks),
                        "difficulty": difficulty,
                        "date": time.strftime("%Y-%m-%d"),
                        "mode": "LLM (" + model + ")" if use_llm else "Offline Deterministic",
                        "elapsed": elapsed
                    }
                    st.toast("Question paper generated successfully!", icon="✅")
                except Exception as e:
                    st.error(f"Generation error: {e}")

    # Display Assessment Results
    questions = st.session_state.questions
    if questions:
        meta = st.session_state.meta
        st.markdown("---")
        st.markdown("#### 2. Review & Customize Assessment")

        # Top Summary KPIs
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Subject & Scope</div>
                <div class="metric-value" style="font-size: 1.1rem;">{meta.get('subject')}</div>
                <div class="metric-sub">{meta.get('grade')}</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Assessment</div>
                <div class="metric-value" style="font-size: 1.1rem;">{meta.get('exam_type')}</div>
                <div class="metric-sub">{meta.get('difficulty')} Standard</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Questions</div>
                <div class="metric-value">{len(questions)}</div>
                <div class="metric-sub">Items configured</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi4:
            actual_marks = sum(int(q["marks"]) for q in questions)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Weightage</div>
                <div class="metric-value">{actual_marks} <span style="font-size: 0.9rem; font-weight: normal; color:#64748b;">Marks</span></div>
                <div class="metric-sub">Budget met</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Engine Mode</div>
                <div class="metric-value" style="font-size: 1.1rem;">{'🤖 AI Model' if 'LLM' in meta.get('mode','') else '🔒 Offline'}</div>
                <div class="metric-sub">{meta.get('elapsed', 0)}s compute</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Presentation Tabs (Interactive Editor vs Academic Printable Preview)
        view_edit, view_print = st.tabs(["✏️ Interactive Editor", "🖨️ Printable Academic Layout"])

        with view_edit:
            edited_questions = []
            for i, q in enumerate(questions):
                q_type = q.get("type", "Short answer")
                q_marks = q.get("marks", 1)
                
                with st.expander(f"Question {i+1} • [{q_type} — {q_marks} Marks]", expanded=True):
                    q_col1, q_col2 = st.columns([3.5, 1])
                    with q_col1:
                        q["question"] = st.text_area("Question Statement", q["question"], key=f"q_text_{i}", height=80)
                    with q_col2:
                        q["marks"] = st.number_input("Marks", min_value=1, max_value=50, value=int(q_marks), key=f"q_marks_{i}")
                    
                    if q.get("options"):
                        st.markdown("**Multiple Choice Options:**")
                        for j, opt in enumerate(q["options"]):
                            st.markdown(f"- **{chr(65+j)}.** {opt}")

                    st.markdown(f"""
                    <div style="margin: 8px 0;">
                        <span class="badge-source">📌 Grounded Context: {q.get('source', 'Syllabus Excerpt')}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("🔑 Teacher Marking Scheme & Model Answer", expanded=False):
                        q["answer"] = st.text_area("Model Answer", q.get("answer", ""), key=f"ans_{i}", height=60)
                        st.caption(f"**Marking Rubric:** {q.get('explanation', 'Award marks for factual completeness.')}")

                    edited_questions.append(q)

            st.session_state.questions = edited_questions

        with view_print:
            st.caption("This layout formats the assessment as an accredited university or institutional examination paper:")
            inst_name = st.text_input("Institution / Organization Name", value="ACADEMIC DEPARTMENT OF EXAMINATIONS")
            time_allowed = "1 Hour 30 Minutes" if actual_marks <= 50 else "3 Hours"

            student_paper_html = f"""
            <div class="exam-paper-container">
                <div class="exam-header">
                    <h2>{inst_name}</h2>
                    <h3>{meta.get('subject')} — {meta.get('exam_type')}</h3>
                    <div class="exam-meta-grid">
                        <span>Academic Level: {meta.get('grade')}</span>
                        <span>Date: {meta.get('date')}</span>
                        <span>Time Allowed: {time_allowed}</span>
                        <span>Maximum Marks: {actual_marks}</span>
                    </div>
                </div>
                <div class="exam-instructions">
                    <strong>General Instructions:</strong>
                    <ul style="margin: 4px 0 0 16px; padding: 0;">
                        <li>Read all questions thoroughly before attempting.</li>
                        <li>All questions are compulsory. Marks are indicated against each item.</li>
                        <li>Write clear, precise answers supported by relevant diagrams where necessary.</li>
                    </ul>
                </div>
            """
            for i, q in enumerate(questions):
                student_paper_html += f"""
                <div class="exam-question-item">
                    <table style="width: 100%; border: none;">
                        <tr>
                            <td style="vertical-align: top; width: 35px; font-weight: bold;">Q{i+1}.</td>
                            <td style="vertical-align: top;">{q['question']}</td>
                            <td style="vertical-align: top; width: 75px; text-align: right; font-weight: bold;">[{q['marks']} Marks]</td>
                        </tr>
                    </table>
                """
                if q.get("options"):
                    student_paper_html += '<div style="margin-left: 35px; margin-top: 6px;">'
                    for j, opt in enumerate(q["options"]):
                        student_paper_html += f'<div style="margin-bottom: 4px;"><strong>({chr(65+j)})</strong> {opt}</div>'
                    student_paper_html += '</div>'
                student_paper_html += "</div>"

            student_paper_html += """
                <div style="text-align: center; margin-top: 2rem; border-top: 1px dashed #666; padding-top: 0.8rem; font-style: italic;">
                    *** END OF EXAMINATION PAPER ***
                </div>
            </div>
            """
            st.markdown(student_paper_html, unsafe_allow_html=True)

        # Download Studio
        st.markdown("---")
        st.markdown("#### 3. Export Paper Studio")
        
        student_text_lines = [
            f"{meta.get('subject')} — {meta.get('exam_type')}",
            f"Class / Course: {meta.get('grade')} | Max Marks: {actual_marks} | Date: {meta.get('date')}",
            "----------------------------------------------------------------------",
            "INSTRUCTIONS: Answer all questions. Marks are indicated in brackets.",
            "----------------------------------------------------------------------\n"
        ]
        for i, q in enumerate(questions):
            student_text_lines.append(f"Q{i+1}. [{q['marks']} Marks] {q['question']}")
            if q.get("options"):
                for j, opt in enumerate(q["options"]):
                    student_text_lines.append(f"    ({chr(65+j)}) {opt}")
            student_text_lines.append("")

        teacher_text_lines = [
            f"TEACHER MARKING GUIDE & ANSWER KEY",
            f"Subject: {meta.get('subject')} — {meta.get('exam_type')}",
            f"Total Marks: {actual_marks} | Date: {meta.get('date')}",
            "======================================================================\n"
        ]
        for i, q in enumerate(questions):
            teacher_text_lines.append(f"Q{i+1}. [{q['marks']} Marks] {q['question']}")
            teacher_text_lines.append(f"Model Answer: {q.get('answer')}")
            teacher_text_lines.append(f"Marking Rubric: {q.get('explanation')}")
            teacher_text_lines.append(f"Source Reference: {q.get('source')}\n")

        exp1, exp2, exp3 = st.columns(3)
        with exp1:
            st.download_button(
                "📄 Download Student Paper (.txt)",
                data="\n".join(student_text_lines),
                file_name=f"{meta.get('subject', 'paper')}_student_exam.txt",
                mime="text/plain",
                use_container_width=True
            )
        with exp2:
            st.download_button(
                "🔑 Download Teacher Answer Key (.txt)",
                data="\n".join(teacher_text_lines),
                file_name=f"{meta.get('subject', 'paper')}_teacher_key.txt",
                mime="text/plain",
                use_container_width=True
            )
        with exp3:
            st.download_button(
                "💾 Download Full Schema (.json)",
                data=json.dumps({"metadata": meta, "questions": questions}, indent=2),
                file_name=f"{meta.get('subject', 'paper')}_schema.json",
                mime="application/json",
                use_container_width=True
            )

# =============================================================================
# TAB 2: DATA & EDA ANALYTICS
# =============================================================================
with tab_eda:
    st.markdown("### 📊 Reference Metadata & Exploratory Data Analysis")
    st.caption("Descriptive analysis of the 500-row synthetic retrieval corpus. This illustrates system grounding benchmarking.")

    eda_summary_path = Path("analysis/eda_summary.json")
    if eda_summary_path.exists():
        with open(eda_summary_path, "r", encoding="utf-8") as f:
            eda_stats = json.load(f)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Corpus Records", f"{eda_stats.get('rows', 500)} Chunks")
        m2.metric("Mean Retrieval Score", f"{eda_stats.get('mean_retrieval_score', 0):.4f}")
        m3.metric("Synthetic Quality Score", f"{eda_stats.get('mean_synthetic_quality_score', 0):.4f}")
        m4.metric("Missing Values", f"{eda_stats.get('missing_cells', 0)}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Distribution Charts")
    
    chart_col1, chart_col2 = st.columns(2)
    chart1_p = Path("analysis/query_type_counts.svg")
    chart2_p = Path("analysis/retrieval_score_distribution.svg")
    chart3_p = Path("analysis/word_count_vs_quality.svg")

    with chart_col1:
        if chart1_p.exists():
            st.image(str(chart1_p), caption="Query Type Frequency Distribution", use_container_width=True)
        if chart3_p.exists():
            st.image(str(chart3_p), caption="Word Count vs Answer Quality Score", use_container_width=True)

    with chart_col2:
        if chart2_p.exists():
            st.image(str(chart2_p), caption="Retrieval Relevance Score Distribution", use_container_width=True)

    st.markdown("---")
    st.markdown("#### Reference Data Dictionary")
    data_dict_p = Path("data/data_dictionary.csv")
    if data_dict_p.exists():
        df_dict = pd.read_csv(data_dict_p)
        st.dataframe(df_dict, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 3: SYSTEM MANUAL & ETHICS
# =============================================================================
with tab_docs:
    st.markdown("### ℹ️ PaperForge System Guide & Ethics Compliance")
    
    doc_col1, doc_col2 = st.columns(2)
    with doc_col1:
        st.markdown("""
        #### 🎯 Core Capabilities
        - **Deterministic Offline Generator:** Extractive NLP algorithms derive factual question stems and suggested answers purely from provided materials.
        - **OpenAI-Compatible LLM:** Integrate with modern API models for creative distractor formulation and advanced synthesis.
        - **Format Balance:** Support for Multiple Choice, Short Answer, and Comprehensive Descriptive items.
        - **Human Review Safeguard:** Full in-browser editor allowing educators to adjust scoring rubrics and questions before distribution.
        """)

    with doc_col2:
        st.markdown("""
        #### ⚖️ Responsible Use & Privacy
        - **Zero Unprompted Data Transmission:** Offline mode operates entirely on your host CPU. No external telemetry or network calls.
        - **Ephemeral Keys:** API keys entered into the UI are held purely in volatile RAM during active sessions and are never written to disk.
        - **Human-in-the-Loop:** Automated generation serves as an editorial drafting aid; an accredited educator must verify syllabus conformity.
        """)

    st.markdown("---")
    st.caption("PaperForge Studio • Designed for accredited educators and pedagogical institutions.")
