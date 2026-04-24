#  Neuro-Symbolic OWIP System  
(Official Website Identification Project)

## 📌 Project Overview

This project solves a real-world problem:

Finding the **official website** of any organization from noisy search results.

Search engines often show:
- Wikipedia links  
- Social media pages  
- Fake or SEO-optimized sites  

Our system intelligently identifies the **correct official website**.

---

## 🧠 Approach Used

We use a **Neuro-Symbolic AI approach**, which combines:

### 🔹 Symbolic (Rule-based logic)
- Domain checking (.edu, .gov, etc.)
- Keyword matching
- Heuristic scoring

### 🔹 Neural (AI reasoning)
- Semantic understanding of search results
- Context-based ranking

This combination improves accuracy significantly.

---

## ⚙️ Features

- 🔎 Accepts any entity name (e.g., MIT, NASA, Apple)
- 🌐 Searches web results automatically
- 🧠 Filters and ranks links intelligently
- ✅ Outputs the most likely official website
- 📊 Evaluates performance using accuracy, precision, recall

---

## 📊 Results

| Metric     | Value |
|------------|------|
| Accuracy   | ~80% |
| Precision  | ~80% |
| Recall     | ~80% |
| F1 Score   | ~80% |

👉 Improved from baseline (~69%) to hybrid model (~80%)

---

## 🧪 Dataset

- Total Samples: 200
- Categories:
  - Universities
  - Government Agencies
  - Scientific Organizations
  - Companies

---

## 🏗️ System Architecture

1. Input query (entity name)
2. Web search (DDGS)
3. Candidate link extraction
4. Heuristic scoring
5. AI-based ranking
6. Final official website output

---

## 🛠️ Technologies Used

- Python
- DDGS (DuckDuckGo Search)
- RapidFuzz (string matching)
- tldextract (domain parsing)
- Streamlit (UI)

---

## 🚀 How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
streamlit run app.py


├── app.py                  # Streamlit UI
├── smart_link_opener.py    # Core logic
├── evaluate.py             # Evaluation script
├── dataset.csv             # Test dataset
├── requirements.txt        # Dependencies
