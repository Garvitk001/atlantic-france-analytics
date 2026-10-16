# Atlantic France Analytics Dashboard
**Atlantic Recording Corporation | Market Strategy & Audience Analytics**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://atlantic-france-analytics-4ypdl2xsqb8trh2j2vktyl.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**[🔴 View the Live Dashboard](https://atlantic-france-analytics-4ypdl2xsqb8trh2j2vktyl.streamlit.app/)**

An interactive Business Intelligence and Data Science dashboard designed to analyze audience preferences, content compliance, and structural track characteristics in the French music market.

---

## 📋 Executive Context
The French music market has distinct characteristics, including a strong emphasis on cultural sensitivity, greater scrutiny of explicit content, and a historical preference for structured album formats over rapid-release singles. 

For **Atlantic Recording Corporation**, understanding these specific market dynamics is essential for:
* Making data-driven release format decisions.
* Managing explicit-content risk.
* Formulating playlist pitching strategies.
* Successfully localizing global music releases.

---

## 🎯 Problem Statement
Despite access to France Top 50 playlist data, music strategists need quantitative answers to:
1. How explicit content performs relative to clean tracks across chart tiers.
2. Whether French listeners currently favor standalone singles or full album tracks.
3. How track duration correlates with streaming volume and chart retention.
4. Whether high-volume album releases dilute individual track engagement.

This project delivers actionable intelligence tailored to the French music market, empowering label executives to design culturally aligned release campaigns.

---

## 🏗️ Tech Stack
* **Frontend / UI:** Streamlit
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Plotly Express & Plotly Graph Objects, Matplotlib, Seaborn
* **Statistical Modeling:** Statsmodels

---

## 📊 Core Analytical Modules
The dashboard is structured into 7 interactive analytical views:
1. **Market Overview:** Trending artists, track velocity, and overall popularity distribution.
2. **Content Compliance Analysis:** Explicit vs. clean content performance and risk profiling.
3. **Release Format Preference:** Single vs. album track market share and performance metrics.
4. **Song Structure Insights:** Track duration histograms and rank alignment (Short, Medium, Long).
5. **Album Structure Impact:** Correlation analysis measuring album size dilution effects.
6. **Rank Tier Analysis:** Comparative attribute density across Top 10, Top 25, and Top 50 tiers.
7. **Audience Preference Insights:** Executive summary highlighting preferred content profiles.

---

## 🛠️ Installation & Execution

To run this dashboard locally:

### 1. Clone the repository
```bash
git clone https://github.com/Garvitk001/atlantic-france-analytics.git
cd atlantic-france-analytics
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to explore the dashboard.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
