# Project Synopsis

**Project title:** Question Paper Generation Using LLM  
**Programme:** HCLTech Career Shaper Programme, III Year Industry Project, 2025–26  
**Domain:** LLM / Python  
**Learner identity fields:** Complete in the DOCX template before submission.

## Problem statement

Teachers and trainers need to produce clear, syllabus-aligned assessments from course notes, often under time constraints. This project creates a reviewable first draft from authorized learning material using an optional large language model and a private offline mode, with educators checking all questions and answer keys before use.

## Proposed solution

A Streamlit web app accepts pasted learning notes or TXT, PDF, and DOCX files. Educators configure the subject, learner level, assessment type, difficulty, question formats, item count, and total marks. Drafts can be generated locally from note excerpts or through an OpenAI-compatible model. The app validates count and marks, shows source context and suggested answers, and exports a student paper, teacher key, and JSON.

## Dataset and results

The cleaned reference dataset has 500 rows and seven metadata columns. It has no question text, answer text, or source passages, so it is used only for descriptive analysis. The mean synthetic retrieval score is 0.7466, and mean synthetic answer-quality score is 0.8029. These are descriptive reference-data statistics, not generator performance metrics. Generator accuracy and response time have not been benchmarked.

## Architecture

Educator notes and settings → Streamlit UI → offline extractive generator or optional LLM API → educator review → student paper, answer key, or JSON. See `architecture.svg` and `architecture.png`.

## Ethical review

Complete and sign the checklist in `Ethical_Compliance_Checklist.md`. Confirm dataset reuse rights, follow institutional AI disclosure rules, avoid personal data, and review every generated question and answer before use.
