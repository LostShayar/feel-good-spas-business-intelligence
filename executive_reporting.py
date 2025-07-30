"""
Automated Executive Reporting System for Feel Good Spas
Scheduled insights delivery and comprehensive business reports
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import json
from dataclasses import dataclass
from enum import Enum

# Import business modules
from business_intelligence import SpaBusinessIntelligence
from predictive_analytics import run_predictive_analysis
from utils.data_utils import load_processed_data

logger = logging.getLogger(__name__)

class ReportFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

@dataclass
class ExecutiveReport:
    """Executive report data structure"""
    report_id: str
    generated_at: datetime
    report_period: str
    frequency: ReportFrequency
    executive_summary: Dict
    key_metrics: Dict
    performance_insights: Dict
    predictive_insights: Dict
    recommendations: List[str]
    alerts: List[Dict]
    attachments: List[str]

class ExecutiveReportGenerator:
    """Generate comprehensive executive reports with automated insights"""
    
    def __init__(self):
        self.bi_engine = SpaBusinessIntelligence()
        self.report_templates = {
            ReportFrequency.DAILY: self._generate_daily_template,
            ReportFrequency.WEEKLY: self._generate_weekly_template,
            ReportFrequency.MONTHLY: self._generate_monthly_template,
            ReportFrequency.QUARTERLY: self._generate_quarterly_template
        }
    
    def generate_executive_report(self, frequency: ReportFrequency, date_range: Optional[tuple] = None) -> ExecutiveReport:
        """Generate comprehensive executive report for specified frequency"""
        try:
            # Load data
            df = load_processed_data()
            if df is None or df.empty:
                return self._generate_empty_report(frequency)
            
            # Filter data by date range if specified
            if date_range:
                start_date, end_date = date_range
                df = df[(df['call_date'] >= start_date) & (df['call_date'] <= end_date)]
            
            # Generate report using template
            template_func = self.report_templates[frequency]
            report = template_func(df)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating executive report: {e}")
            return self._generate_empty_report(frequency)
    
    def _generate_daily_template(self, df: pd.DataFrame) -> ExecutiveReport:
        """Generate daily executive report"""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # Filter to yesterday's data
        daily_data = df[df['call_date'].dt.date == yesterday]
        
        # Calculate daily metrics
        daily_metrics = self._calculate_daily_metrics(daily_data, df)
        
        # Generate insights
        insights = self.bi_engine.generate_insights(daily_data)
        
        # Create alerts
        alerts = self._generate_daily_alerts(daily_metrics)
        
        return ExecutiveReport(
            report_id=f"daily_{yesterday.strftime('%Y%m%d')}",
            generated_at=datetime.now(),
            report_period=f"Daily Report - {yesterday.strftime('%B %d, %Y')}",
            frequency=ReportFrequency.DAILY,
            executive_summary=self._create_daily_summary(daily_metrics),
            key_metrics=daily_metrics,
            performance_insights=insights,
            predictive_insights={},  # Limited for daily reports
            recommendations=self._generate_daily_recommendations(daily_metrics),
            alerts=alerts,
            attachments=[]
        )
    
    def _generate_weekly_template(self, df: pd.DataFrame) -> ExecutiveReport:
        """Generate weekly executive report"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        # Filter to last week's data
        weekly_data = df[(df['call_date'].dt.date >= start_date) & 
                        (df['call_date'].dt.date <= end_date)]
        
        # Calculate weekly metrics
        weekly_metrics = self._calculate_weekly_metrics(weekly_data, df)
        
        # Generate comprehensive insights
        insights = self.bi_engine.generate_insights(weekly_data)
        
        # Generate predictive insights
        predictive_insights = run_predictive_analysis(weekly_data)
        
        # Create alerts
        alerts = self._generate_weekly_alerts(weekly_metrics)
        
        return ExecutiveReport(
            report_id=f"weekly_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}",
            generated_at=datetime.now(),
            report_period=f"Weekly Report - {start_date.strftime('%B %d')} to {end_date.strftime('%B %d, %Y')}",
            frequency=ReportFrequency.WEEKLY,
            executive_summary=self._create_weekly_summary(weekly_metrics),
            key_metrics=weekly_metrics,
            performance_insights=insights,
            predictive_insights=predictive_insights,
            recommendations=self._generate_weekly_recommendations(weekly_metrics, predictive_insights),
            alerts=alerts,
            attachments=[]
        )
    
    def _generate_monthly_template(self, df: pd.DataFrame) -> ExecutiveReport:
        """Generate monthly executive report"""
        today = datetime.now()
        first_day = today.replace(day=1)
        last_month_end = first_day - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        
        # Filter to last month's data
        monthly_data = df[(df['call_date'].dt.date >= last_month_start.date()) & 
                         (df['call_date'].dt.date <= last_month_end.date())]
        
        # Calculate monthly metrics
        monthly_metrics = self._calculate_monthly_metrics(monthly_data, df)
        
        # Generate comprehensive insights
        insights = self.bi_engine.generate_insights(monthly_data)
        
        # Generate predictive insights
        predictive_insights = run_predictive_analysis(df)  # Use all data for better predictions
        
        # Create alerts
        alerts = self._generate_monthly_alerts(monthly_metrics)
        
        return ExecutiveReport(
            report_id=f"monthly_{last_month_start.strftime('%Y%m')}",
            generated_at=datetime.now(),
            report_period=f"Monthly Report - {last_month_start.strftime('%B %Y')}",
            frequency=ReportFrequency.MONTHLY,
            executive_summary=self._create_monthly_summary(monthly_metrics),
            key_metrics=monthly_metrics,
            performance_insights=insights,
            predictive_insights=predictive_insights,
            recommendations=self._generate_monthly_recommendations(monthly_metrics, predictive_insights),
            alerts=alerts,
            attachments=[]
        )
    
    def _generate_quarterly_template(self, df: pd.DataFrame) -> ExecutiveReport:
        """Generate quarterly executive report"""
        today = datetime.now()
        quarter = (today.month - 1) // 3 + 1
        quarter_start = datetime(today.year, 3 * quarter - 2, 1)
        quarter_end = quarter_start + timedelta(days=92)  # Approximate quarter end
        
        # Filter to quarter data
        quarterly_data = df[(df['call_date'] >= quarter_start) & 
                           (df['call_date'] <= quarter_end)]
        
        # Calculate quarterly metrics
        quarterly_metrics = self._calculate_quarterly_metrics(quarterly_data, df)
        
        # Generate comprehensive insights
        insights = self.bi_engine.generate_insights(quarterly_data)
        
        # Generate predictive insights
        predictive_insights = run_predictive_analysis(df)
        
        # Create alerts
        alerts = self._generate_quarterly_alerts(quarterly_metrics)
        
        return ExecutiveReport(
            report_id=f"quarterly_{today.year}Q{quarter}",
            generated_at=datetime.now(),
            report_period=f"Quarterly Report - Q{quarter} {today.year}",
            frequency=ReportFrequency.QUARTERLY,
            executive_summary=self._create_quarterly_summary(quarterly_metrics),
            key_metrics=quarterly_metrics,
            performance_insights=insights,
            predictive_insights=predictive_insights,
            recommendations=self._generate_quarterly_recommendations(quarterly_metrics, predictive_insights),
            alerts=alerts,
            attachments=[]
        )
    
    def _calculate_daily_metrics(self, daily_data: pd.DataFrame, full_data: pd.DataFrame) -> Dict:
        """Calculate key daily metrics"""
        if daily_data.empty:
            return self._empty_metrics()
        
        return {
            'total_calls': len(daily_data),
            'avg_satisfaction': daily_data['customer_satisfaction_score'].mean(),
            'avg_quality': daily_data['call_quality_score'].mean(),
            'avg_script_adherence': daily_data['script_adherence_rate'].mean(),
            'sentiment_distribution': daily_data['sentiment_label'].value_counts().to_dict(),
            'top_agents': daily_data.groupby('agent_name')['customer_satisfaction_score'].mean().nlargest(3).to_dict(),
            'response_time': daily_data['duration_seconds'].mean() / 60,  # Convert to minutes
            'resolution_rate': (daily_data['call_outcome'] == 'resolved').mean()
        }
    
    def _calculate_weekly_metrics(self, weekly_data: pd.DataFrame, full_data: pd.DataFrame) -> Dict:
        """Calculate key weekly metrics"""
        if weekly_data.empty:
            return self._empty_metrics()
        
        # Previous week for comparison
        prev_week_start = weekly_data['call_date'].min() - timedelta(days=7)
        prev_week_end = weekly_data['call_date'].min() - timedelta(days=1)
        prev_week_data = full_data[(full_data['call_date'] >= prev_week_start) & 
                                  (full_data['call_date'] <= prev_week_end)]
        
        current_metrics = {
            'total_calls': len(weekly_data),
            'avg_satisfaction': weekly_data['customer_satisfaction_score'].mean(),
            'avg_quality': weekly_data['call_quality_score'].mean(),
            'avg_script_adherence': weekly_data['script_adherence_rate'].mean(),
            'sentiment_distribution': weekly_data['sentiment_label'].value_counts().to_dict(),
            'unique_customers': weekly_data['customer_name'].nunique(),
            'resolution_rate': (weekly_data['call_outcome'] == 'resolved').mean(),
            'agent_performance': weekly_data.groupby('agent_name').agg({
                'customer_satisfaction_score': 'mean',
                'call_quality_score': 'mean'
            }).to_dict()
        }
        
        # Add week-over-week comparisons
        if not prev_week_data.empty:
            current_metrics['wow_changes'] = {
                'calls': ((len(weekly_data) - len(prev_week_data)) / len(prev_week_data)) * 100,
                'satisfaction': weekly_data['customer_satisfaction_score'].mean() - prev_week_data['customer_satisfaction_score'].mean(),
                'quality': weekly_data['call_quality_score'].mean() - prev_week_data['call_quality_score'].mean()
            }
        
        return current_metrics
    
    def _calculate_monthly_metrics(self, monthly_data: pd.DataFrame, full_data: pd.DataFrame) -> Dict:
        """Calculate comprehensive monthly metrics"""
        if monthly_data.empty:
            return self._empty_metrics()
        
        return {
            'total_calls': len(monthly_data),
            'unique_customers': monthly_data['customer_name'].nunique(),
            'avg_satisfaction': monthly_data['customer_satisfaction_score'].mean(),
            'avg_quality': monthly_data['call_quality_score'].mean(),
            'avg_script_adherence': monthly_data['script_adherence_rate'].mean(),
            'sentiment_distribution': monthly_data['sentiment_label'].value_counts().to_dict(),
            'location_performance': monthly_data.groupby('location').agg({
                'customer_satisfaction_score': 'mean',
                'call_quality_score': 'mean',
                'conversation_id': 'count'
            }).to_dict(),
            'agent_rankings': monthly_data.groupby('agent_name')['customer_satisfaction_score'].mean().nlargest(10).to_dict(),
            'call_volume_trend': monthly_data.groupby(monthly_data['call_date'].dt.day)['conversation_id'].count().to_dict(),
            'resolution_rate': (monthly_data['call_outcome'] == 'resolved').mean(),
            'avg_response_time': monthly_data['duration_seconds'].mean() / 60
        }
    
    def _calculate_quarterly_metrics(self, quarterly_data: pd.DataFrame, full_data: pd.DataFrame) -> Dict:
        """Calculate comprehensive quarterly metrics"""
        if quarterly_data.empty:
            return self._empty_metrics()
        
        return {
            'total_calls': len(quarterly_data),
            'unique_customers': quarterly_data['customer_name'].nunique(),
            'customer_retention_rate': self._calculate_retention_rate(quarterly_data),
            'avg_satisfaction': quarterly_data['customer_satisfaction_score'].mean(),
            'satisfaction_trend': quarterly_data.groupby(quarterly_data['call_date'].dt.month)['customer_satisfaction_score'].mean().to_dict(),
            'location_growth': quarterly_data.groupby(['location', quarterly_data['call_date'].dt.month])['conversation_id'].count().to_dict(),
            'agent_development': self._analyze_agent_development(quarterly_data),
            'operational_efficiency': {
                'avg_resolution_time': quarterly_data['duration_seconds'].mean() / 60,
                'first_call_resolution': (quarterly_data['call_outcome'] == 'resolved').mean(),
                'script_compliance': quarterly_data['script_adherence_rate'].mean()
            }
        }
    
    def _generate_daily_alerts(self, metrics: Dict) -> List[Dict]:
        """Generate daily performance alerts"""
        alerts = []
        
        if metrics.get('avg_satisfaction', 10) < 6.0:
            alerts.append({
                'type': 'critical',
                'title': 'Low Customer Satisfaction',
                'message': f"Daily satisfaction score ({metrics['avg_satisfaction']:.1f}) below critical threshold",
                'action_required': True
            })
        
        if metrics.get('total_calls', 0) == 0:
            alerts.append({
                'type': 'warning',
                'title': 'No Customer Interactions',
                'message': 'No customer calls recorded for yesterday',
                'action_required': True
            })
        
        return alerts
    
    def _generate_weekly_alerts(self, metrics: Dict) -> List[Dict]:
        """Generate weekly performance alerts"""
        alerts = []
        
        wow_changes = metrics.get('wow_changes', {})
        
        if wow_changes.get('satisfaction', 0) < -1.0:
            alerts.append({
                'type': 'warning',
                'title': 'Declining Satisfaction Trend',
                'message': f"Customer satisfaction dropped by {abs(wow_changes['satisfaction']):.1f} points this week",
                'action_required': True
            })
        
        if wow_changes.get('calls', 0) < -20:
            alerts.append({
                'type': 'info',
                'title': 'Call Volume Decrease',
                'message': f"Call volume decreased by {abs(wow_changes['calls']):.1f}% compared to last week",
                'action_required': False
            })
        
        return alerts
    
    def _generate_monthly_alerts(self, metrics: Dict) -> List[Dict]:
        """Generate monthly performance alerts"""
        alerts = []
        
        if metrics.get('avg_satisfaction', 10) < 7.0:
            alerts.append({
                'type': 'critical',
                'title': 'Monthly Satisfaction Below Target',
                'message': f"Monthly average satisfaction ({metrics['avg_satisfaction']:.1f}) below target of 7.0",
                'action_required': True
            })
        
        return alerts
    
    def _generate_quarterly_alerts(self, metrics: Dict) -> List[Dict]:
        """Generate quarterly strategic alerts"""
        alerts = []
        
        retention_rate = metrics.get('customer_retention_rate', 100)
        if retention_rate < 80:
            alerts.append({
                'type': 'critical',
                'title': 'Customer Retention Risk',
                'message': f"Quarterly retention rate ({retention_rate:.1f}%) below healthy threshold",
                'action_required': True
            })
        
        return alerts
    
    def _create_daily_summary(self, metrics: Dict) -> Dict:
        """Create executive summary for daily report"""
        return {
            'headline': f"Daily Performance: {metrics.get('total_calls', 0)} customer interactions",
            'key_points': [
                f"Average satisfaction: {metrics.get('avg_satisfaction', 0):.1f}/10",
                f"Call quality: {metrics.get('avg_quality', 0):.1f}/10",
                f"Resolution rate: {metrics.get('resolution_rate', 0):.0%}"
            ],
            'status': 'healthy' if metrics.get('avg_satisfaction', 0) >= 7.0 else 'attention_needed'
        }
    
    def _create_weekly_summary(self, metrics: Dict) -> Dict:
        """Create executive summary for weekly report"""
        return {
            'headline': f"Weekly Performance: {metrics.get('total_calls', 0)} calls, {metrics.get('unique_customers', 0)} customers",
            'key_points': [
                f"Customer satisfaction: {metrics.get('avg_satisfaction', 0):.1f}/10",
                f"Quality score: {metrics.get('avg_quality', 0):.1f}/10",
                f"Week-over-week changes tracked"
            ],
            'status': 'healthy' if metrics.get('avg_satisfaction', 0) >= 7.0 else 'needs_attention'
        }
    
    def _create_monthly_summary(self, metrics: Dict) -> Dict:
        """Create executive summary for monthly report"""
        return {
            'headline': f"Monthly Performance: {metrics.get('total_calls', 0)} interactions with {metrics.get('unique_customers', 0)} customers",
            'key_points': [
                f"Overall satisfaction: {metrics.get('avg_satisfaction', 0):.1f}/10",
                f"Operational efficiency: {metrics.get('resolution_rate', 0):.0%} resolution rate",
                f"Location and agent performance analyzed"
            ],
            'status': 'excellent' if metrics.get('avg_satisfaction', 0) >= 8.0 else 'good' if metrics.get('avg_satisfaction', 0) >= 7.0 else 'needs_improvement'
        }
    
    def _create_quarterly_summary(self, metrics: Dict) -> Dict:
        """Create executive summary for quarterly report"""
        return {
            'headline': f"Quarterly Review: {metrics.get('total_calls', 0)} customer interactions",
            'key_points': [
                f"Customer retention: {metrics.get('customer_retention_rate', 0):.1f}%",
                f"Satisfaction trends analyzed",
                f"Strategic recommendations provided"
            ],
            'status': 'strong' if metrics.get('avg_satisfaction', 0) >= 8.0 else 'stable' if metrics.get('avg_satisfaction', 0) >= 7.0 else 'requires_attention'
        }
    
    def _generate_daily_recommendations(self, metrics: Dict) -> List[str]:
        """Generate daily actionable recommendations"""
        recommendations = []
        
        if metrics.get('avg_satisfaction', 10) < 7.0:
            recommendations.append("Schedule immediate coaching session for underperforming agents")
        
        if metrics.get('total_calls', 0) > 0:
            recommendations.append("Review top-performing interactions for best practice sharing")
        
        return recommendations
    
    def _generate_weekly_recommendations(self, metrics: Dict, predictive_insights: Dict) -> List[str]:
        """Generate weekly strategic recommendations"""
        recommendations = []
        
        wow_changes = metrics.get('wow_changes', {})
        
        if wow_changes.get('satisfaction', 0) < 0:
            recommendations.append("Implement immediate satisfaction recovery initiatives")
        
        if 'retention_risk' in predictive_insights:
            risk_data = predictive_insights['retention_risk']
            high_risk_count = risk_data.get('risk_segments', {}).get('high_risk', {}).get('count', 0)
            if high_risk_count > 0:
                recommendations.append(f"Prioritize retention efforts for {high_risk_count} high-risk customers")
        
        return recommendations
    
    def _generate_monthly_recommendations(self, metrics: Dict, predictive_insights: Dict) -> List[str]:
        """Generate monthly strategic recommendations"""
        recommendations = []
        
        if metrics.get('avg_satisfaction', 10) < 8.0:
            recommendations.append("Launch customer satisfaction improvement initiative")
        
        # Add predictive recommendations
        if 'satisfaction_drivers' in predictive_insights:
            driver_recs = predictive_insights['satisfaction_drivers'].get('recommendations', [])
            recommendations.extend(driver_recs[:3])  # Top 3 recommendations
        
        return recommendations
    
    def _generate_quarterly_recommendations(self, metrics: Dict, predictive_insights: Dict) -> List[str]:
        """Generate quarterly strategic recommendations"""
        recommendations = []
        
        retention_rate = metrics.get('customer_retention_rate', 100)
        if retention_rate < 85:
            recommendations.append("Develop comprehensive customer retention strategy")
        
        if metrics.get('avg_satisfaction', 10) < 8.0:
            recommendations.append("Invest in customer experience transformation initiatives")
        
        recommendations.append("Review and update service delivery protocols based on performance data")
        
        return recommendations
    
    def _calculate_retention_rate(self, df: pd.DataFrame) -> float:
        """Calculate customer retention rate"""
        if df.empty:
            return 0.0
        
        # Simple retention calculation based on repeat customers
        total_customers = df['customer_name'].nunique()
        repeat_customers = df[df.duplicated(subset=['customer_name'], keep=False)]['customer_name'].nunique()
        
        return (repeat_customers / total_customers) * 100 if total_customers > 0 else 0.0
    
    def _analyze_agent_development(self, df: pd.DataFrame) -> Dict:
        """Analyze agent performance development over time"""
        if df.empty:
            return {}
        
        return df.groupby(['agent_name', df['call_date'].dt.month]).agg({
            'customer_satisfaction_score': 'mean',
            'call_quality_score': 'mean'
        }).to_dict()
    
    def _empty_metrics(self) -> Dict:
        """Return empty metrics structure"""
        return {
            'total_calls': 0,
            'avg_satisfaction': 0,
            'avg_quality': 0,
            'avg_script_adherence': 0,
            'sentiment_distribution': {},
            'resolution_rate': 0
        }
    
    def _generate_empty_report(self, frequency: ReportFrequency) -> ExecutiveReport:
        """Generate empty report when no data available"""
        return ExecutiveReport(
            report_id=f"empty_{frequency.value}_{datetime.now().strftime('%Y%m%d')}",
            generated_at=datetime.now(),
            report_period=f"No data available for {frequency.value} report",
            frequency=frequency,
            executive_summary={'headline': 'No data available', 'key_points': [], 'status': 'no_data'},
            key_metrics=self._empty_metrics(),
            performance_insights={},
            predictive_insights={},
            recommendations=["Ensure data collection systems are operational"],
            alerts=[{
                'type': 'critical',
                'title': 'No Data Available',
                'message': 'No conversation data found for reporting period',
                'action_required': True
            }],
            attachments=[]
        )

class ScheduledReportManager:
    """Manage scheduled report generation and delivery"""
    
    def __init__(self):
        self.report_generator = ExecutiveReportGenerator()
        self.scheduled_reports = {
            'daily_executive': {
                'frequency': ReportFrequency.DAILY,
                'recipients': ['executive@feelgoodspas.com'],
                'enabled': True
            },
            'weekly_management': {
                'frequency': ReportFrequency.WEEKLY,
                'recipients': ['management@feelgoodspas.com'],
                'enabled': True
            },
            'monthly_board': {
                'frequency': ReportFrequency.MONTHLY,
                'recipients': ['board@feelgoodspas.com'],
                'enabled': True
            }
        }
    
    def generate_scheduled_report(self, report_name: str) -> Optional[ExecutiveReport]:
        """Generate a scheduled report by name"""
        if report_name not in self.scheduled_reports:
            logger.error(f"Unknown scheduled report: {report_name}")
            return None
        
        config = self.scheduled_reports[report_name]
        if not config['enabled']:
            logger.info(f"Scheduled report {report_name} is disabled")
            return None
        
        return self.report_generator.generate_executive_report(config['frequency'])
    
    def get_report_schedule(self) -> Dict:
        """Get current report schedule configuration"""
        return self.scheduled_reports

def export_report_to_json(report: ExecutiveReport) -> str:
    """Export executive report to JSON format"""
    return json.dumps({
        'report_id': report.report_id,
        'generated_at': report.generated_at.isoformat(),
        'report_period': report.report_period,
        'frequency': report.frequency.value,
        'executive_summary': report.executive_summary,
        'key_metrics': report.key_metrics,
        'performance_insights': report.performance_insights,
        'predictive_insights': report.predictive_insights,
        'recommendations': report.recommendations,
        'alerts': report.alerts,
        'attachments': report.attachments
    }, indent=2, default=str)