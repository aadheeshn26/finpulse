"""
Base scraper class providing common functionality for all scrapers.

This module contains the base class that all specific scrapers inherit from,
providing common functionality like rate limiting, error handling, and logging.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper(ABC):
    """
    Abstract base class for all data scrapers.
    
    Provides common functionality like:
    - Rate limiting to respect website policies
    - HTTP session management with retries
    - Error handling and logging
    - Progress tracking
    """
    
    def __init__(
        self, 
        delay_seconds: float = 1.0,
        max_retries: int = 3,
        timeout: int = 30,
        user_agent: str = None
    ):
        """
        Initialize the base scraper.
        
        Args:
            delay_seconds: Delay between requests to avoid overwhelming servers
            max_retries: Maximum number of retry attempts for failed requests
            timeout: Request timeout in seconds
            user_agent: Custom User-Agent header for requests
        """
        self.delay_seconds = delay_seconds
        self.max_retries = max_retries
        self.timeout = timeout
        self.user_agent = user_agent or "FinPulse/1.0.0 (+https://github.com/aadheeshn26/finpulse)"
        
        # Set up logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create HTTP session with retry strategy
        self.session = self._create_session()
        
        # Statistics
        self.stats = {
            'requests_made': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'items_scraped': 0,
            'start_time': None,
            'end_time': None
        }
    
    def _create_session(self) -> requests.Session:
        """Create HTTP session with retry strategy and proper headers."""
        session = requests.Session()
        
        # Set up retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        return session
    
    def _make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """
        Make HTTP request with rate limiting and error handling.
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object or None if request failed
        """
        self.stats['requests_made'] += 1
        
        try:
            # Rate limiting
            if self.stats['requests_made'] > 1:
                time.sleep(self.delay_seconds)
            
            # Make request
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            # Check if request was successful
            if response.status_code == 200:
                self.stats['successful_requests'] += 1
                self.logger.debug(f"Successfully fetched: {url}")
                return response
            else:
                self.stats['failed_requests'] += 1
                self.logger.warning(f"Request failed with status {response.status_code}: {url}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.stats['failed_requests'] += 1
            self.logger.error(f"Request error for {url}: {e}")
            return None
    
    def _extract_text_content(self, html: str) -> str:
        """
        Extract clean text content from HTML.
        
        Args:
            html: Raw HTML content
            
        Returns:
            Clean text content
        """
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _detect_ticker_symbols(self, text: str) -> List[str]:
        """
        Detect stock ticker symbols in text using regex patterns.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of detected ticker symbols
        """
        import re
        
        # Common ticker symbol patterns
        patterns = [
            r'\$([A-Z]{1,5})',  # $AAPL format
            r'\b([A-Z]{1,5})\s+stock',  # AAPL stock format
            r'\b(NASDAQ:|NYSE:)([A-Z]{1,5})',  # NASDAQ:AAPL format
        ]
        
        tickers = set()
        
        for pattern in patterns:
            matches = re.findall(pattern, text.upper())
            if isinstance(matches[0], tuple) if matches else False:
                # Handle tuple results from groups
                tickers.update([match[-1] for match in matches])
            else:
                tickers.update(matches)
        
        # Filter out common false positives
        false_positives = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'}
        
        tickers = [t for t in tickers if t not in false_positives and len(t) <= 5]
        
        return sorted(list(tickers))
    
    def _calculate_reading_time(self, text: str) -> float:
        """Calculate estimated reading time in minutes."""
        words = len(text.split())
        # Average reading speed: 200 words per minute
        return round(words / 200, 1)
    
    def start_scraping(self):
        """Mark the start of scraping process."""
        self.stats['start_time'] = datetime.utcnow()
        self.logger.info(f"Starting {self.__class__.__name__} scraping session")
    
    def end_scraping(self):
        """Mark the end of scraping process and log statistics."""
        self.stats['end_time'] = datetime.utcnow()
        
        if self.stats['start_time']:
            duration = self.stats['end_time'] - self.stats['start_time']
            self.logger.info(f"Scraping completed in {duration}")
        
        self.logger.info(f"Scraping statistics: {self.stats}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        return self.stats.copy()
    
    @abstractmethod
    def scrape(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Abstract method to be implemented by specific scrapers.
        
        Returns:
            List of scraped items as dictionaries
        """
        pass
    
    def __enter__(self):
        """Context manager entry."""
        self.start_scraping()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.end_scraping()
        
        if self.session:
            self.session.close()
