"""
Feel Good Spas Data Processor
Transforms raw vCon conversation data into enriched CSV for business intelligence
"""

import pandas as pd
import json
import os
import re
from datetime import datetime, timedelta
from textblob import TextBlob
import logging
from typing import Dict, List, Any
from vcon_parser import VConParser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpaDataProcessor:
    """Processes Feel Good Spas conversation data and enriches with business intelligence"""
    
    def __init__(self):
        self.vcon_parser = VConParser()
        self.processed_data = []
        
    def process_vcon_files(self, file_patterns: List[str]) -> bool:
        """Process all vCon files matching the given patterns"""
        processed_files = []
        
        for pattern in file_patterns:
            # Handle both exact files and patterns
            if os.path.exists(pattern):
                files = [pattern]
            else:
                # Find files matching pattern
                import glob
                files = glob.glob(pattern)
            
            for file_path in files:
                logger.info(f"Processing file: {file_path}")
                
                if self.vcon_parser.load_vcon_file(file_path):
                    conversations = self.vcon_parser.parse_conversations()
                    business_data = self.vcon_parser.extract_business_data()
                    
                    # Enrich each conversation with additional features
                    for conversation in business_data:
                        enriched_data = self._enrich_conversation_data(conversation)
                        self.processed_data.append(enriched_data)
                    
                    processed_files.append(file_path)
                    logger.info(f"Successfully processed {len(business_data)} conversations from {file_path}")
        
        logger.info(f"Total processed conversations: {len(self.processed_data)}")
        return len(processed_files) > 0
    
    def _enrich_conversation_data(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich conversation data with additional business intelligence features"""
        enriched = conversation.copy()
        
        # Get conversation text for analysis
        text = conversation.get('conversation_text', '')
        
        # Sentiment Analysis
        sentiment_data = self._analyze_sentiment(text)
        enriched.update(sentiment_data)
        
        # Topic Classification
        topics = self._classify_topics(text)
        enriched.update(topics)
        
        # Call Quality Assessment
        quality_metrics = self._assess_call_quality(text, conversation)
        enriched.update(quality_metrics)
        
        # Script Adherence Analysis
        script_metrics = self._analyze_script_adherence(text)
        enriched.update(script_metrics)
        
        # Customer Experience Metrics
        cx_metrics = self._analyze_customer_experience(text)
        enriched.update(cx_metrics)
        
        # Temporal Features
        temporal_features = self._extract_temporal_features(conversation.get('created_at', ''))
        enriched.update(temporal_features)
        
        # Call Outcome Classification
        outcome = self._classify_call_outcome(text)
        enriched['call_outcome'] = outcome
        
        # Priority/Urgency Classification
        urgency = self._classify_urgency(text)
        enriched['urgency_level'] = urgency
        
        return enriched
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the conversation"""
        try:
            if not text:
                return {
                    'sentiment_polarity': 0.0,
                    'sentiment_subjectivity': 0.0,
                    'sentiment_label': 'neutral',
                    'customer_satisfaction_score': 5.0
                }
            
            # Analyze overall sentiment
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment_label = 'positive'
            elif polarity < -0.1:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
            
            # Convert to customer satisfaction score (1-10 scale)
            satisfaction_score = 5.0 + (polarity * 5.0)
            satisfaction_score = max(1.0, min(10.0, satisfaction_score))
            
            return {
                'sentiment_polarity': round(polarity, 3),
                'sentiment_subjectivity': round(subjectivity, 3),
                'sentiment_label': sentiment_label,
                'customer_satisfaction_score': round(satisfaction_score, 1)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment_polarity': 0.0,
                'sentiment_subjectivity': 0.0,
                'sentiment_label': 'neutral',
                'customer_satisfaction_score': 5.0
            }
    
    def _classify_topics(self, text: str) -> Dict[str, Any]:
        """Classify conversation topics and themes"""
        text_lower = text.lower()
        
        # Define topic keywords
        topic_keywords = {
            'appointment_scheduling': ['appointment', 'schedule', 'booking', 'book', 'reserve', 'availability'],
            'service_inquiry': ['service', 'treatment', 'massage', 'facial', 'spa', 'therapy', 'package'],
            'billing_payment': ['billing', 'payment', 'charge', 'invoice', 'refund', 'credit', 'cost', 'price'],
            'complaint': ['complaint', 'problem', 'issue', 'unhappy', 'dissatisfied', 'disappointed', 'terrible'],
            'compliment': ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'satisfied'],
            'cancellation': ['cancel', 'cancellation', 'reschedule', 'change', 'modify'],
            'technical_support': ['website', 'app', 'technical', 'login', 'password', 'system'],
            'product_inquiry': ['product', 'gift card', 'membership', 'package', 'voucher'],
            'location_hours': ['hours', 'location', 'address', 'directions', 'parking', 'open', 'closed']
        }
        
        # Count topic occurrences
        topic_scores = {}
        for topic, keywords in topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score
        
        # Find primary topic
        primary_topic = max(topic_scores, key=topic_scores.get) if any(topic_scores.values()) else 'general'
        
        # Calculate confidence
        total_matches = sum(topic_scores.values())
        confidence = topic_scores[primary_topic] / max(total_matches, 1)
        
        return {
            'primary_topic': primary_topic,
            'topic_confidence': round(confidence, 3),
            'topic_scores': json.dumps(topic_scores)
        }
    
    def _assess_call_quality(self, text: str, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Assess call quality based on various factors"""
        try:
            text_lower = text.lower()
            
            # Quality indicators
            positive_indicators = [
                'thank you', 'please', 'help', 'understand', 'sorry', 'apologize',
                'certainly', 'absolutely', 'of course', 'glad to help'
            ]
            
            negative_indicators = [
                'rude', 'unprofessional', 'hang up', 'transfer', 'manager',
                'escalate', 'frustrated', 'angry', 'upset'
            ]
            
            # Count indicators
            positive_count = sum(1 for indicator in positive_indicators if indicator in text_lower)
            negative_count = sum(1 for indicator in negative_indicators if indicator in text_lower)
            
            # Calculate base quality score
            base_score = 7.0  # Start with neutral good score
            
            # Adjust based on indicators
            base_score += positive_count * 0.3
            base_score -= negative_count * 0.5
            
            # Adjust based on conversation length (appropriate length is good)
            duration = conversation.get('duration_seconds', 0)
            if 120 <= duration <= 600:  # 2-10 minutes is good
                base_score += 0.5
            elif duration > 900:  # > 15 minutes might indicate issues
                base_score -= 0.3
            
            # Normalize to 1-10 scale
            quality_score = max(1.0, min(10.0, base_score))
            
            return {
                'call_quality_score': round(quality_score, 1),
                'positive_indicators_count': positive_count,
                'negative_indicators_count': negative_count
            }
            
        except Exception as e:
            logger.error(f"Error assessing call quality: {e}")
            return {
                'call_quality_score': 7.0,
                'positive_indicators_count': 0,
                'negative_indicators_count': 0
            }
    
    def _analyze_script_adherence(self, text: str) -> Dict[str, Any]:
        """Analyze adherence to customer service scripts"""
        text_lower = text.lower()
        
        # Expected script elements
        script_elements = {
            'greeting': ['thank you for calling', 'feel good spas', 'how can i help', 'this is'],
            'identification': ['my name is', 'this is', 'speaking'],
            'problem_acknowledgment': ['understand', 'i see', 'i hear', 'let me help'],
            'solution_offering': ['i can help', 'let me', 'what i can do', 'here\'s what'],
            'follow_up': ['anything else', 'is there anything', 'follow up', 'contact us'],
            'closing': ['thank you', 'have a great', 'wonderful day', 'goodbye']
        }
        
        # Check adherence
        adherence_scores = {}
        for element, phrases in script_elements.items():
            found = any(phrase in text_lower for phrase in phrases)
            adherence_scores[element] = 1 if found else 0
        
        # Calculate overall adherence
        total_elements = len(script_elements)
        followed_elements = sum(adherence_scores.values())
        adherence_rate = followed_elements / total_elements
        
        return {
            'script_adherence_rate': round(adherence_rate, 3),
            'script_elements_followed': followed_elements,
            'script_elements_total': total_elements,
            'script_details': json.dumps(adherence_scores)
        }
    
    def _analyze_customer_experience(self, text: str) -> Dict[str, Any]:
        """Analyze customer experience indicators"""
        text_lower = text.lower()
        
        # Experience indicators
        satisfaction_indicators = [
            'satisfied', 'happy', 'pleased', 'great', 'excellent',
            'wonderful', 'amazing', 'love', 'perfect', 'fantastic'
        ]
        
        dissatisfaction_indicators = [
            'dissatisfied', 'unhappy', 'upset', 'angry', 'frustrated',
            'terrible', 'awful', 'horrible', 'worst', 'hate'
        ]
        
        effort_indicators = [
            'easy', 'simple', 'quick', 'fast', 'convenient',
            'smooth', 'efficient', 'straightforward'
        ]
        
        difficulty_indicators = [
            'difficult', 'hard', 'complicated', 'confusing',
            'slow', 'long wait', 'forever', 'complicated'
        ]
        
        # Count indicators
        satisfaction_count = sum(1 for indicator in satisfaction_indicators if indicator in text_lower)
        dissatisfaction_count = sum(1 for indicator in dissatisfaction_indicators if indicator in text_lower)
        effort_count = sum(1 for indicator in effort_indicators if indicator in text_lower)
        difficulty_count = sum(1 for indicator in difficulty_indicators if indicator in text_lower)
        
        # Calculate experience scores
        satisfaction_score = satisfaction_count - dissatisfaction_count
        effort_score = effort_count - difficulty_count
        
        return {
            'customer_satisfaction_indicators': satisfaction_count,
            'customer_dissatisfaction_indicators': dissatisfaction_count,
            'low_effort_indicators': effort_count,
            'high_effort_indicators': difficulty_count,
            'net_satisfaction_score': satisfaction_score,
            'net_effort_score': effort_score
        }
    
    def _extract_temporal_features(self, created_at: str) -> Dict[str, Any]:
        """Extract temporal features from conversation timestamp"""
        try:
            if not created_at:
                return self._get_default_temporal_features()
            
            # Parse datetime
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            return {
                'call_date': dt.strftime('%Y-%m-%d'),
                'call_time': dt.strftime('%H:%M:%S'),
                'call_hour': dt.hour,
                'call_day_of_week': dt.strftime('%A'),
                'call_month': dt.strftime('%B'),
                'call_year': dt.year,
                'is_weekend': dt.weekday() >= 5,
                'is_business_hours': 9 <= dt.hour <= 17,
                'call_quarter': f"Q{(dt.month - 1) // 3 + 1}"
            }
            
        except Exception as e:
            logger.error(f"Error extracting temporal features: {e}")
            return self._get_default_temporal_features()
    
    def _get_default_temporal_features(self) -> Dict[str, Any]:
        """Return default temporal features"""
        return {
            'call_date': '2025-01-01',
            'call_time': '12:00:00',
            'call_hour': 12,
            'call_day_of_week': 'Monday',
            'call_month': 'January',
            'call_year': 2025,
            'is_weekend': False,
            'is_business_hours': True,
            'call_quarter': 'Q1'
        }
    
    def _classify_call_outcome(self, text: str) -> str:
        """Classify the outcome of the call"""
        text_lower = text.lower()
        
        # Outcome indicators
        if any(word in text_lower for word in ['resolved', 'fixed', 'solved', 'helped', 'booked', 'scheduled']):
            return 'resolved'
        elif any(word in text_lower for word in ['follow up', 'call back', 'transfer', 'escalate']):
            return 'requires_followup'
        elif any(word in text_lower for word in ['cancel', 'cancelled', 'no longer', 'changed mind']):
            return 'cancelled'
        elif any(word in text_lower for word in ['complaint', 'refund', 'manager', 'dissatisfied']):
            return 'complaint'
        else:
            return 'completed'
    
    def _classify_urgency(self, text: str) -> str:
        """Classify urgency level of the conversation"""
        text_lower = text.lower()
        
        # High urgency indicators
        high_urgency = ['urgent', 'emergency', 'asap', 'immediately', 'crisis', 'critical']
        medium_urgency = ['soon', 'today', 'this week', 'important', 'need help']
        
        if any(word in text_lower for word in high_urgency):
            return 'high'
        elif any(word in text_lower for word in medium_urgency):
            return 'medium'
        else:
            return 'low'
    
    def export_to_csv(self, output_file: str = 'processed_spa_data.csv') -> bool:
        """Export processed data to CSV file"""
        try:
            if not self.processed_data:
                logger.error("No data to export")
                return False
            
            # Convert to DataFrame
            df = pd.DataFrame(self.processed_data)
            
            # Ensure consistent column order
            column_order = [
                'conversation_id', 'subject', 'created_at', 'call_date', 'call_time',
                'agent_name', 'agent_email', 'customer_name', 'customer_phone',
                'location', 'duration_seconds', 'message_count', 'conversation_type',
                'primary_topic', 'call_outcome', 'urgency_level',
                'sentiment_polarity', 'sentiment_label', 'customer_satisfaction_score',
                'call_quality_score', 'script_adherence_rate',
                'call_hour', 'call_day_of_week', 'is_weekend', 'is_business_hours'
            ]
            
            # Reorder columns, keeping any additional columns at the end
            existing_cols = [col for col in column_order if col in df.columns]
            additional_cols = [col for col in df.columns if col not in column_order]
            final_columns = existing_cols + additional_cols
            
            df = df[final_columns]
            
            # Export to CSV
            df.to_csv(output_file, index=False)
            logger.info(f"Exported {len(df)} records to {output_file}")
            
            # Print summary statistics
            self._print_summary_stats(df)
            
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def _print_summary_stats(self, df: pd.DataFrame):
        """Print summary statistics of the processed data"""
        print("\n" + "="*50)
        print("FEEL GOOD SPAS DATA PROCESSING SUMMARY")
        print("="*50)
        
        print(f"Total Conversations Processed: {len(df)}")
        print(f"Date Range: {df['call_date'].min()} to {df['call_date'].max()}")
        print(f"Unique Agents: {df['agent_name'].nunique()}")
        print(f"Unique Locations: {df['location'].nunique()}")
        
        print("\nConversation Types:")
        print(df['conversation_type'].value_counts().to_string())
        
        print("\nSentiment Distribution:")
        print(df['sentiment_label'].value_counts().to_string())
        
        print("\nCall Outcomes:")
        print(df['call_outcome'].value_counts().to_string())
        
        print(f"\nAverage Call Quality Score: {df['call_quality_score'].mean():.1f}")
        print(f"Average Script Adherence: {df['script_adherence_rate'].mean():.1%}")
        print(f"Average Customer Satisfaction: {df['customer_satisfaction_score'].mean():.1f}")
        
        print("\n" + "="*50)

def main():
    """Main processing function"""
    processor = SpaDataProcessor()
    
    # File patterns to process
    vcon_files = [
        'attached_assets/feel-good-spas-vcons_1753848151720.json',
        'attached_assets/feel-good-spas-vcons_1753849037994.json',
        'attached_assets/feel-good-spas-vcons*.json'  # Pattern for any additional files
    ]
    
    print("Starting Feel Good Spas Data Processing...")
    print("="*50)
    
    # Process files
    if processor.process_vcon_files(vcon_files):
        # Export to CSV
        if processor.export_to_csv('processed_spa_data.csv'):
            print("\n✅ Data processing completed successfully!")
            print("📊 Output file: processed_spa_data.csv")
        else:
            print("\n❌ Failed to export data to CSV")
    else:
        print("\n❌ Failed to process vCon files")

if __name__ == "__main__":
    main()
