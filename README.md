<div align="center">

# 🔍 Wherelse
### Where else would you look?

**The elegant way to compare tools, apps & services.**  
Wherelse aggregates Reddit threads, online reviews, and feature breakdowns into structured, beautiful comparisons — so you can stop reading 40 tabs and just decide.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-wherelse.app-6C63FF?style=for-the-badge)](https://wherelse.app)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

</div>

---

## ✨ What is Wherelse?

Wherelse is a webapp that turns the chaos of online opinions into clean, structured comparisons.

You pick two (or more) services — say, **Notion vs Obsidian** — and Wherelse does the heavy lifting:

- 🕵️ Scrapes relevant **Reddit threads** and community discussions
- 📰 Pulls **online reviews** from trusted sources
- 📊 Extracts **feature comparisons** from documentation and listicles
- 🤖 Synthesizes everything into a **structured, readable summary**

No more doomscrolling. Just answers.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔄 **Live Aggregation** | Pulls fresh data from Reddit, review sites & more |
| 📋 **Structured Comparisons** | Side-by-side feature tables, pros/cons, use-case fit |
| 🧠 **AI Synthesis** | Summarizes community sentiment into digestible insights |
| 🔖 **Saved Comparisons** | Bookmark and revisit any comparison |
| 🌐 **Shareable Links** | Share a comparison with a single URL |
| 🎨 **Clean UI** | Minimal, fast, and elegant by design |

---

## 🛠️ Tech Stack

> _Replace with your actual stack_

- **Frontend** — [e.g. Next.js, React, Tailwind CSS]
- **Backend** — [e.g. Node.js, FastAPI, Supabase]
- **AI / NLP** — [e.g. OpenAI API, Claude API]
- **Data Sources** — Reddit API, [other sources]
- **Deployment** — [e.g. Vercel, Railway, Fly.io]

---

## 📦 Getting Started

### Prerequisites

```bash
node >= 18.0.0
npm >= 9.0.0
```

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/wherelse.git
cd wherelse

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
```

### Environment Variables

```env
# .env.local

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# AI
OPENAI_API_KEY=your_api_key   # or ANTHROPIC_API_KEY

# Database
DATABASE_URL=your_database_url
```

### Run Locally

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see it running.

---

## 📁 Project Structure

```
wherelse/
├── app/                  # Next.js app directory
│   ├── compare/          # Comparison pages
│   ├── api/              # API routes
│   └── ...
├── components/           # Reusable UI components
├── lib/                  # Utilities, scrapers, AI logic
│   ├── reddit.ts         # Reddit aggregation
│   ├── reviews.ts        # Review scraping
│   └── synthesize.ts     # AI synthesis logic
├── public/               # Static assets
└── README.md
```

---

## 🗺️ Roadmap

- [x] Core comparison engine
- [x] Reddit aggregation
- [ ] Review site integration
- [ ] User accounts & saved comparisons
- [ ] Browser extension
- [ ] API for developers
- [ ] Mobile app

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Commit your changes
git commit -m "feat: add your feature"

# Open a PR
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Made with ❤️ by [Your Name](https://github.com/yourusername)

**[wherelse.app](https://wherelse.app) · [Twitter](https://twitter.com/yourhandle) · [Issues](https://github.com/yourusername/wherelse/issues)**

</div>
