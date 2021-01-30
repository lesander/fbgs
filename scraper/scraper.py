"""
    Selenium Facebook Scraper
    github.com/lesander
"""

import sys
import argparse
import gevent

from .exceptions import InvalidFacebookUrl, ExceptionLoadingDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .datatypes import FacebookPost, FacebookGroup, FacebookProfile
from .utils import save_json

class FacebookScraper:

    def __init__(self, **kwargs):
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.driver = self.load_driver()
        self.log_history = []
        self.wait_timeout = 5
    
    def parse_url(self, url):
        url = url.strip().replace('https://', '').replace('http://','')
        if not url.startswith('m.facebook.com'):
            raise InvalidFacebookUrl(url)
        return url

    def load_driver(self):
        driver = None
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
        except Exception as e:
            raise ExceptionLoadingDriver(f"Unable to load driver: {str(e)}")
        return driver
    
    def log(self, message):
        print(f"[*] {str(message)}")
        self.log_history.append(message)
    
    def navigate(self, url):
        self.log(f"Navigating to {url}")
        self.driver.get("https://" + url)
        
    def click(self, selector):
        self.driver.find_element_by_css_selector(selector).click()
        
    def fill(self, selector, text):
        self.driver.find_element_by_css_selector(selector).send_keys(text)
    
    def get_element(self, selector, element=None):
        if element is None:
            element = self.driver
        try:
            return element.find_element_by_css_selector(selector)
        except NoSuchElementException:
            return False
    
    def get_elements(self, selector, element=None):
        if element is None:
            element = self.driver
        return self.driver.find_elements_by_css_selector(selector)
    
    def get_text(self, selector):
        return self.driver.find_element_by_css_selector(selector).text
        
    def get_post_url(self, element):
        url = self.get_element("a[data-sigil=feed-ufi-trigger]", element)
        if url == False:
            # this could be a shared post
            url = self.get_element("a[data-sigil=share-popup]", element)
            
        if url != False:
            return url.get_attribute("href").split("?")[0]
        else:
            return url
        
    def parse_post(self, element):
        post = FacebookPost()
        post.url = self.get_post_url(element)
        post.timestamp = self.get_element("div[data-sigil=m-feed-voice-subtitle] > a > abbr", element).text
        
        post.text = element.text
        return post
        
    def scroll(self, amount):
        self.driver.execute_script(f"return window.scrollBy(0, {str(amount)})")
        
    #def scroll_to(self, element):
    #    self.driver.execute_script(f"return ")
        
    def wait_after_submit(self):
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(EC.url_changes(self.driver.current_url))
        except TimeoutException:
            pass
            
    def wait_for_element_to_hide(self, selector):
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Exception while waiting: {str(e)}")
            pass
            
    def wait_for_new_posts(self, old_num_posts, selector):
        self.log("Waiting for new posts to have loaded..")
        while True:
            current_num_posts = len(self.get_elements(selector))
            if current_num_posts != old_num_posts:
                self.log("New posts found!")
                break
            gevent.sleep(.5)
    
    def login(self):
        self.navigate("m.facebook.com")
        self.click("a[data-cookiebanner=accept_button]")
        self.fill("input[name=email]", self.username)
        self.fill("input[type=password]", self.password)
        self.click("button[name=login]")
        self.wait_after_submit()
        
        if '/login/save-device' in self.driver.current_url:
            self.click("button[type=submit][value=OK]")
            self.wait_after_submit()
            
        if '/gdpr/consent' in self.driver.current_url:
            self.click("button[type=submit]:last-of-type")
            self.wait_after_submit()
        
        if self.driver.title != 'Facebook':
            self.log("We'd expect to have landed on the homepage by now..")
        else:
            self.log("Login finished.")
    
    def scrape_group(self, url, out=False, max=sys.maxsize):
        url = self.parse_url(url)
        self.navigate(url)
        
        if 'facebook.com/groups' not in self.driver.current_url:
            self.log("Are you sure the provided url is a group?")
        else:
            self.log("Starting scrape of given Facebook Group..")
        
        group = FacebookGroup(url=url)
        group.name = self.get_text("div#MBackNavBar")
        group.posts = []
        post_offset = 0
        
        while True:
            self.log(f"Parsing posts of {group.name}..")
            all_post_elements = self.get_elements("article.async_like")
            post_elements = all_post_elements[post_offset:] # remove previous posts from results
            post_offset = len(all_post_elements)
            if len(post_elements) == 0:
                self.log("No more post elements")
                break
            for post_element in post_elements:
                post = self.parse_post(post_element)
                self.log(f"Parsed post {post.url}")
                group.posts.append(post)
                self.scroll(post_element.size['height'])
            if out != False:
                save_json(out, group)
            if len(group.posts) >= max:
                self.log(f"Reached maximum of posts ({str(max)})")
                break
            
            self.log(f"Finished parsing, we now have parsed {str(len(group.posts))} posts.")
            
            self.scroll(1000)
            self.wait_for_new_posts(len(all_post_elements), "article.async_like")
            # self.wait_for_element_to_hide("div[data-sigil=m-loading-indicator-root]")
            # gevent.sleep(1)
            
        return group
    
    def interactive(self):
        self.log("Starting interactive prompt\n    Access selenium with 'self.driver'\n    Type 'exit' to quit..")
        while True:
            command = input("> ")
            if command == "exit":
                self.driver.close()
                break
            try:
                print(eval(command))
            except Exception as e:
                print(f"Exception: {str(e)}")


