"""
Feel Good Spas Business Intelligence Application
Main Streamlit application providing comprehensive spa management insights
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.data_utils import load_processed_data, get_data_summary
from business_intelligence import SpaBusinessIntelligence
from spa_styles import apply_premium_spa_theme
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Feel Good Spas - Business Intelligence",
    page_icon="🧖‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_data_availability():
    """Check if processed data is available"""
    data_file = 'processed_spa_data.csv'
    
    if not os.path.exists(data_file):
        st.error("📋 No processed data found!")
        st.info("""
        **To get started:**
        1. Run the data processor: `python data_processor.py`
        2. This will process the vCon files and create `processed_spa_data.csv`
        3. Refresh this page to see your data
        """)
        
        with st.expander("🔧 Processing Instructions"):
            st.code("""
# Process the vCon conversation data
python data_processor.py

# The processor will:
# 1. Parse vCon JSON files from attached_assets/
# 2. Extract conversation data and business metrics
# 3. Perform sentiment analysis and topic classification
# 4. Generate enriched CSV with business intelligence features
# 5. Create processed_spa_data.csv ready for dashboard
            """, language="bash")
        
        return False
    
    return True

def display_welcome():
    """Display welcome screen and data processing status"""
    # Apply premium spa theme
    apply_premium_spa_theme()
    
    st.markdown("### Transform Customer Conversations into Actionable Business Insights")
    st.markdown("*Powered by AI-driven analytics and your real spa conversation data*")
    
    # Check data availability
    if not check_data_availability():
        return False
    
    # Load and display data summary
    df = load_processed_data()
    if df is None or df.empty:
        st.error("❌ Failed to load processed data")
        return False
    
    summary = get_data_summary(df)
    
    st.markdown("#### 📊 **Business Overview**")
    
    # Display key metrics in 3 columns instead of 4 to remove empty space
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Conversations",
            value=f"{summary['total_conversations']:,}",
            delta=None
        )
        st.metric(
            label="Avg Quality Score", 
            value=f"{summary['avg_quality_score']:.1f}/10",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Unique Locations",
            value=summary['unique_locations'],
            delta=None
        )
        # Add satisfaction metric if available
        df = load_processed_data() 
        if df is not None and 'customer_satisfaction_score' in df.columns:
            avg_satisfaction = df['customer_satisfaction_score'].mean()
            st.metric(
                label="Avg Satisfaction",
                value=f"{avg_satisfaction:.1f}/10",
                delta=None
            )
    
    with col3:
        st.metric(
            label="Active Agents",
            value=summary['unique_agents'],
            delta=None
        )
        # Add date range info
        if summary['date_range']['start'] and summary['date_range']['end']:
            days_range = (summary['date_range']['end'] - summary['date_range']['start']).days
            st.metric(
                label="Data Range",
                value=f"{days_range} days",
                delta=None
            )
    
    # Data range information
    if summary['date_range']['start'] and summary['date_range']['end']:
        st.info(f"📅 **Data Period:** {summary['date_range']['start'].strftime('%B %d, %Y')} to {summary['date_range']['end'].strftime('%B %d, %Y')}")
    
    return True

def display_quick_insights():
    """Display quick insights on the main page"""
    st.markdown("## 📊 Quick Insights")
    
    try:
        # Initialize business intelligence
        bi = SpaBusinessIntelligence()
        executive_summary = bi.get_executive_summary()
        
        if not executive_summary or 'insights' not in executive_summary:
            st.warning("Unable to generate insights at this time")
            return
        
        # Display insights in an attractive format
        insights = executive_summary['insights']
        
        for insight in insights[:5]:  # Show top 5 insights
            st.markdown(f"• {insight}")
        
        # Critical issues alert
        if executive_summary.get('critical_issues'):
            st.markdown("### 🚨 Critical Issues Requiring Attention")
            for issue in executive_summary['critical_issues'][:3]:
                severity_color = "🔴" if issue['severity'] == 'high' else "🟡"
                st.markdown(f"{severity_color} {issue['description']}")
        
    except Exception as e:
        logger.error(f"Error displaying quick insights: {e}")
        st.warning("Unable to generate insights. Please check data availability.")

def display_sentiment_overview():
    """Display sentiment analysis overview"""
    st.markdown("## 😊 Customer Sentiment Overview")
    
    try:
        df = load_processed_data()
        if df is None or 'sentiment_label' not in df.columns:
            st.warning("Sentiment data not available")
            return
        
        # Create sentiment distribution chart
        sentiment_counts = df['sentiment_label'].value_counts()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Pie chart
            fig = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                color_discrete_map={
                    'positive': '#2E8B57',
                    'neutral': '#FFD700', 
                    'negative': '#DC143C'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sentiment metrics
            total_calls = len(df)
            positive_pct = (sentiment_counts.get('positive', 0) / total_calls) * 100
            negative_pct = (sentiment_counts.get('negative', 0) / total_calls) * 100
            neutral_pct = (sentiment_counts.get('neutral', 0) / total_calls) * 100
            
            st.metric("Positive Sentiment", f"{positive_pct:.1f}%", 
                     delta=f"{positive_pct - 60:.1f}%" if positive_pct > 60 else None)
            st.metric("Negative Sentiment", f"{negative_pct:.1f}%",
                     delta=f"{negative_pct - 20:.1f}%" if negative_pct > 20 else None)
            st.metric("Neutral Sentiment", f"{neutral_pct:.1f}%")
            
            # Sentiment trend insight
            if positive_pct > 60:
                st.success("🟢 Strong positive sentiment!")
            elif negative_pct > 30:
                st.error("🔴 High negative sentiment - needs attention")
            else:
                st.info("🟡 Balanced sentiment distribution")
        
    except Exception as e:
        logger.error(f"Error displaying sentiment overview: {e}")
        st.error("Unable to display sentiment analysis")

def display_performance_snapshot():
    """Display performance snapshot"""
    st.markdown("## 🏆 Performance Snapshot")
    
    try:
        bi = SpaBusinessIntelligence()
        executive_summary = bi.get_executive_summary()
        
        if not executive_summary:
            st.warning("Performance data not available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🥇 Top Performing Locations")
            top_locations = executive_summary.get('top_locations', [])
            if top_locations:
                for i, location in enumerate(top_locations, 1):
                    st.markdown(f"{i}. **{location['location']}** - {location['score']}/10")
            else:
                st.info("No location data available")
        
        with col2:
            st.markdown("### 📈 Recent Trends")
            trends = executive_summary.get('trends', {})
            if trends and any(k in trends for k in ['quality_trend', 'satisfaction_trend', 'volume_trend']):
                if trends.get('quality_trend') is not None:
                    trend_icon = "📈" if trends['quality_trend'] > 0 else "📉" if trends['quality_trend'] < 0 else "➡️"
                    st.markdown(f"{trend_icon} Quality Score: {trends['quality_trend']:+.1f}")
                
                if trends.get('satisfaction_trend') is not None:
                    trend_icon = "📈" if trends['satisfaction_trend'] > 0 else "📉" if trends['satisfaction_trend'] < 0 else "➡️"
                    st.markdown(f"{trend_icon} Satisfaction: {trends['satisfaction_trend']:+.1f}")
                
                if trends.get('volume_trend') is not None:
                    trend_icon = "📈" if trends['volume_trend'] > 0 else "📉" if trends['volume_trend'] < 0 else "➡️"
                    st.markdown(f"{trend_icon} Call Volume: {trends['volume_trend']:+d}")
            else:
                st.info("Trend analysis available after collecting recent data")
        
    except Exception as e:
        logger.error(f"Error displaying performance snapshot: {e}")
        st.error("Unable to display performance snapshot")

def display_navigation_guide():
    """Display navigation guide for the application"""
    st.markdown("## 🧭 Navigation Guide")
    
    with st.expander("📱 How to Use This Dashboard", expanded=False):
        st.markdown("""
        **🏠 Home (Current Page)**
        - Overview of key metrics and insights
        - Quick sentiment analysis
        - Performance snapshots
        
        **📊 Dashboard** 
        - Executive-level analytics and KPIs
        - Location and agent performance comparisons
        - Trend analysis and forecasting
        
        **👥 Agent Analytics**
        - Individual agent performance metrics
        - Coaching recommendations
        - Quality score analysis
        
        **🏢 Location Performance**
        - Location-by-location analysis
        - Comparative performance metrics
        - Regional insights and trends
        
        **🤖 Conversational AI**
        - Ask questions in natural language
        - Get instant insights from your data
        - Export analysis and recommendations
        """)

def main():
    """Main application function"""
    # Display welcome and check data
    if not display_welcome():
        return
    
    # Display main content
    display_quick_insights()
    
    st.divider()
    
    # Create two columns for content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        display_sentiment_overview()
    
    with col2:
        display_performance_snapshot()
    
    st.divider()
    
    # Navigation guide
    display_navigation_guide()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Feel Good Spas Business Intelligence Platform<br>
        Transform conversations into actionable business insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
