# Macro Catalyst

Real-time macro intelligence terminal that tracks how Oil, VIX, 10Y Yields, Gold, S&P 500, and Bitcoin interact as a system — not in isolation.

Built for traders who want to understand what's driving BTC from a macro perspective and when the macro environment is working for or against them.

![Python](https://img.shields.io/badge/Python-3.10+-10b981?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-10b981?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat)

---

## What It Does

**Every number comes from a real API. Every signal is deterministic. No speculation. No fake data.**

### Command Center
- **Macro Confluence Bias** — Scores all 6 catalysts from -2 (risk-off) to +2 (risk-on). Every signal traceable to a factual input. Outputs: RISK-ON / LEAN RISK-ON / NEUTRAL / LEAN RISK-OFF / RISK-OFF.
- **Threat Board** — Visual proximity indicator showing how close each catalyst is to safe, caution, or danger thresholds. Direction arrows show which way things are heading.
- **6 Catalyst Cards** — Live price, zone status, 10-day trend, RSI for Oil, VIX, 10Y Yields, Gold, S&P 500, Bitcoin.
- **Correlations** — 30-day rolling correlations (OIL/BTC, VIX/BTC, GOLD/BTC, S&P/BTC, 10Y/BTC) showing whether macro signals are actually transmitting to crypto.
- **Oil Regime Timeline** — 12-month day count across zones with 30-day mini strip.
- **Economic Calendar** — Upcoming FOMC, CPI, NFP dates with context explaining why each event matters given current conditions.

### Intelligence Briefing
- **Macro Intelligence Briefing** — Rules-based narrative that reads all data and generates contextual analysis. Adapts to current conditions. Flags divergences (e.g., gold rising while VIX falling).
- **Impact Chains** — Visual cause-and-effect chains showing what's currently driving what (e.g., Iran tensions → Oil elevated → Inflation → Fed boxed in → Yields high → BTC headwind).
- **Bull/Bear Scenarios** — Conditional if-then chains. Not probability guesses — factual chains showing what happens if conditions change.

### Scenario Simulator
Standalone React animation that simulates a bear-to-bull macro scenario with animated charts, catalyst event cards, and a confluence bias gauge updating in real time. Built for screen recording.

---

## Data Sources

| Source | What | Why |
|--------|------|-----|
| [Hyperliquid API](https://api.hyperliquid.xyz) | Live WTI oil price (24/7) | Catches weekend geopolitical moves when TradFi is closed |
| [Yahoo Finance](https://finance.yahoo.com) | All historical data, all other live prices | Free, reliable, deep history |

No paid APIs. No API keys needed.

---

## Zone Thresholds

Every zone is calibrated from historical data, not arbitrary round numbers.

### Oil (WTI Crude)
| Zone | Range | Reasoning |
|------|-------|-----------|
| Depressed | < $58 | Demand destruction. COVID crash, 2015-16 bust territory |
| Stable | $58-$78 | Post-2020 recovery band. CPI manageable, Fed has flexibility |
| Elevated | $78-$95 | 2022 inflation crisis accelerated past ~$80 |
| Stress | $95-$115 | 4 of 5 oil shocks above ~$100 preceded recessions |
| Crisis | $115+ | 2008 hit $147, 2022 hit $130. Stagflation risk |

### VIX
| Zone | Range | Reasoning |
|------|-------|-----------|
| Low Fear | < 15 | Below long-term average. Complacency / risk-on |
| Normal | 15-20 | Standard operating range since 1990 |
| Elevated | 20-25 | Institutional hedging building |
| High Fear | 25-35 | Correction territory |
| Extreme | 35+ | Panic. Top 5% of all readings. Historically a contrarian signal |

### 10Y Treasury Yield
| Zone | Range | Reasoning |
|------|-------|-----------|
| Accommodative | < 3.0% | Risk assets benefit from low rates |
| Neutral | 3.0-3.8% | Manageable rate environment |
| Tightening | 3.8-4.5% | Growth pressure building |
| Restrictive | 4.5-5.0% | 2006-07 territory. Equity/crypto headwinds |
| Crisis | 5.0%+ | Severe tightness |

---

## Setup

```bash
git clone https://github.com/devbecrying-eng/macro-catalyst.git
cd macro-catalyst
pip install -r requirements.txt
streamlit run macro_catalyst.py
```

Opens at `http://localhost:8501`

### Requirements
- Python 3.10+
- Dependencies: `streamlit`, `yfinance`, `plotly`, `pandas`, `numpy`, `requests`, `streamlit-autorefresh`

---

## Architecture

```
macro-catalyst/
├── macro_catalyst.py          # Main Streamlit app
├── requirements.txt           # Python dependencies
├── macro-catalyst-trailer.jsx # Scenario simulator (React)
└── README.md
```

### Intelligence Engine
The briefing and scenario systems are entirely rules-based. No LLM calls, no AI generation. Every sentence maps to a data condition:

```
IF oil_zone == "STRESS" AND vix_direction == "RISING"
THEN "Oil in STRESS with VIX rising — double pressure on risk assets"
```

### Confluence Bias Scoring
Each catalyst contributes signals scored -2 to +2:
- **Zone position** — which regime zone the price sits in
- **Speed of move** — abnormal velocity detection across 24h/3d/7d windows
- **Zone transitions** — just entered a new regime = signal event

Inverted logic for fear assets (VIX rising = risk-off, Gold rising = risk-off).

---

## Roadmap

- [ ] News sentiment integration (RSS headlines)
- [ ] DXY (Dollar Index) as 7th catalyst
- [ ] Notification alerts on zone transitions
- [ ] Mobile-responsive layout
- [ ] Historical scenario backtesting

---

## License

MIT

---

*Built by Tobi — Royalty Island Kennels. No paid APIs. No fake data. Signal over noise.*
