"""
Predictive Analytics Module for Feel Good Spas
Customer Satisfaction and Retention Prediction System
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging
from scipy import stats

logger = logging.getLogger(__name__)

class CustomerRetentionPredictor:
    """Advanced customer retention and satisfaction prediction system"""
    
    def __init__(self):
        self.satisfaction_threshold = 7.0
        self.quality_threshold = 7.0
        self.retention_risk_factors = {
            'low_satisfaction': 0.3,
            'poor_quality': 0.25,
            'script_non_adherence': 0.2,
            'negative_sentiment': 0.15,
            'long_wait_times': 0.1
        }
    
    def analyze_customer_satisfaction_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze trends in customer satisfaction over time"""
        try:
            if df.empty or 'customer_satisfaction_score' not in df.columns:
                return self._empty_analysis_result()
            
            # Ensure call_date is datetime
            df['call_date'] = pd.to_datetime(df['call_date'])
            df = df.sort_values('call_date')
            
            # Group by month for trend analysis
            monthly_satisfaction = df.groupby(df['call_date'].dt.to_period('M')).agg({
                'customer_satisfaction_score': ['mean', 'count', 'std'],
                'call_quality_score': 'mean',
                'sentiment_polarity': 'mean'
            }).round(2)
            
            # Calculate trend direction
            satisfaction_values = monthly_satisfaction[('customer_satisfaction_score', 'mean')].values
            if len(satisfaction_values) > 1:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    range(len(satisfaction_values)), satisfaction_values
                )
                trend_direction = "improving" if slope > 0.1 else "declining" if slope < -0.1 else "stable"
                trend_strength = abs(r_value)
            else:
                slope = 0
                trend_direction = "insufficient_data"
                trend_strength = 0
            
            # Identify risk periods
            risk_periods = monthly_satisfaction[
                monthly_satisfaction[('customer_satisfaction_score', 'mean')] < self.satisfaction_threshold
            ]
            
            return {
                'monthly_trends': monthly_satisfaction.to_dict(),
                'trend_direction': trend_direction,
                'trend_slope': slope,
                'trend_strength': trend_strength,
                'risk_periods': len(risk_periods),
                'current_satisfaction': satisfaction_values[-1] if len(satisfaction_values) > 0 else 0,
                'satisfaction_volatility': np.std(satisfaction_values) if len(satisfaction_values) > 1 else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing satisfaction trends: {e}")
            return self._empty_analysis_result()
    
    def predict_customer_retention_risk(self, df: pd.DataFrame) -> Dict:
        """Predict customer retention risk based on interaction patterns"""
        try:
            if df.empty:
                return {'total_customers': 0, 'risk_segments': {}}
            
            # Group by customer to analyze individual patterns
            customer_metrics = df.groupby('customer_name').agg({
                'customer_satisfaction_score': ['mean', 'min', 'count'],
                'call_quality_score': 'mean',
                'script_adherence_rate': 'mean',
                'sentiment_polarity': 'mean',
                'call_date': ['min', 'max']
            }).round(2)
            
            customer_metrics.columns = [
                'avg_satisfaction', 'min_satisfaction', 'interaction_count',
                'avg_quality', 'avg_script_adherence', 'avg_sentiment',
                'first_interaction', 'last_interaction'
            ]
            
            # Calculate retention risk scores
            risk_scores = []
            for _, customer in customer_metrics.iterrows():
                risk_score = 0
                
                # Satisfaction risk
                if customer['avg_satisfaction'] < self.satisfaction_threshold:
                    risk_score += self.retention_risk_factors['low_satisfaction']
                
                # Quality risk
                if customer['avg_quality'] < self.quality_threshold:
                    risk_score += self.retention_risk_factors['poor_quality']
                
                # Script adherence risk
                if customer['avg_script_adherence'] < 0.7:
                    risk_score += self.retention_risk_factors['script_non_adherence']
                
                # Sentiment risk
                if customer['avg_sentiment'] < 0:
                    risk_score += self.retention_risk_factors['negative_sentiment']
                
                # Extreme dissatisfaction risk
                if customer['min_satisfaction'] < 5.0:
                    risk_score += 0.2
                
                risk_scores.append(min(risk_score, 1.0))  # Cap at 100%
            
            customer_metrics['retention_risk'] = risk_scores
            
            # Segment customers by risk level
            high_risk = customer_metrics[customer_metrics['retention_risk'] >= 0.6]
            medium_risk = customer_metrics[
                (customer_metrics['retention_risk'] >= 0.3) & 
                (customer_metrics['retention_risk'] < 0.6)
            ]
            low_risk = customer_metrics[customer_metrics['retention_risk'] < 0.3]
            
            return {
                'total_customers': len(customer_metrics),
                'risk_segments': {
                    'high_risk': {
                        'count': len(high_risk),
                        'percentage': (len(high_risk) / len(customer_metrics)) * 100,
                        'avg_satisfaction': high_risk['avg_satisfaction'].mean() if len(high_risk) > 0 else 0,
                        'customers': high_risk.index.tolist()[:10]  # Top 10 at-risk customers
                    },
                    'medium_risk': {
                        'count': len(medium_risk),
                        'percentage': (len(medium_risk) / len(customer_metrics)) * 100,
                        'avg_satisfaction': medium_risk['avg_satisfaction'].mean() if len(medium_risk) > 0 else 0
                    },
                    'low_risk': {
                        'count': len(low_risk),
                        'percentage': (len(low_risk) / len(customer_metrics)) * 100,
                        'avg_satisfaction': low_risk['avg_satisfaction'].mean() if len(low_risk) > 0 else 0
                    }
                },
                'customer_details': customer_metrics.to_dict('index')
            }
            
        except Exception as e:
            logger.error(f"Error predicting retention risk: {e}")
            return {'total_customers': 0, 'risk_segments': {}}
    
    def generate_satisfaction_forecast(self, df: pd.DataFrame, forecast_months: int = 6) -> Dict:
        """Generate satisfaction score forecasts using trend analysis"""
        try:
            if df.empty or 'customer_satisfaction_score' not in df.columns:
                return {'forecast': [], 'confidence_interval': []}
            
            # Prepare time series data
            df['call_date'] = pd.to_datetime(df['call_date'])
            monthly_data = df.groupby(df['call_date'].dt.to_period('M')).agg({
                'customer_satisfaction_score': 'mean'
            })
            
            if len(monthly_data) < 3:
                return {'forecast': [], 'confidence_interval': [], 'error': 'Insufficient historical data'}
            
            # Simple linear trend forecasting
            months = range(len(monthly_data))
            satisfaction_scores = monthly_data['customer_satisfaction_score'].values
            
            # Fit linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(months, satisfaction_scores)
            
            # Generate forecast
            future_months = range(len(monthly_data), len(monthly_data) + forecast_months)
            forecast_values = [slope * month + intercept for month in future_months]
            
            # Calculate confidence intervals (simplified approach)
            residuals = satisfaction_scores - (slope * np.array(months) + intercept)
            mse = np.mean(residuals ** 2)
            confidence_margin = 1.96 * np.sqrt(mse)  # 95% confidence interval
            
            forecast_periods = pd.date_range(
                start=monthly_data.index[-1].to_timestamp() + pd.DateOffset(months=1),
                periods=forecast_months,
                freq='M'
            )
            
            forecast_data = []
            for i, (period, value) in enumerate(zip(forecast_periods, forecast_values)):
                forecast_data.append({
                    'period': period.strftime('%Y-%m'),
                    'forecast_satisfaction': max(0, min(10, value)),  # Clamp to valid range
                    'lower_bound': max(0, value - confidence_margin),
                    'upper_bound': min(10, value + confidence_margin),
                    'trend_confidence': abs(r_value)
                })
            
            return {
                'forecast': forecast_data,
                'model_performance': {
                    'r_squared': r_value ** 2,
                    'trend_slope': slope,
                    'historical_variance': np.var(satisfaction_scores)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating satisfaction forecast: {e}")
            return {'forecast': [], 'confidence_interval': []}
    
    def identify_satisfaction_drivers(self, df: pd.DataFrame) -> Dict:
        """Identify key factors that drive customer satisfaction"""
        try:
            if df.empty or 'customer_satisfaction_score' not in df.columns:
                return {'drivers': []}
            
            # Calculate correlation with satisfaction
            correlations = {}
            
            numeric_columns = [
                'call_quality_score', 'script_adherence_rate', 'duration_seconds',
                'sentiment_polarity'
            ]
            
            for col in numeric_columns:
                if col in df.columns:
                    correlation = df['customer_satisfaction_score'].corr(df[col])
                    if not pd.isna(correlation):
                        correlations[col] = correlation
            
            # Analyze categorical factors
            categorical_analysis = {}
            
            # Agent performance impact
            if 'agent_name' in df.columns:
                agent_satisfaction = df.groupby('agent_name')['customer_satisfaction_score'].mean()
                categorical_analysis['top_agents'] = agent_satisfaction.nlargest(5).to_dict()
                categorical_analysis['agent_variance'] = agent_satisfaction.var()
            
            # Location impact
            if 'location' in df.columns:
                location_satisfaction = df.groupby('location')['customer_satisfaction_score'].mean()
                categorical_analysis['location_performance'] = location_satisfaction.to_dict()
            
            # Time-based patterns
            if 'call_date' in df.columns:
                df['hour'] = pd.to_datetime(df['call_date']).dt.hour
                hourly_satisfaction = df.groupby('hour')['customer_satisfaction_score'].mean()
                categorical_analysis['best_hours'] = hourly_satisfaction.nlargest(3).index.tolist()
                categorical_analysis['worst_hours'] = hourly_satisfaction.nsmallest(3).index.tolist()
            
            # Rank drivers by importance
            driver_ranking = sorted(
                [(k, abs(v)) for k, v in correlations.items()],
                key=lambda x: x[1],
                reverse=True
            )
            
            return {
                'correlation_drivers': correlations,
                'ranked_drivers': driver_ranking,
                'categorical_insights': categorical_analysis,
                'recommendations': self._generate_driver_recommendations(correlations, categorical_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error identifying satisfaction drivers: {e}")
            return {'drivers': []}
    
    def _generate_driver_recommendations(self, correlations: Dict, categorical_analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on satisfaction drivers"""
        recommendations = []
        
        # Quality-based recommendations
        if correlations.get('call_quality_score', 0) > 0.5:
            recommendations.append("Focus on call quality training - strong correlation with satisfaction")
        
        # Script adherence recommendations
        if correlations.get('script_adherence_rate', 0) > 0.3:
            recommendations.append("Improve script adherence through coaching - moderate satisfaction impact")
        
        # Timing recommendations
        if 'best_hours' in categorical_analysis:
            best_hours = categorical_analysis['best_hours']
            recommendations.append(f"Schedule important calls during peak performance hours: {best_hours}")
        
        # Agent-specific recommendations
        if 'agent_variance' in categorical_analysis and categorical_analysis['agent_variance'] > 1.0:
            recommendations.append("Address agent performance inconsistencies through targeted training")
        
        return recommendations
    
    def _empty_analysis_result(self) -> Dict:
        """Return empty analysis result structure"""
        return {
            'monthly_trends': {},
            'trend_direction': 'no_data',
            'trend_slope': 0,
            'trend_strength': 0,
            'risk_periods': 0,
            'current_satisfaction': 0,
            'satisfaction_volatility': 0
        }

def run_predictive_analysis(df: pd.DataFrame) -> Dict:
    """Run comprehensive predictive analytics on spa data"""
    predictor = CustomerRetentionPredictor()
    
    return {
        'satisfaction_trends': predictor.analyze_customer_satisfaction_trends(df),
        'retention_risk': predictor.predict_customer_retention_risk(df),
        'satisfaction_forecast': predictor.generate_satisfaction_forecast(df),
        'satisfaction_drivers': predictor.identify_satisfaction_drivers(df),
        'generated_at': datetime.now().isoformat()
    }