import pandas as pd
import xml.etree.ElementTree as ET
from lxml import etree
import logging
import numpy as np

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
        from datetime import datetime, timedelta
        
        logger.info(f"Creating sample CIPO dataset with {n_records} records")
        
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
                    year = np.random.randint(2020, 2026)
                month = np.random.randint(1, 13)
                day = np.random.randint(1, 28)
                dates.append(f'{year}-{month:02d}-{day:02d}')
            return dates
        
        data = {
            'ApplicationNumber': [f'CA{1000000 + i}' for i in range(n_records)],
            'FilingDate': generate_filing_dates(n_records),
            'MarkCategory': np.random.choice(
                ['Word', 'Design', 'Combined', None], 
                n_records, 
                p=[0.15, 0.03, 0.02, 0.80]
            ),
            'MarkFeature': np.random.choice(
                ['Standard', 'Color', None], 
                n_records, 
                p=[0.10, 0.05, 0.85]
            ),
            'MarkDescription': [
                f'Trademark {i}' if np.random.random() > 0.82 else None 
                for i in range(n_records)
            ],
            'ImageFile': np.random.choice(
                ['image.png', None], 
                n_records, 
                p=[0.15, 0.85]
            ),
            'CurrentStatus': np.random.choice(
                ['Registered', 'Pending', 'Abandoned', 'Dead'], 
                n_records
            ),
            'Classification': np.random.choice(
                [f'Nice Class {i}' for i in range(1, 46)], 
                n_records
            )
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Created {len(df)} sample trademark records")
        return df
    
    def load_ontario_employment(self, filepath='data/ontario_employment.csv'):
        """Load Ontario employment standards dataset"""
        logger.info(f"Loading Ontario employment data from {filepath}")
        
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            df.columns = df.columns.str.strip()
            logger.info(f"Loaded {len(df)} employment violation records")
            return df
            
        except FileNotFoundError:
            logger.warning(f"File not found: {filepath}")
            logger.info("Creating sample Ontario employment data...")
            return self.create_sample_ontario_data()
            
        except Exception as e:
            logger.error(f"Error loading Ontario data: {e}")
            return self.create_sample_ontario_data()
    
    def create_sample_ontario_data(self, n_records=1000):
        """Create sample Ontario employment violations data"""
        logger.info(f"Creating sample Ontario dataset with {n_records} records")
        
        np.random.seed(42)
        
        data = {
            'ViolationType': np.random.choice(
                ['Wage Theft', 'Overtime', 'Termination', 'Vacation', 'Holiday', 'Other'],
                n_records,
                p=[0.35, 0.17, 0.27, 0.13, 0.05, 0.03]
            ),
            'Year': np.random.randint(2012, 2025, n_records),
            'City': np.random.choice(
                ['Toronto', 'Ottawa', 'Hamilton', 'London', 'Mississauga', 'Other'],
                n_records,
                p=[0.35, 0.15, 0.12, 0.08, 0.08, 0.22]
            ),
            'Amount': np.random.uniform(500, 50000, n_records).round(2),
            'Status': np.random.choice(
                ['Resolved', 'Pending', 'In Progress'],
                n_records,
                p=[0.7, 0.2, 0.1]
            )
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Created {len(df)} sample violation records")
        return df
