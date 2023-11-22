import argparse
import json

from tqdm import tqdm
from utils import get_soup_html_from_raw, extract_products_information, save_product_info_to_database, with_app_context
from models import db, Site


@with_app_context
def add_omoda_site():
    site_name = 'omoda'
    site = Site.query.filter_by(name=site_name.upper()).first()
    if not site:
        site = Site(name=site_name, url='https://omoda.nl')
        db.session.add(site)
        db.session.commit()
    return site

def get_product_lists_from_omoda_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    product_lists = soup.find_all('a', class_='artikel-link googleproduct')
    return list({product["title"] for product in product_lists})


def get_product_details_from_omoda_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    product_string = soup.find('main').get('data-google')
    if not product_string:
        return # Skip if the product does not have data-google attribute as it is not a product page
    product = json.loads(soup.find('main')['data-google'])

    return {
        'name': product['name'],
        'brand': product['brand'],
        'price': product['price'],
    }


def grab_and_save_data_from_omoda_site(file_path):
    products_information = extract_products_information(
        file_path=file_path,
        get_product_lists_func=get_product_lists_from_omoda_site,
        get_product_details_func=get_product_details_from_omoda_site,
    )
    site = add_omoda_site()
    progress_bar_for_saving_data = tqdm(total=len(products_information), desc="Saving data to database")
    for product_info in products_information:
        progress_bar_for_saving_data.update(1)  # Update the progress bar
        save_product_info_to_database(product_info, site=site)



if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process the omoda crawl input file.")
    # Add the crawl_input_file argument
    parser.add_argument('omoda_crawl_input_file_path', type=str, help='Path to the crawl input file')
    # Parse the arguments
    args = parser.parse_args()
    grab_and_save_data_from_omoda_site(file_path=args.omoda_crawl_input_file_path)