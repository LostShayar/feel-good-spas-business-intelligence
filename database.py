"""
Database module for Feel Good Spas Business Intelligence
Handles PostgreSQL database operations for conversation data storage and retrieval
"""

import os
import pandas as pd
import logging
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, List, Any
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()

class ConversationData(Base):
    """SQLAlchemy model for conversation data"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(255), unique=True, nullable=False)
    call_date = Column(DateTime, nullable=False)
    agent_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    conversation_type = Column(String(100), nullable=False)
    sentiment_label = Column(String(50), nullable=False)
    sentiment_score = Column(Float, nullable=False)
    call_quality_score = Column(Float, nullable=False)
    script_adherence_rate = Column(Float, nullable=False)
    customer_satisfaction_score = Column(Float, nullable=False)
    call_outcome = Column(String(100), nullable=False)
    call_duration_minutes = Column(Float, nullable=False)
    topics = Column(Text)  # JSON string of topics
    issue_resolved = Column(Boolean, nullable=False)
    customer_tone = Column(String(50), nullable=False)
    agent_professionalism = Column(Float, nullable=False)
    conversation_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SpaDatabaseManager:
    """Database manager for Feel Good Spas business intelligence data"""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize database connection"""
        self.database_url = database_url or os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        try:
            self.engine = create_engine(self.database_url, echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def create_tables(self):
        """Create all database tables if they don't exist"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            raise
    
    def insert_conversations_from_csv(self, csv_file_path: str = 'processed_spa_data.csv') -> int:
        """Insert conversation data from CSV file into database"""
        try:
            # Read CSV data
            if not os.path.exists(csv_file_path):
                raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
            
            df = pd.read_csv(csv_file_path)
            logger.info(f"Loaded {len(df)} records from {csv_file_path}")
            
            # Clean and prepare data
            df['call_date'] = pd.to_datetime(df['call_date'])
            df = df.fillna({
                'topics': '[]',
                'conversation_summary': '',
                'customer_tone': 'neutral'
            })
            
            # Convert topics to JSON string if it's not already
            if 'topics' in df.columns:
                df['topics'] = df['topics'].apply(lambda x: json.dumps(x) if not isinstance(x, str) else x)
            
            # Insert data using pandas to_sql for efficiency
            records_inserted = df.to_sql(
                'conversations', 
                self.engine, 
                if_exists='replace',  # Replace existing data
                index=False,
                method='multi',
                chunksize=1000
            )
            
            logger.info(f"Successfully inserted {records_inserted} conversation records")
            return records_inserted or len(df)
            
        except Exception as e:
            logger.error(f"Failed to insert conversations from CSV: {e}")
            raise
    
    def get_conversations_dataframe(self, limit: Optional[int] = None) -> pd.DataFrame:
        """Retrieve all conversations as pandas DataFrame"""
        try:
            query = "SELECT * FROM conversations ORDER BY call_date DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            df = pd.read_sql_query(query, self.engine)
            logger.info(f"Retrieved {len(df)} conversation records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to retrieve conversations: {e}")
            raise
    
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get specific conversation by ID"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM conversations WHERE conversation_id = :conv_id"),
                    {"conv_id": conversation_id}
                )
                row = result.fetchone()
                
                if row:
                    return dict(row._mapping)
                return None
                
        except Exception as e:
            logger.error(f"Failed to retrieve conversation {conversation_id}: {e}")
            raise
    
    def get_agent_performance(self, agent_name: Optional[str] = None) -> pd.DataFrame:
        """Get agent performance metrics"""
        try:
            if agent_name:
                query = """
                SELECT agent_name, location,
                       COUNT(*) as total_calls,
                       AVG(call_quality_score) as avg_quality_score,
                       AVG(script_adherence_rate) as avg_script_adherence,
                       AVG(customer_satisfaction_score) as avg_customer_satisfaction,
                       AVG(agent_professionalism) as avg_professionalism,
                       SUM(CASE WHEN issue_resolved THEN 1 ELSE 0 END) as resolved_calls,
                       AVG(call_duration_minutes) as avg_call_duration
                FROM conversations 
                WHERE agent_name = :agent_name
                GROUP BY agent_name, location
                """
                df = pd.read_sql_query(query, self.engine, params={"agent_name": agent_name})
            else:
                query = """
                SELECT agent_name, location,
                       COUNT(*) as total_calls,
                       AVG(call_quality_score) as avg_quality_score,
                       AVG(script_adherence_rate) as avg_script_adherence,
                       AVG(customer_satisfaction_score) as avg_customer_satisfaction,
                       AVG(agent_professionalism) as avg_professionalism,
                       SUM(CASE WHEN issue_resolved THEN 1 ELSE 0 END) as resolved_calls,
                       AVG(call_duration_minutes) as avg_call_duration
                FROM conversations 
                GROUP BY agent_name, location
                ORDER BY avg_quality_score DESC
                """
                df = pd.read_sql_query(query, self.engine)
            
            logger.info(f"Retrieved agent performance data for {len(df)} agents")
            return df
            
        except Exception as e:
            logger.error(f"Failed to get agent performance: {e}")
            raise
    
    def get_location_performance(self, location: Optional[str] = None) -> pd.DataFrame:
        """Get location performance metrics"""
        try:
            if location:
                query = """
                SELECT location,
                       COUNT(*) as total_calls,
                       AVG(call_quality_score) as avg_quality_score,
                       AVG(customer_satisfaction_score) as avg_customer_satisfaction,
                       COUNT(DISTINCT agent_name) as unique_agents,
                       SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_calls,
                       SUM(CASE WHEN issue_resolved THEN 1 ELSE 0 END) as resolved_calls,
                       AVG(call_duration_minutes) as avg_call_duration
                FROM conversations 
                WHERE location = :location
                GROUP BY location
                """
                df = pd.read_sql_query(query, self.engine, params={"location": location})
            else:
                query = """
                SELECT location,
                       COUNT(*) as total_calls,
                       AVG(call_quality_score) as avg_quality_score,
                       AVG(customer_satisfaction_score) as avg_customer_satisfaction,
                       COUNT(DISTINCT agent_name) as unique_agents,
                       SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_calls,
                       SUM(CASE WHEN issue_resolved THEN 1 ELSE 0 END) as resolved_calls,
                       AVG(call_duration_minutes) as avg_call_duration
                FROM conversations 
                GROUP BY location
                ORDER BY total_calls DESC
                """
                df = pd.read_sql_query(query, self.engine)
            
            logger.info(f"Retrieved location performance data for {len(df)} locations")
            return df
            
        except Exception as e:
            logger.error(f"Failed to get location performance: {e}")
            raise
    
    def get_sentiment_analysis(self, date_range: Optional[tuple] = None) -> pd.DataFrame:
        """Get sentiment analysis over time"""
        try:
            query = """
            SELECT DATE(call_date) as call_date,
                   sentiment_label,
                   COUNT(*) as count,
                   AVG(sentiment_score) as avg_sentiment_score
            FROM conversations
            """
            
            params = {}
            if date_range:
                query += " WHERE call_date BETWEEN :start_date AND :end_date"
                params = {"start_date": date_range[0], "end_date": date_range[1]}
            
            query += " GROUP BY DATE(call_date), sentiment_label ORDER BY call_date DESC"
            
            df = pd.read_sql_query(query, self.engine, params=params)
            logger.info(f"Retrieved sentiment analysis data for {len(df)} date/sentiment combinations")
            return df
            
        except Exception as e:
            logger.error(f"Failed to get sentiment analysis: {e}")
            raise
    
    def get_conversation_trends(self, days: int = 7) -> pd.DataFrame:
        """Get conversation trends over specified days"""
        try:
            query = """
            SELECT DATE(call_date) as call_date,
                   COUNT(*) as total_calls,
                   AVG(call_quality_score) as avg_quality,
                   AVG(customer_satisfaction_score) as avg_satisfaction,
                   SUM(CASE WHEN sentiment_label = 'positive' THEN 1 ELSE 0 END) as positive_calls,
                   SUM(CASE WHEN issue_resolved THEN 1 ELSE 0 END) as resolved_calls
            FROM conversations
            WHERE call_date >= CURRENT_DATE - INTERVAL :days DAY
            GROUP BY DATE(call_date)
            ORDER BY call_date DESC
            """
            
            df = pd.read_sql_query(query, self.engine, params={"days": days})
            logger.info(f"Retrieved conversation trends for {len(df)} days")
            return df
            
        except Exception as e:
            logger.error(f"Failed to get conversation trends: {e}")
            raise
    
    def execute_custom_query(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """Execute custom SQL query and return DataFrame"""
        try:
            df = pd.read_sql_query(query, self.engine, params=params or {})
            logger.info(f"Custom query executed successfully, returned {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"Failed to execute custom query: {e}")
            raise
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with self.engine.connect() as conn:
                # Total conversations
                total_conversations = conn.execute(text("SELECT COUNT(*) FROM conversations")).scalar()
                
                # Date range
                date_range = conn.execute(text("""
                    SELECT MIN(call_date) as min_date, MAX(call_date) as max_date 
                    FROM conversations
                """)).fetchone()
                
                # Unique counts
                unique_agents = conn.execute(text("SELECT COUNT(DISTINCT agent_name) FROM conversations")).scalar()
                unique_locations = conn.execute(text("SELECT COUNT(DISTINCT location) FROM conversations")).scalar()
                
                # Average scores
                avg_scores = conn.execute(text("""
                    SELECT AVG(call_quality_score) as avg_quality,
                           AVG(customer_satisfaction_score) as avg_satisfaction,
                           AVG(sentiment_score) as avg_sentiment
                    FROM conversations
                """)).fetchone()
                
                return {
                    'total_conversations': total_conversations,
                    'date_range': {
                        'min_date': date_range.min_date.strftime('%Y-%m-%d') if date_range.min_date else None,
                        'max_date': date_range.max_date.strftime('%Y-%m-%d') if date_range.max_date else None
                    },
                    'unique_agents': unique_agents,
                    'unique_locations': unique_locations,
                    'average_scores': {
                        'quality': round(avg_scores.avg_quality, 2) if avg_scores.avg_quality else 0,
                        'satisfaction': round(avg_scores.avg_satisfaction, 2) if avg_scores.avg_satisfaction else 0,
                        'sentiment': round(avg_scores.avg_sentiment, 2) if avg_scores.avg_sentiment else 0
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        try:
            self.engine.dispose()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

def main():
    """Test database functionality"""
    try:
        # Initialize database manager
        db = SpaDatabaseManager()
        
        # Create tables
        db.create_tables()
        
        # Insert data from CSV
        records_inserted = db.insert_conversations_from_csv()
        print(f"Inserted {records_inserted} records")
        
        # Get database stats
        stats = db.get_database_stats()
        print(f"\nDatabase Stats: {json.dumps(stats, indent=2)}")
        
        # Test queries
        print("\nAgent Performance (Top 5):")
        agent_df = db.get_agent_performance()
        print(agent_df.head().to_string())
        
        print("\nLocation Performance:")
        location_df = db.get_location_performance()
        print(location_df.to_string())
        
        # Close connection
        db.close()
        
    except Exception as e:
        print(f"Database test failed: {e}")

if __name__ == "__main__":
    main()