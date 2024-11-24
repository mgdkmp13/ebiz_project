import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import json
import os

# Base URL for the Warhammer merchandise website
baseUrl = 'https://merch-eur.warhammer.com'
cookies = {
    'localization': 'PL',
    'cart_currency': 'PLN',
}

# Function to extract product details from the product page
def get_info_from_product_page(product_page_url: str) -> Tuple[List[str], Optional[str], Optional[str], List[str], List[str], List[str]]:
    page = requests.get(product_page_url, cookies=cookies)
    soup = BeautifulSoup(page.content, 'html.parser')

    big_product_images = ['https:' + image_link.get('href') for image_link in soup.find_all('a', class_='c-gallery__modal')]

    product_descript_and_details = soup.find_all('div', class_='c-info-tabs__content rte')
    product_description = product_descript_and_details[0].text.strip() if len(product_descript_and_details) > 0 else None
    product_details = product_descript_and_details[1].text.strip() if len(product_descript_and_details) > 1 else None

    product_sizes = [prod_size.text.strip() for prod_size in soup.find_all('label', class_='c-product-options__swatch -is-size')]
    product_colours_button = [prod_colour.text.strip() for prod_colour in soup.find_all('label', class_='c-product-options__swatch -is-color')]

    colours_dropdown = soup.find('select', attrs={'name': 'options[Colour]'})
    product_colours_dropdown = [option.text.strip() for option in colours_dropdown.find_all('option')] if colours_dropdown else []

    return (
        big_product_images,
        product_description,
        product_details,
        product_sizes,
        product_colours_button,
        product_colours_dropdown
    )

# Function to scrape product data from a category page
def get_products_data(page_url: str) -> List[dict]:
    page = requests.get(page_url, cookies=cookies)
    soup = BeautifulSoup(page.content, 'html.parser')

    no_products_message = soup.find('p', class_='c-collections__message')

    if no_products_message:
        return []

    products = soup.find_all('article', class_='c-gallery-item')
    product_data_list = []

    for product in products:
        name_element = product.find('h2', class_='c-product-listing__title')
        price_element = product.find('span', class_='price')
        img_tags = product.find_all('img', class_='image')
        img_src = ['https:' + tag.get('data-src') for tag in img_tags if tag]
        product_page = product.find('a', class_='c-gallery-item__link').get('href')

        prod_info_from_page = get_info_from_product_page(baseUrl + product_page) if product_page else ([], None, None, [], [], [])

        if name_element and price_element:
            product_data = {
                "name": name_element.text.strip(),
                "price": price_element.text.strip().replace(' zł', '').replace(',', '.').strip(),
                "images": img_src,
                "detailed_images": prod_info_from_page[0],
                "description": prod_info_from_page[1],
                "details": prod_info_from_page[2],
                "sizes": prod_info_from_page[3],
                "colours_button": prod_info_from_page[4],
                "colours_dropdown": prod_info_from_page[5]
            }
            product_data_list.append(product_data)

    return product_data_list

# Fetch all products from a category
def fetch_all_pages_in_category(category_name: str, max_page_iters: int = 1):
    page_number = 1
    all_products = []

    while page_number <= max_page_iters:
        page_url = f"{baseUrl}/collections/{category_name}?page={page_number}"
        print(f"Fetching data from: {page_url}")
        products = get_products_data(page_url)

        if not products:
            print(f"No more products found in category '{category_name}' on page {page_number}.")
            break
        all_products.extend(products)
        page_number += 1

    print(f"Total products found in '{category_name}': {len(all_products)}")
    return all_products

# Extract categories without subcategories
def get_categories(soup):
    category_nav = soup.find('nav', class_='main-menu')
    category_buttons = category_nav.find_all('a', class_='main-menu__button')
    return [button.text.strip() for button in category_buttons]

# Extract dropdown categories
def get_dropdown_categories(soup):
    dropdown_cats_info = []
    category_with_subcategories_dropdown = soup.find_all('div', class_='main-menu__item -has-dropdown')

    for cat in category_with_subcategories_dropdown:
        main_cat = cat.find('button', class_='main-menu__button').text.strip()
        subcats = cat.find_all('a', class_='c-dropdown__link')
        subcats_names = [subcat.text.strip() for subcat in subcats]
        dropdown_cats_info.append((main_cat, subcats_names))

    return dropdown_cats_info

def save_to_json(data):
    scrapper_folder = os.path.dirname(os.path.abspath(__file__))
    results_folder = os.path.join(scrapper_folder, 'scraping_results')
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    with open(os.path.join(results_folder, 'warhammer_products.json'), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to 'scraping_results/warhammer_products.json'.")
    print(f"Absolute path: {os.path.join(results_folder, 'warhammer_products.json')}")
    
def main():
    page = requests.get(baseUrl, cookies=cookies)
    soup = BeautifulSoup(page.content, 'html.parser')

    no_subcat_cats = get_categories(soup)
    dropdown_cats_info = get_dropdown_categories(soup)

    print("Categories with no subcategories:", no_subcat_cats)
    print("\nDropdown Categories:", dropdown_cats_info)

    categorized_data = {}

    cat_url_names = {
        **{cat: [subcat.replace(' ', '-').lower() for subcat in subcats] for cat, subcats in dropdown_cats_info},
        "OTHERS": [cat.replace(' ', '-').lower() for cat in no_subcat_cats]
    }

    fetch_with_max_iters = partial(fetch_all_pages_in_category, max_page_iters=6)

    with ThreadPoolExecutor() as executor:
        for cat, subcat_urls in cat_url_names.items():
            results = executor.map(fetch_with_max_iters, subcat_urls)
            for subcat, products in zip(subcat_urls, results):
                if cat not in categorized_data:
                    categorized_data[cat] = {}
                categorized_data[cat][subcat] = products

    print(f"Categorized data structure built successfully.")
    save_to_json(categorized_data)

# Execute main function
if __name__ == "__main__":
    main()
