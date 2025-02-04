import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict

class WeatherVisualizations:
    def __init__(self):
        self.set_style()

    def set_style(self):
        """Set the style for all visualizations"""
        plt.style.use('fivethirtyeight')  # Changed from 'seaborn' to a built-in style
        sns.set_palette("husl")
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['figure.autolayout'] = True  # Added to prevent text cutoff

    def plot_temperature_trend(self, data: List[Dict]):
        """Create temperature trend line plot"""
        if not data:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(10, 6))

        dates = [d["datetime"] for d in data]
        temps = [d["temp"] for d in data]

        ax.plot(dates, temps, marker='o', linewidth=2, markersize=6)
        ax.fill_between(dates, temps, alpha=0.2)

        ax.set_xlabel("Date and Time", fontsize=12)
        ax.set_ylabel("Temperature (°C)", fontsize=12)
        ax.set_title("Temperature Trend Over Time", fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    def plot_weather_conditions(self, data: List[Dict]):
        """Create weather conditions distribution plot"""
        if not data:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(8, 6))

        conditions = [d["condition"] for d in data]
        condition_counts = {}
        for condition in conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1

        conditions = list(condition_counts.keys())
        counts = list(condition_counts.values())

        bars = ax.bar(conditions, counts)

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom')

        ax.set_xlabel("Weather Condition", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title("Distribution of Weather Conditions", fontsize=14, pad=20)
        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    def plot_humidity_pressure(self, data: List[Dict]):
        """Create humidity vs pressure scatter plot"""
        if not data:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, "No data available", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(8, 6))

        humidity = [d["humidity"] for d in data]
        pressure = [d["pressure"] for d in data]

        sns.scatterplot(x=humidity, y=pressure, ax=ax, alpha=0.6, s=100)

        ax.set_xlabel("Humidity (%)", fontsize=12)
        ax.set_ylabel("Pressure (hPa)", fontsize=12)
        ax.set_title("Humidity vs Pressure Correlation", fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)

        # Add trend line
        z = np.polyfit(humidity, pressure, 1)
        p = np.poly1d(z)
        ax.plot(humidity, p(humidity), "r--", alpha=0.8, 
                label=f"Trend line")
        ax.legend()

        plt.tight_layout()

        return fig