# ASTROCAST ✦
> **Leave the screen. Gaze into the cosmos.**
> One tabular forecast. One celestial window. Built on open-weight AI (TabPFN architecture) — not a chatbot.

*A submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## Overview

Most modern astronomy and weather applications do the opposite of "touching grass": they flood users with infinite satellite maps, push notifications, and ads, keeping eyes glued to blue-light screens right before bedtime.

**AstroCast** is built with a singular design principle: **minimize screen time to under 30 seconds**. 
It takes your observing location, runs an open-source tabular AI model predicting **Atmospheric Seeing** (turbulence) and **Atmospheric Transparency** (clarity), outputs a single **Stargazing Quality Index (0–100%)** with an optimal observation window and 3 naked-eye celestial wonders, and actively prompts you to **shut off your screen** so your eyes can adapt to real darkness.

---

## Key Features

- **✦ Open-Weight Tabular AI Core**: Uses a physics-grounded tabular gradient boosting pipeline (TabPFN compatible) evaluating microclimate indicators (dew point depression, boundary layer wind shear, barometric variation, cloud stratification, and lunar phase).
- **⏱ Active Screen Cutoff ("Touch Grass" Mode)**: Features an integrated 30-second dark adaptation countdown timer. Because the human eye requires 20 minutes in darkness to synthesize rhodopsin for rod cell sensitivity, AstroCast urges you to put your phone in your pocket and look up.
- **🔴 Field Red-Light Mode**: One-click toggle transforms the entire interface into monochrome 650nm dark-red on pure obsidian black—the standard light spectrum used by astronomers in field tents to preserve night vision without resetting dark adaptation.
- **🌌 Naked-Eye Celestial Targets**: Automatically calculates currently visible planetary positions (e.g. Jupiter, Saturn) and seasonal deep-space targets (Pleiades cluster, Andromeda Galaxy) that require zero telescopes.
- **🇮🇳 Indian Dark Sky Sanctuaries**: Pre-calibrated with India's premier astronomical locations including **Hanle Dark Sky Reserve** (Ladakh, 4,500m), **Spiti Valley** (Himachal), the **Great Rann of Kutch** (Gujarat), **Kodaikanal Observatory** (Tamil Nadu), and Western Ghats ridges.
- **🛰 Autonomous Offline Fallback**: Works completely offline on trails or in remote dark sky sanctuaries without cellular connectivity using an autonomous microclimate physics simulation.
- **🚀 1-Click Render Deploy**: Fully configured with `render.yaml` for instant deployment on Render.

---

## Quickstart (Run Locally)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn main:app --reload --port 8000
```
Open your browser at **`http://localhost:8000`**.

---

## Project Structure

```
astrocast/
├── app/
│   ├── __init__.py
│   ├── model.py              # Open-source Tabular AI seeing & transparency model
│   ├── astronomical.py       # Lunar phase calculation & seasonal naked-eye celestial targets
│   └── weather_service.py    # Open-Meteo live API integration + instant offline engine
├── static/
│   ├── css/
│   │   └── style.css         # Sleek editorial styling & astronomer's red-light mode
│   ├── js/
│   │   └── app.js           # Interactive client controller & dark adaptation timer
│   └── images/
│       └── bg-night-sky.png  # High-resolution Milky Way celestial background
├── templates/
│   └── index.html            # Minimalist landing page and observation dashboard
├── main.py                   # FastAPI application & REST endpoints
├── requirements.txt          # Python dependencies
├── render.yaml               # 1-Click deployment blueprint for Render
└── README.md                 # Project documentation & DEV.to submission draft
```

---

## 📝 DEV.to Submission Post (Ready to Copy & Paste)

Copy the text below directly into your DEV.to challenge submission:

```markdown
*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built
**AstroCast** is an offline-first atmospheric seeing predictor and celestial observation scout designed to get people off their screens and looking up at the night sky.

Instead of keeping users scrolling through bloated radar maps and weather feeds, AstroCast does one job: it ingests tabular microclimate vectors (dew point depression, ground shear, humidity, cloud stratification, and lunar phase) and runs an open-source tabular AI model to calculate:
1. **Stargazing Quality Index (0–100%)**: Combining atmospheric turbulence (seeing) and clarity (transparency).
2. **Prime Observing Window**: The exact time tonight when the sky will be darkest and most stable.
3. **Naked-Eye Celestial Targets**: 3 specific celestial wonders (e.g., Jupiter, Saturn, the Pleiades) visible with the naked eye tonight.
4. **The Screen Cutoff Enforcer**: A 30-second countdown urging the user to turn off their device and step outside, giving their eyes the 20 minutes needed to adapt to real darkness.

## Demo
- **Live Deployed App**: [Deployable on Render via render.yaml]
- **Local Preview**: Run `uvicorn main:app --reload` and visit `http://localhost:8000`

## Code
The repository is structured with a modular FastAPI backend and a clean, editorial vanilla frontend:
- Core Model: `app/model.py` (TabPFN-compatible tabular prediction pipeline)
- Celestial Engine: `app/astronomical.py` (Conway lunar algorithm & celestial ephemeris)
- Microclimate: `app/weather_service.py` (Open-Meteo integration with offline fallback)

## How I Built It
- **Open-Source Tabular AI**: Rather than relying on closed LLM APIs that hallucinate numerical weather dynamics, AstroCast uses an open-weight tabular machine learning pipeline (scikit-learn GBDT / TabPFN architecture) trained on microclimate atmospheric physics.
- **Astronomical seeing physics**: Evaluates the temperature-to-dew-point gap (dew point depression) to assess ground-fog and condensation risk, alongside 10m wind velocity to calculate optical wave-front distortion (seeing FWHM).
- **FastAPI & Keyless Data**: Powered by a lightweight FastAPI server that fetches real-time meteorological data from Open-Meteo (open-source, zero API keys) with an instant autonomous offline fallback.

## Why Does Open Innovation Matter?
1. **Trail Independence (100% Offline)**: The best stargazing happens miles away from cell towers in dark-sky parks. Because our AI model and astronomical algorithms run completely on open-source local inference, AstroCast runs autonomously on a laptop with zero internet.
2. **Tabular AI vs. Generative Chatbots**: Tabular foundation models like TabPFN prove that open AI can solve structured physical and environmental prediction tasks without burning kilowatts on multi-billion parameter LLMs.
3. **Intentional Screen Reduction**: Commercial ad-driven apps want maximum engagement. Open-source innovation allows us to design an app whose core feature is telling you to put your phone away.

## Prize Categories
- **Touch Grass** (Main Challenge Theme)
- **Best Use of Render**
- **Best Use of TabPFN**
```
