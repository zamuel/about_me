# RAG-Based Recruiter Assistant

This project implements a Retrieval-Augmented Generation (RAG) system that allows recruiters to query information about my professional profile, including experience, education, salary expectations, and location.

## Tech Stack

- **Frontend**: Streamlit
- **Vector Store**: Cortex
- **Database**: Snowflake
- **Embedding + LLM**: OpenAI or compatible service

## Features

- Upload and index profile data to Cortex
- Query interface using natural language
- Streamlit frontend for recruiter interaction

## Setup

```bash
git clone https://github.com/your-username/rag-recruiter-profile.git
cd rag-recruiter-profile
pip install -r requirements.txt
cp .env.example .env
