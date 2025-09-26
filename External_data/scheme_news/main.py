"""
Kerala Agriculture News Scraper - Main Execution File
AGRICULTURE & WEATHER CONTENT ONLY
"""

import sys
import os
import argparse
from datetime import datetime
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_single_scraper(source_name):
    """Run a single scraper by source name"""
    from config.sources import ALL_SOURCES
    from utils.file_manager import FileManager
    from multi_source_scraper import AgricultureOnlyScraper
    
    if source_name not in ALL_SOURCES:
        print(f"❌ Error: Source '{source_name}' not found in configuration")
        available_sources = ', '.join(ALL_SOURCES.keys())
        print(f"Available sources: {available_sources}")
        return []
    
    source_config = ALL_SOURCES[source_name]
    
    print(f"\n🌾 Starting AGRICULTURE-ONLY scraper for: {source_config['name']}")
    print(f"📰 Category: {source_config['category']}")
    print(f"🌐 Language: {source_config['language']}")
    print(f"🔗 URLs: {', '.join(source_config['news_urls'])}")
    
    try:
        scraper = AgricultureOnlyScraper(source_config)
        
        print("🚀 Starting to scrape agriculture content...")
        articles = scraper.run()
        
        if articles:
            file_manager = FileManager()
            filename = file_manager.save_articles_to_text(articles, source_name)
            print(f"✅ Successfully scraped {len(articles)} agriculture articles")
            print(f"📝 Output saved to: {filename}")
            
            # Show sample article
            if articles:
                sample_article = articles[0]
                print(f"\n🌾 Sample Agriculture Article:")
                print(f"Title: {sample_article.get('title', 'No title')}")
                print(f"Keywords: {', '.join(sample_article.get('keywords', [])[:5])}")
                print(f"Content: {sample_article.get('content', 'No content')[:200]}...")
        else:
            print("❌ No agriculture-related content found")
        
        return articles
        
    except Exception as e:
        print(f"❌ Error running scraper: {str(e)}")
        return []

def test_agriculture_scraper():
    """Test agriculture scraper"""
    print("🧪 TESTING AGRICULTURE-ONLY SCRAPER")
    print("=" * 50)
    print("Testing with strict agriculture/weather filtering...\n")
    
    articles = run_single_scraper('mathrubhumi_agriculture')
    
    if articles:
        print(f"\n🎉 TEST SUCCESSFUL!")
        print(f"✅ Found {len(articles)} agriculture articles")
        print(f"📁 Check the 'output/daily/' folder for text files")
        
        print(f"\n🌾 Agriculture Article Titles Found:")
        for i, article in enumerate(articles[:3], 1):
            title = article.get('title', 'No title')
            keywords = ', '.join(article.get('keywords', [])[:3])
            print(f"   {i}. {title}")
            print(f"      Keywords: {keywords}")
    else:
        print(f"\n⚠️  TEST COMPLETED - No agriculture content found")
    
    return articles

def list_agriculture_sources():
    """List all agriculture sources"""
    from config.sources import ALL_SOURCES
    
    print("📋 AGRICULTURE & WEATHER NEWS SOURCES:")
    print("=" * 45)
    
    categories = {}
    for name, config in ALL_SOURCES.items():
        cat = config['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, config['name'], config['language']))
    
    for category, sources in categories.items():
        print(f"\n📂 {category.upper().replace('_', ' ')}:")
        for source_key, source_name, language in sources:
            print(f"   🌾 {source_key}")
            print(f"      Name: {source_name}")
            print(f"      Language: {language}")

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Kerala Agriculture & Weather News Scraper - AGRICULTURE CONTENT ONLY',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --test                              # Test agriculture scraper
  python main.py --agriculture                       # Scrape ALL agriculture sources
  python main.py --source mathrubhumi_agriculture    # Run specific source
  python main.py --list                              # List agriculture sources
        """
    )
    
    parser.add_argument('--agriculture', action='store_true', help='Scrape ALL agriculture sources')
    parser.add_argument('--source', type=str, help='Run specific agriculture source')
    parser.add_argument('--test', action='store_true', help='Test agriculture scraper')
    parser.add_argument('--list', action='store_true', help='List all agriculture sources')
    
    args = parser.parse_args()
    
    # Setup output directories
    os.makedirs('output/daily', exist_ok=True)
    os.makedirs('output/weekly', exist_ok=True) 
    os.makedirs('output/monthly', exist_ok=True)
    os.makedirs('output/consolidated', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    print("🌾 KERALA AGRICULTURE & WEATHER NEWS SCRAPER 🌾")
    print("🔒 STRICT AGRICULTURE/WEATHER FILTERING ENABLED")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if args.list:
        list_agriculture_sources()
    elif args.test:
        test_agriculture_scraper()
    elif args.source:
        run_single_scraper(args.source)
    elif args.agriculture:
        from multi_source_scraper import scrape_agriculture_only
        scrape_agriculture_only()
    else:
        print("Please specify an option. Use --help for usage information.")
        print("\n🌾 Quick start commands:")
        print("   python main.py --test         # Test agriculture scraper")
        print("   python main.py --agriculture  # Scrape ALL agriculture sources")
        print("   python main.py --list         # Show agriculture sources")

if __name__ == "__main__":
    main()
