"""
File Manager - Create output2 at root level and delete output folder after consolidation
"""
import os
import json
import shutil
from datetime import datetime

class FileManager:
    """File manager for agriculture articles"""
    
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """Create directories"""
        os.makedirs('output', exist_ok=True)
        os.makedirs('output/daily', exist_ok=True)
        os.makedirs('output/consolidated', exist_ok=True)
        os.makedirs('output2', exist_ok=True)  # Create output2 at root level (same as config)
    
    def save_articles_to_text(self, articles, source_name):
        """Save articles to individual text file in output/daily (temporary)"""
        if not articles:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/daily/{source_name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"AGRICULTURE CONTENT - {source_name.upper()}\n")
                f.write("=" * 60 + "\n")
                f.write(f"Source: {source_name}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Items: {len(articles)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, article in enumerate(articles, 1):
                    title = article.get('title', 'No Title')
                    content = article.get('content', 'No Content')
                    keywords = article.get('keywords', [])
                    
                    f.write(f"ITEM {i}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"TITLE: {title}\n\n")
                    f.write(f"CONTENT:\n{content}\n\n")
                    f.write(f"KEYWORDS: {', '.join(keywords)}\n")
                    f.write("\n" + "=" * 60 + "\n\n")
            
            return filename
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return None
    
    def save_news_consolidated(self, news_articles):
        """Save NEWS consolidated file in output2/news.txt"""
        if not news_articles:
            return None
        
        filename = "output2/news.txt"  # Root level output2
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("AGRICULTURE NEWS CONSOLIDATED\n")
                f.write("Economic Times + Times of India\n")
                f.write("=" * 70 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total News Articles: {len(news_articles)}\n")
                
                # Source breakdown
                sources = {}
                for article in news_articles:
                    source = article.get('source', 'Unknown')
                    sources[source] = sources.get(source, 0) + 1
                
                f.write(f"Sources: {', '.join([f'{s} ({c})' for s, c in sources.items()])}\n")
                f.write("=" * 70 + "\n\n")
                
                f.write("CONTENT TYPE: Latest Agriculture News & Market Updates\n")
                f.write("USE CASE: Daily news, market trends, policy updates\n")
                f.write("=" * 70 + "\n\n")
                
                for i, article in enumerate(news_articles, 1):
                    title = article.get('title', 'No Title')
                    content = article.get('content', 'No Content')
                    source = article.get('source', 'Unknown')
                    keywords = article.get('keywords', [])
                    
                    f.write(f"NEWS ARTICLE {i}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"SOURCE: {source}\n")
                    f.write(f"TITLE: {title}\n\n")
                    f.write(f"CONTENT:\n{content}\n\n")
                    f.write(f"KEYWORDS: {', '.join(keywords)}\n")
                    f.write("\n" + "=" * 70 + "\n\n")
            
            return filename
            
        except Exception as e:
            print(f"Error saving news consolidated file: {str(e)}")
            return None
    
    def save_schemes_consolidated(self, scheme_articles):
        """Save SCHEMES consolidated file in output2/schemes.txt"""
        if not scheme_articles:
            return None
        
        filename = "output2/schemes.txt"  # Root level output2
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("AGRICULTURE SCHEMES CONSOLIDATED\n")
                f.write("Government Schemes for Farmers\n")
                f.write("=" * 70 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Government Schemes: {len(scheme_articles)}\n")
                
                # Source breakdown
                sources = {}
                for article in scheme_articles:
                    source = article.get('source', 'Unknown')
                    sources[source] = sources.get(source, 0) + 1
                
                f.write(f"Sources: {', '.join([f'{s} ({c})' for s, c in sources.items()])}\n")
                f.write("=" * 70 + "\n\n")
                
                f.write("CONTENT TYPE: Government Schemes & Policy Details\n")
                f.write("USE CASE: Scheme information, eligibility, benefits, application process\n")
                f.write("SCHEMES INCLUDED: PM-KISAN, PMFBY, PMKSY, eNAM, Soil Health Card, etc.\n")
                f.write("=" * 70 + "\n\n")
                
                for i, article in enumerate(scheme_articles, 1):
                    title = article.get('title', 'No Title')
                    content = article.get('content', 'No Content')
                    source = article.get('source', 'Unknown')
                    keywords = article.get('keywords', [])
                    
                    f.write(f"GOVERNMENT SCHEME {i}\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"SOURCE: {source}\n")
                    f.write(f"SCHEME NAME: {title}\n\n")
                    f.write(f"SCHEME DETAILS:\n{content}\n\n")
                    f.write(f"KEYWORDS: {', '.join(keywords)}\n")
                    f.write("\n" + "=" * 70 + "\n\n")
            
            return filename
            
        except Exception as e:
            print(f"Error saving schemes consolidated file: {str(e)}")
            return None
    
    def delete_output_folder(self):
        """Delete the entire output folder after consolidation"""
        try:
            if os.path.exists('output'):
                shutil.rmtree('output')
                print("🗑️  Deleted temporary 'output' folder")
                return True
            else:
                print("⚠️  'output' folder not found")
                return False
        except Exception as e:
            print(f"❌ Error deleting output folder: {str(e)}")
            return False
    
    def save_consolidated_text(self, all_articles, filename_prefix="agriculture_consolidated"):
        """Save general consolidated file (NOT USED)"""
        return None
