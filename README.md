# SHL-RAG-assignment
# SHL Assessment Intelligence Scraper 🔍

This project provides a smart web scraping and analysis pipeline to extract and analyze SHL's public assessment catalog. It is built to help HR teams, researchers, or AI developers gain structured access to detailed assessment data for smarter job screening and candidate evaluation.

## 🔧 Project Overview

SHL offers a wide range of psychometric and job-related assessments through their [product catalog](https://www.shl.com/solutions/products/product-catalog/). However, this data is not directly available in structured format. This tool:

- Crawls all product pages with pagination.
- Visits each individual assessment page.
- Extracts key information such as:
  - Assessment name
  - Description
  - Approximate completion time
  - Remote testing availability
  - Adaptive testing support
  - Direct URL
- Uses [Cohere](https://cohere.com/) to generate semantic embeddings of descriptions.
- Indexes the data using [FAISS](https://github.com/facebookresearch/faiss) for fast similarity search.

---

## 🧠 Use Case

This scraper serves as the data backbone for Gen AI applications such as:

- **Enhanced job-candidate matching**
- **Personalized assessment recommendations**
- **HR analytics dashboards**
- **Assessment similarity search using natural language**

---
## Deployed at:

https://shl-rag-assignment-ksb4vd7cgj2fkvhtus6te5.streamlit.app/

---
## Tech Stack

Selenium – Automated web scraping
BeautifulSoup – HTML parsing
Cohere API – Language embedding
FAISS – Efficient vector similarity search
JSON – Structured output

---

## 📬 Contact
Feel free to reach out via LinkedIn or open an issue if you'd like to collaborate!
https://www.linkedin.com/in/nagaram-kridey-34230b296/

---

## Overview
The SHL Recommender is a web-based application designed to recommend SHL assessment solutions based on a job role or specific keywords. This project integrates a FastAPI backend, Streamlit frontend, Selenium-based web scraper, and AI-powered recommendation system using Cohere embeddings and FAISS for vector search.

## Components:
Frontend: Streamlit
Backend: FastAPI
Data Scraping: Selenium & BeautifulSoup
Recommendation System: Cohere embeddings, FAISS vector search

## Architecture
The architecture is built around a FastAPI backend that handles API requests for recommendations and data updates. The data is scraped from the SHL product catalog and stored in a JSON file. Embeddings for each assessment are computed and indexed using FAISS for fast similarity search.

## Data Flow:
Data Scraping: The web scraper fetches data from the SHL product catalog, extracting relevant details such as assessment name, description, and duration. The data is then saved into a JSON file and the corresponding embeddings are indexed using FAISS.

Frontend: The Streamlit app allows users to enter a job role or keywords to get recommendations from the backend. The frontend sends HTTP requests to the FastAPI backend, which returns relevant assessments based on the query.

Backend: FastAPI serves the data and handles recommendation requests. The backend provides endpoints for fetching all assessments and generating recommendations based on user input.

## Features
1. Data Scraping
Endpoint: POST /update-data

Description: Triggers the web scraping process, fetching the latest assessment data from the SHL catalog and updating the JSON file (shl_assessments.json). It also updates the FAISS index (vectors.index) for the recommendation system.

2. Get All Assessments
Endpoint: GET /recommend

Description: Returns all available assessments from the scraped data in the shl_assessments.json file. This endpoint is used to retrieve and display the entire catalog of SHL assessments.

3. Get Recommendations
Endpoint: POST /recommend

Description: Takes a job role or keyword query as input and returns a list of recommended SHL assessments based on semantic similarity. The backend uses Cohere embeddings to represent the text and FAISS to perform a fast vector search for similar assessments.
