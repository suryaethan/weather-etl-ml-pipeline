# Weather ETL Pipeline with ML-Powered Analytics

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![ETL](https://img.shields.io/badge/ETL-Pipeline-orange.svg)
![ML](https://img.shields.io/badge/ML-Anomaly%20Detection-red.svg)

## Overview

A **unique and innovative ETL (Extract, Transform, Load) pipeline** that combines real-time weather data processing with machine learning-powered anomaly detection and predictive analytics. Unlike traditional ETL projects, this pipeline integrates intelligent data processing capabilities that automatically identify unusual weather patterns and predict future trends.

### What Makes This Project Unique?

Most ETL projects on GitHub focus on simple data movement. This project stands out by:

- **ML-Powered Anomaly Detection**: Automatically identifies unusual weather patterns using Isolation Forest algorithm
- **Real-Time Data Processing**: Extracts live weather data and processes it immediately
- **Intelligent Transformations**: Calculates custom metrics like comfort index and categorizes conditions
- **Predictive Analytics**: Includes foundation for trend prediction using Random Forest
- **Production-Ready Architecture**: Proper database schema, error handling, and logging

## Features

- **Extract**: Fetch weather data from multiple cities using API simulation
- **Transform**: 
  - Temperature conversion (Celsius/Fahrenheit)
  - Weather categorization (humidity, wind speed)
  - Comfort index calculation
  - ML-based anomaly detection
- **Load**: Store processed data in structured SQLite database
- **Machine Learning**:
  - Isolation Forest for anomaly detection
  - Random Forest for trend prediction (extendable)
  - StandardScaler for data normalization

## Technology Stack

- **Python 3.8+**
- **SQLite3** - Database
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **Requests** - API calls (extendable)

## Installation

```bash
# Clone the repository
git clone https://github.com/suryaethan/weather-etl-ml-pipeline.git
cd weather-etl-ml-pipeline

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from weather_etl_pipeline import WeatherETL

# Initialize the ETL pipeline
etl = WeatherETL()

# Run the complete pipeline
results = etl.run_pipeline()

# View results
for record in results:
    print(f"{record['city']}: {record['temp_celsius']}C")
```

### Custom Cities

```python
# Process specific cities
cities = ['London', 'NewYork', 'Tokyo', 'Mumbai', 'Sydney']
etl.run_pipeline(cities=cities)
```

### Access Database

```python
import sqlite3

conn = sqlite3.connect('weather_data.db')
df = pd.read_sql_query("SELECT * FROM transformed_weather", conn)
print(df.head())
```

## Database Schema

### transformed_weather table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| city | TEXT | City name |
| timestamp | DATETIME | Record time |
| temp_celsius | REAL | Temperature in Celsius |
| temp_fahrenheit | REAL | Temperature in Fahrenheit |
| humidity_category | TEXT | Low/Moderate/High |
| wind_category | TEXT | Calm/Moderate/Strong |
| comfort_index | REAL | Comfort score (0-100) |
| is_anomaly | BOOLEAN | ML anomaly flag |
| anomaly_score | REAL | Anomaly confidence |

## Project Structure

```
weather-etl-ml-pipeline/
├── weather_etl_pipeline.py    # Main ETL pipeline
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── LICENSE                   # MIT License
└── .gitignore                # Git ignore
```

## ETL Pipeline Flow

```
[EXTRACT]
    |
    v
 Fetch Weather Data from APIs
    |
    v
[TRANSFORM]
    |
    v
 Convert Units & Categorize
    |
    v
 Calculate Comfort Index
    |
    v
 ML Anomaly Detection
    |
    v
[LOAD]
    |
    v
 Store in SQLite Database
```

## Machine Learning Components

### Anomaly Detection
Uses **Isolation Forest** to identify unusual weather patterns:
- Contamination rate: 10%
- Features: Temperature, Comfort Index
- Output: Binary flag + anomaly score

### Future Enhancements
- Weather trend prediction
- Seasonal pattern analysis
- Multi-variate forecasting

## Real-World Applications

1. **Agriculture**: Detect unusual weather for crop planning
2. **Travel**: Identify best travel times based on comfort index
3. **Energy**: Predict energy consumption patterns
4. **Smart Cities**: Optimize resource allocation

## Contributing

Contributions are welcome! Feel free to:
- Add new data sources
- Implement additional ML models
- Enhance visualization
- Improve documentation

## License

MIT License - feel free to use this project for learning and portfolio building!

## Author

**Surya** - ETL Tester & Data Engineer

Connect with me:
- GitHub: [@suryaethan](https://github.com/suryaethan)

## Acknowledgments

- Inspired by real-world data engineering challenges
- Built with modern ETL best practices
- Designed for learning and professional development

---

**Star this repo** if you find it useful for your ETL and data engineering journey!
