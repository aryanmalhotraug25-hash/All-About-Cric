# 🏏 All About Cric

> An interactive **IPL Analytics Dashboard** with an **ML-powered Score Predictor** built using Python, Pandas, Seaborn, Scikit-learn and Streamlit.

🔗 **Live Demo:** [all-about-cric.streamlit.app](https://all-about-cric.streamlit.app)

---

## 📌 About The Project

**All About Cric** is a complete IPL analytics platform that turns 260,000+ deliveries and 1,095 matches from IPL 2008–2024 into insightful, beautiful visualizations.

It also features an AI-powered **First Innings Score Predictor** built using **Linear Regression**, trained on 85,000+ ball-by-ball samples.

---

## ✨ Features

### 📊 Analytics
- **Season Analysis** – Champions, titles, matches per season
- **Team Analysis** – Win %, performance summary, team deep-dive
- **Player Analysis** – Top batters, bowlers, six hitters, four hitters, wicketkeepers, POM awards
- **Orange Cap & Purple Cap** – Per-season leaders with trends
- **Venue Analysis** – Most-hosted venues, highest scoring grounds
- **Head-to-Head** – Compare any two teams instantly

### 🤖 AI Score Predictor
- Predicts final 1st innings score based on live match situation
- Inputs: batting team, bowling team, venue, current runs, wickets, overs, recent momentum
- Built with Linear Regression on smart engineered features (CRR, momentum, wickets-in-hand)
- **R² Score:** 0.68 | **MAE:** ~13 runs

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python |
| **Data** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn (Linear Regression) |
| **Web App** | Streamlit |
| **Styling** | Custom CSS + Google Fonts |

---

## 📂 Project Structure

```
IPL/
├── app/
│   ├── app.py              # Streamlit application
│   └── utils.py            # Data processing & ML logic
│
├── data/
│   ├── matches.csv         # Match-level data
│   └── deliveries.csv      # Ball-by-ball data
│
├── models/
│   ├── score_predictor.pkl # Trained Linear Regression model
│   └── metadata.pkl        # Teams + venues metadata
│
├── notebooks/
│   └── analysis.ipynb      # EDA + Model training notebook
│
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/aryanmalhotraug25-hash/All-About-Cric.git
cd All-About-Cric
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app/app.py
```

App opens at `http://localhost:8501` 🎉

---

## 📈 ML Model Details

### Features Used
- `batting_team`, `bowling_team`, `venue` (One-Hot Encoded)
- `current_runs`
- `wickets_left` (smarter than raw wickets)
- `crr` (current run rate)
- `overs_left`
- `momentum` (runs in last 5 - expected runs)
- `wickets_last_5`

### Pipeline
```
Raw Data → Feature Engineering → One-Hot Encoding → Linear Regression
```

### Performance
- **R² Score:** 0.68
- **MAE:** 13.45 runs

---

## 📊 Data Source

Dataset from [Kaggle - IPL Complete Dataset (2008–2024)](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)

---

## 👤 Author

**Aryan Malhotra**

- GitHub: [@aryanmalhotraug25-hash](https://github.com/aryanmalhotraug25-hash)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
