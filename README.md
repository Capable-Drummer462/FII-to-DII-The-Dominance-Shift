(Kindly Check Jupytr file for findings, hypothesis and conclusions.)

(To check out Dashboard - https://fii-to-dii-the-dominance-shift-djvjnp4e6pw82pmgbkxzzu.streamlit.app)


# FII to DII: The Dominance Shift
### India Capital Markets Analysis — FY 1992-93 to FY 2025-26

> *How three decades of foreign capital dependence gave way to domestic muscle — and why Indian markets no longer panic when foreign investors leave.*

---

## The Thesis

India's equity markets have undergone a structural shift from FII dependence to DII dominance. This project tracks that shift across five defining crisis events — from the Harshad Mehta Scam of 1992, where domestic institutions barely existed, to the Russia-Ukraine selloff of 2022, where DII absorbed 6.8x more than FII sold without the market flinching.

**The core finding:** By FY 2025-26, DII deployed ₹8,49,000 crore against FII's ₹2,26,000 crore outflow. This is not a cyclical fluctuation. It is a structural, irreversible shift in who owns and anchors Indian markets.

---

## Project Structure

```
FII_to_DII_The_Dominance_Shift/
│
├── data/
│   ├── market_flows.csv          # FII & DII annual flows + index levels (FY 1992–2025)
│   ├── volatility_events.csv     # Crisis behaviour — 5 defining market shocks
│   └── dii_composition.csv       # MF AUM, retail folios, LIC equity (2000–2025)
│
├── FII_to_DII_Analysis.ipynb     # Full analysis notebook — hypothesis to conclusion
├── dashboard.py                   # Streamlit dashboard — dark editorial theme
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Datasets

| File | Rows | Description |
|------|------|-------------|
| `market_flows.csv` | 19 | Annual FII/DII net flows with Nifty & Sensex close — FY 1992-93 to FY 2025-26 |
| `volatility_events.csv` | 5 | Five crisis events: market drop %, recovery months, FII/DII behaviour |
| `dii_composition.csv` | 6 | MF AUM, retail investor folios, LIC equity at 5-year checkpoints |

**Note:** All data on Indian fiscal year basis (April–March). Year notation follows the start year of the fiscal, FY 1992-93 is recorded as 1992.

**Data Sources:**
- FII/DII flows: SEBI, NSE Historical Data, NSDL
- Index levels: BSE/NSE official archives
- MF AUM & Folio data: AMFI (amfiindia.com)
- LIC equity: LIC Annual Reports
- Crisis context: RBI Annual Reports, Ministry of Finance, Economic Survey of India

---

## Analysis Sections

| Section | What it covers |
|---------|----------------|
| 1. Setup & Data Loading | Libraries, cleaning, fiscal year handling |
| 2. EDA | Key statistics, flow ranges, growth multiples |
| 3. Centrepiece Chart | FII vs DII dual area chart — the divergence |
| 4. Crisis Behaviour | Correlation analysis, grouped flow comparison per crisis |
| 5. DII Composition | MF AUM CAGR, folio growth, LIC equity trajectory |
| 6. Sensex Journey | Index levels with crisis moments marked |
| 7. Hypothesis Test | DII dominance ratio, turning point identification, verdict |

---

## Key Findings

| Metric | Value |
|--------|-------|
| MF AUM growth (2000–2025) | 81x — ₹0.91L Cr to ₹73.73L Cr |
| Retail investor folios growth | 27x — 101 lakh to 2,739 lakh |
| LIC equity growth | 137x — ₹0.11L Cr to ₹15.11L Cr |
| FY 2024-25 DII net flow | ₹8,49,000 Crore (all-time high) |
| FY 2024-25 FII net flow | ₹2,26,000 Crore (net outflow) |
| DII/FII ratio FY 2024-25 | DII deployed 3.76x more than FII pulled out |

**The turning point:** 2019-20 (COVID) — first crisis where DII response was structurally larger than FII selling at scale. Confirmed and amplified in 2022.

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Jupyter Notebook
```bash
jupyter notebook FII_to_DII_Analysis.ipynb
```

### Streamlit Dashboard
```bash
streamlit run dashboard.py
```
Opens at `http://localhost:8501`

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| pandas | Data loading, cleaning, analysis |
| matplotlib | All visualizations |
| numpy | Numerical operations, CAGR calculations |
| Streamlit | Interactive dark-themed dashboard |
| Jupyter | Notebook-based analysis with narrative |

---

## Requirements
```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
streamlit>=1.30
jupyter>=1.0
notebook>=7.0
plotly>=5.0
```

---

### What This Project Is Not

This is not a trading strategy, a stock recommendation, or a prediction model. It is a historical structural analysis of capital flow patterns in Indian equity markets. The data reflects publicly available information from regulatory and institutional sources.

---

#### ***Gopal Vashistha | Data Analysis Project | Python  pandas Streamlit Matplotlib Plotly***
 ****| Fiscal year basis throughout****
=======

