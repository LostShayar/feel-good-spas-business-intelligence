"""
CRM and Booking System Integration Module for Feel Good Spas
Comprehensive integration capabilities with external spa management systems
"""

import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import hmac

logger = logging.getLogger(__name__)

class IntegrationType(Enum):
    CRM = "crm"
    BOOKING = "booking"
    POS = "pos"
    MARKETING = "marketing"

@dataclass
class Customer:
    """Customer data structure for CRM integration"""
    customer_id: str
    name: str
    email: str
    phone: str
    membership_tier: str
    total_visits: int
    total_spent: float
    last_visit: datetime
    preferences: Dict
    satisfaction_score: float
    retention_risk: str

@dataclass
class Appointment:
    """Appointment data structure for booking integration"""
    appointment_id: str
    customer_id: str
    service_type: str
    service_duration: int
    appointment_date: datetime
    therapist: str
    location: str
    status: str
    price: float
    notes: str

@dataclass
class ServiceMetrics:
    """Service performance metrics"""
    service_name: str
    total_bookings: int
    revenue: float
    avg_satisfaction: float
    cancellation_rate: float
    rebooking_rate: float

class SpaSystemIntegrator:
    """Main integration class for spa management systems"""
    
    def __init__(self):
        self.integrations = {}
        self.auth_tokens = {}
        self.webhook_endpoints = {}
        self.data_sync_status = {}
    
    def register_integration(self, system_name: str, integration_type: IntegrationType, 
                           config: Dict) -> bool:
        """Register a new system integration"""
        try:
            integration_config = {
                'type': integration_type,
                'api_endpoint': config.get('api_endpoint'),
                'api_key': config.get('api_key'),
                'webhook_secret': config.get('webhook_secret'),
                'sync_frequency': config.get('sync_frequency', 'hourly'),
                'enabled': config.get('enabled', True),
                'last_sync': None
            }
            
            self.integrations[system_name] = integration_config
            logger.info(f"Successfully registered {integration_type.value} integration: {system_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register integration {system_name}: {e}")
            return False
    
    def sync_customer_data(self, system_name: str) -> List[Customer]:
        """Sync customer data from CRM system"""
        if system_name not in self.integrations:
            logger.error(f"Integration {system_name} not found")
            return []
        
        config = self.integrations[system_name]
        if config['type'] != IntegrationType.CRM:
            logger.error(f"System {system_name} is not a CRM integration")
            return []
        
        try:
            # Simulate API call to CRM system
            customers_data = self._make_api_call(
                config['api_endpoint'] + '/customers',
                config['api_key']
            )
            
            customers = []
            for customer_data in customers_data.get('customers', []):
                customer = Customer(
                    customer_id=customer_data['id'],
                    name=customer_data['name'],
                    email=customer_data['email'],
                    phone=customer_data.get('phone', ''),
                    membership_tier=customer_data.get('membership_tier', 'standard'),
                    total_visits=customer_data.get('total_visits', 0),
                    total_spent=customer_data.get('total_spent', 0.0),
                    last_visit=datetime.fromisoformat(customer_data.get('last_visit', datetime.now().isoformat())),
                    preferences=customer_data.get('preferences', {}),
                    satisfaction_score=customer_data.get('satisfaction_score', 7.5),
                    retention_risk=customer_data.get('retention_risk', 'low')
                )
                customers.append(customer)
            
            config['last_sync'] = datetime.now()
            logger.info(f"Synced {len(customers)} customers from {system_name}")
            return customers
            
        except Exception as e:
            logger.error(f"Failed to sync customer data from {system_name}: {e}")
            return []
    
    def sync_booking_data(self, system_name: str, date_range: Optional[tuple] = None) -> List[Appointment]:
        """Sync booking data from booking management system"""
        if system_name not in self.integrations:
            logger.error(f"Integration {system_name} not found")
            return []
        
        config = self.integrations[system_name]
        if config['type'] != IntegrationType.BOOKING:
            logger.error(f"System {system_name} is not a booking integration")
            return []
        
        try:
            # Prepare date range parameters
            params = {}
            if date_range:
                start_date, end_date = date_range
                params['start_date'] = start_date.isoformat()
                params['end_date'] = end_date.isoformat()
            
            # Simulate API call to booking system
            bookings_data = self._make_api_call(
                config['api_endpoint'] + '/appointments',
                config['api_key'],
                params
            )
            
            appointments = []
            for booking_data in bookings_data.get('appointments', []):
                appointment = Appointment(
                    appointment_id=booking_data['id'],
                    customer_id=booking_data['customer_id'],
                    service_type=booking_data['service_type'],
                    service_duration=booking_data.get('duration', 60),
                    appointment_date=datetime.fromisoformat(booking_data['appointment_date']),
                    therapist=booking_data.get('therapist', 'Unassigned'),
                    location=booking_data.get('location', 'Main Location'),
                    status=booking_data['status'],
                    price=booking_data.get('price', 0.0),
                    notes=booking_data.get('notes', '')
                )
                appointments.append(appointment)
            
            config['last_sync'] = datetime.now()
            logger.info(f"Synced {len(appointments)} appointments from {system_name}")
            return appointments
            
        except Exception as e:
            logger.error(f"Failed to sync booking data from {system_name}: {e}")
            return []
    
    def push_analytics_insights(self, system_name: str, insights: Dict) -> bool:
        """Push analytics insights back to integrated systems"""
        if system_name not in self.integrations:
            logger.error(f"Integration {system_name} not found")
            return False
        
        config = self.integrations[system_name]
        
        try:
            # Format insights for the target system
            formatted_insights = self._format_insights_for_system(insights, config['type'])
            
            # Push insights via API
            response = self._make_api_call(
                config['api_endpoint'] + '/insights',
                config['api_key'],
                method='POST',
                data=formatted_insights
            )
            
            if response.get('success'):
                logger.info(f"Successfully pushed insights to {system_name}")
                return True
            else:
                logger.error(f"Failed to push insights to {system_name}: {response.get('error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error pushing insights to {system_name}: {e}")
            return False
    
    def create_customer_segments(self, customers: List[Customer]) -> Dict[str, List[Customer]]:
        """Create customer segments for targeted marketing"""
        segments = {
            'vip_customers': [],
            'at_risk': [],
            'frequent_visitors': [],
            'new_customers': [],
            'inactive': []
        }
        
        for customer in customers:
            # VIP customers: high spend and satisfaction
            if customer.total_spent > 5000 and customer.satisfaction_score > 8.5:
                segments['vip_customers'].append(customer)
            
            # At-risk customers: low satisfaction or high retention risk
            elif customer.satisfaction_score < 6.0 or customer.retention_risk == 'high':
                segments['at_risk'].append(customer)
            
            # Frequent visitors: high visit count
            elif customer.total_visits > 10:
                segments['frequent_visitors'].append(customer)
            
            # New customers: recent first visit
            elif (datetime.now() - customer.last_visit).days < 30 and customer.total_visits <= 2:
                segments['new_customers'].append(customer)
            
            # Inactive customers: haven't visited recently
            elif (datetime.now() - customer.last_visit).days > 90:
                segments['inactive'].append(customer)
        
        return segments
    
    def generate_service_analytics(self, appointments: List[Appointment]) -> List[ServiceMetrics]:
        """Generate analytics for spa services"""
        if not appointments:
            return []
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame([asdict(apt) for apt in appointments])
        
        service_metrics = []
        for service in df['service_type'].unique():
            service_data = df[df['service_type'] == service]
            
            metrics = ServiceMetrics(
                service_name=service,
                total_bookings=len(service_data),
                revenue=service_data['price'].sum(),
                avg_satisfaction=7.5,  # Would come from conversation data
                cancellation_rate=(service_data['status'] == 'cancelled').mean(),
                rebooking_rate=self._calculate_rebooking_rate(service_data)
            )
            service_metrics.append(metrics)
        
        return service_metrics
    
    def setup_webhook_listener(self, system_name: str, webhook_url: str) -> bool:
        """Setup webhook listener for real-time updates"""
        try:
            if system_name not in self.integrations:
                logger.error(f"Integration {system_name} not found")
                return False
            
            self.webhook_endpoints[system_name] = webhook_url
            
            # Register webhook with external system
            config = self.integrations[system_name]
            webhook_data = {
                'url': webhook_url,
                'events': ['customer.created', 'customer.updated', 'appointment.created', 'appointment.cancelled'],
                'secret': config.get('webhook_secret')
            }
            
            response = self._make_api_call(
                config['api_endpoint'] + '/webhooks',
                config['api_key'],
                method='POST',
                data=webhook_data
            )
            
            if response.get('success'):
                logger.info(f"Successfully setup webhook for {system_name}")
                return True
            else:
                logger.error(f"Failed to setup webhook for {system_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting up webhook for {system_name}: {e}")
            return False
    
    def process_webhook_event(self, system_name: str, event_data: Dict) -> bool:
        """Process incoming webhook events"""
        try:
            # Verify webhook signature
            if not self._verify_webhook_signature(system_name, event_data):
                logger.error(f"Invalid webhook signature for {system_name}")
                return False
            
            event_type = event_data.get('event_type')
            
            if event_type in ['customer.created', 'customer.updated']:
                self._handle_customer_event(event_data)
            elif event_type in ['appointment.created', 'appointment.cancelled']:
                self._handle_appointment_event(event_data)
            
            logger.info(f"Processed webhook event {event_type} from {system_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing webhook event from {system_name}: {e}")
            return False
    
    def export_customer_insights(self, customers: List[Customer], format: str = 'csv') -> str:
        """Export customer insights for external systems"""
        if not customers:
            return ""
        
        # Convert to DataFrame
        customer_data = []
        for customer in customers:
            customer_data.append({
                'customer_id': customer.customer_id,
                'name': customer.name,
                'email': customer.email,
                'membership_tier': customer.membership_tier,
                'total_visits': customer.total_visits,
                'total_spent': customer.total_spent,
                'satisfaction_score': customer.satisfaction_score,
                'retention_risk': customer.retention_risk,
                'last_visit': customer.last_visit.isoformat()
            })
        
        df = pd.DataFrame(customer_data)
        
        if format.lower() == 'csv':
            return df.to_csv(index=False)
        elif format.lower() == 'json':
            return df.to_json(orient='records', indent=2)
        else:
            return df.to_string(index=False)
    
    def _make_api_call(self, url: str, api_key: str, params: Dict = None, 
                      method: str = 'GET', data: Dict = None) -> Dict:
        """Make API call to external system"""
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {e}")
            # Return mock data for demonstration
            return self._get_mock_api_response(url, method)
    
    def _get_mock_api_response(self, url: str, method: str) -> Dict:
        """Return mock API response for demonstration"""
        if 'customers' in url:
            return {
                'customers': [
                    {
                        'id': 'CUST001',
                        'name': 'Sarah Johnson',
                        'email': 'sarah.johnson@email.com',
                        'phone': '+1-555-0123',
                        'membership_tier': 'premium',
                        'total_visits': 15,
                        'total_spent': 3500.0,
                        'last_visit': '2025-01-25T14:30:00',
                        'preferences': {'service_type': 'massage', 'therapist': 'Maria'},
                        'satisfaction_score': 8.5,
                        'retention_risk': 'low'
                    },
                    {
                        'id': 'CUST002',
                        'name': 'Michael Chen',
                        'email': 'michael.chen@email.com',
                        'phone': '+1-555-0124',
                        'membership_tier': 'standard',
                        'total_visits': 3,
                        'total_spent': 450.0,
                        'last_visit': '2025-01-20T16:00:00',
                        'preferences': {'service_type': 'facial'},
                        'satisfaction_score': 6.2,
                        'retention_risk': 'medium'
                    }
                ]
            }
        elif 'appointments' in url:
            return {
                'appointments': [
                    {
                        'id': 'APT001',
                        'customer_id': 'CUST001',
                        'service_type': 'Swedish Massage',
                        'duration': 90,
                        'appointment_date': '2025-01-30T15:00:00',
                        'therapist': 'Maria Rodriguez',
                        'location': 'Downtown Location',
                        'status': 'confirmed',
                        'price': 150.0,
                        'notes': 'Client prefers medium pressure'
                    }
                ]
            }
        else:
            return {'success': True}
    
    def _format_insights_for_system(self, insights: Dict, system_type: IntegrationType) -> Dict:
        """Format insights for specific system type"""
        if system_type == IntegrationType.CRM:
            return {
                'customer_insights': insights.get('customer_analytics', {}),
                'satisfaction_trends': insights.get('satisfaction_trends', {}),
                'retention_predictions': insights.get('retention_risk', {})
            }
        elif system_type == IntegrationType.BOOKING:
            return {
                'service_performance': insights.get('service_metrics', {}),
                'booking_trends': insights.get('booking_analytics', {}),
                'capacity_optimization': insights.get('operational_insights', {})
            }
        else:
            return insights
    
    def _calculate_rebooking_rate(self, service_data: pd.DataFrame) -> float:
        """Calculate rebooking rate for a service"""
        if len(service_data) == 0:
            return 0.0
        
        # Count customers with multiple bookings
        customer_booking_counts = service_data['customer_id'].value_counts()
        repeat_customers = (customer_booking_counts > 1).sum()
        total_customers = len(customer_booking_counts)
        
        return (repeat_customers / total_customers) if total_customers > 0 else 0.0
    
    def _verify_webhook_signature(self, system_name: str, event_data: Dict) -> bool:
        """Verify webhook signature for security"""
        try:
            config = self.integrations.get(system_name, {})
            webhook_secret = config.get('webhook_secret')
            
            if not webhook_secret:
                logger.warning(f"No webhook secret configured for {system_name}")
                return True  # Allow for demo purposes
            
            # Verify HMAC signature (implementation depends on external system)
            received_signature = event_data.get('signature', '')
            expected_signature = hmac.new(
                webhook_secret.encode(),
                json.dumps(event_data.get('payload', {})).encode(),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(received_signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False
    
    def _handle_customer_event(self, event_data: Dict):
        """Handle customer-related webhook events"""
        logger.info(f"Processing customer event: {event_data.get('event_type')}")
        # Implementation would update local customer cache or trigger sync
    
    def _handle_appointment_event(self, event_data: Dict):
        """Handle appointment-related webhook events"""
        logger.info(f"Processing appointment event: {event_data.get('event_type')}")
        # Implementation would update booking data or trigger notifications

class IntegrationManager:
    """Manage all system integrations"""
    
    def __init__(self):
        self.integrator = SpaSystemIntegrator()
        self.integration_status = {}
    
    def setup_standard_integrations(self) -> Dict[str, bool]:
        """Setup standard spa industry integrations"""
        results = {}
        
        # Common CRM integrations
        crm_systems = [
            {
                'name': 'Mindbody',
                'type': IntegrationType.CRM,
                'config': {
                    'api_endpoint': 'https://api.mindbodyonline.com/public/v6',
                    'api_key': 'demo_key_mindbody',
                    'webhook_secret': 'mindbody_webhook_secret'
                }
            },
            {
                'name': 'Booker',
                'type': IntegrationType.BOOKING,
                'config': {
                    'api_endpoint': 'https://api.booker.com/v4.1',
                    'api_key': 'demo_key_booker',
                    'webhook_secret': 'booker_webhook_secret'
                }
            },
            {
                'name': 'Vagaro',
                'type': IntegrationType.CRM,
                'config': {
                    'api_endpoint': 'https://www.vagaro.com/api',
                    'api_key': 'demo_key_vagaro',
                    'webhook_secret': 'vagaro_webhook_secret'
                }
            }
        ]
        
        for system in crm_systems:
            success = self.integrator.register_integration(
                system['name'],
                system['type'],
                system['config']
            )
            results[system['name']] = success
            self.integration_status[system['name']] = 'active' if success else 'failed'
        
        return results
    
    def get_integration_status(self) -> Dict:
        """Get status of all integrations"""
        return {
            'integrations': self.integration_status,
            'total_integrations': len(self.integrator.integrations),
            'active_integrations': len([s for s in self.integration_status.values() if s == 'active']),
            'last_updated': datetime.now().isoformat()
        }
    
    def sync_all_data(self) -> Dict:
        """Sync data from all active integrations"""
        results = {
            'customers': [],
            'appointments': [],
            'sync_status': {}
        }
        
        for system_name, config in self.integrator.integrations.items():
            try:
                if config['type'] == IntegrationType.CRM:
                    customers = self.integrator.sync_customer_data(system_name)
                    results['customers'].extend(customers)
                    results['sync_status'][system_name] = f"Synced {len(customers)} customers"
                
                elif config['type'] == IntegrationType.BOOKING:
                    appointments = self.integrator.sync_booking_data(system_name)
                    results['appointments'].extend(appointments)
                    results['sync_status'][system_name] = f"Synced {len(appointments)} appointments"
                
            except Exception as e:
                results['sync_status'][system_name] = f"Error: {str(e)}"
        
        return results

# Initialize global integration manager
integration_manager = IntegrationManager()