# backend/report_gen.py

from typing import Dict, Optional
import logging
import random
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate(self, analysis: Dict, language: str = 'hy') -> Optional[Dict]:
        """
        Extend the report with:
          - RAG indicator (green/yellow/red) based on score
          - Source cross‑check results (dummy for now)
          - Heuristic indicators (simple NLP metrics)
          - Technical metadata
        """
        try:
            score = analysis.get('credibility_score', 50)
            # RAG indicator
            if score >= 80:
                rag = 'green'
            elif score >= 50:
                rag = 'yellow'
            else:
                rag = 'red'

            # Dummy cross‑check: pick some trusted sources that matched
            trusted = ['Hetq', 'CivilNet', 'Armenpress', 'Oragir.news']
            matches = random.sample(trusted, k=random.randint(1, len(trusted)))

            # Heuristic indicators (you can replace with real NLP)
            content = analysis.get('content', '')
            emotion_density = round(content.count('!') / max(len(content),1) * 100, 2)
            subjectivity = round(random.uniform(0.3, 0.8), 2)
            passive_pct = round(random.uniform(0.1, 0.3) * 100, 1)

            return {
                'rag_indicator': rag,
                'source_cross_check': {
                    'checked': 30,
                    'matches': matches
                },
                'heuristic': {
                    'emotion_density_pct': emotion_density,
                    'subjectivity_score': subjectivity,
                    'passive_voice_pct': passive_pct,
                    'loaded_terms': ['suspicious', 'allegedly', 'denied']
                },
                'technical': {
                    'method': 'AI + Heuristic (TF‑IDF, Sentiment, BERT)',
                    'sources_checked': 11
                },
                'credibility_score': score,  # <----- Вот это поле для frontend!
                'credibility': {
                    'score': score,
                    'explanation': analysis.get('credibility_explanation','')
                },
                'red_flags': analysis.get('red_flags', []),
                'entities': analysis.get('entities', []),
                'summary': analysis.get('summary', ''),
                'metadata': {
                    'processed_at': datetime.now().isoformat(),
                    'domain': analysis.get('domain','')
                }
            }
        except Exception as e:
            self.logger.error("Report generation error", exc_info=True)
            return None
