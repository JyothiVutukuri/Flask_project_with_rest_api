import argparse
import json
import re

from tqdm import tqdm
from utils import get_soup_html_from_raw, extract_products_information, save_product_info_to_database, with_app_context
from models import db, Site


@with_app_context
def add_zalando_site():
    site_name = 'zalando'
    site = Site.query.filter_by(name=site_name.upper()).first()
    if not site:
        site = Site(name=site_name, url='https://zalando.nl')
        db.session.add(site)
        db.session.commit()
    return site


def get_product_lists_from_zalando_site(raw_html):
    """
    Get product lists from raw html
    """
    soup = get_soup_html_from_raw(raw_html)
    product_lists = soup.find_all("div", class_="catalogArticlesList_articleName")
    return list({product.get_text(strip=True) for product in product_lists})


def get_product_details_from_zalando_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)

    script_tag = soup.find("script", string=re.compile(r'dataLayer\.push\({.*}\);', re.DOTALL))

    # Extract the JSON data from the script
    script_data = re.search(r'dataLayer\.push\(({.*?})\);', script_tag.text, re.DOTALL).group(1)
    try:
        data = json.loads(script_data)  # Load the JSON data

        return {
            'name': data.get("productName"),
            'brand': data.get("productBrand"),
            'price': data.get("productPrice")
        }

    except json.decoder.JSONDecodeError:
        # If the JSON data is not valid, return None
        return None


def grab_and_save_data_from_zalando_site(file_path):
    products_information = extract_products_information(
        file_path=file_path,
        get_product_lists_func=get_product_lists_from_zalando_site,
        get_product_details_func=get_product_details_from_zalando_site,
        chunk_size=1000
        )
    site = add_zalando_site()
    progress_bar_for_saving_data = tqdm(total=len(products_information), desc="Saving data to database")
    for product_info in products_information:
        progress_bar_for_saving_data.update(1)  # Update the progress bar
        save_product_info_to_database(product_info, site=site)


if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process the zalando crawl input file.")
    # Add the crawl_input_file argument
    parser.add_argument('zalando_crawl_input_file_path', type=str, help='Path to the crawl input file')
    # Parse the arguments
    args = parser.parse_args()
    grab_and_save_data_from_zalando_site(file_path=args.zalando_crawl_input_file_path)