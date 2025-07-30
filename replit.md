# Feel Good Spas Business Intelligence Solution

## Overview

This is a comprehensive business intelligence platform that transforms vCon (Virtualized Conversation) conversation data into actionable insights for Feel Good Spas management. The system provides data processing, analytics, executive dashboards, and a conversational AI interface to help spa managers understand customer sentiment, agent performance, and operational efficiency.

## User Preferences

Preferred communication style: Simple, everyday language.

## Project Status - COMPLETED ✅

**Date:** July 30, 2025
**Status:** All 4 key outcomes successfully delivered

### Recent Achievements
- Fixed duplicate "Feel Good Spas" titles across all dashboard sections
- Removed empty columns from all layouts (Dashboard, Predictive Analytics, Executive Reports, Conversational AI)  
- Applied consistent premium spa theme styling to all pages
- Enhanced agent performance heatmap with robust error handling and data validation
- Optimized layout spacing and content organization across all dashboard sections
- Created comprehensive project documentation including README.md and completion summary
- Prepared for version control with .gitignore and project structure setup

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web application interface
- **Multi-page Application**: Organized with separate pages for different analytics views
  - Main dashboard (app.py)
  - Executive Dashboard (pages/1_Dashboard.py)
  - Agent Analytics (pages/2_Agent_Analytics.py)
  - Location Performance (pages/3_Location_Performance.py)
  - Conversational AI (pages/4_Conversational_AI.py)
  - Predictive Analytics (pages/5_Predictive_Analytics.py)
  - Executive Reports (pages/6_Executive_Reports.py)
  - CRM Integration (pages/7_CRM_Integration.py)
  - Database Administration (pages/8_Database_Admin.py)
- **Visualization**: Plotly for interactive charts and graphs
- **Responsive Design**: Wide layout configuration optimized for business dashboards

### Backend Architecture
- **Language**: Python 3.11+
- **Data Processing Pipeline**: Multi-stage processing from raw vCon JSON to enriched CSV
- **Business Intelligence Engine**: Custom analytics engine (business_intelligence.py)
- **Conversational AI**: OpenAI GPT-4o integration for natural language queries
- **Modular Design**: Separated concerns with utility modules for data processing and visualization

### Data Processing Pipeline
1. **vCon Parser** (vcon_parser.py): Parses IETF-compliant vCon conversation format
2. **Data Processor** (data_processor.py): Transforms raw JSON into structured CSV with enrichments
3. **Business Intelligence Engine**: Generates executive summaries and analytics
4. **Real-time Processing**: On-demand data loading and analysis

## Key Components

### Data Layer
- **Input Format**: vCon JSON files containing customer service conversations
- **Processing**: Sentiment analysis, topic classification, quality scoring
- **Output Format**: Structured CSV with enriched business metrics
- **Storage**: PostgreSQL database with CSV fallback (processed_spa_data.csv)
- **Database**: 570 conversation records loaded into PostgreSQL for improved querying and scalability

### Analytics Engine
- **Business Intelligence Module**: Core analytics calculations and insights generation
- **Metrics Calculation**: KPIs, performance scores, trend analysis
- **Executive Summaries**: High-level business insights and recommendations
- **Multi-dimensional Analysis**: By location, agent, time period, and customer sentiment

### Visualization Layer
- **Interactive Dashboards**: Executive, agent, and location-specific views
- **Chart Types**: KPIs, trends, heatmaps, distribution charts
- **Real-time Updates**: Dynamic filtering and data refresh capabilities
- **Export Functionality**: Data download capabilities for offline analysis

### AI Integration
- **Groq AI**: Free, fast AI models for natural language processing
- **Conversational Interface**: Natural language queries about business data
- **Context Awareness**: Maintains conversation history for coherent interactions
- **Business Question Library**: Pre-built analytics queries for common business needs
- **Predictive Analytics**: Advanced customer satisfaction and retention prediction system
- **Executive Reporting**: Automated report generation with scheduled insights delivery
- **CRM Integration**: Comprehensive integration with spa management and booking systems

## Data Flow

1. **Data Ingestion**: Raw vCon JSON files from attached_assets directory
2. **Parsing**: vCon format validation and conversation extraction
3. **Enrichment**: Sentiment analysis, quality scoring, business metric calculation
4. **Storage**: Processed data saved as structured CSV
5. **Analytics**: Business intelligence engine processes data for insights
6. **Visualization**: Streamlit interface presents data through interactive dashboards
7. **AI Interaction**: Conversational AI provides natural language access to insights

## External Dependencies

### Required APIs
- **Groq API**: For free conversational AI functionality (Llama models)
- **API Key Management**: Environment variable GROQ_API_KEY required

### Python Libraries
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualization library
- **TextBlob**: Natural language processing for sentiment analysis
- **Groq**: Official Groq Python client for free AI models
- **NumPy**: Numerical computing support
- **SQLAlchemy**: Database toolkit and ORM for PostgreSQL integration
- **Psycopg2**: PostgreSQL database adapter for Python

### Data Dependencies
- **vCon Files**: Customer service conversation data in JSON format
- **Business Questions**: Pre-defined analytics queries in CSV format
- **Configuration**: Environment variables for API keys and settings
- **PostgreSQL Database**: Primary data storage with automatic failover to CSV

## Deployment Strategy

### Local Development
- **Setup**: Python environment with required dependencies
- **Data Processing**: Run data_processor.py to generate processed_spa_data.csv
- **Application Launch**: streamlit run app.py --server.port 5000
- **Port Configuration**: Automatic forwarding to port 5000 for consistency

### Production Considerations
- **Scalability**: PostgreSQL database implemented for production-ready data storage
- **Security**: API key management through environment variables
- **Performance**: Database-optimized queries with CSV fallback for reliability
- **Monitoring**: Comprehensive logging infrastructure with database admin interface

### Architecture Decisions

**Problem**: Need to process unstructured conversation data into business insights
**Solution**: Multi-stage pipeline with vCon parsing, enrichment, and analytics
**Alternatives**: Direct database integration, real-time streaming processing
**Pros**: Simple, maintainable, follows data standards (vCon format)
**Cons**: File-based storage limits scalability

**Problem**: Provide intuitive business intelligence interface
**Solution**: Streamlit multi-page application with role-based views
**Alternatives**: Traditional BI tools, custom React/Vue.js frontend
**Pros**: Rapid development, Python-native, good for analytics
**Cons**: Limited customization compared to custom frontend

**Problem**: Enable natural language data queries
**Solution**: Groq AI integration with business context for free usage
**Alternatives**: Custom NLP models, rule-based query systems, paid OpenAI
**Pros**: Advanced language understanding, minimal training required, completely free
**Cons**: External API dependency, but no usage costs

The system is designed for rapid prototyping and demonstration while maintaining extensibility for production deployment. The modular architecture allows for easy replacement of components as requirements evolve.