# Weather ETL Pipeline with ML-Powered Predictive Analytics
# Author: Surya
# Description: Real-time weather data extraction, transformation, and loading
#              with machine learning anomaly detection and trend prediction

import requests
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class WeatherETL:
    def __init__(self, api_key=None, db_name='weather_data.db'):
        self.api_key = api_key or 'demo'
        self.db_name = db_name
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.trend_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS raw_weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                timestamp DATETIME,
                temperature REAL,
                humidity INTEGER,
                pressure INTEGER,
                wind_speed REAL,
                weather_condition TEXT,
                raw_json TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transformed_weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                timestamp DATETIME,
                temp_celsius REAL,
                temp_fahrenheit REAL,
                humidity_category TEXT,
                wind_category TEXT,
                comfort_index REAL,
                is_anomaly BOOLEAN,
                anomaly_score REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized: {self.db_name}")
    
    def extract(self, cities=['London', 'NewYork', 'Tokyo', 'Mumbai']):
        print("EXTRACT: Fetching weather data...")
        extracted_data = []
        
        for city in cities:
            try:
                # Simulate API call
                data = self._simulate_weather_data(city)
                extracted_data.append(data)
                print(f"  Extracted data for {city}")
            except Exception as e:
                print(f"  Error extracting {city}: {e}")
        
        return extracted_data
    
    def _simulate_weather_data(self, city):
        # Simulate realistic weather data
        base_temps = {'London': 15, 'NewYork': 20, 'Tokyo': 18, 'Mumbai': 30}
        base_temp = base_temps.get(city, 20)
        
        return {
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'temperature': base_temp + np.random.uniform(-5, 5),
            'humidity': int(np.random.uniform(40, 90)),
            'pressure': int(np.random.uniform(1000, 1020)),
            'wind_speed': round(np.random.uniform(0, 15), 2),
            'weather_condition': np.random.choice(['Clear', 'Clouds', 'Rain', 'Snow'])
        }
    
    def transform(self, raw_data):
        print("TRANSFORM: Processing and enriching data...")
        transformed_data = []
        
        for record in raw_data:
            # Convert temperature
            temp_c = round(record['temperature'], 2)
            temp_f = round((temp_c * 9/5) + 32, 2)
            
            # Categorize humidity
            humidity = record['humidity']
            if humidity < 50:
                humidity_cat = 'Low'
            elif humidity < 70:
                humidity_cat = 'Moderate'
            else:
                humidity_cat = 'High'
            
            # Categorize wind
            wind = record['wind_speed']
            if wind < 5:
                wind_cat = 'Calm'
            elif wind < 10:
                wind_cat = 'Moderate'
            else:
                wind_cat = 'Strong'
            
            # Calculate comfort index
            comfort_index = round(100 - (abs(temp_c - 22) * 2) - (humidity / 2), 2)
            
            transformed = {
                'city': record['city'],
                'timestamp': record['timestamp'],
                'temp_celsius': temp_c,
                'temp_fahrenheit': temp_f,
                'humidity_category': humidity_cat,
                'wind_category': wind_cat,
                'comfort_index': max(0, comfort_index)
            }
            
            transformed_data.append(transformed)
            print(f"  Transformed {record['city']}: Comfort Index = {comfort_index}")
        
        # ML: Detect anomalies
        self._detect_anomalies(transformed_data)
        
        return transformed_data
    
    def _detect_anomalies(self, data):
        if len(data) < 2:
            return
        
        features = np.array([[d['temp_celsius'], d['comfort_index']] for d in data])
        
        try:
            anomalies = self.anomaly_detector.fit_predict(features)
            scores = self.anomaly_detector.score_samples(features)
            
            for i, record in enumerate(data):
                record['is_anomaly'] = bool(anomalies[i] == -1)
                record['anomaly_score'] = round(scores[i], 3)
        except:
            pass
    
    def load(self, transformed_data):
        print("LOAD: Saving to database...")
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for record in transformed_data:
            cursor.execute('''
                INSERT INTO transformed_weather (
                    city, timestamp, temp_celsius, temp_fahrenheit,
                    humidity_category, wind_category, comfort_index,
                    is_anomaly, anomaly_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['city'],
                record['timestamp'],
                record['temp_celsius'],
                record['temp_fahrenheit'],
                record['humidity_category'],
                record['wind_category'],
                record['comfort_index'],
                record.get('is_anomaly', False),
                record.get('anomaly_score', 0)
            ))
        
        conn.commit()
        conn.close()
        print(f"  Loaded {len(transformed_data)} records")
    
    def run_pipeline(self, cities=None):
        print("=" * 50)
        print("WEATHER ETL PIPELINE WITH ML - STARTING")
        print("=" * 50)
        
        start_time = time.time()
        
        # ETL Process
        raw_data = self.extract(cities)
        transformed_data = self.transform(raw_data)
        self.load(transformed_data)
        
        elapsed = round(time.time() - start_time, 2)
        print("=" * 50)
        print(f"PIPELINE COMPLETED in {elapsed}s")
        print("=" * 50)
        
        return transformed_data

# Example usage
if __name__ == "__main__":
    etl = WeatherETL()
    results = etl.run_pipeline()
    
    for record in results:
        print(f"{record['city']}: {record['temp_celsius']}°C | Comfort: {record['comfort_index']}")
