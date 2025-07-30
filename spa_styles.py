"""
Luxurious Spa-Inspired Styling for Feel Good Spas Business Intelligence
Premium design with elegant gradients, animations, and interactive elements
"""

def get_premium_spa_css():
    """Return premium spa-inspired CSS styling with luxury design elements"""
    return """
    <style>
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global premium styling */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 25%, #2c5364 50%, #5f9ea0 75%, #98d8c8 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif !important;
        min-height: 100vh;
    }
    
    /* Premium overlay pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(120, 252, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(152, 216, 200, 0.15) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Main container styling */
    .main .block-container {
        padding: 3rem 2rem;
        max-width: 1400px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
        margin: 2rem auto;
    }
    
    /* Premium title styling */
    h1 {
        font-family: 'Playfair Display', serif !important;
        background: linear-gradient(135deg, #78fcff 0%, #98d8c8 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 1rem !important;
        text-shadow: 0 4px 20px rgba(120, 252, 255, 0.3);
        letter-spacing: -0.02em;
    }
    
    h2 {
        font-family: 'Montserrat', sans-serif !important;
        color: #78fcff !important;
        font-weight: 600 !important;
        font-size: 2.2rem !important;
        margin: 2rem 0 1rem 0 !important;
        text-shadow: 0 2px 10px rgba(120, 252, 255, 0.3);
    }
    
    h3 {
        color: #98d8c8 !important;
        font-weight: 500 !important;
        font-size: 1.4rem !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    /* Premium metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border: 2px solid rgba(120, 252, 255, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(120, 252, 255, 0.2), transparent);
        transition: left 0.6s;
    }
    
    [data-testid="metric-container"]:hover::before {
        left: 100%;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(120, 252, 255, 0.6);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 40px rgba(120, 252, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    /* Premium button styling */
    .stButton > button {
        background: linear-gradient(135deg, #78fcff 0%, #98d8c8 50%, #5f9ea0 100%);
        color: #0f2027 !important;
        border: none;
        border-radius: 16px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 8px 24px rgba(120, 252, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 15px 40px rgba(120, 252, 255, 0.6),
            0 0 30px rgba(120, 252, 255, 0.4);
    }
    
    /* Premium chat styling */
    .stChatMessage {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        border: 1px solid rgba(120, 252, 255, 0.2) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(15px) !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Premium sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 32, 39, 0.9) 0%, rgba(32, 58, 67, 0.9) 100%);
        border-right: 2px solid rgba(120, 252, 255, 0.3);
        backdrop-filter: blur(20px);
    }
    
    /* Premium DataFrame styling */
    .dataframe {
        border: 2px solid rgba(120, 252, 255, 0.3) !important;
        border-radius: 16px !important;
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        backdrop-filter: blur(15px) !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #78fcff, #98d8c8) !important;
        color: #0f2027 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
    }
    
    .dataframe td {
        color: #ffffff !important;
        padding: 0.8rem !important;
        border-bottom: 1px solid rgba(120, 252, 255, 0.1) !important;
    }
    
    /* Premium message styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(152, 216, 200, 0.2), rgba(120, 252, 255, 0.1)) !important;
        border: 2px solid rgba(152, 216, 200, 0.5) !important;
        border-radius: 16px !important;
        color: #98d8c8 !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 99, 132, 0.2), rgba(255, 159, 64, 0.1)) !important;
        border: 2px solid rgba(255, 99, 132, 0.5) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(120, 252, 255, 0.2), rgba(152, 216, 200, 0.1)) !important;
        border: 2px solid rgba(120, 252, 255, 0.5) !important;
        border-radius: 16px !important;
        color: #78fcff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Premium input styling */
    .stSelectbox > div > div, .stTextInput > div > div > input {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05)) !important;
        border: 2px solid rgba(120, 252, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSelectbox > div > div:focus-within, .stTextInput > div > div > input:focus {
        border-color: rgba(120, 252, 255, 0.8) !important;
        box-shadow: 0 0 20px rgba(120, 252, 255, 0.3) !important;
    }
    
    /* Premium tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border: 2px solid rgba(120, 252, 255, 0.2);
        border-radius: 12px;
        color: #98d8c8;
        font-weight: 500;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #78fcff, #98d8c8);
        color: #0f2027 !important;
        border-color: #78fcff;
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(120, 252, 255, 0.4);
    }
    
    /* Premium logo design */
    .spa-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin: 2rem 0 3rem 0;
        padding: 2rem;
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 24px;
        border: 2px solid rgba(120, 252, 255, 0.3);
        backdrop-filter: blur(20px);
        box-shadow: 
            0 8px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .spa-logo::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(120, 252, 255, 0.1), transparent);
        animation: rotate 8s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .spa-logo-icon {
        font-size: 4rem;
        background: linear-gradient(135deg, #78fcff 0%, #98d8c8 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 4px 20px rgba(120, 252, 255, 0.5));
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .spa-logo-text h1 {
        margin: 0 !important;
        font-size: 3rem !important;
        background: linear-gradient(135deg, #78fcff 0%, #98d8c8 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .spa-logo-text p {
        margin: 0.5rem 0 0 0;
        color: #98d8c8;
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Premium header styling */
    .spa-header {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        border-radius: 24px;
        padding: 3rem;
        margin-bottom: 3rem;
        border: 2px solid rgba(120, 252, 255, 0.3);
        backdrop-filter: blur(25px);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .spa-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #78fcff, #98d8c8, #78fcff, transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Chart container styling */
    .chart-container {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid rgba(120, 252, 255, 0.2);
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        border-color: rgba(120, 252, 255, 0.4);
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.3),
            0 0 40px rgba(120, 252, 255, 0.2);
    }
    
    /* Fade in animation */
    .fade-in {
        animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #78fcff, #98d8c8) !important;
        box-shadow: 0 0 20px rgba(120, 252, 255, 0.5);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #78fcff, #98d8c8);
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(120, 252, 255, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #98d8c8, #78fcff);
    }
    
    /* Premium text styling */
    p, div, span {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Enhanced Sidebar styling with high visibility */
    .css-1d391kg, section[data-testid="stSidebar"] > div {
        background: linear-gradient(145deg, rgba(15, 32, 39, 0.98), rgba(44, 83, 100, 0.95)) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 3px solid rgba(120, 252, 255, 0.6) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Sidebar container enhanced visibility */
    section[data-testid="stSidebar"] {
        background: linear-gradient(145deg, rgba(15, 32, 39, 0.98), rgba(44, 83, 100, 0.95)) !important;
        border-right: 3px solid rgba(120, 252, 255, 0.6) !important;
    }
    
    /* All sidebar navigation links with maximum visibility */
    section[data-testid="stSidebar"] a, 
    section[data-testid="stSidebar"] .css-12oz5g7,
    .css-1d391kg a,
    .css-1d391kg .css-12oz5g7 {
        color: #ffffff !important;
        background: linear-gradient(135deg, rgba(120, 252, 255, 0.15), rgba(152, 216, 200, 0.1)) !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        margin: 0.8rem 0 !important;
        transition: all 0.3s ease !important;
        border: 2px solid rgba(120, 252, 255, 0.4) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Sidebar link hover states */
    section[data-testid="stSidebar"] a:hover,
    section[data-testid="stSidebar"] .css-12oz5g7:hover,
    .css-1d391kg a:hover,
    .css-1d391kg .css-12oz5g7:hover {
        background: linear-gradient(135deg, rgba(120, 252, 255, 0.3), rgba(152, 216, 200, 0.2)) !important;
        border-color: rgba(120, 252, 255, 0.8) !important;
        color: #78fcff !important;
        transform: translateX(8px) scale(1.02) !important;
        box-shadow: 0 4px 20px rgba(120, 252, 255, 0.4) !important;
    }
    
    /* Active/selected sidebar link */
    section[data-testid="stSidebar"] a[aria-selected="true"],
    section[data-testid="stSidebar"] .css-12oz5g7[aria-selected="true"],
    .css-1d391kg a[aria-selected="true"],
    .css-1d391kg .css-12oz5g7[aria-selected="true"] {
        background: linear-gradient(135deg, rgba(120, 252, 255, 0.4), rgba(152, 216, 200, 0.3)) !important;
        border-color: #78fcff !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 25px rgba(120, 252, 255, 0.5) !important;
        transform: scale(1.05) !important;
    }
    
    /* All sidebar text visibility enhancement */
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    .css-1d391kg *,
    .css-1d391kg p,
    .css-1d391kg span,
    .css-1d391kg div {
        color: rgba(255, 255, 255, 0.98) !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar title/header visibility */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #78fcff !important;
        text-shadow: 0 2px 8px rgba(120, 252, 255, 0.4) !important;
        font-weight: 700 !important;
    }
    
    /* Force maximum visibility for navigation text */
    .css-1d391kg, 
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] nav {
        color: #ffffff !important;
        background: linear-gradient(145deg, rgba(15, 32, 39, 1), rgba(44, 83, 100, 0.98)) !important;
    }
    
    /* Navigation menu items enhanced visibility */
    nav[aria-label="main navigation"] a,
    .css-17eq0hr a,
    .css-1vq4p4l a {
        color: #ffffff !important;
        background: rgba(120, 252, 255, 0.15) !important;
        border: 2px solid rgba(120, 252, 255, 0.4) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-decoration: none !important;
        display: block !important;
        transition: all 0.3s ease !important;
    }
    
    nav[aria-label="main navigation"] a:hover,
    .css-17eq0hr a:hover,
    .css-1vq4p4l a:hover {
        background: rgba(120, 252, 255, 0.25) !important;
        border-color: rgba(120, 252, 255, 0.7) !important;
        color: #78fcff !important;
        transform: translateX(4px) !important;
    }
    
    /* Additional Streamlit sidebar visibility fixes */
    .st-emotion-cache-16txtl3, 
    .st-emotion-cache-1y4p8pa, 
    .st-emotion-cache-10oheav {
        background: linear-gradient(145deg, rgba(15, 32, 39, 1), rgba(44, 83, 100, 0.95)) !important;
        color: #ffffff !important;
    }
    
    /* Streamlit sidebar menu links universal fix */
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] ul,
    section[data-testid="stSidebar"] .element-container,
    .css-1d391kg li,
    .css-1d391kg ul,
    .css-1d391kg .element-container {
        background: rgba(120, 252, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        margin: 4px 0 !important;
        padding: 8px !important;
    }
    
    /* Text contrast enhancement for all sidebar content */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
        background: transparent !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7) !important;
        font-weight: 600 !important;
    }
    
    /* Loading animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(120, 252, 255, 0.3);
        border-radius: 50%;
        border-top-color: #78fcff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
    """

def get_premium_spa_logo_html():
    """Return premium spa logo HTML with luxury design"""
    return """
    <div class="spa-logo fade-in">
        <div class="spa-logo-icon">🏨</div>
        <div class="spa-logo-text">
            <h1>Feel Good Spas</h1>
            <p>Executive Intelligence Suite</p>
        </div>
    </div>
    """

def apply_premium_spa_theme():
    """Apply premium spa theme to Streamlit app"""
    import streamlit as st
    st.markdown(get_premium_spa_css(), unsafe_allow_html=True)
    st.markdown(get_premium_spa_logo_html(), unsafe_allow_html=True)

# Legacy function for backward compatibility
def apply_spa_theme():
    """Legacy function - redirects to premium theme"""
    apply_premium_spa_theme()

def get_spa_css():
    """Legacy function - redirects to premium CSS"""
    return get_premium_spa_css()

def get_spa_logo_html():
    """Legacy function - redirects to premium logo"""
    return get_premium_spa_logo_html()