import html
import json
from models import db, Site, Brand, ProductCategory, ProductType, Product

from bs4 import BeautifulSoup


def out_html_from_raw(raw_html):
    """Output html from raw html"""
    normal_html = html.unescape(raw_html).replace('\\', '')
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(normal_html)


def get_product_lists_form_omoda_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    product_lists = soup.find_all('a', class_='artikel-link googleproduct')
    return list({product["title"] for product in product_lists})


def get_soup_html_from_raw(raw_html):
    """Get soup html from raw html"""
    normal_html = html.unescape(raw_html).replace('\\', '')
    return BeautifulSoup(normal_html, 'html.parser')


def get_product_lists_form_ziengs_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    product_lists = soup.select('.productList .title')
    return list({product["title"] for product in product_lists})


def get_product_details_form_ziengs_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    return {
        'name': soup.find('h1', {'itemprop': 'name'}).text.strip(),
        'brand': soup.find('meta', {'itemprop': 'brand'})['content'],
        'price': soup.find('meta', {'itemprop': 'price'})['content']
    }


def grab_and_save_data_from_ziengs_site(file_name):
    """Grab data from ziengs site"""

    site = Site.query.filter_by(name='ZIENGS').first()
    if not site:
        site = Site(name='ZIENGS', url='https://zeigns.nl')
        db.session.add(site)
        db.session.commit()

    product_info_from_listing_page_type = list(dict())
    product_info_from_detail_page_type = list(dict())
    with open(file_name) as file:
        for line in file:
            json_obj = json.loads(line)
            raw_html = json_obj['body']
            if json_obj['page_type'] == 'product_listing':
                product_lists = get_product_lists_form_ziengs_site(raw_html)
                for product in product_lists:
                    product_info_from_listing_page_type.append({
                        'name': product,
                        'page_url': json_obj['page_url'],
                        'page_number': json_obj['page_number'],
                        'product_category': json_obj['product_category'][0],
                        'product_type': json_obj['product_category'][1:] if len(json_obj['product_category']) > 1 else None
                    })
            elif json_obj['page_type'] == 'product_detail':
                product_info_from_detail_page_type.append(get_product_details_form_ziengs_site(raw_html))
            else:
                raise Exception('Unknown page type')

    all_products_info = [
        {**listing,
         **next((detail for detail in product_info_from_detail_page_type if detail['name'] == listing['name']), {})}
        for listing in product_info_from_listing_page_type
    ]

    for product_info in all_products_info:
        add_product_info_to_db(product_info, site=site)


def add_product_info_to_db(product_info, site: Site):
    # Create or update Brand
    brand = Brand.query.filter_by(name=product_info['brand']).first()
    if not brand:
        brand = Brand(name=product_info['brand'])
        db.session.add(brand)
        db.session.commit()

    # Create or update ProductCategory
    category = ProductCategory.query.filter_by(name=product_info['product_category']).first()
    if not category:
        category = ProductCategory(name=product_info['product_category'])
        db.session.add(category)
        db.session.commit()

    # Create or update ProductType (if applicable)
    product_type_name = product_info['product_type']
    if product_type_name:
        product_type = ProductType.query.filter_by(name=product_type_name).first()
        if not product_type:
            product_type = ProductType(name=product_type_name)
            db.session.add(product_type)
            db.session.commit()
    else:
        product_type = None

    # Create or update Product
    product = Product.query.filter_by(name=product_info['name']).first()
    if not product:
        product = Product(
            name=product_info['name'],
            price=float(product_info['price']),
            page_number=product_info['page_number'],
            site_id=site.id,
            brand_id=brand.id,
            product_category_id=category.id,
            product_type_id=product_type.id if product_type else None
        )
        db.session.add(product)
        db.session.commit()

    # Commit all changes to the database
    db.session.commit()


# input_file = 'raw.jl'
#
# with open(input_file, 'r', encoding='utf-8') as file:
#     raw_html = file.read()
#
# out_html_from_raw(raw_html)

# print(get_product_lists_form_ziengs_site(raw_html))
# print(get_product_lists_form_omoda_site(raw_html))
grab_and_save_data_from_ziengs_site("/Users/jyothi/Desktop/jyothi/N/20160530_nelson_mini_project_crawls/crawl_ziengs.nl_2016-05-30T23-15-20.jl")


