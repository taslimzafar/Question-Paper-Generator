from __future__ import annotations
import json, os, re, time, urllib.request
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='PaperForge | Question Paper Generator', page_icon='📝', layout='wide')

st.markdown('''<style>
:root{--ink:#172b4d;--muted:#52627a;--blue:#2459d3;--line:#dce4ef}
.block-container{padding-top:2rem;max-width:1250px}
.hero{background:linear-gradient(115deg,#102a56,#2459d3);color:white;padding:28px 32px;border-radius:18px;margin-bottom:18px}
.hero h1{color:white;margin:0;font-size:2.2rem}.hero p{margin:.45rem 0 0;color:#e1eaff;font-size:1.05rem}
section[data-testid="stSidebar"]{background:#f4f7fb}
[data-testid="stMetric"]{background:white;border:1px solid var(--line);border-radius:12px;padding:14px}
.question{border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:12px 0;background:white}
.small{color:var(--muted);font-size:.9rem}
</style>''',unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>Question Paper Generator</h1><p>Build a balanced, editable paper from your syllabus notes with a hosted LLM or a private offline mode.</p></div>',unsafe_allow_html=True)

def extract_text(upload):
    if not upload:return ''
    suffix=Path(upload.name).suffix.lower()
    try:
        if suffix=='.txt': return upload.getvalue().decode('utf-8',errors='replace')
        if suffix=='.pdf':
            from pypdf import PdfReader
            reader=PdfReader(upload)
            return '\n'.join(p.extract_text() or '' for p in reader.pages)
        if suffix=='.docx':
            from docx import Document
            import io
            d=Document(io.BytesIO(upload.getvalue()))
            return '\n'.join(p.text for p in d.paragraphs)
    except Exception as e:
        st.error(f'Could not read {upload.name}: {e}')
    return ''

def split_sentences(text):
    clean=re.sub(r'\s+',' ',text).strip()
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+',clean) if len(s.strip().split())>=5]

def offline_generate(notes,subject,grade,exam_type,total_marks,n_questions,formats,difficulty):
    sentences=split_sentences(notes)
    if not sentences: raise ValueError('Add syllabus notes containing at least one complete sentence.')
    verbs={'Easy':'Define or explain','Moderate':'Describe how','Challenging':'Analyze the significance of'}
    out=[]
    for i in range(n_questions):
        source=sentences[i%len(sentences)]
        words=source.split()
        # Create a defensible question anchored to submitted material; answer remains a cited excerpt.
        keyphrase=' '.join(words[:min(7,len(words))]).rstrip('.,:;')
        fmt=formats[i%len(formats)]
        action=verbs[difficulty]
        if fmt=='Multiple choice':
            # Offline MCQs are deliberately avoided unless alternatives can be derived from supplied notes.
            other=[s for s in sentences if s!=source]
            options=[source]+other[:3]
            if len(options)<4: fmt='Short answer'
            else:
                import random
                random.Random(i+17).shuffle(options)
                out.append({'type':'Multiple choice','marks':1,'question':f'Which note statement begins with this exact phrase: “{keyphrase} …”?','options':options[:4],'answer':source,'explanation':'The correct statement reproduces the relevant idea from the supplied notes.' ,'source':f'Provided notes, sentence {i%len(sentences)+1}'})
                continue
        if fmt=='Short answer': prompt=f'{action} the following concept from {subject}: “{keyphrase}”.'
        elif fmt=='Long answer': prompt=f'{action} “{keyphrase}” and support your response with details from the provided {subject} notes.'
        else: prompt=f'{action} the idea “{keyphrase}” in the context of {subject}.'
        out.append({'type':fmt,'marks':1,'question':prompt,'answer':source,'explanation':'Use the answer key as a reference and award marks for accurate coverage of the key idea.','source':f'Provided notes, sentence {i%len(sentences)+1}'})
    # Respect total mark budget without altering user question count
    base,rem=divmod(total_marks,n_questions)
    for i,item in enumerate(out): item['marks']=base+(1 if i<rem else 0)
    return out

def llm_generate(notes,subject,grade,exam_type,total_marks,n_questions,formats,difficulty,model,api_key,base_url):
    prompt=f'''Create an original {exam_type} question paper for {grade} on {subject}. Return only valid JSON with a top-level "questions" array. Exactly {n_questions} questions and exactly {total_marks} total marks. Allowed types: {formats}. Difficulty: {difficulty}. Use ONLY these source notes; do not invent facts. Each item must include type, marks (integer), question, answer, explanation, source (short quoted phrase from notes), and options (array for multiple choice, otherwise empty). Ensure marks add up exactly and MCQ has one unambiguous correct answer.
SOURCE NOTES:\n{notes[:18000]}'''
    url=base_url.rstrip('/')+'/chat/completions'
    body=json.dumps({'model':model,'temperature':0.3,'messages':[{'role':'system','content':'You create assessment materials grounded only in provided notes. Return strict JSON, no markdown.'},{'role':'user','content':prompt}]}).encode()
    req=urllib.request.Request(url,data=body,headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=90) as response: payload=json.loads(response.read())
    content=payload['choices'][0]['message']['content']
    content=re.sub(r'^```(?:json)?\s*|\s*```$','',content.strip(),flags=re.I)
    result=json.loads(content)
    questions=result.get('questions',[])
    if len(questions)!=n_questions: raise ValueError(f'The model returned {len(questions)} questions; expected {n_questions}. Try again.')
    if sum(int(q.get('marks',0)) for q in questions)!=total_marks: raise ValueError('The model returned a paper whose marks do not total the requested marks. Try again.')
    for q in questions:
        if not q.get('question') or not q.get('answer'): raise ValueError('The model omitted a question or answer. Try again.')
        q.setdefault('options',[]); q.setdefault('source','See supplied notes'); q.setdefault('explanation','')
    return questions

with st.sidebar:
    st.header('Paper settings')
    subject=st.text_input('Subject',value='Computer Science')
    grade=st.text_input('Class / course',value='Undergraduate')
    exam_type=st.selectbox('Assessment', ['Practice test','Unit test','Midterm examination','Final examination','Quiz'])
    total_marks=st.number_input('Total marks',min_value=5,max_value=200,value=30,step=5)
    n_questions=st.number_input('Number of questions',min_value=1,max_value=50,value=10)
    difficulty=st.select_slider('Difficulty',options=['Easy','Moderate','Challenging'],value='Moderate')
    formats=st.multiselect('Question formats',['Short answer','Long answer','Multiple choice'],default=['Short answer','Long answer'])
    st.divider(); st.subheader('LLM settings')
    use_llm=st.toggle('Use an OpenAI compatible LLM',value=False)
    api_key=st.text_input('API key',type='password',help='Kept in memory for this session only; do not commit API keys.') if use_llm else ''
    model=st.text_input('Model',value='gpt-4o-mini',disabled=not use_llm)
    base_url=st.text_input('API base URL',value='https://api.openai.com/v1',disabled=not use_llm)
    st.caption('Without an API key, generation runs locally using only the notes you provide.')

st.subheader('1. Add learning material')
left,right=st.columns([1.1,.9])
with left:
    upload=st.file_uploader('Upload notes or syllabus',type=['txt','pdf','docx'])
    uploaded_text=extract_text(upload) if upload else ''
    notes=st.text_area('Paste or edit source notes',value=uploaded_text,height=240,placeholder='Paste syllabus excerpts, learning objectives, or textbook notes here. Questions and answer keys are grounded in this content.')
with right:
    st.markdown('#### How it works')
    st.markdown('1. Add authorized course material.\n2. Set the paper length and question mix.\n3. Generate, review, and edit every item.\n4. Export a student copy or answer key.')
    if notes.strip():
        st.metric('Source material',f'{len(notes.split()):,} words')
        st.caption('Only text you enter or upload is sent to the selected model. Offline mode sends nothing.')

if 'questions' not in st.session_state: st.session_state.questions=[]
if st.button('Generate question paper',type='primary',use_container_width=True,disabled=not notes.strip() or not formats):
    if use_llm and not api_key:
        st.error('Enter an API key or switch off LLM mode to use offline generation.')
    elif not subject.strip(): st.error('Enter a subject.')
    else:
        try:
            with st.spinner('Preparing your question paper…'):
                if use_llm:
                    questions=llm_generate(notes,subject,grade,exam_type,int(total_marks),int(n_questions),formats,difficulty,model,api_key,base_url)
                else:
                    questions=offline_generate(notes,subject,grade,exam_type,int(total_marks),int(n_questions),formats,difficulty)
                st.session_state.questions=questions
                st.session_state.meta={'subject':subject,'grade':grade,'exam_type':exam_type,'total_marks':total_marks,'difficulty':difficulty,'date':time.strftime('%Y-%m-%d')}
            st.success('Paper generated. Review the question wording and answer key before use.')
        except Exception as e: st.error(f'Generation failed: {e}')

questions=st.session_state.questions
if questions:
    meta=st.session_state.meta
    st.divider(); st.subheader('2. Review and export')
    c1,c2,c3=st.columns(3); c1.metric('Questions',len(questions)); c2.metric('Total marks',sum(int(q['marks']) for q in questions)); c3.metric('Mode','LLM' if use_llm else 'Offline')
    st.markdown(f"### {meta['subject']} — {meta['exam_type']}")
    st.caption(f"{meta['grade']}  ·  {meta['difficulty']}  ·  {meta['date']}  ·  Total: {sum(int(q['marks']) for q in questions)} marks")
    edited=[]
    for i,q in enumerate(questions):
        with st.expander(f"Q{i+1}. {q['question'][:110]}{'…' if len(q['question'])>110 else ''}  |  {q['marks']} marks",expanded=True):
            q['question']=st.text_area('Question',q['question'],key=f'q_{i}')
            if q.get('options'):
                for j,opt in enumerate(q['options']): st.write(f'{chr(65+j)}. {opt}')
            st.caption(f"Source: {q.get('source','Provided notes')}")
            with st.expander('Answer key (teacher view)'):
                q['answer']=st.text_area('Suggested answer',q['answer'],key=f'a_{i}')
                st.write(q.get('explanation',''))
            edited.append(q)
    st.session_state.questions=edited
    student_lines=[f"{i+1}. [{q['marks']} marks] {q['question']}" + ('\n'+'\n'.join(f"   {chr(65+j)}. {o}" for j,o in enumerate(q.get('options',[]))) if q.get('options') else '') for i,q in enumerate(edited)]
    teacher_lines=[f"{i+1}. {q['question']}\nAnswer: {q['answer']}\nRationale: {q.get('explanation','')}\nSource: {q.get('source','')}" for i,q in enumerate(edited)]
    d1,d2,d3=st.columns(3)
    d1.download_button('Download student paper (.txt)',f"{meta['subject']}\n{meta['exam_type']}\nTotal marks: {sum(int(q['marks']) for q in edited)}\n\n"+'\n\n'.join(student_lines),'question_paper.txt','text/plain',use_container_width=True)
    d2.download_button('Download answer key (.txt)',f"{meta['subject']} — Answer Key\n\n"+'\n\n'.join(teacher_lines),'answer_key.txt','text/plain',use_container_width=True)
    d3.download_button('Download editable paper (.json)',json.dumps({'metadata':meta,'questions':edited},indent=2),'question_paper.json','application/json',use_container_width=True)
    st.info('Review generated content for syllabus alignment, fairness, accessibility, and marking accuracy before an examination.')
