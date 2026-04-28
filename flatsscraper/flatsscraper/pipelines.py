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


'''
from scrapy.http import Request, Response
from scrapy.pipelines.media import FileInfo, FileInfoOrError, MediaPipeline
from typing import Any #IO, TYPE_CHECKING, Any

from scrapy.pipelines.images import ImagesPipeline

class CustomImagesPipeline(ImagesPipeline): #ctrl click on IMagesPipeline
    def file_path(
        self,
        request: Request,
        response: Response | None = None,
        info: MediaPipeline.SpiderInfo | None = None,
        *,
        item: Any = None,
    ) -> str:
        return request.url.split('/')[-1] #file name
'''
from urllib.parse import urlparse
import scrapy, re
from scrapy.pipelines.images import ImagesPipeline

class FlatsDirectoryImagesPipeline(ImagesPipeline):


    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        # Grab the original image file name
        image_filename = request.url.split('/')[-1]
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        # Check if we have a title
        if item and 'title' in item and item['title']:
            raw_title = item['title']

            # SANITIZE THE TITLE!
            # This regex replaces anything that isn't a letter, number, or dash with an underscore
            safe_title = re.sub(r'[^\w\-]', '_', raw_title)

            # Remove any trailing or multiple underscores to make it look neat
            safe_title = re.sub(r'_+', '_', safe_title).strip('_')

            folder_name = safe_title if safe_title else "unknown_book"
        else:
            folder_name = "unknown_book"

        # Combine the safe folder name and the image name
        #return f"{folder_name}/{image_guid[:2]}/{image_guid}.jpg"
        return f"{folder_name}/{image_guid}.jpg"