#!/usr/bin/env python3
"""
Ontario Employment Standards Analysis
"""

import logging
from src.data_loader import DataLoader
from src.quality_analyzer import QualityAnalyzer
from src.visualizer import QualityVisualizer

logging.basicConfig(level=logging.INFO)

def main():
    print("=" * 60)
    print("Ontario Employment Standards - Quality Analysis")
    print("=" * 60)
    print()
    
    # Load data
    loader = DataLoader()
    df = loader.load_ontario_employment()
    
    if df.empty:
        print("No data loaded")
        return
    
    print(f"✓ Loaded {len(df)} violation records")
    print()
    
    # Analyze quality
    analyzer = QualityAnalyzer(df)
    scores = analyzer.analyze_all()
    
    print("\n📈 Quality Scores:")
    for dim, score in scores.items():
        print(f"  • {dim.capitalize()}: {score:.2f}/5")
    print()
    
    # Generate visualizations
    viz = QualityVisualizer(output_dir='outputs/ontario')
    
    if 'ViolationType' in df.columns:
        viz.plot_violations_by_type(df, 'ViolationType')
    
    if 'Year' in df.columns:
        viz.plot_violations_by_year(df, 'Year')
    
    if 'City' in df.columns:
        viz.plot_geographic_distribution(df, 'City')
    
    viz.plot_quality_radar(scores, "Ontario Data Quality")
    
    print("=" * 60)
    print("Analysis Complete!")
    print("Results saved in: ./outputs/ontario/")
    print("=" * 60)

if __name__ == "__main__":
    main()
