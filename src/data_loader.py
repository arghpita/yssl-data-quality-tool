import pandas as pd
import xml.etree.ElementTree as ET
from lxml import etree
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Loads and parses regulatory datasets"""
    
    def __init__(self):
        self.data = None
    
    def load_csv(self, filepath):
        """Load CSV dataset"""
        logger.info(f"Loading CSV from {filepath}")
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            try:
                df = pd.read_csv(filepath, encoding='latin-1')
                return df
            except:
                return pd.DataFrame()
    
    def create_sample_data(self, n_records=1000):
        """Create sample CIPO-like dataset"""
        import numpy as np
        from datetime import datetime, timedelta
        
        logger.info(f"Creating sample dataset with {n_records} records")
        
        np.random.seed(42)
        
        def generate_filing_dates(n):
            dates = []
            for _ in range(n):
                rand = np.random.random()
                if rand < 0.70:
                    year = np.random.randint(1980, 2000)
                elif rand < 0.85:
                    year = np.random.randint(2000, 2010)
                elif rand < 0.95:
                    year = np.random.randint(2010, 2020)
                else:
                    year = np.random.randint(2020, 2025)
                month = np.random.randint(1, 13)
                day = np.random.randint(1, 28)
                dates.append(f'{year}-{month:02d}-{day:02d}')
            return dates
        
        data = {
            'ApplicationNumber': [f'CA{1000000 + i}' for i in range(n_records)],
            'FilingDate': generate_filing_dates(n_records),
            'MarkCategory': np.random.choice(['Word', 'Design', 'Combined', None], n_records, p=[0.15, 0.03, 0.02, 0.80]),
            'MarkFeature': np.random.choice(['Standard', 'Color', None], n_records, p=[0.10, 0.05, 0.85]),
            'MarkDescription': [f'Trademark {i}' if np.random.random() > 0.82 else None for i in range(n_records)],
            'ImageFile': np.random.choice(['image.png', None], n_records, p=[0.15, 0.85]),
            'CurrentStatus': np.random.choice(['Registered', 'Pending', 'Abandoned', 'Dead'], n_records),
            'Classification': np.random.choice([f'Nice Class {i}' for i in range(1, 46)], n_records)
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Created {len(df)} sample records")
        return df
