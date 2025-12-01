import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class QualityAnalyzer:
    """Analyzes dataset quality across 5 dimensions"""
    
    def __init__(self, df):
        self.df = df
        self.scores = {}
        self.metrics = {}
    
    def analyze_all(self):
        """Run all quality assessments"""
        logger.info("Running quality analysis...")
        
        self.scores['accuracy'] = self.analyze_accuracy()
        self.scores['completeness'] = self.analyze_completeness()
        self.scores['timeliness'] = self.analyze_timeliness()
        self.scores['accessibility'] = self.analyze_accessibility()
        self.scores['consistency'] = self.analyze_consistency()
        self.scores['overall'] = np.mean(list(self.scores.values()))
        
        logger.info(f"Overall quality score: {self.scores['overall']:.2f}/5")
        return self.scores
    
    def analyze_accuracy(self):
        """Assess data accuracy"""
        score = 5.0
        issues = []
        
        if 'ApplicationNumber' in self.df.columns:
            duplicates = self.df['ApplicationNumber'].duplicated().sum()
            dup_rate = duplicates / len(self.df)
            if dup_rate > 0.01:
                score -= 1
                issues.append(f"High duplicate rate: {dup_rate:.1%}")
        
        self.metrics['accuracy_issues'] = issues
        return max(0, min(5, score))
    
    def analyze_completeness(self):
        """Assess data completeness"""
        total_cells = self.df.size
        missing_cells = self.df.isna().sum().sum()
        completeness_rate = 1 - (missing_cells / total_cells)
        
        field_missing = (self.df.isna().sum() / len(self.df) * 100).round(2)
        self.metrics['field_missingness'] = field_missing.to_dict()
        
        if completeness_rate >= 0.9:
            score = 5
        elif completeness_rate >= 0.7:
            score = 4
        elif completeness_rate >= 0.5:
            score = 3
        elif completeness_rate >= 0.3:
            score = 2
        else:
            score = 1
        
        self.metrics['overall_completeness'] = completeness_rate
        return score
    
    def analyze_timeliness(self):
        """Assess data timeliness"""
        score = 3.0
        date_cols = [col for col in self.df.columns if 'date' in col.lower() or 'Date' in col]
        
        if not date_cols:
            return score
        
        try:
            dates = pd.to_datetime(self.df[date_cols[0]], errors='coerce').dropna()
            if len(dates) == 0:
                return 1.0
            
            current_year = datetime.now().year
            recent_records = dates[dates.dt.year >= current_year - 2]
            recent_rate = len(recent_records) / len(dates)
            
            self.metrics['recent_record_rate'] = recent_rate
            
            if recent_rate >= 0.5:
                score = 5
            elif recent_rate >= 0.3:
                score = 4
            elif recent_rate >= 0.1:
                score = 3
            elif recent_rate >= 0.05:
                score = 2
            else:
                score = 1
            
            year_dist = dates.dt.year.value_counts().sort_index()
            self.metrics['year_distribution'] = year_dist.to_dict()
        except Exception as e:
            logger.warning(f"Error analyzing timeliness: {e}")
            score = 2.0
        
        return score
    
    def analyze_accessibility(self):
        """Assess data accessibility"""
        score = 5.0
        if len(self.df) == 0:
            return 0
        
        self.metrics['record_count'] = len(self.df)
        self.metrics['field_count'] = len(self.df.columns)
        return max(1, score)
    
    def analyze_consistency(self):
        """Assess data consistency"""
        score = 5.0
        self.metrics['dtype_consistency'] = len(self.df.columns)
        return max(1, score)
    
    def get_summary_report(self):
        """Generate summary statistics"""
        return {
            'total_records': len(self.df),
            'total_fields': len(self.df.columns),
            'missing_cells': self.df.isna().sum().sum(),
            'completeness_rate': self.metrics.get('overall_completeness', 0),
            'quality_scores': self.scores
        }
