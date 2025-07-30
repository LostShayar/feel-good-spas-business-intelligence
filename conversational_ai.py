"""
Conversational AI system for Feel Good Spas business intelligence
Uses Groq API for free AI-powered natural language interface to business data
"""

import os
import json
import pandas as pd
from groq import Groq
from typing import Dict, List, Any, Optional
import logging
from business_intelligence import SpaBusinessIntelligence
from utils.data_utils import load_processed_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpaConversationalAI:
    """Conversational AI system for Feel Good Spas business intelligence"""
    
    def __init__(self, data_file: str = 'processed_spa_data.csv'):
        # Initialize Groq client for free AI capabilities
        # Using Groq's fast, free LLM models for business intelligence
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", "gsk-test-key"))
        
        # Initialize business intelligence engine
        self.bi_engine = SpaBusinessIntelligence(data_file)
        
        # Load business questions for enhanced responses
        self.business_questions = self._load_business_questions()
        
        # Initialize conversation context
        self.conversation_history = []
        
        # System prompt for the AI
        self.system_prompt = self._create_system_prompt()
    
    def _load_business_questions(self) -> List[str]:
        """Load predefined business questions from CSV"""
        try:
            # Try to load from the assessment file
            question_files = [
                'attached_assets/untagged-questions-assessment_1753848143135.csv',
                'attached_assets/untagged-questions-assessment_1753849037995.csv'
            ]
            
            for file_path in question_files:
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path, header=None)
                    questions = df.iloc[:, 0].dropna().tolist()
                    logger.info(f"Loaded {len(questions)} business questions from {file_path}")
                    return questions
            
            # Fallback to default questions if files not found
            return self._get_default_questions()
            
        except Exception as e:
            logger.error(f"Error loading business questions: {e}")
            return self._get_default_questions()
    
    def _get_default_questions(self) -> List[str]:
        """Default business questions if file loading fails"""
        return [
            "Which locations have the highest call volume?",
            "Which agents have the best quality scores?",
            "What percentage of calls have positive sentiment?",
            "What are the most common customer complaints?",
            "Which locations need improvement in call quality?",
            "What are the busiest call times?",
            "Which agents need coaching support?",
            "How has customer satisfaction changed over time?",
            "What are the most common call topics?",
            "Which locations have the best script adherence?"
        ]
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for the AI assistant"""
        data_summary = self._get_data_context()
        
        return f"""You are a business intelligence assistant for Feel Good Spas, a spa management company. 
You help managers analyze customer service conversation data to make informed business decisions.

CONTEXT:
{data_summary}

CAPABILITIES:
- Answer questions about call quality, customer satisfaction, and agent performance
- Provide insights on location performance and trends
- Analyze customer sentiment and feedback patterns
- Identify operational improvement opportunities
- Generate coaching recommendations for agents
- Explain business metrics and KPIs

RESPONSE GUIDELINES:
1. Be conversational but professional
2. Use specific data and numbers when available
3. Provide actionable insights and recommendations
4. Ask clarifying questions when needed
5. Offer related insights that might be valuable
6. Format responses clearly with bullet points or sections when helpful

SAMPLE QUESTIONS YOU CAN ANSWER:
- Location performance comparisons
- Agent coaching needs
- Customer satisfaction trends
- Call volume patterns
- Quality improvement opportunities
- Sentiment analysis insights
- Operational efficiency metrics

Always ground your responses in the actual data and provide specific, actionable business insights."""
    
    def _get_data_context(self) -> str:
        """Get data context for the system prompt"""
        if self.bi_engine.df is None or self.bi_engine.df.empty:
            return "No conversation data currently available."
        
        df = self.bi_engine.df
        
        context = f"""
DATA OVERVIEW:
- Total conversations analyzed: {len(df)}
- Date range: {df['call_date'].min().strftime('%Y-%m-%d')} to {df['call_date'].max().strftime('%Y-%m-%d')}
- Number of locations: {df['location'].nunique()}
- Number of agents: {df['agent_name'].nunique()}
- Average call quality score: {df['call_quality_score'].mean():.1f}/10
- Average customer satisfaction: {df['customer_satisfaction_score'].mean():.1f}/10

AVAILABLE DATA FIELDS:
- Call quality scores and script adherence rates
- Customer sentiment analysis (positive/negative/neutral)
- Call topics and conversation types
- Agent and location performance metrics
- Temporal patterns (hourly, daily, weekly)
- Call outcomes and resolution status
"""
        return context
    
    def chat(self, user_message: str) -> Dict[str, Any]:
        """Process user message and return AI response"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Check if this is a direct data query
            data_response = self._try_direct_data_query(user_message)
            
            # Prepare messages for OpenAI
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add recent conversation history (last 10 messages)
            messages.extend(self.conversation_history[-10:])
            
            # If we have direct data, include it in the context
            if data_response:
                data_context = f"\nDIRECT DATA QUERY RESULT: {json.dumps(data_response, indent=2)}"
                messages.append({"role": "system", "content": data_context})
            
            # Get AI response using Groq's free models
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast, free model from Groq (updated)
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to conversation history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Generate suggested follow-up questions
            suggestions = self._generate_suggestions(user_message, ai_response)
            
            return {
                'response': ai_response,
                'data': data_response.get('data') if data_response else None,
                'suggestions': suggestions,
                'conversation_id': len(self.conversation_history)
            }
            
        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return {
                'response': "I apologize, but I encountered an error processing your request. Please try asking your question in a different way.",
                'data': None,
                'suggestions': self._get_fallback_suggestions(),
                'conversation_id': len(self.conversation_history)
            }
    
    def _try_direct_data_query(self, message: str) -> Optional[Dict[str, Any]]:
        """Try to answer query directly from business intelligence engine"""
        try:
            return self.bi_engine.answer_business_question(message)
        except Exception as e:
            logger.error(f"Error in direct data query: {e}")
            return None
    
    def _generate_suggestions(self, user_message: str, ai_response: str) -> List[str]:
        """Generate relevant follow-up questions"""
        message_lower = user_message.lower()
        
        # Location-related suggestions
        if 'location' in message_lower:
            return [
                "Which locations need the most improvement?",
                "What are the best practices from top-performing locations?",
                "How do location performance trends compare over time?"
            ]
        
        # Agent-related suggestions
        elif 'agent' in message_lower:
            return [
                "Which agents need coaching support?",
                "What training topics would help improve performance?",
                "How do agent performance metrics correlate with customer satisfaction?"
            ]
        
        # Quality-related suggestions
        elif 'quality' in message_lower:
            return [
                "What factors most impact call quality scores?",
                "How has call quality changed over time?",
                "Which script elements improve call quality?"
            ]
        
        # Sentiment-related suggestions
        elif 'sentiment' in message_lower:
            return [
                "What are the main drivers of negative sentiment?",
                "How does sentiment vary by location or agent?",
                "What actions can improve customer sentiment?"
            ]
        
        # Default suggestions
        else:
            return [
                "What are the biggest opportunities for improvement?",
                "Show me key performance trends",
                "What insights would help me make better decisions?"
            ]
    
    def _get_fallback_suggestions(self) -> List[str]:
        """Get fallback suggestions when there's an error"""
        return [
            "Which locations have the highest call volume?",
            "What are the most common customer complaints?",
            "How is our overall customer satisfaction?",
            "Which agents are performing best?"
        ]
    
    def get_popular_questions(self) -> List[str]:
        """Get popular/example questions users can ask"""
        return [
            "What's our overall performance summary?",
            "Which locations need the most attention?",
            "How are our agents performing?",
            "What are customers most concerned about?",
            "What trends should I be aware of?",
            "Which metrics are improving or declining?",
            "What actionable insights do you recommend?",
            "How can we improve customer satisfaction?"
        ]
    
    def get_suggested_questions_by_category(self) -> Dict[str, List[str]]:
        """Get suggested questions organized by category"""
        return {
            "Performance Overview": [
                "What's our overall performance summary?",
                "How are we trending compared to last month?",
                "What are our key strengths and weaknesses?"
            ],
            "Location Analysis": [
                "Which locations have the highest call volume?",
                "Which locations need quality improvement?",
                "How do locations compare in customer satisfaction?"
            ],
            "Agent Performance": [
                "Which agents have the best quality scores?",
                "Who needs coaching support?",
                "How do agent metrics correlate with outcomes?"
            ],
            "Customer Experience": [
                "What percentage of calls are positive vs negative?",
                "What are the most common complaints?",
                "How satisfied are our customers overall?"
            ],
            "Operational Insights": [
                "What are our busiest call times?",
                "Which topics come up most frequently?",
                "How can we optimize our operations?"
            ]
        }
    
    def analyze_conversation_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in user conversations with the AI"""
        if not self.conversation_history:
            return {'message': 'No conversation history available'}
        
        user_messages = [msg['content'] for msg in self.conversation_history if msg['role'] == 'user']
        
        # Analyze question types
        question_types = {
            'location_questions': len([msg for msg in user_messages if 'location' in msg.lower()]),
            'agent_questions': len([msg for msg in user_messages if 'agent' in msg.lower()]),
            'quality_questions': len([msg for msg in user_messages if 'quality' in msg.lower()]),
            'sentiment_questions': len([msg for msg in user_messages if 'sentiment' in msg.lower()]),
            'trend_questions': len([msg for msg in user_messages if any(word in msg.lower() for word in ['trend', 'change', 'improve', 'decline'])])
        }
        
        return {
            'total_interactions': len(user_messages),
            'question_categories': question_types,
            'most_asked_category': max(question_types, key=question_types.get) if question_types else None
        }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def export_conversation(self) -> str:
        """Export conversation history as formatted text"""
        if not self.conversation_history:
            return "No conversation history to export."
        
        formatted_conversation = "FEEL GOOD SPAS - AI CONVERSATION EXPORT\n"
        formatted_conversation += "=" * 50 + "\n\n"
        
        for i, message in enumerate(self.conversation_history, 1):
            role = "User" if message['role'] == 'user' else "AI Assistant"
            formatted_conversation += f"{i}. {role}:\n{message['content']}\n\n"
        
        formatted_conversation += f"Exported: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return formatted_conversation

def main():
    """Test the conversational AI system"""
    ai = SpaConversationalAI()
    
    print("Feel Good Spas Conversational AI Test")
    print("=" * 40)
    
    # Test questions
    test_questions = [
        "What's our overall performance?",
        "Which locations have the highest call volume?",
        "Which agents need coaching?",
        "What are customers most unhappy about?"
    ]
    
    for question in test_questions:
        print(f"\nQ: {question}")
        response = ai.chat(question)
        print(f"A: {response['response'][:200]}...")
        
        if response['suggestions']:
            print(f"Suggestions: {response['suggestions'][:2]}")

if __name__ == "__main__":
    main()
