import html
from functools import wraps

from bs4 import BeautifulSoup
import json

from tqdm import tqdm

from app import app
from models import db, Site, Brand, ProductCategory, ProductType, Product

def with_app_context(func):
    """Decorator to run function with app context"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper


def out_html_from_raw(raw_html):
    """Output html from raw html"""
    normal_html = html.unescape(raw_html).replace('\\', '')
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(normal_html)

def get_soup_html_from_raw(raw_html):
    """Get soup html from raw html"""
    normal_html = html.unescape(raw_html).replace('\\', '')
    return BeautifulSoup(normal_html, 'html.parser')

def read_json_lines(file_path):
    """Generator to read JSON lines from a file"""
    with open(file_path) as file:
        for line in file:
            yield json.loads(line)


def total_lines(file_path):
    """Get total lines from a file"""
    with open(file_path) as file:
        return sum(1 for _ in file)


def extract_products_information(
    file_path,
    get_product_lists_func,
    get_product_details_func,
):
    product_info_from_listing_page_type = list(dict())
    product_info_from_detail_page_type = list(dict())

    # Create a progress bar for reading data
    progress_bar_for_reading_data = tqdm(total=total_lines(file_path), desc="Reading data from file")
    for json_obj in read_json_lines(file_path):

        progress_bar_for_reading_data.update(1)  # Update the progress bar

        raw_html = json_obj['body']
        if json_obj['page_type'] == 'product_listing':
            product_lists = get_product_lists_func(raw_html)
            for product in product_lists:
                product_info_from_listing_page_type.append({
                    'name': product,
                    'page_url': json_obj['page_url'],
                    'page_number': json_obj['page_number'],
                    'product_category': json_obj['product_category'][0],
                    'product_type': json_obj['product_category'][1] if len(json_obj['product_category']) > 1 else None
                })
        elif json_obj['page_type'] == 'product_detail':
            product_info_from_detail_page_type.append(get_product_details_func(raw_html))
        else:
            raise Exception('Unknown page type')

    return [
        {**listing,
         **next((detail for detail in product_info_from_detail_page_type if detail['name'] == listing['name']), {})}
        for listing in product_info_from_listing_page_type
    ]


@with_app_context
def save_product_info_to_database(product_info, site: Site, progress_bar_info):
    """Save product information to database with progress bar"""

    # Create or update Brand
    product_name = product_info['name'].upper()
    brand_name = product_info['brand'].upper() if "brand" in product_info.keys() else "UNKNOWN"
    product_category_name = product_info['product_category'].upper()

    # Create or update Brand
    brand = Brand.query.filter_by(name=brand_name).first()
    if not brand:
        brand = Brand(name=brand_name)
        db.session.add(brand)
        db.session.commit()
        progress_bar_info.set_postfix_str(f"Created Brand: {brand_name} ")

    # Create or update ProductCategory
    category = ProductCategory.query.filter_by(name=product_category_name).first()
    if not category:
        category = ProductCategory(name=product_category_name)
        db.session.add(category)
        db.session.commit()
        progress_bar_info.set_postfix_str(f"Created ProductCategory: {product_category_name}")

    # Create or update ProductType (if applicable)
    product_type_name = product_info['product_type'].upper() if product_info['product_type'] else None
    product_type = ProductType.query.filter_by(name=product_type_name).first()
    if not product_type and product_type_name:
        product_type = ProductType(name=product_type_name)
        db.session.add(product_type)
        db.session.commit()
        progress_bar_info.set_postfix_str(f"Created ProductType: {product_type_name} ")

    # Create or update Product
    product = Product.query.filter_by(name=product_name).first()
    if not product:
        product = Product(
            name=product_name,
            price=float(product_info['price']) if "price" in product_info.keys() else None,
            page_number=product_info['page_number'],
            site_id=site.id,
            brand_id=brand.id,
            product_category_id=category.id,
            product_type_id=product_type.id if product_type else None
        )
        db.session.add(product)
        db.session.commit()
        progress_bar_info.set_postfix_str(f"Created Product: {product_name}")
