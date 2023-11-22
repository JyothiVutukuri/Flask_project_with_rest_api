import html
import re
from functools import wraps
from typing import List

from bs4 import BeautifulSoup
import json

from sqlalchemy import exc
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


def replace_apostrophes_with_space(html_content):
    # Replace occurrences of a letter followed by a single quote with the letter followed by a space
    modified_html = re.sub(r"([a-zA-Z0-9])'([a-zA-Z0-9])", r"\1 ", html_content)
    return modified_html


def output_html_from_raw(raw_html):
    """Output html from raw html fot check"""
    normal_html = html.unescape(raw_html).replace('\\', '').replace("Mini's", "Minis").replace("d'Oro", "d Oro").replace("'INCH", "INCH").replace("Don't", "Dont").replace("d'Angelo", "d Angelo").replace("W'S", "WS")
    corrected_html = replace_apostrophes_with_space(normal_html)
    with open('check_output.html', 'w', encoding='utf-8') as file:
        file.write(corrected_html)


def get_soup_html_from_raw(raw_html):
    """Get soup html from raw html"""
    normal_html = html.unescape(raw_html).replace('\\', '')
    corrected_html = replace_apostrophes_with_space(normal_html)
    return BeautifulSoup(corrected_html, 'html.parser')

# def read_json_lines(file_path):
#     """Generator to read JSON lines from a file"""
#     with open(file_path) as file:
#         for line in file:
#             yield json.loads(line)


def total_lines(file_path):
    """Get total lines from a file"""
    with open(file_path) as file:
        return sum(1 for _ in file)


def read_json_lines(file_path, start_line, chunk_size):
    """Read a chunk of JSON lines from a file"""
    with open(file_path) as file:
        # Skip to the starting line
        for _ in range(start_line):
            next(file)
        # Read the chunk of lines
        for _ in range(chunk_size):
            try:
                yield json.loads(next(file))
            except StopIteration:
                break


def extract_products_information(
    file_path,
    get_product_lists_func,
    get_product_details_func,
    chunk_size=1000
):
    total_lines_count = total_lines(file_path)
    progress_bar_for_reading_data = tqdm(total=total_lines_count, desc="Reading data from file")

    product_info_from_listing_page_type = list(dict())
    product_info_from_detail_page_type = list(dict())

    start_line = 0
    while start_line < total_lines_count:
        end_line = min(start_line + chunk_size, total_lines_count)
        progress_bar_for_reading_data.set_postfix_str(f"Chunk from {start_line} to {end_line}")

        for json_obj in read_json_lines(file_path, start_line, end_line - start_line):
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
                product_info = get_product_details_func(raw_html)
                product_info_from_detail_page_type.append(product_info) if product_info else None
            else:
                raise Exception('Unknown page type')

        start_line = end_line

    # Create a dictionary with 'id' as the key for each list
    dict1 = {item['name']: item for item in product_info_from_listing_page_type}
    dict2 = {item['name']: item for item in product_info_from_detail_page_type}

    # Merge dictionaries based on the common field 'id'
    all_product_info = [
        {**dict1[key], **dict2[key]}
        for key in set(dict1.keys()) & set(dict2.keys())
    ]

    return all_product_info


@with_app_context
def save_product_info_to_database(product_info, site: Site):
    """Save product information to the database with progress bar"""

    product_name = product_info.get('name')
    brand_name = product_info.get('brand', 'UNKNOWN')
    product_category_name = product_info.get('product_category')
    product_type_name = product_info.get('product_type', '').upper() if product_info.get('product_type') else None

    brand = Brand.get_or_create(brand_name)
    category = ProductCategory.get_or_create(product_category_name)
    product_type = ProductType.get_or_create(product_type_name) if product_type_name else None

    try:
        Product.get_or_create(
            name=product_name,
            price=float(product_info.get('price')),
            page_number=product_info.get('page_number'),
            site_id=site.id,
            brand_id=brand.id,
            product_category_id=category.id,
            product_type_id=product_type.id if product_type else None
        )

    except exc.IntegrityError:
        db.session.rollback()

