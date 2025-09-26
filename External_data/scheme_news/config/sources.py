"""
Agriculture Sources - Economic Times + Times of India + Testbook Schemes
"""

ALL_SOURCES = {
    "economic_times_agriculture": {
        "name": "Economic Times Agriculture",
        "base_url": "https://economictimes.indiatimes.com/",
        "news_urls": [
            "https://economictimes.indiatimes.com/news/economy/agriculture?from=mdr"
        ],
        "selectors": {
            "title": "h1, h2, h3, .story-headline, .headline, .artTitle, .eachStory h3",
            "content": ".artText, .story-content, .article-content, .summary, .eachStory, p",
            "date": ".date, .publish-date, .story-date, .time"
        },
        "category": "business_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "times_of_india_agriculture": {
        "name": "Times of India Agriculture",
        "base_url": "https://timesofindia.indiatimes.com/",
        "news_urls": [
            "https://timesofindia.indiatimes.com/topic/agriculture/news"
        ],
        "selectors": {
            "title": "h1, h2, h3, .headline, .story-headline, ._2-bYW, .EOHY_ZZ",
            "content": ".story-content, .article-content, ._s30J, .ga-headlines, .content, p",
            "date": "time, .publish_on, .date, ._3k8Kt"
        },
        "category": "news_agriculture",
        "language": "english",
        "scrape_method": "requests_bs4"
    },
    
    "testbook_agriculture_schemes": {
        "name": "Testbook Agriculture Schemes",
        "base_url": "https://testbook.com/",
        "news_urls": [
            "https://testbook.com/ias-preparation/agriculture-schemes-in-india"
        ],
        "selectors": {
            "title": "h1, h2, h3, h4, h5, h6",
            "content": "p, .content, .article-content, div",
            "date": ".date"
        },
        "category": "government_schemes",
        "language": "english",
        "scrape_method": "testbook_extractor"
    }
}

# NO KEYWORD FILTERING
KERALA_AGRICULTURE_KEYWORDS = []
REJECT_KEYWORDS = []
