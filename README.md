# Feel Good Spas Business Intelligence Solution

A comprehensive business intelligence platform that transforms conversational data (vCon format) into actionable insights for spa management through advanced analytics, real-time monitoring, and AI-driven performance optimization.

## 🎯 Project Overview

This solution addresses the challenge of extracting business value from customer service conversation data, providing Feel Good Spas management with intuitive dashboards, predictive analytics, and natural language business intelligence.

## 📋 Key Deliverables

### 1. Insight & Strategy Plan
**File:** `STRATEGY_PLAN.md`
- Comprehensive analysis of business value within conversation dataset
- Key insights: customer sentiment trends, agent performance metrics, call drivers
- Strategic recommendations for operational improvements

### 2. Transformed & Enriched Dataset
**Files:** `data_processor.py`, `processed_spa_data.csv`
- Processes raw `feel-good-spas-vcons.json` → structured CSV (570 records)
- Enriched with sentiment analysis, quality scores, topics, call outcomes
- PostgreSQL database integration for production scalability

### 3. Dashboard Concept
**Files:** `app.py`, `pages/`, `spa_styles.py`
- Multi-page Streamlit dashboard with premium spa theming
- Executive Dashboard, Agent Analytics, Location Performance views
- Real-time data visualization with interactive charts
- User-centric design for non-technical managers

### 4. Conversational AI System
**Files:** `conversational_ai.py`, `pages/4_Conversational_AI.py`
- Natural language business intelligence queries
- Groq AI integration (100% free) for conversational data analysis
- Export functionality and comprehensive analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database (optional - CSV fallback available)
- Groq API key (free at https://console.groq.com)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd feel-good-spas-bi
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or if using uv:
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   export GROQ_API_KEY="your-groq-api-key-here"
   export DATABASE_URL="your-postgresql-url" # Optional
   ```

4. **Process the data:**
   ```bash
   python data_processor.py
   ```

5. **Launch the application:**
   ```bash
   streamlit run app.py --server.port 5000
   ```

## 🏗️ Architecture

### Data Processing Pipeline
1. **vCon Parser** (`vcon_parser.py`) - Parses IETF-compliant conversation format
2. **Data Processor** (`data_processor.py`) - Transforms JSON → enriched CSV
3. **Business Intelligence** (`business_intelligence.py`) - Generates insights
4. **Database Layer** (`database.py`) - PostgreSQL integration with CSV fallback

### Frontend Architecture
- **Framework:** Streamlit with multi-page organization
- **Styling:** Custom premium spa theme (`spa_styles.py`)
- **Visualization:** Plotly for interactive charts
- **AI Integration:** Groq AI for conversational queries

### Key Components
- **Executive Dashboard** - High-level KPIs and trends
- **Agent Analytics** - Performance heatmaps and coaching recommendations
- **Location Performance** - Regional analysis and comparisons
- **Conversational AI** - Natural language business queries
- **Predictive Analytics** - Customer satisfaction and retention forecasting

## 📊 Features

### Business Intelligence
- Real-time KPI monitoring (Quality Score: 7.2/10, Satisfaction: 7.4/10)
- Sentiment analysis across 570 conversation records
- Agent performance tracking and coaching recommendations
- Location-based performance comparisons

### Advanced Analytics
- Customer satisfaction prediction models
- Retention risk analysis and early warning systems
- Business forecasting and trend analysis
- Performance heatmaps with drill-down capabilities

### Conversational AI
- Natural language queries: "Which agents need coaching?"
- Business context awareness and conversation history
- Pre-built question library for common business needs
- Export functionality for management reports

## 🎯 Business Value

### For Management
- **Operational Efficiency:** Identify underperforming locations and agents
- **Customer Experience:** Track satisfaction trends and sentiment patterns
- **Strategic Planning:** Data-driven decisions based on conversation analytics
- **Resource Optimization:** Targeted coaching and training recommendations

### Technical Benefits
- **Scalable Architecture:** PostgreSQL database with 570+ conversation records
- **Free AI Integration:** Groq-powered natural language processing
- **Production Ready:** Comprehensive error handling and data validation
- **Extensible Design:** Modular components for future enhancements

## 📁 Project Structure

```
feel-good-spas-bi/
├── README.md                   # This file
├── STRATEGY_PLAN.md           # Business insight & strategy analysis
├── replit.md                  # Technical architecture documentation
├── app.py                     # Main Streamlit application
├── data_processor.py          # Data transformation pipeline
├── vcon_parser.py            # vCon format parser
├── business_intelligence.py   # Core analytics engine
├── conversational_ai.py      # AI chat system
├── spa_styles.py             # Premium UI theming
├── database.py               # Database integration
├── pages/                    # Multi-page dashboard components
│   ├── 1_Dashboard.py        # Executive dashboard
│   ├── 2_Agent_Analytics.py  # Agent performance analysis
│   ├── 3_Location_Performance.py # Location comparisons
│   ├── 4_Conversational_AI.py    # AI chat interface
│   ├── 5_Predictive_Analytics.py # Forecasting models
│   ├── 6_Executive_Reports.py    # Automated reporting
│   └── 7_CRM_Integration.py      # System integrations
├── utils/                    # Utility modules
│   ├── data_utils.py        # Data loading and validation
│   ├── database_utils.py    # Database operations
│   └── visualization_utils.py # Chart generation
├── attached_assets/          # Source data files
│   ├── feel-good-spas-vcons.json # Raw conversation data
│   └── untagged-questions-assessment.csv # Business questions
└── processed_spa_data.csv   # Enriched dataset output
```

## 🔧 Configuration

### Database Setup (Optional)
The system supports PostgreSQL for production environments with automatic CSV fallback:

```python
# Automatic database connection with fallback
df = load_processed_data()  # Uses DB if available, else CSV
```

### AI Configuration
Set up free Groq AI integration:

```bash
# Get free API key from https://console.groq.com
export GROQ_API_KEY="gsk-your-key-here"
```

## 📈 Performance Metrics

- **Data Processing:** 570 conversation records successfully parsed and enriched
- **Database Performance:** PostgreSQL integration with optimized queries
- **AI Response Time:** Sub-second natural language query processing
- **Dashboard Load:** Real-time visualization with sub-2-second refresh

## 🧪 Testing

### Data Validation
```bash
python -c "from utils.data_validation import validate_data; validate_data()"
```

### Heatmap Functionality
```bash
python fix_heatmap_and_styling.py  # Validates agent performance visualization
```

### AI Integration
```bash
python -c "from conversational_ai import SpaConversationalAI; ai = SpaConversationalAI(); print('AI initialized successfully')"
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 5000
```

### Production Deployment
- Configure PostgreSQL database connection
- Set environment variables for API keys
- Deploy via Replit, Heroku, or similar platform
- Ensure port 5000 is accessible

## 🤝 Contributing

This project follows professional development practices:

1. **Version Control:** Regular commits with clear messages
2. **Documentation:** Comprehensive inline and external documentation  
3. **Testing:** Data validation and component testing
4. **Code Quality:** Modular design with separation of concerns

## 📄 License

This project is developed for Feel Good Spas business intelligence requirements.

## 📞 Support

For technical questions or business inquiries:
- Review `STRATEGY_PLAN.md` for business context
- Check `replit.md` for technical architecture details
- Use the Conversational AI feature for data queries

---

**Built with:** Python, Streamlit, Plotly, PostgreSQL, Groq AI  
**Data Source:** vCon conversation format (570 records)  
**Business Focus:** Spa management operational excellence