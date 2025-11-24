from sentence_transformers import SentenceTransformer
from rubric_loader import RubricLoader
from stats_calculator import StatsCalculator
from transcript_scorer import TranscriptScorer

class Scorer:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        
        print("Loading AI Models...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.stats_calculator = StatsCalculator()
        
        print("Loading rubric from Excel...")
        rubric_loader = RubricLoader(excel_path)
        self.rubric = rubric_loader.load()
        print(f"Rubric loaded: {len(self.rubric)} criteria rows found.")
        
        self.scorer = TranscriptScorer(self.rubric, self.stats_calculator)
    
    def score_transcript(self, transcript: str, duration_sec: int = 60):
        return self.scorer.score(transcript, duration_sec)

if __name__ == "__main__":
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(base_dir, "Case study for interns.xlsx")
    sample_path = os.path.join(base_dir, "Sample text for case study.txt")
    
    print("Initializing Scorer...")
    scorer = Scorer(excel_path)
    
    print("\nReading sample transcript...")
    with open(sample_path, "r", encoding="utf-8") as f:
        transcript = f.read()
    
    print(f"Transcript: {len(transcript.split())} words\n")
    
    print("Scoring transcript...")
    result = scorer.score_transcript(transcript)
    
    print("\n" + "="*80)
    print("SCORING RESULTS")
    print("="*80)
    print(f"\nOverall Score: {result['overall_score']}/100")
    print(f"\nStats:")
    for key, value in result['stats'].items():
        print(f"  {key}: {value}")
    
    print(f"\nBreakdown:")
    for item in result['breakdown']:
        print(f"\n  {item['metric']}")
        print(f"    Score: {item['score']}/{item['max']}")
        print(f"    Feedback: {item['feedback']}")