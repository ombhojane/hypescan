from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Dict, List, Optional, Union
from pydantic import BaseModel
import logging
import time
from datetime import datetime
import urllib.parse
from enum import Enum
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchType(str, Enum):
    """Available search types for Twitter search"""
    LATEST = "live"
    TOP = "top"
    PEOPLE = "people"
    PHOTOS = "image"
    VIDEOS = "video"

class TweetUser(BaseModel):
    name: str
    screen_name: str

class Tweet(BaseModel):
    text: str
    created_at: str
    reply_count: str
    retweet_count: str
    favorite_count: str
    user: TweetUser
    _scrape_timestamp: str

class TwitterSearchResponse(BaseModel):
    tweets: List[Tweet]
    status: str = "success"
    error: Optional[str] = None

class TwitterScraper:
    def __init__(self, headless: bool = True):
        """Initialize the Twitter scraper with Chrome profile support."""
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('--headless=new')
        
        # Set up Chrome profile and cookies directory
        self.user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

        # Use existing Chrome profile
        self.options.add_argument(f'--user-data-dir={self.user_data_dir}')
        self.options.add_argument('--profile-directory=Default')
        
        # Essential options
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('--disable-popup-blocking')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument("--start-maximized")
        
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=self.options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            self.cleanup()
            raise

    def cleanup(self):
        """Clean up resources."""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except:
            pass

    def login(self, username: str, password: str) -> bool:
        """Login to Twitter."""
        try:
            if not password:
                logger.error("Password is required for login")
                return False

            self.driver.get("https://twitter.com/login")
            time.sleep(3)

            username_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            username_input.send_keys(username)
            
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            next_button.click()
            time.sleep(2)

            password_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
            )
            password_input.send_keys(password)

            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
            )
            login_button.click()
            time.sleep(5)

            return "login" not in self.driver.current_url.lower()

        except Exception as e:
            logger.error(f"Failed to login: {str(e)}")
            return False

    def _extract_tweet_data(self, tweet_element) -> Optional[Dict]:
        """Extract tweet data from a tweet element."""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of(tweet_element)
            )
            
            try:
                text_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                text = text_element.text
            except:
                text_element = tweet_element.find_element(By.CSS_SELECTOR, 'div[lang]')
                text = text_element.text

            stats = tweet_element.find_elements(By.CSS_SELECTOR, '[role="group"] [data-testid$="-count"]')
            reply_count = stats[0].text if len(stats) > 0 else "0"
            retweet_count = stats[1].text if len(stats) > 1 else "0"
            like_count = stats[2].text if len(stats) > 2 else "0"

            try:
                user_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]')
                user_texts = user_element.text.split('\n')
                user_name = user_texts[0]
                user_handle = user_texts[1].replace('@', '') if len(user_texts) > 1 else ""
            except:
                user_name = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"] span').text
                user_handle = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"] div span').text.replace('@', '')

            try:
                time_element = tweet_element.find_element(By.TAG_NAME, 'time')
                timestamp = time_element.get_attribute('datetime')
            except:
                timestamp = ""

            if text and (user_name or user_handle):
                return {
                    'text': text,
                    'created_at': timestamp,
                    'reply_count': reply_count,
                    'retweet_count': retweet_count,
                    'favorite_count': like_count,
                    'user': {
                        'name': user_name,
                        'screen_name': user_handle
                    },
                    '_scrape_timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error extracting tweet data: {str(e)}")
        return None

    def search_tweets(
        self, 
        query: str, 
        search_type: SearchType = SearchType.TOP,
        max_tweets: int = 20,
        username: str = None,
        password: str = None
    ) -> TwitterSearchResponse:
        """Search tweets based on query."""
        try:
            if username and password:
                login_success = self.login(username, password)
                if not login_success:
                    return TwitterSearchResponse(tweets=[], status="error", error="Login failed")

            encoded_query = urllib.parse.quote(query)
            search_url = f"https://twitter.com/search?q={encoded_query}&f={search_type}"
            
            logger.info(f"Searching tweets with query: {query}")
            self.driver.get(search_url)
            time.sleep(3)
            
            if "login" in self.driver.current_url.lower():
                return TwitterSearchResponse(tweets=[], status="error", error="Not logged in to Twitter")
            
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
            except TimeoutException:
                return TwitterSearchResponse(tweets=[], status="error", error="Timeout waiting for tweets")
            
            tweets = []
            last_height = 0
            retry_count = 0
            
            while len(tweets) < max_tweets and retry_count < 5:
                tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
                
                if not tweet_elements:
                    retry_count += 1
                    time.sleep(2)
                    continue
                
                for tweet_element in tweet_elements:
                    if len(tweets) >= max_tweets:
                        break
                        
                    tweet_data = self._extract_tweet_data(tweet_element)
                    if tweet_data and not any(
                        t['text'] == tweet_data['text'] and 
                        t['user']['screen_name'] == tweet_data['user']['screen_name'] 
                        for t in tweets
                    ):
                        tweets.append(tweet_data)
                
                if len(tweets) >= max_tweets:
                    break
                
                self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                
                new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
                if new_height == last_height:
                    retry_count += 1
                else:
                    retry_count = 0
                    
                last_height = new_height
            
            return TwitterSearchResponse(tweets=tweets[:max_tweets])

        except Exception as e:
            logger.error(f"Failed to search tweets: {str(e)}")
            return TwitterSearchResponse(tweets=[], status="error", error=str(e))
            
        finally:
            self.cleanup()

async def search_twitter(
    query: str,
    search_type: Union[SearchType, str] = SearchType.TOP,
    max_tweets: int = 20,
    username: str = None,
    password: str = None
) -> TwitterSearchResponse:
    """Async wrapper for Twitter search functionality."""
    if isinstance(search_type, str):
        try:
            search_type = SearchType[search_type.upper()]
        except KeyError:
            logger.warning(f"Invalid search type: {search_type}. Using TOP.")
            search_type = SearchType.TOP
    
    scraper = TwitterScraper(headless=True)
    return scraper.search_tweets(query, search_type, max_tweets, username, password) 