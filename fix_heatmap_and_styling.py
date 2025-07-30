#!/usr/bin/env python3
"""
Comprehensive fix for heatmap and styling issues
This script addresses all the reported problems systematically
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.data_utils import load_processed_data

def create_robust_agent_heatmap(df):
    """Create a robust agent performance heatmap that works reliably"""
    try:
        if df is None or df.empty:
            return None
        
        # Check for required columns
        required_cols = ['agent_name', 'call_quality_score', 'customer_satisfaction_score']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"Missing columns: {missing_cols}")
            return None
        
        # Prepare data
        metrics = ['call_quality_score', 'customer_satisfaction_score']
        if 'script_adherence_rate' in df.columns:
            metrics.append('script_adherence_rate')
        if 'sentiment_polarity' in df.columns:
            metrics.append('sentiment_polarity')
        
        # Group by agent and calculate means
        agent_data = df.groupby('agent_name')[metrics].mean().round(2)
        
        # Handle missing data
        agent_data = agent_data.fillna(0)
        
        # Create normalized version for color mapping
        norm_data = agent_data.copy()
        for col in norm_data.columns:
            if col == 'sentiment_polarity':
                # Convert -1,1 to 0,1 scale
                norm_data[col] = (norm_data[col] + 1) / 2
            else:
                # Assume 0-10 scale, normalize to 0-1
                norm_data[col] = norm_data[col] / 10
        
        # Limit to top 15 agents for readability
        if len(agent_data) > 15:
            top_agents = agent_data.mean(axis=1).nlargest(15).index
            agent_data = agent_data.loc[top_agents]
            norm_data = norm_data.loc[top_agents]
        
        # Create the heatmap
        fig = go.Figure(data=go.Heatmap(
            z=norm_data.values,
            x=[col.replace('_', ' ').title() for col in norm_data.columns],
            y=list(norm_data.index),
            colorscale='RdYlGn',
            zmid=0.5,
            showscale=True,
            colorbar=dict(
                title="Performance Score",
                tickmode="array",
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=["Low", "Below Avg", "Average", "Above Avg", "Excellent"]
            ),
            hovertemplate="<b>%{y}</b><br>" +
                          "%{x}: %{z:.2f}<br>" +
                          "<extra></extra>"
        ))
        
        fig.update_layout(
            title="Agent Performance Heatmap",
            xaxis_title="Performance Metrics",
            yaxis_title="Agent Name",
            height=max(400, len(norm_data) * 25),
            font=dict(size=11),
            margin=dict(l=120, r=80, t=60, b=50)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating heatmap: {e}")
        return None

def test_heatmap():
    """Test the heatmap with real data"""
    print("Testing heatmap creation...")
    
    df = load_processed_data()
    if df is None:
        print("No data loaded")
        return
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    fig = create_robust_agent_heatmap(df)
    if fig:
        print("Heatmap created successfully!")
        return fig
    else:
        print("Failed to create heatmap")
        return None

if __name__ == "__main__":
    test_heatmap()