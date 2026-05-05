# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import hashlib

from itemadapter import ItemAdapter


class FlatsscraperPipeline:
    def process_item(self, item, spider):
        return item

import scrapy
from scrapy.pipelines.images import ImagesPipeline
import hashlib, re
from scrapy.pipelines.media import FileInfo

class FlatsDirectoryImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # Only request images if 'image_urls' exists
        for image_url in item.get('image_urls', []):
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, item=None):
        image_filename = request.url.split('/')[-1]
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()

        # Safe folder name based on title
        if item and 'title' in item and item['title']:
            raw_title = item['title']
            safe_title = re.sub(r'[^\w\-]', '_', raw_title)
            safe_title = re.sub(r'_+', '_', safe_title).strip('_')
            folder_name = safe_title if safe_title else "unknown_flat"
        else:
            folder_name = "unknown_flat"

        return f"{folder_name}/{image_guid}.jpg"
    '''
    def item_completed(self, results, item, info):
        # Images are downloaded, but we remove all image-related fields from the item
        if 'image_urls' in item:
            del item['image_urls']
        if 'images' in item:
            del item['images']
        if 'page_url' in item:
            del item['page_url']
        return item
    '''
    '''
    def item_completed(self, results, item, info):
        # Don't drop item if images fail — just store what worked
        item['images'] = [r for ok, r in results if ok]
        # Remove image_urls so feed exporter doesn't choke on it
        item.pop('image_urls', None)
        return item  # ← always return the item, never raise DropItem
    '''