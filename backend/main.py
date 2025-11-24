from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scoring import Scorer
import os
import logging
import hashlib
import json
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
ACCESS_LOG_FILE = LOGS_DIR / "access.log"

app = FastAPI(
    title="AI Communication Scoring API",
    description="API for scoring spoken communication transcripts",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    client_ip = request.client.host if request.client else "unknown"
    ip_hash = hashlib.md5(client_ip.encode()).hexdigest()[:8]
    
    response = await call_next(request)
    
    duration = (datetime.now() - start_time).total_seconds()
    
    log_entry = {
        "timestamp": start_time.isoformat(),
        "ip_hash": ip_hash,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": round(duration * 1000, 2)
    }
    
    with open(ACCESS_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, "Case study for interns.xlsx")

scorer = None
scorer_error = None

try:
    logger.info(f"Initializing scorer with Excel file: {EXCEL_PATH}")
    scorer = Scorer(EXCEL_PATH)
    logger.info(f"Scorer initialized successfully with {len(scorer.rubric)} rubric items")
except Exception as e:
    scorer_error = str(e)
    logger.error(f"Error initializing scorer: {e}", exc_info=True)

class ScoreRequest(BaseModel):
    transcript: str

class ScoreResponse(BaseModel):
    overall_score: float
    total_points: float
    max_points: int
    word_count: int
    wpm: float
    ttr: float
    details: list
    summary: dict

def transform_response(raw_result):
    stats = raw_result['stats']
    breakdown = raw_result['breakdown']
    
    total_points = sum(item['score'] for item in breakdown)
    max_points = sum(item['max'] for item in breakdown)
    
    details = []
    category_scores = {
        "content_structure": 0,
        "speech_rate": 0,
        "language_grammar": 0,
        "clarity": 0,
        "engagement": 0
    }
    
    for item in breakdown:
        metric_lower = item['metric'].lower()
        
        if "salutation" in metric_lower or "presence" in metric_lower or "flow" in metric_lower:
            category = "Content & Structure"
            category_scores["content_structure"] += item['score']
        elif "speech rate" in metric_lower or "wpm" in metric_lower:
            category = "Speech Rate"
            category_scores["speech_rate"] += item['score']
        elif "grammar" in metric_lower or "vocabulary" in metric_lower:
            category = "Language & Grammar"
            category_scores["language_grammar"] += item['score']
        elif "filler" in metric_lower:
            category = "Clarity"
            category_scores["clarity"] += item['score']
        elif "sentiment" in metric_lower or "engagement" in metric_lower:
            category = "Engagement"
            category_scores["engagement"] += item['score']
        else:
            category = "General"
        
        if "grammar" in metric_lower or "sentiment" in metric_lower:
            approach = "NLP"
        elif "presence" in metric_lower or "salutation" in metric_lower:
            approach = "Rule-based + NLP"
        else:
            approach = "Rule-based"
        
        details.append({
            "criteria": category,
            "metric": item['metric'],
            "score": item['score'],
            "max_score": item['max'],
            "feedback": item['feedback'],
            "approach": approach
        })
    
    return {
        "overall_score": raw_result['overall_score'],
        "total_points": round(total_points, 2),
        "max_points": int(max_points),
        "word_count": stats['word_count'],
        "wpm": round(stats['wpm'], 1),
        "ttr": round(stats['ttr'], 3),
        "details": details,
        "summary": category_scores
    }

@app.get("/")
async def root():
    return {
        "message": "AI Communication Scoring API",
        "status": "ok" if scorer else "error",
        "error": scorer_error if scorer_error else None,
        "endpoints": {
            "/score": "POST - Score a transcript",
            "/health": "GET - Health check",
            "/rubric": "GET - Get rubric structure"
        }
    }

@app.post("/score", response_model=ScoreResponse)
async def score_transcript(request: ScoreRequest):
    if not scorer:
        raise HTTPException(status_code=500, detail=f"Scorer not initialized: {scorer_error}")
    
    if not request.transcript or not request.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")
    
    try:
        logger.info(f"Scoring transcript ({len(request.transcript.split())} words)")
        raw_result = scorer.score_transcript(request.transcript)
        logger.info(f"Scoring complete: {raw_result['overall_score']}/100")
        
        return transform_response(raw_result)
    except Exception as e:
        logger.error(f"Error scoring transcript: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {
        "status": "ok" if scorer else "error",
        "scorer_initialized": scorer is not None,
        "error": scorer_error if scorer_error else None
    }

@app.get("/rubric")
async def get_rubric():
    if not scorer:
        raise HTTPException(status_code=500, detail=f"Scorer not initialized: {scorer_error}")
    
    return {
        "total_items": len(scorer.rubric),
        "rubric": scorer.rubric
    }

@app.get("/analytics/download")
async def download_analytics():
    try:
        if not ACCESS_LOG_FILE.exists():
            return {"total_requests": 0, "logs": [], "message": "No logs yet"}
        
        with open(ACCESS_LOG_FILE, "r", encoding="utf-8") as f:
            logs = [json.loads(line.strip()) for line in f if line.strip()]
        
        score_requests = [log for log in logs if log["path"] == "/score"]
        
        return {
            "total_requests": len(logs),
            "score_requests": len(score_requests),
            "logs": logs[-50:],
            "message": "Showing last 50 requests"
        }
    except Exception as e:
        return {"error": str(e), "total_requests": 0, "logs": []}
