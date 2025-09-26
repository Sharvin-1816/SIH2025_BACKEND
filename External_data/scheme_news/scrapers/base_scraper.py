"""
Enhanced Scraper with Testbook Agriculture Schemes Extraction
"""
import requests
import time
import random
import logging
from datetime import datetime
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class BaseScraper(ABC):
    """Enhanced scraper with Testbook scheme extraction"""
    
    def __init__(self, source_config):
        self.source_config = source_config
        self.session = requests.Session()
        self.setup_session()
        self.setup_logging()
        
    def setup_session(self):
        """Configure requests session"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })
        self.session.timeout = 30
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_page(self, url):
        """Fetch webpage with retries"""
        for attempt in range(2):
            try:
                self.logger.info(f"Fetching: {url}")
                response = self.session.get(url)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < 1:
                    time.sleep(3)
        return None
    
    def parse_html(self, html_content):
        """Parse HTML"""
        return BeautifulSoup(html_content, 'html.parser')
    
    def clean_text(self, text):
        """Basic text cleaning"""
        if not text:
            return ""
        
        text = text.replace('*agriculture*', 'agriculture')
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def light_refine_content(self, text):
        """Light content refinement"""
        if not text:
            return ""
        
        # Remove obvious junk
        light_junk_patterns = [
            r'Advertisement',
            r'Must Watch',
            r'Subscribe now',
            r'Follow us on',
            r'Share this',
            r'Read more about',
            r'Also read:',
            r'Copyright.*?reserved',
            r'\(Reuters\)|\(PTI\)|\(ANI\)',
            r'Last Modified\s*:.*',
            r'Published\s*:.*',
            r'Updated\s*:.*',
            r'Download.*?app.*',
            r'Get.*?SuperCoaching.*',
            r'Scan this QR code.*',
            r'₹\d+.*Your Total Savings.*'
        ]
        
        for pattern in light_junk_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up spacing
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def is_meaningful_content(self, title, content):
        """Content validation"""
        if not title or not content:
            return False, "Empty content"
        
        if len(content) < 50:  # Increased minimum for schemes
            return False, f"Content too short ({len(content)} chars)"
        
        if len(title) < 15:
            return False, f"Title too short ({len(title)} chars)"
        
        return True, "Content accepted"
    
    def extract_synopsis_articles(self, soup, url):
        """Main extraction router"""
        articles = []
        
        self.logger.info(f"🔍 Processing: {url}")
        
        if 'testbook' in url.lower():
            self.logger.info("📚 Using TESTBOOK SCHEME extraction")
            articles = self.extract_testbook_schemes(soup, url)
            
        elif 'timesofindia' in url.lower():
            self.logger.info("📰 Using TOI extraction methods")
            articles = self.extract_toi_articles(soup, url)
            
        else:
            self.logger.info("📈 Using Economic Times extraction")
            articles = self.extract_et_complete_articles(soup, url)
        
        self.logger.info(f"🎯 TOTAL ARTICLES FOUND: {len(articles)}")
        return articles
    
    def extract_testbook_schemes(self, soup, url):
        """Extract agriculture schemes from Testbook"""
        schemes = []
        
        self.logger.info("📚 Starting Testbook agriculture schemes extraction...")
        
        try:
            # Method 1: Extract scheme sections based on the content structure
            schemes = self.extract_testbook_scheme_sections(soup)
            
            # Method 2: If scheme sections not found, try heading-based extraction
            if not schemes:
                schemes = self.extract_testbook_by_headings(soup)
            
            # Method 3: Fallback to paragraph-based extraction
            if not schemes:
                schemes = self.extract_testbook_by_paragraphs(soup)
            
        except Exception as e:
            self.logger.error(f"❌ Error in Testbook extraction: {str(e)}")
        
        self.logger.info(f"📚 TESTBOOK RESULT: {len(schemes)} schemes extracted")
        return schemes
    
    def extract_testbook_scheme_sections(self, soup):
        """Extract schemes by identifying scheme sections"""
        schemes = []
        
        # Based on your content, look for scheme patterns
        scheme_indicators = [
            'Pradhan Mantri', 'PM-', 'PM ', 'Yojana', 'Scheme', 'Mission', 
            'Abhiyan', 'PMFBY', 'PMKSY', 'eNAM', 'NFSM', 'SHC', 'NBM',
            'Krishi', 'Agriculture', 'Farmer'
        ]
        
        # Find all headings and their associated content
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in headings:
            heading_text = self.clean_text(heading.get_text())
            
            # Check if heading indicates a scheme
            if (len(heading_text) > 10 and 
                any(indicator in heading_text for indicator in scheme_indicators)):
                
                # Get content following this heading
                content_parts = []
                current = heading.next_sibling
                
                # Collect content until next heading or end
                while current and current.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if current.name == 'p':
                        para_text = self.clean_text(current.get_text())
                        if len(para_text) > 30:
                            content_parts.append(para_text)
                    elif hasattr(current, 'find_all'):
                        # Check for paragraphs within this element
                        paras = current.find_all('p')
                        for p in paras:
                            para_text = self.clean_text(p.get_text())
                            if len(para_text) > 30:
                                content_parts.append(para_text)
                    
                    current = current.next_sibling
                    
                    # Limit to avoid infinite loops
                    if len(content_parts) > 10:
                        break
                
                if content_parts:
                    content = '\n\n'.join(content_parts)
                    content = self.light_refine_content(content)
                    
                    is_good, reason = self.is_meaningful_content(heading_text, content)
                    if is_good:
                        schemes.append({
                            'title': heading_text,
                            'content': content
                        })
                        self.logger.info(f"✅ Scheme: {heading_text}")
        
        return schemes
    
    def extract_testbook_by_headings(self, soup):
        """Extract by analyzing heading structure"""
        schemes = []
        
        # Get all text and look for scheme patterns
        full_text = soup.get_text()
        
        # Split by known scheme names from the content
        known_schemes = [
            'Pradhan Mantri Kisan Samman Nidhi',
            'Pradhan Mantri Fasal Bima Yojana',
            'Pradhan Mantri Krishi Sinchai Yojana', 
            'Ayushman Sahakar Scheme',
            'eNAM',
            'Pradhan Mantri Kisan Maandhan Yojana',
            'Krishi Kalyan Abhiyan',
            'Soil Health Card',
            'National Bamboo Mission',
            'Krishonnati Yojana',
            'Yuva Sahakar',
            'PM-AASHA',
            'Paramparagat Krishi Vikas Yojana',
            'National Food Security Mission',
            'Pandit Deen Dayal Upadhyay',
            'Rashtriya Gokul Mission',
            'Mission Amrit Sarovar',
            'National Beekeeping and Honey Mission',
            'National Mission on Edible Oils',
            'National Mission on Natural Farming'
        ]
        
        for scheme_name in known_schemes:
            # Find scheme in text
            scheme_pattern = rf'({re.escape(scheme_name)}.*?)(?=(?:{"|".join([re.escape(s) for s in known_schemes])})|$)'
            matches = re.findall(scheme_pattern, full_text, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                clean_content = self.clean_text(match)
                clean_content = self.light_refine_content(clean_content)
                
                if len(clean_content) > 100:
                    # Split into title and content
                    lines = clean_content.split('\n')
                    title = lines[0] if lines else scheme_name
                    content = '\n'.join(lines[1:]) if len(lines) > 1 else clean_content
                    
                    is_good, reason = self.is_meaningful_content(title, content)
                    if is_good:
                        schemes.append({
                            'title': title,
                            'content': content
                        })
        
        return schemes
    
    def extract_testbook_by_paragraphs(self, soup):
        """Extract by analyzing paragraphs"""
        schemes = []
        
        # Get all paragraphs
        paragraphs = soup.find_all('p')
        
        current_scheme = None
        content_parts = []
        
        for para in paragraphs:
            para_text = self.clean_text(para.get_text())
            
            if not para_text or len(para_text) < 20:
                continue
            
            # Check if this paragraph starts a new scheme
            scheme_starters = [
                'The Pradhan Mantri',
                'PM-', 
                'eNAM',
                'The National',
                'Krishi Kalyan',
                'Soil Health Card',
                'Mission Amrit'
            ]
            
            is_scheme_start = any(para_text.startswith(starter) for starter in scheme_starters)
            
            if is_scheme_start:
                # Save previous scheme if exists
                if current_scheme and content_parts:
                    content = '\n\n'.join(content_parts)
                    content = self.light_refine_content(content)
                    
                    is_good, reason = self.is_meaningful_content(current_scheme, content)
                    if is_good:
                        schemes.append({
                            'title': current_scheme,
                            'content': content
                        })
                
                # Start new scheme
                current_scheme = para_text.split('.')[0]  # First sentence as title
                content_parts = [para_text]
            
            elif current_scheme:
                # Add to current scheme
                content_parts.append(para_text)
                
                # Limit content parts to avoid very long schemes
                if len(content_parts) > 15:
                    content = '\n\n'.join(content_parts)
                    content = self.light_refine_content(content)
                    
                    is_good, reason = self.is_meaningful_content(current_scheme, content)
                    if is_good:
                        schemes.append({
                            'title': current_scheme,
                            'content': content
                        })
                    
                    current_scheme = None
                    content_parts = []
        
        # Don't forget the last scheme
        if current_scheme and content_parts:
            content = '\n\n'.join(content_parts)
            content = self.light_refine_content(content)
            
            is_good, reason = self.is_meaningful_content(current_scheme, content)
            if is_good:
                schemes.append({
                    'title': current_scheme,
                    'content': content
                })
        
        return schemes
    
    # Keep existing TOI and ET methods
    def extract_toi_articles(self, soup, url):
        """TOI extraction using multiple methods"""
        articles = []
        
        methods = [
            self.extract_toi_complete_articles,
            self.extract_toi_by_paragraphs,
            self.extract_toi_by_sentences
        ]
        
        for i, method in enumerate(methods, 1):
            try:
                method_articles = method(soup, url)
                if method_articles:
                    existing_titles = {article['title'].lower() for article in articles}
                    new_articles = [a for a in method_articles if a['title'].lower() not in existing_titles]
                    articles.extend(new_articles)
                    self.logger.info(f"✅ TOI Method {i} found {len(new_articles)} new articles")
            except Exception as e:
                self.logger.debug(f"TOI Method {i} failed: {str(e)}")
                continue
        
        return articles
    
    def extract_toi_complete_articles(self, soup, url):
        """TOI Method 1"""
        articles = []
        full_text = soup.get_text(separator='\n')
        paragraphs = full_text.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if len(para) < 50:
                continue
            
            clean_para = self.clean_text(para)
            sentences = clean_para.split('. ')
            
            if len(sentences) >= 2:
                title = sentences[0].strip()
                content = '. '.join(sentences[1:]).strip()
                
                if len(title) > 15 and len(content) > 30:
                    refined_title = self.light_refine_content(title)
                    refined_content = self.light_refine_content(content)
                    
                    is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                    if is_good:
                        articles.append({'title': refined_title, 'content': refined_content})
        
        return articles
    
    def extract_toi_by_paragraphs(self, soup, url):
        """TOI Method 2"""
        articles = []
        full_text = soup.get_text(separator='\n')
        lines = [line.strip() for line in full_text.split('\n') if len(line.strip()) > 30]
        
        i = 0
        while i < len(lines) - 1:
            potential_title = self.clean_text(lines[i])
            content_lines = []
            j = i + 1
            while j < len(lines) and j < i + 4:
                content_lines.append(lines[j])
                j += 1
            
            potential_content = ' '.join(content_lines)
            potential_content = self.clean_text(potential_content)
            
            if len(potential_title) > 20 and len(potential_content) > 50:
                refined_title = self.light_refine_content(potential_title)
                refined_content = self.light_refine_content(potential_content)
                
                is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                if is_good:
                    articles.append({'title': refined_title, 'content': refined_content})
                    i = j
                else:
                    i += 1
            else:
                i += 1
        
        return articles
    
    def extract_toi_by_sentences(self, soup, url):
        """TOI Method 3"""
        articles = []
        full_text = soup.get_text()
        sentences = full_text.split('. ')
        
        i = 0
        while i < len(sentences) - 2:
            title = self.clean_text(sentences[i])
            content_sentences = sentences[i+1:i+4]
            content = '. '.join(content_sentences)
            content = self.clean_text(content)
            
            if len(title) > 25 and len(content) > 60:
                refined_title = self.light_refine_content(title)
                refined_content = self.light_refine_content(content)
                
                is_good, reason = self.is_meaningful_content(refined_title, refined_content)
                if is_good:
                    articles.append({'title': refined_title, 'content': refined_content})
                    i += 4
                else:
                    i += 1
            else:
                i += 1
        
        return articles
    
    def extract_et_complete_articles(self, soup, url):
        """Economic Times extraction"""
        articles = []
        containers = soup.select('.eachStory')
        
        for container in containers:
            try:
                title_elem = container.find(['h1', 'h2', 'h3']) or container.select_one('.story-headline, .headline, .title')
                title = "Economic Times News"
                
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                
                content = self.clean_text(container.get_text())
                if title in content:
                    content = content.replace(title, '').strip()
                
                title = self.light_refine_content(title)
                content = self.light_refine_content(content)
                
                is_good, reason = self.is_meaningful_content(title, content)
                if is_good:
                    articles.append({'title': title, 'content': content})
                
            except Exception as e:
                continue
        
        return articles
    
    def extract_keywords(self, text):
        """Extract keywords"""
        refined_text = self.light_refine_content(text)
        words = refined_text.lower().split()
        keywords = []
        
        for word in words:
            if len(word) > 4 and word.isalpha():
                keywords.append(word)
        
        return list(dict.fromkeys(keywords))[:8]
    
    def rate_limit(self):
        """Rate limiting"""
        time.sleep(2)
    
    @abstractmethod
    def scrape_articles(self):
        pass
    
    def run(self):
        """Run scraper"""
        self.logger.info(f"Starting scraper for {self.source_config['name']}")
        articles = self.scrape_articles()
        self.logger.info(f"Found {len(articles)} articles/schemes")
        return articles
