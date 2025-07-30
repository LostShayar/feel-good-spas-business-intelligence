"""
vCon (Virtualized Conversation) Parser for Feel Good Spas
Processes vCon format conversation data according to IETF specifications
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VConParser:
    """
    Parser for vCon (Virtualized Conversation) format data
    Follows IETF draft-ietf-vcon-vcon-container specification
    """
    
    def __init__(self):
        self.conversations = []
        self.parsed_data = []
        
    def load_vcon_file(self, file_path: str) -> bool:
        """Load vCon data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            if isinstance(data, list):
                self.conversations = data
            else:
                self.conversations = [data]
                
            logger.info(f"Loaded {len(self.conversations)} conversations from {file_path}")
            return True
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return False
    
    def parse_conversations(self) -> List[Dict[str, Any]]:
        """Parse all loaded conversations and extract business data"""
        self.parsed_data = []
        
        for conversation in self.conversations:
            try:
                parsed_conv = self._parse_single_conversation(conversation)
                if parsed_conv:
                    self.parsed_data.append(parsed_conv)
            except Exception as e:
                logger.error(f"Error parsing conversation {conversation.get('id', 'unknown')}: {e}")
                continue
                
        logger.info(f"Successfully parsed {len(self.parsed_data)} conversations")
        return self.parsed_data
    
    def _parse_single_conversation(self, vcon_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a single vCon conversation"""
        try:
            # Extract basic metadata
            conversation_id = vcon_data.get('id', vcon_data.get('uuid', ''))
            subject = vcon_data.get('subject', 'Unknown')
            created_at = vcon_data.get('created_at', '')
            updated_at = vcon_data.get('updated_at', '')
            
            # Get the actual vCon content
            vcon_json = vcon_data.get('vcon_json', {})
            
            # Extract parties (participants)
            parties = self._extract_parties(vcon_json.get('parties', []))
            
            # Extract dialog (conversation content)
            dialog_data = self._extract_dialog(vcon_json.get('dialog', []))
            
            # Extract analysis data if available
            analysis_data = self._extract_analysis(vcon_json.get('analysis', []))
            
            # Calculate derived metrics
            metrics = self._calculate_conversation_metrics(dialog_data, analysis_data)
            
            return {
                'conversation_id': conversation_id,
                'subject': subject,
                'created_at': created_at,
                'updated_at': updated_at,
                'parties': parties,
                'dialog': dialog_data,
                'analysis': analysis_data,
                'metrics': metrics,
                'raw_vcon': vcon_data  # Keep original for reference
            }
            
        except Exception as e:
            logger.error(f"Error parsing conversation: {e}")
            return None
    
    def _extract_parties(self, parties_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract party (participant) information"""
        parties = []
        
        for party in parties_data:
            party_info = {
                'name': party.get('name', 'Unknown'),
                'tel': party.get('tel', ''),
                'email': party.get('email', ''),
                'role': self._determine_party_role(party),
                'location': party.get('location', ''),
                'organization': party.get('organization', '')
            }
            parties.append(party_info)
            
        return parties
    
    def _determine_party_role(self, party: Dict[str, Any]) -> str:
        """Determine if party is agent or customer based on available data"""
        name = party.get('name', '').lower()
        email = party.get('email', '').lower()
        
        # Check for agent indicators
        if any(indicator in name for indicator in ['support', 'agent', 'rep', 'service']):
            return 'agent'
        if 'feelgoodspas' in email or 'spa' in email:
            return 'agent'
            
        return 'customer'
    
    def _extract_dialog(self, dialog_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract dialog/conversation content"""
        dialog = []
        
        for entry in dialog_data:
            dialog_entry = {
                'type': entry.get('type', 'text'),
                'party': entry.get('party', 0),
                'start': entry.get('start', 0),
                'duration': entry.get('duration', 0),
                'body': entry.get('body', ''),
                'mimetype': entry.get('mimetype', ''),
                'url': entry.get('url', ''),
                'encoding': entry.get('encoding', 'none')
            }
            dialog.append(dialog_entry)
            
        return dialog
    
    def _extract_analysis(self, analysis_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract analysis results from vCon"""
        analysis = []
        
        for entry in analysis_data:
            analysis_entry = {
                'type': entry.get('type', ''),
                'dialog': entry.get('dialog', 0),
                'vendor': entry.get('vendor', ''),
                'schema': entry.get('schema', ''),
                'body': entry.get('body', {}),
                'encoding': entry.get('encoding', 'json')
            }
            analysis.append(analysis_entry)
            
        return analysis
    
    def _calculate_conversation_metrics(self, dialog_data: List[Dict[str, Any]], 
                                      analysis_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate conversation metrics for business intelligence"""
        metrics = {
            'total_duration': 0,
            'message_count': len(dialog_data),
            'agent_messages': 0,
            'customer_messages': 0,
            'avg_response_time': 0,
            'conversation_type': 'unknown',
            'has_recording': False,
            'has_analysis': len(analysis_data) > 0
        }
        
        # Calculate duration and message distribution
        for entry in dialog_data:
            duration = entry.get('duration', 0)
            if isinstance(duration, (int, float)):
                metrics['total_duration'] += duration
                
            party = entry.get('party', 0)
            if party == 0:  # Assuming party 0 is typically the agent
                metrics['agent_messages'] += 1
            else:
                metrics['customer_messages'] += 1
                
            if entry.get('type') == 'recording':
                metrics['has_recording'] = True
        
        # Determine conversation type based on content
        all_text = ' '.join([entry.get('body', '') for entry in dialog_data])
        metrics['conversation_type'] = self._classify_conversation_type(all_text)
        
        return metrics
    
    def _classify_conversation_type(self, text: str) -> str:
        """Classify conversation type based on content"""
        text_lower = text.lower()
        
        # Define keywords for different conversation types
        booking_keywords = ['appointment', 'booking', 'schedule', 'reserve', 'book']
        complaint_keywords = ['complaint', 'problem', 'issue', 'unhappy', 'dissatisfied']
        billing_keywords = ['billing', 'payment', 'charge', 'invoice', 'refund']
        service_keywords = ['service', 'treatment', 'massage', 'facial', 'spa']
        
        # Count keyword occurrences
        booking_count = sum(1 for keyword in booking_keywords if keyword in text_lower)
        complaint_count = sum(1 for keyword in complaint_keywords if keyword in text_lower)
        billing_count = sum(1 for keyword in billing_keywords if keyword in text_lower)
        service_count = sum(1 for keyword in service_keywords if keyword in text_lower)
        
        # Determine primary type
        max_count = max(booking_count, complaint_count, billing_count, service_count)
        
        if max_count == 0:
            return 'general'
        elif max_count == booking_count:
            return 'booking'
        elif max_count == complaint_count:
            return 'complaint'
        elif max_count == billing_count:
            return 'billing'
        else:
            return 'service_inquiry'
    
    def extract_business_data(self) -> List[Dict[str, Any]]:
        """Extract structured business data for analysis"""
        business_data = []
        
        for conversation in self.parsed_data:
            try:
                # Extract agent information
                agent_info = self._get_agent_info(conversation)
                customer_info = self._get_customer_info(conversation)
                
                # Extract call details
                call_details = {
                    'conversation_id': conversation['conversation_id'],
                    'subject': conversation['subject'],
                    'created_at': conversation['created_at'],
                    'duration_seconds': conversation['metrics']['total_duration'],
                    'message_count': conversation['metrics']['message_count'],
                    'conversation_type': conversation['metrics']['conversation_type'],
                    'has_recording': conversation['metrics']['has_recording'],
                    'agent_name': agent_info.get('name', 'Unknown'),
                    'agent_email': agent_info.get('email', ''),
                    'customer_name': customer_info.get('name', 'Unknown'),
                    'customer_phone': customer_info.get('tel', ''),
                    'location': agent_info.get('location', 'Unknown'),
                }
                
                # Extract conversation text for analysis
                conversation_text = self._extract_full_conversation_text(conversation)
                call_details['conversation_text'] = conversation_text
                
                business_data.append(call_details)
                
            except Exception as e:
                logger.error(f"Error extracting business data: {e}")
                continue
                
        return business_data
    
    def _get_agent_info(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Extract agent information from conversation"""
        parties = conversation.get('parties', [])
        for party in parties:
            if party.get('role') == 'agent':
                return party
        
        # If no agent role identified, assume party 0 is agent
        if parties:
            return parties[0]
        
        return {}
    
    def _get_customer_info(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Extract customer information from conversation"""
        parties = conversation.get('parties', [])
        for party in parties:
            if party.get('role') == 'customer':
                return party
        
        # If no customer role identified, assume party 1 is customer
        if len(parties) > 1:
            return parties[1]
        
        return {}
    
    def _extract_full_conversation_text(self, conversation: Dict[str, Any]) -> str:
        """Extract complete conversation text for analysis"""
        dialog = conversation.get('dialog', [])
        text_parts = []
        
        for entry in dialog:
            if entry.get('type') == 'text' and entry.get('body'):
                party = entry.get('party', 0)
                speaker = 'Agent' if party == 0 else 'Customer'
                text_parts.append(f"{speaker}: {entry['body']}")
        
        return '\n'.join(text_parts)

def main():
    """Test the vCon parser with sample data"""
    parser = VConParser()
    
    # Try to load the provided vCon data
    file_paths = [
        'attached_assets/feel-good-spas-vcons_1753848151720.json',
        'attached_assets/feel-good-spas-vcons_1753849037994.json'
    ]
    
    for file_path in file_paths:
        if parser.load_vcon_file(file_path):
            conversations = parser.parse_conversations()
            business_data = parser.extract_business_data()
            
            print(f"Processed {len(business_data)} conversations from {file_path}")
            
            # Print sample data
            if business_data:
                sample = business_data[0]
                print("\nSample conversation data:")
                for key, value in sample.items():
                    if key != 'conversation_text':  # Skip long text
                        print(f"{key}: {value}")
            
            break

if __name__ == "__main__":
    main()
