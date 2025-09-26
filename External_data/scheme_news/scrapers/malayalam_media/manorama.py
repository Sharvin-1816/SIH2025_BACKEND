"""
Malayala Manorama Agriculture news scraper
"""
from scrapers.base_scraper import BaseScraper

class ManoramaScraper(BaseScraper):
    """Scraper for Malayala Manorama agriculture news"""
    
    def scrape_articles(self):
        """Scrape articles from Manorama agriculture section"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                # Get the main page
                html_content = self.get_page(news_url)
                if not html_content:
                    continue
                
                soup = self.parse_html(html_content)
                
                # Find article links
                article_links = self.find_article_links(soup, self.source_config['base_url'])
                
                self.logger.info(f"Found {len(article_links)} article links")
                
                # Scrape each article
                for link in article_links[:10]:  # Limit to 10 articles per run
                    article_html = self.get_page(link)
                    if article_html:
                        article_soup = self.parse_html(article_html)
                        article_data = self.extract_article_data(article_soup, link)
                        
                        # Only add if we got meaningful content
                        if len(article_data['title']) > 10 and len(article_data['content']) > 100:
                            articles.append(article_data)
                    
                    # Rate limiting
                    self.rate_limit()
                
            except Exception as e:
                self.logger.error(f"Error scraping {news_url}: {str(e)}")
        
        return articles
