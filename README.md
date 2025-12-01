# YSSL Data Quality Assessment Tool

Evaluates Canadian regulatory datasets for ERP integration readiness.

## Features
- 5-dimension quality scoring framework
- Automated visualization generation
- Support for CIPO trademark and Ontario employment data
- PDF report generation

## Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/yssl-data-quality-tool.git
cd yssl-data-quality-tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
# Run analysis
python main.py

# Results will be saved in outputs/
```

## Project Structure
```
├── src/
│   ├── data_loader.py      # Dataset loading
│   ├── quality_analyzer.py # Quality assessment
│   └── visualizer.py       # Visualization
├── data/                   # Raw datasets
├── outputs/                # Generated reports
└── main.py                 # Main script
```

## Authors
ALY6080 - Northeastern University
- Arpita Kachhwah
