# -*- coding: utf-8 -*-

# Scrapy settings for crawlArtical project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import os
BOT_NAME = 'crawlArtical'

SPIDER_MODULES = ['crawlArtical.spiders']
NEWSPIDER_MODULE = 'crawlArtical.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlArtical (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY =False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
 "Cookies":'l_n_c=1; Domain=zhihu.com; Path=/;l_cap_id=; Domain=zhihu.com; expires=Wed, 17 Aug 2016 10:22:47 GMT; Path=/;z_c0="MS4xY2t5cUJRQUFBQUFYQUFBQVlRSlZUWGY3dkZsdWlFNFFkUlkwZkxRZ25ZejBPMUJwVmlyTWZRPT0=|1502965367|fcf257f7a83967cf4eeedfa1af723f94444e0192"; Domain=zhihu.com; expires=Sat, 16 Sep 2017 10:22:47 GMT; httponly; Path=/;n_c=; Domain=zhihu.com; expires=Wed, 17 Aug 2016 10:22:47 GMT; Path=/'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawlArtical.middlewares.CrawlarticalSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawlArtical.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawlArtical.pipelines.CrawlarticalPipeline': 300,
     # 'scrapy.pipelines.images.ImagesPipeline':1,
     #  'crawlArtical.pipelines.ArticalImagePipeline':1,
     #   "crawlArtical.pipelines.MysqlTwistedPipeline":2,
      "crawlArtical.pipelines.MysqlPipeline":2
}
IMAGES_URLS_FIELD="front_image_url"
project_dir=os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE=os.path.join(project_dir,"images")
# IMAGES_STORE='/Users/lijunlin/project/crawlArtical-scrapy/crawlArtical/crawlArtical/images'
print(IMAGES_STORE)
# IMAGE_MIN_HEIGNT
# IMAGE_MIN_WIDTH

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST="localhost"
MYSQL_DBNAME="crawl"
MYSQL_USER="root"
MYSQL_PASSWORD=""