import requests
import logging
import bs4
import csv
import collections
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'sale_price',
        'price',
        'brand_name',
        'goods_name',
        'url',
    ),
)

HEADERS = (
    'Скидка',
    'Цена',
    'Бренд',
    'Товар',
    'Ссылка',
)


class Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Accept-Language': 'ru',
        }
        self.result = []
        self.brand_name = []
        self.params = self.create_params()

    def load_page(self, brand_key='', size_key=''):
        url = f'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/podguzniki/podguzniki-detskie{brand_key}{size_key}'
        print(url)
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.dtList.i-dtList.j-card-item')
        for block in container:
            self.parse_block(block=block)

    def create_params(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--min_price', default=1000, type=int)
        parser.add_argument('--active_min_price', action='store_false', default=False,
                            help='Булевое значение True или False')
        return parser

    def parse_block(self, block):
        url_block = block.select_one('a.ref_goods_n_p')
        if not url_block:
            logger.error('no urlblock')
            return

        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return

        name_block = block.select_one('div.dtlist-inner-brand-name')
        if not name_block:
            logger.error(f'no name-block on {url}')

        brand_name = block.select_one('strong.brand-name')
        if not name_block:
            logger.error(f'no brand-name on {url}')

        brand_name = brand_name.text
        brand_name = brand_name.replace('/', '').strip()

        if brand_name not in self.brand_name:
            self.brand_name.append(brand_name)

        goods_name = block.select_one('span.goods-name')
        if not goods_name:
            logger.error(f'no goods-name on {url}')

        goods_name = goods_name.text.strip()

        sale_price = block.select_one('ins.lower-price')
        if not sale_price:
            sale_price = block.select_one('span.lower-price')
            if not sale_price:
                logger.error(f'no sale_price on {url}')

        if sale_price == None:
            sale_price = 0
        else:
            sale_price = sale_price.text.replace('&nbsp;', '').strip()
            sale_price = int(sale_price.replace("\xa0", '').replace('₽', ''))

        args_sale_price = sale_price

        price = block.select_one('span.price-old-block del')
        if not price:
            price = block.select_one('span.lower-price')
            if not price:
                logger.error(f'no price on {url}')

        if price == None:
            price = 0
        else:
            price = price.text.replace('&nbsp;', '').strip()

        logger.debug('%s, %s, %s, %s, %s', url, brand_name, goods_name, sale_price, price)
        logger.debug('=' * 100)

        args = self.params.parse_args()
        if args.active_min_price:
            if int(args_sale_price) <= args.min_price:
                self.result.append(ParseResult(
                    sale_price=sale_price,
                    price=price,
                    url=url,
                    brand_name=brand_name,
                    goods_name=goods_name,
                ))

        else:
            self.result.append(ParseResult(
                sale_price=sale_price,
                price=price,
                url=url,
                brand_name=brand_name,
                goods_name=goods_name,
            ))

    def save_results(self):
        path = 'test.csv'
        sortedlist = sorted(self.result, key=lambda x: int(x[0]))
        with open(path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in sortedlist:
                writer.writerow(item)

    def run(self, brand_key='', size_key=''):
        text = self.load_page(brand_key, size_key)
        self.parse_page(text=text)
        logger.info(f'Получено: {len(self.result)}')
        self.save_results()


if __name__ == '__main__':
    parser = Client()
    parser.run()
