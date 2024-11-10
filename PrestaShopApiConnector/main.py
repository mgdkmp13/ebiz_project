import json
import requests 
from requests.auth import HTTPBasicAuth

product_file_path = "../Scrapper/warhammer_products.json"
API_URL = "http://your-prestashop-site.com/api"
API_KEY = "your_prestashop_api_key"

def get_all_ids(resource):
    response = requests.get(
        f"{API_URL}/{resource}",
        auth=HTTPBasicAuth(API_KEY, '')
    )
    if response.status_code == 200:
        data = response.json()
        return [item['id'] for item in data[resource]]
    else:
        print(f"Błąd podczas pobierania ID dla {resource}: {response.content}")
        return []

def delete_resource(resource, resource_id):
    response = requests.delete(
        f"{API_URL}/{resource}/{resource_id}",
        auth=HTTPBasicAuth(API_KEY, '')
    )
    return response

def delete_all_products():
    product_ids = get_all_ids("products")
    for product_id in product_ids:
        response = delete_resource("products", product_id)
        if response.status_code == 200:
            print(f"Produkt {product_id} został usunięty.")
        else:
            print(f"Błąd podczas usuwania produktu {product_id}: {response.content}")

def delete_all_categories():
    category_ids = get_all_ids("categories")
    for category_id in category_ids:
        if int(category_id) != 2:  # Pomiń główną kategorię
            response = delete_resource("categories", category_id)
            if response.status_code == 200:
                print(f"Kategoria {category_id} została usunięta.")
            else:
                print(f"Błąd podczas usuwania kategorii {category_id}: {response.content}")

def send_category(category, category_id):
    category_xml = f"""
    <prestashop>
        <category>
            <id_parent>{category_id}</id_parent>
            <active>1</active>
            <name>
                <language id="1">{category_name}</language>
            </name>
            <description>
                <language id="1">Description for {category_name}</language>
            </description>
            <link_rewrite>
                <language id="1">{category_name.lower().replace(" ", "-")}</language>
            </link_rewrite>
        </category>
    </prestashop>
    """

    headers = {'Content-Type': 'application/xml', 'Output-Format': 'JSON'}
    response = requests.post(
        f"{API_URL}/categories",
        data=category_xml,
        headers=headers,
        auth=HTTPBasicAuth(API_KEY, '')
    )
    return response

def main():
    delete_all_products()
    delete_all_categories()

    with open(product_file_path, 'r') as file:
        parsed_data = json.load(file)

    category_to_idx = {}
    for idx, category in enumerate(parsed_data.keys(), 1):
        category_to_idx[category] = idx
        res = send_category(category, idx)

        if res.status_code == 201:
            print(f"Category {category} created successfully")
        else:
            print(f"Error creating category {category}: {res.text}")

if __name__ == "__main__":
    main()