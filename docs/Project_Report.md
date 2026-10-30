# Project report

## 1. Executive summary

This project implements a browser-based question paper generator for educators who need a first draft of assessments from authorized course notes. It provides a local, extractive offline mode and an optional OpenAI-compatible model integration. Educators set the subject, learner level, assessment type, difficulty, item formats, number of questions, and total marks; they review editable questions and export the student paper, answer key, or JSON. The purpose is to reduce repetitive drafting while keeping a teacher in control of the final assessment.

The provided reference CSV was not a question-answer dataset. It contains 500 rows of synthetic document retrieval metadata and seven columns. It has no source passages, prompts, responses, ground-truth labels, or validated human judgments. It was cleaned and analyzed as a separate reference dataset; none of its metadata is used to generate questions or represented as generator evaluation. This distinction is central to interpreting the results.

## 2. Problem statement and objectives

Teachers and trainers often have to turn course materials into question sets under time pressure. Manual drafting can make it harder to maintain consistent coverage, marks, and difficulty across several versions. A generative model can help draft questions, but may introduce unsupported facts, ambiguous distractors, or errors in answer keys. The system therefore grounds generation in educator-provided notes, displays source attribution and suggested answers, and makes review and editing part of the workflow.

Objectives are to provide a simple web interface; accept pasted text and TXT, PDF, or DOCX notes; support configurable assessment settings; generate a student paper and separate teacher key; offer an offline option; provide a hosted LLM option through a compatible endpoint; and clearly explain data, evaluation, and ethical limits.

## 3. Scope and requirements

The prototype is a single-user local Streamlit application. Input material is user supplied. It supports one paper per generation request, with editable generated wording and downloadable TXT and JSON files. It is intended for formative drafts and educator-reviewed assessment creation, not automated grading or unsupervised high-stakes examinations.

Functional requirements include settings for subject, class/course, assessment, difficulty, item formats, count, and total marks; parsing of common study-note files; offline generation without network calls; optional API generation; an answer key with source context; and exports. Quality requirements include clear warnings, a session-only API key field, bounded upload size via Streamlit defaults, model-output JSON validation, count and marks validation, and no persistence of uploaded learning content by this application.

## 4. System design

The Streamlit front end gathers notes and configuration. The offline generator splits notes into sentences, creates prompts around note phrases, and uses source excerpts as answer anchors. The API mode sends notes and settings to an OpenAI-compatible `/chat/completions` endpoint and requests strict JSON. It checks question count, sum of marks, and required fields before displaying a paper. Both paths share the same review and export interface. The app stores current results in Streamlit session state; it does not include a vector database or persistent corpus.

The data-flow diagram is included at `architecture.svg`. In hosted mode, the educator's notes leave the local process and go to the configured provider. In offline mode, generation is local after the software dependencies have been installed. The selected model and provider determine external retention and billing; educators must review those terms and avoid submitting material they are not authorized to share.

## 5. Implementation and technology

The application uses Python and Streamlit. `pypdf` extracts text from PDF; `python-docx` extracts paragraphs from Word files; TXT uses UTF-8 decoding. A Python standard-library HTTP client calls compatible model endpoints. The interface offers clear settings, session-only API key entry, progress feedback, editable question text and answer key, source text, and downloads in TXT or JSON. The CSV analysis uses pandas; charts are standalone SVGs and do not require a plotting library.

Offline mode is deliberately described as a baseline, not equivalent to a capable LLM. It turns supplied note excerpts into prompts and uses the note excerpt for the answer key. The fallback is useful for checking interface flow and producing a grounded draft, but it has limited linguistic variety and cannot guarantee a balanced exam. Its multiple-choice behavior requires enough distinct notes and still requires educator review.

## 6. Dataset and exploratory analysis

The source file contained 500 records and seven columns: `doc_id`, `doc_type`, `chunk_id`, `word_count`, `retrieval_score`, `query_type`, and `answer_quality_score`. The cleaning script trims identifiers/categories, converts numerical columns, drops exact duplicates and incomplete rows, normalizes labels, clips scores to the expected 0–1 range, and rounds display values. In this supplied file no duplicates or missing fields were found, so the clean dataset remains 500 rows by seven columns. The completed data dictionary is in `data/data_dictionary.csv`.

The mean synthetic retrieval score is 0.7466. The mean synthetic answer-quality score is 0.8029, with observed range 0.600–1.000. Query categories are summarization 118, procedural 106, factual 94, comparative 92, and analytical 90. These numbers describe only the supplied synthetic metadata. No inference about question quality, model accuracy, or application performance follows from them. Three EDA charts show the retrieval score distribution, query type counts, and word count versus synthetic quality score.

## 7. Evaluation, limitations, and ethics

Evaluation criteria are defined for a future human review: (1) syllabus alignment, measured as the proportion of questions judged answerable from source notes; (2) factual correctness of answer keys, rated by a subject expert; (3) mark consistency, checked against the requested total; (4) clarity and ambiguity, rated by an educator; and (5) generation latency measured over repeated runs and reported separately for offline and hosted modes. No empirical accuracy or latency claim is made here because no representative question corpus, answer key, model credential, or measured benchmark was supplied. The interface performs deterministic structural checks for item count, mark total, and required fields when using the API path.

Limitations include short-note dependence, sentence splitting that may lose context, no adaptive coverage planner, no plagiarism or bias audit, no student-response grading, and no persistence or institution authentication. Model output can still be wrong even when it cites a phrase. The generated paper must be checked for accessibility, fairness, age appropriateness, syllabus coverage, and answer-key quality. Use only content with permission; avoid personal data. Disclose AI assistance as required by the institution. Hosted API use transmits content to a third party; provider settings, privacy terms, and data-processing obligations require review.

## 8. Installation, conclusion, and references

On Windows, install Python 3.10+, then run `run_windows.bat`. It creates a virtual environment, installs the packages in `requirements.txt`, and starts the local Streamlit service. The first setup requires package-download access. Once installed, offline generation does not require an LLM API. Hosted generation requires a compatible endpoint, model name, and provider key. The project is intended to be portable as a folder; do not commit `.venv` or API secrets.

The project delivers a usable assessment-drafting workflow and separates the real user-provided notes from the unrelated synthetic reference dataset. Its principal value is a reviewable first draft, not autonomous assessment authority. Future work should add a validated syllabus-aligned benchmark, topic coverage constraints, reliable question-level mark rubrics, DOCX/PDF exports, institutional authentication, and educator usability evaluation.

References

1. Streamlit documentation, https://docs.streamlit.io/
2. OpenAI API Chat Completions guide, https://platform.openai.com/docs/guides/text-generation
3. Python documentation, https://docs.python.org/3/
4. HCLTech Career Shaper Programme, Project Brief and Synopsis Template supplied by the learner (2025–26).
