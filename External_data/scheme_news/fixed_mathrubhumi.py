"""
Fixed Mathrubhumi scraper that extracts individual article full content
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.base_scraper import BaseScraper
from datetime import datetime
import re

class FixedMathrubhumiScraper(BaseScraper):
    def __init__(self, source_config):
        super().__init__(source_config)
    
    def extract_individual_article_urls(self, soup):
        """Extract individual article URLs from listing page"""
        article_urls = []
        
        # Look for agriculture article links - these are the specific patterns used by Mathrubhumi
        selectors = [
            'a[href*="gac-fruit"]',
            'a[href*="rubber"]',
            'a[href*="magnesium"]', 
            'a[href*="fertilizer"]',
            'a[href*="coconut"]',
            'a[href*="rice"]',
            'a[href*="agriculture"]',
            'a[href*="farming"]'
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    if href.startswith('/'):
                        full_url = "https://www.mathrubhumi.com" + href
                    else:
                        full_url = href
                    
                    if full_url not in article_urls:
                        article_urls.append(full_url)
        
        return article_urls

    def extract_full_article(self, article_url):
        """Extract full content from individual article page"""
        print(f"🔍 Extracting full content from: {article_url}")
        
        html = self.get_page(article_url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        # Extract title
        title = "No Title"
        title_selectors = ['h1', '.headline', '.story-title', 'title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                if len(title) > 10:
                    break
        
        # Extract content - try multiple methods
        content = ""
        content_selectors = [
            '.story-content',
            '.article-content',
            '.post-content',
            '[data-testid="story-content"]',
            'article',
            '.content'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Remove unwanted elements
                for unwanted in content_elem(['script', 'style', 'nav', 'footer', 'header', '.ads', '.advertisement']):
                    unwanted.decompose()
                
                content = content_elem.get_text(separator='\n', strip=True)
                if len(content) > 200:  # Substantial content
                    break
        
        # If no specific content found, extract from paragraphs
        if not content or len(content) < 100:
            paragraphs = soup.find_all('p')
            content_parts = []
            for p in paragraphs:
                p_text = p.get_text().strip()
                if len(p_text) > 20:  # Avoid short fragments
                    content_parts.append(p_text)
            
            content = '\n\n'.join(content_parts)
        
        return {
            'title': title,
            'content': content,
            'url': article_url
        }

    def scrape_articles(self):
        """Main scraping method"""
        articles = []
        
        # Get the listing page first
        main_url = "https://www.mathrubhumi.com/agriculture"
        print(f"📄 Getting article list from: {main_url}")
        
        html = self.get_page(main_url)
        if not html:
            return articles
        
        soup = self.parse_html(html)
        
        # Extract individual article URLs
        article_urls = self.extract_individual_article_urls(soup)
        print(f"📋 Found {len(article_urls)} individual article URLs")
        
        # Extract full content from each article
        for i, url in enumerate(article_urls[:10]):  # Limit to 10 articles
            print(f"\n📰 Processing article {i+1}/{min(10, len(article_urls))}")
            
            article_data = self.extract_full_article(url)
            if article_data and len(article_data['content']) > 100:
                full_article = {
                    'url': article_data['url'],
                    'source': self.source_config['name'],
                    'category': self.source_config['category'],
                    'language': self.source_config['language'],
                    'scraped_at': datetime.now().isoformat(),
                    'title': article_data['title'],
                    'content': article_data['content'],
                    'date': '',
                    'author': '',
                    'images': [],
                    'keywords': self.extract_keywords(article_data['title'] + " " + article_data['content'])
                }
                
                articles.append(full_article)
                print(f"✅ SUCCESS: {article_data['title'][:60]}...")
                print(f"   Content length: {len(article_data['content'])} characters")
            else:
                print(f"❌ FAILED: Insufficient content")
            
            # Rate limiting
            self.rate_limit()
        
        return articles

# Test the fixed scraper
if __name__ == "__main__":
    from config.sources import ALL_SOURCES
    from utils.file_manager import FileManager
    
    print("🔧 TESTING FIXED MATHRUBHUMI SCRAPER")
    print("="*50)
    
    source_config = ALL_SOURCES['mathrubhumi_agriculture']
    scraper = FixedMathrubhumiScraper(source_config)
    
    articles = scraper.run()
    
    if articles:
        print(f"\n🎉 SUCCESS! Found {len(articles)} full articles")
        
        # Save articles
        file_manager = FileManager()
        filename = file_manager.save_articles_to_text(articles, "mathrubhumi_fixed")
        
        print(f"💾 Saved to: {filename}")
        
        # Show sample
        sample = articles[0]
        print(f"\n📖 SAMPLE FULL ARTICLE:")
        print(f"Title: {sample['title']}")
        print(f"Content length: {len(sample['content'])} characters")
        print(f"Content preview: {sample['content'][:300]}...")
    else:
        print("❌ No articles extracted")
