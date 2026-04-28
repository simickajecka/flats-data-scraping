import scrapy
import re
from flatsscraper.items import FlatsscraperItem

class FlatspiderSpider(scrapy.Spider):

    name = 'flatspider'
    allowed_domains = ['www.nekretnine.rs', 'img.nekretnine.rs']
    start_urls = ['https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/lista/po-stranici/']


    def parse(self, response):
        flats = response.css('.row.offer')
        for flat in flats:
            relative_url = flat.css('h2 a').attrib['href']
            flat_url = 'https://www.nekretnine.rs' + relative_url
            yield response.follow(flat_url, callback=self.parse_flat_page)


        next_page = response.css('.next-article-button::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.nekretnine.rs' + next_page
            yield response.follow(next_page_url, callback=self.parse)


    def parse_flat_page(self, response):
        title = response.css('h1::text').get().strip()
        prices = self.get_prices(response)
        area = re.findall(r'\d+', response.css('.stickyBox__size::text').get())[0] #without m2
        dataflat = self.flat_detalis_info(response)
        description = self.get_description(response)
        coordinates = self.get_coordinates(response)


        flat_item = FlatsscraperItem()
        self.get_carousel(response, flat_item)

        flat_item['title'] = title
        flat_item['prices'] = prices
        flat_item['area'] = area
        flat_item['dataflat'] = dataflat
        flat_item['coordinates'] = coordinates
        flat_item["page_url"] = response.url
        print('-------------------------------------------')
        flat_item["description"] = description
        print(flat_item['description'])
        print("------------------------------------------------")
        yield flat_item
        '''
        yield {
            #'url': response.url,
            'title': title,
            'prices': prices,
            'area': area,
            'details': data,
            'coordinates': coordinates,
            'carousel': carousel
            #'description': description,
            #'image_urls': list(set(img_urls)) #key has to be image_urls
            #'img urls': carousel_just_links
            }
        '''

    def flat_detalis_info(self, response):
        sections = response.css('.property__amenities')
        data = {}
        for section in sections:
            section_title = section.css("h3::text").get()

            items = section.css("ul li")

            # Case 1: key-value pairs (first section)
            if items.css("strong"):
                section_data = {}

                for item in items:
                    #key = item.xpath("normalize-space(text()[1])").get()
                    key = item.css('::text').get().strip()
                    value = item.css("strong::text").get()

                    if key:
                        key = key.replace(":", "").strip()
                    if value:
                        value = value.strip()

                    section_data[key] = value

                data[section_title] = section_data

            else:
                section_data = []
                '''
                for item in items:
                    text = item.css("::text").get().strip()
                    #if text:
                    section_data.append(text)

                data[section_title] = section_data
                '''
                for item in items:
                    text = ' '.join(item.css("::text").get().strip().split())
                    if text:  # Make sure the text isn't empty
                        section_data.append(text)
                data[section_title] = section_data

        return data

    def get_description(self, response):
        paragraphs = response.css('.cms-content-inner::text').getall()
        cleaned = [
            p.replace('\xa0', ' ').strip()
            for p in paragraphs
                if p.strip()
        ]

        return "\n".join(cleaned)


    def get_carousel(self, response, item):

        relative_urls = response.css('.advert-picture img::attr(src)').getall()
        item['image_urls'] = [response.urljoin(url) for url in relative_urls]


    def get_prices(self, response):
        full_price_currency = response.css('h4::text').get()
        (price, currency) = separate_digits_letters(full_price_currency)

        per_m2 = response.css('h4 span::text').get()
        (price_m2, curr_m2) = separate_digits_letters(per_m2)

        #yield((price, currency), (price_m2, curr_m2))
        return {
            'price': price,
            'currency': currency,
            'price_per_m2': price_m2,
            'm2': curr_m2
        }

    def get_img_links(selfe, response):
        urls = response.css('.swiper-zoom-container::attr(src)').getall()
        img_urls = []
        for url in urls:
            img_urls.append(url)

        return img_urls

    def get_coordinates(self, response):
        latitude = response.css('script::text').re_first(r'ppLat\s=\s([0-9.]+)')
        longitude = response.css('script::text').re_first(r'ppLng\s=\s([0-9.]+)')
        return (latitude, longitude)
        #sorce =  response.css('id = div.ppMap::text').get()

def separate_digits_letters(full_price_currency):
    price = ''.join(re.findall(r'\d+', full_price_currency))
    currency = ''.join(re.findall(r'[a-zA-Z]+', full_price_currency)).strip()
    return (price, currency)
