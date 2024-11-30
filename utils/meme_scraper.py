import requests
from bs4 import BeautifulSoup
import random

class MemeScraper:
    def __init__(self):
        self.meme_sources = [
            'https://www.reddit.com/r/memes/top/',
            'https://imgur.com/r/memes',
            'https://9gag.com/memes'
        ]
        
        # Headers to mimic browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_reddit_memes(self):
        """
        Scrape memes from Reddit
        
        Returns:
            list: Dictionary of meme details
        """
        try:
            response = requests.get(self.meme_sources[0], headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            memes = []
            for post in soup.find_all('div', class_='Post'):
                try:
                    img = post.find('img', class_='ImageBox-image')
                    title = post.find('h3', class_='_eYtD2XCVieq6emjKBH3m')
                    
                    if img and title:
                        meme = {
                            'source': 'Reddit',
                            'image_url': img.get('src'),
                            'title': title.text,
                            'upvotes': self._extract_upvotes(post)
                        }
                        memes.append(meme)
                except Exception as e:
                    print(f"Error processing Reddit meme: {e}")
            
            return memes
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            return []

    def scrape_imgur_memes(self):
        """
        Scrape memes from Imgur
        
        Returns:
            list: Dictionary of meme details
        """
        try:
            response = requests.get(self.meme_sources[1], headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            memes = []
            for post in soup.find_all('div', class_='post-image-container'):
                try:
                    img = post.find('img')
                    if img:
                        meme = {
                            'source': 'Imgur',
                            'image_url': img.get('src'),
                            'title': img.get('alt', 'No Title')
                        }
                        memes.append(meme)
                except Exception as e:
                    print(f"Error processing Imgur meme: {e}")
            
            return memes
        except Exception as e:
            print(f"Error scraping Imgur: {e}")
            return []

    def _extract_upvotes(self, post):
        """
        Extract upvotes from a Reddit post
        
        Args:
            post (BeautifulSoup): Post element
        
        Returns:
            int: Number of upvotes
        """
        try:
            upvote_elem = post.find('div', class_='_1rZYMD_4xY3gRcNHqg6bTQ')
            return int(upvote_elem.text) if upvote_elem else 0
        except:
            return 0

    def search_memes(self, query, text_processor):
        """
        Search memes based on processed query
        
        Args:
            query (str): Search query
            text_processor (TextProcessor): Text processing instance
        
        Returns:
            list: Filtered and ranked memes
        """
        # Process the query
        processed_query = text_processor.process_query(query)
        
        # Collect memes from different sources
        all_memes = (
            self.scrape_reddit_memes() + 
            self.scrape_imgur_memes()
        )
        
        # Filter and rank memes
        matched_memes = []
        for meme in all_memes:
            # Process meme title
            processed_title = text_processor.process_query(meme.get('title', ''))
            
            # Simple matching: check if any query tokens are in title tokens
            if any(token in processed_title for token in processed_query):
                matched_memes.append(meme)
        
        # Shuffle to provide variety
        random.shuffle(matched_memes)
        
        return matched_memes[:20]  # Limit to 20 results