from prestapyt import PrestaShopWebServiceDict
import json
import os
import copy
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

product_file_path = "../Scrapper/scraping_results/warhammer_products.json"
API_URL = "http://localhost:8080/api"
API_KEY = "FLMGUSUKA2JS1GMSJ5UE538HMSEN25BL"

prestashop = PrestaShopWebServiceDict(API_URL, API_KEY)

def get_blank_schemas():
    print("Fetching blank schemas")
    category_schema = prestashop.get("categories", options={
        "schema": "blank"
    })
    product_schema = prestashop.get("products", options={
        "schema": "blank"
    })

    del product_schema["product"]["associations"]["combinations"]
    del product_schema["product"]["position_in_category"]
    
    return category_schema, product_schema

def get_category_ids():
    print("Fetching category IDs")
    resources = prestashop.get("categories")

    if 'category' not in resources["categories"]:
        return []

    return [item["attrs"]['id'] for item in resources["categories"]["category"]]

def get_product_ids():
    print("Fetching product IDs")
    resources = prestashop.get("products")

    if 'product' not in resources["products"]:
        return []

    return [item["attrs"]['id'] for item in resources["products"]["product"]]

def delete_product_batch(batch_ids):
    try:
        prestashop.delete("products", resource_ids=batch_ids)
        print(f"Deleted batch of products: {batch_ids}")
    except Exception as e:
        print(f"Error deleting batch: {batch_ids}, Error: {e}")

def delete_all_products(batch_size=100):
    print("Deleting all products")
    product_ids = get_product_ids()

    if not product_ids:
        print("No products to delete.")
        return

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        # Submit delete tasks to the executor
        for i in range(0, len(product_ids), batch_size):
            batch_ids = product_ids[i:i + batch_size]
            futures.append(executor.submit(delete_product_batch, batch_ids))

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing batch deletion: {e}")

def delete_category_batch(batch_ids):
    try:
        prestashop.delete("categories", resource_ids=batch_ids)
        print(f"Deleted batch of categories: {batch_ids}")
    except Exception as e:
        print(f"Error deleting batch: {batch_ids}, Error: {e}")

def delete_all_categories(batch_size=100):
    print("Deleting all categories")
    category_ids = get_category_ids()
    ids_to_delete = [id for id in category_ids if id != '1' and id != '2']

    if not ids_to_delete:
        print("No categories to delete.")
        return

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        # Submit delete tasks to the executor
        for i in range(0, len(ids_to_delete), batch_size):
            batch_ids = ids_to_delete[i:i + batch_size]
            futures.append(executor.submit(delete_category_batch, batch_ids))

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing batch deletion: {e}")

def send_category(category_name, category_schema, parent_id='2'):
    category_data = copy.deepcopy(category_schema)

    category_data['category']['id_parent'] = parent_id
    category_data['category']['active'] = '1'
    category_data['category']['id_shop_default'] = '1'
    category_data['category']['name'] = {
        'language': [
            {'attrs': {'id': '1'}, 'value': category_name},  
            {'attrs': {'id': '2'}, 'value': category_name},  
            {'attrs': {'id': '3'}, 'value': category_name}   
        ]
    }

    category_data['category']['description'] = {
        'language': [
            {'attrs': {'id': '1'}, 'value': f''}, 
            {'attrs': {'id': '2'}, 'value': f''}, 
            {'attrs': {'id': '3'}, 'value': f''}  
        ]
    }

    category_data['category']['link_rewrite'] = {
        'language': [
            {'attrs': {'id': '1'}, 'value': ''}, 
            {'attrs': {'id': '2'}, 'value': ''}, 
            {'attrs': {'id': '3'}, 'value': ''}  
        ]
    }

    try:
        response = prestashop.add('categories', category_data)
        print(f"Category '{category_name}' created with ID: {response['prestashop']['category']['id']}")
        return response["prestashop"]['category']['id']
    except Exception as e:
        print(f"Error creating category '{category_name}': {e}")
        return None

def send_product(product_data, product_schema):
    product_data_schema = copy.deepcopy(product_schema)
    product_data['quantity'] = random.randint(0, 10)
    product_data_schema['product']['id_category_default'] = {'value': product_data['category_id']}
    product_data_schema['product']['active'] = '1'
    product_data_schema['product']['state'] = '1'
    product_data_schema['product']['price'] = round(float(product_data['price'])/1.23, 2)
    product_data_schema['product']['name'] = {
        'language': [
            {'attrs': {'id': '1'}, 'value': product_data['name'][:128]}, 
            {'attrs': {'id': '2'}, 'value': product_data['name'][:128]}, 
            {'attrs': {'id': '3'}, 'value': product_data['name'][:128]}  
        ]
    }
    product_data_schema['product']['description'] = {
        'language': [
            {
                'attrs': {'id': '1'},
                'value': (
                    f"{product_data.get('description', '')}<br><br>"
                    f"{product_data.get('details', '')}<br><br>"
                )
            },
            {
                'attrs': {'id': '2'},
                'value': (
                    f"{product_data.get('description', '')}<br><br>"
                    f"{product_data.get('details', '')}<br><br>"
                )
            },
            {
                'attrs': {'id': '3'},
                'value': (
                    f"{product_data.get('description', '')}<br><br>"
                    f"{product_data.get('details', '')}<br><br>"
                )
            }
        ]
    }
    product_data_schema['product']['associations']['categories'] = {'category': [{'id': product_data['category_id']}]}
    product_data_schema['product']['id_shop_default'] = '1'
    product_data_schema['product']['id_tax_rules_group'] = '2'
    product_data_schema['product']['available_for_order'] = '1'
    product_data_schema['product']['minimal_quantity'] = '1'
    product_data_schema['product']['show_price'] = '1'

    try:
        response = prestashop.add('products', product_data_schema)
        print(f"Product '{product_data['name']}' created successfully.")
        product_id = response["prestashop"]['product']['id']

        available_id = prestashop.search('stock_availables', options={'filter[id_product]': product_id})[0]
        stock_available_schema = prestashop.get('stock_availables', available_id)
        stock_available_schema['stock_available']['quantity'] = product_data['quantity']
        prestashop.edit('stock_availables', stock_available_schema)

        print(f"Stock for product '{product_data['name']}' updated to {product_data['quantity']}")

        for image_url in product_data["detailed_images"]:
            upload_image_to_prestashop(image_url, product_id)

    except Exception as e:
        print(f"Error creating product '{product_data['name']}': {e}")

def download_image(image_url: str) -> bytes:
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania obrazu: {e}")
        return None

def upload_image_to_prestashop(image_url: str, product_id: str):
    image_content = download_image(image_url)
    
    if image_content:
        image_name = image_url.split('/')[-1].split('?')[0]
        try:
            prestashop.add(f"images/products/{product_id}", files=[("image", image_name, image_content)])
            print(f"Obraz {image_name} został pomyślnie przesłany dla produktu {product_id}.")
        except Exception as e:
            print(f"Nie udało się przesłać obrazu: {e}")
    else:
        print("Nie udało się pobrać obrazu.")

def main():
    delete_all_products()
    delete_all_categories()

    shop_by_faction = "SHOP BY FACTION"
    shop_by_product = "SHOP BY PRODUCT"
    shop_by_brand = "SHOP BY BRAND"
    others = "OTHERS"

    category_schema, product_schema = get_blank_schemas()

    if not category_schema or not product_schema:
        print("Failed to retrieve schemas, exiting.")
        return

    if not os.path.exists(product_file_path):
        print(f"Product file not found at path: {product_file_path}")
        return

    with open(product_file_path, 'r') as file:
        parsed_data = json.load(file)

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []

        for category, sub_categories in parsed_data.items():
            if category == shop_by_faction:
                continue
            if not any(sub_categories.values()):
                print(f"Main category '{category}' has no subcategories with products. Skipping.")
                continue

            if category != others:
                category_id = send_category(category, category_schema)
                if category_id:
                    for sub_category, products in sub_categories.items():
                        if not products:
                            print(f"Subcategory '{sub_category}' under '{category}' has no products. Skipping.")
                            continue
                        
                        sub_category_id = send_category(sub_category, category_schema, category_id)
                        if sub_category_id:
                            for product in products:
                                product['category_id'] = sub_category_id
                                futures.append(executor.submit(send_product, product, product_schema))
            else:
                for sub_category, products in sub_categories.items():
                    if not products:
                        print(f"Subcategory '{sub_category}' under '{category}' has no products. Skipping.")
                        continue
                        
                    sub_category_id = send_category(sub_category, category_schema)
                    if sub_category_id:
                        for product in products:
                            product['category_id'] = sub_category_id
                            futures.append(executor.submit(send_product, product, product_schema))

        if shop_by_faction in parsed_data:
            faction_data = parsed_data[shop_by_faction]
            faction_category_id = send_category(shop_by_faction, category_schema)
            
            if faction_category_id:
                for faction_name, faction_sub_categories in faction_data.items():
                    if not any(faction_sub_categories):
                        print(f"Faction '{faction_name}' has no subcategories with products. Skipping.")
                        continue
                    
                    faction_sub_category_id = send_category(faction_name, category_schema, faction_category_id)
                    if faction_sub_category_id:
                        for faction_sub_category in faction_sub_categories:
                            faction_sub_category_name = list(faction_sub_category.keys())[0]
                            faction_sub_category_products = faction_sub_category[faction_sub_category_name]['products']
                            
                            sub_category_id = send_category(faction_sub_category_name, category_schema, faction_sub_category_id)
                            if sub_category_id:
                                for product in faction_sub_category_products:
                                    product['category_id'] = sub_category_id
                                    futures.append(executor.submit(send_product, product, product_schema))

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing product: {e}")

if __name__ == "__main__":
    main()
