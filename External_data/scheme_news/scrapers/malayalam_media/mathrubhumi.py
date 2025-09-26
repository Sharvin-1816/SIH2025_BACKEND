"""
Mathrubhumi Agriculture news scraper - CORRECTED VERSION
"""
from scrapers.base_scraper import BaseScraper
from datetime import datetime

class MathrubhumiScraper(BaseScraper):
    """Scraper for Mathrubhumi agriculture news - extracts individual articles"""
    
    def find_article_links(self, soup, base_url):
        """Find individual article URLs from listing page - UPDATED SELECTORS"""
        article_links = []
        
        # Updated selectors based on actual website structure
        selectors = [
            # Direct agriculture article links
            'a[href*="/agriculture/news/"]',
            'a[href*="/agriculture/features/"]',
            'a[href*="/agriculture/tips/"]',
            # General article links that might be agriculture-related
            'a[href*="gac-fruit"]',
            'a[href*="rubber"]', 
            'a[href*="magnesium"]',
            'a[href*="plantation"]',
            'a[href*="fertilizer"]',
            'a[href*="farming"]',
            'a[href*="crop"]',
            'a[href*="coconut"]',
            'a[href*="rice"]',
            'a[href*="dairy"]'
        ]
        
        # Also look for any links in agriculture sections
        agriculture_sections = soup.find_all(['div', 'section'], class_=lambda x: x and 'agriculture' in x.lower() if x else False)
        
        for section in agriculture_sections:
            links = section.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                if href and ('/news/' in href or '/agriculture/' in href):
                    if href.startswith('/'):
                        full_url = base_url.rstrip('/') + href
                        if full_url not in article_links:
                            article_links.append(full_url)
        
        # If no specific selectors work, try general approach
        if not article_links:
            # Look for any links that contain agriculture-related keywords in the link text
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                link_text = link.get_text().lower()
                
                # Check if link text contains Malayalam agriculture terms
                agriculture_terms = ['കൃഷി', 'കർഷക', 'നെല്ല്', 'തേങ്ങ', 'റബ്ബർ', 'കാപ്പി', 'പശു', 'പാൽ']
                english_terms = ['gac', 'fruit', 'rubber', 'farming', 'agriculture', 'coconut', 'rice', 'dairy']
                
                has_agriculture_term = any(term in link_text for term in agriculture_terms + english_terms)
                
                if href and has_agriculture_term and ('/news/' in href or 'mathrubhumi.com' in href):
                    if href.startswith('/'):
                        full_url = base_url.rstrip('/') + href
                    elif href.startswith('http'):
                        full_url = href
                    else:
                        continue
                    
                    if full_url not in article_links and len(article_links) < 15:
                        article_links.append(full_url)
        
        return article_links
    
    def extract_article_content(self, soup):
        """Extract full content from individual article page"""
        content_selectors = [
            '.story-content',
            '.article-body', 
            '.content',
            '.story-body',
            'div[data-testid="story-content"]',
            '.field-body',
            '.post-content',
            '.entry-content',
            '[class*="content"]',
            '[class*="story"]',
            '[class*="article"]'
        ]
        
        content = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Remove unwanted elements
                for unwanted in content_elem(['script', 'style', 'nav', 'footer', 'header', '.advertisement', '.ads', '.related', '.share']):
                    unwanted.decompose()
                
                content = content_elem.get_text(separator='\n', strip=True)
                if len(content) > 100:  # Only use if substantial content
                    break
        
        # If no specific content found, try to get main content
        if not content or len(content) < 100:
            # Remove common navigation and non-content elements
            for unwanted in soup(['nav', 'header', 'footer', 'aside', '.menu', '.navigation', '.ads', '.advertisement']):
                unwanted.decompose()
            
            # Get text from main content areas
            main_content = soup.find(['main', 'article', 'div'], class_=lambda x: x and any(term in x.lower() for term in ['content', 'story', 'article', 'post']) if x else False)
            if main_content:
                content = main_content.get_text(separator='\n', strip=True)
        
        return self.clean_text(content)
    
    def extract_article_title(self, soup):
        """Extract article title"""
        title_selectors = [
            'h1.story-headline',
            'h1',
            '.headline',
            '.story-title',
            '.article-title',
            '[class*="headline"]',
            '[class*="title"]'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                if len(title) > 5 and title.lower() not in ['agriculture', 'news', 'home']:
                    return self.clean_text(title)
        
        # Try to get title from meta tags
        meta_title = soup.find('meta', property='og:title') or soup.find('meta', attrs={'name': 'title'})
        if meta_title:
            title = meta_title.get('content', '').strip()
            if len(title) > 5:
                return self.clean_text(title)
        
        # Last resort - get from page title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
            # Remove site name and common suffixes
            title = title.replace(' - Mathrubhumi', '').replace(' | Mathrubhumi', '').strip()
            if len(title) > 5:
                return self.clean_text(title)
        
        return "No Title"
    
    def scrape_articles(self):
        """Scrape individual articles from Mathrubhumi agriculture section"""
        articles = []
        
        for news_url in self.source_config['news_urls']:
            try:
                self.logger.info(f"Processing listing page: {news_url}")
                
                # Get the listing page
                html_content = self.get_page(news_url)
                if not html_content:
                    continue
                
                soup = self.parse_html(html_content)
                
                # Find individual article links
                article_links = self.find_article_links(soup, self.source_config['base_url'])
                
                self.logger.info(f"Found {len(article_links)} individual article links")
                
                # Print found links for debugging
                for i, link in enumerate(article_links[:5], 1):
                    self.logger.info(f"  {i}. {link}")
                
                # Scrape each individual article
                for i, article_url in enumerate(article_links[:10]):  # Limit to 10 articles
                    try:
                        self.logger.info(f"Scraping article {i+1}/{min(10, len(article_links))}: {article_url}")
                        
                        # Get individual article page
                        article_html = self.get_page(article_url)
                        if not article_html:
                            continue
                        
                        article_soup = self.parse_html(article_html)
                        
                        # Extract title and content
                        title = self.extract_article_title(article_soup)
                        content = self.extract_article_content(article_soup)
                        
                        self.logger.info(f"Extracted - Title: {title[:50]}... | Content length: {len(content)}")
                        
                        if len(title) > 5 and len(content) > 50:
                            article_data = {
                                'url': article_url,
                                'source': self.source_config['name'],
                                'category': self.source_config['category'],
                                'language': self.source_config['language'],
                                'scraped_at': datetime.now().isoformat(),
                                'title': title,
                                'content': content,
                                'date': '',
                                'author': '',
                                'images': [],
                                'keywords': self.extract_keywords(title + " " + content)
                            }
                            
                            articles.append(article_data)
                            self.logger.info(f"✅ Successfully added article: {title[:50]}...")
                        else:
                            self.logger.warning(f"⚠️ Insufficient content - Title len: {len(title)}, Content len: {len(content)}")
                        
                        # Rate limiting
                        self.rate_limit()
                        
                    except Exception as e:
                        self.logger.error(f"❌ Error processing {article_url}: {str(e)}")
                        continue
                
            except Exception as e:
                self.logger.error(f"❌ Error processing listing page {news_url}: {str(e)}")
        
        self.logger.info(f"📊 Total articles extracted: {len(articles)}")
        return articles
