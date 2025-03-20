#!/usr/bin/env python3
import os
import re
import argparse
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)

class AcademicCrawler:
    """
    Web crawler to fetch academic papers and format them in Cranfield format
    for use with the IR Java application.
    """
    
    def __init__(self, start_urls, output_dir="src/main/resources/crawled", 
                 max_pages=100, delay=1, max_workers=5):
        """
        Initialize the crawler with starting URLs and configuration.
        
        Args:
            start_urls (list): List of URLs to start crawling from
            output_dir (str): Directory to save crawled documents
            max_pages (int): Maximum number of pages to crawl
            delay (float): Delay between requests in seconds
            max_workers (int): Number of concurrent workers for fetching
        """
        self.start_urls = start_urls
        self.output_dir = output_dir
        self.max_pages = max_pages
        self.delay = delay
        self.max_workers = max_workers
        
        self.visited_urls = set()
        self.queue = list(start_urls)
        self.papers = []
        self.document_id = 1
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "results"), exist_ok=True)
    
    def is_valid_url(self, url):
        """
        Check if URL is valid and should be crawled.
        
        Args:
            url (str): URL to check
            
        Returns:
            bool: True if URL should be crawled, False otherwise
        """
        parsed = urlparse(url)
        
        # Check if URL is valid
        if not parsed.netloc or not parsed.scheme:
            return False
        
        # Only crawl HTTP(S) URLs
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for file extensions to avoid
        avoid_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.zip', '.rar', 
                          '.jpg', '.jpeg', '.png', '.gif', '.svg', '.mp4', '.avi', '.mov']
        
        if any(url.lower().endswith(ext) for ext in avoid_extensions):
            return False
        
        return True
    
    def extract_paper_info(self, url, html_content):
        """
        Extract title, author, and content from HTML.
        
        Args:
            url (str): URL of the page
            html_content (str): HTML content of the page
            
        Returns:
            dict or None: Paper information if found, None otherwise
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try to extract title
        title = None
        title_tag = soup.find('h1') or soup.find('title')
        if title_tag:
            title = title_tag.get_text().strip()
        
        # Try to extract author
        author = None
        author_tag = soup.find('meta', {'name': 'author'}) or soup.find(class_=re.compile(r'author', re.I))
        if author_tag:
            if author_tag.get('content'):
                author = author_tag.get('content').strip()
            else:
                author = author_tag.get_text().strip()
        
        # Extract body text
        body = ""
        
        # Look for article content in common containers
        content_tags = soup.find_all(['article', 'div', 'section'], 
                                   class_=re.compile(r'(content|article|text|body)', re.I))
        
        if content_tags:
            for tag in content_tags:
                # Skip navigation, header, footer, sidebar
                if any(cls in tag.get('class', []) for cls in ['nav', 'header', 'footer', 'sidebar']):
                    continue
                
                # Extract paragraphs
                paragraphs = tag.find_all('p')
                if paragraphs:
                    body += "\n".join(p.get_text().strip() for p in paragraphs)
        
        # If no content found, use all paragraphs
        if not body:
            paragraphs = soup.find_all('p')
            body = "\n".join(p.get_text().strip() for p in paragraphs)
        
        # Clean up the text
        body = re.sub(r'\s+', ' ', body).strip()
        
        # Check if enough content was found
        if title and body and len(body) > 100:
            return {
                'url': url,
                'title': title,
                'author': author or 'Unknown',
                'body': body
            }
        
        return None
    
    def extract_links(self, url, html_content):
        """
        Extract links from HTML content.
        
        Args:
            url (str): URL of the page
            html_content (str): HTML content of the page
            
        Returns:
            list: List of extracted links
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href').strip()
            
            # Skip empty links and anchors
            if not href or href.startswith('#'):
                continue
            
            # Create absolute URL
            absolute_url = urljoin(url, href)
            
            # Check if URL is valid
            if self.is_valid_url(absolute_url) and absolute_url not in self.visited_urls:
                links.append(absolute_url)
        
        return links
    
    def fetch_url(self, url):
        """
        Fetch and process a URL.
        
        Args:
            url (str): URL to fetch
            
        Returns:
            tuple: (paper_info, new_links) if successful, (None, []) otherwise
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Only process text/html content
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type.lower():
                return None, []
            
            html_content = response.text
            paper_info = self.extract_paper_info(url, html_content)
            links = self.extract_links(url, html_content)
            
            return paper_info, links
            
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None, []
    
    def crawl(self):
        """
        Main crawling method.
        """
        logging.info(f"Starting crawl with {len(self.start_urls)} URLs")
        
        while self.queue and len(self.papers) < self.max_pages:
            # Get next batch of URLs to process
            batch_size = min(self.max_workers, len(self.queue))
            batch = [self.queue.pop(0) for _ in range(batch_size) if self.queue]
            
            # Mark URLs as visited
            self.visited_urls.update(batch)
            
            # Fetch URLs concurrently
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_url = {executor.submit(self.fetch_url, url): url for url in batch}
                
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    paper_info, new_links = future.result()
                    
                    # Add paper if found
                    if paper_info:
                        self.papers.append(paper_info)
                        logging.info(f"Found paper: {paper_info['title'][:40]}... ({len(self.papers)}/{self.max_pages})")
                    
                    # Add new links to queue
                    for link in new_links:
                        if link not in self.visited_urls and link not in self.queue:
                            self.queue.append(link)
            
            # Delay between batches
            time.sleep(self.delay)
        
        self.save_results()
    
    def format_as_cranfield(self):
        """
        Format the papers in Cranfield format.
        
        Returns:
            str: Papers formatted in Cranfield format
        """
        output = []
        
        for i, paper in enumerate(self.papers, start=1):
            output.append(f".I {i}")
            output.append(f".T")
            output.append(paper['title'])
            output.append(f".A")
            output.append(paper['author'])
            output.append(f".B")
            output.append(paper['url'])
            output.append(f".W")
            output.append(paper['body'])
            output.append("")
        
        return "\n".join(output)
    
    def create_sample_queries(self, num_queries=10):
        """
        Create sample queries from paper titles.
        
        Args:
            num_queries (int): Number of queries to create
            
        Returns:
            str: Queries formatted in Cranfield format
        """
        if not self.papers:
            return ""
        
        output = []
        max_queries = min(num_queries, len(self.papers))
        
        for i in range(1, max_queries + 1):
            paper = self.papers[i-1]
            # Create a query from the title
            query = paper['title'].strip()
            
            output.append(f".I {i:03d}")
            output.append(f".W")
            output.append(query)
        
        return "\n".join(output)
    
    def save_results(self):
        """
        Save the crawled papers and queries to files.
        """
        # Save papers in Cranfield format
        cran_path = os.path.join(self.output_dir, "cran.all.crawled")
        with open(cran_path, "w", encoding="utf-8") as f:
            f.write(self.format_as_cranfield())
        
        # Save sample queries
        query_path = os.path.join(self.output_dir, "cran.qry.crawled")
        with open(query_path, "w", encoding="utf-8") as f:
            f.write(self.create_sample_queries())
        
        # Save raw data as JSON for reference
        json_path = os.path.join(self.output_dir, "papers.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.papers, f, indent=2)
        
        logging.info(f"Saved {len(self.papers)} papers to {cran_path}")
        logging.info(f"Saved queries to {query_path}")
        logging.info(f"Saved raw data to {json_path}")


def main():
    """
    Main function to run the crawler.
    """
    parser = argparse.ArgumentParser(description="Academic web crawler")
    parser.add_argument("--urls", nargs="+", default=["https://arxiv.org/list/cs.IR/recent"], 
                      help="Starting URLs for crawling")
    parser.add_argument("--output", default="src/main/resources/crawled", 
                      help="Output directory")
    parser.add_argument("--max-pages", type=int, default=100, 
                      help="Maximum number of pages to crawl")
    parser.add_argument("--delay", type=float, default=1.0, 
                      help="Delay between requests in seconds")
    parser.add_argument("--workers", type=int, default=5, 
                      help="Number of concurrent workers")
    
    args = parser.parse_args()
    
    crawler = AcademicCrawler(
        start_urls=args.urls,
        output_dir=args.output,
        max_pages=args.max_pages,
        delay=args.delay,
        max_workers=args.workers
    )
    
    crawler.crawl()


if __name__ == "__main__":
    main() 