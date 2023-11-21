import argparse

from tqdm import tqdm
from utils import get_soup_html_from_raw, extract_products_information, save_product_info_to_database, with_app_context
from models import db, Site


def get_product_lists_form_omoda_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    product_lists = soup.find_all('a', class_='artikel-link googleproduct')
    return list({product["title"] for product in product_lists})


def get_product_details_form_omoda_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    return {
        'name': '',
        'brand': '',
        'price': '',
    }

@with_app_context
def create_zeigns_site():
    site_name = 'omoda'
    site = Site.query.filter_by(name=site_name.upper()).first()
    if not site:
        site = Site(name=site_name, url='https://omoda.nl')
        db.session.add(site)
        db.session.commit()
    return site

def grab_and_save_data_from_omoda_site(file_path):
    products_information = extract_products_information(
        file_path=file_path,
        get_product_lists_func=get_product_lists_form_omoda_site,
        get_product_details_func=get_product_details_form_omoda_site,
    )
    site = create_zeigns_site()
    progress_bar_for_saving_data = tqdm(total=len(products_information), desc="Saving data to database")
    for product_info in products_information:
        progress_bar_for_saving_data.update(1)  # Update the progress bar
        save_product_info_to_database(product_info, site=site, progress_bar_info=progress_bar_for_saving_data)



if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process the omoda crawl input file.")
    # Add the crawl_input_file argument
    parser.add_argument('omoda_crawl_input_file_path', type=str, help='Path to the crawl input file')
    # Parse the arguments
    args = parser.parse_args()
    grab_and_save_data_from_ziengs_site(file_path=args.omoda_crawl_input_file_path)