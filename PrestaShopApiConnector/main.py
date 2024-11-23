from prestapyt import PrestaShopWebServiceDict
import json
import os
import copy
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure constants
product_file_path = "../Scrapper/scraping_results/warhammer_products.json"
API_URL = "http://localhost:8080/api"
API_KEY = "FLMGUSUKA2JS1GMSJ5UE538HMSEN25BL"

# Initialize PrestaShop API client
prestashop = PrestaShopWebServiceDict(API_URL, API_KEY)

def get_blank_schemas():
    print("Fetching blank schemas")
    category_schema = prestashop.get("categories", options={
        "schema": "blank"
    })
    product_schema = prestashop.get("products", options={
        "schema": "blank"
    })
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

def delete_all_products(batch_size=50):
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

def delete_all_categories(batch_size=50):
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
    category_data['category']['name'] = {'language': [{'attrs': {'id': '1'}, 'value': category_name}]}
    category_data['category']['description'] = {'language': [{'attrs': {'id': '1'}, 'value': f'Description for {category_name}'}]}
    category_data['category']['link_rewrite'] = {'language': [{'attrs': {'id': '1'}, 'value': category_name.lower().replace(" ", "-")}]}

    try:
        response = prestashop.add('categories', category_data)
        print(f"Category '{category_name}' created with ID: {response['prestashop']['category']['id']}")
        return response["prestashop"]['category']['id']
    except Exception as e:
        print(f"Error creating category '{category_name}': {e}")
        return None

def send_product(product_data, product_schema):
    product_data_schema = copy.deepcopy(product_schema)

    product_data_schema['product']['id_category_default'] = {'value': product_data['category_id']}
    product_data_schema['product']['active'] = '1'
    product_data_schema['product']['state'] = '1'
    product_data_schema['product']['price'] = round(float(product_data['price'])/1.23, 2)
    product_data_schema['product']['name'] = {'language': [{'attrs': {'id': '1'}, 'value': product_data['name'][:128]}]}
    product_data_schema['product']['description'] = {
        'language': [
            {
                'attrs': {'id': '1'},
                'value': (
                    f"{product_data.get('description', 'No description available.')}<br><br>"
                    f"{product_data.get('details', '')}<br><br>"
                    f"Available Sizes: {', '.join(product_data.get('sizes', ['Not specified']))}<br>"
                    f"Available Colours: {', '.join(product_data.get('colours_dropdown', ['Not specified']))}<br>"
                )
            }
        ]
    }
    product_data_schema['product']['associations']['categories'] = {'category': [{'id': product_data['category_id']}]}
    product_data_schema['product']['id_shop_default'] = '1'
    product_data_schema['product']['id_tax_rules_group'] = '1'
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

    except Exception as e:
        print(f"Error creating product '{product_data['name']}': {e}")

def main():
    delete_all_products()
    delete_all_categories()

    category_schema, product_schema = get_blank_schemas()

    del product_schema["product"]["associations"]["combinations"]
    del product_schema["product"]["position_in_category"]

    if not category_schema or not product_schema:
        print("Failed to retrieve schemas, exiting.")
        return

    if not os.path.exists(product_file_path):
        print(f"Product file not found at path: {product_file_path}")
        return

    with open(product_file_path, 'r') as file:
        parsed_data = json.load(file)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for category, sub_categories in parsed_data.items():
            if not any(sub_categories.values()):
                print(f"Main category '{category}' has no subcategories with products. Skipping.")
                continue

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
                            product['quantity'] = random.randint(0, 10)
                            futures.append(executor.submit(send_product, product, product_schema))

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing product: {e}")

if __name__ == "__main__":
    main()
