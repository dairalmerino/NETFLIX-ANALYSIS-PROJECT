# 🎬 Netflix Content Strategy Analysis (2016–2021)

## Overview
An exploratory data analysis investigating how Netflix's content strategy evolved 
from 2016 to 2021, with a focus on whether COVID-19 changed what they produced.

**Thesis:** How did Netflix's content strategy evolve from 2016 to 2021, and did 
COVID-19 change what they produced?

## 🔗 Live Dashboard
[View the interactive Streamlit dashboard here](https://netflix-analysis-project-covid-impact.streamlit.app/)

## 📊 Key Findings
- **Content growth:** Movie additions grew +231.6% from 2016–2017 before declining 
  -22.7% by 2021. TV shows proved more resilient to COVID disruption.
- **Genre shifts:** All top 5 genres increased post-COVID. Comedies grew the most 
  sharply at +49.1% avg per year.
- **International content:** Peaked at 63.6% in 2018, dipped during COVID, with 
  partial recovery by 2021.
- **Content maturity:** Netflix shifted toward mature content; PG-13 grew +143.6% 
  and R-rated content nearly doubled (+81.4%) post-COVID.
- **Seasonal patterns:** Netflix front-loaded its release calendar post-COVID, 
  peaking in June (+102.8%) while Q4 declined sharply (-45.0% in December).

## 🛠️ Tech Stack
- Python, pandas, numpy
- Plotly (visualizations)
- Streamlit (dashboard)
- Jupyter Notebook (analysis)
- Git & GitHub (version control)

## 📁 Project Structure

```
NETFLIX-PROJECT/
│
├── analysis.ipynb       ← full EDA notebook
├── app.py               ← Streamlit dashboard
├── netflix_titles.csv   ← dataset (Kaggle)
└── README.md
```

## 🚀 How to Run Locally
```bash
git clone https://github.com/dairalmerino/NETFLIX-ANALYSIS-PROJECT.git
cd NETFLIX-ANALYSIS-PROJECT
pip install pandas numpy plotly streamlit
streamlit run app.py
```

## 📦 Dataset
[Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

## ⚠️ Limitations
- Dataset covers 2016–2021 only; post-COVID window limited to 2 years
- 9% of titles missing country data excluded from international analysis
- Statistical significance limited by small sample size (TVD p=0.143)

## 🔮 Future Work
- Incorporate 2022–2024 data to confirm whether trends persisted
- Analyze Netflix original vs licensed content separately
- Cross-reference with Netflix subscriber growth data
- Apply a recommender system to predict what content Netflix might prioritize next

## 👩‍💻 Author
Daira Merino | [GitHub](https://github.com/dairalmerino)