#!/usr/bin/env python3
"""
YSSL Data Quality Assessment Tool
Main execution script
"""

import sys
import logging
from src.data_loader import DataLoader
from src.quality_analyzer import QualityAnalyzer
from src.visualizer import QualityVisualizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    print("=" * 60)
    print("YSSL Data Quality Assessment Tool")
    print("=" * 60)
    print()
    
    # Step 1: Load Data
    print("📊 Step 1: Loading dataset...")
    loader = DataLoader()
    
    # Create sample data (replace with real data loading if available)
    df = loader.create_sample_data(n_records=1000)
    
    print(f"✓ Loaded {len(df)} records with {len(df.columns)} fields")
    print()
    
    # Step 2: Analyze Quality
    print("🔍 Step 2: Analyzing data quality...")
    analyzer = QualityAnalyzer(df)
    scores = analyzer.analyze_all()
    
    print("\n📈 Quality Scores:")
    print(f"  • Overall:       {scores['overall']:.2f}/5")
    print(f"  • Accuracy:      {scores['accuracy']:.2f}/5")
    print(f"  • Completeness:  {scores['completeness']:.2f}/5")
    print(f"  • Timeliness:    {scores['timeliness']:.2f}/5")
    print(f"  • Accessibility: {scores['accessibility']:.2f}/5")
    print(f"  • Consistency:   {scores['consistency']:.2f}/5")
    print()
    
    # Step 3: Generate Visualizations
    print("📊 Step 3: Generating visualizations...")
    viz = QualityVisualizer(output_dir='outputs')
    
    try:
        viz.plot_temporal_distribution(df, 'FilingDate', 
                                      "Trademark Applications by Year")
        viz.plot_missingness(analyzer.metrics['field_missingness'],
                           "Missing Value Rate by Field")
        viz.plot_quality_radar(scores, "Data Quality Assessment")
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}")
    
    print()
    print("=" * 60)
    print("✅ Analysis Complete!")
    print(f"📁 Results saved in: ./outputs/")
    print("=" * 60)

if __name__ == "__main__":
    main()
