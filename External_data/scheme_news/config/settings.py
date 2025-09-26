"""
Configuration settings for Kerala News Scraper
"""
import os

class Config:
    # Project Info
    PROJECT_NAME = "Kerala Agriculture & Weather News Scraper"
    VERSION = "1.0.0"
    
    # Scraping Settings
    DEFAULT_DELAY = 2  # seconds between requests
    MAX_CONCURRENT_REQUESTS = 5
    REQUEST_TIMEOUT = 30
    RETRY_ATTEMPTS = 3
    
    # File Paths
    OUTPUT_DIR = "output"
    LOGS_DIR = "logs"
    
    # Kerala Districts
    KERALA_DISTRICTS = [
        "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha",
        "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad",
        "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
    ]
    
    # User Agents
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    # Expanded keywords for agriculture filtering
    AGRICULTURE_KEYWORDS = [
        # English keywords
        "agriculture", "farming", "crop", "harvest", "irrigation", "fertilizer",
        "paddy", "rice", "coconut", "spice", "rubber", "tea", "coffee",
        "weather", "rain", "drought", "flood", "monsoon", "kerala", "krishi",
        "banana", "ginger", "cardamom", "pepper", "farmers", "cultivation",
        "seeds", "pesticide", "organic", "dairy", "milk", "cattle", "cow",
        "chicken", "poultry", "fish", "aquaculture", "plantation", "garden",
        "farm", "field", "soil", "water", "climate", "season", "yield",
        "production", "market", "price", "subsidy", "scheme", "technology",
        "innovation", "sustainable", "bio", "natural", "rural", "village",
        
        # Malayalam keywords (in English script for detection)
        "കൃഷി", "കർഷകൻ", "കർഷകർ", "നെല്ല്", "നെല്ലുകൃഷി", "തേങ്ങ", "റബ്ബർ",
        "കാപ്പി", "ചായ", "ഇഞ്ചി", "ഏലം", "കുരുമുളക്", "വാഴ", "പച്ചക്കറി",
        "മഴ", "വരൾച്ച", "വെള്ളപ്പൊക്കം", "കാലാവസ്ഥ", "വിള", "വിത്ത്", "വളം",
        "പശു", "പാൽ", "മുട്ട", "കോഴി", "മത്സ്യം", "തോട്ടം", "പൂന്തോട്ടം",
        "ഗാക്ക്", "ശതാവരി", "കുങ്കുമപ്പൂവ്", "കൂൺ", "ചന്ദനം", "കറുവപ്പട്ട",
        "പാൽ", "ക്ഷീരം", "ഡയറി", "മഗ്നീഷ്യം", "പ്ലാന്റേഷൻ", "വിപണി",
        
        # Common terms found in agriculture articles
        "gac", "fruit", "magnesium", "deficiency", "cows", "plantation",
        "challenges", "fertilizer", "shortage", "welfare", "patent",
        "procurement", "sandalwood", "mushroom", "saffron", "asparagus"
    ]

config = Config()
