# AI Communication Scoring Tool

An intelligent system for analyzing and scoring spoken communication skills from transcribed text. Built as part of the Nirmaan AI Intern Case Study.

## 🎯 Overview

This tool evaluates communication transcripts across multiple dimensions:
- **Content & Structure**: Salutation, keyword presence, logical flow
- **Speech Rate**: Words per minute analysis
- **Language & Grammar**: Grammar accuracy and vocabulary richness
- **Clarity**: Filler word detection
- **Engagement**: Sentiment and positivity analysis

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Backend**: FastAPI + Python
- **NLP**: Sentence Transformers, VADER Sentiment, LanguageTool
- **Scoring**: Rule-based + NLP hybrid approach

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and pnpm
- Python 3.11+
- uv (Python package manager)

### Local Development

**Backend:**
```bash
cd backend
uv sync
uv run uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
pnpm install
pnpm dev
```

Visit `http://localhost:5173` to use the application.

## 📊 Scoring Methodology

The system uses a data-driven approach combining:
1. **Rule-based scoring** for structure and flow
2. **NLP-based analysis** for grammar and sentiment
3. **Semantic similarity** for keyword presence
4. **Statistical metrics** for vocabulary richness

Total score: 100 points across 8 metrics

## 📁 Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   ├── scoring.py           # Main scorer class
│   ├── transcript_scorer.py # Metric calculations
│   ├── stats_calculator.py  # Statistical analysis
│   ├── rubric_loader.py     # Excel rubric parser
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities
│   │   └── App.tsx          # Main application
│   └── package.json         # Node dependencies
└── Case study for interns.xlsx  # Scoring rubric
```

## 🌐 Deployment

- **Frontend**: See [DEPLOYMENT_FRONTEND.md](./DEPLOYMENT_FRONTEND.md)
- **Backend**: See [DEPLOYMENT_BACKEND.md](./DEPLOYMENT_BACKEND.md)

## 🔍 API Endpoints

- `POST /score` - Score a transcript
- `GET /health` - Health check
- `GET /rubric` - Get scoring rubric
- `GET /` - API information

## 📝 Sample Usage

```json
POST /score
{
  "transcript": "Hello everyone, my name is John..."
}

Response:
{
  "overall_score": 75.5,
  "total_points": 75.5,
  "max_points": 100,
  "word_count": 150,
  "wpm": 150,
  "ttr": 0.75,
  "details": [...],
  "summary": {...}
}
```

## 🛠️ Technologies Used

**Backend:**
- FastAPI - Modern Python web framework
- Sentence Transformers - Semantic similarity
- VADER - Sentiment analysis
- LanguageTool - Grammar checking
- Pandas - Data processing

**Frontend:**
- React 18 - UI library
- TypeScript - Type safety
- Vite - Build tool
- TailwindCSS - Styling
- Shadcn/ui - Component library

## 📄 License

This project was created as part of the Nirmaan AI Intern Case Study.

## 👤 Author

Mayuresh (PREDATOR)

---

**Note**: This tool is designed for educational purposes and provides automated scoring based on predefined rubrics. Human review is recommended for final assessments.
