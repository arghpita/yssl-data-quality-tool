import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

class QualityVisualizer:
    """Creates visualizations for data quality reports"""
    
    def __init__(self, output_dir='outputs'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def plot_temporal_distribution(self, df, date_column, title="Temporal Distribution"):
        """Create temporal distribution chart"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
        year_counts = dates.dt.year.value_counts().sort_index()
        
        ax.bar(year_counts.index, year_counts.values, color='#8b5cf6', alpha=0.8, edgecolor='black')
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Records', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        for year, count in year_counts.items():
            ax.text(year, count + max(year_counts.values) * 0.01, 
                   f'{count:,}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/temporal_distribution.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
    
    def plot_missingness(self, field_missing_dict, title="Missing Value Rate by Field"):
        """Create missing value chart"""
        sorted_fields = sorted(field_missing_dict.items(), key=lambda x: x[1], reverse=True)
        fields = [f[0] for f in sorted_fields[:10]]
        missing_rates = [f[1] for f in sorted_fields[:10]]
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(fields, missing_rates, color='#3b82f6', alpha=0.8, edgecolor='black')
        
        for bar, rate in zip(bars, missing_rates):
            if rate > 80:
                bar.set_color('#ef4444')
            elif rate > 50:
                bar.set_color('#f97316')
            elif rate > 20:
                bar.set_color('#eab308')
            else:
                bar.set_color('#22c55e')
        
        ax.set_xlabel('Missing (%)', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        for i, (field, rate) in enumerate(zip(fields, missing_rates)):
            ax.text(rate + 2, i, f'{rate:.1f}%', va='center', fontsize=10)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/missing_values.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
    
    def plot_quality_radar(self, scores, title="Data Quality Radar Chart"):
        """Create quality radar chart"""
        categories = ['Accuracy', 'Completeness', 'Timeliness', 'Accessibility', 'Consistency']
        values = [
            scores.get('accuracy', 0),
            scores.get('completeness', 0),
            scores.get('timeliness', 0),
            scores.get('accessibility', 0),
            scores.get('consistency', 0)
        ]
        
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        values += values[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values, 'o-', linewidth=2, color='#3b82f6')
        ax.fill(angles, values, alpha=0.25, color='#3b82f6')
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=10)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/quality_radar.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
    
    def plot_violations_by_type(self, df, type_column='ViolationType', 
                                title="Employment Violations by Type"):
        """Create pie chart for violation types"""
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        type_counts = df[type_column].value_counts()
        colors = ['#ef4444', '#f97316', '#f59e0b', '#eab308', '#84cc16', '#22c55e']
        
        wedges, texts, autotexts = ax.pie(
            type_counts.values,
            labels=type_counts.index,
            autopct='%1.1f%%',
            colors=colors[:len(type_counts)],
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/violations_by_type.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
    
    def plot_violations_by_year(self, df, year_column='Year',
                                title="Employment Violations by Year (Ontario)"):
        """Create line chart for yearly trends"""
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        yearly_counts = df[year_column].value_counts().sort_index()
        
        ax.plot(yearly_counts.index, yearly_counts.values, 
                marker='o', linewidth=3, markersize=8,
                color='#8b5cf6')
        
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Violations', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for year, count in yearly_counts.items():
            ax.text(year, count + max(yearly_counts.values) * 0.02,
                   f'{count:,}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/violations_by_year.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
    
    def plot_geographic_distribution(self, df, location_column='City',
                                     title="Violations by City (Ontario)"):
        """Create bar chart for geographic distribution"""
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        location_counts = df[location_column].value_counts().head(10)
        
        bars = ax.bar(range(len(location_counts)), location_counts.values,
                      color='#3b82f6', alpha=0.8, edgecolor='black')
        
        # Highlight Toronto (first bar)
        bars[0].set_color('#10b981')
        
        ax.set_xticks(range(len(location_counts)))
        ax.set_xticklabels(location_counts.index, rotation=45, ha='right')
        ax.set_ylabel('Number of Violations', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Add value labels
        for i, (loc, count) in enumerate(location_counts.items()):
            ax.text(i, count + max(location_counts.values) * 0.01,
                   f'{count:,}', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/geographic_distribution.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
    
    def plot_ip_composition(self, composition_dict, title="IP Dataset Composition"):
        """Create donut chart for IP composition"""
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        labels = list(composition_dict.keys())
        sizes = list(composition_dict.values())
        colors = ['#3b82f6', '#8b5cf6', '#ec4899']
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors[:len(sizes)],
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        # Add donut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        filepath = f'{self.output_dir}/ip_composition.png'
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved {filepath}")
        return filepath
