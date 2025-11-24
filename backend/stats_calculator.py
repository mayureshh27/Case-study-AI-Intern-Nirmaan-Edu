import re
import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class StatsCalculator:
    def __init__(self):
        try:
            # Use public API to avoid starting local Java server (saves ~300MB RAM)
            self.grammar_tool = language_tool_python.LanguageTool('en-US', remote_server='https://api.languagetool.org/v2/')
        except Exception as e:
            print(f"Warning: LanguageTool initialization failed: {e}")
            self.grammar_tool = None
        
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.filler_words = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah']
    
    def calculate(self, transcript: str, duration_sec: int = 60):
        words = transcript.split()
        word_count = len(words)
        
        return {
            "wpm": self._calculate_wpm(word_count, duration_sec),
            "ttr": self._calculate_ttr(words),
            "grammar": self._calculate_grammar(transcript, word_count),
            "sentiment": self._calculate_sentiment(transcript),
            "filler_rate": self._calculate_filler_rate(words, word_count),
            "word_count": word_count
        }
    
    def _calculate_wpm(self, word_count, duration_sec):
        return (word_count / duration_sec) * 60 if duration_sec else 0
    
    def _calculate_ttr(self, words):
        if not words:
            return 0
        unique = set(w.lower() for w in words)
        return len(unique) / len(words)
    
    def _calculate_grammar(self, transcript, word_count):
        if not self.grammar_tool or word_count == 0:
            return 1.0
        errors = len(self.grammar_tool.check(transcript))
        return max(0, 1 - ((errors / word_count) * 100) / 10)
    
    def _calculate_sentiment(self, transcript):
        sent = self.sentiment_analyzer.polarity_scores(transcript)
        return (sent['compound'] + 1) / 2
    
    def _calculate_filler_rate(self, words, word_count):
        if word_count == 0:
            return 0
        f_count = sum(1 for w in words if w.lower() in self.filler_words)
        return (f_count / word_count) * 100
