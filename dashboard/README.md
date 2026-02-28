# Quantum Lab Dashboard

Interactive web dashboard for visualizing all 20 quantum computing experiments.

## Features

- **Overview** — 8 animated KPI cards, bar chart (experiments by level), donut chart (result distribution)
- **Experiments Explorer** — Filterable card grid of all 20 experiments with detail modals
- **AI vs Quantum Results** — Grouped bar chart comparing Classical vs Quantum accuracy
- **Concepts Map** — 14 quantum concepts with explanations and experiment references
- **Tech Stack** — Layered architecture display
- **About** — Credits and "Why This Matters" section

## How to Run

Just open `index.html` in any modern browser. No build tools or server needed.

```bash
cd dashboard
open index.html   # macOS
xdg-open index.html   # Linux
start index.html   # Windows
```

## Tech

- Pure HTML/CSS/JS — no framework
- Chart.js 4.4 via CDN for data visualization
- Responsive from 375px to 2560px
- Dark/light theme toggle
- Hash-based routing for sidebar navigation

## Live Demo

Deployed via Perplexity Sites.
