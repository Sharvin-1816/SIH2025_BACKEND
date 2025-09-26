"""
Agriculture Scraper - Create output2 and delete output folder after consolidation
- Economic Times Agriculture News
- Times of India Agriculture News  
- Testbook Agriculture Schemes

Output: news.txt and schemes.txt in output2 folder, then delete output folder
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.sources import ALL_SOURCES
from scrapers.base_scraper import BaseScraper
from utils.file_manager import FileManager
from datetime import datetime
import time

class SimpleConsolidatedScraper(BaseScraper):
    """Scraper that creates simple consolidated files"""
    
    def scrape_articles(self):
        """Scrape using site-specific methods"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                self.logger.info(f"🔍 Processing: {news_url}")
                
                html = self.get_page(news_url)
                if not html:
                    continue
                
                soup = self.parse_html(html)
                
                # Extract using site-specific methods
                extracted_content = self.extract_synopsis_articles(soup, news_url)
                
                for content_data in extracted_content:
                    article = {
                        'url': news_url,
                        'source': self.source_config['name'],
                        'category': self.source_config['category'],
                        'language': self.source_config['language'],
                        'scraped_at': datetime.now().isoformat(),
                        'title': content_data['title'],
                        'content': content_data['content'],
                        'keywords': self.extract_keywords(content_data['title'] + " " + content_data['content'])
                    }
                    articles.append(article)
                
                self.rate_limit()
                
            except Exception as e:
                self.logger.error(f"Error processing {news_url}: {str(e)}")
                continue
        
        return articles

def main():
    """Main function with output2 folder and output folder deletion"""
    print("📚 AGRICULTURE SCRAPER - CLEAN OUTPUT")
    print("📰 News: Economic Times + Times of India")
    print("📋 Schemes: Testbook Government Schemes")
    print("📁 Final Output: output2/ folder only")
    print("🗑️  Temporary files will be cleaned up")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_articles = []
    news_articles = []  # For ET + TOI
    scheme_articles = []  # For Testbook schemes
    successful_sources = 0
    
    for source_name, source_config in ALL_SOURCES.items():
        print(f"\n📊 Processing: {source_config['name']}")
        print(f"🔗 URL: {source_config['news_urls'][0]}")
        
        if 'testbook' in source_name.lower():
            print("📋 SCHEMES → will go to output2/schemes.txt")
        else:
            print("📰 NEWS → will go to output2/news.txt")
        
        try:
            scraper = SimpleConsolidatedScraper(source_config)
            articles = scraper.run()
            
            if articles:
                all_articles.extend(articles)
                successful_sources += 1
                
                # Separate articles by type
                if 'testbook' in source_name.lower() or source_config.get('category') == 'government_schemes':
                    scheme_articles.extend(articles)
                    print(f"✅ SUCCESS: {len(articles)} SCHEMES extracted")
                else:
                    news_articles.extend(articles)
                    print(f"✅ SUCCESS: {len(articles)} NEWS articles extracted")
                
                total_chars = sum(len(a.get('content', '')) for a in articles)
                avg_chars = total_chars // len(articles)
                
                print(f"📊 Total content: {total_chars:,} characters")
                print(f"📊 Average per item: {avg_chars} characters")
                
                # Save individual file temporarily in output/daily
                file_manager = FileManager()
                filename = file_manager.save_articles_to_text(articles, source_name)
                print(f"💾 Temporary file: {filename}")
                
                # Show samples
                print(f"📋 Sample content:")
                for i, article in enumerate(articles[:2], 1):
                    title = article.get('title', '')[:70]
                    content_len = len(article.get('content', ''))
                    
                    print(f"   {i}. {title}...")
                    print(f"      📊 {content_len} characters")
                print()
            else:
                print("⚠️  No content extracted")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            print("🔍 Continuing to next source...")
        
        time.sleep(2)
    
    # Create consolidated files and clean up
    if all_articles:
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"✅ Successful sources: {successful_sources}/{len(ALL_SOURCES)}")
        print(f"📊 Total items: {len(all_articles)}")
        
        # Show breakdown
        print(f"\n📊 Content Breakdown:")
        print(f"   📰 News Articles: {len(news_articles)}")
        print(f"   📋 Government Schemes: {len(scheme_articles)}")
        
        file_manager = FileManager()
        
        # Create consolidated files in output2
        print(f"\n📁 CREATING CONSOLIDATED FILES IN OUTPUT2...")
        
        # Create NEWS consolidated file → output2/news.txt
        if news_articles:
            print(f"📰 Creating news.txt...")
            
            news_file = file_manager.save_news_consolidated(news_articles)
            
            news_total_chars = sum(len(a.get('content', '')) for a in news_articles)
            news_avg_chars = news_total_chars // len(news_articles)
            
            print(f"✅ NEWS FILE CREATED:")
            print(f"   📁 File: {news_file}")
            print(f"   📊 Articles: {len(news_articles)}")
            print(f"   📊 Total content: {news_total_chars:,} characters")
            print(f"   📰 Sources: Economic Times + Times of India")
        
        # Create SCHEMES consolidated file → output2/schemes.txt
        if scheme_articles:
            print(f"📋 Creating schemes.txt...")
            
            schemes_file = file_manager.save_schemes_consolidated(scheme_articles)
            
            schemes_total_chars = sum(len(a.get('content', '')) for a in scheme_articles)
            schemes_avg_chars = schemes_total_chars // len(scheme_articles)
            
            print(f"✅ SCHEMES FILE CREATED:")
            print(f"   📁 File: {schemes_file}")
            print(f"   📊 Schemes: {len(scheme_articles)}")
            print(f"   📊 Total content: {schemes_total_chars:,} characters")
            print(f"   📋 Source: Testbook Government Schemes")
        
        # DELETE THE OUTPUT FOLDER
        print(f"\n🗑️  CLEANING UP TEMPORARY FILES...")
        deletion_success = file_manager.delete_output_folder()
        
        if deletion_success:
            print(f"✅ Cleanup complete! Only output2/ folder remains.")
        else:
            print(f"⚠️  Cleanup had issues, but consolidated files are ready.")
        
        # Show final result
        print(f"\n🚀 FINAL RESULT:")
        print(f"📁 Folder: output2/ (same directory as config/)")
        print(f"📰 output2/news.txt - {len(news_articles)} news articles")
        print(f"📋 output2/schemes.txt - {len(scheme_articles)} government schemes")
        print(f"🗑️  Temporary 'output' folder deleted")
        print(f"💼 Clean setup ready for your farmer app!")
        
        return {
            'news_articles': news_articles,
            'scheme_articles': scheme_articles,
            'total_articles': all_articles
        }
    
    else:
        print("❌ No content found")
        return None

if __name__ == "__main__":
    main()
