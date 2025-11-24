import re
from itertools import groupby

class TranscriptScorer:
    def __init__(self, rubric, stats_calculator):
        self.rubric = rubric
        self.stats_calculator = stats_calculator
    
    def score(self, transcript: str, duration_sec: int = 60):
        stats = self.stats_calculator.calculate(transcript, duration_sec)
        results = []
        total_score = 0
        max_possible = 0

        rubric_sorted = sorted(self.rubric, key=lambda x: x['metric'])
        
        for metric, rows in groupby(rubric_sorted, key=lambda x: x['metric']):
            rows = list(rows)
            metric_result = self._score_metric(metric, rows, transcript, stats)
            
            results.append(metric_result)
            total_score += metric_result['score']
            max_possible += metric_result['max']

        overall_score = (total_score / max_possible) * 100 if max_possible else 0
        
        return {
            "overall_score": round(overall_score, 1),
            "stats": stats,
            "breakdown": results
        }
    
    def _score_metric(self, metric, rows, transcript, stats):
        metric_lower = metric.lower()
        is_additive = "presence" in metric_lower or "flow" in metric_lower
        
        metric_score = 0
        metric_max = sum(r['points'] for r in rows) if is_additive else max(r['max_score'] for r in rows)
        feedback = []

        stat_val = self._get_stat_value(metric_lower, stats)

        if is_additive:
            metric_score, feedback = self._score_additive(rows, transcript, metric_lower)
        else:
            metric_score, feedback = self._score_exclusive(rows, transcript, stat_val)

        return {
            "metric": metric,
            "score": round(metric_score, 2),
            "max": round(metric_max, 2),
            "feedback": "; ".join(feedback) if feedback else "Criteria not met"
        }
    
    def _get_stat_value(self, metric_lower, stats):
        if "speech rate" in metric_lower or "wpm" in metric_lower:
            return stats['wpm']
        elif "grammar" in metric_lower:
            # Convert 0-1 scale to percentage (0-100) for range matching
            return stats['grammar'] * 100
        elif "vocabulary" in metric_lower:
            return stats['ttr']
        elif "filler" in metric_lower:
            return stats['filler_rate']
        elif "sentiment" in metric_lower or "engagement" in metric_lower or "positivity" in metric_lower:
            # Sentiment ranges in Excel are 0-1 scale, no conversion needed
            return stats['sentiment']
        return None
    
    def _score_additive(self, rows, transcript, metric_lower):
        metric_score = 0
        feedback = []
        
        # Handle flow metric separately
        if "flow" in metric_lower:
            for r in rows:
                if self._check_flow(transcript):
                    metric_score += r['points']
                    feedback.append("Correct flow: Salutation → Name → Details")
            return metric_score, feedback
        
        # Handle keyword presence with additive scoring
        if "presence" in metric_lower:
            # Define semantic patterns for each keyword concept
            keyword_patterns = {
                'name': r'\b(myself|my name is|i am|i\'m|called)\s+[A-Z]',
                'age': r'\b\d+\s*years?\s*old\b',
                'school': r'\b(school|studying in)\b',
                'class': r'\b(class|grade)\s*\d',
                'family': r'\b(family|mother|father|parent|brother|sister|people in my family)\b',
                'hobbies': r'\b(enjoy|like|love|play|playing|hobby|hobbies)\b',
                'interest': r'\b(interest|passionate about)\b',
                'about family': r'\b(special.*family|family.*special|kind.*family|family.*kind)\b',
                'origin': r'\b(i am from|i\'m from|born in|native of|parents are from)\b',
                'location': r'\b(i live in|from [A-Z][a-z]+)\b',
                'ambition': r'\b(dream|goal|ambition|aspire|want to become)\b',
                'fun fact': r'\b(fun fact|interesting thing|unique about|special thing|don\'t know about me)\b',
                'strength': r'\b(strength|achievement|accomplish|award|good at)\b'
            }
            
            # Track which concepts have been found to avoid double-counting
            found_concepts = set()
            
            for r in rows:
                if r['keywords']:
                    points_per_keyword = r['points'] / len(r['keywords'])
                    
                    for keyword in r['keywords']:
                        keyword_lower = keyword.lower()
                        matched = False
                        concept_key = None
                        
                        # Try to match against known patterns
                        if 'name' in keyword_lower and 'about' not in keyword_lower:
                            concept_key = 'name'
                            if concept_key not in found_concepts and re.search(keyword_patterns['name'], transcript):
                                matched = True
                        
                        elif 'age' in keyword_lower:
                            concept_key = 'age'
                            if concept_key not in found_concepts and re.search(keyword_patterns['age'], transcript, re.IGNORECASE):
                                matched = True
                        
                        elif 'school' in keyword_lower and 'class' in keyword_lower:
                            # Combined School/Class keyword
                            concept_key = 'school_class'
                            if concept_key not in found_concepts:
                                if re.search(keyword_patterns['school'], transcript, re.IGNORECASE) or \
                                   re.search(keyword_patterns['class'], transcript, re.IGNORECASE):
                                    matched = True
                        
                        elif 'family' in keyword_lower and 'about' not in keyword_lower:
                            concept_key = 'family'
                            if concept_key not in found_concepts and re.search(keyword_patterns['family'], transcript, re.IGNORECASE):
                                matched = True
                        
                        elif 'hobi' in keyword_lower or ('interest' in keyword_lower and 'free time' in keyword_lower):
                            concept_key = 'hobbies_interest'
                            if concept_key not in found_concepts:
                                if re.search(keyword_patterns['hobbies'], transcript, re.IGNORECASE) or \
                                   re.search(keyword_patterns['interest'], transcript, re.IGNORECASE):
                                    matched = True
                        
                        elif 'about family' in keyword_lower:
                            concept_key = 'about_family'
                            if concept_key not in found_concepts and re.search(keyword_patterns['about family'], transcript, re.IGNORECASE):
                                matched = True
                        
                        elif 'origin' in keyword_lower and 'location' in keyword_lower:
                            concept_key = 'origin_location'
                            if concept_key not in found_concepts:
                                if re.search(keyword_patterns['origin'], transcript, re.IGNORECASE) or \
                                   re.search(keyword_patterns['location'], transcript, re.IGNORECASE):
                                    matched = True
                        
                        elif 'ambition' in keyword_lower or 'goal' in keyword_lower or 'dream' in keyword_lower:
                            concept_key = 'ambition'
                            if concept_key not in found_concepts and re.search(keyword_patterns['ambition'], transcript, re.IGNORECASE):
                                matched = True
                        
                        elif 'fun fact' in keyword_lower or 'interesting thing' in keyword_lower or 'unique' in keyword_lower:
                            concept_key = 'fun_fact'
                            if concept_key not in found_concepts and re.search(keyword_patterns['fun fact'], transcript, re.IGNORECASE):
                                matched = True
                        
                        elif 'strength' in keyword_lower or 'achievement' in keyword_lower:
                            concept_key = 'strength'
                            if concept_key not in found_concepts and re.search(keyword_patterns['strength'], transcript, re.IGNORECASE):
                                matched = True
                        
                        if matched and concept_key:
                            found_concepts.add(concept_key)
                            metric_score += points_per_keyword
                            feedback.append(f"{keyword}")
            
            return metric_score, feedback
        
        # Default additive behavior for other metrics
        for r in rows:
            if r['keywords']:
                found = [k for k in r['keywords'] if re.search(r'\b' + re.escape(k) + r'\b', transcript, re.IGNORECASE)]
                if len(r['keywords']) > 0:
                    points_per_kw = r['points'] / len(r['keywords'])
                    earned = min(len(found) * points_per_kw, r['points'])
                    metric_score += earned
                    if earned > 0:
                        feedback.append(f"Found {len(found)}/{len(r['keywords'])} keywords")
        
        return metric_score, feedback
    
    def _score_exclusive(self, rows, transcript, stat_val):
        rows.sort(key=lambda x: x['points'], reverse=True)
        
        for r in rows:
            if r['has_range'] and stat_val is not None:
                if r['min_val'] <= stat_val <= r['max_val']:
                    return r['points'], [f"{r['description']} ({stat_val:.2f})"]
            elif r['keywords']:
                for kw in r['keywords']:
                    if re.search(r'\b' + re.escape(kw) + r'\b', transcript, re.IGNORECASE):
                        return r['points'], [f"Matched: {kw}"]
        
        return 0, []
    
    def _check_flow(self, transcript):
        transcript_lower = transcript.lower()
        words = transcript_lower.split()
        
        salutation_words = ['hello', 'hi', 'good morning', 'good afternoon', 'good evening', 'greetings', 'hey']
        name_indicators = ['name', 'myself', 'i am', "i'm", 'called']
        detail_words = ['age', 'years old', 'year old', 'class', 'grade', 'school', 'family', 'study', 'studying']
        
        salutation_pos = -1
        for word in salutation_words:
            pos = transcript_lower.find(word)
            if pos != -1:
                salutation_pos = pos
                break
        
        name_pos = -1
        for phrase in name_indicators:
            pos = transcript_lower.find(phrase)
            if pos != -1:
                name_pos = pos
                break
        
        detail_pos = -1
        for word in detail_words:
            pos = transcript_lower.find(word)
            if pos != -1:
                detail_pos = pos
                break
        
        if salutation_pos != -1 and name_pos != -1:
            if salutation_pos < name_pos:
                if detail_pos != -1:
                    return name_pos < detail_pos
                return True
        
        return False
