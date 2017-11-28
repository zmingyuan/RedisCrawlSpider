from scrapy import cmdline
import os

os.chdir('fiftyonejob/spiders')
cmdline.execute('scrapy crawl fifty'.split())
