import requests
from bs4 import BeautifulSoup
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from functools import partial

# Base URL for the Warhammer merchandise website
baseUrl = 'https://merch-eur.warhammer.com'


# Function to retrieve product data (name, price, image sources) from a category page
def get_products_data(page_url: str) -> List[Tuple[str, str, List[str]]]:
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    no_products_message = soup.find('p', class_='c-collections__message')

    if no_products_message:
      return None

    products = soup.find_all('article', class_='c-gallery-item')
    product_descripts, product_prices, product_img_src = [], [], []

    for product in products:
        desc = product.find('h2', class_='c-product-listing__title')
        price = product.find('span', class_='price')
        img_tags = product.find_all('img', class_='image')
        img_src = [tag.get('data-src') for tag in img_tags if tag]

        if desc and price:
            product_descripts.append(desc.text.strip())
            product_prices.append(price.text.strip())
            product_img_src.append(img_src)

    return list(zip(product_descripts, product_prices, product_img_src))

def fetch_all_pages_in_category(category_name: str, max_page_iters: int):
    page_number = 1
    all_products = []

    while page_number <= max_page_iters:
        page_url = f"{baseUrl}/collections/{category_name}?page={page_number}"
        print(f"Fetching data from: {page_url}")
        products = get_products_data(page_url)


        if products is None:
            print(f"No more products found in category '{category_name}' on page {page_number}.")
            break

        all_products.extend(products)
        page_number += 1

    print(f"Total products found in '{category_name}': {len(all_products)}")
    return all_products


def get_categories(soup):
    # Finding categories without subcategories
    category_nav = soup.find('nav', class_='main-menu')
    category_buttons = category_nav.find_all('a', class_='main-menu__button')
    category_no_subcategories = [button.text.strip() for button in category_buttons]

    return category_no_subcategories


def get_dropdown_categories(soup):
    dropdown_cats_info = []
    category_with_subcategories_dropdown = soup.find_all('div', class_='main-menu__item -has-dropdown')

    for cat in category_with_subcategories_dropdown:
        main_cat = cat.find('button', class_='main-menu__button').text.strip()
        subcats = cat.find_all('a', class_='c-dropdown__link')
        subcats_names = [subcat.text.strip() for subcat in subcats]
        dropdown_cats_info.append((main_cat, subcats_names))

    return dropdown_cats_info


def get_mega_panel_categories(soup):
    mega_cats_info = []
    category_with_subcategories_mega = soup.find_all('div', class_='main-menu__item -has-mega-panel')

    for cat in category_with_subcategories_mega:
        main_cat = cat.find('button', class_='main-menu__button').text.strip()
        subcats_info = []

        for subcat in cat.find_all("div", class_="c-mega-image-panel__menu"):
            subcat_name = subcat.find("span", class_="title").text.strip()
            sub_sub_cats_info = [
                (
                    sub_sub_cat.find("h3", class_="title").text.strip(),
                    sub_sub_cat.find("img", class_="image").get("src")
                )
                for sub_sub_cat in subcat.find_all("li")
            ]
            subcats_info.append((subcat_name, sub_sub_cats_info))

        mega_cats_info.append((main_cat, subcats_info))

    return mega_cats_info


def get_regular_cats_urls(soup):
    regular_categories = soup.find_all('a', class_='main-menu__button')

    urls = []

    for category in regular_categories:
        url = category.get('href')
        if url:
            full_url = baseUrl + url
            urls.append(full_url)

    return urls


def get_urls_of_subcategories(soup, main_category_name: str) -> List[str]:
    dropdown_categories = soup.find_all('div', class_='main-menu__item -has-dropdown')
    urls = []

    for category in dropdown_categories:
        category_button = category.find('button', class_='main-menu__button')

        if category_button and category_button.text.strip() == main_category_name:
            subcategories = category.find_all('a', class_='c-dropdown__link')

            for subcat in subcategories:
                subcat_url = subcat.get('href')
                if subcat_url:
                    full_url = baseUrl + subcat_url
                    urls.append(full_url)
            break

    return urls


def get_urls_subcategories_mega(soup):
    urls = []

    # Find major categories in the mega panel
    mega_major_cats = soup.find_all('h2', class_='c-mega-image-panel__menu--title -js-pos-ref')

    # Extract links within major categories
    for major_cat in mega_major_cats:
        link_tag = major_cat.find('a')
        if link_tag:
            url = link_tag.get('href')
            if url:
                full_url = baseUrl + url
                urls.append(full_url)

    # Find subcategory items within the mega panel
    mega_categories = soup.find_all('li', class_='c-mega-image-panel__submenu--item')

    # Extract links within subcategories
    for category in mega_categories:
        link_tag = category.find('a')
        if link_tag:
            url = link_tag.get('href')
            if url:
                full_url = baseUrl + url
                urls.append(full_url)

    return urls


# Main scraping function to get category structure and product data
def main():
    page = requests.get(baseUrl)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get category information
    no_subcat_cats = get_categories(soup)
    dropdown_cats_info = get_dropdown_categories(soup)
    #mega_cats_info = get_mega_panel_categories(soup)

    print("Categories with no subcategories:", no_subcat_cats)
    print("\nDropdown Categories:", dropdown_cats_info)
    #print("\nMega Panel Categories:", mega_cats_info)

    non_drop_urls = get_regular_cats_urls(soup)
    drop_urls_product = get_urls_of_subcategories(soup, "SHOP BY PRODUCT")
    drop_urls_brand = get_urls_of_subcategories(soup, "SHOP BY BRAND")
    #mega_urls = get_urls_subcategories_mega(soup)

    print("\nRegular Categories URLs:", non_drop_urls)
    print("\nProduct Subcategories URLs:", drop_urls_product)
    print("\nBrand Subcategories URLs:", drop_urls_brand)
    #print("\nMega Panel Subcategories URLs:", mega_urls)

    # Prepare to fetch product data for dropdown categories
    cat_url_names = [subcat.replace(' ', '-').lower() for cat in dropdown_cats_info for subcat in cat[1]]
    all_cats_prod_info = []

    fetch_with_max_iters = partial(fetch_all_pages_in_category, max_page_iters=1)

    # Fetch product data for dropdown categories
    with ThreadPoolExecutor() as executor:
      results = executor.map(fetch_with_max_iters, cat_url_names)

      for cat, prod_info in zip(cat_url_names, results):
        all_cats_prod_info.append((cat, prod_info))


    # Uncomment the next line to see all products info
    counter = 0
    for cat in all_cats_prod_info:
        counter += len(cat[1])
    print(counter)
    print(no_subcat_cats)
    print(dropdown_cats_info)


# Execute main function
if __name__ == "__main__":
    main()
