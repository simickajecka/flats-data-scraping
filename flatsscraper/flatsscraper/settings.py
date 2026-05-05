# Scrapy settings for flatsscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "flatsscraper"

SPIDER_MODULES = ["flatsscraper.spiders"]
NEWSPIDER_MODULE = "flatsscraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "flatsscraper (+http://www.yourdomain.com)"

#import os
#os.makedirs("dataset", exist_ok=True)  # da bih mogla da zovem -o output.json i da imam dataset folder

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": ["--disable-blink-features=AutomationControlled"],
}
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "sr-RS,sr;q=0.9,en;q=0.8",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"


PLAYWRIGHT_CONTEXTS = {
    "default": {
        "user_data_dir": "C:/RGZ/webStanovi/browser_profile",
    }
}

PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

'''
PLAYWRIGHT_ABORT_REQUEST = lambda req: req.resource_type in ("image", "font", "ping") or any(
    domain in req.url for domain in ["google-analytics", "facebook", "hotjar", "doubleclick", "adocean"]
)
'''
PLAYWRIGHT_ABORT_REQUEST = lambda req: any(
    domain in req.url for domain in ["google-analytics", "facebook", "hotjar", "doubleclick", "adocean"]
)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
#ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "flatsscraper.middlewares.FlatsscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "flatsscraper.middlewares.FlatsscraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html


ITEM_PIPELINES = {
    'flatsscraper.pipelines.FlatsDirectoryImagesPipeline':1
}

#ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}  #ovo je defoult zato i koristimo image_urls
#pip install pillow
IMAGES_STORE = 'carousels'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value

FEED_EXPORT_ENCODING = "utf-8"

#creating dataset/ folder:

FEEDS = {
    "dataset/data.json": {
        "format": "json",
        "encoding": "utf8",
        "indent": 2,
    }
}
