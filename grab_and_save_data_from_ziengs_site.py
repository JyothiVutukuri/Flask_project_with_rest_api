import argparse

from tqdm import tqdm
from utils import get_soup_html_from_raw, extract_products_information, save_product_info_to_database, with_app_context
from models import db, Site

def get_product_lists_from_ziengs_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    product_lists = soup.select('.productList .title')
    return list({product["title"] for product in product_lists})


def get_product_details_from_ziengs_site(raw_html):
    """Get product lists from raw html"""
    soup = get_soup_html_from_raw(raw_html)
    return {
        'name': soup.find('h1', {'itemprop': 'name'}).text.strip(),
        'brand': soup.find('meta', {'itemprop': 'brand'})['content'],
        'price': soup.find('meta', {'itemprop': 'price'})['content']
    }


@with_app_context
def add_zeigns_site():
    site_name = 'zeigns'
    site = Site.query.filter_by(name=site_name.upper()).first()
    if not site:
        site = Site(name='zeigns', url='https://zeigns.nl')
        db.session.add(site)
        db.session.commit()
    return site


def grab_and_save_data_from_ziengs_site(file_path):
    products_information = extract_products_information(
        file_path=file_path,
        get_product_lists_func=get_product_lists_from_ziengs_site,
        get_product_details_func=get_product_details_from_ziengs_site,
    )
    site = add_zeigns_site()
    progress_bar_for_saving_data = tqdm(total=len(products_information), desc="Saving data to database")
    for product_info in products_information:
        progress_bar_for_saving_data.update(1)  # Update the progress bar
        save_product_info_to_database(product_info, site=site)


if __name__ == '__main__':
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process the `ziengs` crawl input file.")
    # Add the crawl_input_file argument
    parser.add_argument('ziengs_crawl_input_file_path', type=str, help='Path to the crawl input file')
    # Parse the arguments
    args = parser.parse_args()
    grab_and_save_data_from_ziengs_site(file_path=args.ziengs_crawl_input_file_path)



